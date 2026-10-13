import logging
import sys
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI

from infrastructure.composition import create_application
from infrastructure.http.routes import router as tickets_router

load_dotenv()

# Configure logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    stream=sys.stdout,
)

# Reduce noise from third-party loggers
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("ollama").setLevel(logging.WARNING)
logging.getLogger("langchain").setLevel(logging.INFO)
logging.getLogger("langchain_ollama").setLevel(logging.INFO)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    app.state.container = create_application()
    logger.info("Application started successfully")
    yield
    logger.info("Shutting down application...")


app = FastAPI(title="Solvos", lifespan=lifespan)
app.include_router(tickets_router)


@app.get("/health")
def health():
    return {"status": "ok"}