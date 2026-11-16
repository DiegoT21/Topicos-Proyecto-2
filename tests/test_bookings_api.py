"""Pruebas de API de reservar y cancelar. Cubren CA-01, CA-02, CA-03, CA-04, CA-05, CA-06, CA-07, CA-08, CA-10."""
from datetime import datetime

import pytest

from app import models
from app.config import settings


def t(h, m=0):
    return datetime(2099, 1, 5, h, m).isoformat()  # fecha lejana: nunca es "pasado"


@pytest.fixture()
def env(session_factory, client):
    s = session_factory()
    math = models.Subject(name="Cálculo I")
    physics = models.Subject(name="Física")
    ana = models.Tutor(name="Ana", email="ana@utp.ac.pa", subjects=[math])
    bea = models.Tutor(name="Bea", email="bea@utp.ac.pa", subjects=[math])
    s.add_all([math, physics, ana, bea])
    s.commit()
    for tutor in (ana, bea):  # ambos disponibles 9:00-13:00
        s.add(models.Availability(tutor_id=tutor.id, start_at=datetime(2099, 1, 5, 9), end_at=datetime(2099, 1, 5, 13)))
    s.commit()
    ids = {"math": math.id, "physics": physics.id, "ana": ana.id, "bea": bea.id}
    s.close()
    yield client, ids


def register(client, name, email):
    r = client.post("/api/students", json={"name": name, "email": email})
    assert r.status_code == 201
    return r.json()["token"]


def book(client, token, tutor, subject, start):
    return client.post("/api/bookings", headers={"X-Student-Token": token},
                       json={"tutor_id": tutor, "subject_id": subject, "start_at": start})


def test_reservar_espacio_libre(env):  # CA-01
    c, i = env
    tok = register(c, "Luis", "luis@utp.ac.pa")
    r = book(c, tok, i["ana"], i["math"], t(10))
    assert r.status_code == 201
    body = r.json()
    assert body["status"] == "confirmada" and body["end_at"].startswith("2099-01-05T11:00")


def test_no_doble_reserva_mismo_tutor_mismo_horario(env):  # CA-02
    c, i = env
    a, b = register(c, "Luis", "luis@utp.ac.pa"), register(c, "Eva", "eva@utp.ac.pa")
    assert book(c, a, i["ana"], i["math"], t(10)).status_code == 201
    r = book(c, b, i["ana"], i["math"], t(10))
    assert r.status_code == 409 and r.json()["detail"]["code"] == "tutor_conflict"


def test_inicio_fuera_de_espacio_rechazado(env):  # CA-15, RN-03 / E-02 (B-04)
    """Antes 10:30 daba 409 por solape; ahora no es un espacio publicado y se rechaza antes (422).
    El solape parcial del mismo tutor ya no puede ocurrir desde la API; se prueba en test_rules.py."""
    c, i = env
    a, b = register(c, "Luis", "luis@utp.ac.pa"), register(c, "Eva", "eva@utp.ac.pa")
    assert book(c, a, i["ana"], i["math"], t(10)).status_code == 201
    r = book(c, b, i["ana"], i["math"], t(10, 30))
    assert r.status_code == 422 and r.json()["detail"]["code"] == "not_a_slot"
    r = book(c, b, i["bea"], i["math"], t(9, 15))  # aunque el espacio esté libre
    assert r.status_code == 422 and r.json()["detail"]["code"] == "not_a_slot"


def test_estudiante_solape_parcial_con_otro_tutor(env, session_factory):  # CA-04, RN-02
    """Con bloques que empiezan a horas distintas, el solape parcial del estudiante sí es posible."""
    c, i = env
    s = session_factory()
    cami = models.Tutor(name="Cami", email="cami@utp.ac.pa", subjects=[s.get(models.Subject, i["math"])])
    s.add(cami)
    s.commit()
    s.add(models.Availability(tutor_id=cami.id, start_at=datetime(2099, 1, 5, 10, 30), end_at=datetime(2099, 1, 5, 12, 30)))
    s.commit()
    cami_id = cami.id
    s.close()
    tok = register(c, "Luis", "luis@utp.ac.pa")
    assert book(c, tok, i["ana"], i["math"], t(10)).status_code == 201
    r = book(c, tok, cami_id, i["math"], t(10, 30))
    assert r.status_code == 409 and r.json()["detail"]["code"] == "student_conflict"


