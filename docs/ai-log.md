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
| 5 | 2026-11-11 | Diego | Disponibilidad, catálogo y admin (ciclo 3) | Claude Code | Implementar `free_slots`, endpoints de materias/tutores/espacios libres, publicación de disponibilidad, agenda y pruebas | 25 pruebas nuevas; 66 passed (`docs/evidencia/pytest_disponibilidad.txt`) | **Modificada**: se añadió `token` al tutor y la regla RN-12 (sin solape de bloques), que no estaban en las specs; ya reflejadas en `business-rules.md`, `data-model.md` y `api.md`. Diego debe revisar |
| 6 | 2026-11-11 | Diego | Filtros del admin (RF-10) | Claude Code | Implementar `GET /api/admin/bookings` con filtros combinables, paginación y pruebas | 10 pruebas nuevas; 76 passed (`docs/evidencia/pytest_filtros_admin.txt`) | **Aceptada**: se añadieron paginación (`limit`/`offset`) y nombres en la respuesta, no pedidos en la spec; `api.md` actualizado. Diego debe revisar |
| 7 | 2026-11-11 | Omar | Infraestructura de pruebas y CI (issue #5) | Claude Code | Unificar la BD de pruebas en `tests/conftest.py` compatible con Windows y crear el workflow de GitHub Actions con Python 3.12 | `conftest.py` con SQLite en memoria por prueba, 4 archivos de prueba migrados y `.github/workflows/tests.yml`; 76 passed en local. El workflow aún no se había ejecutado en GitHub al registrar esto | **Aceptada parcialmente**: la protección de ramas no se automatizó (requiere permisos de admin; la activa Diego en Settings) |
| 8 | 2026-11-11 | Omar | Suite de no doble reserva (issue #6, rama `test/doble-reserva`, PR #14) | Claude Code | Escribir `tests/test_double_booking.py` con los casos de CA-02, CA-03, CA-04, RN-01 y RN-02, incluida la carrera con hilos | 6 pruebas nuevas; 82 passed en total. La prueba con 8 hilos usa SQLite en archivo temporal; al quitar temporalmente el lock de `services.book` falló 3 de 3 veces, y con el lock pasó 3 de 3 | **Aceptada**: no se encontró carrera en el código; el lock sigue siendo solo de proceso (limitación ya documentada) |
| 9 | 2026-11-12 | Victor | Validación del ODD (issue #3) | Claude | Pasar las respuestas de la encuesta (5 estudiantes, 3 tutores) a `specs/outcomes.md` sin nombres, marcar supuestos y ajustar problema, outcome e indicadores | Tablas de respuestas anónimas (E1–E5, T1–T3), 10 supuestos marcados (confirmados / descartados), outcome e indicadores con línea base, implicaciones para el issue #4 | **Modificada**: Victor pidió verificar el documento contra el issue #3; se corrigieron generalizaciones (ver sección 2), un conteo (4 → 5 de 8 piden verificación del correo) y se generalizaron las materias de los profesores para mantener el anonimato |
| 10 | 2026-11-12 | Victor | Validación del ODD, preguntas 6–8 (issue #3) | Claude | Simular respuestas a las preguntas 6–8 mientras no se conseguían usuarios | Tabla de respuestas simuladas, marcada como simulación | **Rechazada**: se reemplazó por las respuestas reales de la encuesta (ver sección 3) |

## 2. Respuestas incorrectas de la IA
| Fecha | Qué se pidió | Qué respondió mal | Cómo se detectó | Corrección | Evidencia |
|---|---|---|---|---|---|
| 2026-11-12 | Resumir las respuestas de usuarios en `outcomes.md` | Generalizó más allá de las respuestas: lo dicho por un solo usuario presentado como tendencia, líneas base en "0 %" que nadie midió, una meta propia sin indicar que era del equipo y un conteo equivocado (4 de 8 en vez de 5 de 8) | Victor pidió verificar el documento contra el issue #3 y se comparó cada afirmación con las respuestas | Se reescribió con la evidencia exacta (qué usuario lo dijo), la meta se marcó como propuesta del equipo y se corrigió el conteo | `specs/outcomes.md`, rama `docs/validacion-odd` |

## 3. Cambios rechazados
| Fecha | Cambio propuesto | Motivo del rechazo |
|---|---|---|
| 2026-11-12 | Usar respuestas simuladas con IA para las preguntas 6–8 del ODD | El issue #3 pide validar con usuarios reales; se reemplazaron por las respuestas de la encuesta |

## 4. Decisiones humanas importantes
| Fecha | Decisión | Quién |
|---|---|---|
| 2026-11-11 | Dominio: tutorías universitarias | Diego |
