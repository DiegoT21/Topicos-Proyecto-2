# TutoríasUTP — Sistema de reservas de tutorías universitarias

Proyecto #2 · Tópicos Especiales II (Prof. Regis Rivera) · Desarrollo orientado por resultados y especificaciones (ODD → SDD → código → pruebas → valor).

**Equipo:** Diego Torres · Victor Rodriguez · Omar Jaramillo

## Problema y resultado buscado
Los estudiantes coordinan tutorías por WhatsApp, correo o en el pasillo: tardan de 2 a 4 días en conseguir horario, hay cruces y los cupos de quien no llega se pierden (encuesta a 5 estudiantes y 3 tutores, `specs/outcomes.md`).

**Outcome:** cero conflictos de horario y que un estudiante reserve en minutos, sin intermediarios, un espacio de su materia a una hora que le sirva.

## Qué hace
- **Estudiante:** entra con su correo `@utp.ac.pa`, elige materia y día, ve los espacios libres de **todos** los tutores ordenados por hora, reserva en 3 pasos y cancela.
- **Tutor:** publica bloques de disponibilidad con cupo por sesión (1 = individual, hasta 6 = grupal) y ve su agenda.
- **Coordinación:** crea y desactiva materias, registra tutores y consulta reservas con filtros.
- **Reglas críticas:** ni el tutor ni el estudiante pueden tener sesiones solapadas; una sesión grupal acepta reservas hasta su cupo (`specs/business-rules.md`).

## Cómo correrlo (Python 3.12)
```bash
py -3.12 -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/seed_demo.py --reset   # datos FICTICIOS de demostración; imprime el código de cada tutor
python scripts/run_demo.py        # http://localhost:8000
```
- Estudiante: <http://localhost:8000/> · Tutor: `/tutor.html` · Coordinación: `/admin.html` · API: `/docs`
- La clave de coordinación por defecto (`cambia-este-token-admin`) **solo sirve en desarrollo**. Para cualquier otro uso, define `ADMIN_TOKEN` en `.env` (decisión D-03).
- No hay migraciones: si cambia el modelo, recrea la base con `python src/seed_demo.py --reset`.

## Pruebas
```bash
pytest -q        # 110 pruebas; cobertura 97 % (docs/testing.md)
```
La regla de no doble reserva tiene su suite dedicada: `tests/test_double_booking.py`.

## Estructura
```
specs/   outcomes, requirements, business-rules, architecture, data-model, api, acceptance-criteria, implementation-plan
docs/    ai-log (uso de IA), decisions (incluye el cambio de especificación), testing, evidencia/
src/     app/ (FastAPI: reglas, modelos, servicios, rutas), frontend/ (HTML/CSS/JS), seed_demo.py
tests/   pytest
scripts/ run_demo.py
```

## Recorrido ODD → SDD → código → pruebas
| Etapa | Dónde |
|---|---|
| ODD: problema, outcome, validación con usuarios | `specs/outcomes.md` |
| SDD: requisitos, reglas, criterios, arquitectura, API | `specs/` |
| Decisiones y cambio de especificación (sesiones grupales) | `docs/decisions.md` |
| Código | `src/` |
| Pruebas y resultados | `tests/`, `docs/testing.md`, `docs/evidencia/` |
| Uso de IA | `docs/ai-log.md` |

## Flujo de trabajo
- `main` estable (solo por PR desde `develop`); `develop` integración; ramas `feature/*`, `fix/*`, `docs/*`, `test/*`, `chore/*`.
- Commits convencionales en español con `Refs #N`; cada PR indica Developer, Reviewer y QA (`.github/pull_request_template.md`).
- CI: `.github/workflows/tests.yml` corre las pruebas en cada PR.

## Stack
Python 3.12, FastAPI, SQLAlchemy 2, SQLite, Pydantic, pytest, HTML/CSS/JS sin framework, GitHub Actions. Detalle y motivos en `specs/architecture.md` y `docs/decisions.md`.