def test_correo_no_institucional_rechazado(env):  # CA-16, RN-11 / D-01 (B-01)
    c, _ = env
    r = c.post("/api/students", json={"name": "Luis", "email": "luis@gmail.com"})
    assert r.status_code == 422
    r = c.post("/api/students", json={"name": "Luis", "email": "luis@utp.ac.pa.evil.com"})
    assert r.status_code == 422
    r = c.post("/api/students", json={"name": "Luis", "email": "  Luis@UTP.AC.PA "})
    assert r.status_code == 201 and r.json()["email"] == "luis@utp.ac.pa"


def test_sesiones_consecutivas_permitidas(env):  # CA-03
    c, i = env
    a, b = register(c, "Luis", "luis@utp.ac.pa"), register(c, "Eva", "eva@utp.ac.pa")
    assert book(c, a, i["ana"], i["math"], t(10)).status_code == 201
    assert book(c, b, i["ana"], i["math"], t(11)).status_code == 201


def test_mismo_estudiante_dos_tutores_misma_hora(env):  # CA-04
    c, i = env
    tok = register(c, "Luis", "luis@utp.ac.pa")
    assert book(c, tok, i["ana"], i["math"], t(10)).status_code == 201
    r = book(c, tok, i["bea"], i["math"], t(10))
    assert r.status_code == 409 and r.json()["detail"]["code"] == "student_conflict"


def test_fuera_de_disponibilidad(env):  # CA-05
    c, i = env
    tok = register(c, "Luis", "luis@utp.ac.pa")
    r = book(c, tok, i["ana"], i["math"], t(15))
    assert r.status_code == 422 and r.json()["detail"]["code"] == "outside_availability"


def test_hora_pasada(env):  # CA-06
    c, i = env
    tok = register(c, "Luis", "luis@utp.ac.pa")
    r = book(c, tok, i["ana"], i["math"], datetime(2020, 1, 1, 10).isoformat())
    assert r.status_code == 422 and r.json()["detail"]["code"] == "past"


def test_materia_que_el_tutor_no_ofrece(env):  # RN-06
    c, i = env
    tok = register(c, "Luis", "luis@utp.ac.pa")
    r = book(c, tok, i["ana"], i["physics"], t(10))
    assert r.status_code == 422 and r.json()["detail"]["code"] == "subject_not_taught"


def test_cancelar_libera_el_espacio(env):  # CA-07
    c, i = env
    a, b = register(c, "Luis", "luis@utp.ac.pa"), register(c, "Eva", "eva@utp.ac.pa")
    bid = book(c, a, i["ana"], i["math"], t(10)).json()["id"]
    r = c.post(f"/api/bookings/{bid}/cancel", headers={"X-Student-Token": a})
    assert r.status_code == 200 and r.json()["status"] == "cancelada"
    assert book(c, b, i["ana"], i["math"], t(10)).status_code == 201  # el espacio vuelve a estar libre


def test_cancelar_ajena_prohibido(env):  # CA-08
    c, i = env
    a, b = register(c, "Luis", "luis@utp.ac.pa"), register(c, "Eva", "eva@utp.ac.pa")
    bid = book(c, a, i["ana"], i["math"], t(10)).json()["id"]
    assert c.post(f"/api/bookings/{bid}/cancel", headers={"X-Student-Token": b}).status_code == 403


def test_admin_puede_cancelar(env):  # RN-08
    c, i = env
    a = register(c, "Luis", "luis@utp.ac.pa")
    bid = book(c, a, i["ana"], i["math"], t(10)).json()["id"]
    r = c.post(f"/api/bookings/{bid}/cancel", headers={"X-Admin-Token": settings.admin_token})
    assert r.status_code == 200


def test_cancelar_dos_veces_rechazado(env):  # RN-09
    c, i = env
    a = register(c, "Luis", "luis@utp.ac.pa")
    bid = book(c, a, i["ana"], i["math"], t(10)).json()["id"]
    h = {"X-Student-Token": a}
    assert c.post(f"/api/bookings/{bid}/cancel", headers=h).status_code == 200
    assert c.post(f"/api/bookings/{bid}/cancel", headers=h).status_code == 409


def test_sin_token_401(env):
    c, i = env
    r = c.post("/api/bookings", json={"tutor_id": i["ana"], "subject_id": i["math"], "start_at": t(10)})
    assert r.status_code == 401


def test_nombre_con_html_rechazado(env):  # CA-10
    c, _ = env
    r = c.post("/api/students", json={"name": "<img src=x onerror=alert(1)>", "email": "x@utp.ac.pa"})
    assert r.status_code == 422


def test_email_duplicado_409(env):
    c, _ = env
    register(c, "Luis", "luis@utp.ac.pa")
    assert c.post("/api/students", json={"name": "Otro", "email": "LUIS@utp.ac.pa"}).status_code == 409
