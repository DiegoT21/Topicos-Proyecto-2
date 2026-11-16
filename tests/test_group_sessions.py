"""Cambio de especificación 2026-11-16: sesiones grupales con cupo (RN-01 reformulada, RN-13).

Cubre CA-23 a CA-28. Usa un archivo SQLite temporal (como test_double_booking.py) para que la
prueba de concurrencia tenga una conexión por hilo.
"""
import threading
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.database import Base, get_db
from app.main import app


def t(h):
    return datetime(2099, 1, 5, h).isoformat()


@pytest.fixture()
def env(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'group.db'}", connect_args={"check_same_thread": False})
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
    calc, fis = models.Subject(name="Cálculo I"), models.Subject(name="Física")
    ana = models.Tutor(name="Ana", email="ana@utp.ac.pa", subjects=[calc, fis])
    s.add_all([calc, fis, ana])
    s.commit()
    # 9:00-11:00 grupal con cupo 3; 11:00-12:00 individual (cupo por defecto)
    s.add(models.Availability(tutor_id=ana.id, start_at=datetime(2099, 1, 5, 9), end_at=datetime(2099, 1, 5, 11), capacity=3))
    s.add(models.Availability(tutor_id=ana.id, start_at=datetime(2099, 1, 5, 11), end_at=datetime(2099, 1, 5, 12)))
    s.commit()
    ids = {"calc": calc.id, "fis": fis.id, "ana": ana.id, "ana_token": ana.token}
    s.close()
    yield TestClient(app), Session, ids
    app.dependency_overrides.clear()
    engine.dispose()


def student(c, n):
    r = c.post("/api/students", json={"name": f"Est {n}", "email": f"est{n}@utp.ac.pa"})
    assert r.status_code == 201
    return r.json()["token"]


def book(c, tok, tutor, subject, start):
    return c.post("/api/bookings", headers={"X-Student-Token": tok},
                  json={"tutor_id": tutor, "subject_id": subject, "start_at": start})


def subject_slots(c, subject):
    return {s["start_at"][11:16]: s for s in c.get(f"/api/subjects/{subject}/slots?date=2099-01-05").json()["slots"]}


def test_cupo_3_acepta_tres_y_rechaza_el_cuarto(env):  # CA-23
    c, _, i = env
    for n in range(3):
        r = book(c, student(c, n), i["ana"], i["calc"], t(9))
        assert r.status_code == 201 and r.json()["status"] == "confirmada"
    r = book(c, student(c, 3), i["ana"], i["calc"], t(9))
    assert r.status_code == 409 and r.json()["detail"]["code"] == "session_full"


def test_cupos_libres_bajan_y_vuelven_al_cancelar(env):  # CA-24
    c, _, i = env
    assert subject_slots(c, i["calc"])["09:00"]["seats_left"] == 3
    toks = [student(c, n) for n in range(3)]
    ids = [book(c, tok, i["ana"], i["calc"], t(9)).json()["id"] for tok in toks]
    assert "09:00" not in subject_slots(c, i["calc"])  # llena: deja de aparecer
    c.post(f"/api/bookings/{ids[0]}/cancel", headers={"X-Student-Token": toks[0]})
    slot = subject_slots(c, i["calc"])["09:00"]
    assert slot["seats_left"] == 1 and slot["capacity"] == 3


def test_otra_materia_en_la_misma_sesion_es_conflicto(env):  # CA-25, G-02
    c, _, i = env
    assert book(c, student(c, 0), i["ana"], i["calc"], t(9)).status_code == 201
    r = book(c, student(c, 1), i["ana"], i["fis"], t(9))
    assert r.status_code == 409 and r.json()["detail"]["code"] == "tutor_conflict"
    assert "09:00" not in subject_slots(c, i["fis"])  # Física no ve la sesión tomada por Cálculo
    assert "10:00" in subject_slots(c, i["fis"])     # la siguiente sigue libre para cualquiera


def test_estudiante_no_reserva_dos_veces_la_misma_sesion(env):  # CA-26, G-04
    c, _, i = env
    tok = student(c, 0)
    assert book(c, tok, i["ana"], i["calc"], t(9)).status_code == 201
    r = book(c, tok, i["ana"], i["calc"], t(9))
    assert r.status_code == 409 and r.json()["detail"]["code"] == "student_conflict"


def test_bloque_individual_sigue_como_antes(env):  # RN-01 con cupo 1: mismo contrato que CA-02
    c, _, i = env
    assert book(c, student(c, 0), i["ana"], i["calc"], t(11)).status_code == 201
    r = book(c, student(c, 1), i["ana"], i["calc"], t(11))
    assert r.status_code == 409 and r.json()["detail"]["code"] == "tutor_conflict"


def test_publicar_cupo_valido_e_invalido(env):  # CA-27
    c, _, i = env
    h = {"X-Tutor-Token": i["ana_token"]}
    day = "2099-01-06"
    for bad in (0, 7):
        r = c.post("/api/tutor/availability", headers=h,
                   json={"start_at": f"{day}T09:00:00", "end_at": f"{day}T10:00:00", "capacity": bad})
        assert r.status_code == 422, bad
    r = c.post("/api/tutor/availability", headers=h, json={"start_at": f"{day}T09:00:00", "end_at": f"{day}T10:00:00"})
    assert r.status_code == 201 and r.json()["capacity"] == 1
    r = c.post("/api/tutor/availability", headers=h,
               json={"start_at": f"{day}T10:00:00", "end_at": f"{day}T11:00:00", "capacity": 6})
    assert r.status_code == 201 and r.json()["capacity"] == 6


def test_cupo_invalido_rechazado_por_la_bd(env):  # CA-27, restricción en BD
    _, Session, i = env
    from sqlalchemy.exc import IntegrityError
    with Session() as s:
        s.add(models.Availability(tutor_id=i["ana"], start_at=datetime(2099, 2, 1, 9), end_at=datetime(2099, 2, 1, 10), capacity=9))
        with pytest.raises(IntegrityError):
            s.commit()


def test_ocho_a_la_vez_con_cupo_3_solo_tres_entran(env):  # CA-28: la carrera con grupos
    c, Session, i = env
    tokens = [student(c, n) for n in range(8)]
    barrier = threading.Barrier(len(tokens))
    codes, errors = [], []

    def worker(tok):
        try:
            barrier.wait()
            codes.append(book(c, tok, i["ana"], i["calc"], t(9)).status_code)
        except Exception as e:  # que un fallo de hilo no se esconda
            errors.append(e)

    threads = [threading.Thread(target=worker, args=(tok,)) for tok in tokens]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    assert not errors
    assert sorted(codes) == [201] * 3 + [409] * 5
    with Session() as s:
        assert s.query(models.Booking).filter_by(tutor_id=i["ana"], status="confirmada").count() == 3


def test_espacios_del_tutor_incluyen_cupos(env):  # CA-24 en /api/tutors/{id}/slots
    c, _, i = env
    data = c.get(f"/api/tutors/{i['ana']}/slots?date=2099-01-05").json()
    assert [s[11:16] for s in data["slots"]] == ["09:00", "10:00", "11:00"]
    assert [(x["seats_left"], x["capacity"]) for x in data["seats"]] == [(3, 3), (3, 3), (1, 1)]
