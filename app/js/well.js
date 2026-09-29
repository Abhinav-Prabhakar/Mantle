// Thermal wellhead + the completion shown in half-section inside the pit slot:
// cement sheath, production casing, vacuum-insulated tubing (VIT), rod string with couplings
// and guides, insert pump (barrel, plunger, travelling + standing valves), perforations,
// annulus fluid with its level, and live oil / steam particles in the reservoir.
import * as THREE from 'three';
import { WELL, UNIT, WELLBORE, depthToY, STRATA, PIT, FACE_Z, STROKE } from './rig.js';
import { materials, box, cylY, cylX, cylZ, pipe, rod } from './util3d.js';
import { softDot, mulberry32 } from './textures.js';

const R = WELLBORE.r;
const resTop = depthToY(STRATA.find((s) => s.reservoir).top), resBot = depthToY(STRATA.find((s) => s.reservoir).bot);

// half cylinder (back half, z <= 0 in local space), open, facing inward or outward
function halfCyl(r, y0, y1, mat, inward = false, seg = 28) {
  const g = new THREE.CylinderGeometry(r, r, y1 - y0, seg, 1, true, Math.PI / 2, Math.PI);
  if (inward) { const idx = g.index.array; for (let i = 0; i < idx.length; i += 3) { const t = idx[i]; idx[i] = idx[i + 2]; idx[i + 2] = t; } const n = g.attributes.normal; for (let i = 0; i < n.count; i++) n.setXYZ(i, -n.getX(i), -n.getY(i), -n.getZ(i)); }
  const m = new THREE.Mesh(g, mat);
  m.position.y = (y0 + y1) / 2;
  m.castShadow = m.receiveShadow = true;
  return m;
}
// flat section strip on the cut plane (z = 0 local), facing +z
function strip(x0, x1, y0, y1, mat, z = 0.001) {
  const m = new THREE.Mesh(new THREE.PlaneGeometry(x1 - x0, y1 - y0), mat);
  m.position.set((x0 + x1) / 2, (y0 + y1) / 2, z);
  m.receiveShadow = true;
  return m;
}

function sectionMaterials() {
  const c = document.createElement('canvas'); c.width = 64; c.height = 256;
  const g = c.getContext('2d');
  // steel section: light with fine 45° hatching (drawing convention, rendered physically)
  g.fillStyle = '#b9bcbf'; g.fillRect(0, 0, 64, 256);
  g.strokeStyle = 'rgba(60,64,70,0.35)'; g.lineWidth = 1;
  for (let i = -256; i < 256; i += 6) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i + 256, 256); g.stroke(); }
  const steelTex = new THREE.CanvasTexture(c); steelTex.wrapS = steelTex.wrapT = THREE.RepeatWrapping; steelTex.repeat.set(1, 20); steelTex.colorSpace = THREE.SRGBColorSpace;
  const c2 = document.createElement('canvas'); c2.width = 128; c2.height = 128;
  const g2 = c2.getContext('2d'), rnd = mulberry32(5);
  g2.fillStyle = '#8f8b84'; g2.fillRect(0, 0, 128, 128);
  for (let i = 0; i < 900; i++) { g2.fillStyle = `rgba(${40 + rnd() * 60},${40 + rnd() * 60},${40 + rnd() * 55},${0.2 + rnd() * 0.4})`; g2.fillRect(rnd() * 128, rnd() * 128, 1 + rnd() * 2, 1 + rnd() * 2); }
  const cemTex = new THREE.CanvasTexture(c2); cemTex.wrapS = cemTex.wrapT = THREE.RepeatWrapping; cemTex.repeat.set(1, 30); cemTex.colorSpace = THREE.SRGBColorSpace;
  return {
    steelCut: new THREE.MeshStandardMaterial({ map: steelTex, roughness: 0.35, metalness: 0.8 }),
    cement: new THREE.MeshStandardMaterial({ map: cemTex, roughness: 0.95, metalness: 0 }),
    casingIn: new THREE.MeshStandardMaterial({ color: 0x5b4a3c, roughness: 0.7, metalness: 0.6 }),
    tubingIn: new THREE.MeshStandardMaterial({ color: 0x4e4e50, roughness: 0.45, metalness: 0.85 }),
    vac: new THREE.MeshStandardMaterial({ color: 0x15171a, roughness: 0.3, metalness: 0.5 }),
  };
}

