// The well site as a cut block of Thar ground (a diorama). The top is a muted, compacted desert
// crust; the front face is the geological section through the well (with a slot exposing the
// wellbore in half-section), and the sides and back are cut faces too. Every cut face carries the
// stratigraphic texture and the reservoir temperature field in-shader.
import * as THREE from 'three';
import { BLOCK, PIT, WELL, FACE_Z, WELLBORE, depthToY, STRATA, PIT_DEPTH, KNOTS } from './rig.js';
import { soilTextures, strataTextures, STRATA_TILE_M, mulberry32 } from './textures.js';
import { mergeVertices } from 'three/addons/utils/BufferGeometryUtils.js';

/* ------------------------------------------------------------------ height field */

function valueNoise2(seed) {
  const rnd = mulberry32(seed), N = 512, g = new Float32Array(N * N);
  for (let i = 0; i < g.length; i++) g[i] = rnd();
  const at = (x, y) => g[((y & (N - 1)) * N) + (x & (N - 1))];
  return (x, y) => {
    const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
    const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
    const a = at(xi, yi), b = at(xi + 1, yi), c = at(xi, yi + 1), d = at(xi + 1, yi + 1);
    return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
  };
}
const vn = valueNoise2(1234);
const fbm = (x, y, o = 5) => { let s = 0, a = 0.5, f = 1, n = 0; for (let i = 0; i < o; i++) { s += a * vn(x * f, y * f); n += a; a *= 0.5; f *= 2.03; } return s / n; };
const smoothstep = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };

// Graded, flat ground under the infrastructure; low hummocks and scour hollows elsewhere.
const FLAT = [
  [-8.5, 18, -14.5, 0.5],      // well pad
  [-29, -5, -35, -27],         // steam generator
  [-24, -5, -6, -3],           // steam line corridor
  [-24, -20, -28, -3],
  [9, 24, -24, -2],            // flowline + cabin + VFD
  [7, 31, -38, -23],           // tank battery
]
function flatness(x, z) {
  let f = 0;
  for (const [x0, x1, z0, z1] of FLAT) {
    const d = Math.max(x0 - x, 0, x - x1, z0 - z, 0, z - z1);
    f = Math.max(f, 1 - smoothstep(0, 3.5, d));
  }
  return f;
}
export function groundHeight(x, z) {
  const hum = (fbm(x * 0.07 + 5, z * 0.07, 4) - 0.45) * 0.55 + (fbm(x * 0.3, z * 0.3, 2) - 0.5) * 0.08;
  return hum * (1 - flatness(x, z));
}

/* ------------------------------------------------------------------ build */

export function buildTerrain(scene) {
  const group = new THREE.Group();
  scene.add(group);
  const { x0, x1, z0 } = BLOCK, hw = PIT.slot.hw;

  // top surface: regular grid whose lines fall on the block and slot edges
  const xs = [], zs = [];
  for (let x = x0; x < x1 - 1e-6; x += 0.5) xs.push(+x.toFixed(3));
  xs.push(x1, -hw, hw); 
  for (let z = z0; z < FACE_Z - 1e-6; z += 0.5) zs.push(+z.toFixed(3));
  zs.push(FACE_Z, WELL.z);
  const ux = [...new Set(xs)].sort((a, b) => a - b), uz = [...new Set(zs)].sort((a, b) => a - b);
  const nx = ux.length, nz = uz.length;
  const pos = new Float32Array(nx * nz * 3), uv = new Float32Array(nx * nz * 2), col = new Float32Array(nx * nz * 3);
  for (let j = 0; j < nz; j++) for (let i = 0; i < nx; i++) {
    const k = j * nx + i, x = ux[i], z = uz[j], y = groundHeight(x, z);
    pos[k * 3] = x; pos[k * 3 + 1] = y; pos[k * 3 + 2] = z;
    uv[k * 2] = x / 4; uv[k * 2 + 1] = z / 4;
    // macro variation: paler scoured crust, darker silty hollows, a faint ferruginous cast
    const m = fbm(x * 0.045 + 50, z * 0.045, 4), m2 = fbm(x * 0.012 + 9, z * 0.012, 3);
    const t = 0.94 + (m - 0.5) * 0.2 + (m2 - 0.5) * 0.12 + Math.min(0.06, Math.max(-0.08, y * 0.25));
    col[k * 3] = t * (1 + (m2 - 0.5) * 0.04); col[k * 3 + 1] = t; col[k * 3 + 2] = t * (0.98 - (m2 - 0.5) * 0.04);
  }
  const inSlot = (x, z) => x > -hw && x < hw && z > WELL.z;
  const idx = [];
  for (let j = 0; j < nz - 1; j++) for (let i = 0; i < nx - 1; i++) {
    if (inSlot((ux[i] + ux[i + 1]) / 2, (uz[j] + uz[j + 1]) / 2)) continue;
    const a = j * nx + i, b = a + 1, c = a + nx, d = c + 1;
    idx.push(a, c, b, b, c, d);
  }
  const gg = new THREE.BufferGeometry();
  gg.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  gg.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
  gg.setAttribute('color', new THREE.BufferAttribute(col, 3));
  gg.setIndex(new THREE.Uint32BufferAttribute(idx, 1));
  gg.computeVertexNormals();
  const soil = soilTextures();
  const groundMat = new THREE.MeshStandardMaterial({
    map: soil.map, normalMap: soil.normalMap, roughnessMap: soil.roughnessMap, vertexColors: true,
    normalScale: new THREE.Vector2(1, 1), roughness: 1, metalness: 0, color: 0xffffff,
  });
  const ground = new THREE.Mesh(gg, groundMat);
  ground.receiveShadow = true; ground.castShadow = true;
  ground.name = 'ground';
  group.add(ground);

  const walls = buildCutFaces();
  group.add(walls.mesh);

  return { group, ground, groundMat, wallMat: walls.material, heatUniforms: walls.uniforms };
}

