---
name: code-review
description: >-
  Revisa código buscando bugs reales antes de darlo por bueno. Activar cuando el
  usuario pida revisar, mencione "mira si está bien", "antes de commitear",
  "/revisar", "code review", al terminar cualquier tanda de cambios de código, o cuando haya
  cambios sin commitear que revisar. No es un linter de estilo: busca fallos de
  corrección, errores silenciados, retornos mentirosos y residuos.
---

# Revisar cambios

Segunda pasada sobre tu propio trabajo. La primera la hiciste creyendo que funcionaba;
esta la haces asumiendo que algo está roto y que tienes que encontrarlo.

## 0a. Si el fallo lo ha reportado el usuario, REPRODÚCELO primero

El lo tiene delante y tú no. Su "no me deja scrollear" es un dato; tu "debería
funcionar" no lo es. Antes de tocar una línea:

1. **Reproduce su escenario exacto**, con su gesto y su tamaño de ventana.
2. **Mide el mecanismo, no el síntoma.** Un número cierra la discusión; una impresión la alarga.
3. **Si no consigues reproducirlo, dilo**: "no lo reproduzco; probé X e Y, vi Z, me falta W". Nunca "a mí me funciona".
4. Cuando lo arregles, vuelve a medir **lo mismo** y enseña los dos números.

Si dos arreglos seguidos no mueven la aguja: para. Instrumenta. Busca dónde muere el efecto.

## 0. Si se ejecuta, EJECÚTALO (antes de leer nada)

Leer código no es revisarlo.

- **HTML/juego**: `agy-ver abrir <fichero>` → `agy-ver logs` → interactúa → `agy-ver foto` → **abre el png**.
- **Script/CLI**: ejecútalo con entrada normal Y con entrada rara (vacía, enorme, inválida).
- **Servidor**: arráncalo y pídele algo real.
- **Librería**: llama a lo que cambiaste desde fuera.

Si no hay forma de ejecutarlo: "no verificado, solo revisión estática".

## 1. Consigue el diff

```sh
git status --short
git --no-pager diff
git --no-pager diff --staged
```

Si el diff pasa de ~400 líneas, trocéalo por archivo.

## 2. Lee el código NUEVO entero, no solo el diff

El diff miente por omisión. Abre la función completa donde cae cada hunk.
La mayoría de bugs viven en la interacción con el código que no cambiaste.

## 3. Busca esto, en este orden

1. **Corrección**: recorre a mano un caso concreto. "Con lista vacía pasa X."
2. **Casos límite**: vacío, nulo, cero, negativo, un elemento, unicode.
3. **Errores silenciados** (🔴 automático):
   - `except: pass` / `except Exception` que no relanza
   - `default=str` u otro fallback que convierte un error en dato silenciosamente
   - `catch {}` vacío
4. **Retornos mentirosos** (🔴 automático): función que retorna `True`/éxito sin comprobar `rowcount` ni verificar que la operación tuvo efecto.
5. **Rotura de contratos**: firmas cambiadas, campos renombrados. `grep -rn "nombre_funcion"`.
6. **Estado y concurrencia**: variables compartidas, orden de inicialización.
7. **Residuos** (🟡 automático sin excepción):
   - `# TODO`, `# BUG`, `# HACK`, `# FIXME`, `# DEBUG`
   - `print(` de depuración
   - Código comentado
   - Imports sin usar
   - Archivos compilados (`.pyc`, `.class`) versionados
8. **Simplificación**: solo si hay duplicación literal.

## 4. Verifica antes de reportar

- Escribe el caso de fallo concreto: "con entrada X, devuelve Y, debería ser Z".
- Si no puedes escribir esa frase, no es un hallazgo: bórralo.
- Comprueba que no está ya manejado arriba en el llamante.

Un hallazgo falso cuesta más que uno omitido.

## 5. Reporta con este formato exacto

Ordenados de más grave a menos.

```
### 🔴 ruta/archivo.py:42 — resumen en media línea
Con <entrada concreta>, <lo que pasa> en vez de <lo que debería>.
Arreglo: <una frase>.

### 🟡 ruta/archivo.py:10 — residuo / riesgo
<descripción en una frase>.

### 🔵 ruta/archivo.py:5 — simplificación posible
<descripción en una frase>.
```

- 🔴 fallos de corrección
- 🟡 riesgos, residuos, errores silenciados
- 🔵 simplificaciones

Si no hay nada: una línea y ya.

## Qué NO hacer

- No arregles nada durante la revisión salvo que el usuario lo pida.
- No comentes estilo, nombres ni formato.
- No digas "considera revisar si…". O es un fallo demostrable, o no se menciona.
