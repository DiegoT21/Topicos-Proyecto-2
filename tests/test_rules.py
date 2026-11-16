"""Pruebas unitarias del núcleo de reglas. Cubren CA-02, CA-03, CA-05, CA-06, CA-09 (parte pura)."""
from dataclasses import dataclass
from datetime import datetime, timedelta

import pytest

from app.rules import (
    BookingRuleError,
    Interval,
    find_conflict,
    overlaps,
    validate_booking_window,
)


@dataclass
class B:
    id: int
    start_at: datetime
    end_at: datetime
    status: str = "confirmada"


def t(h, m=0):
    return datetime(2026, 12, 1, h, m)


# --- overlaps (RN-01) ---
def test_overlap_mismo_horario():
    assert overlaps(t(10), t(11), t(10), t(11))


def test_overlap_parcial():
    assert overlaps(t(10), t(11), t(10, 30), t(11, 30))


def test_consecutivas_no_chocan():  # CA-03
    assert not overlaps(t(10), t(11), t(11), t(12))
    assert not overlaps(t(11), t(12), t(10), t(11))


def test_separadas_no_chocan():
    assert not overlaps(t(8), t(9), t(10), t(11))


# --- find_conflict ---
def test_conflicto_mismo_horario():  # CA-02
    assert find_conflict(t(10), t(11), [B(1, t(10), t(11))]).id == 1


def test_conflicto_parcial():  # CA-02 (10:30 con sesión de 60 min)
    assert find_conflict(t(10, 30), t(11, 30), [B(1, t(10), t(11))]) is not None


def test_sin_conflicto_consecutiva():  # CA-03
    assert find_conflict(t(11), t(12), [B(1, t(10), t(11))]) is None


def test_cancelada_no_bloquea():  # RN-07
    assert find_conflict(t(10), t(11), [B(1, t(10), t(11), "cancelada")]) is None


def test_realizada_si_bloquea():
    assert find_conflict(t(10), t(11), [B(1, t(10), t(11), "realizada")]) is not None


def test_exclude_id_permite_reprogramar_a_si_misma():  # RN-10
    assert find_conflict(t(10), t(11), [B(1, t(10), t(11))], exclude_id=1) is None


def test_exclude_id_no_oculta_otras():  # RN-10 / CA-09
    existing = [B(1, t(10), t(11)), B(2, t(10), t(11))]
    assert find_conflict(t(10), t(11), existing, exclude_id=1).id == 2


def test_intervalo_invalido():
    with pytest.raises(BookingRuleError) as e:
        find_conflict(t(11), t(10), [])
    assert e.value.code == "invalid_interval"


# --- validate_booking_window (RN-03, RN-04) ---
NOW = datetime(2026, 12, 1, 8, 0)
AV = [Interval(t(9), t(13))]


def code_of(start, end, av=AV, notice=60):
    with pytest.raises(BookingRuleError) as e:
        validate_booking_window(start, end, NOW, av, notice)
    return e.value.code


def test_ventana_valida():
    validate_booking_window(t(10), t(11), NOW, AV, 60)


def test_fuera_de_disponibilidad():  # CA-05
    assert code_of(t(13), t(14)) == "outside_availability"


def test_sesion_que_se_sale_del_bloque():  # CA-05
    assert code_of(t(12, 30), t(13, 30)) == "outside_availability"


def test_hora_pasada():  # CA-06
    assert code_of(t(7), t(8)) == "past"


def test_sin_anticipacion_minima():  # CA-06
    assert code_of(t(8, 30), t(9, 30)) == "too_soon"


def test_anticipacion_exacta_permitida():
    validate_booking_window(NOW + timedelta(minutes=60), NOW + timedelta(minutes=120), NOW, [Interval(t(8), t(13))], 60)


def test_sin_disponibilidades():
    assert code_of(t(10), t(11), av=[]) == "outside_availability"


