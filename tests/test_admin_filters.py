"""RF-10 / CA-12: listado de reservas del admin con filtros."""
from datetime import datetime

import pytest

from app import models
from app.config import settings

ADMIN = {"X-Admin-Token": settings.admin_token}


def d(day, h):
    return datetime(2099, 1, day, h)


@pytest.fixture()
def env(session_factory, client):
    """4 reservas: Ana/Cálculo (5 y 6 ene), Bea/Física (5 ene), Ana/Cálculo cancelada (7 ene)."""
    s = session_factory()
    calc, fis = models.Subject(name="Cálculo I"), models.Subject(name="Física")
    ana = models.Tutor(name="Ana", email="ana@utp.ac.pa", subjects=[calc])
    bea = models.Tutor(name="Bea", email="bea@utp.ac.pa", subjects=[fis])
    luis, eva = models.Student(name="Luis", email="l@utp.ac.pa"), models.Student(name="Eva", email="e@utp.ac.pa")
    s.add_all([calc, fis, ana, bea, luis, eva])
    s.commit()

    def bk(tutor, student, subject, day, h, status="confirmada"):
        s.add(models.Booking(tutor_id=tutor.id, student_id=student.id, subject_id=subject.id,
                             start_at=d(day, h), end_at=d(day, h + 1), status=status))

    bk(ana, luis, calc, 5, 10)
    bk(ana, eva, calc, 6, 9)
    bk(bea, luis, fis, 5, 15)
    bk(ana, eva, calc, 7, 11, "cancelada")
    s.commit()
    ids = {"ana": ana.id, "bea": bea.id, "calc": calc.id, "fis": fis.id}
    s.close()
    yield client, ids


def get(c, **params):
    r = c.get("/api/admin/bookings", params=params, headers=ADMIN)
    assert r.status_code == 200, r.text
    return r.json()


def test_requiere_token_admin(env):
    c, _ = env
    assert c.get("/api/admin/bookings").status_code == 401
    assert c.get("/api/admin/bookings", headers={"X-Admin-Token": "mal"}).status_code == 401


def test_sin_filtros_devuelve_todo_ordenado_con_nombres(env):  # CA-12
    c, _ = env
    rows = get(c)
    assert len(rows) == 4
    assert [r["start_at"][:13] for r in rows] == sorted(r["start_at"][:13] for r in rows)
    assert rows[0]["tutor_name"] == "Ana" and rows[0]["student_name"] == "Luis" and rows[0]["subject_name"] == "Cálculo I"


def test_filtro_por_tutor(env):  # CA-12
    c, i = env
    assert {r["tutor_name"] for r in get(c, tutor_id=i["bea"])} == {"Bea"}
    assert len(get(c, tutor_id=i["ana"])) == 3


def test_filtro_por_materia(env):  # CA-12
    c, i = env
    assert {r["subject_name"] for r in get(c, subject_id=i["fis"])} == {"Física"}


def test_filtro_por_estado(env):  # CA-12
    c, _ = env
    rows = get(c, status="cancelada")
    assert len(rows) == 1 and rows[0]["start_at"].startswith("2099-01-07")
    assert len(get(c, status="confirmada")) == 3
    assert get(c, status="realizada") == []


def test_filtro_por_rango_de_fechas_inclusivo(env):  # CA-12
    c, _ = env
    assert len(get(c, date_from="2099-01-05", date_to="2099-01-05")) == 2   # el día completo
    assert len(get(c, date_from="2099-01-06")) == 2
    assert len(get(c, date_to="2099-01-06")) == 3


def test_filtros_combinados(env):  # CA-12
    c, i = env
    rows = get(c, tutor_id=i["ana"], status="confirmada", date_from="2099-01-06")
    assert len(rows) == 1 and rows[0]["start_at"].startswith("2099-01-06T09")


def test_sin_resultados_devuelve_lista_vacia(env):
    c, _ = env
    assert get(c, date_from="2100-01-01") == []


def test_paginacion(env):
    c, _ = env
    assert len(get(c, limit=2)) == 2
    assert len(get(c, limit=2, offset=3)) == 1


def test_parametros_invalidos_422(env):
    c, _ = env
    for params in ({"status": "inventado"}, {"date_from": "2099-02-01", "date_to": "2099-01-01"},
                   {"date_from": "hoy"}, {"limit": 0}, {"limit": 501}, {"tutor_id": "x"}):
        assert c.get("/api/admin/bookings", params=params, headers=ADMIN).status_code == 422, params
