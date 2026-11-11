"""Consultas públicas: materias, tutores y espacios libres (RF-04, RF-05)."""
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


@router.get("/subjects", response_model=list[schemas.SubjectOut])
def list_subjects(db: Session = Depends(get_db)):
    return db.query(models.Subject).filter_by(active=True).order_by(models.Subject.name).all()


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
    day_start, day_end = datetime.combine(date, time.min), datetime.combine(date, time.max)
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
    slots = free_slots(date, blocks, bookings, settings.session_minutes, local_now(), settings.min_notice_minutes)
    return {"tutor_id": tutor_id, "date": date.isoformat(), "session_minutes": settings.session_minutes, "slots": slots}
