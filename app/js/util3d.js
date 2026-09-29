// Small geometry/material helpers shared by the scene modules.
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { paintTextures, concreteTextures, hazardTexture, claddingTexture } from './textures.js';

const _up = new THREE.Vector3(0, 1, 0);

// A box-section member between two points (w along local x, h along local z).
export function member(p0, p1, w, h, mat, { round = 0 } = {}) {
  const a = new THREE.Vector3(...p0), b = new THREE.Vector3(...p1);
  const len = a.distanceTo(b);
  const g = round > 0 ? new RoundedBoxGeometry(w, len, h, 2, round) : new THREE.BoxGeometry(w, len, h);
  const m = new THREE.Mesh(g, mat);
  m.position.copy(a).add(b).multiplyScalar(0.5);
  m.quaternion.setFromUnitVectors(_up, b.clone().sub(a).normalize());
  m.castShadow = m.receiveShadow = true;
  return m;
}

// A cylinder between two points.
export function rod(p0, p1, r, mat, seg = 16) {
  const a = new THREE.Vector3(...p0), b = new THREE.Vector3(...p1);
  const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, a.distanceTo(b), seg), mat);
  m.position.copy(a).add(b).multiplyScalar(0.5);
  m.quaternion.setFromUnitVectors(_up, b.clone().sub(a).normalize());
  m.castShadow = m.receiveShadow = true;
  return m;
}

// Angle iron (L section) between two points — reads as real structural steel.
export function angle(p0, p1, s, t, mat, twist = 0) {
  const shape = new THREE.Shape();
  shape.moveTo(0, 0); shape.lineTo(s, 0); shape.lineTo(s, t); shape.lineTo(t, t); shape.lineTo(t, s); shape.lineTo(0, s); shape.closePath();
  const a = new THREE.Vector3(...p0), b = new THREE.Vector3(...p1), len = a.distanceTo(b);
  const g = new THREE.ExtrudeGeometry(shape, { depth: len, bevelEnabled: false });
  g.translate(-s / 2, -s / 2, 0);
  g.rotateZ(twist);
  const m = new THREE.Mesh(g, mat);
  m.position.copy(a);
  m.lookAt(b);
  m.castShadow = m.receiveShadow = true;
  return m;
}

// I-beam profile extruded along +X from x0 to x1 (centred on y=0, z=0).
export function iBeamGeometry(x0, x1, h, bf, tw, tf) {
  const s = new THREE.Shape();
  const hh = h / 2, hb = bf / 2, ht = tw / 2;
  s.moveTo(-hb, -hh); s.lineTo(hb, -hh); s.lineTo(hb, -hh + tf); s.lineTo(ht, -hh + tf); s.lineTo(ht, hh - tf);
  s.lineTo(hb, hh - tf); s.lineTo(hb, hh); s.lineTo(-hb, hh); s.lineTo(-hb, hh - tf); s.lineTo(-ht, hh - tf);
  s.lineTo(-ht, -hh + tf); s.lineTo(-hb, -hh + tf); s.closePath();
  const g = new THREE.ExtrudeGeometry(s, { depth: x1 - x0, bevelEnabled: true, bevelSize: 0.006, bevelThickness: 0.006, bevelSegments: 1 });
  // profile lies in x-y (z = extrude); rotate so extrusion runs along +X, profile in y-z
  g.rotateY(Math.PI / 2);
  g.translate(x0, 0, 0);
  return g;
}

export function box(w, h, d, mat, x = 0, y = 0, z = 0, round = 0) {
  const g = round > 0 ? new RoundedBoxGeometry(w, h, d, 2, round) : new THREE.BoxGeometry(w, h, d);
  const m = new THREE.Mesh(g, mat);
  m.position.set(x, y, z);
  m.castShadow = m.receiveShadow = true;
  return m;
}

export function cylZ(r, len, mat, x = 0, y = 0, z = 0, seg = 24) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, len, seg), mat);
  m.rotation.x = Math.PI / 2;
  m.position.set(x, y, z);
  m.castShadow = m.receiveShadow = true;
  return m;
}
export function cylY(r, len, mat, x = 0, y = 0, z = 0, seg = 24, r2 = r) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r2, len, seg), mat);
  m.position.set(x, y, z);
  m.castShadow = m.receiveShadow = true;
  return m;
}
export function cylX(r, len, mat, x = 0, y = 0, z = 0, seg = 24) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, len, seg), mat);
  m.rotation.z = Math.PI / 2;
  m.position.set(x, y, z);
  m.castShadow = m.receiveShadow = true;
  return m;
}

