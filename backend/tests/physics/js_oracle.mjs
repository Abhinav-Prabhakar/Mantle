// Dumps the browser twin's outputs for a fixed set of scenarios so pytest can compare the Python port.
// Usage: node js_oracle.mjs > _oracle.json   (or: node js_oracle.mjs out.json)
import { writeFileSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const appJs = path.resolve(here, '../../../app/js');
const { WellSim, CYCLE, viscosityCp } = await import(pathToFileURL(path.join(appJs, 'sim.js')).href);
const rig = await import(pathToFileURL(path.join(appJs, 'rig.js')).href);

const scenarios = [];
const add = (s) => scenarios.push(s);

// grid: spm x day x kd x steam (deterministic subset, ~50 scenarios)
const days = [0, 5, 13.5, 16, 18, 18.5, 22, 30, 41, 55, 60, 75, 90, 105, 120];
const spms = [2, 5.4, 9];
const kds = [0.5, 0.62, 0.4, 0.7];
const steams = [800, 500, 1100];
let i = 0;
for (const day of days) for (const spm of spms) {
  const kd = kds[i % kds.length], steam = steams[Math.floor(i / 2) % steams.length];
  add({ spm, cycleDay: day, kd, steam, steps: 10 + (i % 4) * 7 });
  i++;
}
// extras: extremes and clamped inputs
add({ spm: 15, cycleDay: 100, kd: 0.7, steam: 1400, steps: 5 });
add({ spm: 0.2, cycleDay: 60, kd: 0.3, steam: 100, steps: 5 });
add({ spm: 7.25, cycleDay: 41.37, kd: 0.5504, steam: 923.6, steps: 3 });
add({ spm: 4, cycleDay: 200, kd: 0.5, steam: 800, steps: 3 });

const round = (v) => v;
const out = { cycle: CYCLE, scenarios: [], sequence: [], unitPose: [], depth: [], viscosity: [], stroke: rig.STROKE };

for (const sc of scenarios) {
  const sim = new WellSim({ spm: sc.spm, cycleDay: sc.cycleDay, kd: sc.kd, steam: sc.steam });
  const st0 = JSON.parse(JSON.stringify(sim.state));
  for (let k = 0; k < sc.steps; k++) sim.step(0.05);
  const m = sim.metrics();
  out.scenarios.push({
    input: sc, state0: st0, state: JSON.parse(JSON.stringify(sim.state)), theta: sim.theta,
    metrics: m, series: sim.series(), profile: sim.profile(), dyno: { n180: sim.dynoCard(180), n12: sim.dynoCard(12) },
  });
}

// stateful sequence on one sim: exercises caches (base/cycle/kd/coupling) and step dynamics
{
  const sim = new WellSim();
  const seq = [
    { spm: 6 }, { cycleDay: 30 }, { kd: 0.62 }, { steam: 950 }, { cycleDay: 10 }, { cycleDay: 45, spm: 3 },
    { spm: 3.0004 }, { cycleDay: 90, spm: 8.5, kd: 0.55 }, { steam: 949.7 }, { cycleDay: 16 }, { cycleDay: 70 },
  ];
  for (const s of seq) {
    sim.set(s);
    for (let k = 0; k < 15; k++) sim.step(0.05);
    out.sequence.push({ set: s, theta: sim.theta, state: JSON.parse(JSON.stringify(sim.state)), metrics: sim.metrics(), series: sim.series() });
  }
}

for (let k = 0; k < 73; k++) {
  const th = (k / 73) * Math.PI * 2 * 1.3 - 0.4;
  out.unitPose.push({ theta: th, pose: rig.unitPose(th), pos: rig.rodPosition(th) });
}
for (const d of [-5, 0, 10, 30, 31, 500, 999, 1000, 1080, 1100, 1160, 1200, 1250, 1300]) {
  const y = rig.depthToY(d);
  out.depth.push({ d, y, back: rig.yToDepth(y) });
}
for (const y of [1, 0, -1, -3.5, -10, -16, -17, -18.5, -22, -26, -28, -29, -35]) out.depth.push({ y, d: rig.yToDepth(y) });
for (const T of [-50, 5, 20, 47, 50, 80, 100, 150, 200, 320, 400, NaN]) out.viscosity.push({ T: Number.isNaN(T) ? null : T, mu: viscosityCp(T) });

const json = JSON.stringify(out);
if (process.argv[2]) writeFileSync(process.argv[2], json); else process.stdout.write(json);
