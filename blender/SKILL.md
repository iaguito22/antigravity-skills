---
name: blender
description: >-
  Blender through its MCP: scenes, models, materials, Poly Haven/Sketchfab, renders with
  Cycles or EEVEE. The traps on a low-VRAM laptop that crash the session.
---

# Blender on a low-VRAM laptop

## Start
- `run_command` with `blender` as is, no `&` or `setsid` (agy backgrounds it and it stays
  alive; with `setsid … &` it closed). With the UI: with `blender -b` the MCP addon doesn't
  listen. Ready when `get_addon_status` says `up_to_date: true`.
- Poly Haven, Sketchfab and Poly Pizza are off per scene and answer
  `Unknown command type`. First:
  `bpy.context.scene.blendermcp_use_polyhaven = True` (and `_use_polypizza`, `_use_sketchfab`).

## Assets
- Poly Haven always at `resolution: "1k"`: 2k and 4k exceed the MCP's 3-minute timeout.
- Tested: trees `fir_sapling`, `tree_small_02`; rock `boulder_01`; ground
  `forest_ground_04`; HDRI `alps_field`.
- Many copies = linked duplicates (`o = template.copy(); o.data = template.data`),
  30-60 at most.

## A render that doesn't crash
- Hybrid GPU with little VRAM: Cycles OptiX gives `out of GPU memory` and EEVEE Next with
  dense meshes takes down the iGPU (`amdgpu: context is lost`). The stable option: Cycles
  on CPU, 32 samples and the denoiser.
- Color: `view_transform = 'AgX'`, `look = 'AgX - Base Contrast'`; HDRI at strength ~2 plus
  a warm sun (~16) so nothing comes out as a silhouette.
- Aim the camera at a point: `cam.rotation_euler = (target - cam.location).to_track_quat('-Z', 'Y').to_euler()`,
  and nothing closer than 3 m to the lens.

## Check (done = render looked at)
Render to a png, open it with `view_file` and look at it like the user would: framing,
black silhouettes, object scale, floating objects. To show it: `setsid xdg-open render.png &`.
