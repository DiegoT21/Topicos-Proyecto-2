# Plan de implementación

> Estado: BORRADOR. Roles rotan por ciclo (Spec Lead / Dev Lead / QA-DevOps Lead). Cada tarea = un issue + una rama `feature/*` + un PR a `develop`.

| Ciclo | Objetivo | Tareas | Rol líder |
|---|---|---|---|
| 0 | Fundación | Repo, ramas, plantilla de PR, issues, specs aprobadas | Spec |
| 1 | Núcleo de reglas | `rules.py` (solapamiento, validaciones) + pruebas unitarias **antes** del resto | Dev |
| 2 | Reservar / cancelar | Modelos, servicios transaccionales, endpoints, prueba de **no doble reserva** | Dev |
| 3 | Disponibilidad y consulta | Bloques del tutor, listar tutores y espacios libres | Dev |
| 4 | Admin y frontend | Filtros, UI mínima, escape de HTML | QA |
| 5 | **Cambio de especificación** | Seguir el ciclo de `docs/decisions.md` | Todos |
| 6 | Cierre | Cobertura, QA independiente, evidencia, presentación, entrega | QA |

## Definición de hecho (por tarea)
Spec actualizada → criterio de aceptación con prueba → código → PR revisado por otra persona → QA → `ai-log.md` actualizado.
