# Outcomes (Fase 1 — ODD)

> Estado: **VALIDADO** (2026-11-12) con una encuesta a 5 estudiantes y 3 tutores (2 profesores y 1 tutora de maestría) que respondieron las 8 preguntas de la sección 6. Las respuestas se registran sin nombres en la sección 9. Las decisiones que salen de aquí se cierran en el issue #4.

## 1. Pregunta guía
¿Qué resultado queremos conseguir para el usuario? (no: ¿qué app queremos programar?)

## 2. Problema
Los estudiantes coordinan tutorías por WhatsApp, Instagram, correo, carteleras, el directorio de la universidad o preguntando al profesor al final de la clase. La encuesta confirma que esto provoca:
- **Demora para conseguir un horario**: desde un par de horas (si ya conocen al tutor) hasta una semana; lo típico es de 2 a 4 días. Algunos se rinden y buscan a otro (E1–E5). *[confirmado]*
- **No saber cuándo hay un tutor libre**: aunque el profesor publique horas fijas, los estudiantes le escriben por fuera (T1); en las horas de consulta abiertas se forma fila y no todos alcanzan (E4). *[confirmado]*
- **Cruces de horario**: el tutor atiende a otro estudiante porque le escribieron por medios distintos y se confundió (E1, 2 veces). *[confirmado]*
- **Inasistencias y cancelaciones tardías, de ambos lados**: el tutor olvidó anotar la cita y no llegó (E2), el tutor canceló 15 min antes (E3), los estudiantes no llegan y el cupo se pierde (T1, T2, T3). *[confirmado]*
- **Cambios que no llegan a tiempo**: un cambio de salón avisado por correo que el estudiante no vio (E5). *[nuevo]*
- **Sin registro común**: cada tutor lleva su propio control (lista personal de inasistencias T3, Google Calendar T2, historial que T1 quiere conservar). *[confirmado]*

## 3. Usuarios
| Usuario | Necesidad principal |
|---|---|
| Estudiante | Encontrar un espacio libre **a la hora que tiene disponible**, de la materia que necesita y, si puede, con un tutor recomendado; reservarlo sin perseguir a nadie |
| Tutor (profesor o estudiante avanzado) | Publicar su disponibilidad en un solo lugar, con la anticipación que necesita, saber de antemano qué tema trae el estudiante y no perder los cupos de quien no llega |
| Administrador (coordinación / departamento) | Ver el uso de las tutorías (reportes del departamento, T3) y gestionar tutores y materias |

## 4. Outcome (resultado esperado)
Reducir a **cero** los conflictos de horario en tutorías y permitir que un estudiante encuentre y reserve **en minutos**, sin intervención de terceros, un espacio disponible de su materia **a una hora que le sirva**, respetando la anticipación que pide cada tutor; y que los espacios cancelados queden **disponibles para otro estudiante** al instante.

## 5. Indicadores de éxito
| Indicador | Línea base (encuesta) | Meta |
|---|---|---|
| Reservas con doble asignación (tutor o estudiante) | Ocurre: E1 lo vivió 2 veces en el semestre | 0 |
| Tiempo desde que el estudiante busca hasta tener la reserva confirmada | De horas a 1 semana; típico 2–4 días | < 5 minutos (meta propuesta por el equipo) |
| Pasos para reservar (elegir materia → elegir espacio libre → confirmar) | Mensajes por varios canales hasta cuadrar | ≤ 3 |
| Reservas hechas sin contactar al tutor por otro canal | Ninguna: todo se coordina por mensajes, correo o en persona | 100 % del flujo cubierto en la app |
| Cancelaciones que liberan el espacio automáticamente | El cupo se pierde (T1, T2, T3) | 100 % |

## 6. Preguntas ODD (explorar antes de especificar)
**Valor para el estudiante**
1. ¿Cómo encuentran hoy a un tutor? ¿Cuánto tardan en conseguir un horario?
2. ¿Qué es más importante: elegir la materia, el tutor o la hora?
3. ¿Cuántas veces les ha pasado que la tutoría se cruzó o nadie llegó?

**Valor para el tutor**
4. ¿Cómo manejan hoy su disponibilidad? ¿Con cuánta anticipación quieren que reserven?
5. ¿Qué hacen cuando un estudiante cancela a último minuto?

