// vegetation.js — trees with real leaves, soft clouds and crack-free rocks for three.js (>= 0.150).
// Crowns = hundreds of leaf cards with alphaTest and volume normals (not spheres);
// clouds = shaded vapor sprites, white on top and grey below (not balls);
// rocks = an icosahedron displaced as a function of position (no cracks between faces).
//   import { tree, cloud, rock, sway } from './vegetation.js';
//   scene.add(tree({ kind: 'oak', height: 6 }));      // 'oak' | 'birch' | 'pine'
//   scene.add(cloud({ width: 40 }));                  // far and high: y 25-60
//   scene.add(rock({ size: 1 }));                     // rest it: position.y = ground
//   in the loop: sway(scene, clock.getElapsedTime());
import * as THREE from 'three';

const rand = (a, b) => a + Math.random() * (b - a);

// ---------- textures (canvas, no files) ----------
const cache = {};

function leafTexture(kind) {
  if (cache[kind]) return cache[kind];
  const c = document.createElement('canvas');
  c.width = c.height = 256;
  const g = c.getContext('2d');
  const pine = kind === 'pine';
  const n = pine ? 60 : 55;
  for (let i = 0; i < n; i++) {
    const x = rand(30, 226), y = rand(30, 226);
    const l = pine ? rand(50, 80) : rand(40, 62);
    const a = pine ? rand(0.14, 0.2) * l : rand(0.3, 0.42) * l;
    const hue = pine ? rand(105, 135) : kind === 'birch' ? rand(70, 95) : rand(85, 112);
    const light = pine ? rand(20, 34) : rand(28, 50);
    g.save();
    g.translate(x, y);
    g.rotate(rand(0, Math.PI * 2));
    g.beginPath();
    g.moveTo(-l / 2, 0);
    g.quadraticCurveTo(0, -a, l / 2, 0);
    g.quadraticCurveTo(0, a, -l / 2, 0);
    g.fillStyle = `hsl(${hue} ${rand(35, 55)}% ${light}%)`;
    g.fill();
    if (!pine) {
      g.strokeStyle = `hsl(${hue} 40% ${light - 8}%)`;
      g.lineWidth = 1.2;
      g.beginPath(); g.moveTo(-l / 2, 0); g.lineTo(l / 2, 0); g.stroke();
    }
    g.restore();
  }
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 4;
  return (cache[kind] = t);
}

function vaporTexture() {
  if (cache.vapor) return cache.vapor;
  const s = 128, c = document.createElement('canvas');
  c.width = c.height = s;
  const g = c.getContext('2d');
  const img = g.createImageData(s, s);
  // smooth gaussian falloff, solid in the middle: the relief comes from overlapping puffs,
  // not from blotches inside the sprite (those read as holes)
  for (let y = 0; y < s; y++) for (let x = 0; x < s; x++) {
    const dx = x / s - 0.5, dy = y / s - 0.5;
    const r2 = (dx * dx + dy * dy) * 4;
    const v = r2 >= 1 ? 0 : Math.min(1, 1.6 * Math.exp(-r2 * 3.2)) * (1 - r2);
    const i = (y * s + x) * 4;
    // each puff shaded like a ball of vapor lit from above: light on top, grey below
    const light = 255 * (1 - 0.18 * Math.max(0, Math.min(1, y / s * 1.15 - 0.1)));
    img.data[i] = img.data[i + 1] = img.data[i + 2] = light;
    img.data[i + 3] = v * 255;
  }
  g.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return (cache.vapor = t);
}

