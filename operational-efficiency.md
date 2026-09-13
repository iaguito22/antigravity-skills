---
name: operational-efficiency
description: >-
  Reduce tokens y tiempo en tareas operacionales: edición de archivos, búsqueda,
  ejecución de comandos, cualquier secuencia de pasos mecánicos. Activar en
  cualquier tarea de código (editar, refactorizar, buscar archivos) para
  minimizar lecturas innecesarias y maximizar el paralelismo de llamadas.
  No cubre el formato del output (esa es la skill output-quality) y NO actives para
  revisión de código o búsqueda de bugs: en esos casos, completitud importa
  más que velocidad.
---

# Eficiencia operacional: mínimo movimiento, máximo efecto

## Comandos de shell antes que tool calls individuales

Para cambios textuales en múltiples archivos, **un comando de shell es siempre mejor que N tool calls**:

```sh
# Renombrar función en todos los .py de un directorio:
sed -i 's/old_name/new_name/g' /ruta/*.py

# Verificar que quedó bien:
grep -rn "old_name" /ruta/  # debe devolver 0 resultados

# Añadir import en varios archivos:
sed -i '1s/^/import logging\n/' file1.py file2.py
```

Usa `run_command` con `sed`, `awk`, `grep`, `find -exec` para operaciones masivas.
Reserva `replace_file_content` solo cuando el cambio es específico y contextual (lógica, no texto plano).

## Grep antes que open

`grep -n "nombre"` → número de línea → `view_file` con `StartLine`/`EndLine`.
Nunca abras un archivo de 200 líneas para leer 10.

## Leer solo lo que vas a tocar

Si editas `parse_date`, busca la función con grep, lee esas líneas, edita, cierra.

## Paralelizar

Llamadas sin dependencia entre sí en el mismo bloque. Espera solo si B necesita el resultado de A.

## Calibrar antes de leer

`wc -l archivo` o `git diff --stat` antes de decidir cuánto leer.

## Nunca como atajo

Velocidad no justifica `except: pass`, retornos sin verificar `rowcount`, ni validaciones omitidas.
Si no sabes manejar el error, relánzalo.

## Cuándo NO activar

- Revisión de código / búsqueda de bugs: completitud > velocidad.
- Depurando algo desconocido: leer más contexto es correcto.
