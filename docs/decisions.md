# Decisiones y cambios de especificación

## Decisiones (ADR corto)
| Fecha | Decisión | Alternativas | Motivo | Quién |
|---|---|---|---|---|
| 2026-11-11 | Dominio: tutorías universitarias | Cancha deportiva | Reglas más ricas (tutor y estudiante), se diferencia del Proyecto 1 | Diego |
| 2026-11-13 | **Stack**: Python 3.12 + FastAPI + SQLAlchemy 2 + SQLite + Pydantic; pruebas con pytest y CI en GitHub Actions | Flask; Django; Node.js + Express; PostgreSQL | Es lo que ya usa el código de los PR #8–#13 (`requirements.txt`). FastAPI valida con Pydantic (RNF-02) y genera la documentación de la API; SQLite no necesita servidor y basta para un solo proceso. Python 3.13 queda fuera porque algunas dependencias fallan | Victor (propuesta, issue #4) |
| 2026-11-13 | **Autenticación**: el estudiante se identifica con su correo institucional y recibe un token (`X-Student-Token`); el tutor recibe su token cuando el admin lo registra (`X-Tutor-Token`); el admin usa un token configurado en `.env` (`X-Admin-Token`) | Login con contraseña; SSO institucional (Google/Microsoft); código de verificación al correo | Simplicidad y sin datos sensibles (RNF-04). La encuesta del ODD aceptó el correo institucional (8 de 8). Ver condiciones D-01 a D-04 | Victor (propuesta, issue #4) |

### Condiciones de la autenticación
| ID | Condición | Motivo | Estado |
|---|---|---|---|
| D-01 | Solo se aceptan correos del dominio institucional (`@utp.ac.pa`) para estudiantes y tutores | Hoy el código acepta cualquier correo (`schemas.py`), lo que contradice "correo institucional" | Requiere cambio de código (backlog B-01) |
| D-02 | **Riesgo conocido**: no se verifica que el correo pertenezca a quien se registra; alguien podría registrarse con un correo ajeno y quedarse con su token. Se acepta en el MVP y se documenta | La verificación por código o SSO requiere enviar correos o integrar un proveedor externo. 5 de 8 personas encuestadas la pidieron | Aceptado como riesgo; mejora en backlog B-02 |
| D-03 | El token del admin se define en `.env`; el valor por defecto de `config.py` (`cambia-este-token-admin`) solo sirve en desarrollo y no debe usarse al desplegar | Evitar un acceso de administrador con una clave conocida | Documentar en el README |
| D-04 | Se **confirma el token del tutor** (agregado por Diego en el PR #11): lo genera el sistema al registrar al tutor y se muestra una sola vez. **Limitación**: hoy no se puede recuperar ni cambiar | Sin token, cualquiera podría publicar disponibilidad a nombre de un tutor | Confirmado; recuperación en backlog B-03 |

## Decisiones sobre las specs (issue #4)
Revisión de `requirements.md`, `business-rules.md` y `acceptance-criteria.md` contra el código de los PR #8–#14 y la encuesta del ODD (`specs/outcomes.md`, PR #15). Los cambios en `business-rules.md` y `acceptance-criteria.md` se aplicarán **después de fusionar la pila #7–#12**, porque esos archivos tienen cambios de Diego en esos PR.

| ID | Hallazgo | Decisión | Dónde se aplica |
|---|---|---|---|
| E-01 | **RN-12** (agregada por Diego): los bloques de un tutor no se solapan, son del mismo día y futuros | **Confirmada**. Está implementada y probada (CA-14). Se moverá después de RN-11 en la tabla | `business-rules.md` (tras la pila) |
| E-02 | El sistema muestra espacios de duración fija (10:00, 11:00…), pero acepta reservas a cualquier hora: una reserva a las 10:30 bloquea dos espacios | El inicio de una reserva **debe coincidir con un espacio** calculado por `free_slots` (se agrega a RN-03). El ejemplo de solape parcial de CA-02 pasa a probarse a nivel de reglas, no de API | `business-rules.md`, `acceptance-criteria.md`; código en backlog B-04 |
| E-03 | Bloques contiguos (9–11 y 11–13): RN-03 rechaza una sesión que cruce el borde (observación de Omar en el PR #8) | Una sesión debe caber en **un solo bloque**; los bloques contiguos no se fusionan. Con E-02 el caso no ocurre desde la API | `business-rules.md` (nota en RN-03) |
| E-04 | RN-04: anticipación mínima de 1 h. La encuesta la descarta (los tutores piden 4–6 h, 12 h y 24 h) | El valor por defecto pasa a **12 h** (ya es configurable en `config.py`). La anticipación propia de cada tutor queda como candidato al cambio de especificación | `business-rules.md`; código en backlog B-05 |
| E-05 | RN-10 / CA-09: reactivar o reprogramar no tiene endpoint y CA-09 sigue pendiente | **Fuera del MVP**. La lógica (`exclude_id` en `rules.py`) ya existe y está probada para cuando se implemente | `business-rules.md`, `acceptance-criteria.md` |
| E-06 | RN-09: el estado `realizada` existe, pero nadie puede asignarlo; RN-08 no deja cancelar al tutor | Se mantiene así en el MVP y se agrupa en el candidato **"gestión de la sesión por el tutor"** (marcar realizada, marcar inasistencia y cancelar) | Backlog B-06 |
| E-07 | RN-11 exige formato de teléfono, pero el modelo no tiene teléfono | Se quita el teléfono de RN-11. En la encuesta, 3 de 5 estudiantes no quieren darlo | `business-rules.md` |
| E-08 | La nota de `business-rules.md` dice "verificar e insertar en una misma transacción", pero el código usa un lock de proceso | Se corrige la nota: lock de proceso + verificación dentro del lock, probado con hilos (PR #14). **Limitación**: protege un solo proceso; con varios haría falta una restricción en BD | `business-rules.md` |
| E-09 | `acceptance-criteria.md`: RN-06, RN-09, RF-01, RF-02 y RF-09 no tienen criterio; CA-12 a CA-14 están desordenados; CA-02 debe apuntar a `tests/test_double_booking.py` | Se agregan los criterios faltantes con las pruebas que ya existen y se reordena | `acceptance-criteria.md` (tras la pila) |
| E-10 | Varias specs siguen en "BORRADOR" | `requirements.md` pasa a **aprobado** en este issue; el resto, al aplicar E-01 a E-09 | Este PR y el siguiente |

Los cambios de `requirements.md` (RF-01, RF-02, RF-03 y backlog) se aplican en este mismo PR.

## Cambio de especificación a mitad del proyecto
Ciclo a documentar, con evidencia (commits/PR) en cada paso:
`cambio solicitado → actualizar spec → actualizar criterios de aceptación → actualizar plan/tareas → modificar código → modificar pruebas → ver resultados`

| Paso | Evidencia (enlace a commit/PR/archivo) |
|---|---|
| Cambio solicitado | |
| Spec actualizada | |
| Criterios de aceptación | |
| Plan / tareas | |
| Código | |
| Pruebas | |
| Resultado | |

Candidatos si el profesor no da uno propio: sesiones grupales con cupo, política de cancelación (mínimo X horas), límite de tutorías por semana, tutoría virtual con enlace.
