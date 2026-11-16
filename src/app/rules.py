"""Reglas de negocio puras (sin base de datos).

Spec: specs/business-rules.md (RN-01, RN-02, RN-03, RN-04, RN-07, RN-10).
Todas las fechas son datetime comparables entre sí (misma zona / ambas naive).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Iterable, Optional, Protocol

STATUS_CONFIRMED = "confirmada"
STATUS_CANCELLED = "cancelada"
STATUS_DONE = "realizada"


class _HasInterval(Protocol):
    start_at: datetime
    end_at: datetime


class BookingRuleError(ValueError):
    """Violación de una regla de negocio. `code` identifica cuál."""

    def __init__(self, code: str, message: str = "") -> None:
        super().__init__(message or code)
        self.code = code


@dataclass(frozen=True)
class Interval:
    """Intervalo simple, útil para pruebas y disponibilidades."""

    start_at: datetime
    end_at: datetime


def overlaps(a_start: datetime, a_end: datetime, b_start: datetime, b_end: datetime) -> bool:
    """True si [a_start, a_end) y [b_start, b_end) se solapan.

    Intervalo semiabierto: 10:00-11:00 y 11:00-12:00 NO chocan (RN-01).
    """
    return a_start < b_end and b_start < a_end


def find_conflict(
    start: datetime,
    end: datetime,
    existing: Iterable,
    exclude_id: Optional[int] = None,
):
    """Devuelve la primera reserva activa que choca con [start, end), o None.

    - Ignora reservas canceladas (RN-07).
    - `exclude_id` omite la propia reserva al reprogramar/reactivar (RN-10).
    - Sirve igual para RN-01 (reservas del tutor) y RN-02 (reservas del estudiante):
      quien llama decide qué lista pasa en `existing`.
    """
    if end <= start:
        raise BookingRuleError("invalid_interval", "La hora de fin debe ser posterior a la de inicio")
    for b in existing:
        if getattr(b, "status", STATUS_CONFIRMED) == STATUS_CANCELLED:
            continue
        if exclude_id is not None and getattr(b, "id", None) == exclude_id:
            continue
        if overlaps(start, end, b.start_at, b.end_at):
            return b
    return None


def validate_slot_alignment(start: datetime, availabilities: Iterable[_HasInterval], session_minutes: int) -> None:
    """RN-03 (decisión E-02): el inicio debe coincidir con un espacio del bloque que lo contiene.

    Con bloque 9:00-13:00 y sesiones de 60 min, solo valen 9:00, 10:00, 11:00 y 12:00; las 10:30 no,
    porque bloquearía dos espacios del tutor. Si `start` no cae en ningún bloque no hace nada:
    eso ya lo rechaza `validate_booking_window` con "outside_availability".
    """
    step = session_minutes * 60
    for block in availabilities:
        if block.start_at <= start < block.end_at:
            if (start - block.start_at).total_seconds() % step != 0:
                raise BookingRuleError(
                    "not_a_slot", "La hora de inicio no coincide con un espacio publicado por el tutor"
                )
            return


def seats_left(start: datetime, end: datetime, capacity: int, bookings: Iterable, subject_id: Optional[int] = None) -> int:
    """Cupos libres de la sesión [start, end) de un tutor (RN-01 reformulada + RN-13, cambio 2026-11-16).

    - Solo cuentan reservas activas (no canceladas) que se solapan con la sesión.
    - Si alguna se solapa sin ser **la misma sesión** (otro inicio u otro fin), el tutor está ocupado: 0.
    - Si `subject_id` se indica y la sesión ya tiene otra materia (G-02), tampoco hay cupo: 0.
    - Si no, quedan `capacity - reservas de esa sesión` (nunca negativo).
    Con capacity = 1 equivale a la regla original: una reserva ocupa el espacio.
    """
    taken = 0
    for b in bookings:
        if getattr(b, "status", STATUS_CONFIRMED) == STATUS_CANCELLED:
            continue
        if not overlaps(start, end, b.start_at, b.end_at):
            continue
        if b.start_at != start or b.end_at != end:
            return 0
        if subject_id is not None and getattr(b, "subject_id", subject_id) != subject_id:
            return 0
        taken += 1
    return max(capacity - taken, 0)


def free_slots_with_seats(
    day: date,
    availabilities: Iterable[_HasInterval],
    bookings: Iterable,
    session_minutes: int,
    now: datetime,
    min_notice_min: int = 60,
    subject_id: Optional[int] = None,
) -> list[tuple[datetime, int, int]]:
    """Sesiones con cupo de un tutor en `day`: lista de (inicio, cupos_libres, cupo_total).

    Parte cada bloque en sesiones de `session_minutes`, descarta las que no cumplen RN-04 y las que
    no tienen cupo según `seats_left`. El cupo sale del bloque (`capacity`, 1 si no existe).
    Se asume que cada bloque empieza y termina el mismo día.
    """
    delta = timedelta(minutes=session_minutes)
    bookings = list(bookings)
    result: list[tuple[datetime, int, int]] = []
    for block in sorted(availabilities, key=lambda a: a.start_at):
        if block.start_at.date() != day:
            continue
        capacity = getattr(block, "capacity", 1) or 1
        cur = block.start_at
        while cur + delta <= block.end_at:
            end = cur + delta
            try:
                validate_booking_window(cur, end, now, [block], min_notice_min)
            except BookingRuleError:
                cur = end
                continue
            left = seats_left(cur, end, capacity, bookings, subject_id)
            if left > 0:
                result.append((cur, left, capacity))
            cur = end
    return result


def free_slots(
    day: date,
    availabilities: Iterable[_HasInterval],
    bookings: Iterable,
    session_minutes: int,
    now: datetime,
    min_notice_min: int = 60,
) -> list[datetime]:
    """Horas de inicio con cupo de un tutor en `day` (RF-05). Ver `free_slots_with_seats`."""
    return [s for s, _, _ in free_slots_with_seats(day, availabilities, bookings, session_minutes, now, min_notice_min)]


def validate_booking_window(
    start: datetime,
    end: datetime,
    now: datetime,
    availabilities: Iterable[_HasInterval],
    min_notice_min: int = 60,
) -> None:
    """Valida RN-03 (dentro de disponibilidad) y RN-04 (futuro con anticipación).

    Lanza BookingRuleError con code: "invalid_interval" | "past" | "too_soon" | "outside_availability".
    """
    if end <= start:
        raise BookingRuleError("invalid_interval", "La hora de fin debe ser posterior a la de inicio")
    if start <= now:
        raise BookingRuleError("past", "No se puede reservar una hora pasada")
    if start < now + timedelta(minutes=min_notice_min):
        raise BookingRuleError("too_soon", f"Se requiere al menos {min_notice_min} min de anticipación")
    if not any(a.start_at <= start and end <= a.end_at for a in availabilities):
        raise BookingRuleError("outside_availability", "El horario está fuera de la disponibilidad del tutor")
