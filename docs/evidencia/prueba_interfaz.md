# Prueba de la interfaz web en navegador (2026-11-16)

**Quién la ejecutó:** Claude Code (agente de IA) por encargo de Diego, en el navegador integrado de la app de escritorio (Chromium), contra `python scripts/run_demo.py` con los datos ficticios de `python src/seed_demo.py --reset`.
**No es QA independiente**: la hizo la misma IA que escribió la interfaz. Falta que otra persona del grupo la repita (ver `docs/testing.md`).

| # | Pantalla | Paso | Resultado observado |
|---|---|---|---|
| 1 | Reservar | Entrar con `demo@gmail.com` | Mensaje: "Revisa el campo correo: Solo se aceptan correos @utp.ac.pa" (CA-16) |
| 2 | Reservar | Entrar con `demo@utp.ac.pa` | Aparecen búsqueda y "Mis reservas"; arriba "Estudiante Demo (demo@utp.ac.pa)" |
| 3 | Reservar | Cálculo I, martes 17 de noviembre | Riel de horas 08:00–18:00 con los tutores de la materia (Ana, Bruno, Darío), ordenados por hora (CA-17) |
| 4 | Reservar | Elegir "10:00 con Ana Pérez" → Reservar | "Reservado: 10:00 con Ana Pérez."; el botón de Ana a las 10:00 desaparece; la reserva sale en "Mis reservas" como `confirmada` (CA-01) |
| 5 | Reservar | Cancelar la reserva | "Reserva cancelada. El espacio quedó libre para otro estudiante."; estado `cancelada`; 10:00 con Ana vuelve al riel (CA-07) |
| 6 | Coordinación | Entrar con el token de desarrollo | Se ven las 4 materias y la tabla de reservas |
| 7 | Coordinación | Registrar tutor con nombre `Prueba <b>XSS</b>` | "Revisa el campo nombre: El nombre no puede contener HTML" (CA-10) |
| 8 | Soy tutor | Entrar con el código de Ana y publicar el viernes 20, 12:00–13:00 | "Bloque publicado: viernes, 20 de noviembre, de 12:00 a 13:00." |
| 9 | Soy tutor | Publicar el mismo bloque otra vez | "El bloque se solapa con otro ya publicado" (CA-14) |

## Errores encontrados y corregidos durante la prueba
- **Carrera al cambiar materia y día seguidos**: una respuesta vieja (vacía) se pintaba junto con la nueva y el riel mostraba "No hay espacios libres" encima de las horas. Se corrigió descartando respuestas que no son la última consulta (`slotsRequest` en `index.html`).
- **Orden de materias**: "Contabilidad" salía antes que "Cálculo I" (orden por bytes). Se corrigió ordenando sin tildes (`_sort_key` en `catalog.py`).
- **Mensajes de validación con nombres en inglés** ("campo email"): se tradujeron los nombres de campo en `app.js`.

## No probado
Otros navegadores, móvil real (solo ancho estrecho del panel), lector de pantalla, varias pestañas a la vez.
