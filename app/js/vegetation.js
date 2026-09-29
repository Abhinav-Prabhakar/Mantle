// Desert vegetation as painted cross-billboards: khejri trees (Prosopis cineraria) with
// umbrella canopies of fine leaflets, and dry thorny shrubs. Canvas-painted at runtime,
// alpha-tested (shadows respect the cut-out), instanced.
import * as THREE from 'three';
import { mulberry32 } from './textures.js';
import { groundHeight } from './terrain.js';

function paintTree(seed) {
  const W = 512, H = 512, c = document.createElement('canvas'); c.width = W; c.height = H;
  const g = c.getContext('2d'), rnd = mulberry32(seed);
  // twisted trunk with a few forks
  const branch = (x, y, a, len, w, depth) => {
    const segs = 6;
    let px = x, py = y, ang = a;
    for (let i = 0; i < segs; i++) {
      ang += (rnd() - 0.5) * 0.35;
      const nx = px + Math.cos(ang) * len / segs, ny = py - Math.sin(ang) * len / segs;
      g.strokeStyle = `rgb(${58 + rnd() * 20},${44 + rnd() * 14},${34 + rnd() * 10})`;
      g.lineWidth = w * (1 - i / segs * 0.5); g.lineCap = 'round';
      g.beginPath(); g.moveTo(px, py); g.lineTo(nx, ny); g.stroke();
      px = nx; py = ny;
    }
    if (depth > 0) {
      const n = depth > 1 ? 3 : 4;
      for (let k = 0; k < n; k++) branch(px, py, ang + (rnd() - 0.5) * 1.6, len * (0.45 + rnd() * 0.25), w * 0.55, depth - 1);
    } else tips.push([px, py]);
  };
  const tips = [];
  branch(W / 2 + (rnd() - 0.5) * 20, H - 6, Math.PI / 2 + (rnd() - 0.5) * 0.2, 190, 20, 3);
  // umbrella canopy: layered leaf clumps, darker underneath, sun-lit on top
  const clumps = [];
  for (let i = 0; i < 70; i++) {
    const t = tips[(rnd() * tips.length) | 0];
    clumps.push([t[0] + (rnd() - 0.5) * 70, t[1] + (rnd() - 0.6) * 40, 16 + rnd() * 26]);
  }
  clumps.sort((a, b) => b[1] - a[1]);
  for (const [x, y, r] of clumps) {
    for (let k = 0; k < 90; k++) {
      const a = rnd() * Math.PI * 2, d = Math.sqrt(rnd()) * r;
      const lx = x + Math.cos(a) * d, ly = y + Math.sin(a) * d * 0.6;
      const top = 1 - (ly - (y - r * 0.6)) / (r * 1.2);
      const l = 0.18 + top * 0.2 + rnd() * 0.06;
      g.fillStyle = `hsl(${78 + rnd() * 18}, ${22 + rnd() * 12}%, ${l * 100}%)`;
      g.fillRect(lx, ly, 2 + rnd() * 2.5, 1.2 + rnd() * 1.6);
    }
  }
  return c;
}

function paintShrub(seed) {
  const W = 256, H = 256, c = document.createElement('canvas'); c.width = W; c.height = H;
  const g = c.getContext('2d'), rnd = mulberry32(seed);
  const dry = rnd() < 0.45;
  for (let i = 0; i < 70; i++) {
    const a = Math.PI / 2 + (rnd() - 0.5) * 2.4, len = 60 + rnd() * 120;
    let x = W / 2 + (rnd() - 0.5) * 30, y = H - 4, ang = a;
    g.lineCap = 'round';
    for (let s = 0; s < 5; s++) {
      ang += (rnd() - 0.5) * 0.5;
      const nx = x + Math.cos(ang) * len / 5, ny = y - Math.sin(ang) * len / 5;
      g.strokeStyle = dry ? `rgb(${120 + rnd() * 40},${98 + rnd() * 30},${70 + rnd() * 20})` : `rgb(${70 + rnd() * 25},${62 + rnd() * 20},${44 + rnd() * 14})`;
      g.lineWidth = 2.2 - s * 0.35;
      g.beginPath(); g.moveTo(x, y); g.lineTo(nx, ny); g.stroke();
      x = nx; y = ny;
      if (!dry || rnd() < 0.3) for (let k = 0; k < 7; k++) {
        g.fillStyle = dry ? `hsl(${34 + rnd() * 10}, ${25 + rnd() * 15}%, ${40 + rnd() * 18}%)` : `hsl(${70 + rnd() * 25}, ${18 + rnd() * 18}%, ${24 + rnd() * 16}%)`;
        g.fillRect(x + (rnd() - 0.5) * 14, y + (rnd() - 0.5) * 10, 2 + rnd() * 2, 1.5 + rnd() * 1.5);
      }
    }
  }
  return c;
}

