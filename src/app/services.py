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
from .rules import (
    STATUS_CANCELLED,
    STATUS_CONFIRMED,
    BookingRuleError,
    find_conflict,
    seats_left,
    validate_booking_window,
    validate_slot_alignment,
)

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
        validate_slot_alignment(start_at, availabilities, settings.session_minutes)  # RN-03 / E-02 (B-04)

        # RN-01 reformulada + RN-13 (cambio 2026-11-16): varias reservas de la misma sesión hasta el cupo.
        block = next(a for a in availabilities if a.start_at <= start_at and end_at <= a.end_at)
        tutor_bookings = _active_overlapping(db, models.Booking.tutor_id, tutor_id, start_at, end_at)
        same_session = all(b.start_at == start_at and b.end_at == end_at and b.subject_id == subject_id
                           for b in tutor_bookings)
        if not same_session:  # otra sesión solapada u otra materia en la misma sesión (G-02)
            raise BookingRuleError("tutor_conflict", "El tutor ya tiene una sesión en ese horario")
        if seats_left(start_at, end_at, block.capacity, tutor_bookings, subject_id) == 0:
            if block.capacity == 1:  # sesión individual: mismo contrato que antes del cambio (CA-02)
                raise BookingRuleError("tutor_conflict", "El tutor ya tiene una sesión en ese horario")
            raise BookingRuleError("session_full", "La sesión grupal ya no tiene cupos")  # RN-13
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
