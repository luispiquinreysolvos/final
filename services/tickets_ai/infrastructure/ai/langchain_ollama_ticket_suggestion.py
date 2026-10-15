import asyncio
import base64
import logging
import os
import time
from typing import List

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

from application.dtos.suggest_ticket_response import SuggestTicketResponse
from application.interfaces.ticket_suggestion_service import TicketSuggestionService
from domain.value_objects.ticket_images import TicketImages
from presentation.schemas.suggest_ticket_http_response import SuggestTicketHttpResponse

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are an expert IT Support and Helpdesk AI assistant.

Your task is to analyze a user's issue report and generate
structured data for a ticket suggestion.

FIELD SPECIFICATIONS:

- title:
  Create a concise and professional title summarizing the main issue.
  Prefer between 5 and 10 words.

- description:
  Generate a comprehensive, detailed, and highly explanatory
  description of the reported issue.

  The description should be as long and informative as possible,
  making full use of all relevant information provided by the user.

  Clearly explain the problem, observed symptoms, affected systems,
  impacted users, operational consequences, error messages,
  circumstances, and any other relevant technical or business context.

  Organize the information into coherent, well-structured paragraphs
  using clear and professional technical language.

  Expand upon the user's report to improve clarity, readability,
  and technical precision, while preserving its original meaning.

  Do not summarize excessively or omit potentially useful details.
  Prioritize completeness, accuracy, and explanatory depth over brevity.

  Never fabricate technical details, causes, error messages,
  troubleshooting steps, or circumstances that were not provided
  or cannot be reasonably inferred from the user's report.

  If the available information is limited, explain everything
  that is known without artificially extending the description
  through repetition or speculation.

- category:
  Categorize the issue based on the nature of the problem and its impact on the business or users.

- priority:
  Use the Odoo Helpdesk priority convention:

  "0" = Low
  Minor issue, general question, cosmetic problem,
  or low-impact request.

  "1" = Medium
  Standard issue affecting normal work but without
  significant operational impact.

  "2" = High
  Important functionality is unavailable or multiple
  users are affected.

  "3" = Very High
  Critical service outage or severe business impact.

- tags:
  Generate between 2 and 5 concise lowercase keywords.
  Tags should describe the technologies, systems,
  components, or issue types involved.

IMPORTANT RULES:

- Do not invent information that is not present or
  reasonably inferable from the user's report.
