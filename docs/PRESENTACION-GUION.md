# Guion de presentación (8–10 min)

El presentador se elige al azar: **los tres deben poder dar todo el guion.** Las diapositivas están en el deck de Slides (link en la entrega); las notas del orador repiten lo esencial.

| # | Diapositiva | Qué decir (idea principal) | Tiempo |
|---|---|---|---|
| 1 | Portada | Resolvimos la coordinación de tutorías empezando por el resultado para el usuario | 0:30 |
| 2 | Problema | Encuesta a 5 estudiantes y 3 tutores: 2–4 días para conseguir horario, cruces, cupos perdidos. Muestra pequeña | 1:00 |
| 3 | Outcome | Cero cruces, reservar en minutos y en ≤ 3 pasos, cancelar libera el espacio | 0:45 |
| 4 | Recorrido | ODD → SDD → código → pruebas → valor; todo en el repo (`specs/` manda) | 0:45 |
| 5 | Reglas | RN-01 y RN-02 (no doble reserva), RN-03 (espacio exacto), RN-13 (cupo) | 1:00 |
| 6 | Arquitectura | FastAPI + SQLite; reglas puras en `rules.py`; lock al reservar | 0:45 |
| 7 | Demo | En vivo: reservar, ver que desaparece, cancelar, ver que vuelve; sesión grupal | 2:00 |
| 8 | Pruebas | 110 pruebas, 97 %; 8 hilos contra un espacio, entra uno | 0:45 |
| 9 | Cambio | Sesiones grupales: un commit por paso del ciclo; el hallazgo con `session_full` | 1:00 |
| 10 | Proceso | Roles, issues, ramas, PR con revisor, CI | 0:30 |
| 11 | IA | Cuatro errores de la IA y cómo se detectaron | 0:30 |
| 12 | Cierre | Qué funciona, límites, invitar al cambio en vivo | 0:30 |

## Antes de presentar (checklist)
- [ ] `pytest -q` → 110 passed.
- [ ] `python src/seed_demo.py --reset` y guardar los códigos de tutor que imprime.
- [ ] `python scripts/run_demo.py` y abrir <http://localhost:8000>, `/tutor.html`, `/admin.html`.
- [ ] Clave de coordinación de la demo: la de `config.py` (solo desarrollo).
- [ ] Elegir el día de mañana en la demo (los bloques empiezan mañana).
- [ ] Tener abierto `docs/CAMBIOS_EN_VIVO.md`.

## Demo paso a paso (2 min)
1. Estudiante: entrar con `demo@gmail.com` → muestra el error del correo institucional. Entrar con `demo@utp.ac.pa`.
2. Cálculo I, mañana: el riel muestra a Ana, Bruno (grupal) y Darío por hora.
3. Reservar 10:00 con Ana → desaparece del riel y sale en "Mis reservas".
4. Cancelarla → vuelve al riel.
5. Reservar 10:00 con Bruno (grupal) → "3 cupos de 4".
6. Tutor: entrar con el código de Ana, publicar un bloque, intentar publicarlo otra vez → "se solapa".
7. Coordinación: filtrar reservas por estado `cancelada`.

## Preguntas probables
- *¿Dónde está la prueba de no doble reserva?* `tests/test_double_booking.py` (de Omar), CA-02 a CA-04.
- *¿Cómo se trazó el cambio?* `docs/decisions.md`, tabla con los 7 commits.
- *¿Qué hizo cada uno?* Diapositiva 10 y `docs/ai-log.md` (columna "Quién").
