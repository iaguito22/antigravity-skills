// vegetacion.js — árboles con hojas de verdad y nubes blandas para three.js (>= 0.150).
// Copas = cientos de tarjetas de hojas con alphaTest y normales de volumen (no esferas);
// nubes = sprites de vapor con ruido, blancos arriba y grises abajo (no bolas).
// rocas = icosaedro deformado en función de la posición (sin grietas entre caras).
//   import { arbol, nube, roca, mecer } from './vegetacion.js';
//   scene.add(arbol({ tipo: 'roble', altura: 6 }));   // 'roble' | 'abedul' | 'pino'
//   scene.add(nube({ ancho: 40 }));                    // ponla lejos y alta: y 25-60
//   scene.add(roca({ tam: 1 }));                       // apóyala: position.y = suelo
//   en el bucle: mecer(scene, reloj.getElapsedTime());
import * as THREE from 'three';

const azar = (a, b) => a + Math.random() * (b - a);

// ---------- texturas (canvas, sin ficheros) ----------
const cache = {};

function texturaHojas(tipo) {
  if (cache[tipo]) return cache[tipo];
  const c = document.createElement('canvas');
  c.width = c.height = 256;
  const g = c.getContext('2d');
  const pino = tipo === 'pino';
  const n = pino ? 60 : 55;
  for (let i = 0; i < n; i++) {
    const x = azar(30, 226), y = azar(30, 226);
    const l = pino ? azar(50, 80) : azar(40, 62);
    const a = pino ? azar(0.14, 0.2) * l : azar(0.3, 0.42) * l;
    const tono = pino ? azar(105, 135) : tipo === 'abedul' ? azar(70, 95) : azar(85, 112);
    const luz = pino ? azar(20, 34) : azar(28, 50);
    g.save();
    g.translate(x, y);
    g.rotate(azar(0, Math.PI * 2));
    g.beginPath();
    g.moveTo(-l / 2, 0);
    g.quadraticCurveTo(0, -a, l / 2, 0);
    g.quadraticCurveTo(0, a, -l / 2, 0);
    g.fillStyle = `hsl(${tono} ${azar(35, 55)}% ${luz}%)`;
    g.fill();
    if (!pino) {
      g.strokeStyle = `hsl(${tono} 40% ${luz - 8}%)`;
      g.lineWidth = 1.2;
      g.beginPath(); g.moveTo(-l / 2, 0); g.lineTo(l / 2, 0); g.stroke();
    }
    g.restore();
  }
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 4;
  return (cache[tipo] = t);
}

function texturaVapor() {
  if (cache.vapor) return cache.vapor;
  const s = 128, c = document.createElement('canvas');
  c.width = c.height = s;
  const g = c.getContext('2d');
  const img = g.createImageData(s, s);
  // caída gaussiana lisa y macizo en el centro: el relieve lo dan los puffs solapados,
  // no manchas dentro del sprite (eso se veía como agujeros)
  for (let y = 0; y < s; y++) for (let x = 0; x < s; x++) {
    const dx = x / s - 0.5, dy = y / s - 0.5;
    const r2 = (dx * dx + dy * dy) * 4;
    const v = r2 >= 1 ? 0 : Math.min(1, 1.6 * Math.exp(-r2 * 3.2)) * (1 - r2);
    const i = (y * s + x) * 4;
    // cada puff sombreado como una bola de vapor con luz de arriba: claro arriba, gris abajo
    const luz = 255 * (1 - 0.18 * Math.max(0, Math.min(1, y / s * 1.15 - 0.1)));
    img.data[i] = img.data[i + 1] = img.data[i + 2] = luz;
    img.data[i + 3] = v * 255;
  }
  g.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return (cache.vapor = t);
}

