"""Shared pytest fixtures: one in-memory SQLite database per test (no files, Windows-safe).

StaticPool keeps a single connection so every session (and every thread served by the
TestClient) sees the same in-memory database; check_same_thread=False allows that sharing.
"""
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture()
def engine():
    eng = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(eng)
    yield eng
    eng.dispose()


@pytest.fixture()
def session_factory(engine):
    return sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture()
def db(session_factory):
    """A plain session for tests that touch the models directly (no HTTP)."""
    with session_factory() as s:
        yield s


@pytest.fixture()
def client(session_factory):
    """TestClient whose get_db dependency is bound to the per-test in-memory database."""

    def override():
        s = session_factory()
        try:
            yield s
        finally:
            s.close()

    app.dependency_overrides[get_db] = override
    yield TestClient(app)
    app.dependency_overrides.clear()
