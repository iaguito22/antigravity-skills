---
name: unit-testing
description: >-
  Escribe tests unitarios que realmente detecten bugs. Activar cuando el usuario
  pida escribir tests, "añade tests", "cubre esto con tests", "quiero saber si
  funciona", o cuando acabe de escribir una función nueva y quiera verificarla.
  No es para tests de integración ni E2E: es para tests rápidos que fallen si
  el código está roto.
---

# Tests que cazan bugs

Un test que no puede fallar no es un test.

## Orden de valor (empieza por el más valioso)

1. **Error cases**: entrada inválida, nulo, vacío, negativo, tipo incorrecto → ¿qué lanza/devuelve?
2. **Límites**: mínimo, máximo, lista de un elemento, primera y última iteración.
3. **Happy path**: al final. Testear solo lo que funciona no aporta.

## Reglas

- Nombre = documentación: `test_remove_missing_raises_keyerror` > `test_remove`.
- Una aserción por test cuando sea posible.
- No mockees lo que testeas; solo dependencias externas (BD en `:memory:`, `unittest.mock` para red/tiempo).
- Fixture mínima: si necesitas BD, `sqlite3.connect(":memory:")`.

## Ejecuta una sola vez y reporta

```sh
python -m pytest test_archivo.py -v
```

Reporta exactamente:
```
Tests: N | Pasan: N | Fallan: N
· test_nombre — qué bug caza o qué caso verifica
```

Si algo falla inesperadamente: pega el error completo, no lo resumas.