// ---------- copa: tarjetas de hojas fundidas en una sola malla ----------
// Cada tarjeta lleva la normal del volumen de la copa (de su centro hacia fuera): la copa
// se ilumina como un volumen suave y no como cartón. Color por vértice = oclusión dentro.
function copa({ tipo, centros, radio, tarjetas }) {
  const pos = [], nor = [], uv = [], col = [], idx = [];
  const lado = radio * (tipo === 'pino' ? 0.55 : 0.5);
  const q = new THREE.Quaternion(), e = new THREE.Euler();
  const v = new THREE.Vector3(), centro = new THREE.Vector3(), dir = new THREE.Vector3();
  const esquinas = [[-1, -1], [1, -1], [1, 1], [-1, 1]];
  for (let k = 0; k < tarjetas; k++) {
    const [cx, cy, cz, r] = centros[k % centros.length];
    centro.set(cx, cy, cz);
    dir.set(azar(-1, 1), azar(-1, 1), azar(-1, 1)).normalize();
    const d = r * Math.pow(Math.random(), 0.35);           // más hojas cerca de la piel
    const p = centro.clone().addScaledVector(dir, d);
    e.set(azar(0, Math.PI), azar(0, Math.PI), azar(0, Math.PI));
    q.setFromEuler(e);
    const fuera = p.clone().sub(centro).normalize();
    const oclusion = 0.55 + 0.45 * (d / r);
    const arriba = 0.85 + 0.15 * fuera.y;
    const base = pos.length / 3;
    const tam = lado * azar(0.75, 1.2);
    for (const [sx, sy] of esquinas) {
      v.set(sx * tam / 2, sy * tam / 2, 0).applyQuaternion(q).add(p);
      pos.push(v.x, v.y, v.z);
      nor.push(fuera.x, fuera.y, fuera.z);
      uv.push((sx + 1) / 2, (sy + 1) / 2);
      const c = oclusion * arriba;
      col.push(c, c, c);
    }
    idx.push(base, base + 1, base + 2, base, base + 2, base + 3);
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  geo.setAttribute('normal', new THREE.Float32BufferAttribute(nor, 3));
  geo.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
  geo.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
  geo.setIndex(idx);
  const mat = new THREE.MeshStandardMaterial({
    map: texturaHojas(tipo), alphaTest: 0.35, side: THREE.DoubleSide,
    vertexColors: true, roughness: 0.85,
  });
  mat.onBeforeCompile = (sh) => {
    sh.fragmentShader = sh.fragmentShader.replace('normal *= faceDirection;', '');
  };
  const m = new THREE.Mesh(geo, mat);
  m.castShadow = m.receiveShadow = true;
  m.userData.mecer = azar(0, 6.28);
  const relleno = new THREE.MeshStandardMaterial({
    color: tipo === 'pino' ? 0x1a3520 : 0x27441b, roughness: 1,
  });
  for (const [cx, cy, cz, r] of centros) {
    const b = new THREE.Mesh(new THREE.IcosahedronGeometry(r * 0.5, 2), relleno);
    b.position.set(cx, cy, cz);
    b.receiveShadow = true;
    m.add(b);
  }
  return m;
}

// ---------- árbol ----------
const CORTEZA = { roble: 0x4a3626, abedul: 0xd9d4c7, pino: 0x3b2a1e };

function rama(desde, hasta, r0, r1, mat) {
  const largo = desde.distanceTo(hasta);
  const g = new THREE.CylinderGeometry(r1, r0, largo, 7, 1);
  g.translate(0, largo / 2, 0);
  const m = new THREE.Mesh(g, mat);
  m.position.copy(desde);
  m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), hasta.clone().sub(desde).normalize());
  m.castShadow = true;
  return m;
}

export function arbol({ tipo = 'roble', altura = 6 } = {}) {
  const g = new THREE.Group();
  const corteza = new THREE.MeshStandardMaterial({ color: CORTEZA[tipo], roughness: 0.95 });
  const h = altura;
  if (tipo === 'pino') {
    g.add(rama(new THREE.Vector3(), new THREE.Vector3(0, h, 0), h * 0.035, h * 0.008, corteza));
    const centros = [];
    for (let i = 0; i < 7; i++) {                     // pisos que se estrechan hacia arriba
      const t = i / 6, r = h * 0.3 * (1 - t * 0.85);   // cono: ancho abajo, punta arriba
      centros.push([0, h * (0.22 + t * 0.72), 0, r]);
    }
    g.add(copa({ tipo, centros, radio: h * 0.16, tarjetas: Math.round(h * 200) }));
    return g;
  }
  const tronco = h * (tipo === 'abedul' ? 0.45 : 0.35);
  const arriba = new THREE.Vector3(azar(-0.2, 0.2), tronco, azar(-0.2, 0.2));
  g.add(rama(new THREE.Vector3(), arriba, h * 0.05, h * 0.03, corteza));
  // 3-5 ramas que acaban en racimos: la silueta queda irregular, con huecos de cielo
  const centros = [[arriba.x, arriba.y + h * 0.22, arriba.z, h * 0.26]];
  const nRamas = Math.floor(azar(3, 6));
  for (let i = 0; i < nRamas; i++) {
    const ang = (i / nRamas) * Math.PI * 2 + azar(-0.4, 0.4);
    const lejos = h * azar(0.2, 0.32);
    const fin = arriba.clone().add(new THREE.Vector3(Math.cos(ang) * lejos, h * azar(0.08, 0.35), Math.sin(ang) * lejos));
    g.add(rama(arriba, fin, h * 0.022, h * 0.01, corteza));
    centros.push([fin.x, fin.y + h * 0.04, fin.z, h * azar(0.17, 0.23)]);
  }
  g.add(copa({ tipo, centros, radio: h * 0.2, tarjetas: Math.round(h * (tipo === 'abedul' ? 160 : 220)) }));
  return g;
}

