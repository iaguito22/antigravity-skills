---
name: root-cause-analysis
description: >-
  Depuración metódica de fallos complejos. Activar cuando hay un error oscuro,
  el sistema crashea sin motivo claro, o cuando los intentos previos de arreglo
  han fallado. Prohíbe parchear a ciegas.
---

# Root Cause Analysis: Método Científico para Bugs

## 1. Prohibición de Arreglo Temprano
Está **ESTRICTAMENTE PROHIBIDO** intentar solucionar la lógica del código en tu primer turno, por muy obvio que te parezca el error.
Tu primer commit o modificación debe ser EXCLUSIVAMENTE para añadir instrumentación.

## 2. Instrumentación Obligatoria
1. Ejecuta el código para ver el error.
2. Añade `print()`, `console.log()` o trazas justo antes de la línea que crashea para exponer el estado de las variables.
3. Vuelve a ejecutar el código para capturar esa salida.

## 3. Intervención Mínima
Solo cuando tengas la salida de tus `prints` confirmando el error, estás autorizado a borrar los prints y proponer el código que soluciona el fallo.
