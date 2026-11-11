# Modelo de datos

> Estado: BORRADOR.

| Entidad | Campos principales | Notas |
|---|---|---|
| `subjects` | id, name, active | Materias |
| `tutors` | id, name, email, active | Email institucional único |
| `tutor_subjects` | tutor_id, subject_id | Relación N:M (RN-06) |
| `students` | id, name, email | Email institucional único; `token` de acceso |
| `availabilities` | id, tutor_id, start_at, end_at | Bloques publicados (RN-03). Se guardan como intervalos concretos (datetime), no por día de semana, para coincidir con `rules.validate_booking_window` |
| `bookings` | id, tutor_id, student_id, subject_id, start_at, end_at, status, created_at | `status`: confirmada / cancelada / realizada |

## Restricciones
- `end_at > start_at`.
- Solapamiento (RN-01, RN-02) se valida en `services.py` dentro de la transacción; considerar índice por `(tutor_id, start_at)` y `(student_id, start_at)`.
- Las reservas canceladas se conservan (historial) y no cuentan para el solapamiento.
