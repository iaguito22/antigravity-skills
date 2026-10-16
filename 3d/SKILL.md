---
name: 3d
description: >-
  Trees, bushes, leaves, clouds and rocks in three.js / WebGL scenes: use the tested module
  instead of spheres or icosahedra. Use it as soon as a 3D scene has vegetation, sky or rocks.
---

# Vegetation and clouds that don't look like balloons

The default habit is a crown made of spheres or flat-shaded icosahedra and a cloud made of
stuck-together spheres: it looks like a toy, like balloons. And rocks, displacing vertices
with `Math.random()`, come out cracked (faces don't share vertices). The realistic look
comes from many small textured **cards** with alpha: leaf cards carrying the crown's volume
normal, and vapor sprites for clouds. That is already built and tested in `vegetation.js`.

## Use it (the module is copied, not read or rewritten)
`cp ~/.gemini/config/skills/3d/vegetation.js .` next to `index.html`, and in a
`<script type="module">` with the `three` importmap:
```js
import { tree, cloud, rock, sway } from './vegetation.js';
const t = tree({ kind: 'oak', height: 6 });   // 'oak' | 'birch' | 'pine', height 4-9
t.position.set(x, 0, z); scene.add(t);
const c = cloud({ width: 40, sun: sunLight.position }); c.position.set(x, 40, -90); scene.add(c);
// clouds high and far; `sun` = the DirectionalLight, so their lit side matches
const r = rock({ size: 0.8 }); r.position.set(x, groundY, z); scene.add(r);
// in the loop: sway(scene, clock.getElapsedTime());
```
- Every tree is random: create one per position, don't clone a single one.
- 10-25 trees and 3-6 clouds run smoothly. Bushes = `tree` with `height` 1-1.5 sunk half a
  metre into the ground.
- When done, `python3 ~/.gemini/config/skills/3d/inline.py index.html`: it puts the module
  inside the page so it opens on double click (file:// doesn't load modules from another
  file); then delete the `vegetation.js` copy from the folder.

## The rest of the scene is still yours
The module only provides trees, clouds and rocks. Grass, flowers, water, paths, the sky and
warm light get the same care you would give them without it: with the skill the scene must
not come out poorer than without it.

## Light that makes it work
`HemisphereLight` (bluish sky, dark green ground) + a warm `DirectionalLight` with
`castShadow` and `shadow.mapSize` 2048, `renderer.toneMapping = ACESFilmicToneMapping`,
`Fog` in the horizon color. Clouds ignore tone mapping so they stay white.

## Check (done = far and close screenshots looked at)
`agy-ver abrir` + `agy-ver foto`, and another with the camera 3-4 m from a crown. Far:
irregular silhouettes with gaps of sky, no smooth balls or facets. Close: separate leaves,
no half-black crown. Clouds: solid, vapor edges, grey base and white top, no holes. Rocks:
no cracks.
