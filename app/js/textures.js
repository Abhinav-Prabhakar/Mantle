// Procedural textures — every surface is painted at runtime on a canvas, no image assets.
// Height canvases are converted to tangent-space normal maps with a Sobel filter.
import * as THREE from 'three';
import { STRATA, depthToY, PIT_DEPTH } from './rig.js';

export function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/* ------------------------------------------------------------------ value noise (tileable) */

function makeNoise(seed) {
  const rnd = mulberry32(seed);
  const P = 256, perm = new Uint8Array(P * 2), g = new Float32Array(P);
  for (let i = 0; i < P; i++) { perm[i] = i; g[i] = rnd(); }
  for (let i = P - 1; i > 0; i--) { const j = (rnd() * (i + 1)) | 0; [perm[i], perm[j]] = [perm[j], perm[i]]; }
  for (let i = 0; i < P; i++) perm[i + P] = perm[i];
  const h = (x, y) => g[perm[(perm[x & 255] + (y & 255)) & 511]];
  // periodic value noise with period px, py (integers)
  return (x, y, px = 256, py = 256) => {
    const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
    const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
    const x0 = ((xi % px) + px) % px, x1 = (x0 + 1) % px, y0 = ((yi % py) + py) % py, y1 = (y0 + 1) % py;
    const a = h(x0, y0), b = h(x1, y0), c = h(x0, y1), d = h(x1, y1);
    return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
  };
}
function fbmT(noise, x, y, px, py, oct = 5) {
  let s = 0, a = 0.5, f = 1, n = 0;
  for (let i = 0; i < oct; i++) { s += a * noise(x * f, y * f, px * f, py * f); n += a; a *= 0.5; f *= 2; }
  return s / n;
}

function canvas(w, h) {
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  return c;
}

// height (Float32Array w*h, 0..1) -> normal map canvas
function normalFromHeight(hgt, w, h, strength = 2, wrapX = true, wrapY = true) {
  const c = canvas(w, h), g = c.getContext('2d'), img = g.createImageData(w, h), d = img.data;
  const at = (x, y) => {
    x = wrapX ? (x + w) % w : Math.min(w - 1, Math.max(0, x));
    y = wrapY ? (y + h) % h : Math.min(h - 1, Math.max(0, y));
    return hgt[y * w + x];
  };
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const dx = (at(x + 1, y - 1) + 2 * at(x + 1, y) + at(x + 1, y + 1)) - (at(x - 1, y - 1) + 2 * at(x - 1, y) + at(x - 1, y + 1));
    const dy = (at(x - 1, y + 1) + 2 * at(x, y + 1) + at(x + 1, y + 1)) - (at(x - 1, y - 1) + 2 * at(x, y - 1) + at(x + 1, y - 1));
    let nx = -dx * strength, ny = dy * strength, nz = 1;
    const l = Math.hypot(nx, ny, nz); nx /= l; ny /= l; nz /= l;
    const i = (y * w + x) * 4;
    d[i] = (nx * 0.5 + 0.5) * 255; d[i + 1] = (ny * 0.5 + 0.5) * 255; d[i + 2] = (nz * 0.5 + 0.5) * 255; d[i + 3] = 255;
  }
  g.putImageData(img, 0, 0);
  return c;
}

function tex(c, { repeat = true, srgb = true, aniso = 8 } = {}) {
  const t = new THREE.CanvasTexture(c);
  if (repeat) t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.colorSpace = srgb ? THREE.SRGBColorSpace : THREE.NoColorSpace;
  t.anisotropy = aniso;
  t.generateMipmaps = true;
  t.minFilter = THREE.LinearMipmapLinearFilter;
  return t;
}

/* ------------------------------------------------------------------ desert soil */

