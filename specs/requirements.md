# Requisitos (MVP)

> Estado: BORRADOR. Cada requisito enlaza con el outcome que sirve (ver `outcomes.md`).

## Requisitos funcionales
| ID | Requisito | Rol | Prioridad |
|---|---|---|---|
| RF-01 | El administrador puede crear, listar y desactivar materias | Admin | Alta |
| RF-02 | El administrador puede registrar tutores y asignarles materias | Admin | Alta |
| RF-03 | El tutor publica bloques de disponibilidad (día, hora inicio, hora fin) | Tutor | Alta |
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

## Supuestos
- Autenticación simple (identificación por correo institucional + token); decisión final en `docs/decisions.md`.
- Una sola zona horaria y una sola institución.
