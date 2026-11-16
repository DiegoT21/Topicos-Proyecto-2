# Modelo de datos

> Estado: **APROBADO**. Actualizado el 2026-11-16 por el cambio de especificación (sesiones grupales).

| Entidad | Campos principales | Notas |
|---|---|---|
| `subjects` | id, name, active | Materias |
| `tutors` | id, name, email, active, token | Email institucional único; `token` para publicar disponibilidad y ver su agenda |
| `tutor_subjects` | tutor_id, subject_id | Relación N:M (RN-06) |
| `students` | id, name, email | Email institucional único; `token` de acceso |
| `availabilities` | id, tutor_id, start_at, end_at, **capacity** | Bloques publicados (RN-03). Se guardan como intervalos concretos (datetime), no por día de semana, para coincidir con `rules.validate_booking_window`. `capacity` (1–6, por defecto 1) es el cupo de cada sesión del bloque (RN-13) |
| `bookings` | id, tutor_id, student_id, subject_id, start_at, end_at, status, created_at | `status`: confirmada / cancelada / realizada |

## Restricciones
- `end_at > start_at`.
- Solapamiento (RN-01, RN-02) se valida en `services.py` dentro de la transacción; considerar índice por `(tutor_id, start_at)` y `(student_id, start_at)`.
- Las reservas canceladas se conservan (historial) y no cuentan para el solapamiento ni para el cupo.
- `1 <= capacity <= 6` (restricción en BD y validación en la API).
- No hay migraciones: al agregar `capacity` hay que recrear la base local (`python src/seed_demo.py --reset`).