// Compacted Thar soil: a pale, wind-scoured silty crust broken into shallow polygons,
// loose fines in the lows, scattered grit and small calcrete pebbles. Deliberately muted.
export function soilTextures(seed = 7) {
  const S = 1024, n = makeNoise(seed), n2 = makeNoise(seed + 11), n3 = makeNoise(seed + 23);
  const rnd = mulberry32(seed + 3);
  const hgt = new Float32Array(S * S), alb = new Float32Array(S * S * 3), ro = new Float32Array(S * S);
  // Voronoi crust polygons (tileable): distance to nearest and second-nearest cell centre
  const G = 9, pts = [];
  for (let j = 0; j < G; j++) for (let i = 0; i < G; i++) pts.push([(i + 0.15 + rnd() * 0.7) / G, (j + 0.15 + rnd() * 0.7) / G]);
  const crack = (u, v) => {
    const ci = Math.floor(u * G), cj = Math.floor(v * G);
    let d1 = 9, d2 = 9;
    for (let dj = -1; dj <= 1; dj++) for (let di = -1; di <= 1; di++) {
      const ii = ci + di, jj = cj + dj, iw = ((ii % G) + G) % G, jw = ((jj % G) + G) % G, p = pts[jw * G + iw];
      const px = p[0] + (ii - iw) / G, py = p[1] + (jj - jw) / G;
      const dx = u - px, dy = v - py, d = dx * dx + dy * dy;
      if (d < d1) { d2 = d1; d1 = d; } else if (d < d2) d2 = d;
    }
    return Math.sqrt(d2) - Math.sqrt(d1);
  };
  for (let y = 0; y < S; y++) for (let x = 0; x < S; x++) {
    const u = x / S, v = y / S, k = y * S + x;
    const w1 = fbmT(n, u * 8, v * 8, 8, 8, 3), w2 = fbmT(n2, u * 8 + 3, v * 8, 8, 8, 3);
    const e = crack(u + (w1 - 0.5) * 0.02, v + (w2 - 0.5) * 0.02);
    const edge = 1 - Math.min(1, e / 0.006);                 // crack line
    const plate = Math.min(1, e / 0.03);                       // plates dome slightly
    const blotch = fbmT(n3, u * 4, v * 4, 4, 4, 5);
    const fines = Math.max(0, 0.5 - blotch) * 2;               // loose dust pooled in lows
    const grain = rnd();
    const streak = fbmT(n2, u * 2, v * 22, 2, 22, 3);          // faint wind scour
    hgt[k] = plate * 0.25 * (1 - fines) - edge * 0.35 + grain * 0.06 + streak * 0.08;
    let t = 0.9 + (blotch - 0.5) * 0.28 + (grain - 0.5) * 0.1 + (streak - 0.5) * 0.08 - edge * 0.22 + fines * 0.06;
    let r = 176 * t, g = 160 * t, b = 136 * t;
    if (grain > 0.992) { r = 205; g = 196; b = 180; } else if (grain < 0.01) { r *= 0.5; g *= 0.48; b *= 0.46; }
    alb[k * 3] = r; alb[k * 3 + 1] = g; alb[k * 3 + 2] = b;
    ro[k] = 238 - fines * 10 - (grain > 0.992 ? 60 : 0);
  }
  // scattered grit and pebbles (calcrete, quartz, ironstone)
  for (let p = 0; p < 1800; p++) {
    const cx = rnd() * S, cy = rnd() * S, r = 0.8 + rnd() * rnd() * rnd() * 7;
    const kind = rnd(), tone = kind < 0.6 ? [196, 186, 168] : kind < 0.85 ? [150, 128, 104] : [112, 82, 62];
    const ri = Math.ceil(r);
    for (let yy = -ri; yy <= ri; yy++) for (let xx = -ri; xx <= ri; xx++) {
      const dd = (xx * xx + yy * yy) / (r * r);
      if (dd > 1) continue;
      const k = (((cy + yy) | 0) + S) % S * S + ((((cx + xx) | 0) + S) % S);
      const sh = Math.sqrt(1 - dd), lit = 0.8 + 0.3 * (-(xx + yy) / (2 * r));
      alb[k * 3] = tone[0] * lit; alb[k * 3 + 1] = tone[1] * lit; alb[k * 3 + 2] = tone[2] * lit;
      hgt[k] = Math.max(hgt[k], 0.2 + sh * (0.3 + r / 10));
      ro[k] = 200;
    }
  }
  const c = canvas(S, S), g = c.getContext('2d'), img = g.createImageData(S, S), d = img.data;
  const rough = canvas(S, S), rg = rough.getContext('2d'), rimg = rg.createImageData(S, S), rd = rimg.data;
  for (let k = 0; k < S * S; k++) {
    d[k * 4] = alb[k * 3]; d[k * 4 + 1] = alb[k * 3 + 1]; d[k * 4 + 2] = alb[k * 3 + 2]; d[k * 4 + 3] = 255;
    rd[k * 4] = rd[k * 4 + 1] = rd[k * 4 + 2] = ro[k]; rd[k * 4 + 3] = 255;
  }
  g.putImageData(img, 0, 0); rg.putImageData(rimg, 0, 0);
  return { map: tex(c), normalMap: tex(normalFromHeight(hgt, S, S, 2.4), { srgb: false }), roughnessMap: tex(rough, { srgb: false }) };
}
export const sandTextures = soilTextures;

/* ------------------------------------------------------------------ gravel pad */

