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


def free_slots(
    day: date,
    availabilities: Iterable[_HasInterval],
    bookings: Iterable,
    session_minutes: int,
    now: datetime,
    min_notice_min: int = 60,
) -> list[datetime]:
    """Horas de inicio libres de un tutor en `day` (RF-05).

    Parte cada bloque de disponibilidad en sesiones consecutivas de `session_minutes`, y descarta
    las que no cumplen RN-04 (pasado / sin anticipación) o chocan con reservas activas (RN-01).
    Se asume que cada bloque empieza y termina el mismo día.
    """
    delta = timedelta(minutes=session_minutes)
    bookings = list(bookings)
    slots: list[datetime] = []
    for block in sorted(availabilities, key=lambda a: a.start_at):
        if block.start_at.date() != day:
            continue
        cur = block.start_at
        while cur + delta <= block.end_at:
            end = cur + delta
            try:
                validate_booking_window(cur, end, now, [block], min_notice_min)
            except BookingRuleError:
                cur = end
                continue
            if find_conflict(cur, end, bookings) is None:
                slots.append(cur)
            cur = end
    return slots


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
