# Reparto del equipo — Ciclos 0 y 1

Los roles **rotan por ciclo** (enunciado). Cada tarea = un issue + una rama + un PR a `develop`. Nadie aprueba su propio PR.

## Roles en este ciclo
| Persona | Rol | Foco |
|---|---|---|
| Diego Torres | Architecture / Development Lead | Código del núcleo de reglas, modelos y BD |
| Victor Rodriguez | Product / Spec Lead | Validar ODD, cerrar decisiones de specs, backlog |
| Omar Jaramillo | QA / DevOps Lead | Infraestructura de pruebas, CI, prueba de no doble reserva |

## Tareas
| Issue | Tarea | Responsable | Rama | Revisa |
|---|---|---|---|---|
| 1 | Núcleo de reglas (`rules.py`) + pruebas unitarias | Diego | `feature/nucleo-reglas` | Omar |
| 2 | Modelos SQLAlchemy, config y base de datos | Diego | `feature/modelos-bd` | Victor |
| 3 | Validar el ODD con 3–5 estudiantes/tutores y actualizar `outcomes.md` | Victor | `docs/validacion-odd` | Diego |
| 4 | Revisar las specs y cerrar decisiones pendientes (stack, autenticación, duración) | Victor | `docs/cierre-specs` | Omar |
| 5 | Infraestructura de pruebas (`conftest.py`, pytest) y CI en GitHub Actions | Omar | `chore/ci-pruebas` | Diego |
| 6 | Prueba obligatoria de **no doble reserva** (CA-02, CA-03, CA-04) | Omar | `test/doble-reserva` | Victor |

Orden: 1 y 5 pueden empezar ya y en paralelo; 6 depende de la interfaz de 1 (definida en el issue); 2 después de 1; 3 y 4 son independientes del código.

## Interfaz acordada del núcleo (para que Omar escriba pruebas sin esperar)
Módulo `src/app/rules.py`, funciones puras (sin BD):
```python
overlaps(a_start, a_end, b_start, b_end) -> bool          # intervalo semiabierto [inicio, fin)
find_conflict(start, end, existing) -> Booking | None      # existing: sesiones activas (no canceladas)
validate_booking_window(start, end, now, availabilities, min_notice_min) -> None  # lanza BookingRuleError
class BookingRuleError(ValueError): code: str              # "outside_availability" | "too_soon" | "past"
```

## Reglas del equipo (del Proyecto 1)
- Commits convencionales en español: `feat(reglas): ...`, con `Refs #N`.
- Usar la plantilla de PR (Developer / Reviewer / QA).
- Todo uso significativo de IA va a `docs/ai-log.md` (incluye respuestas incorrectas y cambios rechazados).
- No fusionar PR sin revisión de otra persona. Activar protección de rama en GitHub.
