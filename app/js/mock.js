// MOCK LAYER — every value here is a stand-in until the field data / optimiser services are wired.
// Values are derived from the live WellSim state where that makes them move plausibly; the rest are
// fixed, clearly-fake fixtures. Replace `derive()` field by field when the real feeds land.
import { CYCLE, viscosityCp } from './sim.js';

const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

export const FLUID = { api: '17–19', asphaltene: 9.2, tRes: 47, pRes: 3.1, deadOilCp: Math.round(viscosityCp(47) / 100) * 100 };

export const ROD = {
  count: 140, lengthM: 7.62,
  tapers: [{ label: '1″', to: 400 }, { label: '⅞″', to: 800 }, { label: '¾″', to: 1020 }, { label: 'sinker', to: 1068 }],
  failures: [
    { rod: 57, depth: 432, size: '⅞″', mode: 'pin break at coupling', date: '14 Mar 2026', cause: 'rod float → compressive buckling' },
    { rod: 103, depth: 781, size: '¾″', mode: 'body break', date: '2 Aug 2026', cause: 'corrosion-fatigue, high Goodman' },
  ],
  mtbfDays: 142, mtbfMantle: 260,
};

// last 12 months of pump unseat events (index 0 = oldest)
export const UNSEATS = { months: ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'], events: [2, 5, 9], holdDownKn: 18 };

export const PAST_CYCLES = [{ n: 1, k: 1.26 }, { n: 2, k: 1.13 }, { n: 3, k: 1.03 }];

export const PLAN = {
  practice: { steam: 800, pInj: 9.0, soak: 4, cutoff: 120 },
  mantle: { steam: 920, pInj: 9.8, soak: 6, cutoff: 0 },          // cutoff filled from the sim
  ranges: { steam: [500, 1200], pInj: [7, 12], soak: [2, 10], cutoff: [40, 120] },
  oilLift: 0.084, sor: [3.6, 3.1], inrPerCycle: 420000, jointShare: 160000,
};

export const COST = { maintPerDay: 6500, chemPerDay: 1800, steamPerT: 2800, kwh: 8 };

export function derive(m, st) {
  const prod = m.phase === 'PRODUCTION';
  const spm = st?.spmActual ?? m.spm;
  const hz = spm * 50 / 9;
  const ampsAvg = prod ? (m.motorKw * 1000) / (1.732 * 415 * 0.86) : 0;
  const loadFrac = m.pprl > 0 ? clamp((st?.load ?? m.pprl) / m.pprl, 0, 1.2) : 0;
  const amps = prod ? ampsAvg * (0.55 + 0.9 * loadFrac) : 0;
  // VFD speed profile across one stroke (kd shapes the downstroke slower)
  const profile = Array.from({ length: 36 }, (_, i) => { const th = (i / 35) * Math.PI * 2; return 1 + (m.kd - 0.5) * 0.9 * Math.cos(th) + 0.05 * Math.sin(2 * th); });

  const thp = prod ? 0.55 + m.oilRate * 0.004 : m.phase === 'INJECTION' ? 9.4 : 2.8;
  const chp = prod ? 0.28 : m.phase === 'INJECTION' ? 0.4 : 1.9;
  const pip = 0.2 + m.submergence * 0.0091;
  const flowT = prod ? 40 + (m.sandfaceT - 47) * 0.45 : m.phase === 'INJECTION' ? 285 : 60;

  // impact loading (fluid pound): share of strokes that pound, and plunger velocity at impact
  const pound = (fill) => clamp((0.85 - fill) / 0.35, 0, 1);
  const impactsDay = prod ? spm * 1440 * pound(m.fillage) : 0;
  const rec = m.recommendation;
  const fill2 = clamp(m.fillage * m.spm / Math.max(rec.spm, 0.5), 0, 0.97);
  const impactsMantle = prod ? rec.spm * 1440 * pound(fill2) : 0;
  const impactVel = prod ? (0.15 + (1 - m.fillage) * 1.3) * spm / 5.4 : 0;

  // pump unseating: uplift (viscous drag + pound) vs hold-down
  const uplift = 9 + (m.viscosity / 1000) * 2.5 + (1 - m.fillage) * 8;
  const upliftMargin = UNSEATS.holdDownKn / uplift;
  const unseatRisk = clamp(0.05 + (2.0 - upliftMargin) * 0.3, 0.03, 0.7);

  // costs
  const prodDays = CYCLE.days - CYCLE.soakEnd;
  const steamDay = (COST.steamPerT * m.steamTons) / prodDays;
  const powerDay = m.motorKw * 24 * COST.kwh;
  const costDay = steamDay + powerDay + COST.maintPerDay + COST.chemPerDay;
  const costBbl = prod && m.oilRate > 0.5 ? costDay / m.oilRate : null;

  const pastCum = 3900 + 3500 + 3150;
  const recovery = (pastCum + m.cumOil) / 1.2e6;

  return {
    hz, amps, ampsAvg, profile, stroke: m.stroke,
    thp, chp, pip, flowT, pRes: FLUID.pRes,
    counterbalance: clamp(0.97 - Math.abs(m.kd - 0.52) * 0.25, 0.7, 1), beamLoad: m.pprl / 120,
    impactsDay, impactsMantle, impactVel,
    uplift, upliftMargin, unseatRisk,
    cost: { steamDay, powerDay, maintDay: COST.maintPerDay, chemDay: COST.chemPerDay, costDay, costBbl },
    recovery,
  };
}
