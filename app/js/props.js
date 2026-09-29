// Surface infrastructure and environment around the well pad: gravel pad, pit guardrail,
// insulated steam line from the steam generator, flowline to the tank battery, control cabin,
// VFD cabinet, RTU pole, flood masts, power line, fence, distant pumpjacks and vegetation.
import * as THREE from 'three';
import { WELL, PIT, FACE_Z, UNIT, BLOCK } from './rig.js';
import { materials, box, cylY, cylX, cylZ, pipe, member, rod } from './util3d.js';
import { gravelTextures, mulberry32, softDot, signTexture } from './textures.js';
import { groundHeight } from './terrain.js';
import { buildPumpjack } from './pumpjack.js';
import { buildVegetation } from './vegetation.js';

export function buildProps(scene) {
  const M = materials();
  const g = new THREE.Group(); g.name = 'props'; scene.add(g);
  const rnd = mulberry32(2024);
  const lights = { flood: [], windows: [], hmi: [], led: [], burner: [], beacons: [] };

  /* ---------------- gravel pad (ends at the section face, notched for the well slot) */
  const gr = gravelTextures();
  gr.map.repeat.set(0.35, 0.35); gr.normalMap.repeat.set(0.35, 0.35);
  const pad = new THREE.Shape();
  const px0 = -7.5, px1 = 17, pz0 = -13, pz1 = FACE_Z - 0.02, hw = PIT.slot.hw + 0.02;
  pad.moveTo(px0, -pz1); pad.lineTo(-hw, -pz1); pad.lineTo(-hw, -WELL.z); pad.lineTo(hw, -WELL.z); pad.lineTo(hw, -pz1);
  pad.lineTo(px1, -pz1); pad.lineTo(px1, -pz0); pad.lineTo(px0, -pz0); pad.closePath();
  const padGeo = new THREE.ShapeGeometry(pad);
  padGeo.rotateX(-Math.PI / 2);
  // shape y -> world -z, so we built it with negated z
  const uv = padGeo.attributes.uv, pp = padGeo.attributes.position;
  for (let i = 0; i < uv.count; i++) uv.setXY(i, pp.getX(i) / 3, pp.getZ(i) / 3);
  const padMat = new THREE.MeshStandardMaterial({ map: gr.map, normalMap: gr.normalMap, roughness: 0.96, color: 0xe8ded0 });
  const padMesh = new THREE.Mesh(padGeo, padMat);
  padMesh.position.y = 0.03; padMesh.receiveShadow = true;
  g.add(padMesh);
  // oil staining + tyre-darkened patches (soft decals)
  const stain = (x, z, r, a, col = '20,12,6') => {
    const c = document.createElement('canvas'); c.width = c.height = 128; const cg = c.getContext('2d');
    for (let k = 0; k < 7; k++) {
      const rx = 64 + (rnd() - 0.5) * 50, ry = 64 + (rnd() - 0.5) * 50, rr = 20 + rnd() * 40;
      const gg = cg.createRadialGradient(rx, ry, 0, rx, ry, rr);
      gg.addColorStop(0, `rgba(${col},${a})`); gg.addColorStop(1, `rgba(${col},0)`);
      cg.fillStyle = gg; cg.fillRect(0, 0, 128, 128);
    }
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
    const m = new THREE.Mesh(new THREE.PlaneGeometry(r * 2, r * 2), new THREE.MeshStandardMaterial({ map: t, transparent: true, depthWrite: false, roughness: 0.35, polygonOffset: true, polygonOffsetFactor: -2 }));
    m.rotation.x = -Math.PI / 2; m.position.set(x, 0.045, z); m.receiveShadow = true;
    g.add(m);
  };
  stain(0.9, WELL.z - 1.1, 1.8, 0.75);
  stain(2.8, WELL.z - 0.5, 1.2, 0.5);
  stain(8.2, WELL.z + 0.2, 2.2, 0.35);
  stain(-3, -7, 3.5, 0.25, '70,52,34');
  stain(12, -9, 4, 0.22, '70,52,34');

  // hazard boards at the slot edges
  for (const sx of [-1, 1]) g.add(box(0.06, 0.25, 1.2, M.hazard, sx * (hw + 0.2), 0.2, WELL.z * 0.5));

  /* ---------------- steam line: generator → expansion loop → wellhead (aluminium-clad) */
  const gen = { x: -17, z: -31 };
  const sy = 0.62, sz = WELL.z - 2.8;
  const steamRoute = [[-6, sy, sz], [-12, sy, sz], [-12, sy, sz - 0.01], [-14, sy, sz], [-14, 3.2, sz], [-17, 3.2, sz], [-17, sy, sz], [-22, sy, sz], [-22, sy, gen.z + 3.2], [gen.x + 9.4, sy, gen.z + 3.2], [gen.x + 9.4, 1.8, gen.z + 3.2]];
  g.add(pipe(steamRoute.filter((_, i) => i !== 2), 0.14, M.cladding, 0.55));
  for (let x = -7; x > -22; x -= 3.5) if (x < -12.8 || x > -11.6) g.add(sleeper(x, sz, M));
  for (let z = sz - 3; z > gen.z + 4; z -= 3.5) g.add(sleeper(-22, z, M, true));
  // isolation valve with handwheel near the pad edge
  g.add(box(0.45, 0.42, 0.4, M.red, -8.5, sy, sz, 0.03));
  const hwheel = new THREE.Mesh(new THREE.TorusGeometry(0.26, 0.02, 8, 28), M.red); hwheel.rotation.x = Math.PI / 2; hwheel.position.set(-8.5, sy + 0.62, sz); g.add(hwheel);
  g.add(cylY(0.03, 0.4, M.steel, -8.5, sy + 0.4, sz));

  /* ---------------- steam generator (once-through, gas fired) */
  const sg = new THREE.Group(); sg.position.set(gen.x, 0, gen.z); g.add(sg);
  sg.add(box(21, 0.35, 5.2, M.concrete, 0, 0.17, 0));
  const shell = box(17, 4.2, 4.2, M.white, -0.5, 2.45, 0, 0.12);
  sg.add(shell);
  for (let x = -8.5; x <= 7.5; x += 1.6) sg.add(box(0.05, 4.1, 4.26, M.grey, x, 2.45, 0));   // panel seams
  sg.add(cylX(1.5, 3.2, M.white, 9.6, 2.35, 0, 32));                                          // radiant section end
  sg.add(cylX(1.55, 0.2, M.grey, 11.2, 2.35, 0, 32));
  const burnerWin = cylX(0.2, 0.06, M.emissiveWarm.clone(), 11.32, 2.35, 0, 20);
  lights.burner.push(burnerWin); sg.add(burnerWin);
  const stackX = -7.5;
  sg.add(cylY(0.8, 17, M.grey, stackX, 8.5 + 4.5, 0, 28, 0.95));
  sg.add(cylY(1.05, 0.3, M.charcoal, stackX, 21.2, 0, 28));
  for (const y of [8, 14]) { const r = new THREE.Mesh(new THREE.TorusGeometry(1.05, 0.05, 6, 24), M.yellow); r.rotation.x = Math.PI / 2; r.position.set(stackX, y, 0); sg.add(r); }
  const stackBeacon = new THREE.Mesh(new THREE.SphereGeometry(0.16, 12, 8), M.beacon.clone());
  stackBeacon.position.set(stackX + 0.9, 21.5, 0); sg.add(stackBeacon); lights.beacons.push(stackBeacon);
  sg.add(box(3.5, 2.8, 3, M.blueGrey, 5, 1.75, 4.4, 0.05));      // control shed
  const shedWin = box(1.2, 0.7, 0.05, M.emissiveWarm.clone(), 5, 2.1, 5.92); lights.windows.push(shedWin); sg.add(shedWin);
  for (const [x, z] of [[-3, -4.5], [0.5, -4.5]]) sg.add(cylY(1.1, 4.2, M.white, x, 2.2, z, 24));   // softener vessels
  g.add(pipe([[gen.x - 3, 3.2, gen.z - 4.5], [gen.x - 3, 5.2, gen.z - 4.5], [gen.x - 3, 5.2, gen.z - 1.2], [gen.x - 3, 3.5, gen.z - 1.2]], 0.08, M.galv, 0.3));

  /* ---------------- flowline to the tank battery + heater-treated storage */
  const tb = { x: 19, z: -31 };
  g.add(pipe([[4, 0.48, WELL.z - 2.6], [11, 0.48, WELL.z - 2.6], [11, 0.48, tb.z + 6.5], [tb.x - 3, 0.48, tb.z + 6.5], [tb.x - 3, 1.3, tb.z + 6.5]], 0.075, M.grey, 0.4));
  for (let x = 5; x < 11; x += 3.2) g.add(sleeper(x, WELL.z - 2.6, M, false, 0.35));
  const tbG = new THREE.Group(); tbG.position.set(tb.x, 0, tb.z); g.add(tbG);
  // bund wall
  const bw = 22, bd = 12;
  for (const [x, z, w, d] of [[0, -bd / 2, bw, 0.3], [0, bd / 2, bw, 0.3], [-bw / 2, 0, 0.3, bd], [bw / 2, 0, 0.3, bd]]) tbG.add(box(w, 0.9, d, M.concrete, x, 0.45, z));
  const tankMat = tankMaterial();
  for (const [x, col] of [[-5, tankMat], [4.5, tankMat]]) {
    const tank = cylY(3.6, 7.2, col, x, 3.6, 0, 48);
    tbG.add(tank);
    tbG.add(cylY(3.66, 0.12, M.grey, x, 7.24, 0, 48));
    const roof = new THREE.Mesh(new THREE.ConeGeometry(3.66, 0.7, 48), col); roof.position.set(x, 7.6, 0); roof.castShadow = roof.receiveShadow = true; tbG.add(roof);
    for (let y = 1.2; y < 7; y += 1.2) { const b = new THREE.Mesh(new THREE.TorusGeometry(3.62, 0.025, 4, 64), M.grey); b.rotation.x = Math.PI / 2; b.position.set(x, y, 0); tbG.add(b); }
    // rust streaks: a few thin dark strips down the shell
    tbG.add(cylY(0.12, 1.2, M.grey, x + 1.5, 8.2, 0.5));    // vent
  }
  // walkway between the tanks + stair
  tbG.add(box(1.4, 0.08, 1.2, M.galv, -0.25, 7.4, 0));
  for (let i = 0; i < 16; i++) tbG.add(box(1.0, 0.06, 0.28, M.galv, 8.8, 0.45 * i + 0.3, 3.8 - i * 0.28));
  tbG.add(member([9.3, 0.3, 3.8], [9.3, 7.5, -0.7], 0.05, 0.05, M.yellow));
  tbG.add(member([8.3, 0.3, 3.8], [8.3, 7.5, -0.7], 0.05, 0.05, M.yellow));
  const tbSign = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 1.2), new THREE.MeshStandardMaterial({ map: signTexture(['NO SMOKING', 'FLAMMABLE', 'CRUDE OIL STORAGE']), roughness: 0.7 }));
  tbSign.position.set(0, 0.95, bd / 2 + 0.17); tbG.add(tbSign);

  /* ---------------- control cabin, VFD cabinet, RTU pole */
  const cab = new THREE.Group(); cab.position.set(19.5, 0, -9); cab.rotation.y = -0.12; g.add(cab);
  cab.add(box(6.2, 2.7, 2.6, M.white, 0, 1.55, 0, 0.05));
  cab.add(box(6.3, 0.12, 2.7, M.grey, 0, 2.95, 0));
  for (let x = -2.2; x <= 2.2; x += 2.2) { const w = box(1.1, 0.8, 0.05, M.emissiveWarm.clone(), x, 1.8, 1.31); lights.windows.push(w); cab.add(w); }
  cab.add(box(0.95, 2.0, 0.05, M.blueGrey, 2.8, 1.2, 1.31));
  cab.add(box(1.0, 0.7, 0.55, M.white, -2.4, 2.15, -1.6, 0.04));    // AC unit
  for (let i = 0; i < 3; i++) cab.add(box(1.0, 0.1, 0.35, M.galv, 2.8, 0.1 + i * 0.2, 1.5 + (2 - i) * 0.3));
  g.add(box(0.6, 0.35, 0.6, M.concrete, 19.5, 0.18, -9));

  const vfd = new THREE.Group(); vfd.position.set(12.4, 0, WELL.z - 3.2); g.add(vfd);
  vfd.add(box(1.4, 0.25, 0.9, M.concrete, 0, 0.12, 0));
  vfd.add(box(1.2, 1.9, 0.62, M.grey, 0, 1.2, 0, 0.03));
  const hmi = box(0.34, 0.24, 0.02, M.emissiveCool.clone(), -0.25, 1.55, 0.32); lights.hmi.push(hmi); vfd.add(hmi);
  const vfdLed = new THREE.Mesh(new THREE.SphereGeometry(0.025, 8, 6), new THREE.MeshStandardMaterial({ color: 0x113311, emissive: 0x44ff66, emissiveIntensity: 2 }));
  vfdLed.position.set(0.3, 1.7, 0.32); vfd.add(vfdLed); lights.led.push(vfdLed);
  vfd.add(box(1.8, 0.06, 1.3, M.galv, 0, 2.55, 0.1));              // sunshade
  for (const x of [-0.8, 0.8]) vfd.add(cylY(0.03, 2.4, M.galv, x, 1.3, 0.6));
  g.add(pipe([[12.4 - 0.4, 0.25, WELL.z - 2.9], [12.4 - 0.4, 0.1, WELL.z - 1.6], [UNIT.motor.x + 0.3, 0.8, WELL.z - 0.4]], 0.035, M.rubber, 0.3));

  const rtu = new THREE.Group(); rtu.position.set(-4, 0, -7.5); g.add(rtu);
  rtu.add(cylY(0.07, 5.2, M.galv, 0, 2.6, 0, 12));
  rtu.add(box(0.55, 0.7, 0.3, M.white, 0, 1.6, 0.22, 0.02));
  const rtuLed = new THREE.Mesh(new THREE.SphereGeometry(0.03, 8, 6), new THREE.MeshStandardMaterial({ color: 0x113311, emissive: 0x44ff66, emissiveIntensity: 2 }));
  rtuLed.position.set(0.18, 1.85, 0.38); rtu.add(rtuLed); lights.led.push(rtuLed);
  const panel = box(1.1, 0.04, 0.75, new THREE.MeshStandardMaterial({ color: 0x1c2a44, roughness: 0.15, metalness: 0.6 }), 0, 4.3, 0.25);
  panel.rotation.x = 0.45; rtu.add(panel);
  rtu.add(cylY(0.012, 1.4, M.galv, 0.15, 5.9, 0, 6));

  /* ---------------- flood masts (spot lights at night) */
  for (const [x, z, tx] of [[-6.5, -11.5, 1], [16, -11.8, 5]]) {
    const mast = new THREE.Group(); mast.position.set(x, 0, z); g.add(mast);
    mast.add(cylY(0.13, 10, M.galv, 0, 5, 0, 12, 0.18));
    mast.add(box(1.4, 0.08, 0.2, M.galv, 0, 9.8, 0));
    for (const dx of [-0.5, 0.5]) {
      const head = box(0.45, 0.28, 0.2, M.darkSteel, dx, 9.55, 0.15, 0.03);
      head.lookAt(new THREE.Vector3(tx - x, -9, WELL.z - z).add(new THREE.Vector3(dx, 9.55, 0.15)));
      mast.add(head);
      const lens = box(0.38, 0.2, 0.02, M.emissiveWarm.clone(), 0, 0, 0.11); head.add(lens); lights.windows.push(lens);
    }
    const spot = new THREE.SpotLight(0xffc98a, 0, 60, 0.62, 0.55, 1.6);
    spot.position.set(x, 9.6, z); spot.target.position.set(tx, 0, WELL.z);
    spot.castShadow = lights.flood.length === 0;
    if (spot.castShadow) { spot.shadow.mapSize.set(1024, 1024); spot.shadow.bias = -0.0004; }
    g.add(spot, spot.target); lights.flood.push(spot);
  }
  // a warm work light down into the section (so the cut reads at night)
  const pitLight = new THREE.SpotLight(0xffd7a8, 0, 120, 0.72, 0.9, 1.1);
  pitLight.position.set(6, 14, 62); pitLight.target.position.set(0, -14, 0);
  g.add(pitLight, pitLight.target); lights.flood.push(pitLight);

  /* ---------------- power line along the back of the site */
  const poleZ = BLOCK.z0 + 2;
  const polePts = [];
  for (let x = BLOCK.x0 + 3; x <= BLOCK.x1 - 2; x += 44) {
    const y0 = groundHeight(x, poleZ);
    g.add(cylY(0.16, 11, new THREE.MeshStandardMaterial({ color: 0x8d8475, roughness: 0.9 }), x, y0 + 5.5, poleZ, 10, 0.22));
    g.add(box(2.6, 0.14, 0.14, M.galv, x, y0 + 10.4, poleZ));
    polePts.push([x, y0 + 10.5, poleZ]);
  }
  const wireMat = new THREE.LineBasicMaterial({ color: 0x1a1a1a, transparent: true, opacity: 0.8 });
  for (const off of [-1.1, 0, 1.1]) {
    const pts = [];
    for (let i = 1; i < polePts.length; i++) {
      const a = polePts[i - 1], b = polePts[i];
      for (let k = 0; k <= 16; k++) { const t = k / 16; pts.push(new THREE.Vector3(a[0] + (b[0] - a[0]) * t + off, a[1] + (b[1] - a[1]) * t - Math.sin(Math.PI * t) * 1.3, a[2])); }
    }
    g.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), wireMat));
  }

  /* ---------------- chain-link fence around the back and sides of the pad */
  const fenceTex = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 64; const cg = c.getContext('2d');
    cg.strokeStyle = 'rgba(170,175,178,1)'; cg.lineWidth = 2.4;
    cg.beginPath(); cg.moveTo(0, 0); cg.lineTo(64, 64); cg.moveTo(64, 0); cg.lineTo(0, 64); cg.stroke();
    const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; return t;
  })();
  const fenceMat = new THREE.MeshStandardMaterial({ map: fenceTex, alphaTest: 0.4, transparent: false, side: THREE.DoubleSide, metalness: 0.6, roughness: 0.5 });
  const fence = [[-9, -0.6], [-9, -15.5], [24, -15.5], [24, -0.6]];
  for (let i = 1; i < fence.length; i++) {
    const [ax, az] = fence[i - 1], [bx, bz] = fence[i];
    const len = Math.hypot(bx - ax, bz - az);
    const t = fenceTex.clone(); t.repeat.set(len * 4, 8); t.needsUpdate = true;
    const mesh = new THREE.Mesh(new THREE.PlaneGeometry(len, 2), new THREE.MeshStandardMaterial({ map: t, alphaMap: t, alphaTest: 0.35, side: THREE.DoubleSide, metalness: 0.5, roughness: 0.55, color: 0xb9bdc0 }));
    mesh.position.set((ax + bx) / 2, 1.05, (az + bz) / 2);
    mesh.rotation.y = -Math.atan2(bz - az, bx - ax);
    mesh.castShadow = true;
    g.add(mesh);
    const n = Math.ceil(len / 3);
    for (let k = 0; k <= n; k++) { const x = ax + (bx - ax) * k / n, z = az + (bz - az) * k / n; g.add(cylY(0.04, 2.2, M.galv, x, 1.1, z, 8)); }
    g.add(rod([ax, 2.1, az], [bx, 2.1, bz], 0.022, M.galv, 6));
  }

  const far = [];

  /* ---------------- vegetation: khejri trees and dry shrubs, plus scattered stones */
  const inBlock = (x, z) => x > BLOCK.x0 + 0.8 && x < BLOCK.x1 - 0.8 && z > BLOCK.z0 + 0.8 && z < FACE_Z - 0.8;
  const avoid = (x, z) => !inBlock(x, z) || (x > -10 && x < 25 && z > -16) || (x > gen.x - 14 && x < gen.x + 14 && z > gen.z - 8 && z < gen.z + 8) || (x > tb.x - 13 && x < tb.x + 13 && z > tb.z - 8 && z < tb.z + 8);
  buildVegetation(g, avoid);
  const q = new THREE.Quaternion(), sc = new THREE.Vector3(), ps = new THREE.Vector3();
  const stoneGeo = new THREE.DodecahedronGeometry(1, 0);
  const NR = 260, stones = new THREE.InstancedMesh(stoneGeo, new THREE.MeshStandardMaterial({ color: 0x8a7760, roughness: 0.9, flatShading: true }), NR);
  for (let i = 0; i < NR; i++) {
    let x, z; do { x = BLOCK.x0 + rnd() * (BLOCK.x1 - BLOCK.x0); z = BLOCK.z0 + rnd() * -BLOCK.z0; } while (avoid(x, z));
    const s = 0.04 + rnd() * rnd() * 0.22;
    q.setFromEuler(new THREE.Euler(rnd() * 6, rnd() * 6, rnd() * 6));
    stones.setMatrixAt(i, new THREE.Matrix4().compose(ps.set(x, groundHeight(x, z) + s * 0.2, z), q, sc.set(s, s * 0.6, s * 1.2)));
  }
  stones.castShadow = true; stones.receiveShadow = true; g.add(stones);

  /* ---------------- steam generator exhaust + drifting dust */
  const dot = softDot(64);
  const plumeN = 90, plumePos = new Float32Array(plumeN * 3), plumeA = new Float32Array(plumeN), plumeS = new Float32Array(plumeN);
  const plume = Array.from({ length: plumeN }, () => ({ t: rnd(), a: rnd() * 6.28 }));
  const plumeGeo = new THREE.BufferGeometry();
  plumeGeo.setAttribute('position', new THREE.BufferAttribute(plumePos, 3));
  plumeGeo.setAttribute('aAlpha', new THREE.BufferAttribute(plumeA, 1));
  plumeGeo.setAttribute('aSize', new THREE.BufferAttribute(plumeS, 1));
  const plumeMat = new THREE.ShaderMaterial({
    uniforms: { uMap: { value: dot }, uPx: { value: 1 }, uCol: { value: new THREE.Color(1, 1, 1) } }, transparent: true, depthWrite: false,
    vertexShader: `attribute float aAlpha; attribute float aSize; uniform float uPx; varying float vA; void main(){ vA=aAlpha; vec4 mv=modelViewMatrix*vec4(position,1.0); gl_Position=projectionMatrix*mv; gl_PointSize=aSize*uPx*300.0/-mv.z; }`,
    fragmentShader: `uniform sampler2D uMap; uniform vec3 uCol; varying float vA; void main(){ vec4 t=texture2D(uMap,gl_PointCoord); gl_FragColor=vec4(uCol, t.a*vA); }`,
  });
  const plumePts = new THREE.Points(plumeGeo, plumeMat); plumePts.frustumCulled = false; g.add(plumePts);

  /* ---------------- update */
  function update({ dt, time, env, steamOn = 1, pxRatio = 1 }) {
    const L = env.lightsOn;
    for (const s of lights.flood) s.intensity = L * (s.castShadow ? 900 : 700);
    lights.flood[lights.flood.length - 1].intensity = L * 420;
    for (const w of lights.windows) w.material.emissiveIntensity = 0.15 + L * 2.2;
    for (const h of lights.hmi) h.material.emissiveIntensity = 0.6 + L * 1.4;
    for (const b of lights.burner) b.material.emissiveIntensity = 1.2 + L * 3;
    const blink = (Math.sin(time * 3.4) > 0.6 ? 1 : 0.05);
    for (const b of lights.beacons) b.material.emissiveIntensity = blink * (1 + L * 5);
    for (const l of lights.led) l.material.emissiveIntensity = 1 + (Math.sin(time * 5 + l.id) > 0 ? 2 : 0);
    for (const f of far) f.pj.update(time * (2 * Math.PI * f.spm / 60) + f.ph);
    // exhaust plume rises and drifts downwind (+x, +z), fading
    plumeMat.uniforms.uPx.value = pxRatio;
    const warm = env.night > 0.5 ? 0.5 : 1;
    plumeMat.uniforms.uCol.value.setRGB(0.95 * warm, 0.94 * warm, 0.92 * warm);
    for (let i = 0; i < plumeN; i++) {
      const p = plume[i];
      p.t += dt * 0.06;
      if (p.t > 1) { p.t -= 1; p.a = rnd() * 6.28; }
      const t = p.t;
      plumePos[i * 3] = gen.x + stackX + t * 14 + Math.sin(p.a + time * 0.3) * t * 2;
      plumePos[i * 3 + 1] = 21.8 + t * 9 + Math.sin(p.a) * 0.4;
      plumePos[i * 3 + 2] = gen.z + t * 6 + Math.cos(p.a) * t * 2;
      plumeA[i] = (1 - t) * Math.min(1, t * 8) * 0.22 * steamOn;
      plumeS[i] = 0.6 + t * 3.5;
    }
    plumeGeo.attributes.position.needsUpdate = true; plumeGeo.attributes.aAlpha.needsUpdate = true; plumeGeo.attributes.aSize.needsUpdate = true;
  }

  g.traverse((o) => { if (o.isMesh && !o.material.transparent) { o.castShadow = o.castShadow || false; o.receiveShadow = true; } });
  return { group: g, update, lights };
}

