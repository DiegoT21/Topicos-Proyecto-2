# Pruebas

## Mínimo exigido por el enunciado y dónde se cumple
| Exigencia | Dónde | Pruebas |
|---|---|---|
| Pruebas unitarias | `tests/test_rules.py` (reglas puras: solape, ventana, alineación, cupos, espacios libres) y `tests/test_models.py` (restricciones de BD) | 34 + 7 |
| Pruebas de reglas críticas | RN-01, RN-02, RN-03, RN-13 en `test_rules.py`, `test_double_booking.py`, `test_group_sessions.py` | ver tabla de reglas abajo |
| Validación de conflictos de reserva | `tests/test_double_booking.py` (incluye 8 hilos contra el mismo espacio) y `tests/test_group_sessions.py` (8 hilos contra cupo 3) | 6 + 9 |
| **No permitir doble reserva (obligatoria)** | `tests/test_double_booking.py` | 6 |
| Validaciones de usuario | `tests/test_bookings_api.py` y `tests/test_availability_api.py`: correo institucional, HTML en nombres, horas pasadas, fuera de bloque, inicio fuera de espacio, cupo 0 o 7, parámetros de filtros | — |
| Pruebas de criterios de aceptación | Cada CA de `specs/acceptance-criteria.md` nombra su prueba en la columna "Prueba" (CA-01 a CA-28; CA-09 está fuera del MVP) | — |

Total por archivo: `test_rules.py` 34 · `test_availability_api.py` 25 · `test_bookings_api.py` 19 · `test_admin_filters.py` 10 · `test_group_sessions.py` 9 · `test_models.py` 7 · `test_double_booking.py` 6 = **110**.

## Reglas críticas y su prueba
| Regla | Prueba |
|---|---|
| RN-01 tutor sin sesiones distintas solapadas | `test_double_booking.py`: mismo horario, solape parcial, hilos; `test_rules.py`: overlaps, find_conflict, seats_left |
| RN-02 estudiante sin solapes | `test_double_booking.py`: dos tutores a la misma hora; `test_bookings_api.py`: solape parcial con otro tutor; `test_group_sessions.py`: dos veces la misma sesión |
| RN-03 dentro de un bloque y en un espacio | `test_bookings_api.py`: fuera de disponibilidad, inicio fuera de espacio; `test_rules.py`: alineación |
| RN-07 cancelada no bloquea | `test_double_booking.py`, `test_bookings_api.py`, `test_group_sessions.py` (el cupo vuelve) |
| RN-13 cupo por sesión | `test_group_sessions.py` (CA-23 a CA-28) |

## Cómo correr
```bash
pytest -q
pytest -q --cov=src/app --cov-report=term-missing   # cobertura (requiere pytest-cov)
```
En GitHub, `.github/workflows/tests.yml` (de Omar) corre `pytest` con Python 3.12 en cada PR y en cada push a `main` y `develop`.

## Resultados (salidas reales en `docs/evidencia/`)
| Momento | Pruebas | Archivo |
|---|---|---|
| Núcleo de reglas | 19 passed | `pytest_nucleo_reglas.txt` |
| Modelos y BD | 26 passed | `pytest_modelos_bd.txt` |
| Reservar y cancelar | 41 passed | `pytest_reservas.txt` |
| Disponibilidad y catálogo | 66 passed | `pytest_disponibilidad.txt` |
| Filtros del admin | 76 passed | `pytest_filtros_admin.txt` |
| Integración + decisiones de Victor | 93 passed | `pytest_decisiones_victor.txt` |
| Interfaz web | 95 passed | `pytest_interfaz.txt` |
| Cambio de especificación (sesiones grupales) | 110 passed | `pytest_cambio_grupales.txt` |
| Cobertura final | 110 passed, **97 %** de `src/app` (568 sentencias, 15 sin cubrir) | `pytest_cobertura.txt` |

Lo no cubierto es sobre todo arranque (`main.py` lifespan, `database.get_db` real) y dos ramas defensivas de `services.py` (tutor o materia inactivos al reservar).

## Pruebas en navegador
`docs/evidencia/prueba_interfaz.md`: 12 pasos en Chromium (navegador integrado de la app de escritorio) contra `scripts/run_demo.py`, incluidos los de sesiones grupales. **Las ejecutó Claude Code (IA) por encargo de Diego**, no una persona distinta del desarrollador.

## QA independiente
**No se realizó QA independiente.** Omar (rol QA) no pudo hacerlo antes de la entrega y el equipo decidió entregar igualmente, dejándolo dicho aquí.

En su lugar hay una **QA funcional hecha por IA** (Claude Code, por encargo de Diego) en Chrome, con 19 pasos sobre las tres pantallas: `docs/evidencia/qa/qa_ia_2026-11-16.md`. Encontró **2 errores de la interfaz** (un mensaje de rechazo que se borraba y un `alert()` bloqueante), ambos corregidos; las 110 pruebas siguen pasando. No hay capturas: la extensión del navegador no pudo tomarlas.

Esto no reemplaza la revisión de una persona distinta al desarrollador: sigue siendo una limitación de la entrega.

## Limitaciones conocidas
- El lock contra reservas simultáneas protege **un solo proceso** (E-08).
- No probado: otros navegadores, móvil real, PostgreSQL, varias instancias del servidor.