function crossGeometry(w, h, planes = 2) {
  const geos = [];
  for (let i = 0; i < planes; i++) {
    const p = new THREE.PlaneGeometry(w, h);
    p.translate(0, h / 2, 0);
    p.rotateY((i / planes) * Math.PI);
    geos.push(p);
  }
  const g = mergeGeos(geos);
  // soft, sky-facing normals: foliage reads lit from every side instead of flat cards
  const n = g.attributes.normal;
  for (let i = 0; i < n.count; i++) n.setXYZ(i, 0, 1, 0);
  return g;
}
function mergeGeos(list) {
  const pos = [], uv = [], nor = [], idx = [];
  let off = 0;
  for (const g of list) {
    const p = g.attributes.position, u = g.attributes.uv, n = g.attributes.normal;
    for (let i = 0; i < p.count; i++) { pos.push(p.getX(i), p.getY(i), p.getZ(i)); uv.push(u.getX(i), u.getY(i)); nor.push(n.getX(i), n.getY(i), n.getZ(i)); }
    for (const i of g.index.array) idx.push(i + off);
    off += p.count;
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
  g.setAttribute('normal', new THREE.Float32BufferAttribute(nor, 3));
  g.setIndex(idx);
  return g;
}

function foliageMaterial(canvas) {
  const t = new THREE.CanvasTexture(canvas);
  t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
  const m = new THREE.MeshStandardMaterial({ map: t, alphaTest: 0.5, side: THREE.DoubleSide, roughness: 0.92, metalness: 0 });
  const depth = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking, map: t, alphaTest: 0.5 });
  return { m, depth };
}

export function buildVegetation(scene, avoid) {
  const group = new THREE.Group(); group.name = 'vegetation'; scene.add(group);
  const rnd = mulberry32(88);
  const q = new THREE.Quaternion(), s = new THREE.Vector3(), p = new THREE.Vector3(), mtx = new THREE.Matrix4(), col = new THREE.Color();

  // 3 tree variants × instances
  for (let v = 0; v < 3; v++) {
    const { m, depth } = foliageMaterial(paintTree(100 + v * 7));
    const geo = crossGeometry(7, 7, 3);
    const N = 2, im = new THREE.InstancedMesh(geo, m, N);
    im.customDepthMaterial = depth;
    let i = 0;
    while (i < N) {
      const x = -31 + rnd() * 64, z = -40 + rnd() * 40;
      if (avoid(x, z)) continue;
      const sc = 0.55 + rnd() * 0.35;
      q.setFromEuler(new THREE.Euler(0, rnd() * Math.PI, 0));
      im.setMatrixAt(i, mtx.compose(p.set(x, groundHeight(x, z) - 0.15, z), q, s.set(sc * (0.9 + rnd() * 0.3), sc, sc)));
      im.setColorAt(i, col.setScalar(0.85 + rnd() * 0.3));
      i++;
    }
    im.castShadow = true; im.receiveShadow = true;
    group.add(im);
  }
  // 4 shrub variants
  for (let v = 0; v < 4; v++) {
    const { m, depth } = foliageMaterial(paintShrub(300 + v * 13));
    const geo = crossGeometry(1.6, 1.6, 2);
    const N = 26, im = new THREE.InstancedMesh(geo, m, N);
    im.customDepthMaterial = depth;
    let i = 0;
    while (i < N) {
      const x = -31 + rnd() * 64, z = -40 + rnd() * 40;
      if (avoid(x, z)) continue;
      const sc = 0.35 + rnd() * rnd() * 1.1;
      q.setFromEuler(new THREE.Euler(0, rnd() * Math.PI, 0));
      im.setMatrixAt(i, mtx.compose(p.set(x, groundHeight(x, z) - 0.05, z), q, s.set(sc * (0.8 + rnd() * 0.6), sc, sc)));
      im.setColorAt(i, col.setScalar(0.8 + rnd() * 0.35));
      i++;
    }
    im.castShadow = true; im.receiveShadow = true;
    group.add(im);
  }
  return group;
}
