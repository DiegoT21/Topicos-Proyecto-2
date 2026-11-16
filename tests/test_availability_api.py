"""Pruebas de disponibilidad, catálogo, admin y flujo completo (ciclo 3). Cubren CA-11, CA-13, CA-14."""
from datetime import datetime

import pytest

from app.config import settings

ADMIN = {"X-Admin-Token": settings.admin_token}


def t(h, m=0, day=5):
    return datetime(2099, 1, day, h, m).isoformat()


@pytest.fixture()
def c(client):
    return client


def subject(c, name="Cálculo I"):
    r = c.post("/api/admin/subjects", json={"name": name}, headers=ADMIN)
    assert r.status_code == 201
    return r.json()["id"]


def tutor(c, name="Ana", email="ana@utp.ac.pa", subjects=()):
    r = c.post("/api/admin/tutors", json={"name": name, "email": email, "subject_ids": list(subjects)}, headers=ADMIN)
    assert r.status_code == 201, r.text
    return r.json()


def publish(c, tok, start, end):
    return c.post("/api/tutor/availability", json={"start_at": start, "end_at": end}, headers={"X-Tutor-Token": tok})


def student(c, name="Luis", email="luis@utp.ac.pa"):
    return c.post("/api/students", json={"name": name, "email": email}).json()["token"]


# --- admin (RF-01, RF-02) ---
def test_admin_requiere_token(c):
    assert c.post("/api/admin/subjects", json={"name": "Física"}).status_code == 401
    assert c.post("/api/admin/subjects", json={"name": "Física"}, headers={"X-Admin-Token": "mal"}).status_code == 401


def test_materia_con_html_rechazada(c):
    assert c.post("/api/admin/subjects", json={"name": "<b>x</b>"}, headers=ADMIN).status_code == 422


def test_materia_duplicada_409(c):
    subject(c)
    assert c.post("/api/admin/subjects", json={"name": "Cálculo I"}, headers=ADMIN).status_code == 409


def test_materia_desactivada_no_se_lista(c):
    sid = subject(c)
    assert c.delete(f"/api/admin/subjects/{sid}", headers=ADMIN).status_code == 200
    assert c.get("/api/subjects").json() == []


def test_tutor_devuelve_token_y_no_se_filtra_en_lista(c):
    sid = subject(c)
    created = tutor(c, subjects=[sid])
    assert created["token"]
    listed = c.get("/api/tutors").json()
    assert listed[0]["name"] == "Ana" and "token" not in listed[0] and "email" not in listed[0]


def test_tutor_con_materia_inexistente_422(c):
    r = c.post("/api/admin/tutors", json={"name": "Ana", "email": "a@utp.ac.pa", "subject_ids": [99]}, headers=ADMIN)
    assert r.status_code == 422


def test_tutor_email_duplicado_409(c):
    tutor(c)
    r = c.post("/api/admin/tutors", json={"name": "Otra", "email": "ANA@utp.ac.pa"}, headers=ADMIN)
    assert r.status_code == 409


# --- catálogo (RF-04) ---
def test_listar_tutores_por_materia(c):  # CA-11
    math, phys = subject(c), subject(c, "Física")
    tutor(c, "Ana", "ana@utp.ac.pa", [math])
    tutor(c, "Bea", "bea@utp.ac.pa", [phys])
    names = [x["name"] for x in c.get(f"/api/tutors?subject_id={math}").json()]
    assert names == ["Ana"]
    assert len(c.get("/api/tutors").json()) == 2


# --- disponibilidad del tutor (RF-03) ---
def test_publicar_requiere_token_de_tutor(c):
    assert publish(c, "mal", t(9), t(13)).status_code == 401


def test_publicar_disponibilidad(c):
    tok = tutor(c)["token"]
    r = publish(c, tok, t(9), t(13))
    assert r.status_code == 201 and r.json()["start_at"].startswith("2099-01-05T09:00")


def test_bloques_solapados_rechazados(c):  # CA-14
    tok = tutor(c)["token"]
    assert publish(c, tok, t(9), t(12)).status_code == 201
    r = publish(c, tok, t(11), t(14))
    assert r.status_code == 409 and r.json()["detail"]["code"] == "availability_overlap"
    assert publish(c, tok, t(12), t(14)).status_code == 201  # consecutivo sí