// Tubing fluid column: dark crude with slow upward-moving streaks while producing, steam going down while injecting.
function fluidColumnMaterial() {
  const u = { uTime: { value: 0 }, uFlow: { value: 0 }, uSteam: { value: 0 }, uMobility: { value: 0.5 }, uNight: { value: 0 } };
  const m = new THREE.ShaderMaterial({
    uniforms: u, transparent: false,
    vertexShader: `varying vec2 vUv; varying vec3 vW; void main(){ vUv=uv; vec4 w=modelMatrix*vec4(position,1.0); vW=w.xyz; gl_Position=projectionMatrix*viewMatrix*w; }`,
    fragmentShader: `
      uniform float uTime,uFlow,uSteam,uMobility,uNight; varying vec2 vUv; varying vec3 vW;
      float h(vec2 p){ return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453); }
      float n(vec2 p){ vec2 i=floor(p),f=fract(p); f=f*f*(3.0-2.0*f); return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y); }
      void main(){
        float y = vW.y;
        float up = n(vec2(vUv.x*6.0, y*1.4 - uTime*uFlow*1.6));
        float streak = smoothstep(0.55, 0.95, n(vec2(vUv.x*18.0, y*0.6 - uTime*uFlow*1.6)));
        vec3 crude = vec3(0.028,0.018,0.01) + vec3(0.12,0.07,0.03) * streak * (0.3+uMobility) + vec3(0.03,0.02,0.01)*up;
        float st = smoothstep(0.35,0.8, n(vec2(vUv.x*5.0, y*0.9 + uTime*3.0)));
        vec3 steam = mix(vec3(0.62,0.66,0.7), vec3(0.95,0.97,1.0), st);
        vec3 c = mix(crude, steam, uSteam);
        // edge darkening (reads as a cylinder in section)
        float e = 1.0 - pow(abs(vUv.x-0.5)*2.0, 3.0)*0.6;
        gl_FragColor = vec4(c*e, 1.0);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }`,
  });
  return { material: m, uniforms: u };
}