export function gravelTextures(seed = 21) {
  const S = 512, rnd = mulberry32(seed), n = makeNoise(seed);
  const c = canvas(S, S), g = c.getContext('2d');
  const hgt = new Float32Array(S * S);
  g.fillStyle = '#9d9282'; g.fillRect(0, 0, S, S);
  const img0 = g.getImageData(0, 0, S, S), d0 = img0.data;
  for (let y = 0; y < S; y++) for (let x = 0; x < S; x++) {
    const i = (y * S + x) * 4, k = 0.8 + fbmT(n, x / 64, y / 64, 8, 8, 4) * 0.35;
    d0[i] *= k; d0[i + 1] *= k; d0[i + 2] *= k;
  }
  g.putImageData(img0, 0, 0);
  // pebbles: painted discs + a matching height bump
  for (let p = 0; p < 2600; p++) {
    const x = rnd() * S, y = rnd() * S, r = 1.5 + rnd() * rnd() * 7;
    const tone = 110 + rnd() * 110, warm = rnd() * 22;
    for (const [ox, oy] of [[0, 0], [S, 0], [-S, 0], [0, S], [0, -S]]) {
      const cx = x + ox, cy = y + oy;
      if (cx < -r || cx > S + r || cy < -r || cy > S + r) continue;
      const gr = g.createRadialGradient(cx - r * 0.3, cy - r * 0.3, r * 0.1, cx, cy, r);
      gr.addColorStop(0, `rgb(${tone + 40 + warm},${tone + 34},${tone + 24})`);
      gr.addColorStop(1, `rgb(${tone * 0.7 + warm},${tone * 0.66},${tone * 0.6})`);
      g.fillStyle = gr; g.beginPath(); g.ellipse(cx, cy, r, r * (0.7 + rnd() * 0.3), rnd() * 3, 0, Math.PI * 2); g.fill();
    }
    const xi = x | 0, yi = y | 0, ri = Math.ceil(r);
    for (let yy = -ri; yy <= ri; yy++) for (let xx = -ri; xx <= ri; xx++) {
      const dd = (xx * xx + yy * yy) / (r * r);
      if (dd > 1) continue;
      const k = ((yi + yy + S) % S) * S + ((xi + xx + S) % S);
      hgt[k] = Math.max(hgt[k], Math.sqrt(1 - dd) * (0.4 + r / 12));
    }
  }
  // oil staining near the wellhead is added with a decal elsewhere
  return { map: tex(c), normalMap: tex(normalFromHeight(hgt, S, S, 1.6), { srgb: false }) };
}

/* ------------------------------------------------------------------ concrete */

export function concreteTextures(seed = 33) {
  const S = 512, n = makeNoise(seed), n2 = makeNoise(seed + 1), rnd = mulberry32(seed);
  const c = canvas(S, S), g = c.getContext('2d'), img = g.createImageData(S, S), d = img.data;
  const hgt = new Float32Array(S * S);
  for (let y = 0; y < S; y++) for (let x = 0; x < S; x++) {
    const u = x / S, v = y / S;
    const m = fbmT(n, u * 5, v * 5, 5, 5, 5), s = fbmT(n2, u * 24, v * 24, 24, 24, 3);
    const pit = rnd() > 0.992 ? -0.4 : 0;
    const k = 0.78 + m * 0.3 + s * 0.08 + pit * 0.3;
    const i = (y * S + x) * 4;
    d[i] = 176 * k; d[i + 1] = 172 * k; d[i + 2] = 162 * k; d[i + 3] = 255;
    hgt[y * S + x] = s * 0.3 + pit;
  }
  g.putImageData(img, 0, 0);
  // hairline cracks + rust drip stains
  g.globalAlpha = 0.35; g.strokeStyle = '#4b4740'; g.lineWidth = 0.8;
  for (let k = 0; k < 7; k++) {
    let x = rnd() * S, y = rnd() * S; g.beginPath(); g.moveTo(x, y);
    for (let s = 0; s < 18; s++) { x += (rnd() - 0.5) * 22; y += (rnd() - 0.3) * 16; g.lineTo(x, y); }
    g.stroke();
  }
  g.globalAlpha = 1;
  return { map: tex(c), normalMap: tex(normalFromHeight(hgt, S, S, 1.2), { srgb: false }) };
}

/* ------------------------------------------------------------------ painted steel (grime + wear) */

