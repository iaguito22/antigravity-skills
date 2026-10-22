---
name: 3d
description: >-
  Árboles, arbustos, hojas y nubes en escenas three.js / WebGL: usa el módulo probado en
  vez de esferas o icosaedros. Úsala en cuanto una escena 3D lleve vegetación o cielo.
---

# Vegetación y nubes que no parezcan globos

Tu costumbre es hacer la copa con esferas o icosaedros con `flatShading` y la nube con
esferas pegadas: queda de juguete, como globos. Y las rocas, deformando vértices con
`Math.random()`, salen agrietadas (las caras no comparten vértices). El aspecto realista sale de muchas
**tarjetas** pequeñas con textura y alpha: tarjetas de hojas con la normal del volumen de
la copa, y sprites de vapor para las nubes. Eso ya está hecho y probado en `vegetacion.js`.

## Usarlo (el módulo se copia, no se lee ni se reescribe)
`cp ~/.gemini/config/skills/3d/vegetacion.js .` junto al `index.html`, y en un
`<script type="module">` con el importmap de `three`:
```js
import { arbol, nube, roca, mecer } from './vegetacion.js';
const a = arbol({ tipo: 'roble', altura: 6 });   // 'roble' | 'abedul' | 'pino', altura 4-9
a.position.set(x, 0, z); scene.add(a);
const n = nube({ ancho: 40, sol: sol.position }); n.position.set(x, 40, -90); scene.add(n);
// nubes altas y lejos; `sol` = la DirectionalLight, para que su lado iluminado cuadre
const r = roca({ tam: 0.8 }); r.position.set(x, sueloY, z); scene.add(r);
// en el bucle: mecer(scene, reloj.getElapsedTime());
```
- Cada árbol es aleatorio: crea uno por posición, no clones uno solo.
- 10-25 árboles y 3-6 nubes van fluidos. Arbustos = `arbol` con `altura` 1-1,5
  hundido medio metro en el suelo.
- Al acabar, `python3 ~/.gemini/config/skills/3d/incrusta.py index.html`: mete el módulo
  dentro de la página para que abra con doble clic (file:// no carga módulos de otro
  fichero) y borra la copia `vegetacion.js` de la carpeta.

## El resto de la escena sigue siendo tuyo
El módulo solo pone árboles, nubes y rocas. Hierba, flores, agua, caminos, el cielo y la
luz cálida van con el mismo mimo que pondrías sin él: con la skill la escena no puede salir
más pobre que sin ella.

## Luz que lo hace funcionar
`HemisphereLight` (cielo azulado, suelo verde oscuro) + `DirectionalLight` cálido con
`castShadow` y `shadow.mapSize` 2048, `renderer.toneMapping = ACESFilmicToneMapping`,
`Fog` del color del horizonte. Las nubes ignoran el tone mapping para seguir blancas.

## Comprobar (hecho = foto de lejos y de cerca mirada)
`agy-ver abrir` + `agy-ver foto`, y otra con la cámara a 3-4 m de una copa. Lejos:
siluetas irregulares con huecos de cielo, nada de bolas lisas ni facetas. Cerca: hojas
sueltas, sin media copa negra. Nubes: macizas, bordes de vapor, base gris y cima blanca, sin agujeros. Rocas: sin grietas.
