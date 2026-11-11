from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import models  # noqa: F401  (registra las tablas)
from .database import Base, engine
from .routers import admin, bookings, catalog, tutor


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="TutoríasUTP", lifespan=lifespan)
app.include_router(bookings.router)
app.include_router(catalog.router)
app.include_router(admin.router)
app.include_router(tutor.router)


@app.get("/health")
def health():
    return {"status": "ok"}
