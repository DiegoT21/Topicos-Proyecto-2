"""Acciones del tutor: publicar disponibilidad y ver su agenda (RF-03, RF-09)."""
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..config import local_now
from ..database import get_db
from ..rules import find_conflict

router = APIRouter(prefix="/api/tutor")


def current_tutor(x_tutor_token: Optional[str] = Header(default=None), db: Session = Depends(get_db)) -> models.Tutor:
    tutor = db.query(models.Tutor).filter_by(token=x_tutor_token, active=True).first() if x_tutor_token else None
    if tutor is None:
        raise HTTPException(401, {"code": "invalid_token", "message": "Token de tutor inválido"})
    return tutor


@router.post("/availability", response_model=schemas.AvailabilityOut, status_code=201)
def publish_availability(
    data: schemas.AvailabilityCreate, tutor: models.Tutor = Depends(current_tutor), db: Session = Depends(get_db)
):
    if data.end_at <= data.start_at:
        raise HTTPException(422, {"code": "invalid_interval", "message": "La hora de fin debe ser posterior a la de inicio"})
    if data.start_at.date() != data.end_at.date():
        raise HTTPException(422, {"code": "multi_day", "message": "Un bloque debe empezar y terminar el mismo día"})
    if data.start_at <= local_now():
        raise HTTPException(422, {"code": "past", "message": "No se puede publicar disponibilidad en el pasado"})
    existing = db.query(models.Availability).filter_by(tutor_id=tutor.id).all()
    if find_conflict(data.start_at, data.end_at, existing):  # RN-12
        raise HTTPException(409, {"code": "availability_overlap", "message": "El bloque se solapa con otro ya publicado"})
    block = models.Availability(tutor_id=tutor.id, start_at=data.start_at, end_at=data.end_at)
    db.add(block)
    db.commit()
    return block


@router.get("/agenda", response_model=list[schemas.BookingOut])
def agenda(tutor: models.Tutor = Depends(current_tutor), db: Session = Depends(get_db)):
    return db.query(models.Booking).filter_by(tutor_id=tutor.id).order_by(models.Booking.start_at).all()
