# Estrategia de pruebas

## Mínimo exigido y dónde se cubre
| Exigencia | Cobertura prevista | Archivo |
|---|---|---|
| Pruebas unitarias | Funciones puras de `rules.py` | `tests/test_rules.py` |
| Reglas críticas | RN-01 a RN-10 | `tests/test_business_rules.py` |
| **No doble reserva (obligatoria)** | CA-02, CA-03, CA-04 | `tests/test_double_booking.py` |
| Validaciones de usuario | CA-05, CA-06, CA-10 | `tests/test_validation.py` |
| Criterios de aceptación | CA-01 a CA-12 | `tests/test_acceptance.py` |

## Cómo correr
```bash
pytest -q
```

## Resultados
_Pegar aquí salidas reales de pytest y cobertura. No inventar._

## QA independiente
_Quién lo ejecutó, cómo, qué no se probó. Declarar si lo hizo una IA._