export function buildWell(scene) {
  const M = materials(), SM = sectionMaterials();
  const root = new THREE.Group();
  root.name = 'well';
  root.position.set(WELL.x, 0, WELL.z);
  scene.add(root);

  /* ================= surface: thermal wellhead ================= */
  const wh = new THREE.Group(); root.add(wh);
  const flange = (y, r, h, mat) => { wh.add(cylY(r, h, mat, 0, y, 0, 28)); const n = 12; for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2; wh.add(cylY(0.02, h + 0.06, M.darkSteel, Math.cos(a) * (r - 0.05), y, Math.sin(a) * (r - 0.05), 6)); } };
  wh.add(cylY(R.casing + 0.02, 0.5, M.rust, 0, -0.1, 0, 28));                // surface casing stub
  flange(0.2, 0.46, 0.12, M.grey);                                           // casing head
  wh.add(cylY(0.3, 0.3, M.grey, 0, 0.4, 0, 28));
  flange(0.58, 0.42, 0.1, M.grey);                                           // tubing head
  // quilted insulation jacket over the tubing head spool (thermal service)
  const jacket = cylY(0.36, 0.34, new THREE.MeshStandardMaterial({ color: 0xb9b3a4, roughness: 0.95 }), 0, 0.8, 0, 28);
  wh.add(jacket);
  // master gate valve with handwheel
  wh.add(box(0.34, 0.36, 0.3, M.red, 0, 1.15, 0, 0.03));
  wh.add(cylY(0.04, 0.3, M.steel, 0, 1.15, 0.28).rotateX(Math.PI / 2));
  const hwMat = M.red;
  const wheel = new THREE.Mesh(new THREE.TorusGeometry(0.17, 0.018, 8, 28), hwMat); wheel.position.set(0, 1.15, 0.44); wh.add(wheel);
  for (let i = 0; i < 3; i++) { const sp = box(0.3, 0.018, 0.018, hwMat, 0, 1.15, 0.44); sp.rotation.z = i * Math.PI / 3; wh.add(sp); }
  flange(1.36, 0.28, 0.08, M.grey);
  // flow tee with wing outlets (−x: steam injection, +x: production), gauges
  wh.add(cylY(0.2, 0.3, M.grey, 0, 1.55, 0, 24));
  wh.add(cylX(0.13, 1.1, M.grey, 0, 1.55, 0, 20));
  for (const sx of [-1, 1]) {
    wh.add(cylX(0.19, 0.06, M.grey, sx * 0.56, 1.55, 0, 20));
    wh.add(box(0.28, 0.3, 0.3, sx < 0 ? M.red : M.green, sx * 0.78, 1.55, 0, 0.03));   // wing valve
    const w2 = new THREE.Mesh(new THREE.TorusGeometry(0.12, 0.014, 8, 24), sx < 0 ? M.red : M.green); w2.position.set(sx * 0.78, 1.83, 0); w2.rotation.x = Math.PI / 2; wh.add(w2);
    wh.add(cylY(0.025, 0.14, M.steel, sx * 0.78, 1.73, 0));
  }
  // stuffing box + polished-rod BOP
  wh.add(box(0.26, 0.18, 0.4, M.charcoal, 0, 1.8, 0, 0.03));
  wh.add(cylY(0.11, 0.24, M.steel, 0, 1.98, 0, 20));
  wh.add(cylY(0.13, 0.05, M.darkSteel, 0, UNIT.stuffingBoxY - 0.02, 0, 20));
  // pressure gauges (dial faces drawn on canvas)
  const gaugeTex = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d');
    g.fillStyle = '#f2efe6'; g.beginPath(); g.arc(64, 64, 60, 0, Math.PI * 2); g.fill();
    g.strokeStyle = '#222'; g.lineWidth = 3;
    for (let i = 0; i <= 10; i++) { const a = Math.PI * 0.75 + i * Math.PI * 0.15; g.beginPath(); g.moveTo(64 + Math.cos(a) * 44, 64 + Math.sin(a) * 44); g.lineTo(64 + Math.cos(a) * 54, 64 + Math.sin(a) * 54); g.stroke(); }
    g.fillStyle = '#b42318'; g.beginPath(); g.arc(64, 64, 6, 0, Math.PI * 2); g.fill();
    g.save(); g.translate(64, 64); g.rotate(Math.PI * 0.75 + 0.45 * Math.PI * 1.5); g.fillRect(0, -2, 46, 4); g.restore();
    g.fillStyle = '#333'; g.font = 'bold 13px Arial'; g.textAlign = 'center'; g.fillText('bar', 64, 96);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
  })();
  const gauge = (x, y, z, ry) => {
    const gg = new THREE.Group();
    gg.add(cylY(0.018, 0.2, M.steel, 0, -0.12, 0));
    const body = cylZ(0.1, 0.06, M.steel, 0, 0, 0, 24); gg.add(body);
    const face = new THREE.Mesh(new THREE.CircleGeometry(0.088, 24), new THREE.MeshStandardMaterial({ map: gaugeTex, roughness: 0.3 }));
    face.position.z = 0.031; gg.add(face);
    gg.position.set(x, y, z); gg.rotation.y = ry; wh.add(gg);
  };
  gauge(-0.45, 1.84, 0.02, 0);
  gauge(0.44, 0.52, 0.28, 0.4);
  // annulus (casing) valve + temperature transmitter
  wh.add(cylZ(0.07, 0.35, M.grey, 0.0, 0.4, 0.42));
  wh.add(box(0.18, 0.16, 0.14, M.red, 0, 0.4, 0.62, 0.02));
  wh.add(box(0.12, 0.16, 0.1, M.white, 0.26, 1.55, 0.2, 0.02));
  wh.add(cylY(0.008, 0.25, M.darkSteel, 0.28, 1.75, 0.2, 6));

  // steam line (−x) and flowline (+x, then behind the unit) — insulated / bare
  const steamPts = [[-0.92, 1.55, 0], [-1.6, 1.55, 0], [-1.6, 0.62, 0], [-1.6, 0.62, -2.8], [-6, 0.62, -2.8]];
  root.add(pipe(steamPts, 0.14, M.cladding, 0.45));
  const flowPts = [[0.92, 1.55, 0], [1.25, 1.55, 0], [1.25, 1.55, -0.2], [1.25, 0.48, -0.2], [1.25, 0.48, -2.6], [4, 0.48, -2.6]];
  root.add(pipe(flowPts, 0.075, M.grey, 0.3));

  /* ================= subsurface half-section ================= */
  const sub = new THREE.Group(); root.add(sub);
  const yShoe = depthToY(WELLBORE.casingShoe), yTD = -PIT.depth + 0.02;
  // cement sheath (cut faces) and casing wall (cut faces + inner back half)
  for (const s of [-1, 1]) {
    sub.add(strip(s > 0 ? R.casing : -R.hole, s > 0 ? R.hole : -R.casing, yShoe, -0.35, SM.cement));
    sub.add(strip(s > 0 ? R.casingIn : -R.casing, s > 0 ? R.casing : -R.casingIn, yShoe, 0.02, SM.steelCut, 0.002));
  }
  sub.add(halfCyl(R.casingIn, yShoe, 0.02, SM.casingIn, true));
  // casing collars (slightly proud bands every ~1.4 m, fewer in the compressed zone)
  for (let y = -1.2; y > yShoe + 0.3; y -= 1.4) {
    for (const s of [-1, 1]) sub.add(strip(s > 0 ? R.casingIn - 0.012 : -R.casing - 0.03, s > 0 ? R.casing + 0.03 : -R.casingIn + 0.012, y - 0.08, y + 0.08, SM.steelCut, 0.003));
  }
  // open hole below the shoe (rathole)
  // VIT tubing: inner wall, vacuum gap, outer wall in section
  const yTub = depthToY(WELLBORE.tubingBottom);
  for (const s of [-1, 1]) {
    const a = (x0, x1, m, z) => sub.add(strip(s > 0 ? x0 : -x1, s > 0 ? x1 : -x0, yTub, 0.05, m, z));
    a(R.tubingIn, R.tubingIn + 0.014, SM.steelCut, 0.004);
    a(R.tubingIn + 0.014, R.tubing - 0.014, SM.vac, 0.004);
    a(R.tubing - 0.014, R.tubing, SM.steelCut, 0.004);
  }
  // tubing fluid column (section face) + inner back wall
  const fluid = fluidColumnMaterial();
  const fcol = new THREE.Mesh(new THREE.PlaneGeometry(R.tubingIn * 2, yTub * -1 + 0.05, 1, 60), fluid.material);
  fcol.position.set(0, yTub / 2, -0.004);
  sub.add(fcol);
  // annulus: gas above the dynamic fluid level, crude below it (section faces)
  const yFL = depthToY(WELLBORE.fluidLevel);
  const annMat = new THREE.MeshStandardMaterial({ color: 0x0c0806, roughness: 0.15, metalness: 0.1 });
  const annGroup = new THREE.Group(); sub.add(annGroup);
  const annL = strip(-R.casingIn, -R.tubing, yShoe, yFL, annMat, 0.0015), annR = strip(R.tubing, R.casingIn, yShoe, yFL, annMat, 0.0015);
  annGroup.add(annL, annR);
  const meniscus = new THREE.Mesh(new THREE.RingGeometry(R.tubing, R.casingIn, 32, 1, Math.PI, Math.PI), new THREE.MeshStandardMaterial({ color: 0x2a1a0c, roughness: 0.05, metalness: 0.2, emissive: 0x000000 }));
  meniscus.rotation.x = -Math.PI / 2;
  meniscus.position.y = yFL;
  sub.add(meniscus);
  // tubing anchor + seating nipple
  const yAnchor = depthToY(1040);
  sub.add(box(R.tubing * 2 + 0.12, 0.35, 0.02, M.darkSteel, 0, yAnchor, 0.01));
  // insert pump: barrel (x-ray: back half) from pumpTop to pumpBottom, stretched for legibility
  const yPT = depthToY(WELLBORE.pumpTop) + 0.9, yPB = depthToY(WELLBORE.pumpBottom) - 0.3;
  const barrel = halfCyl(R.barrel, yPB, yPT, new THREE.MeshStandardMaterial({ color: 0x9aa0a6, roughness: 0.25, metalness: 0.9 }), true);
  sub.add(barrel);
  for (const s of [-1, 1]) sub.add(strip(s > 0 ? R.barrel - 0.02 : -R.barrel, s > 0 ? R.barrel : -R.barrel + 0.02, yPB, yPT, SM.steelCut, 0.006));
  const sv = new THREE.Mesh(new THREE.SphereGeometry(0.075, 16, 12), M.chrome); sv.position.set(0, yPB + 0.1, 0); sub.add(sv);   // standing valve ball
  sub.add(box(0.26, 0.05, 0.1, M.darkSteel, 0, yPB + 0.02, 0));                                                                   // seat
  sub.add(box(R.barrel * 2 + 0.1, 0.2, 0.04, M.charcoal, 0, yPB - 0.12, 0.01));                                                   // seating nipple / hold-down

  // perforations: shot tunnels through casing + cement into the sand (dark tapered cones, helical)
  const yPt = depthToY(WELLBORE.perfTop), yPb = depthToY(WELLBORE.perfBot);
  const perfGeo = new THREE.ConeGeometry(0.05, 0.9, 8, 1, true); perfGeo.rotateZ(Math.PI / 2); perfGeo.translate(-0.45, 0, 0);
  const perfMat = new THREE.MeshStandardMaterial({ color: 0x0a0604, roughness: 0.3, side: THREE.DoubleSide });
  const perfN = 26, perfs = new THREE.InstancedMesh(perfGeo, perfMat, perfN), pm = new THREE.Matrix4(), pq = new THREE.Quaternion();
  let pi = 0;
  for (let i = 0; i < perfN; i++) {
    const y = yPt + (yPb - yPt) * (i + 0.5) / perfN, a = Math.PI + (i * 2.3) % Math.PI;       // back half only
    pq.setFromAxisAngle(new THREE.Vector3(0, 1, 0), -a);
    pm.compose(new THREE.Vector3(Math.cos(a) * R.casingIn, y, Math.sin(a) * R.casingIn), pq, new THREE.Vector3(1, 1, 1));
    perfs.setMatrixAt(pi++, pm);
  }
  sub.add(perfs);
  // shot tunnels in the cut plane: tapered, oil-filled, staggered left/right
  const tunMat = new THREE.MeshStandardMaterial({ color: 0x0d0805, roughness: 0.18, metalness: 0.1, transparent: true, opacity: 0.85 });
  for (let i = 0; i < 9; i++) {
    const y = yPt + (yPb - yPt) * (i + 0.5) / 9, s = i % 2 ? 1 : -1, len = 0.5 + ((i * 37) % 10) / 20;
    const sh = new THREE.Shape();
    sh.moveTo(s * R.casingIn, y - 0.04); sh.lineTo(s * (R.hole + len), y + 0.005); sh.lineTo(s * R.casingIn, y + 0.04); sh.closePath();
    const m = new THREE.Mesh(new THREE.ShapeGeometry(sh), tunMat); m.position.z = 0.005; sub.add(m);
  }

  /* ---------------- moving rod string (world-aligned group translated by rod position) */
  const rods = new THREE.Group(); sub.add(rods);
  const yTopRod = -0.3, yPlungerTop = yPT - 0.3;          // at bottom of stroke the plunger top sits here
  const taper = [[yTopRod, depthToY(400), 0.05], [depthToY(400), depthToY(800), 0.044], [depthToY(800), depthToY(1020), 0.038], [depthToY(1020), yPlungerTop, 0.062]]; // 1" · 7/8" · 3/4" · sinker bars
  for (const [a, b, r] of taper) rods.add(cylY(r, a - b, r > 0.055 ? M.darkSteel : M.steel, 0, (a + b) / 2, 0, 12));
  const cplGeo = new THREE.CylinderGeometry(0.068, 0.068, 0.12, 14), guideGeo = new THREE.CylinderGeometry(0.1, 0.1, 0.16, 6);
  const cplN = 60, cpls = new THREE.InstancedMesh(cplGeo, M.steel, cplN), guides = new THREE.InstancedMesh(guideGeo, new THREE.MeshStandardMaterial({ color: 0xd8d2c4, roughness: 0.6 }), cplN);
  let ci = 0;
  for (let y = yTopRod - 0.6; y > yPlungerTop + 0.4 && ci < cplN; y -= 0.95, ci++) {
    pm.makeTranslation(0, y, 0); cpls.setMatrixAt(ci, pm);
    pm.makeTranslation(0, y - 0.45, 0); guides.setMatrixAt(ci, pm);
  }
  cpls.count = guides.count = ci;
  cpls.castShadow = guides.castShadow = true;
  rods.add(cpls, guides);
  // plunger + travelling valve
  const plunger = cylY(R.barrel - 0.035, 1.0, M.chrome, 0, yPlungerTop - 0.5, 0, 20);
  rods.add(plunger);
  const tv = new THREE.Mesh(new THREE.SphereGeometry(0.06, 16, 12), M.chrome); tv.position.set(0, yPlungerTop - 1.06, 0); rods.add(tv);
  // fluid charge inside the barrel below the plunger (fillage)
  const charge = new THREE.Mesh(new THREE.PlaneGeometry(R.barrel * 2 - 0.05, 1), annMat);
  charge.position.z = 0.003; sub.add(charge);

  /* ---------------- reservoir particles on the section faces: oil drifting toward the perforations */
  const dot = softDot(64);
  const OILN = 900, rnd = mulberry32(17);
  const oilPos = new Float32Array(OILN * 3), oilSeed = new Float32Array(OILN), oilSize = new Float32Array(OILN);
  const oilState = [];
  const spawn = (i, first) => {
    // pick a face: back wall (z = FACE_Z) or slot sides; radial distance r from the axis
    const side = rnd() < 0.5 ? -1 : 1;
    const r = first ? 0.8 + rnd() * 15 : 9 + rnd() * 7;
    const y = resBot + 0.15 + rnd() * (resTop - resBot - 0.3);
    oilState[i] = { side, r, y, face: rnd() < 0.8 ? 'back' : 'slot' };
    oilSize[i] = 0.6 + rnd() * 1.1; oilSeed[i] = rnd();
  };
  for (let i = 0; i < OILN; i++) spawn(i, true);
  const oilGeo = new THREE.BufferGeometry();
  oilGeo.setAttribute('position', new THREE.BufferAttribute(oilPos, 3));
  oilGeo.setAttribute('aSize', new THREE.BufferAttribute(oilSize, 1));
  oilGeo.setAttribute('aSeed', new THREE.BufferAttribute(oilSeed, 1));
  const oilMat = new THREE.ShaderMaterial({
    uniforms: { uMap: { value: dot }, uPx: { value: 1 }, uTime: { value: 0 }, uLight: { value: 1 } },
    transparent: true, depthWrite: false,
    vertexShader: `attribute float aSize; attribute float aSeed; uniform float uPx; varying float vS;
      void main(){ vS=aSeed; vec4 mv = modelViewMatrix*vec4(position,1.0); gl_Position = projectionMatrix*mv; gl_PointSize = aSize * uPx * 26.0 / -mv.z; }`,
    fragmentShader: `uniform sampler2D uMap; uniform float uLight; varying float vS;
      void main(){ vec4 t = texture2D(uMap, gl_PointCoord); vec2 d = gl_PointCoord-0.5;
        float spec = smoothstep(0.12, 0.0, length(d-vec2(-0.12,-0.14)));
        vec3 c = vec3(0.02,0.012,0.006) + vec3(0.9,0.75,0.55)*spec*0.8*uLight;
        gl_FragColor = vec4(c, t.a*0.92); }`,
  });
  const oilPts = new THREE.Points(oilGeo, oilMat);
  oilPts.frustumCulled = false; oilPts.renderOrder = 3;
  scene.add(oilPts);

  /* ---------------- steam: plume in the tubing going down, bursting out through the perforations */
  const STN = 420;
  const stPos = new Float32Array(STN * 3), stSize = new Float32Array(STN), stAlpha = new Float32Array(STN);
  const stState = Array.from({ length: STN }, () => ({ t: rnd(), a: rnd() * Math.PI * 2, spd: 0.5 + rnd(), y: 0 }));
  const stGeo = new THREE.BufferGeometry();
  stGeo.setAttribute('position', new THREE.BufferAttribute(stPos, 3));
  stGeo.setAttribute('aSize', new THREE.BufferAttribute(stSize, 1));
  stGeo.setAttribute('aAlpha', new THREE.BufferAttribute(stAlpha, 1));
  const stMat = new THREE.ShaderMaterial({
    uniforms: { uMap: { value: dot }, uPx: { value: 1 }, uTint: { value: new THREE.Color(1, 1, 1) } },
    transparent: true, depthWrite: false,
    vertexShader: `attribute float aSize; attribute float aAlpha; uniform float uPx; varying float vA;
      void main(){ vA=aAlpha; vec4 mv = modelViewMatrix*vec4(position,1.0); gl_Position=projectionMatrix*mv; gl_PointSize = aSize*uPx*60.0 / -mv.z; }`,
    fragmentShader: `uniform sampler2D uMap; uniform vec3 uTint; varying float vA;
      void main(){ vec4 t=texture2D(uMap, gl_PointCoord); gl_FragColor = vec4(uTint, t.a*vA*0.55); }`,
  });
  const stPts = new THREE.Points(stGeo, stMat);
  stPts.frustumCulled = false; stPts.renderOrder = 4;
  scene.add(stPts);

  /* ---------------- per-frame update */
  const wx = WELL.x, wz = WELL.z;
  function update({ dt, time, rodPos, fillage = 0.8, phase = 'PRODUCTION', mobility = 0.5, heatedRadius = 9, steamRate = 0, pxRatio = 1, lightLevel = 1 }) {
    // rod string moves rigidly with the polished rod (displacement below top-of-stroke)
    const disp = rodPos - STROKE.length;                  // 0 at top of stroke, −S at bottom
    rods.position.y = disp + STROKE.length;               // modelled at bottom-of-stroke; translate up by rodPos
    rods.position.y = rodPos;
    // barrel charge: fluid below the plunger fills to `fillage` of the swept volume on the upstroke
    const plungerBottom = yPlungerTop - 1.0 + rodPos;
    const chargeTop = Math.min(plungerBottom - 0.02, yPB + 0.15 + (plungerBottom - yPB - 0.15) * fillage);
    charge.position.set(0, (yPB + 0.1 + chargeTop) / 2, 0.003);
    charge.scale.y = Math.max(0.02, chargeTop - yPB - 0.1);
    sv.position.y = yPB + 0.1 + (phase === 'PRODUCTION' ? Math.max(0, Math.sin(time * 6)) * 0.03 : 0);

    const inj = phase === 'INJECTION' ? 1 : 0;
    fluid.uniforms.uTime.value = time;
    fluid.uniforms.uFlow.value = phase === 'PRODUCTION' ? 0.2 + mobility * 0.8 : 0;
    fluid.uniforms.uSteam.value += ((inj ? 1 : 0) - fluid.uniforms.uSteam.value) * Math.min(1, dt * 1.5);
    fluid.uniforms.uMobility.value = mobility;
    annGroup.visible = phase !== 'INJECTION';

    // oil particles: speed ∝ local mobility (hot near the well, sluggish far out)
    oilMat.uniforms.uPx.value = pxRatio; oilMat.uniforms.uLight.value = lightLevel;
    const prod = phase === 'PRODUCTION';
    for (let i = 0; i < OILN; i++) {
      const s = oilState[i];
      const hot = Math.exp(-Math.pow(s.r / Math.max(heatedRadius, 1), 2) * 1.6);
      const v = prod ? (0.03 + 0.9 * hot * mobility) : (phase === 'INJECTION' ? -0.25 * hot : 0.004);
      s.r -= v * dt * (0.7 + oilSeed[i] * 0.6);
      if (s.r < R.hole + 0.1 || s.r > 17) spawn(i, false);
      const px = s.side * s.r;
      if (s.face === 'back') {
        const x = wx + px;
        if (Math.abs(px) < PIT.slot.hw + 0.05 || x < PIT.x0 + 0.3 || x > PIT.x1 - 0.3) { oilPos.set([x, s.y, -99], i * 3); continue; }
        oilPos[i * 3] = x; oilPos[i * 3 + 1] = s.y + Math.sin(time * 0.3 + i) * 0.02; oilPos[i * 3 + 2] = FACE_Z + 0.03;
      } else {
        const rr = Math.min(s.r, Math.abs(wz - FACE_Z) + 0.0);
        oilPos[i * 3] = wx + s.side * (PIT.slot.hw - 0.03); oilPos[i * 3 + 1] = s.y; oilPos[i * 3 + 2] = wz + rr;
        if (s.r > Math.abs(wz - FACE_Z)) oilPos[i * 3 + 2] = -99;
      }
    }
    oilGeo.attributes.position.needsUpdate = true;
    oilPts.visible = phase !== 'INJECTION' || true;

    // steam particles
    stMat.uniforms.uPx.value = pxRatio;
    const on = Math.min(1, steamRate);
    for (let i = 0; i < STN; i++) {
      const s = stState[i];
      s.t += dt * 0.12 * s.spd;
      if (s.t > 1) { s.t -= 1; s.a = rnd() * Math.PI * 2; }
      let x, y, z, size, alpha;
      if (i < STN * 0.45) {           // descending the tubing (section face)
        const yy = 0.2 + (yPB - 0.2) * s.t;
        x = wx + (Math.sin(s.a + s.t * 20) * 0.08); y = yy; z = wz + 0.02; size = 0.35; alpha = on * 0.8;
      } else {                        // pushing out into the sand around the perforations
        const yy = yPt + (yPb - yPt) * ((i * 0.618) % 1);
        const r = R.hole + s.t * heatedRadius * 0.9;
        const face = i % 3 === 0;
        x = wx + Math.cos(s.a) * r * (face ? 1 : 0.2); z = face ? FACE_Z + 0.05 : wz + 0.02; y = yy + Math.sin(s.a * 3 + time) * 0.15;
        if (face && (Math.abs(x - wx) < PIT.slot.hw + 0.1)) x = wx + Math.sign(Math.cos(s.a) || 1) * (PIT.slot.hw + 0.2 + s.t * heatedRadius * 0.8);
        size = 0.6 + s.t * 1.6; alpha = on * (1 - s.t) * 0.7;
      }
      stPos[i * 3] = x; stPos[i * 3 + 1] = y; stPos[i * 3 + 2] = z; stSize[i] = size; stAlpha[i] = alpha;
    }
    stGeo.attributes.position.needsUpdate = true; stGeo.attributes.aSize.needsUpdate = true; stGeo.attributes.aAlpha.needsUpdate = true;
    stPts.visible = on > 0.01;
  }

  root.traverse((o) => { if (o.isMesh) { o.castShadow = o.castShadow ?? true; o.receiveShadow = true; } });
  return { root, update, wellhead: wh, meniscus, fluid };
}
