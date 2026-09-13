---
name: web-3d
description: >-
  3D scenes in the browser (Three.js, WebGL, React Three Fiber) that look
  realistic and not like plastic. Use when dealing with 3D, models, cameras,
  materials, lights, shaders.
---

# 3D that doesn't look like plastic

90% of bad scenes fail because of the same thing: render configuration, flat lighting, and invented scale.

## 1. Vanilla Three.js: The 4 sacred settings
Without this, any scene looks matte and washed out. ALWAYS include in Vanilla JS:

```js
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
```

## 2. React Three Fiber (R3F)
In R3F **DO NOT modify the renderer imperatively**.
The `<Canvas>` already applies SRGB and ACESFilmic by default.
Just explicitly enable shadows: `<Canvas shadows dpr={[1, 2]}>`

## 3. The Shadow Trap
Enabling `shadowMap` is NOT enough. The AI always forgets the rest.
For shadows to exist, you MUST add:
1. A light that casts: `light.castShadow = true`
2. Objects that cast: `mesh.castShadow = true`
3. Objects that receive: `mesh.receiveShadow = true`