- Always respect the priority values exactly.
- Keep tags concise and lowercase.
"""

TICKET_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        (
            "human",
            (
                "The main production database is completely "
                "unresponsive and customers cannot complete "
                "purchases in the store!"
            ),
        ),
        (
            "ai",
            """{{
    "title": "Production Database Down",
    "description": "The production database is unresponsive, preventing customers from completing purchases in the online store.",
    "category": "Technical",
    "priority": "3",
    "tags": ["database", "production", "outage", "checkout"]
}}""",
        ),
        (
            "human",
            (
                "Hi, I forgot my email password and I'm "
                "locked out of Outlook on my laptop."
            ),
        ),
        (
            "ai",
            """{{
    "title": "Outlook Account Lockout",
    "description": "The user cannot access Outlook because they forgot their email credentials.",
    "category": "Technical",
    "priority": "1",
    "tags": ["email", "outlook", "password-reset", "authentication"]
}}""",
        ),
        MessagesPlaceholder("user_report"),
    ]
)


async def _safe_invoke(chain, payload: dict, max_retries: int = 2):
    retries = 0
    while retries <= max_retries:
        try:
            return await chain.ainvoke(payload)
        except (KeyError, ValueError, TypeError):
            raise
        except Exception as e:
            retries += 1
            if retries > max_retries:
                logger.error(
                    "LLM invocation failed after %d retries: %s",
                    max_retries,
                    e,
                    extra={
                        "retries": max_retries,
                        "payload_keys": list(payload.keys()),
                    },
                )
                raise

            wait_time = 2 * retries
            logger.warning(
                "LLM invocation failed (attempt %d/%d), retrying in %ds: %s",
                retries,
                max_retries,
                wait_time,
                e,
                extra={
                    "attempt": retries,
                    "max_retries": max_retries,
                    "wait_time": wait_time,
                },
            )
            await asyncio.sleep(wait_time)


def _parse_float_env(key: str, default: float) -> float:
    val = os.getenv(key)
    return float(val) if val is not None else default


def _parse_int_env(key: str, default: int) -> int:
    val = os.getenv(key)
    return int(val) if val is not None else default


def _parse_stop_env(key: str) -> List[str] | None:
    val = os.getenv(key)
    if not val:
        return None
    return [s.strip() for s in val.split(",") if s.strip()]


class LangChainOllamaTicketSuggestionService(TicketSuggestionService):
    def __init__(
        self,
        host: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        top_k: int | None = None,
        top_p: float | None = None,
        max_tokens: int | None = None,
        presence_penalty: float | None = None,
        frequency_penalty: float | None = None,
        stop: List[str] | None = None,
        reasoning_effort: str | None = None,
        num_gpu: int | None = None,
        num_thread: int | None = None,
        max_retries: int = 2,
    ) -> None:
        self.host = host if host is not None else os.getenv(
            "OLLAMA_HOST", "http://localhost:11434"
        )
        self.model = model if model is not None else os.getenv(
            "OLLAMA_MODEL", "llama3.1"
        )

        self.temperature = temperature if temperature is not None else _parse_float_env(
            "OLLAMA_TEMPERATURE", 0.1
        )
        self.top_k = top_k if top_k is not None else _parse_int_env(
            "OLLAMA_TOP_K", 40
        )
        self.top_p = top_p if top_p is not None else _parse_float_env(
            "OLLAMA_TOP_P", 0.9
        )
        self.max_tokens = max_tokens if max_tokens is not None else _parse_int_env(
            "OLLAMA_MAX_TOKENS", 2048
        )

        self.presence_penalty = (
            presence_penalty
            if presence_penalty is not None
            else _parse_float_env("OLLAMA_PRESENCE_PENALTY", 0.0)
        )
        self.frequency_penalty = (
            frequency_penalty
            if frequency_penalty is not None
            else _parse_float_env("OLLAMA_FREQUENCY_PENALTY", 0.0)
        )

        self.stop = stop if stop is not None else _parse_stop_env("OLLAMA_STOP")

        self.reasoning_effort = (
            reasoning_effort
            if reasoning_effort is not None
            else os.getenv("OLLAMA_REASONING_EFFORT")
        )

        self.num_gpu = num_gpu if num_gpu is not None else _parse_int_env(
            "OLLAMA_NUM_GPU", 1
        )
        self.num_thread = num_thread if num_thread is not None else _parse_int_env(
            "OLLAMA_NUM_THREAD", 4
        )

        self.max_retries = max_retries

        self.llm = ChatOllama(
            base_url=self.host,
            model=self.model,
            temperature=self.temperature,
            top_k=self.top_k,
            top_p=self.top_p,
            num_predict=self.max_tokens,
            repeat_penalty=1.0 + self.presence_penalty,
            stop=self.stop,
            num_gpu=self.num_gpu,
            num_thread=self.num_thread,
            reasoning=False
        )

        logger.info(
            "Initialized Ollama service: model=%s, host=%s, temperature=%.2f, top_k=%d, top_p=%.2f, max_tokens=%d, num_gpu=%d, num_thread=%d, max_retries=%d",
            self.model,
            self.host,
            self.temperature,
            self.top_k,
            self.top_p,
            self.max_tokens,
            self.num_gpu,
            self.num_thread,
            self.max_retries,
        )

        self.chain = TICKET_PROMPT | self.llm.with_structured_output(
            SuggestTicketHttpResponse
        )

    async def suggest_ticket(self, description: str, images: TicketImages | None = None) -> SuggestTicketResponse:
        if not description or not description.strip():
            logger.warning("Empty description provided for ticket suggestion")
            raise ValueError("Description cannot be empty.")

        logger.info(
            "Generating ticket suggestion",
            extra={
                "description_length": len(description),
                "model": self.model,
            },
        )

        content: list[dict] = [{"type": "text", "text": f"User report:\n{description.strip()}"}]
        if images is not None:
            for image in images.images:
                encoded = base64.b64encode(image.content).decode("ascii")
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:{image.content_type};base64,{encoded}"},
                })
        payload = {"user_report": [HumanMessage(content=content)]}

        start_time = time.perf_counter()

        schema_response: SuggestTicketHttpResponse = await _safe_invoke(
            self.chain,
            payload,
            max_retries=self.max_retries,
        )

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        logger.info(
            "Ticket suggestion generated successfully",
            extra={
                "title": schema_response.title,
                "priority": schema_response.priority,
                "tags_count": len(schema_response.tags),
                "elapsed_ms": round(elapsed_ms, 2),
            },
        )

        return SuggestTicketResponse(
            title=schema_response.title,
            description=schema_response.description,
            category=schema_response.category,
            priority=schema_response.priority,
            tags=schema_response.tags,
        )