// Tube along a polyline with rounded (bent) corners.
export function pipe(points, r, mat, bend = 0.35, seg = 12) {
  const path = new THREE.CurvePath();
  const P = points.map((p) => new THREE.Vector3(...p));
  let prev = P[0];
  for (let i = 1; i < P.length; i++) {
    const a = P[i - 1], b = P[i];
    if (i < P.length - 1) {
      const c = P[i + 1];
      const d1 = b.clone().sub(a), d2 = c.clone().sub(b);
      const r1 = Math.min(bend, d1.length() / 2), r2 = Math.min(bend, d2.length() / 2);
      const q1 = b.clone().addScaledVector(d1.normalize(), -r1), q2 = b.clone().addScaledVector(d2.normalize(), r2);
      path.add(new THREE.LineCurve3(prev, q1));
      path.add(new THREE.QuadraticBezierCurve3(q1, b, q2));
      prev = q2;
    } else path.add(new THREE.LineCurve3(prev, b));
  }
  const len = path.getLength();
  const m = new THREE.Mesh(new THREE.TubeGeometry(path, Math.max(8, Math.ceil(len * 3)), r, seg, false), mat);
  m.castShadow = m.receiveShadow = true;
  return m;
}

/* ------------------------------------------------------------------ materials */

let _mats = null;
export function materials() {
  if (_mats) return _mats;
  const paint = paintTextures();
  const conc = concreteTextures();
  const painted = (color, extra = {}) => new THREE.MeshStandardMaterial({
    color, map: paint.map, roughnessMap: paint.roughnessMap, normalMap: paint.normalMap, normalScale: new THREE.Vector2(0.35, 0.35),
    roughness: 0.78, metalness: 0.25, ...extra,
  });
  const clad = claddingTexture();
  clad.repeat.set(1, 1);
  _mats = {
    yellow: painted(0xc9951f),               // faded safety yellow (sun-bleached)
    yellowDark: painted(0xa7781a),
    charcoal: painted(0x2e3033, { roughness: 0.7 }),
    grey: painted(0x6d7479),
    blueGrey: painted(0x46596a),
    motorGreen: painted(0x4d6a5e),
    red: painted(0x9c2b22),
    green: painted(0x2f6b3c),
    white: painted(0xd9d6cc, { metalness: 0.1 }),
    steel: new THREE.MeshStandardMaterial({ color: 0x8e9194, roughness: 0.42, metalness: 0.9, map: paint.map }),
    darkSteel: new THREE.MeshStandardMaterial({ color: 0x3b3d40, roughness: 0.5, metalness: 0.85 }),
    rust: new THREE.MeshStandardMaterial({ color: 0x6e3f22, roughness: 0.9, metalness: 0.3, map: paint.map }),
    chrome: new THREE.MeshStandardMaterial({ color: 0xe4e8ec, roughness: 0.08, metalness: 1.0 }),
    rope: new THREE.MeshStandardMaterial({ color: 0x3a3b3d, roughness: 0.55, metalness: 0.8 }),
    rubber: new THREE.MeshStandardMaterial({ color: 0x151515, roughness: 0.9, metalness: 0 }),
    concrete: new THREE.MeshStandardMaterial({ color: 0xffffff, map: conc.map, normalMap: conc.normalMap, roughness: 0.95, metalness: 0 }),
    hazard: new THREE.MeshStandardMaterial({ map: hazardTexture(), roughness: 0.75, metalness: 0.2 }),
    cladding: new THREE.MeshStandardMaterial({ map: clad, color: 0xffffff, roughness: 0.38, metalness: 0.75 }),
    galv: new THREE.MeshStandardMaterial({ color: 0xa3a8ab, roughness: 0.55, metalness: 0.7, map: paint.map }),
    oil: new THREE.MeshStandardMaterial({ color: 0x0b0704, roughness: 0.12, metalness: 0.05 }),
    glassDark: new THREE.MeshStandardMaterial({ color: 0x121a22, roughness: 0.08, metalness: 0.4 }),
    emissiveWarm: new THREE.MeshStandardMaterial({ color: 0x222222, emissive: 0xffc27a, emissiveIntensity: 0, roughness: 0.4 }),
    emissiveCool: new THREE.MeshStandardMaterial({ color: 0x1a2330, emissive: 0x7fd0ff, emissiveIntensity: 0, roughness: 0.3 }),
    beacon: new THREE.MeshStandardMaterial({ color: 0x551010, emissive: 0xff2a1a, emissiveIntensity: 0, roughness: 0.3 }),
  };
  return _mats;
}
