# Cambios que el profesor podría pedir en vivo

El enunciado dice que en la presentación pueden pedir un cambio. Para cualquiera, seguir **el mismo ciclo** que el cambio de sesiones grupales (`docs/decisions.md`), aunque sea en versión corta y en voz alta:

1. Repetir el pedido y escribirlo en `docs/decisions.md`.
2. Decir qué regla o requisito cambia (`specs/business-rules.md`, `specs/requirements.md`).
3. Escribir el criterio de aceptación nuevo (`specs/acceptance-criteria.md`).
4. Cambiar el código: casi siempre `src/app/config.py`, `src/app/rules.py` o `src/app/services.py`.
5. Agregar o ajustar la prueba y correr `pytest -q`.
6. Mostrarlo en la interfaz (`python scripts/run_demo.py`).

Rutas relativas a la raíz del repo. Después de tocar el modelo: `python src/seed_demo.py --reset` (no hay migraciones).

## Solo configuración (los más rápidos)
`src/app/config.py`, clase `Settings`; también por variables de entorno o `.env`.

| Pedido | Cambio | Prueba a mirar |
|---|---|---|
| Sesiones de 45 o 30 min | `session_minutes` (RN-05). Lo usan `services.book`, `rules.validate_slot_alignment` y `rules.free_slots_with_seats` | `test_availability_api.py::test_espacios_libres_del_dia` espera 4 espacios de 60 min: con 30 min serían 8 |
| Reservar con más anticipación (p. ej. 12 h) | `min_notice_minutes` (RN-04) | `test_rules.py::test_sin_anticipacion_minima` |
| Otro dominio de correo | `institutional_domain` (RN-11) | `test_bookings_api.py::test_correo_no_institucional_rechazado` |
| Otra zona horaria | `business_timezone`; la usa `local_now()` | — |

## Cambios de código
### 1. Cupo máximo distinto de 6
- `src/app/schemas.py`, `AvailabilityCreate.capacity`: `Field(1, ge=1, le=6)` → cambiar `le`.
- `src/app/models.py`, `Availability.__table_args__`: `CheckConstraint("capacity BETWEEN 1 AND 6")`.
- `src/frontend/tutor.html`: opciones del `<select id="capacity">`.
- Prueba: `test_group_sessions.py::test_publicar_cupo_valido_e_invalido`.

### 2. Anticipación mínima por tutor (candidato 3 del issue #4)
- `models.Tutor`: columna `min_notice_minutes` (por defecto `settings.min_notice_minutes`).
- `services.book`: pasar `tutor.min_notice_minutes` a `validate_booking_window`.
- `routers/catalog._tutor_free_slots`: pasar el del tutor a `free_slots_with_seats`.
- Prueba nueva: tutor con 24 h; reservar a 2 h → 422 `too_soon`.

### 3. Límite de reservas activas por estudiante (p. ej. 3 por semana)
- `services.book`, antes de insertar: contar `Booking` del estudiante con `status == "confirmada"` en la semana de `start_at`; si llega al límite, `BookingRuleError("weekly_limit")` y agregar `"weekly_limit": 409` a `_STATUS` en `routers/bookings.py`.
- Prueba: 3 reservas pasan, la 4.ª da 409.

### 4. El tutor marca una sesión como realizada o inasistencia (candidato 2)
- Nuevo endpoint en `routers/tutor.py`: `POST /api/tutor/bookings/{id}/done` con `X-Tutor-Token`; validar que la reserva es suya y está `confirmada` (RN-09).
- Para inasistencia, agregar el estado a `VALID_STATUSES` y al `CheckConstraint` de `Booking` (recrear la BD).

### 5. Cancelación solo hasta X horas antes
- `services.cancel`: si no es admin y `booking.start_at - local_now() < timedelta(hours=X)` → `BookingRuleError("too_late")`, y `"too_late": 409` en `_STATUS`.
- Prueba: reservar en `datetime(2099, …)` pasa; para probar el rechazo, llamar a `services.cancel` con un `now` cercano (agregar parámetro `now` como en `book`).

### 6. Campo "tema o duda" en la reserva (lo pidieron los tutores)
- `models.Booking.topic` (String 200), `schemas.BookingCreate.topic` (sin HTML: reutilizar `_clean_name`), `services.book` lo guarda.
- Mostrarlo en `tutor.html` (agenda) con `el(...)` para escaparlo.

## Respuestas honestas si preguntan
- **¿Es seguro para producción?** No del todo: no se verifica que el correo sea de quien se registra (D-02), la clave de coordinación por defecto es solo de desarrollo (D-03) y el bloqueo protege un solo proceso (E-08).
- **¿Quién hizo QA?** Las pruebas automáticas y la prueba en navegador las ejecutó la IA a pedido de Diego; el QA independiente está pendiente (`docs/testing.md`).
- **¿Cuánto hizo la IA?** Todo lo significativo está en `docs/ai-log.md`, con errores detectados y cambios rechazados.
