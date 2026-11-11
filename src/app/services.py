"""Casos de uso: reservar y cancelar (spec: business-rules.md, acceptance-criteria.md).

`book` verifica y guarda dentro de un mismo bloque protegido por un lock de proceso, para evitar
la carrera check-then-insert del Proyecto 1 (hallazgo 9). Limitación conocida: el lock sirve para
un solo proceso; con varios procesos haría falta una restricción en BD o transacción serializable.
"""
import threading
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from . import models
from .config import local_now, settings
from .rules import STATUS_CANCELLED, STATUS_CONFIRMED, BookingRuleError, find_conflict, validate_booking_window

_book_lock = threading.Lock()


def _active_overlapping(db: Session, column, value: int, start: datetime, end: datetime):
    return (
        db.query(models.Booking)
        .filter(column == value, models.Booking.status != STATUS_CANCELLED)
        .filter(models.Booking.start_at < end, models.Booking.end_at > start)
        .all()
    )


def book(
    db: Session,
    student: models.Student,
    tutor_id: int,
    subject_id: int,
    start_at: datetime,
    now: Optional[datetime] = None,
) -> models.Booking:
    now = now or local_now()
    end_at = start_at + timedelta(minutes=settings.session_minutes)
    with _book_lock:
        tutor = db.get(models.Tutor, tutor_id)
        if tutor is None or not tutor.active:
            raise BookingRuleError("tutor_not_found", "Tutor no encontrado")
        subject = db.get(models.Subject, subject_id)
        if subject is None or not subject.active:
            raise BookingRuleError("subject_not_found", "Materia no encontrada")
        if subject not in tutor.subjects:  # RN-06
            raise BookingRuleError("subject_not_taught", "El tutor no ofrece esa materia")

        availabilities = db.query(models.Availability).filter_by(tutor_id=tutor_id).all()
        validate_booking_window(start_at, end_at, now, availabilities, settings.min_notice_minutes)  # RN-03, RN-04

        if find_conflict(start_at, end_at, _active_overlapping(db, models.Booking.tutor_id, tutor_id, start_at, end_at)):
            raise BookingRuleError("tutor_conflict", "El tutor ya tiene una sesión en ese horario")  # RN-01
        if find_conflict(start_at, end_at, _active_overlapping(db, models.Booking.student_id, student.id, start_at, end_at)):
            raise BookingRuleError("student_conflict", "Ya tienes una sesión en ese horario")  # RN-02

        booking = models.Booking(
            tutor_id=tutor_id, student_id=student.id, subject_id=subject_id,
            start_at=start_at, end_at=end_at, status=STATUS_CONFIRMED,
        )
        db.add(booking)
        db.commit()
        return booking


def cancel(db: Session, booking_id: int, student: Optional[models.Student] = None, is_admin: bool = False) -> models.Booking:
    booking = db.get(models.Booking, booking_id)
    if booking is None:
        raise BookingRuleError("booking_not_found", "Reserva no encontrada")
    if not is_admin and (student is None or booking.student_id != student.id):  # RN-08
        raise BookingRuleError("forbidden", "Solo el dueño de la reserva puede cancelarla")
    if booking.status != STATUS_CONFIRMED:  # RN-09: solo confirmada -> cancelada
        raise BookingRuleError("invalid_transition", f"No se puede cancelar una reserva {booking.status}")
    booking.status = STATUS_CANCELLED  # RN-07: deja de bloquear el espacio, queda en el historial
    db.commit()
    return booking
