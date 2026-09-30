// Conventional crank-balanced beam pumping unit, built part by part with pivots at the true
// joints. Motion is procedural: update(theta) solves the four-bar linkage (rig.unitPose) and
// poses the walking beam, horsehead, bridle, carrier bar, polished rod, pitmans and cranks.
import * as THREE from 'three';
import { UNIT, WELL, unitPose } from './rig.js';
import { materials, member, rod, angle, iBeamGeometry, box, cylZ, cylY, cylX } from './util3d.js';
import { signTexture } from './textures.js';

export function buildPumpjack({ simple = false } = {}) {
  const M = materials();
  const root = new THREE.Group();
  root.name = 'pumpjack';
  root.position.set(0, 0, WELL.z);
  const S = UNIT.saddle, K = UNIT.crank;

  /* ---------------- foundation + skid */
  const found = box(10.6, 0.36, 3.1, M.concrete, 6.55, 0.18, 0);
  found.receiveShadow = true;
  root.add(found);
  const { x0, x1, y0, y1 } = UNIT.skid, sh = y1 - y0;
  for (const z of [-0.86, 0.86]) {
    const g = iBeamGeometry(x0, x1, sh, 0.24, 0.02, 0.028);
    const m = new THREE.Mesh(g, M.charcoal); m.position.set(0, (y0 + y1) / 2, z); m.castShadow = m.receiveShadow = true;
    root.add(m);
  }
  for (const x of [x0 + 0.2, 3.6, 5.3, 7.4, 9.1, x1 - 0.2]) root.add(box(0.2, sh * 0.8, 1.72, M.charcoal, x, (y0 + y1) / 2, 0));
  // anchor bolts along the skid flanges
  const boltGeo = new THREE.CylinderGeometry(0.028, 0.028, 0.08, 8);
  const bolts = new THREE.InstancedMesh(boltGeo, M.darkSteel, 24);
  let bi = 0;
  const bm = new THREE.Matrix4();
  for (let i = 0; i < 12; i++) for (const z of [-0.86 - 0.09, 0.86 + 0.09]) { bm.makeTranslation(x0 + 0.4 + i * 0.8, y0 + 0.03, z); bolts.setMatrixAt(bi++, bm); }
  bolts.castShadow = true;
  root.add(bolts);

  /* ---------------- samson post: A-frame, bracing, ladder, platform */
  const topY = S.y - 0.28;
  const legs = [
    [[3.55, y1, 1.02], [5.0, topY, 0.2]], [[3.55, y1, -1.02], [5.0, topY, -0.2]],
    [[7.55, y1, 0.55], [5.45, topY, 0.14]], [[7.55, y1, -0.55], [5.45, topY, -0.14]],
  ];
  for (const [a, b] of legs) root.add(angle(a, b, 0.2, 0.018, M.yellow, Math.PI / 4));
  const legAt = (L, t) => L[0].map((v, i) => v + (L[1][i] - v) * t);
  for (const t of [0.22, 0.5, 0.74]) {
    // horizontal ties and X bracing between the front legs, and front-to-rear ties
    const f0 = legAt(legs[0], t), f1 = legAt(legs[1], t);
    root.add(angle(f0, f1, 0.1, 0.012, M.yellow));
    const r0 = legAt(legs[2], t), r1 = legAt(legs[3], t);
    root.add(angle(r0, r1, 0.09, 0.011, M.yellow));
    root.add(angle(f0, r0, 0.08, 0.01, M.yellow));
    root.add(angle(f1, r1, 0.08, 0.01, M.yellow));
  }
  root.add(angle(legAt(legs[0], 0.22), legAt(legs[1], 0.5), 0.08, 0.01, M.yellow));
  root.add(angle(legAt(legs[1], 0.22), legAt(legs[0], 0.5), 0.08, 0.01, M.yellow));
  root.add(angle(legAt(legs[0], 0.5), legAt(legs[1], 0.74), 0.08, 0.01, M.yellow));
  root.add(angle(legAt(legs[1], 0.5), legAt(legs[0], 0.74), 0.08, 0.01, M.yellow));
  // saddle bearing block on its cap plate
  root.add(box(0.95, 0.12, 0.72, M.yellowDark, S.x, topY + 0.02, 0));
  root.add(box(0.5, 0.26, 0.5, M.charcoal, S.x, S.y - 0.08, 0, 0.04));
  root.add(cylZ(0.13, 0.62, M.steel, S.x, S.y, 0, 20));
  // ladder up the rear leg pair (rails + rungs + safety hoops) and a small platform
  const lz = 0.0;
  const lb = [7.28, y1, lz], lt = [5.75, topY - 0.55, lz];
  for (const dz of [-0.22, 0.22]) root.add(member([lb[0], lb[1], dz], [lt[0], lt[1], dz], 0.04, 0.05, M.yellow));
  const rungs = 16;
  for (let i = 1; i < rungs; i++) {
    const t = i / rungs, p = legAt([lb, lt], t);
    root.add(rod([p[0], p[1], -0.22], [p[0], p[1], 0.22], 0.014, M.galv, 6));
  }
  if (!simple) {
    for (let i = 4; i < rungs; i += 2) {
      const p = legAt([lb, lt], i / rungs);
      const hoop = new THREE.Mesh(new THREE.TorusGeometry(0.42, 0.012, 6, 20, Math.PI * 1.2), M.yellow);
      hoop.position.set(p[0] + 0.3, p[1], 0);
      hoop.rotation.set(Math.PI / 2, 0, -Math.PI * 0.6 + Math.atan2(lt[1] - lb[1], lt[0] - lb[0]) - Math.PI / 2);
      hoop.castShadow = true;
      root.add(hoop);
    }
    const py = topY - 0.52;
    const plat = box(1.25, 0.05, 1.3, M.galv, S.x + 0.55, py, 0);
    root.add(plat);
    for (const [a, b] of [[[S.x - 0.05, py, -0.65], [S.x + 1.15, py, -0.65]], [[S.x - 0.05, py, 0.65], [S.x + 1.15, py, 0.65]]]) {
      root.add(rod([a[0], a[1] + 1.0, a[2]], [b[0], b[1] + 1.0, b[2]], 0.02, M.yellow, 8));
      root.add(rod([a[0], a[1] + 0.5, a[2]], [b[0], b[1] + 0.5, b[2]], 0.015, M.yellow, 8));
      for (const x of [a[0], (a[0] + b[0]) / 2, b[0]]) root.add(rod([x, py, a[2]], [x, py + 1.0, a[2]], 0.02, M.yellow, 8));
    }
  }

  /* ---------------- walking beam group (pivot = saddle) */
  const beam = new THREE.Group();
  beam.position.set(S.x, S.y, 0);
  root.add(beam);
  const BH = 0.6, off = BH / 2 + 0.06;                               // beam sits on the bearing
  const bg = iBeamGeometry(UNIT.beamLen[0], UNIT.beamLen[1], BH, 0.36, 0.022, 0.034);
  const bmesh = new THREE.Mesh(bg, M.yellow); bmesh.position.y = off; bmesh.castShadow = bmesh.receiveShadow = true;
  beam.add(bmesh);
  for (let x = UNIT.beamLen[0] + 0.45; x < UNIT.beamLen[1] - 0.1; x += 0.72) {
    for (const z of [-0.1, 0.1]) beam.add(box(0.018, BH - 0.07, 0.15, M.yellowDark, x, off, z));
  }
  beam.add(box(0.9, 0.08, 0.5, M.yellowDark, 0, 0.1, 0));          // saddle clamp plate
  // tail bearing + equalizer (cross-beam carrying both pitmans) at the rear arm
  const eq = new THREE.Group();
  eq.position.set(UNIT.C, 0, 0);
  beam.add(eq);
  eq.add(box(0.46, 0.22, 0.4, M.charcoal, 0, 0.18, 0, 0.03));
  eq.add(box(0.34, 0.28, 2.12, M.yellow, 0, -0.02, 0, 0.03));
  for (const z of [-0.96, 0.96]) eq.add(cylZ(0.11, 0.24, M.steel, 0, -0.02, z, 16));

  // horsehead: annular sector about the pivot, arc radius A, with side plates, ribs and rope groove
  const A = UNIT.A, dpt = UNIT.horseheadDepth, span = UNIT.horseheadSpan;
  const hs = new THREE.Shape();
  const N = 28;
  for (let i = 0; i <= N; i++) { const a = Math.PI - span + (2 * span * i) / N; const p = [Math.cos(a) * A, Math.sin(a) * A]; i ? hs.lineTo(...p) : hs.moveTo(...p); }
  for (let i = N; i >= 0; i--) { const a = Math.PI - span * 0.82 + (2 * span * 0.82 * i) / N; hs.lineTo(Math.cos(a) * (A - dpt), Math.sin(a) * (A - dpt) * 0.95 + off * 0.4); }
  hs.closePath();
  const hW = 0.62;
  const hg = new THREE.ExtrudeGeometry(hs, { depth: hW, bevelEnabled: true, bevelSize: 0.02, bevelThickness: 0.02, bevelSegments: 2, curveSegments: 24 });
  hg.translate(0, 0, -hW / 2);
  const head = new THREE.Mesh(hg, M.yellow);
  head.castShadow = head.receiveShadow = true;
  beam.add(head);
  // arc face (rope groove) as a darker steel band
  const groove = new THREE.Mesh(new THREE.CylinderGeometry(A + 0.005, A + 0.005, 0.26, 48, 1, true, Math.PI / 2 - span, span * 2), M.darkSteel);
  groove.rotation.x = Math.PI / 2;
  groove.rotation.y = 0;
  groove.castShadow = true;
  const grooveHolder = new THREE.Group(); grooveHolder.add(groove); grooveHolder.rotation.z = Math.PI;   // face −x
  beam.add(grooveHolder);
  for (const t of [0.3, 0.55, 0.8]) {
    const a = Math.PI - span + 2 * span * t;
    beam.add(box(dpt * 0.9, 0.03, hW + 0.05, M.yellowDark, Math.cos(a) * (A - dpt * 0.5), Math.sin(a) * (A - dpt * 0.5), 0));
  }
  // horsehead hinge pin + latch plate to the beam end
  beam.add(cylZ(0.07, hW + 0.24, M.steel, UNIT.beamLen[0] + 0.12, off + 0.18, 0, 12));
  beam.add(box(0.5, 0.5, hW + 0.08, M.yellowDark, UNIT.beamLen[0] + 0.2, off - 0.05, 0));
  // a wrapped rope over the groove to the anchor at the top of the horsehead
  const ropeWrap = new THREE.Group();
  for (const z of [-0.16, 0.16]) {
    const tw = new THREE.Mesh(new THREE.TorusGeometry(A + 0.02, 0.022, 6, 48, span * 1.9), M.rope);
    tw.rotation.z = Math.PI - span * 0.95;
    tw.position.z = z;
    tw.castShadow = true;
    ropeWrap.add(tw);
  }
  beam.add(ropeWrap);

  /* ---------------- bridle, carrier bar, polished rod (world-aligned, updated per frame) */
  const hang = new THREE.Group();
  root.add(hang);
  const ropeGeo = new THREE.CylinderGeometry(0.022, 0.022, 1, 8);
  ropeGeo.translate(0, -0.5, 0);
  const ropes = [-0.16, 0.16].map((z) => { const m = new THREE.Mesh(ropeGeo, M.rope); m.position.z = z; m.castShadow = true; hang.add(m); return m; });
  const carrier = new THREE.Group();
  hang.add(carrier);
  carrier.add(box(0.2, 0.13, 0.6, M.charcoal, 0, 0, 0, 0.02));
  for (const z of [-0.16, 0.16]) carrier.add(box(0.1, 0.18, 0.07, M.steel, 0, 0.08, z));   // rope sockets
  carrier.add(box(0.16, 0.14, 0.16, M.darkSteel, 0, 0.14, 0, 0.02));    // polished-rod clamp
  carrier.add(box(0.12, 0.1, 0.12, M.darkSteel, 0, 0.26, 0, 0.02));     // second clamp (safety)
  const prGeo = new THREE.CylinderGeometry(0.032, 0.032, 1, 16);
  prGeo.translate(0, -0.5, 0);
  const polished = new THREE.Mesh(prGeo, M.chrome);
  polished.castShadow = true;
  hang.add(polished);

  /* ---------------- gear reducer, cranks, counterweights, pitmans */
  const gb = UNIT.gearbox;
  const gbox = box(gb.x1 - gb.x0, gb.y1 - gb.y0 - 0.35, gb.hz * 2, M.blueGrey, (gb.x0 + gb.x1) / 2, gb.y0 + (gb.y1 - gb.y0 - 0.35) / 2, 0, 0.06);
  root.add(gbox);
  const dome = cylZ((gb.x1 - gb.x0) / 2, gb.hz * 2, M.blueGrey, (gb.x0 + gb.x1) / 2, gb.y1 - 0.35, 0, 32);
  dome.scale.set(1, 1, 0.42);
  root.add(dome);
  root.add(box(gb.x1 - gb.x0 + 0.08, 0.06, gb.hz * 2 + 0.1, M.charcoal, (gb.x0 + gb.x1) / 2, gb.y0 + 0.9, 0));   // split-line flange
  for (const z of [-gb.hz - 0.04, gb.hz + 0.04]) {
    root.add(cylZ(0.32, 0.1, M.charcoal, K.x, K.y, z, 24));        // output bearing caps
    root.add(cylZ(0.18, 0.08, M.charcoal, gb.x1 - 0.3, gb.y0 + 0.75, z, 18)); // input bearing
  }
  root.add(cylZ(0.12, UNIT.crankZ * 2 + 0.3, M.steel, K.x, K.y, 0, 16)); // crankshaft
  root.add(cylY(0.05, 0.12, M.glassDark, gb.x0 + 0.25, gb.y0 + 0.55, gb.hz + 0.02, 12)); // oil sight glass (rough)
  root.add(cylY(0.035, 0.18, M.darkSteel, gb.x0 + 0.4, gb.y1 - 0.05, 0.1, 8));        // breather

  const cranks = [];
  for (const side of [-1, 1]) {
    const cg = new THREE.Group();
    cg.position.set(K.x, K.y, side * UNIT.crankZ);
    root.add(cg);
    // crank arm: tapered plate from the pin side (R) through the shaft to the counterweight tail
    const s = new THREE.Shape();
    s.moveTo(UNIT.R + 0.18, 0.13); s.lineTo(UNIT.R + 0.18, -0.13); s.lineTo(0, -0.26); s.lineTo(-1.62, -0.34); s.lineTo(-1.62, 0.34); s.lineTo(0, 0.26); s.closePath();
    const ag = new THREE.ExtrudeGeometry(s, { depth: 0.1, bevelEnabled: true, bevelSize: 0.012, bevelThickness: 0.012, bevelSegments: 1 });
    ag.translate(0, 0, -0.05);
    const arm = new THREE.Mesh(ag, M.charcoal); arm.castShadow = arm.receiveShadow = true;
    cg.add(arm);
    cg.add(cylZ(0.2, 0.2, M.charcoal, 0, 0, 0, 20));                 // hub
    cg.add(cylZ(0.09, 0.34, M.steel, UNIT.R, 0, side * 0.12, 14));  // wrist pin
    // two counterweight blocks per arm, bolted at the tail, with hazard stripes on the rim
    for (const [r, w] of [[-1.05, 0.62], [-1.5, 0.3]]) {
      const cw = box(w, 1.02, 0.24, M.charcoal, r, 0, side * 0.17, 0.04);
      cg.add(cw);
      for (const sy of [-0.42, 0.42]) {
        const stripe = new THREE.Mesh(new THREE.PlaneGeometry(w - 0.06, 0.12), M.hazard);
        stripe.rotation.y = side > 0 ? 0 : Math.PI;
        stripe.position.set(r, sy, side * (0.17 + 0.1225));
        cg.add(stripe);
      }
      for (const by of [-0.3, 0, 0.3]) cg.add(cylZ(0.035, 0.3, M.darkSteel, r + w / 2 - 0.08, by, side * 0.17, 8));
    }
    cranks.push(cg);
  }
  const pitmans = [-0.96, 0.96].map((z) => {
    const g = new THREE.Group();
    root.add(g);
    const pg = new THREE.BoxGeometry(0.16, 1, 0.13); pg.translate(0, 0.5, 0);
    const bar = new THREE.Mesh(pg, M.yellow); bar.castShadow = bar.receiveShadow = true;
    g.add(bar);
    const bearing = cylZ(0.12, 0.2, M.charcoal, 0, 0, 0, 16);
    g.add(bearing);
    g.userData = { bar, z };
    g.position.z = z;
    return g;
  });

  /* ---------------- prime mover: belt guard, motor on slide rails, brake */
  const mo = UNIT.motor;
  root.add(box(1.5, 0.12, 0.9, M.charcoal, mo.x, y1 + 0.06, -0.05));                 // slide base
  for (const z of [-0.35, 0.3]) root.add(box(1.55, 0.06, 0.08, M.steel, mo.x, y1 + 0.15, z));
  const motor = cylZ(mo.r, mo.len, M.motorGreen, mo.x, mo.y, -0.05, 32);
  root.add(motor);
  for (let i = 0; i < 14; i++) {                                                       // cooling fins
    const a = (i / 14) * Math.PI * 2;
    root.add(box(0.03, 0.07, mo.len * 0.86, M.motorGreen, mo.x + Math.cos(a) * (mo.r + 0.02), mo.y + Math.sin(a) * (mo.r + 0.02), -0.05).rotateZ(a));
  }
  root.add(cylZ(mo.r * 0.95, 0.22, M.motorGreen, mo.x, mo.y, -0.05 + mo.len / 2 + 0.1, 32)); // fan cowl
  root.add(box(0.26, 0.22, 0.28, M.motorGreen, mo.x, mo.y + mo.r + 0.1, 0.1, 0.02));        // terminal box
  // belt guard: stadium around the sheaves (gearbox input + motor), perforated
  const gIn = { x: gb.x1 - 0.3, y: gb.y0 + 0.75 }, rA = 0.62, rB = 0.34;
  const gs = new THREE.Shape();
  const ang = Math.atan2(mo.y - gIn.y, mo.x - gIn.x);
  gs.absarc(gIn.x, gIn.y, rA, ang + Math.PI / 2, ang + Math.PI * 1.5, false);
  gs.absarc(mo.x, mo.y, rB, ang - Math.PI / 2, ang + Math.PI / 2, false);
  gs.closePath();
  const gg = new THREE.ExtrudeGeometry(gs, { depth: 0.24, bevelEnabled: true, bevelSize: 0.015, bevelThickness: 0.015, bevelSegments: 2, curveSegments: 32 });
  const guard = new THREE.Mesh(gg, M.yellow);
  guard.position.z = -gb.hz - 0.42; guard.castShadow = guard.receiveShadow = true;
  root.add(guard);
  if (!simple) {
    const sign = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 0.375), new THREE.MeshStandardMaterial({ map: signTexture(), roughness: 0.6 }));
    sign.position.set((gIn.x + mo.x) / 2, (gIn.y + mo.y) / 2 + 0.02, -gb.hz - 0.44);
    sign.rotation.y = Math.PI;
    root.add(sign);
  }
  // brake: drum on the input shaft (other side) + lever stand
  root.add(cylZ(0.3, 0.14, M.charcoal, gIn.x, gIn.y, gb.hz + 0.18, 24));
  root.add(member([mo.x - 0.5, y1, 1.0], [mo.x - 0.65, y1 + 1.35, 1.02], 0.06, 0.06, M.red));
  root.add(box(0.1, 0.24, 0.14, M.darkSteel, mo.x - 0.5, y1 + 0.15, 1.0));
  root.add(rod([mo.x - 0.63, y1 + 1.25, 1.0], [gIn.x + 0.1, gIn.y + 0.2, gb.hz + 0.3], 0.012, M.steel, 6));

  /* ---------------- aviation beacon on the samson post */
  const beacon = new THREE.Mesh(new THREE.SphereGeometry(0.07, 12, 8), M.beacon);
  beacon.position.set(S.x + 0.1, S.y - 0.02, 0.36);
  root.add(beacon);

  const state = { ropes, carrier, polished, beam, cranks, pitmans, beacon };

  // exploded view (inspect mode): the beam lifts off the samson post, the cranks swing out
  let explode = 0;
  const LIFT = 1.7, SPREAD = 1.5;
  function setExplode(v) { explode = v; }

  function update(theta) {
    const p = unitPose(theta);
    const lift = explode * LIFT;
    beam.rotation.z = p.beam;
    beam.position.y = S.y + lift;
    cranks.forEach((c, i) => { c.rotation.z = theta; c.position.z = (i ? 1 : -1) * (UNIT.crankZ + explode * SPREAD); });
    for (const pm of pitmans) {
      const wx = p.crankPin.x, wy = p.crankPin.y, ex = p.equalizer.x, ey = p.equalizer.y - 0.02 + lift;
      const zz = Math.sign(pm.userData.z) * (Math.abs(pm.userData.z) + explode * SPREAD);
      pm.position.set(wx, wy, zz);
      const L = Math.hypot(ex - wx, ey - wy);
      pm.userData.bar.scale.y = L;
      pm.rotation.z = Math.atan2(ey - wy, ex - wx) - Math.PI / 2;
    }
    // rope hangs from the arc's tangent point (x = S.x − A, y = S.y) to the carrier bar
    const topY = S.y + lift, cy = p.carrierY;
    for (const r of ropes) { r.position.set(p.ropeX, topY, r.position.z); r.scale.y = Math.max(0.05, topY - cy - 0.08); }
    carrier.position.set(p.ropeX, cy, 0);
    const prTop = cy + 0.5, prBot = UNIT.stuffingBoxY - 0.35;
    polished.position.set(p.ropeX, prTop, 0);
    polished.scale.y = prTop - prBot;
    return p;
  }
  update(0);
  root.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  return { root, update, state, setExplode, parts: { beam, cranks, pitmans } };
}
