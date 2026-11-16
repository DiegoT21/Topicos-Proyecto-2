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

## Backlog priorizado (fuera del MVP actual)
Requisitos detectados al revisar las specs contra el código y la encuesta del ODD. Ordenados por prioridad (issue #4, parte 3) con este criterio: primero lo que corrige una decisión ya tomada o un desperdicio en el MVP, luego lo que acerca al outcome, después lo que pidieron los usuarios y al final lo de bajo impacto. Los marcados como **candidato** son opciones para el cambio de especificación de mitad de proyecto (`docs/decisions.md`). El responsable de cada ítem se asigna en un issue propio.

| Orden | ID | Requisito | Prioridad | Motivo | Origen |
|---|---|---|---|---|---|
| 1 | B-01 | Aceptar solo correos del dominio institucional (`@utp.ac.pa`) | Alta | Hace cumplir la decisión de autenticación; hoy el código la contradice | `decisions.md` D-01 |
| 2 | B-04 | Rechazar reservas cuyo inicio no coincida con un espacio de `free_slots` | Alta | Evita que una reserva bloquee dos espacios del tutor (desperdicio que el outcome quiere eliminar) | `decisions.md` E-02 |
| 3 | B-10 | El estudiante ve los espacios libres de **todos** los tutores de una materia en una fecha y elige por hora | Alta | Sin esto no se cumple el indicador "≤ 3 pasos para reservar" (materia → espacio → confirmar); la hora es el criterio más mencionado (4 de 5) | Encuesta; `outcomes.md` |
| 4 | B-11 | Sesiones grupales con cupo (máximo configurable por sesión) | Media — **candidato 1** | La aceptan 6 de 8 encuestados (grupos de 3 a 6) | Encuesta; `outcomes.md` §7 |
| 5 | B-06 | Gestión de la sesión por el tutor: marcar realizada, marcar inasistencia y cancelar | Media — **candidato 2** | La piden los 3 tutores y da uso al estado `realizada` (RN-09), hoy sin flujo | `decisions.md` E-06; encuesta (3 de 3 tutores) |
| 6 | B-05 | Cada tutor define su anticipación mínima (el valor global de 1 h queda como valor por defecto) | Media — **candidato 3** | Los 3 tutores piden más de 1 h y no coinciden entre sí | `decisions.md` E-04; encuesta (3 de 3 tutores) |
| 7 | B-07 | El administrador cambia las materias de un tutor y puede desactivarlo | Media | Hueco de RF-02: hoy las materias solo se asignan al crear el tutor y no hay forma de desactivarlo | Revisión de specs |
| 8 | B-09 | El tutor borra o corrige un bloque de disponibilidad publicado | Media | Hueco de RF-03: un bloque mal publicado no se puede arreglar | Revisión de specs |
| 9 | B-02 | Verificar que el correo pertenece a quien se registra (código al correo o SSO institucional) | Baja | Lo piden 5 de 8, pero requiere enviar correos o un proveedor externo; queda como riesgo aceptado (D-02) | `decisions.md` D-02 |
| 10 | B-03 | Recuperar o cambiar el token de un tutor | Baja | Hoy el admin puede registrar de nuevo al tutor como solución temporal | `decisions.md` D-04 |
| 11 | B-08 | El administrador ve también las materias inactivas | Baja | Solo afecta la consulta del admin | Hueco de RF-01 |

## Supuestos
- Autenticación por correo institucional + token, con las condiciones D-01 a D-04 de `docs/decisions.md`.
- Una sola zona horaria y una sola institución.