export function paintTextures(seed = 44) {
  const S = 256, n = makeNoise(seed), rnd = mulberry32(seed);
  // grey-scale albedo multiplier: tinted by material colour, keeps a single texture for all paints
  const c = canvas(S, S), g = c.getContext('2d'), img = g.createImageData(S, S), d = img.data;
  const r = canvas(S, S), rg = r.getContext('2d'), rimg = rg.createImageData(S, S), rd = rimg.data;
  const hgt = new Float32Array(S * S);
  for (let y = 0; y < S; y++) for (let x = 0; x < S; x++) {
    const u = x / S, v = y / S;
    const grime = fbmT(n, u * 6, v * 6, 6, 6, 5);
    const chip = fbmT(n, u * 22 + 9, v * 22 + 3, 22, 22, 3);
    const worn = chip > 0.7 ? 1 : 0;
    const i = (y * S + x) * 4;
    const k = worn ? 0.55 : 0.9 + grime * 0.16 + (rnd() - 0.5) * 0.04;
    d[i] = k * 255; d[i + 1] = k * 250; d[i + 2] = k * 240; d[i + 3] = 255;
    const ro = worn ? 150 : 115 + grime * 70;
    rd[i] = rd[i + 1] = rd[i + 2] = ro; rd[i + 3] = 255;
    hgt[y * S + x] = worn ? 0 : 0.35 + grime * 0.05;
  }
  g.putImageData(img, 0, 0); rg.putImageData(rimg, 0, 0);
  return { map: tex(c), roughnessMap: tex(r, { srgb: false }), normalMap: tex(normalFromHeight(hgt, S, S, 0.9), { srgb: false }) };
}

// Black/yellow hazard chevrons for the counterweights.
export function hazardTexture() {
  const c = canvas(256, 64), g = c.getContext('2d');
  g.fillStyle = '#e1a91a'; g.fillRect(0, 0, 256, 64);
  g.fillStyle = '#16161a';
  for (let x = -64; x < 256 + 64; x += 32) {
    g.beginPath(); g.moveTo(x, 64); g.lineTo(x + 16, 64); g.lineTo(x + 48, 0); g.lineTo(x + 32, 0); g.closePath(); g.fill();
  }
  return tex(c, { repeat: false });
}

/* ------------------------------------------------------------------ strata section (pit walls) */

