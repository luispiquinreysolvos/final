from pydantic import BaseModel, Field


class SuggestTicketHttpResponse(BaseModel):
    title: str = Field(..., description="Concise professional title, 5-10 words")
    description: str = Field(..., description="Clear description of the issue")
    priority: str = Field(..., description="Odoo priority: 0=Low, 1=Medium, 2=High, 3=Very High")
    tags: tuple[str, ...] = Field(default_factory=tuple, description="2-5 lowercase keywords")