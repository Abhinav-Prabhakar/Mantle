// Shared geometry for the well site: one source of truth for the 3D scene, the
// physics sim and the 2D section drawing. Metres, +X toward the pumping unit's
// motor end, +Y up, +Z toward the viewer (the section face is the plane z = FACE_Z).
//
// The well axis sits WELL.z behind the section face; a slot cut into the face
// exposes the wellbore in half-section. Depth below ground is shown on a
// piecewise scale (true metres -> visual metres) so a 1.25 km well fits a 34 m pit.

export const FACE_Z = 0;
export const WELL = { x: 0, z: -1.6 };

// Conventional crank-balanced beam unit (C-320D-256-120 class), in the x-y plane at z = WELL.z.
export const UNIT = {
  saddle: { x: 5.2, y: 6.4 },   // walking-beam pivot (samson post bearing)
  A: 5.2,                        // front arm: pivot -> horsehead arc (arc radius)
  C: 3.0,                        // rear arm: pivot -> equalizer
  crank: { x: 8.2, y: 2.5 },     // gear-reducer output shaft
  R: 0.86,                       // crank radius (pin circle)
  P: 3.9,                        // pitman length
  bridle: 1.55,                  // wire-rope length from arc tangent to carrier bar
  beamLen: [-4.45, 3.4],          // walking beam extent along its axis (from pivot)
  horseheadDepth: 0.95,          // radial depth of the horsehead
  horseheadSpan: 0.34,           // half angle (rad) of the arc face
  halfWidth: 1.1,                // skid half width (z)
  crankZ: 0.78,                  // crank arms sit at z = well.z ± crankZ
  skid: { x0: 1.6, x1: 11.4, y0: 0.35, y1: 0.75 },
  gearbox: { x0: 7.35, x1: 9.05, y0: 0.75, y1: 2.95, hz: 0.52 },
  motor: { x: 10.25, y: 1.35, r: 0.42, len: 1.15 },
  stuffingBoxY: 2.05,            // top of the wellhead (polished rod enters here)
};

// Crank angle theta (rad) -> linkage pose.
// Beam axis u = (cos b, sin b) points pivot -> equalizer; b > 0 lifts the rear and drops the horsehead.
export function unitPose(theta) {
  const { saddle: S, C, crank: K0, R, P, A } = UNIT;
  const kx = K0.x + R * Math.cos(theta), ky = K0.y + R * Math.sin(theta);
  const f = (b) => Math.hypot(S.x + C * Math.cos(b) - kx, S.y + C * Math.sin(b) - ky) - P;
  // f is monotonic on the working range; bisection is exact and branch-safe.
  let lo = -0.9, hi = 0.9;
  const flo = f(lo);
  for (let i = 0; i < 40; i++) {
    const mid = (lo + hi) / 2, fm = f(mid);
    if ((fm > 0) === (flo > 0)) lo = mid; else hi = mid;
  }
  const b = (lo + hi) / 2;
  const ex = S.x + C * Math.cos(b), ey = S.y + C * Math.sin(b);
  // The wire rope leaves the arc tangentially at x = S.x - A; paying out A·b as the beam turns.
  const ropeTopY = S.y;
  const carrierY = ropeTopY - UNIT.bridle - A * b;
  return { beam: b, crankPin: { x: kx, y: ky }, equalizer: { x: ex, y: ey }, ropeX: S.x - A, carrierY };
}

// Polished-rod travel over one crank revolution (for sims and scales).
export const STROKE = (() => {
  let min = Infinity, max = -Infinity;
  for (let i = 0; i < 720; i++) {
    const y = unitPose((i / 720) * Math.PI * 2).carrierY;
    min = Math.min(min, y); max = Math.max(max, y);
  }
  return { bottomY: min, topY: max, length: max - min };
})();

// Polished-rod position above bottom-of-stroke (0 … STROKE.length) for a crank angle.
export const rodPosition = (theta) => unitPose(theta).carrierY - STROKE.bottomY;

/* ------------------------------------------------------------------ depth scale */

