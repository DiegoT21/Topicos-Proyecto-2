"""Gestión del administrador: materias y tutores (RF-01, RF-02)."""
from datetime import date, datetime, time
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas
from ..config import settings
from ..database import get_db

router = APIRouter(prefix="/api/admin")


def require_admin(x_admin_token: Optional[str] = Header(default=None)) -> None:
    if x_admin_token is None or x_admin_token != settings.admin_token:
        raise HTTPException(401, {"code": "invalid_token", "message": "Token de administrador inválido"})


@router.get("/bookings", response_model=list[schemas.AdminBookingOut], dependencies=[Depends(require_admin)])
def list_bookings(
    tutor_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    status: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """RF-10: reservas filtradas por tutor, materia, estado y rango de fechas (inclusivo)."""
    if status is not None and status not in models.VALID_STATUSES:
        raise HTTPException(422, {"code": "invalid_status", "message": f"Estado inválido: {status}"})
    if date_from and date_to and date_from > date_to:
        raise HTTPException(422, {"code": "invalid_range", "message": "date_from no puede ser posterior a date_to"})

    B = models.Booking
    q = (
        db.query(B, models.Tutor.name, models.Student.name, models.Subject.name)
        .join(models.Tutor, models.Tutor.id == B.tutor_id)
        .join(models.Student, models.Student.id == B.student_id)
        .join(models.Subject, models.Subject.id == B.subject_id)
    )
    if tutor_id is not None:
        q = q.filter(B.tutor_id == tutor_id)
    if subject_id is not None:
        q = q.filter(B.subject_id == subject_id)
    if status is not None:
        q = q.filter(B.status == status)
    if date_from is not None:
        q = q.filter(B.start_at >= datetime.combine(date_from, time.min))
    if date_to is not None:
        q = q.filter(B.start_at <= datetime.combine(date_to, time.max))
    rows = q.order_by(B.start_at, B.id).limit(limit).offset(offset).all()
    return [
        schemas.AdminBookingOut(
            id=b.id, tutor_id=b.tutor_id, tutor_name=tn, student_id=b.student_id, student_name=sn,
            subject_id=b.subject_id, subject_name=subn, start_at=b.start_at, end_at=b.end_at, status=b.status,
        )
        for b, tn, sn, subn in rows
    ]


@router.post("/subjects", response_model=schemas.SubjectOut, status_code=201, dependencies=[Depends(require_admin)])
def create_subject(data: schemas.SubjectCreate, db: Session = Depends(get_db)):
    subject = models.Subject(name=data.name)
    db.add(subject)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, {"code": "subject_exists", "message": "La materia ya existe"})
    return subject


@router.delete("/subjects/{subject_id}", response_model=schemas.SubjectOut, dependencies=[Depends(require_admin)])
def deactivate_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.get(models.Subject, subject_id)
    if subject is None:
        raise HTTPException(404, {"code": "subject_not_found", "message": "Materia no encontrada"})
    subject.active = False  # se desactiva, no se borra: las reservas viejas conservan su referencia
    db.commit()
    return subject


@router.post("/tutors", response_model=schemas.TutorCreatedOut, status_code=201, dependencies=[Depends(require_admin)])
def create_tutor(data: schemas.TutorCreate, db: Session = Depends(get_db)):
    subjects = db.query(models.Subject).filter(models.Subject.id.in_(data.subject_ids), models.Subject.active).all()
    if len(subjects) != len(set(data.subject_ids)):
        raise HTTPException(422, {"code": "subject_not_found", "message": "Alguna materia no existe o está inactiva"})
    tutor = models.Tutor(name=data.name, email=data.email.lower(), subjects=subjects)
    db.add(tutor)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, {"code": "email_taken", "message": "Ese correo ya está registrado"})
    return tutor
