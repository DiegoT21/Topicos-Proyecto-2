"""Dedicated no-double-booking suite (issue #6). Covers CA-02, CA-03, CA-04, RN-01, RN-02, RN-07.

Uses a temporary on-disk SQLite file (tmp_path) with the default pool, so every thread gets its
own connection. That is closer to production than a shared in-memory connection and lets the
concurrency test exercise the real check-then-insert race.
"""
import sys
import threading
from datetime import datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import models  # noqa: E402
from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402


def t(h, m=0):
    return datetime(2099, 1, 5, h, m).isoformat()  # far future: never "past"


@pytest.fixture()
def env(tmp_path):
    engine = create_engine(
        f"sqlite:///{tmp_path / 'double_booking.db'}", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    def override():
        s = Session()
        try:
            yield s
        finally:
            s.close()

    app.dependency_overrides[get_db] = override
    s = Session()
    math = models.Subject(name="Cálculo I")
    ana = models.Tutor(name="Ana", email="ana@utp.ac.pa", subjects=[math])
    bea = models.Tutor(name="Bea", email="bea@utp.ac.pa", subjects=[math])
    s.add_all([math, ana, bea])
    s.commit()
    for tutor in (ana, bea):  # both available 9:00-13:00
        s.add(models.Availability(tutor_id=tutor.id, start_at=datetime(2099, 1, 5, 9), end_at=datetime(2099, 1, 5, 13)))
    s.commit()
    ids = {"math": math.id, "ana": ana.id, "bea": bea.id}
    s.close()
    yield TestClient(app), Session, ids
    app.dependency_overrides.clear()
    engine.dispose()


def register(client, name, email):
    r = client.post("/api/students", json={"name": name, "email": email})
    assert r.status_code == 201
    return r.json()["token"]


def book(client, token, tutor, subject, start):
    return client.post(
        "/api/bookings",
        headers={"X-Student-Token": token},
        json={"tutor_id": tutor, "subject_id": subject, "start_at": start},
    )


def count_active(Session, tutor_id, start):
    with Session() as s:
        return (
            s.query(models.Booking)
            .filter(models.Booking.tutor_id == tutor_id, models.Booking.start_at == datetime.fromisoformat(start),
                    models.Booking.status != "cancelada")
            .count()
        )


def test_mismo_tutor_mismo_horario_409(env):  # CA-02, RN-01
    c, _, i = env
    a, b = register(c, "Luis", "luis@utp.ac.pa"), register(c, "Eva", "eva@utp.ac.pa")
    assert book(c, a, i["ana"], i["math"], t(10)).status_code == 201
    r = book(c, b, i["ana"], i["math"], t(10))
    assert r.status_code == 409 and r.json()["detail"]["code"] == "tutor_conflict"


def test_mismo_tutor_solape_parcial_409(env):  # CA-02, RN-01: 10:30 overlaps the 10:00-11:00 session
    c, _, i = env
    a, b = register(c, "Luis", "luis@utp.ac.pa"), register(c, "Eva", "eva@utp.ac.pa")
    assert book(c, a, i["ana"], i["math"], t(10)).status_code == 201
    r = book(c, b, i["ana"], i["math"], t(10, 30))
    assert r.status_code == 409 and r.json()["detail"]["code"] == "tutor_conflict"


def test_sesiones_consecutivas_permitidas(env):  # CA-03: [10,11) and [11,12) do not overlap
    c, _, i = env
    a, b = register(c, "Luis", "luis@utp.ac.pa"), register(c, "Eva", "eva@utp.ac.pa")
    assert book(c, a, i["ana"], i["math"], t(10)).status_code == 201
    assert book(c, b, i["ana"], i["math"], t(11)).status_code == 201


def test_mismo_estudiante_dos_tutores_misma_hora_409(env):  # CA-04, RN-02
    c, _, i = env
    a = register(c, "Luis", "luis@utp.ac.pa")
    assert book(c, a, i["ana"], i["math"], t(10)).status_code == 201
    r = book(c, a, i["bea"], i["math"], t(10))
    assert r.status_code == 409 and r.json()["detail"]["code"] == "student_conflict"


def test_reserva_cancelada_no_bloquea_el_espacio(env):  # RN-07
    c, _, i = env
    a, b = register(c, "Luis", "luis@utp.ac.pa"), register(c, "Eva", "eva@utp.ac.pa")
    first = book(c, a, i["ana"], i["math"], t(10))
    assert first.status_code == 201
    cancel = c.post(f"/api/bookings/{first.json()['id']}/cancel", headers={"X-Student-Token": a})
    assert cancel.status_code == 200
    assert book(c, b, i["ana"], i["math"], t(10)).status_code == 201  # same tutor, same slot, now free
    assert book(c, a, i["bea"], i["math"], t(10)).status_code == 201  # the cancelled student is free too


def test_dos_reservas_simultaneas_mismo_espacio_solo_una_gana(env):  # the Project 1 race
    c, Session, i = env
    tokens = [register(c, f"Est{n}", f"est{n}@utp.ac.pa") for n in range(8)]
    barrier = threading.Barrier(len(tokens))
    statuses = []
    errors = []

    def worker(token):
        try:
            barrier.wait(timeout=10)
            statuses.append(book(c, token, i["ana"], i["math"], t(10)).status_code)
        except Exception as e:  # surface thread failures instead of hiding them
            errors.append(repr(e))

    threads = [threading.Thread(target=worker, args=(tok,)) for tok in tokens]
    for th in threads:
        th.start()
    for th in threads:
        th.join(timeout=30)

    assert not errors, errors
    assert sorted(statuses) == [201] + [409] * (len(tokens) - 1), statuses
    assert count_active(Session, i["ana"], t(10)) == 1