def test_bloque_invalido(c):
    tok = tutor(c)["token"]
    assert publish(c, tok, t(13), t(9)).status_code == 422
    assert publish(c, tok, t(9), t(9, day=6)).status_code == 422  # cruza de día
    assert publish(c, tok, datetime(2020, 1, 1, 9).isoformat(), datetime(2020, 1, 1, 10).isoformat()).status_code == 422


def test_un_tutor_no_ve_ni_publica_en_otro(c):
    a, b = tutor(c, "Ana", "ana@utp.ac.pa")["token"], tutor(c, "Bea", "bea@utp.ac.pa")
    publish(c, a, t(9), t(13))
    assert c.get(f"/api/tutors/{b['id']}/slots?date=2099-01-05").json()["slots"] == []


# --- espacios libres (RF-05) ---
def test_espacios_libres_del_dia(c):  # CA-13
    sid = subject(c)
    tu = tutor(c, subjects=[sid])
    publish(c, tu["token"], t(9), t(13))
    r = c.get(f"/api/tutors/{tu['id']}/slots?date=2099-01-05").json()
    assert [s[11:16] for s in r["slots"]] == ["09:00", "10:00", "11:00", "12:00"]


def test_reservado_desaparece_y_cancelar_lo_devuelve(c):  # CA-13, CA-07
    sid = subject(c)
    tu = tutor(c, subjects=[sid])
    publish(c, tu["token"], t(9), t(13))
    stu = student(c)
    h = {"X-Student-Token": stu}
    bid = c.post("/api/bookings", headers=h, json={"tutor_id": tu["id"], "subject_id": sid, "start_at": t(10)}).json()["id"]
    slots = lambda: [s[11:16] for s in c.get(f"/api/tutors/{tu['id']}/slots?date=2099-01-05").json()["slots"]]
    assert slots() == ["09:00", "11:00", "12:00"]
    c.post(f"/api/bookings/{bid}/cancel", headers=h)
    assert slots() == ["09:00", "10:00", "11:00", "12:00"]


def test_dia_sin_bloques_devuelve_vacio(c):
    tu = tutor(c)
    assert c.get(f"/api/tutors/{tu['id']}/slots?date=2099-02-01").json()["slots"] == []


def test_slots_de_tutor_inexistente_404(c):
    assert c.get("/api/tutors/99/slots?date=2099-01-05").status_code == 404


def test_slots_fecha_invalida_422(c):
    tu = tutor(c)
    assert c.get(f"/api/tutors/{tu['id']}/slots?date=hoy").status_code == 422


# --- agenda (RF-09) ---
def test_agenda_del_tutor(c):
    sid = subject(c)
    tu = tutor(c, subjects=[sid])
    publish(c, tu["token"], t(9), t(13))
    c.post("/api/bookings", headers={"X-Student-Token": student(c)},
           json={"tutor_id": tu["id"], "subject_id": sid, "start_at": t(11)})
    ag = c.get("/api/tutor/agenda", headers={"X-Tutor-Token": tu["token"]}).json()
    assert len(ag) == 1 and ag[0]["start_at"].startswith("2099-01-05T11:00")
    assert c.get("/api/tutor/agenda").status_code == 401


# --- flujo completo desde las specs: admin -> tutor -> estudiante ---
def test_flujo_completo_reserva_en_espacio_publicado(c):
    sid = subject(c)
    tu = tutor(c, subjects=[sid])
    publish(c, tu["token"], t(9), t(11))
    first = c.get(f"/api/tutors/{tu['id']}/slots?date=2099-01-05").json()["slots"][0]
    r = c.post("/api/bookings", headers={"X-Student-Token": student(c)},
               json={"tutor_id": tu["id"], "subject_id": sid, "start_at": first})
    assert r.status_code == 201
    r2 = c.post("/api/bookings", headers={"X-Student-Token": student(c, "Eva", "eva@utp.ac.pa")},
                json={"tutor_id": tu["id"], "subject_id": sid, "start_at": first})
    assert r2.status_code == 409
