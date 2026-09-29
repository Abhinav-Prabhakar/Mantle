// Run: node sim.test.mjs
import assert from 'node:assert/strict';
import { WellSim } from './sim.js';
import { STROKE } from './rig.js';

const isFin = (v) => typeof v === 'number' && Number.isFinite(v);
function checkFinite(o, path = '') {
  if (o === null || o === undefined) return;
  if (typeof o === 'number') return assert.ok(Number.isFinite(o), `non-finite ${path}`);
  if (Array.isArray(o)) return o.forEach((v, i) => checkFinite(v, `${path}[${i}]`));
  if (typeof o === 'object') for (const k of Object.keys(o)) checkFinite(o[k], `${path}.${k}`);
}

// 1. finite over a grid
const sim = new WellSim();
for (const kd of [0.5, 0.62, 0.7]) for (let spm = 2; spm <= 9; spm += 1.75)
  for (let day = 0; day <= 120; day += 6) {
    sim.set({ spm, cycleDay: day, kd });
    for (let i = 0; i < 5; i++) sim.step(0.05);
    const m = sim.metrics();
    checkFinite(m, `metrics(spm=${spm},day=${day},kd=${kd})`);
    checkFinite(sim.state, 'state');
  }
console.log('ok finite grid');

// 2. viscosity monotone in production
sim.set({ spm: 5.4, kd: 0.5 });
let prev = 0;
for (let d = 18; d <= 120; d += 2) { sim.set({ cycleDay: d }); const v = sim.metrics().viscosity; assert.ok(v >= prev, `mu not monotone at ${d}`); prev = v; }

// 3. oil rate decline, spmSafe decline
sim.set({ cycleDay: 20 }); const m20 = sim.metrics();
sim.set({ cycleDay: 110 }); const m110 = sim.metrics();
assert.ok(m20.oilRate > m110.oilRate, 'oil 20 > 110');
assert.ok(m20.spmSafe > m110.spmSafe, 'spmSafe declines');

// 4. float margin decreases with spm
sim.set({ cycleDay: 90 });
let pm = 2;
for (let spm = 2; spm <= 9; spm += 0.5) { sim.set({ spm }); const fm = sim.metrics().floatMargin; assert.ok(fm <= pm + 1e-12); pm = fm; }
sim.set({ spm: 9 }); assert.ok(sim.metrics().floatMargin < 0, 'float negative at 9 SPM late');

// 5. dyno card
for (const [spm, day] of [[5.4, 41], [8, 100], [3, 25], [9, 120]]) {
  sim.set({ spm, cycleDay: day });
  const c = sim.dynoCard(180);
  assert.equal(c.surface.length, 180); assert.equal(c.downhole.length, 180);
  for (const L of [c.surface, c.downhole]) {
    assert.deepEqual(L[0], L[L.length - 1], 'closed loop');
    for (const p of L) assert.ok(p.x >= -1e-9 && p.x <= STROKE.length + 1e-9 && isFin(p.f));
  }
  assert.ok(c.fMax > c.fMin);
  assert.ok(['NORMAL', 'FLUID POUND', 'ROD FLOAT RISK', 'VISCOUS DRAG'].includes(c.cls));
  checkFinite(c);
}
console.log('ok cards');

// 6. phases + stepping
const s2 = new WellSim({ cycleDay: 5 }); assert.equal(s2.state.phase, 'INJECTION');
s2.set({ cycleDay: 16 }); assert.equal(s2.state.phase, 'SOAK');
s2.set({ cycleDay: 30 }); assert.equal(s2.state.phase, 'PRODUCTION');
const s3 = new WellSim({ cycleDay: 5, spm: 6 });
const th0 = s3.theta; for (let i = 0; i < 100; i++) s3.step(0.05);
assert.equal(s3.theta, th0, 'parked in injection');
s3.set({ cycleDay: 30 }); const t1 = s3.theta;
for (let i = 0; i < 100; i++) { s3.step(0.05); const p = s3.state.rodPos; assert.ok(p >= 0 && p <= STROKE.length); }
assert.notEqual(s3.theta, t1, 'advances in production');
// parking back at top
s3.set({ cycleDay: 10 }); for (let i = 0; i < 600; i++) s3.step(0.05);
assert.ok(s3.state.rodPos > STROKE.length - 0.01, 'parked at top: ' + s3.state.rodPos);
assert.equal(s3.state.spmActual, 0);
console.log('ok phases');

// 7. series
const ser = sim.series();
for (const k of Object.keys(ser)) assert.equal(ser[k].length, 121, k);
const prof = sim.profile();
assert.equal(prof.depth.length, 126); checkFinite(prof);
console.log('ok series/profile');

// tables
const fmt = (m) => ({
  phase: m.phase, sandfaceT: m.sandfaceT.toFixed(0), visc: m.viscosity.toFixed(0), rh: m.heatedRadius.toFixed(1),
  oil: m.oilRate.toFixed(1), wc: m.waterCut.toFixed(2), liq: m.liquidRate.toFixed(1), PD: m.pumpDisplacement.toFixed(0),
  fill: m.fillage.toFixed(2), bottleneck: m.bottleneck, pprl: m.pprl.toFixed(1), mprl: m.mprl.toFixed(1),
  floatM: m.floatMargin.toFixed(2), spmSafe: m.spmSafe.toFixed(1), goodman: m.goodman.toFixed(2), torque: m.torquePct.toFixed(2),
  kW: m.motorKw.toFixed(1), kwhBbl: m.kwhPerBbl.toFixed(1), sor: m.sor.toFixed(1), cumOil: m.cumOil.toFixed(0),
  co2: m.co2PerBbl.toFixed(1), water: m.waterPerBbl.toFixed(2), net: m.netPerDay.toFixed(0), level: m.fluidLevel.toFixed(0),
  toCut: m.daysToCutoff, dividend: JSON.stringify({ inr: Math.round(m.couplingDividend.inrPerCycle), oil: +m.couplingDividend.oilPct.toFixed(3) }),
  rec: m.recommendation.title, alerts: m.alerts.map((a) => a.level + ':' + a.text).join(' | '),
});
for (const [spm, day] of [[5.4, 41], [8, 100], [5.4, 20], [5.4, 120], [4, 8], [5.4, 16]]) {
  const s = new WellSim({ spm, cycleDay: day });
  console.log(`\n--- spm ${spm}, day ${day} ---`); for (const [k, v] of Object.entries(fmt(s.metrics()))) console.log('  ' + k.padEnd(11) + v);
}
const S = new WellSim({ spm: 5.4 }).series();
console.log('day  T    mu     oil  spmSafe margin sor');
for (const d of [0, 10, 14, 18, 20, 30, 41, 60, 80, 100, 120]) console.log(d, S.T[d].toFixed(0), S.mu[d].toFixed(0), S.oil[d].toFixed(1), S.spmSafe[d].toFixed(1), S.floatMargin[d].toFixed(2), S.sor[d] && S.sor[d].toFixed(1));
console.log('\nALL TESTS PASSED');
