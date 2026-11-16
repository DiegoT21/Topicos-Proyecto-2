"""Pruebas de modelos y restricciones (issue #2, specs/data-model.md)."""
from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from app import models
from app.rules import find_conflict


def t(h):
    return datetime(2026, 12, 1, h)


def seed(db):
    m = models.Subject(name="Cálculo I")
    tutor = models.Tutor(name="Ana", email="ana@utp.ac.pa", subjects=[m])
    st = models.Student(name="Luis", email="luis@utp.ac.pa")
    db.add_all([m, tutor, st])
    db.commit()
    return m, tutor, st


def test_tutor_tiene_materias(db):
    m, tutor, _ = seed(db)
    assert tutor.subjects[0].name == "Cálculo I"


def test_estudiante_recibe_token_unico(db):
    _, _, st = seed(db)
    other = models.Student(name="Eva", email="eva@utp.ac.pa")
    db.add(other)
    db.commit()
    assert len(st.token) >= 24 and st.token != other.token


def test_email_de_tutor_unico(db):
    seed(db)
    db.add(models.Tutor(name="Otra", email="ana@utp.ac.pa"))
    with pytest.raises(IntegrityError):
        db.commit()


def test_reserva_por_defecto_confirmada(db):
    m, tutor, st = seed(db)
    b = models.Booking(tutor_id=tutor.id, student_id=st.id, subject_id=m.id, start_at=t(10), end_at=t(11))
    db.add(b)
    db.commit()
    assert b.status == "confirmada" and b.created_at is not None


def test_fin_debe_ser_posterior_al_inicio(db):
    m, tutor, st = seed(db)
    db.add(models.Booking(tutor_id=tutor.id, student_id=st.id, subject_id=m.id, start_at=t(11), end_at=t(10)))
    with pytest.raises(IntegrityError):
        db.commit()


def test_estado_invalido_rechazado(db):
    m, tutor, st = seed(db)
    db.add(models.Booking(tutor_id=tutor.id, student_id=st.id, subject_id=m.id,
                          start_at=t(10), end_at=t(11), status="inventado"))
    with pytest.raises(IntegrityError):
        db.commit()


def test_modelos_se_integran_con_reglas(db):
    """Las reservas guardadas funcionan con rules.find_conflict (RN-01)."""
    m, tutor, st = seed(db)
    db.add(models.Booking(tutor_id=tutor.id, student_id=st.id, subject_id=m.id, start_at=t(10), end_at=t(11)))
    db.commit()
    existing = db.query(models.Booking).filter_by(tutor_id=tutor.id).all()
    assert find_conflict(t(10), t(11), existing) is not None
    assert find_conflict(t(11), t(12), existing) is None
