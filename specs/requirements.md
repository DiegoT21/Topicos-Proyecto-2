# Requisitos (MVP)

> Estado: **APROBADO** (2026-11-13, issue #4), pendiente de la revisión de Omar. Cada requisito enlaza con el outcome que sirve (ver `outcomes.md`). Las decisiones que justifican los cambios están en `docs/decisions.md`.

## Requisitos funcionales
| ID | Requisito | Rol | Prioridad |
|---|---|---|---|
| RF-01 | El administrador puede crear y desactivar materias; las materias activas se listan para todos | Admin | Alta |
| RF-02 | El administrador registra tutores con las materias que ofrecen | Admin | Alta |
| RF-03 | El tutor publica bloques de disponibilidad con fecha, hora de inicio y hora de fin (ver RN-12) | Tutor | Alta |
| RF-04 | El estudiante lista tutores por materia | Estudiante | Alta |
| RF-05 | El estudiante ve los espacios libres de un tutor en un día | Estudiante | Alta |
| RF-06 | El estudiante reserva un espacio libre (sesión individual) | Estudiante | Alta |
| RF-07 | El sistema rechaza una reserva que choque con otra del tutor o del estudiante | Sistema | **Crítica** |
| RF-08 | El estudiante cancela su reserva y el espacio queda libre | Estudiante | Alta |
| RF-09 | El tutor ve su agenda de sesiones | Tutor | Media |
| RF-10 | El administrador consulta reservas con filtros (tutor, materia, fecha, estado) | Admin | Media |

## Requisitos no funcionales
| ID | Requisito |
|---|---|
| RNF-01 | Toda regla crítica (RF-07) tiene prueba automatizada |
| RNF-02 | Validar y escapar toda entrada de usuario (evitar el XSS que apareció en el Proyecto 1) |
| RNF-03 | Fechas y horas en una sola zona horaria definida (`America/Panama`) |
| RNF-04 | No guardar datos sensibles (sin contraseñas reales ni pagos) |
| RNF-05 | Reproducible: instalar y correr con comandos documentados en el README |

## Backlog (fuera del MVP actual)
Requisitos detectados al revisar las specs contra el código y la encuesta del ODD. La prioridad y los candidatos al cambio de especificación se definen en la parte 3 del issue #4.

| ID | Requisito | Origen |
|---|---|---|
| B-01 | Aceptar solo correos del dominio institucional (`@utp.ac.pa`) | `decisions.md` D-01 |
| B-02 | Verificar que el correo pertenece a quien se registra (código al correo o SSO institucional) | `decisions.md` D-02; encuesta (5 de 8) |
| B-03 | Recuperar o cambiar el token de un tutor | `decisions.md` D-04 |
| B-04 | Rechazar reservas cuyo inicio no coincida con un espacio de `free_slots` | `decisions.md` E-02 |
| B-05 | Cambiar el valor por defecto de la anticipación mínima a 12 h | `decisions.md` E-04; encuesta (3 de 3 tutores) |
| B-06 | Gestión de la sesión por el tutor: marcar realizada, marcar inasistencia y cancelar | `decisions.md` E-06; encuesta (3 de 3 tutores) |
| B-07 | El administrador cambia las materias de un tutor y puede desactivarlo | Hueco de RF-02: hoy las materias solo se asignan al crear el tutor y no hay forma de desactivarlo |
| B-08 | El administrador ve también las materias inactivas | Hueco de RF-01 |
| B-09 | El tutor borra o corrige un bloque de disponibilidad publicado | Hueco de RF-03 |
| B-10 | El estudiante ve los espacios libres de **todos** los tutores de una materia en una fecha y elige por hora | Encuesta: la hora es el criterio más mencionado (4 de 5). Permite cumplir el indicador "≤ 3 pasos para reservar" de `outcomes.md` (materia → espacio → confirmar, con el estudiante ya identificado) |

## Supuestos
- Autenticación por correo institucional + token, con las condiciones D-01 a D-04 de `docs/decisions.md`.
- Una sola zona horaria y una sola institución.
