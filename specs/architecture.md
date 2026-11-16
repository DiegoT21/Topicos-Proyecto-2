# Arquitectura

> Estado: **APROBADO** (stack confirmado por Victor el 2026-11-13, `docs/decisions.md`). Actualizado el 2026-11-16 con la estructura real.

## Stack (libertad tecnológica, requisito 10 del enunciado)
| Capa | Tecnología | Motivo |
|---|---|---|
| Lenguaje | Python 3.12 | Conocido del Proyecto 1; en 3.13 fallan algunas dependencias |
| API | FastAPI | Valida con Pydantic (RNF-02) y genera documentación en `/docs` |
| Datos | SQLAlchemy 2 + SQLite | Sin servidor de BD; suficiente para un proceso; migrable a PostgreSQL |
| Validación | Pydantic 2 | Entradas declarativas: correo institucional, nombres sin HTML, cupo 1–6 |
| Interfaz | HTML, CSS y JavaScript sin framework, servidos por la misma API | Liviana; el foco está en las specs y las reglas |
| Pruebas | pytest + TestClient de FastAPI; pytest-cov para cobertura | Reglas puras, API y concurrencia con hilos |
| CI | GitHub Actions (`.github/workflows/tests.yml`) | Corre las pruebas en cada PR |
| Control de versiones | Git + GitHub (issues, ramas, PR) | Requisito del enunciado |

## Estructura
```
src/
  app/
    main.py          # FastAPI; monta la interfaz web en "/" después de /api
    config.py        # Zona America/Panama, duración de sesión, anticipación, dominio institucional, token admin
    database.py      # Motor y sesión de SQLAlchemy
    models.py        # Subject, Tutor, Student, Availability (con capacity), Booking
    schemas.py       # Entradas y salidas (Pydantic)
    rules.py         # Reglas PURAS, sin BD: overlaps, find_conflict, seats_left, alineación, ventana, espacios libres
    services.py      # Casos de uso: reservar (dentro de un lock) y cancelar
    routers/         # bookings (estudiante), catalog (público), tutor, admin
  frontend/          # index.html (estudiante), tutor.html, admin.html, app.js, styles.css
  seed_demo.py       # Datos ficticios de demostración
scripts/run_demo.py  # Arranca la app en http://localhost:8000
tests/               # pytest (conftest.py compartido)
```

## Flujo de una reserva
```
Navegador ──POST /api/bookings──▶ routers/bookings.py ──▶ services.book()
                                                            │  (lock de proceso)
                                                            ├─ tutor y materia existen; el tutor la ofrece (RN-06)
                                                            ├─ rules.validate_booking_window   (RN-03, RN-04)
                                                            ├─ rules.validate_slot_alignment   (RN-03 / E-02)
                                                            ├─ rules.seats_left sobre reservas del tutor (RN-01, RN-13)
                                                            ├─ rules.find_conflict sobre reservas del estudiante (RN-02)
                                                            └─ INSERT + commit
```

## Decisiones de diseño
- **Reglas como funciones puras** en `rules.py`: se prueban sin BD y el cambio de especificación (sesiones grupales) se resolvió agregando `seats_left` sin reescribir el resto.
- **Verificar e insertar dentro de un lock de proceso**, para evitar la carrera del Proyecto 1. Limitación: un solo proceso (E-08).
- **Fechas naive en hora de Panamá** en la BD y en la API; la interfaz las lee como texto para no desplazarlas con la zona del navegador.
- **Interfaz sin `innerHTML` con datos**: todo texto de usuario se inserta con `textContent` (RNF-02); una prueba lo verifica.
- **Identificación por tokens** (estudiante, tutor, admin) en headers; sin contraseñas (RNF-04, decisiones D-01 a D-04).

## Riesgos conocidos
Autenticación sin verificar el correo (D-02), lock de un solo proceso, sin migraciones (recrear la BD local al cambiar el modelo), sin notificaciones.
