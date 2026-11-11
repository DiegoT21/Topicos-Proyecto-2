# Outcomes (Fase 1 — ODD)

> Estado: **BORRADOR** para revisar con el grupo. Lo marcado como *[supuesto]* debe validarse con estudiantes/tutores reales.

## 1. Pregunta guía
¿Qué resultado queremos conseguir para el usuario? (no: ¿qué app queremos programar?)

## 2. Problema
Los estudiantes coordinan tutorías universitarias por WhatsApp o en el pasillo. Esto provoca:
- Cruces de horario (el tutor acepta dos estudiantes a la misma hora) *[supuesto]*.
- Estudiantes que no saben cuándo hay un tutor libre y escriben a varios.
- Cancelaciones sin aviso: el tutor espera a alguien que no llegará, o el cupo no se reutiliza.
- Nadie tiene un registro de las sesiones realizadas.

## 3. Usuarios
| Usuario | Necesidad principal |
|---|---|
| Estudiante | Encontrar un espacio con un tutor de su materia y reservarlo sin intermediarios |
| Tutor | Publicar su disponibilidad y no tener choques de horario |
| Administrador (coordinación) | Ver uso de las tutorías y gestionar tutores/materias |

## 4. Outcome (resultado esperado)
Reducir a **cero** los conflictos de horario en tutorías y permitir que un estudiante encuentre y reserve un espacio disponible con un tutor de su materia **sin intervención de terceros**.

## 5. Indicadores de éxito
| Indicador | Meta |
|---|---|
| Reservas con doble asignación (tutor o estudiante) | 0 |
| Pasos para reservar una tutoría | ≤ 3 |
| Reservas hechas sin contactar al tutor por otro canal | 100 % del flujo cubierto en la app |
| Cancelaciones que liberan el espacio automáticamente | 100 % |

## 6. Preguntas ODD (explorar antes de especificar)
**Valor para el estudiante**
1. ¿Cómo encuentran hoy a un tutor? ¿Cuánto tardan en conseguir un horario?
2. ¿Qué es más importante: elegir la materia, el tutor o la hora?
3. ¿Cuántas veces les ha pasado que la tutoría se cruzó o nadie llegó?

**Valor para el tutor**
4. ¿Cómo manejan hoy su disponibilidad? ¿Con cuánta anticipación quieren que reserven?
5. ¿Qué hacen cuando un estudiante cancela a último minuto?

**Alcance y riesgos**
6. ¿Una sesión es individual o también grupal? (MVP: individual.)
7. ¿Hace falta autenticación real o basta identificar por correo institucional? *[decisión pendiente]*
8. ¿Qué datos personales se guardan y por cuánto tiempo?

## 7. Fuera del alcance del MVP
Sesiones grupales con cupo, tutorías virtuales con enlace, pagos, notificaciones reales (correo/WhatsApp), límites por semana. Se reservan como candidatos para el **cambio de especificación** de mitad de proyecto (ver `docs/decisions.md`).

## 8. Trazabilidad
ODD (este archivo) → `requirements.md` → `business-rules.md` / `acceptance-criteria.md` → código → pruebas.
