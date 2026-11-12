# AI Development Log

Regla: solo usos de IA que afectaron de forma significativa el desarrollo. Nunca inventar resultados; pegar salidas reales. Si no se usó IA, no se anota.
Decisión humana: **Aceptada**, **Aceptada parcialmente**, **Modificada** (qué se cambió) o **Rechazada** (por qué).

## 1. Registro principal
| # | Fecha | Quién | Actividad | IA utilizada | Solicitud | Resultado | Decisión |
|---|---|---|---|---|---|---|---|
| 1 | 2026-11-11 | Diego | Lectura del enunciado y del Proyecto 1; elección de dominio | Claude Code | Resumir reglas del Proyecto 2, comparar dominios y proponer estructura | Recomendó tutorías universitarias; creó estructura y borradores de `specs/` | **Aceptada parcialmente**: dominio aceptado; los borradores deben revisarse con el grupo |
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