// ---------- nube ----------
// sol = dirección hacia el sol (la misma que la DirectionalLight): ese lado sale más claro.
export function nube({ ancho = 40, alto = ancho * 0.3, puffs = 70, sol = new THREE.Vector3(0.4, 1, 0.3) } = {}) {
  const haciaSol = sol.clone().normalize();
  const medio = new THREE.Vector3(0, alto * 0.35, 0), d = new THREE.Vector3();
  const g = new THREE.Group();
  const tex = texturaVapor();
  for (let i = 0; i < puffs; i++) {
    const x = (Math.random() + Math.random() - 1) * 0.5 * ancho;   // más denso en el centro
    const borde = 1 - Math.abs(x) / (ancho / 2);          // más alta en el centro
    const y = Math.pow(Math.random(), 1.6) * alto * (0.35 + 0.65 * borde);
    const z = azar(-0.25, 0.25) * ancho * 0.5;
    // base gris azulada y cima casi blanca; el lado del sol más claro, el contrario en sombra
    const t = Math.min(1, y / alto);
    const lado = d.set(x, y, z).sub(medio).normalize().dot(haciaSol);
    const l = Math.min(1, 0.74 + 0.22 * t + 0.1 * lado);
    const c = new THREE.Color().setRGB(l * 0.95, l * 0.97, Math.min(1, l * 1.02));
    const mat = new THREE.SpriteMaterial({
      map: tex, color: c, transparent: true, depthWrite: false,
      opacity: azar(0.7, 0.95), fog: false, toneMapped: false,
    });
    const s = new THREE.Sprite(mat);
    const tam = ancho * azar(0.22, 0.38) * (0.6 + 0.4 * borde);
    s.scale.set(tam, tam * azar(0.75, 1), 1);
    s.position.set(x, y, z);
    g.add(s);
  }
  g.userData.nube = azar(0.3, 0.8);
  return g;
}

// ---------- roca ----------
// El fallo típico: desplazar cada vértice con Math.random(). Las geometrías de three no
// comparten vértices entre caras, así que cada cara se mueve por su lado y se abren grietas.
// Aquí el desplazamiento depende solo de la posición: vértices iguales, mismo sitio.
export function roca({ tam = 1, color = 0x7a7d74 } = {}) {
  const geo = new THREE.IcosahedronGeometry(1, 4);
  const p = geo.attributes.position, v = new THREE.Vector3();
  const dirAzar = () => new THREE.Vector3(azar(-1, 1), azar(-1, 1), azar(-1, 1)).normalize();
  const ondas = Array.from({ length: 9 }, (_, k) => [dirAzar(), azar(2, 4) * (1 + k * 0.6), azar(0, 6.28), 0.1 / (1 + k * 0.7)]);
  // cortes planos: caras de fractura con aristas, lo que la separa de un canto rodado liso
  const cortes = Array.from({ length: Math.floor(azar(4, 8)) }, () => [dirAzar(), azar(0.62, 0.85)]);
  const col = [];
  for (let i = 0; i < p.count; i++) {
    v.fromBufferAttribute(p, i).normalize();
    let r = 1;
    for (const [d, f, fase, a] of ondas) r += Math.sin(v.dot(d) * f + fase) * a;
    for (const [d, dist] of cortes) { const c = v.dot(d); if (c > 0.05) r = Math.min(r, dist / c); }
    const tono = 0.8 + 0.2 * Math.sin(v.x * 9 + v.y * 13 + v.z * 7) * Math.sin(v.y * 17 - v.z * 5);
    col.push(tono, tono, tono * 0.97);
    v.multiplyScalar(r);
    v.y = v.y < 0 ? v.y * 0.35 : v.y * 0.7;              // base plana, más ancha que alta
    p.setXYZ(i, v.x * tam, v.y * tam, v.z * tam);
  }
  // normales suaves: promedia las de las caras que comparten posición
  geo.computeVertexNormals();
  const n = geo.attributes.normal, suma = new Map();
  const clave = (i) => `${p.getX(i).toFixed(4)},${p.getY(i).toFixed(4)},${p.getZ(i).toFixed(4)}`;
  for (let i = 0; i < p.count; i++) {
    const k = clave(i), a = suma.get(k) || new THREE.Vector3();
    suma.set(k, a.add(v.fromBufferAttribute(n, i)));
  }
  const propia = new THREE.Vector3();
  for (let i = 0; i < p.count; i++) {
    const a = suma.get(clave(i)).clone().normalize();
    propia.fromBufferAttribute(n, i);
    if (a.dot(propia) > 0.8) n.setXYZ(i, a.x, a.y, a.z);   // arista viva si el ángulo es grande
  }
  geo.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
  const m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color, roughness: 0.92, vertexColors: true }));
  m.rotation.y = azar(0, 6.28);
  m.castShadow = m.receiveShadow = true;
  return m;
}

// ---------- viento ----------
export function mecer(raiz, t) {
  raiz.traverse((o) => {
    if (o.userData.mecer !== undefined) {
      o.rotation.z = Math.sin(t * 0.9 + o.userData.mecer) * 0.012;
      o.rotation.x = Math.cos(t * 0.7 + o.userData.mecer) * 0.008;
    }
    if (o.userData.nube !== undefined) o.position.x += o.userData.nube * 0.004;
  });
}
