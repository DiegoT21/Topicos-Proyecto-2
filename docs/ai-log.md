# AI Development Log

Regla: solo usos de IA que afectaron de forma significativa el desarrollo. Nunca inventar resultados; pegar salidas reales. Si no se usó IA, no se anota.
Decisión humana: **Aceptada**, **Aceptada parcialmente**, **Modificada** (qué se cambió) o **Rechazada** (por qué).

## 1. Registro principal
| # | Fecha | Quién | Actividad | IA utilizada | Solicitud | Resultado | Decisión |
|---|---|---|---|---|---|---|---|
| 1 | 2026-11-11 | Diego | Lectura del enunciado y del Proyecto 1; elección de dominio | Claude Code | Resumir reglas del Proyecto 2, comparar dominios y proponer estructura | Recomendó tutorías universitarias; creó estructura y borradores de `specs/` | **Aceptada parcialmente**: dominio aceptado; los borradores deben revisarse con el grupo |
| 11 | 2026-11-13 | Victor | Cierre de decisiones de las specs (issue #4, partes 1 y 2) | Claude | Revisar `requirements.md`, `business-rules.md` y `acceptance-criteria.md` contra el código de los PR #8–#14 y la encuesta del ODD; proponer la redacción de las decisiones de stack y autenticación | Se encontraron huecos y contradicciones (correo institucional no exigido, reservas fuera de los espacios, RN-04 de 1 h, RN-10 sin endpoint, `realizada` sin uso, RN-11 con teléfono inexistente, entre otros). Se redactaron `docs/decisions.md` (D-01 a D-04, E-01 a E-10) y `specs/requirements.md` (RF-01 a RF-03 y backlog B-01 a B-10) | _pendiente de revisión de Victor_ |

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
