# API (borrador)

| Método | Ruta | Descripción | Req | Auth |
|---|---|---|---|---|
| GET | `/api/subjects` | Materias activas | RF-01 | — |
| GET | `/api/tutors?subject_id=` | Tutores por materia (sin correo ni token) | RF-04 | — |
| GET | `/api/tutors/{id}/slots?date=YYYY-MM-DD` | Espacios libres del día | RF-05 | — |
| POST | `/api/students` | Registrar estudiante `{name, email}` → 201 con `token` / 409 correo repetido / 422 (HTML en nombre) | RN-11 | — |
| POST | `/api/bookings` | Reservar `{tutor_id, subject_id, start_at}` → 201 / 409 / 422. El estudiante se identifica con el header `X-Student-Token` (401 si falta o es inválido) | RF-06, RF-07 | estudiante |
| POST | `/api/bookings/{id}/cancel` | Cancelar reserva → 200 / 403 / 404 / 409 (ya cancelada). Header `X-Student-Token` (dueño) o `X-Admin-Token` | RF-08 | estudiante / admin |
| POST | `/api/tutor/availability` | Publicar bloque `{start_at, end_at}` → 201 / 409 solape / 422. Header `X-Tutor-Token` | RF-03 | tutor |
| GET | `/api/tutor/agenda` | Agenda del tutor. Header `X-Tutor-Token` | RF-09 | tutor |
| GET | `/api/admin/bookings?tutor_id&subject_id&status&date_from&date_to&limit&offset` | Reservas con filtros combinables; incluye nombres de tutor, estudiante y materia (texto de usuario: escapar al mostrar). `date_from`/`date_to` inclusivos; `limit` 1–500 (100 por defecto). 422 si el estado es inválido o el rango está invertido | RF-10 | admin |
| POST | `/api/admin/subjects`, `/api/admin/tutors` | Crear materia / tutor (el tutor se crea con `subject_ids` y devuelve su `token`). Header `X-Admin-Token` | RF-01, RF-02 | admin |
| DELETE | `/api/admin/subjects/{id}` | Desactiva la materia (no la borra) | RF-01 | admin |

## Códigos de error
- `409` conflicto de horario (RN-01, RN-02, RN-10) o transición inválida (RN-09).
- `422` validación (RN-03, RN-04, RN-06, RN-11).
- `403` sin permiso (RN-08); `401` credencial inválida; `404` recurso inexistente.
- El cuerpo de error es `{"detail": {"code": "<codigo>", "message": "..."}}`. Códigos: `tutor_conflict`, `student_conflict`, `outside_availability`, `past`, `too_soon`, `subject_not_taught`, `invalid_transition`, `forbidden`, `invalid_token`, `email_taken`, `tutor_not_found`, `subject_not_found`, `booking_not_found`.
