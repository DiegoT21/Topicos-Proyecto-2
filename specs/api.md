# API (borrador)

| Método | Ruta | Descripción | Req | Auth |
|---|---|---|---|---|
| GET | `/api/subjects` | Materias activas | RF-01 | — |
| GET | `/api/tutors?subject_id=` | Tutores por materia | RF-04 | — |
| GET | `/api/tutors/{id}/slots?date=YYYY-MM-DD` | Espacios libres del día | RF-05 | — |
| POST | `/api/bookings` | Reservar `{tutor_id, student_id/token, subject_id, start_at}` → 201 / 409 / 422 | RF-06, RF-07 | estudiante |
| POST | `/api/bookings/{id}/cancel` | Cancelar reserva → 200 / 403 / 404 | RF-08 | estudiante |
| POST | `/api/tutor/availability` | Publicar bloque | RF-03 | tutor |
| GET | `/api/tutor/agenda` | Agenda del tutor | RF-09 | tutor |
| GET | `/api/admin/bookings?tutor_id&subject_id&date_from&date_to&status` | Reservas con filtros | RF-10 | admin |
| POST/PUT | `/api/admin/subjects`, `/api/admin/tutors` | Gestión | RF-01, RF-02 | admin |

## Códigos de error
- `409` conflicto de horario (RN-01, RN-02, RN-10).
- `422` validación (RN-03, RN-04, RN-11).
- `403` sin permiso (RN-08); `401` credencial inválida.