// ---------- crown: leaf cards merged into a single mesh ----------
// Every card carries the crown's volume normal (from its center outwards): the crown is
// lit like a soft volume, not like cardboard. Vertex color = occlusion inside.
function crown({ kind, centers, radius, cards }) {
  const pos = [], nor = [], uv = [], col = [], idx = [];
  const side = radius * (kind === 'pine' ? 0.55 : 0.5);
  const q = new THREE.Quaternion(), e = new THREE.Euler();
  const v = new THREE.Vector3(), center = new THREE.Vector3(), dir = new THREE.Vector3();
  const corners = [[-1, -1], [1, -1], [1, 1], [-1, 1]];
  for (let k = 0; k < cards; k++) {
    const [cx, cy, cz, r] = centers[k % centers.length];
    center.set(cx, cy, cz);
    dir.set(rand(-1, 1), rand(-1, 1), rand(-1, 1)).normalize();
    const d = r * Math.pow(Math.random(), 0.35);           // more leaves near the skin
    const p = center.clone().addScaledVector(dir, d);
    e.set(rand(0, Math.PI), rand(0, Math.PI), rand(0, Math.PI));
    q.setFromEuler(e);
    const out = p.clone().sub(center).normalize();
    const occlusion = 0.55 + 0.45 * (d / r);
    const up = 0.85 + 0.15 * out.y;
    const base = pos.length / 3;
    const size = side * rand(0.75, 1.2);
    for (const [sx, sy] of corners) {
      v.set(sx * size / 2, sy * size / 2, 0).applyQuaternion(q).add(p);
      pos.push(v.x, v.y, v.z);
      nor.push(out.x, out.y, out.z);
      uv.push((sx + 1) / 2, (sy + 1) / 2);
      const c = occlusion * up;
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
    map: leafTexture(kind), alphaTest: 0.35, side: THREE.DoubleSide,
    vertexColors: true, roughness: 0.85,
  });
  mat.onBeforeCompile = (sh) => {
    sh.fragmentShader = sh.fragmentShader.replace('normal *= faceDirection;', '');
  };
  const m = new THREE.Mesh(geo, mat);
  m.castShadow = m.receiveShadow = true;
  m.userData.sway = rand(0, 6.28);
  const fill = new THREE.MeshStandardMaterial({
    color: kind === 'pine' ? 0x1a3520 : 0x27441b, roughness: 1,
  });
  for (const [cx, cy, cz, r] of centers) {
    const b = new THREE.Mesh(new THREE.IcosahedronGeometry(r * 0.5, 2), fill);
    b.position.set(cx, cy, cz);
    b.receiveShadow = true;
    m.add(b);
  }
  return m;
}

// ---------- tree ----------
const BARK = { oak: 0x4a3626, birch: 0xd9d4c7, pine: 0x3b2a1e };

function branch(from, to, r0, r1, mat) {
  const len = from.distanceTo(to);
  const g = new THREE.CylinderGeometry(r1, r0, len, 7, 1);
  g.translate(0, len / 2, 0);
  const m = new THREE.Mesh(g, mat);
  m.position.copy(from);
  m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), to.clone().sub(from).normalize());
  m.castShadow = true;
  return m;
}

export function tree({ kind = 'oak', height = 6 } = {}) {
  const g = new THREE.Group();
  const bark = new THREE.MeshStandardMaterial({ color: BARK[kind], roughness: 0.95 });
  const h = height;
  if (kind === 'pine') {
    g.add(branch(new THREE.Vector3(), new THREE.Vector3(0, h, 0), h * 0.035, h * 0.008, bark));
    const centers = [];
    for (let i = 0; i < 7; i++) {                     // tiers that narrow upwards
      const t = i / 6, r = h * 0.3 * (1 - t * 0.85);   // cone: wide below, tip on top
      centers.push([0, h * (0.22 + t * 0.72), 0, r]);
    }
    g.add(crown({ kind, centers, radius: h * 0.16, cards: Math.round(h * 200) }));
    return g;
  }
  const trunk = h * (kind === 'birch' ? 0.45 : 0.35);
  const up = new THREE.Vector3(rand(-0.2, 0.2), trunk, rand(-0.2, 0.2));
  g.add(branch(new THREE.Vector3(), up, h * 0.05, h * 0.03, bark));
  // 3-5 branches ending in clusters: an irregular silhouette with gaps of sky
  const centers = [[up.x, up.y + h * 0.22, up.z, h * 0.26]];
  const nBranches = Math.floor(rand(3, 6));
  for (let i = 0; i < nBranches; i++) {
    const ang = (i / nBranches) * Math.PI * 2 + rand(-0.4, 0.4);
    const reach = h * rand(0.2, 0.32);
    const end = up.clone().add(new THREE.Vector3(Math.cos(ang) * reach, h * rand(0.08, 0.35), Math.sin(ang) * reach));
    g.add(branch(up, end, h * 0.022, h * 0.01, bark));
    centers.push([end.x, end.y + h * 0.04, end.z, h * rand(0.17, 0.23)]);
  }
  g.add(crown({ kind, centers, radius: h * 0.2, cards: Math.round(h * (kind === 'birch' ? 160 : 220)) }));
  return g;
}

