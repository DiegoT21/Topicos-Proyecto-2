# Tareas de Victor y Omar — Ciclo 1

Repo: https://github.com/DiegoT21/Topicos-Proyecto-2 (privado; acepten la invitación)
Proyecto: **TutoríasUTP**, sistema de reservas de tutorías universitarias. Proyecto #2 de Tópicos Especiales II.

Lo que ya hizo Diego: núcleo de reglas, modelos y BD, reservar/cancelar, disponibilidad del tutor y listado del admin con filtros. Hay **76 pruebas pasando**. Está en los PR #7 a #12.

---

## Antes de empezar (los dos)

1. Lean `README.md`, `docs/team-plan.md` y la carpeta `specs/` (empiecen por `outcomes.md`).
2. Clonen el repo y creen su rama **desde `develop`**:
   ```bash
   git clone https://github.com/DiegoT21/Topicos-Proyecto-2.git
   cd Topicos-Proyecto-2
   git switch develop
   git switch -c <nombre-de-su-rama>
   ```
3. Para correr las pruebas (Python **3.12**; con 3.13 fallan algunas dependencias):
   ```bash
   py -3.12 -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   pytest -q
   ```
   Nota: el código vive en las ramas de los PR #8 a #12 hasta que se fusionen. Para correr las pruebas antes, usen `git switch feature/filtros-admin`.
4. **Commits en español**, formato `tipo(alcance): descripción`, por ejemplo `docs(odd): agrega respuestas de entrevistas`, y referencien el issue con `Refs #N`.
5. Cada PR usa la plantilla (Developer / Reviewer / QA) y va a `develop`. **Nadie aprueba su propio PR.**
6. Anoten en `docs/ai-log.md` **todo uso significativo de IA**: actividad, IA, solicitud, resultado y decisión. Si la IA se equivoca o rechazan un cambio, va en las secciones 2 y 3. No inventen resultados.

---

## Victor — Product / Spec Lead

### Issue #3 · Validar el ODD con usuarios reales
Rama: `docs/validacion-odd` · Archivo: `specs/outcomes.md`
- [ ] Preguntar a **3–5 estudiantes y 1–2 tutores** con las preguntas de la sección 6 de `outcomes.md`.
- [ ] Registrar las respuestas (sin nombres) y marcar qué *[supuestos]* se confirman o se descartan.
- [ ] Ajustar el problema, el outcome y los indicadores según lo que respondan.
- Revisa: Diego.

### Issue #4 · Cerrar decisiones pendientes de las specs
Rama: `docs/cierre-specs`
- [ ] Confirmar en `docs/decisions.md` el **stack** (Python + FastAPI + SQLite) y la **autenticación** (correo institucional + token).
- [ ] Revisar `requirements.md`, `business-rules.md` y `acceptance-criteria.md` buscando huecos o contradicciones. Diego añadió la regla RN-12 (los bloques de disponibilidad de un tutor no se solapan) y el token del tutor; **confírmenlos o corríjanlos**.
- [ ] Priorizar el backlog y elegir **2–3 candidatos de cambio de especificación** para la mitad del proyecto (por ejemplo: sesiones grupales con cupo, cancelación con mínimo de horas, límite de tutorías por semana).
- Revisa: Omar.

### Revisión
- [ ] Revisar el **PR #9** (modelos y BD). Comentar en GitHub y dejar anotado quién fue Reviewer.

---

## Omar — QA / DevOps Lead

### Issue #5 · Infraestructura de pruebas y CI
Rama: `chore/ci-pruebas`
- [ ] `tests/conftest.py` con una BD temporal compatible con Windows (usar `tempfile` o SQLite en memoria). Hoy cada archivo de pruebas define su propia base; unifíquenla sin romper las 76 pruebas.
- [ ] Workflow de **GitHub Actions** (`.github/workflows/`) que corra `pytest` en cada PR con Python 3.12.
- [ ] Activar la **protección de `main` y `develop`** (PR obligatorio y 1 aprobación) en *Settings → Branches*.
- Revisa: Diego.

### Issue #6 · Prueba obligatoria de no doble reserva
Rama: `test/doble-reserva` · Specs: CA-02, CA-03, CA-04, RN-01, RN-02
Ya hay pruebas básicas en `tests/test_bookings_api.py`. Su tarea es una suite dedicada en `tests/test_double_booking.py`:
- [ ] Mismo tutor, mismo horario → 409.
- [ ] Mismo tutor, solape parcial (10:30 con sesión de 60 min) → 409.
- [ ] Sesiones consecutivas (10–11 y 11–12) → permitido.
- [ ] Mismo estudiante con dos tutores a la misma hora → 409.
- [ ] Reserva cancelada no bloquea el espacio.
- [ ] **Dos reservas simultáneas (hilos) sobre el mismo espacio: solo una gana.** Es la carrera que falló en el Proyecto 1.
- Revisa: Victor.

### Revisión
- [ ] Revisar el **PR #8** (núcleo de reglas). Leer `src/app/rules.py` y sus pruebas.

---

## Orden de fusión de los PR (importante)

Los PR de Diego están **apilados**: cada uno parte del anterior. Se fusionan en este orden, y solo tras una revisión de otra persona:

`#7 → #8 → #9 → #10 → #11 → #12`

Si fusionan fuera de orden, el diff de los siguientes se rompe.

---

## Cómo nos evalúan (del enunciado)

Se evalúa el **proceso**, no cuánto código generó la IA. Cuenta que haya: issues, ramas, commits identificables, PR con revisión, pruebas automatizadas, `ai-log.md` honesto y un cambio de especificación a mitad del proyecto, documentado de punta a punta (en `docs/decisions.md`).

En el Proyecto 1 faltaron aprobaciones de terceros y quedaron líneas PENDIENTE sin cerrar. Esta vez evitémoslo.