// One tall texture covering the full visual pit depth. v = 0 at the surface, 1 at PIT_DEPTH.
// u tiles horizontally every STRATA_TILE_M metres. Each formation gets its own fabric:
// mineral mottling (domain-warped fbm), laminae, joints/fractures, excavator tool marks.
export const STRATA_TILE_M = 14;
const PALETTES = {
  // [mid, light, dark, accent]  (muted, desaturated natural rock tones)
  sand: [[176, 158, 126], [200, 184, 152], [140, 124, 98], [186, 172, 146]],
  tert: [[128, 116, 100], [152, 140, 122], [96, 87, 76], [150, 146, 128]],
  nagaur: [[116, 92, 84], [138, 112, 100], [86, 66, 61], [128, 122, 108]],
  bilara: [[142, 138, 126], [170, 166, 152], [108, 105, 98], [196, 192, 180]],
  carb: [[104, 100, 92], [128, 122, 110], [76, 72, 68], [160, 156, 146]],
  jodhpur: [[62, 47, 36], [86, 66, 50], [30, 22, 17], [98, 84, 66]],
  malani: [[104, 94, 94], [134, 120, 116], [66, 60, 62], [150, 132, 122]],
};
// per-formation fabric: bed thickness range (px), colour/lamina/macro contrasts, relief, roughness
const STRATA_FABRIC = {
  sand: { bed: [40, 110], cross: 0.85, bedC: 0.10, lamC: 0.30, macC: 0.18, fib: 0.05, gr: 0.12, hard: 0.10, lamR: 0.10, rough: 0.96, lamF: 0.55 },
  tert: { bed: [10, 46], cross: 0.0, bedC: 0.18, lamC: 0.22, macC: 0.14, fib: 0.06, gr: 0.06, hard: 0.26, lamR: 0.16, rough: 0.92, lamF: 0.8, coal: 0.07, bleach: 0.12 },
  nagaur: { bed: [24, 84], cross: 0.65, bedC: 0.20, lamC: 0.20, macC: 0.20, fib: 0.05, gr: 0.11, hard: 0.30, lamR: 0.12, rough: 0.94, lamF: 0.6, bleach: 0.16 },
  bilara: { bed: [30, 96], cross: 0, bedC: 0.20, lamC: 0.08, macC: 0.13, fib: 0.05, gr: 0.08, hard: 0.42, lamR: 0.05, rough: 0.86, lamF: 0.3, joints: true, vugs: 90, nod: 60, styl: 3 },
  carb: { bed: [20, 60], cross: 0, bedC: 0.20, lamC: 0.08, macC: 0.12, fib: 0.05, gr: 0.08, hard: 0.42, lamR: 0.05, rough: 0.84, lamF: 0.3, joints: true, vugs: 30, nod: 0, styl: 4 },
  jodhpur: { bed: [14, 42], cross: 0.7, bedC: 0.16, lamC: 0.20, macC: 0.20, fib: 0.05, gr: 0.10, hard: 0.20, lamR: 0.10, rough: 0.9, lamF: 0.6 },
  malani: { bed: [9999, 9999], cross: 0, bedC: 0.0, lamC: 0.0, macC: 0.30, fib: 0.10, gr: 0.16, hard: 0.0, lamR: 0.0, rough: 0.72, lamF: 0.0, massive: true },
};
export function strataTextures(seed = 77) {
  const W = 1024, H = 2048, n = makeNoise(seed), n2 = makeNoise(seed + 5), n3 = makeNoise(seed + 9), rnd = mulberry32(seed);
  const pxPerM = H / PIT_DEPTH;
  const c = canvas(W, H), g = c.getContext('2d'), img = g.createImageData(W, H), d = img.data;
  const hgt = new Float32Array(W * H);
  const rough = canvas(W, H), rg = rough.getContext('2d'), rimg = rg.createImageData(W, H), rdat = rimg.data;
  const bands = STRATA.map((s, i) => ({ ...s, i, y0: -depthToY(s.top) * pxPerM, y1: i === STRATA.length - 1 ? H : -depthToY(s.bot) * pxPerM, pal: PALETTES[s.id], F: STRATA_FABRIC[s.id] }));
  bands[0].y0 = 0;
  const NB = bands.length, PY = 999;
  const smooth01 = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
  const rr = (a, b) => a + (b - a) * rnd();

  /* ---- undulating contacts: boundary k sits at bands[k].y0 + cw[k][x] (same mean depth) */
  const cw = [];
  for (let k = 0; k < NB; k++) {
    const arr = new Float32Array(W);
    const amp = k === 0 ? 0 : bands[k].reservoir ? 9 : k === NB - 1 ? 6 : 4.5;   // erosional top of reservoir
    for (let x = 0; x < W; x++) {
      const u = x / W;
      let v = (fbmT(n3, u * 4 + k * 7, k * 3.1, 4, PY, 3) - 0.5) * 2 * amp;
      if (bands[k].reservoir) v += (fbmT(n2, u * 24 + k, 2.2, 24, PY, 3) - 0.5) * 6;   // rougher scour surface
      arr[x] = v;
    }
    cw.push(arr);
  }

  /* ---- bed tables, one entry per nominal row of each band */
  const rowBand = new Uint8Array(H), rowTone = new Float32Array(H), rowHard = new Float32Array(H), rowPos = new Float32Array(H), rowThick = new Float32Array(H);
  const rowBleach = new Float32Array(H), rowCoal = new Float32Array(H), rowSat = new Float32Array(H), rowAmp = new Float32Array(H), rowKx = new Float32Array(H), rowPh = new Float32Array(H), rowBedId = new Int32Array(H);
  const beds = [];
  let bedCount = 0;
  for (const b of bands) {
    const F = b.F, ya = Math.round(b.y0), yb = Math.round(b.y1);
    let y = ya;
    while (y < yb) {
      let th = F.massive ? yb - ya : rr(F.bed[0], F.bed[1]);
      const coal = F.coal && rnd() < F.coal;
      if (coal) th = rr(3, 7);
      const end = Math.min(yb, Math.round(y + th));
      const bed = { band: b.i, a: y, b: end, tone: rnd(), hard: rnd(), sat: rnd(), bleach: F.bleach && rnd() < F.bleach ? rr(0.5, 1) : 0, coal: coal ? 1 : 0, amp: rnd() < F.cross ? rr(8, 22) : 0, kx: 1 + Math.floor(rnd() * 3), ph: rnd() };
      beds.push(bed);
      for (let yy = y; yy < end; yy++) {
        rowBand[yy] = b.i; rowTone[yy] = bed.tone; rowHard[yy] = bed.hard; rowPos[yy] = yy - y; rowThick[yy] = end - y;
        rowBleach[yy] = bed.bleach; rowCoal[yy] = bed.coal; rowSat[yy] = bed.sat; rowAmp[yy] = bed.amp; rowKx[yy] = bed.kx; rowPh[yy] = bed.ph; rowBedId[yy] = bedCount;
      }
      bedCount++; y = end;
    }
  }

  /* ---- 1D lamina tables (sharpened so laminae read as thin crisp layers) */
  const LO = 120, LN = H + 2 * LO;
  const lamFine = new Float32Array(LN), lamMed = new Float32Array(LN);
  {
    const a = new Float32Array(LN + 2), bb = new Float32Array(LN + 2);
    for (let i = 0; i < a.length; i++) { a[i] = rnd(); bb[i] = rnd(); }
    for (let i = 0; i < LN; i++) {
      const f = i / 2.6, m = i / 11;
      const fi = Math.floor(f), mi = Math.floor(m), ff = f - fi, mf = m - mi;
      lamFine[i] = a[fi % a.length] * (1 - ff) + a[(fi + 1) % a.length] * ff;
      lamMed[i] = bb[mi % bb.length] * (1 - mf) + bb[(mi + 1) % bb.length] * mf;
    }
  }
  const lamAt = (s, wF) => {
    let i = s + LO; if (i < 0) i = 0; else if (i > LN - 2) i = LN - 2;
    const i0 = i | 0, f = i - i0;
    const a = lamFine[i0] * (1 - f) + lamFine[i0 + 1] * f, m = lamMed[i0] * (1 - f) + lamMed[i0 + 1] * f;
    return smooth01(0.25, 0.75, a * wF + m * (1 - wF));
  };

  /* ---- feature masks: dark (joints, partings, stylolites, vugs, fractures) and pale (evaporite) */
  const dark = new Float32Array(W * H), pale = new Float32Array(W * H);
  const put = (arr, x, y, v) => { if (y < 0 || y >= H) return; const k = y * W + ((x % W) + W) % W; if (v > arr[k]) arr[k] = v; };
  const ellipse = (arr, cx, cy, rx, ry, val) => {
    for (let dy = -Math.ceil(ry) - 1; dy <= Math.ceil(ry) + 1; dy++) for (let dx = -Math.ceil(rx) - 1; dx <= Math.ceil(rx) + 1; dx++) {
      const r = Math.hypot(dx / rx, dy / ry); if (r < 1.1) put(arr, Math.round(cx) + dx, Math.round(cy) + dy, val * (1 - smooth01(0.7, 1.1, r)));
    }
  };
  const crackWalk = (x, y, ang, len, val, wid) => {
    for (let i = 0; i < len; i++) {
      ang += (rnd() - 0.5) * 0.45; x += Math.cos(ang) * 1.3; y += Math.sin(ang) * 1.3;
      const xi = Math.round(x), yi = Math.round(y); if (yi < 0 || yi >= H) return;
      put(dark, xi, yi, val); if (wid) { put(dark, xi + 1, yi, val * 0.5); put(dark, xi - 1, yi, val * 0.5); }
    }
  };
  for (const b of bands) {
    const F = b.F, ya = Math.round(b.y0), yb = Math.round(b.y1);
    const bedsHere = beds.filter((q) => q.band === b.i);
    if (F.joints) {
      for (const q of bedsHere) {                    // vertical joints stop at bedding planes, stagger bed to bed
        const nj = Math.floor(rnd() * 3);
        for (let j = 0; j < nj; j++) {
          let x = rnd() * W; const val = rr(0.55, 1);
          for (let y = q.a; y < q.b; y++) { x += (rnd() - 0.5) * 0.9; put(dark, Math.round(x), y, val); if (rnd() < 0.5) put(dark, Math.round(x) + 1, y, val * 0.4); }
        }
      }
      for (let k = 0; k < F.styl; k++) {              // stylolites: jagged dark seams
        const y0 = rr(ya + 8, yb - 8), ph = rnd() * 50, amp = rr(2, 5);
        for (let x = 0; x < W; x++) {
          const yy = y0 + (n2((x / 5) + ph, ph, 205, 256) - 0.5) * amp * 2 + (n3(x / 40 + ph, 1.5, 25, 256) - 0.5) * 6;
          put(dark, x, Math.round(yy), 0.75);
        }
      }
      for (let k = 0; k < F.vugs; k++) {              // small vugs
        const cy = rr(ya + 3, yb - 3), r = rr(1.2, 3.6); ellipse(dark, rnd() * W, cy, r * rr(1, 1.8), r, rr(0.5, 0.95));
      }
      for (let k = 0; k < F.nod; k++) {               // sparse small pale anhydrite nodules
        const cy = rr(ya + 3, yb - 3), rx = rr(2.5, 8); ellipse(pale, rnd() * W, cy, rx, rx * rr(0.22, 0.45), rr(0.55, 0.95));
      }
      if (b.id === 'bilara') for (let k = 0; k < 8; k++) {   // thin discontinuous evaporite layers
        const y0 = rr(ya + 6, yb - 6), ph = rnd() * 90;
        for (let x = 0; x < W; x++) {
          const on = smooth01(0.5, 0.62, n2(x / 30 + ph, 3.3, 34, 256)); if (on <= 0) continue;
          const yy = y0 + (n3(x / 60 + ph, 0.7, 17, 256) - 0.5) * 8; put(pale, x, Math.round(yy), 0.7 * on); if (rnd() < 0.6 * on) put(pale, x, Math.round(yy) + 1, 0.4 * on);
        }
      }
    }
    if (F.massive) {                                 // crystalline basement: interlocking fracture sets
      for (let k = 0; k < 22; k++) crackWalk(rnd() * W, rr(ya, yb), (rnd() < 0.6 ? Math.PI / 2 : rnd() * Math.PI) + (rnd() - 0.5) * 0.5, 60 + rnd() * 200, rr(0.35, 0.8), false);
      for (let k = 0; k < 200; k++) ellipse(pale, rnd() * W, rr(ya, yb), rr(1, 3.2), rr(0.8, 2), rr(0.4, 0.9));   // felsic patches
    }
    if (b.id === 'tert' || b.id === 'nagaur' || b.id === 'jodhpur' || b.id === 'sand') {   // occasional hairline joints
      for (let k = 0; k < (b.id === 'sand' ? 0 : 5); k++) crackWalk(rnd() * W, rr(ya, yb - 60), Math.PI / 2 + (rnd() - 0.5) * 0.4, 20 + rnd() * 50, rr(0.25, 0.5), false);
    }
    // bedding-plane partings (dark, thin) between competent beds
    if (!F.massive) for (const q of bedsHere) {
      if (q.b - q.a < 6) continue;
      const pv = (b.id === 'bilara' || b.id === 'carb') ? rr(0.15, 0.7) : b.id === 'tert' ? 0.4 : 0.32;
      if (rnd() < 0.8) for (let x = 0; x < W; x++) { const on = smooth01(0.3, 0.5, n3(x / 70 + q.a, q.a * 0.31, 14, 256)); if (on > 0) put(dark, x, q.a, pv * on * (0.6 + 0.4 * n2(x / 9, q.a * 0.13, 114, 256))); }
    }
  }

  /* ---- render */
  const yLo = new Float32Array(NB), yHi = new Float32Array(NB);
  for (let y = 0; y < H; y++) {
    const rowIdx = Math.min(H - 1, y);
    for (let x = 0; x < W; x++) {
      const u = x / W, i = (y * W + x) * 4, k = y * W + x;
      // which formation at this column, and remap into that formation's nominal rows
      let bi = 0; for (let q = NB - 1; q > 0; q--) if (y >= bands[q].y0 + cw[q][x]) { bi = q; break; }
      const B = bands[bi], F = B.F, pal = B.pal;
      const t0 = B.y0 + (bi === 0 ? 0 : cw[bi][x]), t1 = B.y1 + (bi === NB - 1 ? 0 : cw[bi + 1][x]);
      let yw = B.y0 + (y - t0) * (B.y1 - B.y0) / Math.max(1, t1 - t0);
      let iy = Math.round(yw); iy = iy < 0 ? 0 : iy >= H ? H - 1 : iy;
      if (rowBand[iy] !== bi) { iy = Math.min(H - 1, Math.max(0, iy + (rowBand[iy] < bi ? 1 : -1))); }
      const amp = rowAmp[iy];
      let s = yw;
      s += (fbmT(n3, u * 5 + 1.7, y / 90, 5, PY, 2) - 0.5) * (F.lamR > 0 ? 9 : 0);
      if (amp > 0) { const f = (u * rowKx[iy] + rowPh[iy]) % 1, curve = 1 - (1 - f) * (1 - f); s = yw - amp * (curve - 0.4) + 0; }
      const lam = F.lamC > 0 ? lamAt(s, F.lamF) : 0.5;
      const macro = fbmT(n, u * 3 + 0.37, y / 140, 3, PY, 3);
      const mac2 = fbmT(n3, u * 2 + 9.1, y / 60, 2, PY, 2);
      const fibr = fbmT(n2, u * 36, y / 3.2, 36, PY, 2);
      const grain = rnd();
      const dk = dark[k], pl = pale[k];
      const pos = rowPos[iy], thick = rowThick[iy];
      let tt = 0.5 + (rowTone[iy] - 0.5) * F.bedC + (lam - 0.5) * F.lamC * (0.45 + 1.1 * mac2) + (macro - 0.5) * F.macC + (fibr - 0.5) * F.fib + (grain - 0.5) * F.gr;
      if (B.id === 'malani') tt += (fbmT(n3, u * 30, y / 12, 30, PY, 2) - 0.5) * 0.35;
      tt = tt < 0 ? 0 : tt > 1 ? 1 : tt;
      let r, gg, bb;
      const dA = tt < 0.5 ? pal[2] : pal[0], dB = tt < 0.5 ? pal[0] : pal[1], ft = tt < 0.5 ? tt * 2 : (tt - 0.5) * 2;
      r = dA[0] + (dB[0] - dA[0]) * ft; gg = dA[1] + (dB[1] - dA[1]) * ft; bb = dA[2] + (dB[2] - dA[2]) * ft;
      let ro = F.rough + (lam - 0.5) * 0.06 + (grain - 0.5) * 0.08;
      if (rowBleach[iy] > 0) { const w = rowBleach[iy] * 0.55 * smooth01(0.3, 0.7, macro); r += (pal[3][0] - r) * w; gg += (pal[3][1] - gg) * w; bb += (pal[3][2] - bb) * w; }
      if (rowCoal[iy] > 0) { r *= 0.42; gg *= 0.42; bb *= 0.42; }
      if (B.reservoir) {                             // oil-saturated sand: darker + glossier where saturated
        const sat = smooth01(0.25, 0.75, rowSat[iy] * 0.55 + fbmT(n3, u * 4 + 2, y / 70, 4, PY, 3) * 0.6 - 0.1 + (lam - 0.5) * 0.2);
        const sh = 1 - sat * 0.4; r *= sh; gg *= sh; bb *= sh * 0.96;
        ro = 0.86 - sat * 0.55 + (grain - 0.5) * 0.08;
      }
      if (pl > 0) { const w = pl * 0.8; r += (206 - r) * w; gg += (202 - gg) * w; bb += (188 - bb) * w; ro -= pl * 0.05; }
      if (dk > 0) { const m = 1 - dk * 0.6; r *= m; gg *= m; bb *= m; ro += dk * 0.08; }
      // relief: hard beds stand proud, soft ones recess; bedding-plane recesses; lamina texture
      const edge = F.massive ? 0 : (1 - smooth01(0, 3.5, pos)) * 0.3 + (1 - smooth01(0, 2.5, thick - pos)) * 0.1;
      let h = 0.5 + (rowHard[iy] - 0.5) * F.hard + (lam - 0.5) * F.lamR + (macro - 0.5) * 0.25 + (fibr - 0.5) * 0.08 + (grain - 0.5) * 0.05 - edge - dk * 0.5 + pl * 0.06;
      if (B.id === 'malani') h += (fbmT(n3, u * 30, y / 12, 30, PY, 2) - 0.5) * 0.35;
      const shade = 0.94 + (h - 0.5) * 0.35 - (rowCoal[iy] ? 0 : 0);
      d[i] = Math.min(255, r * shade); d[i + 1] = Math.min(255, gg * shade); d[i + 2] = Math.min(255, bb * shade); d[i + 3] = 255;
      hgt[k] = h;
      const rv = Math.min(1, Math.max(0.15, ro)) * 255;
      rdat[i] = rdat[i + 1] = rdat[i + 2] = rv; rdat[i + 3] = 255;
    }
  }
  g.putImageData(img, 0, 0); rg.putImageData(rimg, 0, 0);
  const map = tex(c, { aniso: 8 }), nm = tex(normalFromHeight(hgt, W, H, 3.4, true, false), { srgb: false }), rm = tex(rough, { srgb: false });
  for (const t of [map, nm, rm]) t.wrapT = THREE.ClampToEdgeWrapping;
  return { map, normalMap: nm, roughnessMap: rm };
}

