from contextlib import asynccontextmanager
from fastapi import FastAPI

from infrastructure.composition import create_application
from infrastructure.http.routes import router as tickets_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.container = create_application()
    yield


app = FastAPI(title="Solvos", lifespan=lifespan)
app.include_router(tickets_router)

