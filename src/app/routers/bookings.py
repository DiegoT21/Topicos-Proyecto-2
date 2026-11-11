from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas, services
from ..config import settings
from ..database import get_db
from ..rules import BookingRuleError

router = APIRouter(prefix="/api")

# código de regla -> HTTP (api.md: 409 conflicto, 422 validación, 403 permiso, 404 no existe)
_STATUS = {
    "tutor_conflict": 409, "student_conflict": 409, "invalid_transition": 409,
    "forbidden": 403,
    "tutor_not_found": 404, "subject_not_found": 404, "booking_not_found": 404,
}


def rule_error(e: BookingRuleError) -> HTTPException:
    return HTTPException(status_code=_STATUS.get(e.code, 422), detail={"code": e.code, "message": str(e)})


def current_student(
    x_student_token: Optional[str] = Header(default=None), db: Session = Depends(get_db)
) -> models.Student:
    student = db.query(models.Student).filter_by(token=x_student_token).first() if x_student_token else None
    if student is None:
        raise HTTPException(status_code=401, detail={"code": "invalid_token", "message": "Token de estudiante inválido"})
    return student


@router.post("/students", response_model=schemas.StudentOut, status_code=201)
def register_student(data: schemas.StudentCreate, db: Session = Depends(get_db)):
    student = models.Student(name=data.name, email=data.email.lower())
    db.add(student)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail={"code": "email_taken", "message": "Ese correo ya está registrado"})
    return student


@router.post("/bookings", response_model=schemas.BookingOut, status_code=201)
def create_booking(
    data: schemas.BookingCreate, student: models.Student = Depends(current_student), db: Session = Depends(get_db)
):
    try:
        return services.book(db, student, data.tutor_id, data.subject_id, data.start_at)
    except BookingRuleError as e:
        raise rule_error(e)


@router.post("/bookings/{booking_id}/cancel", response_model=schemas.BookingOut)
def cancel_booking(
    booking_id: int,
    x_student_token: Optional[str] = Header(default=None),
    x_admin_token: Optional[str] = Header(default=None),
    db: Session = Depends(get_db),
):
    is_admin = x_admin_token is not None and x_admin_token == settings.admin_token
    student = db.query(models.Student).filter_by(token=x_student_token).first() if x_student_token else None
    if not is_admin and student is None:
        raise HTTPException(status_code=401, detail={"code": "invalid_token", "message": "Credencial inválida"})
    try:
        return services.cancel(db, booking_id, student=student, is_admin=is_admin)
    except BookingRuleError as e:
        raise rule_error(e)