// true depth (m below ground) -> visual y (negative, metres). The reservoir interval is
// shown nearly 1:10 so the heated zone reads; the overburden is compressed ~75:1.
export const KNOTS = [[0, 0], [30, -3.5], [1000, -16], [1080, -18.5], [1160, -26], [1250, -29]];
export const PIT_DEPTH = 29;
export const TRUE_TD = 1250;

export function depthToY(d) {
  for (let i = 1; i < KNOTS.length; i++) {
    if (d <= KNOTS[i][0]) {
      const [d0, y0] = KNOTS[i - 1], [d1, y1] = KNOTS[i];
      return y0 + ((d - d0) / (d1 - d0)) * (y1 - y0);
    }
  }
  return KNOTS[KNOTS.length - 1][1];
}
export function yToDepth(y) {
  for (let i = 1; i < KNOTS.length; i++) {
    if (y >= KNOTS[i][1]) {
      const [d0, y0] = KNOTS[i - 1], [d1, y1] = KNOTS[i];
      return d0 + ((y - y0) / (y1 - y0)) * (d1 - d0);
    }
  }
  return KNOTS[KNOTS.length - 1][0];
}

// Indicative stratigraphy of the Bikaner–Nagaur basin at Baghewala (true depths, m).
export const STRATA = [
  { id: 'sand', name: 'Aeolian sand', age: 'Quaternary', top: 0, bot: 30, color: '#d8b27a', dark: '#b88d56', hatch: 'dots' },
  { id: 'tert', name: 'Clay & siltstone', age: 'Tertiary', top: 30, bot: 260, color: '#a98a6a', dark: '#8a6c50', hatch: 'dash' },
  { id: 'nagaur', name: 'Nagaur sandstone', age: 'Cambrian', top: 260, bot: 620, color: '#b0664a', dark: '#8c4a33', hatch: 'dots' },
  { id: 'bilara', name: 'Bilara dolomite · evaporite', age: 'Cambrian', top: 620, bot: 980, color: '#9ea3a2', dark: '#7a807f', hatch: 'brick' },
  { id: 'carb', name: 'Upper carbonate', age: 'Cambrian', top: 980, bot: 1080, color: '#7d766b', dark: '#5f5850', hatch: 'brick' },
  { id: 'jodhpur', name: 'Jodhpur sandstone · heavy oil', age: 'Neoproterozoic', top: 1080, bot: 1160, color: '#6b4a2e', dark: '#3e2a18', hatch: 'dots', reservoir: true },
  { id: 'malani', name: 'Malani igneous suite', age: 'Basement', top: 1160, bot: 1250, color: '#5a5256', dark: '#3d373a', hatch: 'cross' },
];

// Completion (true depths) and exaggerated visual radii.
export const WELLBORE = {
  casingShoe: 1175,
  tubingBottom: 1092,
  pumpTop: 1068, pumpBottom: 1088,   // insert pump
  perfTop: 1098, perfBot: 1142,
  fluidLevel: 612,                   // dynamic fluid level in the annulus (m)
  r: { hole: 0.62, casing: 0.36, casingIn: 0.31, tubing: 0.17, tubingIn: 0.13, rod: 0.045, coupling: 0.075, barrel: 0.2 },
};

// The site is a cut block of ground (a diorama): its front face is the section plane z = FACE_Z,
// with a slot cut back to the well axis that exposes the wellbore in half-section. The sides and
// back are cut faces too, so the strata read from any angle.
export const BLOCK = { x0: -31, x1: 33, z0: -40, depth: PIT_DEPTH };
export const PIT = { x0: BLOCK.x0, x1: BLOCK.x1, depth: PIT_DEPTH, slot: { hw: 1.25, z0: WELL.z - 1.05 } };

export const SITE = {
  pad: { x0: -4.5, x1: 13.5, z0: -9.5, z1: FACE_Z },   // gravel pad (ends at the section face)
  name: 'BGW-17',
  field: 'Baghewala',
  reservoir: 'Jodhpur Sandstone',
};