**Alcance y riesgos**
6. ¿Una sesión es individual o también grupal? (MVP: individual.)
7. ¿Hace falta autenticación real o basta identificar por correo institucional?
8. ¿Qué datos personales se guardan y por cuánto tiempo?

Todas se respondieron en la encuesta (sección 9). En el formulario, las preguntas 6 a 8 se hicieron tanto a estudiantes como a tutores.

## 7. Fuera del alcance del MVP
Sesiones grupales con cupo, tutorías virtuales con enlace, pagos, notificaciones reales (correo/WhatsApp), límites por semana. Se reservan como candidatos para el **cambio de especificación** de mitad de proyecto (ver `docs/decisions.md`).

La encuesta da evidencia para priorizar estos candidatos: **sesiones grupales con cupo** (las aceptan 3 de 5 estudiantes y los 3 tutores), **anticipación mínima por tutor** y **registro de inasistencias** (los 3 tutores). Ver sección 9.4.

## 8. Trazabilidad
ODD (este archivo) → `requirements.md` → `business-rules.md` / `acceptance-criteria.md` → código → pruebas.

## 9. Validación con usuarios (2026-11-12)
Encuesta aplicada por Victor Rodriguez a 5 estudiantes (1.º a 4.º año, de distintas carreras) y 3 tutores (2 profesores y 1 estudiante de maestría que da tutorías). Se registran sin nombres: E1–E5 para estudiantes y T1–T3 para tutores.

### 9.1 Estudiantes
| Pregunta | E1 (1.er año, Ingeniería) | E2 (3.er año, Administración; trabaja medio tiempo) | E3 (2.º año, Medicina) | E4 (4.º año, Diseño) | E5 (1.er año, Economía) |
|---|---|---|---|---|---|
| 1. Cómo encuentra tutor y cuánto tarda | Grupos de WhatsApp o correo al ayudante; 2–3 días | Carteleras o recomendaciones; ~4 días, casi nadie atiende después de las 6:00 p. m. | Instagram o correo a alumnos de años superiores; horas si los conoce, hasta 1 semana si no | Pregunta al profesor al final de la clase; por correo, 2 días | Directorio y correos formales; si no contestan en 3 días, busca a otro |
| 2. Qué pesa más | Materia, luego hora | Hora | Tutor | Materia (tema) y luego hora | Tutor recomendado y hora |
| 3. Cruces o inasistencias | 2 veces: el tutor atendía a otro porque le escribieron por medios distintos | El tutor no llegó porque olvidó anotar la cita | El tutor canceló 15 min antes | En consulta abierta hay fila de 6 y no lo alcanzan a atender | Se equivocó de salón: el cambio llegó por correo y no lo vio |
| 6. Individual o grupal | Individual si está perdida; grupal de 3–4 para repasar antes de parciales | Individual | Grupal, máximo 5 | Individual | Individual al principio; luego grupal de máximo 3 |
| 7. Acceso | Correo institucional con inicio de sesión de Google/Microsoft | SSO institucional o código al correo, para que nadie reserve a su nombre | Correo institucional, si llega una confirmación | Correo institucional, sin registros ni contraseñas | Correo institucional con código de verificación |
| 8. Datos y tiempo | Nombre, correo, materia; teléfono solo para avisos de último minuto; el semestre | Nombre, correo, materia; sin teléfono; hasta fin del año académico | Nombre, correo, teléfono, materia; toda la carrera (historial) | Nombre y correo; lo que dure el curso | Nombre, correo, materia; mientras la reserva esté activa o máximo un semestre |

### 9.2 Tutores
| Pregunta | T1 (profesor de ciencias básicas) | T2 (estudiante de maestría, tutora de programación) | T3 (profesor del área administrativa) |
|---|---|---|---|
| 4. Disponibilidad y anticipación deseada | 4 h fijas por semana publicadas en el programa, pero le escriben por fuera. **24 h** de anticipación | Google Calendar compartido o mensajes uno a uno. **4–6 h** de anticipación | Abre espacios semana a semana según sus reuniones. **12 h** mínimo |
| 5. Cancelaciones e inasistencias | Espera 10 min; el cupo pudo ser para otro estudiante | Pide aviso; si no llegan dos veces seguidas, los deja de últimos en prioridad | Cierra a los 15 min y anota la inasistencia; la toma en cuenta después |
| 6. Individual o grupal | Grupal antes de exámenes, máximo 6; individual para casos puntuales | Individual (revisar código); grupal de hasta 3 si son del mismo proyecto | Individual de 20 min para dudas rápidas o grupal de máximo 4 para casos prácticos |
| 7. Validación del estudiante | Basta el correo institucional, para evitar bromas o spam | Inicio de sesión institucional (OAuth Google/Microsoft) | Cuenta institucional verificada que traiga la matrícula, para evitar suplantaciones |
| 8. Datos que necesita y retención | Nombre completo, correo, materia/sección y tema a tratar; todo el año | Nombre, correo, materia y un campo de notas con la duda; el semestre (control de horas) | Nombre, matrícula, correo, teléfono opcional y materia; al menos 1 año académico (reportes del departamento) |

