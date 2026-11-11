from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import models  # noqa: F401  (registra las tablas)
from .database import Base, engine
from .routers import bookings


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="TutoríasUTP", lifespan=lifespan)
app.include_router(bookings.router)


@app.get("/health")
def health():
    return {"status": "ok"}