function sleeper(x, z, M, alongZ = false, h = 0.55) {
  const s = new THREE.Group();
  s.add(box(alongZ ? 0.9 : 0.25, 0.1, alongZ ? 0.25 : 0.9, M.concrete, x, 0.05, z));
  s.add(box(alongZ ? 0.6 : 0.12, h - 0.14, alongZ ? 0.12 : 0.6, M.galv, x, (h - 0.14) / 2 + 0.1, z));
  s.add(box(alongZ ? 0.9 : 0.14, 0.06, alongZ ? 0.14 : 0.9, M.galv, x, h - 0.1, z));
  return s;
}

// Weathered storage-tank shell: vertical weld seams, ring seams, dust at the base, rust weeps.
function tankMaterial() {
  const W = 1024, H = 512, c = document.createElement('canvas'); c.width = W; c.height = H;
  const g = c.getContext('2d'), rnd = mulberry32(61);
  g.fillStyle = '#dcd9d0'; g.fillRect(0, 0, W, H);
  for (let i = 0; i < 3000; i++) { g.fillStyle = `rgba(${120 + rnd() * 60},${110 + rnd() * 50},${90 + rnd() * 40},${rnd() * 0.05})`; g.fillRect(rnd() * W, rnd() * H, 4 + rnd() * 40, 2 + rnd() * 20); }
  const dust = g.createLinearGradient(0, H * 0.55, 0, H);
  dust.addColorStop(0, 'rgba(180,150,110,0)'); dust.addColorStop(1, 'rgba(170,135,95,0.55)');
  g.fillStyle = dust; g.fillRect(0, 0, W, H);
  g.strokeStyle = 'rgba(90,85,78,0.35)'; g.lineWidth = 2;
  for (let y = H / 6; y < H; y += H / 6) { g.beginPath(); g.moveTo(0, y); g.lineTo(W, y); g.stroke(); }
  for (let r = 0; r < 6; r++) for (let x = (r % 2) * 64; x < W; x += 128) { g.beginPath(); g.moveTo(x, r * H / 6); g.lineTo(x, (r + 1) * H / 6); g.stroke(); }
  for (let k = 0; k < 26; k++) {
    const x = rnd() * W, y0 = rnd() * H * 0.6, len = 30 + rnd() * 160;
    const gr = g.createLinearGradient(0, y0, 0, y0 + len);
    gr.addColorStop(0, 'rgba(110,60,25,0.55)'); gr.addColorStop(1, 'rgba(110,60,25,0)');
    g.fillStyle = gr; g.fillRect(x, y0, 2 + rnd() * 4, len);
  }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  return new THREE.MeshStandardMaterial({ map: t, roughness: 0.62, metalness: 0.35 });
}
