"""Gestión del administrador: materias y tutores (RF-01, RF-02)."""
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas
from ..config import settings
from ..database import get_db

router = APIRouter(prefix="/api/admin")


def require_admin(x_admin_token: Optional[str] = Header(default=None)) -> None:
    if x_admin_token is None or x_admin_token != settings.admin_token:
        raise HTTPException(401, {"code": "invalid_token", "message": "Token de administrador inválido"})


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
