# Reglas de negocio

> Estado: BORRADOR. Cada regla debe tener al menos una prueba automatizada (ver `acceptance-criteria.md`).

| ID | Regla | Criticidad |
|---|---|---|
| RN-01 | **Un tutor no puede tener dos sesiones activas que se solapen** (intervalo `[inicio, fin)`) | Crítica |
| RN-02 | **Un estudiante no puede tener dos sesiones activas que se solapen**, aunque sean con tutores distintos | Crítica |
| RN-03 | Solo se reserva dentro de un bloque de disponibilidad publicado por el tutor | Alta |
| RN-04 | Solo se reservan horas futuras (con anticipación mínima configurable, por defecto 1 h) | Alta |
| RN-05 | Duración fija de sesión (por defecto 60 min), configurable | Media |
| RN-06 | El tutor solo ofrece materias que tiene asignadas | Media |
| RN-07 | Una reserva cancelada **no bloquea** el espacio; queda en el historial | Alta |
| RN-08 | Solo el estudiante dueño (o el admin) puede cancelar una reserva | Alta |
| RN-09 | Estados válidos: `confirmada`, `cancelada`, `realizada`. Transiciones: confirmada → cancelada / realizada | Media |
| RN-10 | Reactivar o reprogramar una reserva debe volver a validar RN-01 y RN-02 excluyendo la propia reserva (lección del hallazgo 1 del Proyecto 1) | Alta |
| RN-11 | Teléfono/correo con formato válido; nombre sin HTML | Media |

## Notas
- La detección de solapamiento es **semiabierta**: una sesión 10:00–11:00 y otra 11:00–12:00 **no** chocan.
- La verificación y la inserción deben ocurrir en una misma transacción para evitar la carrera detectada en el Proyecto 1 (hallazgo 9).
