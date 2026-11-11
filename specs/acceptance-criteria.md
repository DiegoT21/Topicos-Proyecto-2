# Criterios de aceptación

> Estado: BORRADOR. Formato Dado/Cuando/Entonces. Cada criterio tendrá una prueba en `tests/` (columna Prueba, a completar).

| ID | Req / Regla | Criterio | Prueba |
|---|---|---|---|
| CA-01 | RF-06 | **Dado** un espacio libre de un tutor, **cuando** un estudiante lo reserva, **entonces** la reserva queda `confirmada` y el espacio deja de aparecer libre | _pendiente_ |
| CA-02 | RF-07 / RN-01 | **Dado** una reserva confirmada del tutor T a las 10:00, **cuando** otro estudiante reserva a T a las 10:00 (o 10:30 con sesión de 60 min), **entonces** el sistema responde 409 y no crea la reserva | _pendiente_ (**obligatoria**: no doble reserva) |
| CA-03 | RN-01 | **Dado** una sesión 10:00–11:00, **cuando** se reserva 11:00–12:00 con el mismo tutor, **entonces** se permite (intervalo semiabierto) | _pendiente_ |
| CA-04 | RN-02 | **Dado** un estudiante con sesión a las 10:00 con el tutor A, **cuando** intenta reservar a las 10:00 con el tutor B, **entonces** se rechaza con 409 | _pendiente_ |
| CA-05 | RN-03 | **Cuando** se reserva fuera de los bloques publicados por el tutor, **entonces** 422 | _pendiente_ |
| CA-06 | RN-04 | **Cuando** se reserva una hora pasada o sin la anticipación mínima, **entonces** 422 | _pendiente_ |
| CA-07 | RF-08 / RN-07 | **Dado** una reserva confirmada, **cuando** el estudiante la cancela, **entonces** pasa a `cancelada` y el espacio vuelve a estar libre | _pendiente_ |
| CA-08 | RN-08 | **Cuando** otro estudiante intenta cancelar una reserva ajena, **entonces** 403 | _pendiente_ |
| CA-09 | RN-10 | **Dado** una reserva cancelada cuyo espacio fue tomado por otro, **cuando** se intenta reactivar, **entonces** se rechaza con 409 | _pendiente_ |
| CA-10 | RN-11 / RNF-02 | **Cuando** el nombre contiene HTML (`<img onerror=...>`), **entonces** se rechaza o se almacena escapado y nunca se ejecuta en pantalla | _pendiente_ |
| CA-11 | RF-04 | **Cuando** se lista tutores por materia, **entonces** solo aparecen los tutores asignados a esa materia | _pendiente_ |
| CA-12 | RF-10 | **Cuando** el admin filtra por tutor, materia, fecha o estado, **entonces** solo recibe las reservas que cumplen | _pendiente_ |
