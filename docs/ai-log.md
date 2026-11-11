# AI Development Log

Regla: solo usos de IA que afectaron de forma significativa el desarrollo. Nunca inventar resultados; pegar salidas reales. Si no se usó IA, no se anota.
Decisión humana: **Aceptada**, **Aceptada parcialmente**, **Modificada** (qué se cambió) o **Rechazada** (por qué).

## 1. Registro principal
| # | Fecha | Quién | Actividad | IA utilizada | Solicitud | Resultado | Decisión |
|---|---|---|---|---|---|---|---|
| 1 | 2026-11-11 | Diego | Lectura del enunciado y del Proyecto 1; elección de dominio | Claude Code | Resumir reglas del Proyecto 2, comparar dominios y proponer estructura | Recomendó tutorías universitarias; creó estructura y borradores de `specs/` | **Aceptada parcialmente**: dominio aceptado; los borradores deben revisarse con el grupo |
| 2 | 2026-11-11 | Diego | Reparto de roles/issues y núcleo de reglas (issue #1) | Claude Code | Repartir el trabajo entre 3 roles; implementar `rules.py` y pruebas unitarias desde las specs | `docs/team-plan.md`, `rules.py` y 19 pruebas; 19 passed (`docs/evidencia/pytest_nucleo_reglas.txt`) | **Aceptada**: Diego debe revisar el código antes del PR; Omar revisa |
| 3 | 2026-11-11 | Diego | Modelos, config y BD (issue #2) | Claude Code | Implementar modelos SQLAlchemy, `config.py`, `database.py` y pruebas de restricciones según `data-model.md` | 7 pruebas nuevas; 26 passed en total (`docs/evidencia/pytest_modelos_bd.txt`). La IA creó la rama desde `develop` y falló al importar `rules.py` (aún no fusionado); se rebasó sobre `feature/nucleo-reglas` | **Modificada**: disponibilidad como intervalos datetime (no día de semana) y `created_at` en hora local; `data-model.md` actualizado |
| 4 | 2026-11-11 | Diego | Reservar y cancelar (ciclo 2) | Claude Code | Implementar `services.py` (reserva con lock), esquemas, endpoints `/api/students`, `/api/bookings`, `/cancel` y pruebas de API | 15 pruebas nuevas; 41 passed en total (`docs/evidencia/pytest_reservas.txt`) | **Aceptada parcialmente**: el lock solo protege un proceso (limitación documentada en `services.py`); identificación por header `X-Student-Token` en vez de `student_id` en el cuerpo (`api.md` actualizado). Diego debe revisar el código |

## 2. Respuestas incorrectas de la IA
| Fecha | Qué se pidió | Qué respondió mal | Cómo se detectó | Corrección | Evidencia |
|---|---|---|---|---|---|

## 3. Cambios rechazados
| Fecha | Cambio propuesto | Motivo del rechazo |
|---|---|---|

## 4. Decisiones humanas importantes
| Fecha | Decisión | Quién |
|---|---|---|
| 2026-11-11 | Dominio: tutorías universitarias | Diego |
