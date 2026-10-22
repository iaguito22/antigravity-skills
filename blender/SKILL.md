---
name: blender
description: >-
  Blender por su MCP: escenas, modelos, materiales, Poly Haven/Sketchfab, renders con
  Cycles o EEVEE. Las trampas de este portátil que tumban la sesión.
---

# Blender en este portátil

## Arrancar
- `run_command` con `~/.local/bin/blender` tal cual, sin `&` ni `setsid` (agy lo pasa a
  segundo plano y sigue vivo; con `setsid … &` se cerraba). Con interfaz: con `blender -b`
  el addon del MCP no escucha. Listo cuando `get_addon_status` dice `up_to_date: true`.
- Poly Haven, Sketchfab y Poly Pizza vienen apagados por escena y devuelven
  `Unknown command type`. Primero:
  `bpy.context.scene.blendermcp_use_polyhaven = True` (y `_use_polypizza`, `_use_sketchfab`).

## Assets
- Poly Haven siempre a `resolution: "1k"`: 2k y 4k pasan el timeout de 3 min del MCP.
- Probados: árboles `fir_sapling`, `tree_small_02`; roca `boulder_01`; suelo
  `forest_ground_04`; HDRI `alps_field`.
- Muchas copias = duplicados enlazados (`o = plantilla.copy(); o.data = plantilla.data`),
  30-60 como mucho.

## Render que no se cae
- GPU híbrida con poca VRAM: Cycles OptiX da `out of GPU memory` y EEVEE Next con mallas
  densas tumba la iGPU (`amdgpu: context is lost`). Lo estable: Cycles en CPU, 32 muestras
  y denoiser.
- Color: `view_transform = 'AgX'`, `look = 'AgX - Base Contrast'`; HDRI a fuerza ~2 más un
  sol cálido (~16) para que no salgan siluetas.
- Cámara a un punto: `cam.rotation_euler = (objetivo - cam.location).to_track_quat('-Z', 'Y').to_euler()`,
  y nada a menos de 3 m de la lente.

## Comprobar (hecho = render mirado)
Renderiza a un png, ábrelo con `view_file` y míralo como él: encuadre, siluetas negras,
escala de los objetos, flotantes. Para enseñárselo: `setsid xdg-open render.png &`.
