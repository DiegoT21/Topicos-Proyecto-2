# Plan de implementación

> Estado: **APROBADO**; actualizado el 2026-11-16 con el estado real y las tareas del cambio de especificación. Roles rotan por ciclo (Spec Lead / Dev Lead / QA-DevOps Lead). Cada tarea = un issue + una rama `feature/*` + un PR a `develop`.

| Ciclo | Objetivo | Tareas | Rol líder |
|---|---|---|---|
| 0 | Fundación | Repo, ramas, plantilla de PR, issues, specs aprobadas | Spec |
| 1 | Núcleo de reglas | `rules.py` (solapamiento, validaciones) + pruebas unitarias **antes** del resto | Dev |
| 2 | Reservar / cancelar | Modelos, servicios transaccionales, endpoints, prueba de **no doble reserva** | Dev |
| 3 | Disponibilidad y consulta | Bloques del tutor, listar tutores y espacios libres | Dev |
| 4 | Admin y frontend | Filtros, UI mínima, escape de HTML | QA (lo hizo Diego por tiempo; ver `ai-log.md` fila 14) |
| 5 | **Cambio de especificación** | Seguir el ciclo de `docs/decisions.md` | Todos |
| 6 | Cierre | Cobertura, QA independiente, evidencia, presentación, entrega | QA |

## Definición de hecho (por tarea)
Spec actualizada → criterio de aceptación con prueba → código → PR revisado por otra persona → QA → `ai-log.md` actualizado.

## Estado (2026-11-16)
| Ciclo | Estado | Dónde |
|---|---|---|
| 0–3 | Hecho | PR #7–#12, issues #1–#2 |
| 1 (Victor, Omar) | Hecho | Issues #3–#6, sus PR |
| Integración | Hecho | Rama `integracion` |
| Decisiones de specs (B-01, B-04, B-10) | Hecho | Rama `fix/decisiones-victor` |
| 4 | Hecho | Rama `feature/interfaz-web` |
| 5 | En curso | Rama `feature/cambio-sesiones-grupales` |
| 6 | Pendiente | QA independiente, presentación, entrega |

## Tareas del cambio de especificación: sesiones grupales (ciclo 5)
Pedido y decisiones G-01 a G-06 en `docs/decisions.md`. Criterios CA-23 a CA-28.

| # | Tarea | Archivos | Criterios |
|---|---|---|---|
| T1 | Columna `capacity` (1–6, por defecto 1) en `Availability`, con restricción en BD | `models.py` | CA-27 |
| T2 | Regla pura `seats_left(start, end, capacity, bookings, subject_id)`; `free_slots` devuelve también cupos | `rules.py` | CA-24, CA-25 |
| T3 | `services.book`: permitir varias reservas de la misma sesión hasta el cupo; otra materia = `tutor_conflict`; llena = `session_full` | `services.py`, `routers/bookings.py` | CA-23, CA-25, CA-26, CA-28 |
| T4 | API: `capacity` al publicar bloque; `seats_left` y `capacity` en los espacios | `schemas.py`, `routers/tutor.py`, `routers/catalog.py` | CA-24, CA-27 |
| T5 | Interfaz: campo cupo en "Soy tutor"; cupos libres en el riel | `frontend/tutor.html`, `frontend/index.html` | CA-24 |
| T6 | Pruebas nuevas y ajuste de las existentes | `tests/test_group_sessions.py`, `tests/test_rules.py` | CA-23 a CA-28 |
| T7 | Datos de demostración con un bloque grupal | `seed_demo.py` | — |

**Riesgo:** RN-01 es la regla crítica; las pruebas de doble reserva con cupo 1 (CA-02 a CA-04, `test_double_booking.py`) deben seguir pasando sin cambios.
