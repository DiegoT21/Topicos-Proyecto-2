# Reglas de negocio

> Estado: **APROBADO** (2026-11-16). Aplica las decisiones E-01 a E-08 de `docs/decisions.md` (issue #4). Cada regla tiene al menos una prueba automatizada (ver `acceptance-criteria.md`).

| ID | Regla | Criticidad |
|---|---|---|
| RN-01 | **Un tutor no puede tener dos sesiones distintas activas que se solapen** (intervalo `[inicio, fin)`). Varias reservas de **la misma sesión** (mismo inicio y misma materia) se permiten hasta el cupo de RN-13; una reserva de otra materia en esa sesión es conflicto (cambio 2026-11-16, G-02 y G-03) | Crítica |
| RN-02 | **Un estudiante no puede tener dos sesiones activas que se solapen**, aunque sean con tutores distintos | Crítica |
| RN-03 | Solo se reserva dentro de un bloque de disponibilidad publicado por el tutor, y **el inicio debe coincidir con un espacio de ese bloque** (inicio del bloque + múltiplos de la duración de sesión). Una sesión debe caber en **un solo bloque**: los bloques contiguos no se fusionan (E-02, E-03) | Alta |
| RN-04 | Solo se reservan horas futuras, con anticipación mínima configurable (por defecto 1 h, global para el MVP; ver E-04) | Alta |
| RN-05 | Duración fija de sesión (por defecto 60 min), configurable | Media |
| RN-06 | El tutor solo ofrece materias que tiene asignadas | Media |
| RN-07 | Una reserva cancelada **no bloquea** el espacio; queda en el historial | Alta |
| RN-08 | Solo el estudiante dueño (o el admin) puede cancelar una reserva | Alta |
| RN-09 | Estados válidos: `confirmada`, `cancelada`, `realizada`. Transiciones: confirmada → cancelada / realizada. En el MVP nadie asigna `realizada` (E-06, backlog B-06) | Media |
| RN-10 | Reactivar o reprogramar una reserva debe volver a validar RN-01 y RN-02 excluyendo la propia reserva. **Fuera del MVP** (E-05): la lógica existe y está probada en `rules.find_conflict(exclude_id=...)` | Alta |
| RN-11 | Correo con formato válido y del **dominio institucional** (`@utp.ac.pa`), guardado en minúsculas; nombre sin HTML. No se pide teléfono (E-07, D-01) | Media |
| RN-12 | Los bloques de disponibilidad de un tutor no pueden solaparse entre sí, deben empezar y terminar el mismo día y ser futuros (E-01) | Media |
| RN-13 | Cada bloque define un **cupo por sesión** entre 1 y 6 (1 = individual). Una sesión acepta reservas activas hasta llenar el cupo; llena, se rechaza con 409 `session_full` y deja de mostrarse como libre (cambio 2026-11-16, G-01 y G-05) | Crítica |

## Notas
- **Sesiones grupales** (RN-13): el cupo vive en el bloque; con cupo 1 todo funciona como antes del cambio.
- La detección de solapamiento es **semiabierta**: una sesión 10:00–11:00 y otra 11:00–12:00 **no** chocan.
- Con RN-03 el solape **parcial del mismo tutor** no puede ocurrir desde la API (10:30 se rechaza como `not_a_slot`); se prueba en `tests/test_rules.py`. El solape parcial **del estudiante con tutores distintos** sí puede ocurrir si sus bloques empiezan a horas distintas, y se prueba en la API.
- Verificación e inserción ocurren **dentro de un lock de proceso** (`services.py`), probado con hilos en `tests/test_double_booking.py`. **Limitación** (E-08): protege un solo proceso; con varios haría falta una restricción en la base de datos.
