# Arquitectura

> Estado: BORRADOR. El enunciado exige que el stack tecnológico esté mencionado aquí.

## Stack propuesto (pendiente de confirmar en el grupo)
| Capa | Tecnología | Motivo |
|---|---|---|
| Backend | Python 3.12 + FastAPI | Ya conocido del Proyecto 1; Swagger automático |
| Datos | SQLAlchemy 2 + SQLite (local) | Sin infraestructura extra; migrable a PostgreSQL |
| Validación | Pydantic | Validación de entrada declarativa |
| Pruebas | pytest + httpx/TestClient | Pruebas de API y de reglas |
| Frontend | HTML/CSS/JS sin framework | Liviano; foco en las specs, no en la UI |
| Control de versiones | Git + GitHub (issues, PR) | Requisito del enunciado |

> Python 3.12: en 3.13 falló `psycopg2-binary` en el Proyecto 1; aquí se evita esa dependencia (SQLite).

## Estructura de código prevista
```
src/
  app/
    main.py          # FastAPI
    config.py        # Zona horaria, duración de sesión, anticipación mínima
    database.py
    models.py        # Subject, Tutor, Student, Availability, Booking
    schemas.py
    rules.py         # Reglas puras: solapamiento, validaciones (testeables sin BD)
    services.py      # Casos de uso: reservar, cancelar (transacción)
    routers/         # public / tutor / admin
  frontend/
tests/
```

## Decisiones de diseño
- **Reglas en `rules.py` como funciones puras**: se prueban unitariamente y facilitan el cambio de especificación en vivo.
- **Reservar es una sola transacción** (verificar solapamiento + insertar) para evitar la carrera del Proyecto 1.
- **Fechas en `America/Panama`**, almacenadas de forma consistente (un solo criterio).

## Riesgos conocidos
Autenticación mínima (no apta para producción), SQLite con concurrencia limitada, sin notificaciones reales.
