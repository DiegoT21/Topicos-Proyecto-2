"""Consultas públicas: materias, tutores y espacios libres (RF-04, RF-05, B-10)."""
from datetime import date as date_type
from datetime import datetime, time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..config import local_now, settings
from ..database import get_db
from ..rules import STATUS_CANCELLED, free_slots

router = APIRouter(prefix="/api")


def _tutor_free_slots(db: Session, tutor_id: int, day: date_type, now: datetime) -> list[datetime]:
    day_start, day_end = datetime.combine(day, time.min), datetime.combine(day, time.max)
    blocks = (
        db.query(models.Availability)
        .filter(models.Availability.tutor_id == tutor_id, models.Availability.start_at >= day_start,
                models.Availability.start_at <= day_end)
        .all()
    )
    bookings = (
        db.query(models.Booking)
        .filter(models.Booking.tutor_id == tutor_id, models.Booking.status != STATUS_CANCELLED,
                models.Booking.start_at >= day_start, models.Booking.start_at <= day_end)
        .all()
    )
    return free_slots(day, blocks, bookings, settings.session_minutes, now, settings.min_notice_minutes)


@router.get("/subjects", response_model=list[schemas.SubjectOut])
def list_subjects(db: Session = Depends(get_db)):
    return db.query(models.Subject).filter_by(active=True).order_by(models.Subject.name).all()


@router.get("/subjects/{subject_id}/slots", response_model=schemas.SubjectSlotsOut)
def subject_slots(subject_id: int, date: date_type, db: Session = Depends(get_db)):
    """B-10: espacios libres de todos los tutores activos de una materia, ordenados por hora y tutor.

    Permite reservar en 3 pasos (materia → espacio → confirmar), eligiendo por hora (outcomes.md).
    """
    subject = db.get(models.Subject, subject_id)
    if subject is None or not subject.active:
        raise HTTPException(404, {"code": "subject_not_found", "message": "Materia no encontrada"})
    tutors = (
        db.query(models.Tutor)
        .filter(models.Tutor.active, models.Tutor.subjects.any(models.Subject.id == subject_id))
        .all()
    )
    now = local_now()
    slots = [
        {"tutor_id": tu.id, "tutor_name": tu.name, "start_at": s}
        for tu in tutors
        for s in _tutor_free_slots(db, tu.id, date, now)
    ]
    slots.sort(key=lambda x: (x["start_at"], x["tutor_name"], x["tutor_id"]))
    return {"subject_id": subject_id, "date": date.isoformat(), "session_minutes": settings.session_minutes, "slots": slots}


@router.get("/tutors", response_model=list[schemas.TutorPublic])
def list_tutors(subject_id: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(models.Tutor).filter_by(active=True)
    if subject_id is not None:
        q = q.filter(models.Tutor.subjects.any(models.Subject.id == subject_id))  # CA-11
    return q.order_by(models.Tutor.name).all()


@router.get("/tutors/{tutor_id}/slots", response_model=schemas.SlotsOut)
def tutor_slots(tutor_id: int, date: date_type, db: Session = Depends(get_db)):
    tutor = db.get(models.Tutor, tutor_id)
    if tutor is None or not tutor.active:
        raise HTTPException(404, {"code": "tutor_not_found", "message": "Tutor no encontrado"})
    slots = _tutor_free_slots(db, tutor_id, date, local_now())
    return {"tutor_id": tutor_id, "date": date.isoformat(), "session_minutes": settings.session_minutes, "slots": slots}
