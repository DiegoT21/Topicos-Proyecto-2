# Issues iniciales (copiar y pegar en GitHub → Issues → New issue)

---
## #1 · Núcleo de reglas de reserva (`rules.py`)
**Responsable:** Diego · **Rama:** `feature/nucleo-reglas` · **Specs:** RN-01, RN-02, RN-03, RN-04, RN-10
- [ ] `overlaps` con intervalo semiabierto
- [ ] `find_conflict` ignora reservas canceladas y permite excluir la propia (`exclude_id`)
- [ ] `validate_booking_window` (disponibilidad, hora pasada, anticipación mínima)
- [ ] Pruebas unitarias en `tests/test_rules.py`

---
## #2 · Modelos, configuración y base de datos
**Responsable:** Diego · **Rama:** `feature/modelos-bd` · **Specs:** `data-model.md`
- [ ] Modelos `Subject, Tutor, Student, Availability, Booking`
- [ ] `config.py` (zona `America/Panama`, duración 60 min, anticipación 60 min)
- [ ] SQLite local; `requirements.txt` (Python 3.12)

---
## #3 · Validar el ODD con usuarios reales
**Responsable:** Victor · **Rama:** `docs/validacion-odd` · **Specs:** `outcomes.md`
- [ ] Preguntar a 3–5 estudiantes y 1–2 tutores usando las preguntas de la sección 6
- [ ] Registrar respuestas (anónimas) y qué *[supuestos]* se confirman o descartan
- [ ] Ajustar problema, outcome e indicadores

---
## #4 · Cerrar decisiones pendientes de las specs
**Responsable:** Victor · **Rama:** `docs/cierre-specs`
- [ ] Confirmar stack y autenticación (`docs/decisions.md`)
- [ ] Revisar `requirements.md`, `business-rules.md` y `acceptance-criteria.md` buscando huecos o contradicciones
- [ ] Priorizar el backlog y elegir candidatos de cambio de especificación

---
## #5 · Infraestructura de pruebas y CI
**Responsable:** Omar · **Rama:** `chore/ci-pruebas`
- [ ] `tests/conftest.py` con BD temporal (con `tempfile`, compatible con Windows)
- [ ] Workflow de GitHub Actions que corra `pytest` en cada PR
- [ ] Activar protección de `main` y `develop` (PR + 1 aprobación)

---
## #6 · Prueba obligatoria de no doble reserva
**Responsable:** Omar · **Rama:** `test/doble-reserva` · **Specs:** CA-02, CA-03, CA-04, RN-01, RN-02
- [ ] Mismo tutor, mismo horario → conflicto
- [ ] Mismo tutor, horario solapado parcialmente → conflicto
- [ ] Sesiones consecutivas (10–11 y 11–12) → permitido
- [ ] Mismo estudiante con dos tutores a la misma hora → conflicto
- [ ] Reserva cancelada no bloquea
- Escribir contra la interfaz definida en `docs/team-plan.md`.
