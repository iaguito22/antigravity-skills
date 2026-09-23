---
name: web-3d
description: >-
  Use for any 3D in the browser: 3D scene, three.js, WebGL, React Three Fiber, model,
  camera, lights, shadows, materials, shaders (also "escena 3D"). Makes scenes look
  right, not like plastic.
---

# 3D that doesn't look like plastic

## 1. Renderer (vanilla three.js)
```js
renderer.toneMapping = THREE.ACESFilmicToneMapping;   // not on by default
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.setPixelRatio(Math.min(devicePixelRatio, 2)); // never bare devicePixelRatio
```
Color textures: `tex.colorSpace = THREE.SRGBColorSpace` (normal/roughness maps: no).
Resize: update `camera.aspect`, `updateProjectionMatrix()` and `renderer.setSize`.

## 2. React Three Fiber
Don't touch the renderer by hand: `<Canvas shadows dpr={[1, 2]}>` already applies sRGB and ACES.

## 3. Shadows: the four pieces
1. `light.castShadow = true` 2. `mesh.castShadow = true` 3. `floor.receiveShadow = true`
4. Shadow camera framing: by default it covers ±5 units. Fit
   `light.shadow.camera.left/right/top/bottom` to the floor and `light.shadow.mapSize.set(2048, 2048)`,
   or the shadow comes out clipped or pixelated.

## 4. Light
Never just `AmbientLight`: a main directional light + a soft `HemisphereLight` fill.

## 5. Check
`agy-ver abrir` → `foto` (is the shadow on the floor?) → `mide 3` (FPS) → `logs` → `cerrar`.
