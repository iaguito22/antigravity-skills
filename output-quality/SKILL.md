---
name: output-quality
description: >-
  Controla el formato y la densidad de cualquier respuesta entregada al usuario.
  Activar siempre que el agente vaya a escribir una respuesta: elimina relleno,
  estructura el informe final y define qué reportar y qué omitir. Complementa
  a operational-efficiency (proceso) y a code-review (qué buscar). Cuando code-review está activa,
  no impone su propio formato: deja que code-review use 🔴🟡🔵.
---

# Calidad: menos output, más señal

**Meta:** si con esta skill produces MÁS texto que sin ella, fallaste — añadiste estructura sin quitar relleno.

## Cortar sin piedad

No escribas: confirmaciones de lectura · resúmenes de lo que el usuario ya ve · elogios · planes en prosa · disculpas largas · "¿Quieres que también...?"

## Respuesta simple → texto plano

Pregunta corta o confirmación: una o dos frases, sin títulos ni viñetas.

## Informe de trabajo (cuando code-review no está activa)

```
**Veredicto 2-5 palabras.** Contexto solo si aporta.

· ruta:linea — qué pasaba

Comprobado: qué ejecutaste y qué viste.
```

- Usa las viñetas que necesites, máximo 6. Si caben 2, usa 2.
- `Comprobado:` obligatorio si tocaste código.
- Después: nada.

## Cuando code-review está activa

Deja el formato 🔴🟡🔵 intacto. No sustituyas por viñetas.

## Pensamiento visible

Una línea suelta solo si hay hipótesis, sorpresa o cambio de rumbo. Nunca antes de un paso obvio.
