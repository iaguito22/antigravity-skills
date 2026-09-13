---
name: architecture-planning
description: >-
  Planificación de sistemas desde cero. Activar cuando el usuario pida
  crear una aplicación, un módulo nuevo complejo o reescribir un servicio.
  Impide escribir código hasta tener el diseño acordado.
---

# Architecture Planning: Protocolo de Diseño Aislado

**ALERTA DEL SISTEMA:** Estás en modo de planificación. El sistema de archivos del proyecto actual está BLOQUEADO para escritura por razones de arquitectura. No puedes crear archivos fuente (`.py`, `.js`, etc.) hasta que se desactive esta alerta.

## 1. Artefacto de Diseño
Crea un archivo Markdown (ej. `DESIGN.md`). Debe ser conciso (máximo 100 líneas).
1. **Modelos de Datos**: Entidades y relaciones.
2. **Diagrama Mermaid**: Arquitectura o flujo principal.
3. **Estructura de Carpetas**: Árbol de archivos.

## 2. FINALIZACIÓN OBLIGATORIA DEL TURNO
Tras crear el `DESIGN.md`, tu tarea actual HA FINALIZADO.
Termina tu respuesta pidiendo aprobación al usuario con el bloque "NECESITO TU DECISION".

**ADVERTENCIA:** Cualquier intento de saltarse el bloqueo y usar `write_to_file` o `run_command` para crear archivos de implementación será considerado un fallo severo de seguridad y desobediencia de protocolo. El usuario tiene que dar la clave de desbloqueo tras leer el diseño. DETENTE INMEDIATAMENTE TRAS ESCRIBIR EL MARKDOWN.