// ---------- cloud ----------
// sun = direction towards the sun (the DirectionalLight's): that side comes out lighter.
export function cloud({ width = 40, tall = width * 0.3, puffs = 70, sun = new THREE.Vector3(0.4, 1, 0.3) } = {}) {
  const toSun = sun.clone().normalize();
  const middle = new THREE.Vector3(0, tall * 0.35, 0), d = new THREE.Vector3();
  const g = new THREE.Group();
  const tex = vaporTexture();
  for (let i = 0; i < puffs; i++) {
    const x = (Math.random() + Math.random() - 1) * 0.5 * width;   // denser in the middle
    const edge = 1 - Math.abs(x) / (width / 2);          // taller in the middle
    const y = Math.pow(Math.random(), 1.6) * tall * (0.35 + 0.65 * edge);
    const z = rand(-0.25, 0.25) * width * 0.5;
    // blue-grey base and near-white top; the sun side lighter, the far side in shadow
    const t = Math.min(1, y / tall);
    const side = d.set(x, y, z).sub(middle).normalize().dot(toSun);
    const l = Math.min(1, 0.74 + 0.22 * t + 0.1 * side);
    const c = new THREE.Color().setRGB(l * 0.95, l * 0.97, Math.min(1, l * 1.02));
    const mat = new THREE.SpriteMaterial({
      map: tex, color: c, transparent: true, depthWrite: false,
      opacity: rand(0.7, 0.95), fog: false, toneMapped: false,
    });
    const s = new THREE.Sprite(mat);
    const size = width * rand(0.22, 0.38) * (0.6 + 0.4 * edge);
    s.scale.set(size, size * rand(0.75, 1), 1);
    s.position.set(x, y, z);
    g.add(s);
  }
  g.userData.cloud = rand(0.3, 0.8);
  return g;
}

// ---------- rock ----------
// The usual bug: displacing each vertex with Math.random(). three's geometries don't share
// vertices between faces, so each face moves on its own and cracks open.
// Here the displacement depends only on position: same vertex, same place.
export function rock({ size = 1, color = 0x7a7d74 } = {}) {
  const geo = new THREE.IcosahedronGeometry(1, 4);
  const p = geo.attributes.position, v = new THREE.Vector3();
  const randDir = () => new THREE.Vector3(rand(-1, 1), rand(-1, 1), rand(-1, 1)).normalize();
  const waves = Array.from({ length: 9 }, (_, k) => [randDir(), rand(2, 4) * (1 + k * 0.6), rand(0, 6.28), 0.1 / (1 + k * 0.7)]);
  // flat cuts: fracture faces with edges, what sets it apart from a smooth pebble
  const cuts = Array.from({ length: Math.floor(rand(4, 8)) }, () => [randDir(), rand(0.62, 0.85)]);
  const col = [];
  for (let i = 0; i < p.count; i++) {
    v.fromBufferAttribute(p, i).normalize();
    let r = 1;
    for (const [d, f, phase, a] of waves) r += Math.sin(v.dot(d) * f + phase) * a;
    for (const [d, dist] of cuts) { const c = v.dot(d); if (c > 0.05) r = Math.min(r, dist / c); }
    const hue = 0.8 + 0.2 * Math.sin(v.x * 9 + v.y * 13 + v.z * 7) * Math.sin(v.y * 17 - v.z * 5);
    col.push(hue, hue, hue * 0.97);
    v.multiplyScalar(r);
    v.y = v.y < 0 ? v.y * 0.35 : v.y * 0.7;              // flat base, wider than tall
    p.setXYZ(i, v.x * size, v.y * size, v.z * size);
  }
  // smooth normals: average the faces that share a position
  geo.computeVertexNormals();
  const n = geo.attributes.normal, sum = new Map();
  const key = (i) => `${p.getX(i).toFixed(4)},${p.getY(i).toFixed(4)},${p.getZ(i).toFixed(4)}`;
  for (let i = 0; i < p.count; i++) {
    const k = key(i), a = sum.get(k) || new THREE.Vector3();
    sum.set(k, a.add(v.fromBufferAttribute(n, i)));
  }
  const own = new THREE.Vector3();
  for (let i = 0; i < p.count; i++) {
    const a = sum.get(key(i)).clone().normalize();
    own.fromBufferAttribute(n, i);
    if (a.dot(own) > 0.8) n.setXYZ(i, a.x, a.y, a.z);   // keep a sharp edge where the angle is large
  }
  geo.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
  const m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color, roughness: 0.92, vertexColors: true }));
  m.rotation.y = rand(0, 6.28);
  m.castShadow = m.receiveShadow = true;
  return m;
}

// ---------- wind ----------
export function sway(root, t) {
  root.traverse((o) => {
    if (o.userData.sway !== undefined) {
      o.rotation.z = Math.sin(t * 0.9 + o.userData.sway) * 0.012;
      o.rotation.x = Math.cos(t * 0.7 + o.userData.sway) * 0.008;
    }
    if (o.userData.cloud !== undefined) o.position.x += o.userData.cloud * 0.004;
  });
}