### 9.3 Supuestos y conclusiones
| Supuesto / hipótesis | Resultado | Evidencia |
|---|---|---|
| Hay cruces de horario porque el tutor acepta a dos estudiantes a la misma hora | **Confirmado** | E1 |
| El estudiante no sabe cuándo hay un tutor libre y escribe por varios canales | **Confirmado** | E1–E5, T1 |
| Las cancelaciones sin aviso hacen perder el espacio | **Confirmado**, y ocurre de ambos lados (también el tutor falta o cancela tarde) | E2, E3, T1, T2, T3 |
| Nadie tiene un registro de las sesiones | **Confirmado**: cada tutor lleva el suyo y 3 de 3 quieren historial | T1, T2, T3 |
| El criterio principal de búsqueda es la materia | **Descartado parcialmente**: la hora es lo más mencionado (4 de 5); la materia es primera para 2 de 5 y el tutor para 2 de 5 | E1–E5 |
| Una anticipación mínima de 1 h es suficiente (RN-04) | **Descartado**: los tutores piden 4–6 h, 12 h y 24 h | T1, T2, T3 |
| Duración fija de 60 min (RN-05) | **Descartado parcialmente**: T3 da sesiones individuales de 20 min | T3 |
| Las sesiones son individuales (MVP) | **Confirmado parcialmente**: individual sirve a todos, pero 3 de 5 estudiantes y 3 de 3 tutores también quieren grupales (máximo 3 a 6 personas) | E1, E3, E5, T1, T2, T3 |
| Basta identificar por correo institucional + token | **Confirmado parcialmente**: todos aceptan el correo institucional, pero 5 de 8 piden verificar que el correo es suyo (código al correo o inicio de sesión institucional/SSO) para evitar suplantaciones | E1, E2, E5, T2, T3 |
| Bastan nombre, correo y materia | **Confirmado** como mínimo; el teléfono debe ser opcional (3 de 5 estudiantes no lo dan) y los tutores piden el **tema o duda** de la sesión | E1–E5, T1, T2 |

### 9.4 Implicaciones para las specs (a resolver en el issue #4)
- **Buscar por hora además de por tutor**: hoy el estudiante ve los espacios libres de un tutor (RF-05). La encuesta pide ver los espacios libres de **todos los tutores de una materia** en una fecha para elegir por hora (E1, E2, E4, E5), sin dejar de poder elegir tutor (E3, E5).
- **Anticipación mínima por tutor**: RN-04 usa 60 min global; ningún tutor lo acepta. Subir el valor por defecto (p. ej. 12 h) o permitir que cada tutor lo configure.
- **Verificación del correo**: con el diseño actual, cualquiera puede registrarse con un correo ajeno y recibir su token. Evaluar un código de verificación al correo o dejarlo documentado como riesgo conocido (`architecture.md`).
- **Tema de la sesión**: agregar a la reserva un campo opcional de tema/duda (T1, T2), validado contra HTML (RN-11).
- **Datos y retención**: teléfono opcional o fuera del modelo; definir retención (las respuestas van de 1 semestre a 1 año académico). La matrícula (T3) no se pide en el MVP (RNF-04).
- **Disponibilidad**: los tutores publican por semana (T3) o con horario fijo (T1); los bloques con fecha concreta del modelo actual sirven, pero cargar semana a semana puede ser tedioso.
- **Candidatos al cambio de especificación**, en orden de evidencia: sesiones grupales con cupo (6 de 8 lo aceptan), registro de inasistencias (3 de 3 tutores), duración variable de sesión (T3).
