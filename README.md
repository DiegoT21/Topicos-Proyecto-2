# TutoríasUTP — Sistema de reservas de tutorías universitarias

Proyecto #2 · Tópicos Especiales II (Prof. Regis Rivera) · Desarrollo orientado por resultados y especificaciones (ODD → SDD).

**Equipo:** Diego Torres · Victor Rodriguez · Omar Jaramillo

## Outcome
Reducir a cero los conflictos de horario en tutorías y permitir que un estudiante encuentre y reserve un espacio con un tutor de su materia sin intervención de terceros. Ver [`specs/outcomes.md`](specs/outcomes.md).

## Flujo de trabajo
ODD → SDD → código → pruebas → valor al usuario.

## Estructura
```
specs/   outcomes, requirements, business-rules, architecture, data-model, api, acceptance-criteria, implementation-plan
docs/    ai-log, decisions (incluye el cambio de especificación), testing
src/     código
tests/   pruebas automatizadas
```

## Ramas y commits
- `main`: estable (solo por PR desde `develop`). `develop`: integración. `feature/*`, `fix/*`, `docs/*`, `test/*`.
- Commits convencionales en español: `feat(reservas): ...`, referenciando issue (`Refs #N`).
- Cada PR indica Developer / Reviewer / QA (ver `.github/pull_request_template.md`).

## Estado
Fase 0: specs en borrador, código pendiente.

## Cómo correrlo
_Se completa cuando exista código (Python 3.12, FastAPI, pytest)._