/* ------------------------------------------------------------------ cut faces with the heat field */

function buildCutFaces() {
  const D = PIT_DEPTH, hw = PIT.slot.hw, rh = WELLBORE.r.hole;
  const { x0, x1, z0: zb } = BLOCK;
  const P = [], N = [], U = [];
  const quad = (a, b, c, d, n, ua, ub) => {
    for (const [p, u] of [[a, ua], [b, ub], [c, ub], [a, ua], [c, ub], [d, ua]]) {
      P.push(...p); N.push(...n); U.push(u / STRATA_TILE_M, 1 + Math.min(0, p[1]) / D);
    }
  };
  // vertical cut from (xa,za) to (xb,zb), running left→right as seen from the normal side;
  // the top edge follows the ground, rows split finely so the heat field interpolates smoothly
  const wall = (ax, az, bx, bz, n, u0, rows = 72) => {
    const len = Math.hypot(bx - ax, bz - az), cols = Math.max(1, Math.ceil(len / 0.5));
    for (let c = 0; c < cols; c++) {
      const t0 = c / cols, t1 = (c + 1) / cols;
      const xa = ax + (bx - ax) * t0, za = az + (bz - az) * t0, xb = ax + (bx - ax) * t1, zb_ = az + (bz - az) * t1;
      const ha = groundHeight(xa, za), hb = groundHeight(xb, zb_);
      for (let r = 0; r < rows; r++) {
        const f0 = r / rows, f1 = (r + 1) / rows;
        const yaT = ha + (-D - ha) * f0, yaB = ha + (-D - ha) * f1, ybT = hb + (-D - hb) * f0, ybB = hb + (-D - hb) * f1;
        quad([xa, yaB, za], [xb, ybB, zb_], [xb, ybT, zb_], [xa, yaT, za], n, u0 + len * t0, u0 + len * t1);
      }
    }
  };
  const z0 = FACE_Z, zs = WELL.z;
  wall(x0, z0, -hw, z0, [0, 0, 1], 0);                          // section face, left of the slot
  wall(hw, z0, x1, z0, [0, 0, 1], 60);                          // right of the slot
  wall(-hw, z0, -hw, zs, [1, 0, 0], 0.3);                       // slot sides
  wall(hw, zs, hw, z0, [-1, 0, 0], 4.1);
  wall(-hw, zs, -rh, zs, [0, 0, 1], 7.0);                       // slot back, either side of the borehole
  wall(rh, zs, hw, zs, [0, 0, 1], 9.0);
  wall(x0, zb, x0, z0, [-1, 0, 0], 120, 48);                    // block sides and back
  wall(x1, z0, x1, zb, [1, 0, 0], 160, 48);
  wall(x1, zb, x0, zb, [0, 0, -1], 200, 48);
  // borehole: concave back half-cylinder behind the tubulars
  const seg = 24, rows = 68;
  for (let r = 0; r < rows; r++) {
    const ya = -D * r / rows, yb = -D * (r + 1) / rows;
    for (let s = 0; s < seg; s++) {
      const a0 = Math.PI + (s / seg) * Math.PI, a1 = Math.PI + ((s + 1) / seg) * Math.PI;
      const p0 = [WELL.x + Math.cos(a0) * rh, zs + Math.sin(a0) * rh], p1 = [WELL.x + Math.cos(a1) * rh, zs + Math.sin(a1) * rh];
      const n0 = [-Math.cos(a0), 0, -Math.sin(a0)];
      quad([p0[0], yb, p0[1]], [p1[0], yb, p1[1]], [p1[0], ya, p1[1]], [p0[0], ya, p0[1]], n0, 8 + s * 0.08, 8 + (s + 1) * 0.08);
    }
  }
  // rock relief: displaced along the normal (deterministic in position), kept clean around the
  // well (a true section there) and faded out at the rim, the base and the block's corners
  for (let i = 0; i < P.length; i += 3) {
    const x = P[i], y = P[i + 1], z = P[i + 2], nx = N[i], nz = N[i + 2];
    const s = x * 0.93 + z * 1.07;
    const nearWell = z > WELL.z - rh - 0.01 && Math.abs(x - WELL.x) <= hw + 0.01;
    const clean = nearWell ? 0 : Math.min(1, Math.max(0, Math.abs(x - WELL.x) - 2.4) / 3);
    const corner = Math.min(1, Math.max(0, Math.abs(nx) > 0.5 ? Math.min(z0 - z, z - zb) : Math.min(x - x0, x1 - x)) / 1.2);
    const fade = Math.min(1, Math.max(0, -y) / 0.8) * Math.min(1, (y + D) / 0.8);
    const amp = clean * fade * corner;
    if (amp <= 0) continue;
    const big = fbm(s * 0.22 + 11, y * 0.28, 4) - 0.5, small = fbm(s * 1.3, y * 1.6, 3) - 0.5, ledge = Math.sin(y * 2.1 + fbm(s * 0.1, y * 0.1, 2) * 6) * 0.5;
    const off = (big * 0.8 + small * 0.22 + ledge * 0.1) * amp;
    P[i] += nx * off; P[i + 2] += nz * off;
  }
  let geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(P, 3));
  geo.setAttribute('normal', new THREE.Float32BufferAttribute(N, 3));
  geo.setAttribute('uv', new THREE.Float32BufferAttribute(U, 2));
  geo = mergeVertices(geo, 1e-4);
  geo.computeVertexNormals();

  const st = strataTextures();
  const uniforms = {
    uWell: { value: new THREE.Vector2(WELL.x, WELL.z) },
    uResTop: { value: depthToY(STRATA.find((s) => s.reservoir).top) },
    uResBot: { value: depthToY(STRATA.find((s) => s.reservoir).bot) },
    uTPeak: { value: 180 },        // near-well formation temperature (°C)
    uRh: { value: 9 },             // heated radius (m)
    uThermal: { value: 0 },        // 0 natural · 1 thermal-camera lens
    uNightGlow: { value: 0 },
    uTime: { value: 0 },
    uSteam: { value: 0 },          // injection intensity (0..1)
    uMob: { value: 0.5 },          // oil mobility (0 cold … 1 hot)
    uKnots: { value: KNOTS.map(([d, y]) => new THREE.Vector2(d, y)) },
  };
  const mat = new THREE.MeshStandardMaterial({ map: st.map, normalMap: st.normalMap, roughnessMap: st.roughnessMap, roughness: 1, metalness: 0, normalScale: new THREE.Vector2(1.1, 1.1) });
  mat.onBeforeCompile = (sh) => {
    Object.assign(sh.uniforms, uniforms);
    sh.vertexShader = sh.vertexShader
      .replace('#include <common>', '#include <common>\nvarying vec3 vWp;')
      .replace('#include <worldpos_vertex>', '#include <worldpos_vertex>\nvWp = (modelMatrix * vec4(transformed, 1.0)).xyz;');
    sh.fragmentShader = sh.fragmentShader
      .replace('#include <common>', `#include <common>
varying vec3 vWp;
uniform vec2 uWell; uniform float uResTop, uResBot, uTPeak, uRh, uThermal, uNightGlow, uTime, uSteam, uMob;
float hsh(vec2 p){ return fract(sin(dot(p, vec2(127.1,311.7)))*43758.5453); }
float vn(vec2 p){ vec2 i=floor(p), f=fract(p); vec2 u=f*f*(3.0-2.0*f);
  return mix(mix(hsh(i),hsh(i+vec2(1,0)),u.x), mix(hsh(i+vec2(0,1)),hsh(i+vec2(1,1)),u.x), u.y); }
float fb(vec2 p){ float s=0.0,a=0.5; for(int i=0;i<4;i++){ s+=a*vn(p); p*=2.1; a*=0.5; } return s; }
// true depth from visual y (piecewise, mirrors rig.depthToY)
uniform vec2 uKnots[6];
float trueDepth(float y){
  for (int i=1;i<6;i++){ if (y >= uKnots[i].y) { vec2 a=uKnots[i-1], b=uKnots[i]; return a.x + (y-a.y)/(b.y-a.y)*(b.x-a.x); } }
  return uKnots[5].x; }
// formation temperature: geothermal gradient + CSS heat (diffuse, rock-textured front)
float formationT(vec3 p){
  float geo = 29.0 + 0.0152 * trueDepth(p.y);
  float r = length(p.xz - uWell);
  float mid = 0.5*(uResTop+uResBot), half_ = 0.5*(uResTop-uResBot);
  float dv = max(abs(p.y - mid) - half_, 0.0);
  float vert = exp(-dv*dv / 1.6);                                   // leakage into cap / base rock
  float n = fb(vec2(p.x*0.35 + p.z*0.35, p.y*1.6)) - 0.5;           // heterogeneous sand: fingered front
  float rr = r / max(uRh, 0.5) * (1.0 + n*0.45);
  float prof = exp(-rr*rr*1.6);
  return geo + max(uTPeak - geo, 0.0) * prof * vert;
}
vec3 inferno(float t){ t=clamp(t,0.0,1.0);
  vec3 a=vec3(0.0015,0.0005,0.014), b=vec3(0.34,0.06,0.43), c=vec3(0.73,0.21,0.33), d=vec3(0.98,0.55,0.04), e=vec3(0.99,1.0,0.64);
  return t<0.25?mix(a,b,t/0.25):t<0.5?mix(b,c,(t-0.25)/0.25):t<0.75?mix(c,d,(t-0.5)/0.25):mix(d,e,(t-0.75)/0.25); }
`)
      .replace('#include <map_fragment>', `#include <map_fragment>
float Tf = formationT(vWp);
float heat = clamp((Tf - 47.0) / 160.0, 0.0, 1.0);
// natural look: heated sand darkens & warms (mobilised oil bleeds to the surface), cap rock bakes paler
float inRes = smoothstep(uResBot - 0.6, uResBot + 0.3, vWp.y) * (1.0 - smoothstep(uResTop - 0.3, uResTop + 0.6, vWp.y));
// mobilised crude bleeding out of hot sand: darker, amber-black, wet; a slow film creeps toward the well
float r2 = length(vWp.xz - uWell);
float flowPh = r2 * 1.7 + uTime * (0.15 + uMob * 1.4);
float film = smoothstep(0.35, 0.8, fb(vec2(flowPh, vWp.y * 2.2 + fb(vWp.xy * 0.6) * 2.0)));
float bleed = smoothstep(0.08, 0.55, heat) * inRes;
vec3 oilCol = vec3(0.075, 0.038, 0.016);
diffuseColor.rgb = mix(diffuseColor.rgb, oilCol, bleed * (0.55 + 0.35 * film));
// heated rock warms in tone: a burnt-sienna cast that fades with the thermal front
float warm = smoothstep(0.05, 0.7, heat);
diffuseColor.rgb = mix(diffuseColor.rgb, vec3(0.46, 0.2, 0.07) * (0.7 + 0.5 * film), warm * (0.35 + 0.35 * inRes));
// baked cap rock above the hot zone: slightly paler and drier
diffuseColor.rgb *= 1.0 + smoothstep(0.1, 0.5, heat) * (1.0 - inRes) * 0.12;
vec3 thermCol = inferno(clamp((Tf - 25.0) / 185.0, 0.0, 1.0));
diffuseColor.rgb = mix(diffuseColor.rgb, thermCol * 0.9 + diffuseColor.rgb * 0.08, uThermal);
`)
      .replace('#include <roughnessmap_fragment>', `#include <roughnessmap_fragment>
roughnessFactor = mix(roughnessFactor, 0.14 + (1.0 - film) * 0.2, bleed);`)
      .replace('#include <emissivemap_fragment>', `#include <emissivemap_fragment>
// very faint incandescence only reads at night; the thermal lens is self-lit
totalEmissiveRadiance += vec3(1.0, 0.42, 0.12) * pow(heat, 2.6) * (0.22 + uNightGlow * 0.5) * (1.0 - uThermal);
totalEmissiveRadiance += thermCol * uThermal * 0.55;`);
  };
  mat.customProgramCacheKey = () => 'cutfaces-v2';
  const mesh = new THREE.Mesh(geo, mat);
  mesh.receiveShadow = true;
  mesh.castShadow = true;
  mesh.name = 'cut-faces';
  // underside of the block
  const base = new THREE.Mesh(new THREE.PlaneGeometry(x1 - x0, -zb).rotateX(Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0x2a2522, roughness: 1 }));
  base.position.set((x0 + x1) / 2, -D, zb / 2);
  mesh.add(base);
  return { mesh, material: mat, uniforms };
}