# --- seats_left (RN-01 reformulada + RN-13, cambio 2026-11-16) ---
from app.rules import seats_left  # noqa: E402


@dataclass
class BS:
    id: int
    start_at: datetime
    end_at: datetime
    subject_id: int = 1
    status: str = "confirmada"


def test_cupos_sin_reservas():
    assert seats_left(t(10), t(11), 3, []) == 3


def test_cupos_misma_sesion_y_materia():
    assert seats_left(t(10), t(11), 3, [BS(1, t(10), t(11)), BS(2, t(10), t(11))], subject_id=1) == 1


def test_cupos_no_negativos_y_canceladas_no_cuentan():
    full = [BS(n, t(10), t(11)) for n in range(4)]
    assert seats_left(t(10), t(11), 3, full) == 0
    assert seats_left(t(10), t(11), 3, [BS(1, t(10), t(11), status="cancelada")]) == 3


def test_otra_materia_ocupa_la_sesion():
    assert seats_left(t(10), t(11), 3, [BS(1, t(10), t(11), subject_id=2)], subject_id=1) == 0


def test_solape_con_otra_sesion_no_deja_cupo():
    assert seats_left(t(10), t(11), 3, [BS(1, t(10, 30), t(11, 30))]) == 0


def test_cupo_1_equivale_a_la_regla_original():
    assert seats_left(t(10), t(11), 1, [BS(1, t(10), t(11))]) == 0
    assert seats_left(t(11), t(12), 1, [BS(1, t(10), t(11))]) == 1  # consecutiva


# --- validate_slot_alignment (RN-03 / E-02, B-04) ---
from app.rules import validate_slot_alignment  # noqa: E402


def test_alineado_al_espacio():
    for h in (9, 10, 11, 12):
        validate_slot_alignment(t(h), [Interval(t(9), t(13))], 60)


def test_no_alineado_rechazado():
    with pytest.raises(BookingRuleError) as e:
        validate_slot_alignment(t(10, 30), [Interval(t(9), t(13))], 60)
    assert e.value.code == "not_a_slot"


def test_alineacion_relativa_al_inicio_del_bloque():
    validate_slot_alignment(t(10, 30), [Interval(t(9, 30), t(13, 30))], 60)  # 9:30, 10:30...
    with pytest.raises(BookingRuleError):
        validate_slot_alignment(t(10), [Interval(t(9, 30), t(13, 30))], 60)


def test_fuera_de_bloque_no_decide():
    validate_slot_alignment(t(15, 10), [Interval(t(9), t(13))], 60)  # lo rechaza validate_booking_window


# --- free_slots (RF-05) ---
from datetime import date

from app.rules import free_slots

DAY = date(2026, 12, 1)


def hours(slots):
    return [s.hour for s in slots]


def test_free_slots_parte_el_bloque_en_sesiones():
    assert hours(free_slots(DAY, [Interval(t(9), t(13))], [], 60, NOW, 60)) == [9, 10, 11, 12]


def test_free_slots_excluye_reservadas_y_canceladas_no():
    bookings = [B(1, t(10), t(11)), B(2, t(11), t(12), "cancelada")]
    assert hours(free_slots(DAY, [Interval(t(9), t(13))], bookings, 60, NOW, 60)) == [9, 11, 12]


def test_free_slots_descarta_pasado_y_sin_anticipacion():
    # NOW = 08:00, anticipación 60 -> la primera sesión válida empieza a las 09:00
    assert hours(free_slots(DAY, [Interval(t(7), t(11))], [], 60, NOW, 60)) == [9, 10]


def test_free_slots_bloque_que_no_cabe():
    assert free_slots(DAY, [Interval(t(9), t(9, 30))], [], 60, NOW, 60) == []


def test_free_slots_ignora_otros_dias():
    other = Interval(datetime(2026, 12, 2, 9), datetime(2026, 12, 2, 13))
    assert free_slots(DAY, [other], [], 60, NOW, 60) == []
