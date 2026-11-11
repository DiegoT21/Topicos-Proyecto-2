"""Pruebas unitarias del núcleo de reglas. Cubren CA-02, CA-03, CA-05, CA-06, CA-09 (parte pura)."""
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app.rules import (  # noqa: E402
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