const hex = (h) => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
const lerp = (a, b, t) => a + (b - a) * t;

/* ------------------------------------------------------------------ misc */

// Soft round sprite for particles (steam, dust, oil droplets).
export function softDot(size = 64) {
  const c = canvas(size, size), g = c.getContext('2d');
  const gr = g.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
  gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.4, 'rgba(255,255,255,0.55)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(0, 0, size, size);
  return tex(c, { repeat: false, srgb: false });
}

// Aluminium-clad pipe insulation: longitudinal seams + band clamps.
export function claddingTexture() {
  const c = canvas(256, 256), g = c.getContext('2d'), rnd = mulberry32(9);
  const gr = g.createLinearGradient(0, 0, 256, 0);
  gr.addColorStop(0, '#9fa4a6'); gr.addColorStop(0.5, '#d7dadb'); gr.addColorStop(1, '#a3a8aa');
  g.fillStyle = gr; g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 400; i++) { g.fillStyle = `rgba(0,0,0,${rnd() * 0.05})`; g.fillRect(rnd() * 256, rnd() * 256, 1 + rnd() * 30, 1); }
  g.fillStyle = 'rgba(40,40,40,0.35)'; g.fillRect(0, 0, 256, 3); g.fillRect(0, 128, 256, 2);
  g.fillStyle = 'rgba(255,255,255,0.5)'; g.fillRect(0, 3, 256, 1);
  return tex(c);
}

// Warning sign (generic text, no branding).
export function signTexture(lines = ['DANGER', 'MOVING PARTS', 'KEEP CLEAR']) {
  const c = canvas(256, 192), g = c.getContext('2d');
  g.fillStyle = '#f4f1ea'; g.fillRect(0, 0, 256, 192);
  g.fillStyle = '#c0261d'; g.fillRect(0, 0, 256, 58);
  g.fillStyle = '#fff'; g.font = 'bold 40px Arial Black, Arial'; g.textAlign = 'center'; g.fillText(lines[0], 128, 44);
  g.fillStyle = '#111'; g.font = 'bold 24px Arial'; g.fillText(lines[1], 128, 104); g.fillText(lines[2], 128, 140);
  g.fillStyle = '#111'; g.font = '14px Arial'; g.fillText('WELL BGW-17 · BAGHEWALA', 128, 176);
  return tex(c, { repeat: false });
}
