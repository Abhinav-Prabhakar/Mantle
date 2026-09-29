// sim.js - physics / engineering model behind the Baghewala (BGW-17) digital twin.
// Pure ES module, no DOM, deterministic. Depends only on rig.js geometry.
//
// Model in one paragraph
//   Cyclic steam stimulation: INJECTION (day 0-14) -> SOAK (14-18) -> PRODUCTION (18-120).
//   Sandface temperature rises during injection, then decays exponentially toward the 47 C
//   reservoir temperature. Viscosity follows an ASTM D341/Walther law fitted through
//   ~12,000 cP @ 50 C and ~80 cP @ 150 C. Inflow uses a Boberg-Lantz style productivity ratio
//   (hot zone of radius r_h in series with a cold outer zone) times a slow depletion decline.
//   A wellbore temperature profile gives viscosity versus depth; rod drag is a Couette
//   annulus integral  F = sum 2*pi*mu*v*dz / ln(Dt/Dr)  (with an effective-viscosity factor for
//   shear-thinning / water wetting). Rod loads follow API RP 11L-style terms (buoyant rod
//   weight, fluid load, Mills acceleration factor, viscous drag). Float margin
//   = 1 - (peak downstroke drag + friction)/W_rf, and the safe SPM is the rate at which that
//   margin hits 15 %. VFD "stroke shaping" (kd = downstroke time share) changes the peak
//   downstroke speed and therefore the safe SPM. Economics are in INR.
//
// Units: SI unless a name says otherwise (loads in N internally, kN at the API boundary).

import { UNIT, STROKE, unitPose, rodPosition, WELLBORE, STRATA, depthToY } from './rig.js';

/* ------------------------------------------------------------------ constants */

const TAU = Math.PI * 2;
const G = 9.81;
const LBF_N = 4.44822;
const S_M = STROKE.length;                 // polished-rod stroke (m)
const S_IN = S_M / 0.0254;                 // stroke in inches
const CYCLE_DAYS = 120, INJ_END = 14, SOAK_END = 18;
export const CYCLE = { days: CYCLE_DAYS, injEnd: INJ_END, soakEnd: SOAK_END };
const T_RES = 47;                          // reservoir temperature (C)
const Z_SAND = 1120;                       // mid-perforation depth (m)
const PUMP_DEPTH = WELLBORE.pumpTop;       // 1068 m
const PUMP_INTAKE = WELLBORE.pumpBottom;   // 1088 m
const PLUNGER_IN = 1.25;                   // plunger diameter (in) - sized to the low liquid rate
const ETA_S = 0.88;                        // stroke loss (rod stretch, slippage)
const OIL_SG = 0.945, WATER_SG = 1.02;
const SPM_MIN = 0.5, SPM_MAX = 15;
const PRICE = { oil: 6000, steamT: 2800, kwh: 8 };
const GRID_CO2_KG_KWH = 0.71, STEAM_CO2_T_PER_T = 0.062;
const BBL_PER_T_CWE = 6.2898;
const TORQUE_RATING_INLB = 320000;
const MU_CAP_CP = 30000;                   // wetted-rod / emulsified cap on annulus viscosity
const KVIS = 0.26;                         // effective viscosity fraction seen by the rods
const FRIC_FRAC = 0.15;                    // rod/tubing friction as a fraction of W_rf
const MARGIN_REQ = 0.15;

// Rod string (top to bottom): 1-1/8", 1", 7/8"; weights in N/m incl. couplings and sinker/heavy
// rods for a deviated completion (x1.25 on bare rod weight); areas in mm2.
const SECT = [
  { top: 0, bot: 500, A: 641, w: 67, lnr: Math.log(62 / 28.575) },
  { top: 500, bot: 800, A: 506.7, w: 53, lnr: Math.log(62 / 25.4) },
  { top: 800, bot: PUMP_DEPTH, A: 387.9, w: 40.6, lnr: Math.log(62 / 22.2) },
];
const W_R = SECT.reduce((a, s) => a + s.w * (s.bot - s.top), 0);           // N in air
const wBelow = (X) => SECT.reduce((a, s) => a + s.w * Math.max(0, s.bot - Math.max(s.top, X)), 0);

const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
const smooth = (t) => { t = clamp(t, 0, 1); return t * t * (3 - 2 * t); };
const fin = (v, d = 0) => (Number.isFinite(v) ? v : d);

/* ------------------------------------------------------------------ viscosity */

// Walther: log10(log10(nu+0.7)) = A - B*log10(T_K). Fit through 12000 cP @ 50 C, 80 cP @ 150 C.
const WAL = (() => {
  const f = (cP, C) => [Math.log10(Math.log10(cP / 0.96 + 0.7)), Math.log10(C + 273.15)];
  const [y1, x1] = f(12000, 50), [y2, x2] = f(80, 150);
  const B = (y1 - y2) / (x2 - x1);
  return { A: y1 + B * x1, B };
})();
export function viscosityCp(TC) {
  const T = clamp(fin(TC, T_RES), 5, 320);
  const nu = Math.pow(10, Math.pow(10, WAL.A - WAL.B * Math.log10(T + 273.15))) - 0.7;
  return Math.max(0.3, nu * 0.96);
}
const MU_COLD = viscosityCp(T_RES);

/* ------------------------------------------------------------------ crank kinematics tables */

const NK = 720, HK = TAU / NK;
const KX = new Float64Array(NK), KXP = new Float64Array(NK);
for (let i = 0; i < NK; i++) KX[i] = rodPosition(i * HK);
for (let i = 0; i < NK; i++) KXP[i] = (KX[(i + 1) % NK] - KX[(i - 1 + NK) % NK]) / (2 * HK);
const XP_MAX = KXP.reduce((a, b) => Math.max(a, Math.abs(b)), 0);

function refine(theta0, sign) {           // golden-section on rodPosition around a table extremum
  let a = theta0 - HK, b = theta0 + HK;
  const gr = 0.6180339887;
  for (let i = 0; i < 40; i++) {
    const c = b - gr * (b - a), d = a + gr * (b - a);
    if (sign * rodPosition(c) > sign * rodPosition(d)) b = d; else a = c;
  }
  return (((a + b) / 2) % TAU + TAU) % TAU;
}
const TH_TOP = (() => { let k = 0; for (let i = 0; i < NK; i++) if (KX[i] > KX[k]) k = i; return refine(k * HK, 1); })();
const TH_BOT = (() => { let k = 0; for (let i = 0; i < NK; i++) if (KX[i] < KX[k]) k = i; return refine(k * HK, -1); })();

function interp(arr, theta) {
  const u = ((theta % TAU + TAU) % TAU) / HK;
  const i = Math.floor(u), f = u - i;
  return arr[i % NK] * (1 - f) + arr[(i + 1) % NK] * f;
}

// Per-kd table: shaped velocity V (m per rad of crank, times omega gives m/s) and acceleration.
// VFD stroke shaping: downstroke runs at 0.5/kd of nominal crank speed, upstroke at 0.5/(1-kd).
const ktCache = new Map();
function kdTable(kd) {
  const key = Math.round(kd * 1000);
  let t = ktCache.get(key);
  if (t) return t;
  const k = clamp(key / 1000, 0.35, 0.75);
  const sUp = 0.5 / (1 - k), sDn = 0.5 / k;
  const s = new Float64Array(NK), V = new Float64Array(NK), Ab = new Float64Array(NK);
  for (let i = 0; i < NK; i++) {
    const w = 0.5 * (1 + Math.tanh(KXP[i] / (0.04 * XP_MAX)));
    s[i] = w * sUp + (1 - w) * sDn;
    V[i] = KXP[i] * s[i];
  }
  let vUp = 0, vDn = 0, aPk = 0, iDrag = 0;
  for (let i = 0; i < NK; i++) {
    Ab[i] = s[i] * (V[(i + 1) % NK] - V[(i - 1 + NK) % NK]) / (2 * HK);
    vUp = Math.max(vUp, V[i]); vDn = Math.max(vDn, -V[i]); aPk = Math.max(aPk, Math.abs(Ab[i]));
    iDrag += Math.abs(V[i]) * Math.abs(KXP[i]) * HK;
  }
  t = { kd: k, s, V, Ab, vUp, vDn, aPk, iDrag };
  ktCache.set(key, t);
  return t;
}
const APK_BASE = kdTable(0.5).aPk;

/* ------------------------------------------------------------------ thermal history */

// Steam scale s = steam/800 t. exc0 = sandface excess over reservoir at end of soak.
function thermal(steam, day) {
  const s = Math.max(0.2, steam / 800);
  const g = (1 - Math.exp(-4.5 * s)) / (1 - Math.exp(-4.5));   // saturating heat delivery
  const exc0 = 143 * (0.3 + 0.7 * g);
  const rh0 = 11 * (0.6 + 0.4 * g);
  const tau = 40 * Math.pow(s, 0.2);
  let phase, exc, rh;
  if (day < INJ_END) {
    phase = 'INJECTION';
    exc = 1.04 * exc0 * (1 - Math.exp(-day / 5)) / (1 - Math.exp(-INJ_END / 5));
    rh = rh0 * Math.sqrt(day / INJ_END);
  } else if (day < SOAK_END) {
    phase = 'SOAK';
    exc = exc0 * (1.04 - 0.04 * (day - INJ_END) / (SOAK_END - INJ_END));
    rh = rh0;
  } else {
    phase = 'PRODUCTION';
    const t = day - SOAK_END;
    exc = exc0 * Math.exp(-t / tau);
    rh = rh0 * (0.75 + 0.25 * Math.exp(-t / 38));
  }
  return { phase, T: T_RES + exc, exc, exc0, rh, rh0, battery: clamp(exc / exc0, 0, 1) };
}

/* ------------------------------------------------------------------ reservoir inflow */

const RW = 0.11, RE = 40;
const steamMult = (s) => (1 - Math.exp(-4 * s)) / (1 - Math.exp(-4));   // saturating contact
function prodRatio(T, rh) {                // Boberg-Lantz style: hot zone in series with cold outer zone
  const muH = viscosityCp(T_RES + 0.65 * (T - T_RES));
  const R = Math.max(rh, RW * 1.5);
  return (MU_COLD * Math.log(RE / RW)) / (muH * Math.log(R / RW) + MU_COLD * Math.log(RE / R));
}
const DEPLETION_TAU = 220;
const Q0 = (() => {                        // calibrate: ~82 bpd liquid on day 20 with 800 t of steam
  const th = thermal(800, 20);
  return 82 / (prodRatio(th.T, th.rh) * Math.exp(-2 / DEPLETION_TAU));
})();
const waterCut = (t) => 0.15 + 0.20 * (1 - Math.exp(-Math.max(0, t) / 70));

/* ------------------------------------------------------------------ wellbore temperature & drag */

const Tgeo = (z) => 28 + 19 * z / 1120;
function tFluid(z, exc, Lr) {              // flowing fluid temperature at depth z
  if (z >= Z_SAND) return Tgeo(z) + exc * Math.exp(-(z - Z_SAND) / 60);
  return Tgeo(z) + exc * Math.exp(-(Z_SAND - z) / Lr);
}

// Drag coefficient c (N*s/m): F_drag = c * |v_rod|. Also c500/c800 = share below those depths.
function dragCoeff(exc, Lr) {
  const dz = 12;
  let c = 0, c500 = 0, c800 = 0;
  for (let z = dz / 2; z < PUMP_DEPTH; z += dz) {
    const mu = Math.min(viscosityCp(tFluid(z, exc, Lr)), MU_CAP_CP) * KVIS / 1000;   // Pa*s
    const sec = z < 500 ? SECT[0] : z < 800 ? SECT[1] : SECT[2];
    const d = TAU * mu * dz / sec.lnr;
    c += d; if (z >= 500) c500 += d; if (z >= 800) c800 += d;
  }
  return { c, c500, c800 };
}

// Per-day production base state (independent of spm/kd).
function prodBase(steam, day) {
  const th = thermal(steam, day);
  const dp = Math.max(day, SOAK_END), tp = thermal(steam, dp);
  const t = dp - SOAK_END;
  const qIn = Q0 * steamMult(Math.max(0.2, steam / 800)) * prodRatio(tp.T, tp.rh) * Math.exp(-t / DEPLETION_TAU);
  const wc = waterCut(t);
  const parked = th.phase !== 'PRODUCTION';
  const Lr = parked ? 4000 : 250 + 5 * qIn;
  const drag = dragCoeff(th.exc, Lr);
  const Tpump = tFluid(PUMP_INTAKE, th.exc, Lr);
  return { day, th, T: th.T, rh: th.rh, qIn, wc, Lr, muPump: viscosityCp(Tpump), Tpump, ...drag };
}
const baseCache = new Map();
function baseArr(steam) {                  // integer days 0..120
  const key = Math.round(steam);
  let a = baseCache.get(key);
  if (!a) {
    a = [];
    for (let d = 0; d <= CYCLE_DAYS; d++) a.push(prodBase(steam, d));
    if (baseCache.size > 40) baseCache.clear();
    baseCache.set(key, a);
  }
  return a;
}

/* ------------------------------------------------------------------ per-point engineering core */

const PD_K = 0.1166 * S_IN * PLUNGER_IN * PLUNGER_IN;    // bbl/d per SPM
const softmin = (a, b, p = 10) => Math.pow(Math.pow(Math.max(a, 1e-6), -p) + Math.pow(Math.max(b, 1e-6), -p), -1 / p);

function core(b, spm, kt) {
  const wc = b.wc;
  const Gfl = (1 - wc) * OIL_SG + wc * WATER_SG;
  const bf = 1 - 0.128 * Gfl;
  const Wrf = W_R * bf;
  const Fo = 0.340 * Gfl * PLUNGER_IN * PLUNGER_IN * (PUMP_DEPTH / 0.3048) * LBF_N;
  const omega = TAU * spm / 60;
  const vUp = omega * kt.vUp, vDn = omega * kt.vDn;
  const dUp = b.c * vUp, dDn = b.c * vDn;
  const Ffric = FRIC_FRAC * Wrf;
  const marginRaw = 1 - (dDn + Ffric) / Wrf;
  const margin = clamp(marginRaw, -1, 1);
  const kSafe = b.c * (TAU / 60) * kt.vDn;
  const spmSafe = kSafe > 1e-9 ? clamp((0.85 * Wrf - Ffric) / kSafe, 0.5, SPM_MAX) : SPM_MAX;
  const etaFloat = 1 - clamp(-marginRaw * 0.8, 0, 0.5);
  const PDg = PD_K * spm;
  const PDe = Math.max(1e-6, PDg * ETA_S * etaFloat);
  const q = softmin(b.qIn, PDe);
  const fill = clamp(q / PDe, 0, 0.98);
  const oil = q * (1 - wc);
  const alpha = (S_IN * spm * spm / 70500) * (kt.aPk / APK_BASE);
  const pprl = (Wrf + Fo + W_R * alpha + dUp) / 1000;
  const mprl = Math.max(0, (Wrf - W_R * alpha - dDn) / 1000);
  const torque = clamp(0.25 * S_IN * ((pprl - mprl) * 1000 / LBF_N) * 0.55 / TORQUE_RATING_INLB, 0, 1.5);
  // Goodman at the top of each rod section (modified Goodman, Grade D 793 MPa, service factor 0.85).
  let goodman = 0;
  for (const X of [0, 500, 800]) {
    const sec = SECT.find((s) => s.top === X);
    const wb = wBelow(X), cb = X === 0 ? b.c : X === 500 ? b.c500 : b.c800;
    const smax = (wb * bf + Fo + wb * alpha + cb * vUp) / sec.A;
    const smin = Math.max(0, (wb * bf - wb * alpha - cb * vDn) / sec.A);
    goodman = Math.max(goodman, smax / (0.85 * (793 / 4 + 0.5625 * smin)));
  }
  goodman = clamp(goodman, 0, 1.5);
  const work = Fo * S_M * fill + b.c * omega * kt.iDrag;           // J per stroke (card area)
  const kwPr = work * spm / 60 / 1000;
  const motorKw = kwPr / (0.85 * 0.9) + 0.5;
  const r = b.qIn / PDe;
  const level = 350 + 550 * (1 - smooth((r - 0.3) / 1.4));           // depth to fluid level (m)
  return {
    c: b.c, wc, Gfl, Wrf, Fo, omega, vUp, vDn, dUp, dDn, Ffric, marginRaw, margin, spmSafe, PDg, PDe, q, fill, oil,
    alpha, pprl, mprl, torque, goodman, motorKw, level, pumpEff: clamp(q / Math.max(PDg, 1e-6), 0, 1),
    bottleneck: b.qIn > PDe ? 'PUMP' : 'RESERVOIR',
  };
}

/* ------------------------------------------------------------------ cycle arrays (day 0..120) */

function cycle(steam, spm, kd) {
  const kt = kdTable(kd), pb = baseArr(steam);
  const o = { wat: [], T: [], mu: [], oil: [], wc: [], spmSafe: [], margin: [], cum: [], cumW: [], netEx: [], kw: [] };
  let cum = 0, cumW = 0;
  for (let d = 0; d <= CYCLE_DAYS; d++) {
    const b = pb[d], prod = d >= SOAK_END;
    const c = core(prod ? b : pb[SOAK_END], spm, kt);   // before production show the day-18 state
    const oil = prod ? c.oil : 0, liq = prod ? c.q : 0, kw = prod ? c.motorKw : 0;
    if (prod && d > SOAK_END) {
      cum += (o.oil[d - 1] + oil) / 2; cumW += (o.wat[d - 1] + liq * c.wc) / 2;
    }
    o.T.push(b.T); o.mu.push(b.muPump); o.oil.push(oil); o.wc.push(prod ? c.wc : 0);
    o.spmSafe.push(c.spmSafe); o.margin.push(c.margin); o.cum.push(cum); o.cumW.push(cumW);
    o.kw.push(kw); o.wat.push(liq * c.wc);
    o.netEx.push(oil * PRICE.oil - kw * 24 * PRICE.kwh);
  }
  return o;
}

/* ------------------------------------------------------------------ coupling dividend */

const STEAM_GRID = [500, 600, 700, 800, 900, 1000, 1100];
const SPM_GRID = (() => { const a = []; for (let s = 2; s <= 9.0001; s += 0.5) a.push(+s.toFixed(2)); return a; })();
function evalPlan(steam, spm, kt, reservoirOnly = false) {
  const pb = baseArr(steam);
  let val = -steam * PRICE.steamT, oil = 0, minM = 1;
  for (let d = SOAK_END; d <= CYCLE_DAYS; d++) {
    if (reservoirOnly) {                 // lift assumed unlimited: pure reservoir response to steam
      const o = pb[d].qIn * (1 - pb[d].wc);
      val += o * PRICE.oil; oil += o; continue;
    }
    const c = core(pb[d], spm, kt);
    val += c.oil * PRICE.oil - c.motorKw * 24 * PRICE.kwh; oil += c.oil;
    minM = Math.min(minM, c.marginRaw);
  }
  return { steam, spm, val, oil, minM, ok: minM >= MARGIN_REQ };
}
const couplingCache = new Map();
function couplingDividend(kd) {
  const key = Math.round(kd * 1000);
  if (couplingCache.has(key)) return couplingCache.get(key);
  const kt = kdTable(kd);
  const better = (a, b) => (!a || b.val > a.val ? b : a);
  // sequential: steam is optimised first at a nominal 6 SPM (feasibility not enforced; float only
  // costs production), then the best feasible SPM is chosen for that fixed steam volume.
  let seqSteam = null;
  for (const st of STEAM_GRID) seqSteam = better(seqSteam, evalPlan(st, 6, kt));
  let seq = null, joint = null, fallback = null;
  for (const spm of SPM_GRID) {
    const p = evalPlan(seqSteam.steam, spm, kt);
    if (p.ok) seq = better(seq, p);
    if (!fallback || p.minM > fallback.minM) fallback = p;
  }
  seq = seq || fallback;
  let jFallback = null;
  for (const st of STEAM_GRID) for (const spm of SPM_GRID) {
    const p = evalPlan(st, spm, kt);
    if (p.ok) joint = better(joint, p);
    if (!jFallback || p.minM > jFallback.minM) jFallback = p;
  }
  joint = joint || jFallback;
  const res = {
    inrPerCycle: Math.max(0, joint.val - seq.val),
    oilPct: Math.max(0, (joint.oil - seq.oil) / Math.max(seq.oil, 1)),
    jointSteam: joint.steam, jointSpm: joint.spm, seqSteam: seq.steam, seqSpm: seq.spm,
  };
  couplingCache.set(key, res);
  return res;
}

/* ------------------------------------------------------------------ dynamometer load model */

// Instantaneous polished-rod load (N) at crank angle theta, given model coefficients m.
function surfacePoint(m, kt, theta, omega) {
  const x = interp(KX, theta);
  const V = interp(kt.V, theta), Ab = interp(kt.Ab, theta);
  const v = omega * V, ag = omega * omega * Ab / G;
  const up = V >= 0;
  const xp = m.xp, w = m.w;
  let F = m.Wrf + m.Wr * ag;
  if (up) {
    const d = x / S_M;
    F += m.Fo * smooth(d / 0.06) + m.c * Math.abs(v) + m.Fo * 0.04 * Math.exp(-d / 0.07) * Math.sin(TAU * d / 0.12);
  } else {
    const psi = 1 / (1 + Math.exp(-(x - xp) / w));
    const d = Math.max(0, xp - x) / S_M;
    F += m.Fo * psi - m.c * Math.abs(v)
      + m.Fo * m.amp * Math.exp(-d / 0.08) * Math.cos(TAU * d / 0.13) * (1 - psi);
  }
  const eps = 0.02 * m.Wrf;                 // soft floor: rods cannot push (float flattening near 0)
  F = 0.5 * (F + Math.sqrt(F * F + eps * eps));
  return { x: clamp(x, 0, S_M), f: F / 1000, up };
}
function downholePoint(m, kt, theta) {
  const x = interp(KX, theta), V = interp(kt.V, theta);
  const xd = x * m.strokeRatio;
  let f;
  if (V >= 0) f = m.Fo * smooth(x / (0.035 * S_M));
  else f = m.Fo / (1 + Math.exp(-(x - m.xp) / m.wDh));
  return { x: clamp(xd, 0, S_M), f: f / 1000 };
}
function loadModel(c, kt) {
  return {
    Wrf: c.Wrf, Wr: W_R, Fo: c.Fo, c: c.c, xp: S_M * c.fill,
    w: S_M * (0.008 + 0.02 * (1 - c.fill)),
    wDh: S_M * (0.006 + 0.03 * (1 - c.fill)),
    amp: 0.06 + 0.6 * Math.max(0, 0.9 - c.fill),
    strokeRatio: ETA_S * (1 - clamp(-c.marginRaw * 0.8, 0, 0.5)) * 1.0 + (1 - ETA_S) * 0.5,
  };
}

/* ------------------------------------------------------------------ the simulator */

export class WellSim {
  constructor({ spm = 5.4, cycleDay = 41, kd = 0.5, steam = 800 } = {}) {
    this._p = { spm: clamp(fin(spm, 5.4), SPM_MIN, SPM_MAX), day: clamp(fin(cycleDay, 41), 0, CYCLE_DAYS), kd: clamp(fin(kd, 0.5), 0.4, 0.7), steam: clamp(fin(steam, 800), 300, 1400) };
    this._theta = this._phaseOf(this._p.day) === 'PRODUCTION' ? TH_BOT : TH_TOP;
    this._spmAct = this._phaseOf(this._p.day) === 'PRODUCTION' ? this._p.spm : 0;
    this._dirty = true; this._cyc = null; this._cycKey = '';
    this._state = { phase: 'SOAK', theta: this._theta, rodPos: 0, rodVel: 0, load: 0, spmActual: 0, floatNow: false };
    this._recompute();
    this._updateState(this._spmAct > 0 ? TAU * this._spmAct / 60 : 0);
  }

  _phaseOf(d) { return d < INJ_END ? 'INJECTION' : d < SOAK_END ? 'SOAK' : 'PRODUCTION'; }

  set({ spm, cycleDay, kd, steam } = {}) {
    const p = this._p;
    if (spm !== undefined) p.spm = clamp(fin(spm, p.spm), SPM_MIN, SPM_MAX);
    if (cycleDay !== undefined) p.day = clamp(fin(cycleDay, p.day), 0, CYCLE_DAYS);
    if (kd !== undefined) p.kd = clamp(fin(kd, p.kd), 0.4, 0.7);
    if (steam !== undefined) p.steam = clamp(fin(steam, p.steam), 300, 1400);
    this._dirty = true;
    this._recompute();
    const run = this._phase === 'PRODUCTION';
    this._updateState(run ? this._omega() : 0);
  }

  _omega() { return TAU * this._spmAct / 60; }

  _recompute() {
    const p = this._p;
    this._phase = this._phaseOf(p.day);
    this._kt = kdTable(p.kd);
    this._b = prodBase(p.steam, p.day);
    this._c = core(this._b, p.spm, this._kt);
    this._lm = loadModel(this._c, this._kt);
    this._m = null; this._dirty = true;
  }

  get theta() { return this._theta; }
  get state() { return this._state; }

  step(dt) {
    dt = clamp(fin(dt, 0), 0, 0.25);
    const run = this._phase === 'PRODUCTION';
    const kt = this._kt;
    const target = run ? this._p.spm : 0;
    this._spmAct += (target - this._spmAct) * (1 - Math.exp(-dt / 0.7));
    let omega = TAU * this._spmAct / 60;
    if (run) {
      const s = interp(kt.s, this._theta);
      this._theta = (this._theta + omega * s * dt) % TAU;
    } else if (this._spmAct !== 0 || Math.abs(this._theta - TH_TOP) > 1e-9) {
      // park with the horsehead at the top of stroke: creep forward, converging on TH_TOP
      const d = (((TH_TOP - this._theta) % TAU) + TAU) % TAU;
      if (d < 0.004 || d > TAU - 0.004) { this._theta = TH_TOP; this._spmAct = 0; omega = 0; }
      else {
        omega = Math.min(Math.max(omega, 0.4), 2.5 * d + 0.02);
        this._theta = (this._theta + omega * dt) % TAU;
        this._spmAct = omega * 60 / TAU;
      }
    }
    this._updateState(omega);
  }

  _updateState(omega) {
    const st = this._state, kt = this._kt, run = this._phase === 'PRODUCTION';
    st.phase = this._phase; st.theta = this._theta;
    st.rodPos = clamp(rodPosition(this._theta), 0, S_M);
    st.spmActual = this._spmAct;
    const V = run ? interp(kt.V, this._theta) : interp(KXP, this._theta);
    st.rodVel = omega * V;
    if (omega > 1e-6 && (run || this._spmAct > 0)) {
      st.load = surfacePoint(this._lm, kt, this._theta, omega).f;
      st.floatNow = run && V < 0 && this._c.marginRaw < 0;
    } else {
      st.load = (this._c.Wrf + (run ? this._c.Fo : 0)) / 1000; st.floatNow = false;
    }
  }

  /* ---- cycle-level values ---- */

  _cycle() {
    const p = this._p, key = `${p.spm.toFixed(3)}|${p.kd}|${Math.round(p.steam)}`;
    if (this._cycKey !== key) { this._cyc = cycle(p.steam, p.spm, p.kd); this._cycKey = key; }
    return this._cyc;
  }

  metrics() {
    if (this._m) return this._m;
    const p = this._p, c = this._c, b = this._b, th = b.th, phase = this._phase;
    const cyc = this._cycle();
    const prod = phase === 'PRODUCTION';
    const day = p.day, i0 = Math.min(CYCLE_DAYS - 1, Math.floor(day)), f = day - i0;
    const cumOil = prod ? cyc.cum[i0] * (1 - f) + cyc.cum[i0 + 1] * f : 0;
    const cumWater = prod ? (cyc.cumW[i0] * (1 - f) + cyc.cumW[i0 + 1] * f) : 0;
    const steamRate = p.steam / INJ_END;
    const steamTons = phase === 'INJECTION' ? steamRate * day : p.steam;
    const oil = prod ? c.oil : 0;
    const liq = prod ? c.q : 0;
    const sor = prod && cumOil > 5 ? clamp(p.steam * BBL_PER_T_CWE / cumOil, 0, 99) : 0;
    const kwh = prod ? c.motorKw * 24 : 0;
    const kwhBbl = prod ? kwh / Math.max(oil, 0.5) : 0;
    const co2 = prod ? Math.min(400, p.steam * STEAM_CO2_T_PER_T * 1000 / Math.max(cumOil, 50) + kwhBbl * GRID_CO2_KG_KWH) : 0;
    const water = prod ? Math.max(0, p.steam - 0.85 * cumWater * 0.159) / Math.max(cumOil, 50) : 0;
    const steamCost = PRICE.steamT * p.steam;
    let net = 0;
    if (prod) net = oil * PRICE.oil - steamCost / (CYCLE_DAYS - SOAK_END) - kwh * PRICE.kwh;
    else if (phase === 'INJECTION') net = -steamRate * PRICE.steamT;

    // marginal-value cutoff: leave when the daily margin falls below the best whole-cycle average
    let cum = 0, best = -Infinity, dcut = CYCLE_DAYS;
    for (let d = SOAK_END + 1; d <= CYCLE_DAYS; d++) {
      cum += (cyc.netEx[d - 1] + cyc.netEx[d]) / 2;
      const avg = (cum - steamCost) / d;
      if (avg > best) { best = avg; dcut = d; }
    }
    const daysToCutoff = Math.max(0, dcut - day);

    const dep = prod ? deposition(th.exc, b.Lr) : { top: null, bot: null };
    const fillage = prod ? c.fill : 0;
    const coupling = couplingDividend(p.kd);
    const level = c.level, submergence = Math.max(0, PUMP_DEPTH - level);
    const m = {
      phase, cycleDay: day,
      dayInPhase: phase === 'INJECTION' ? day : phase === 'SOAK' ? day - INJ_END : day - SOAK_END,
      spm: p.spm, kd: p.kd, stroke: S_M,
      sandfaceT: th.T, viscosity: b.muPump, heatedRadius: th.rh, thermalBattery: th.battery,
      daysToCutoff, oilRate: oil, waterCut: prod ? c.wc : 0, liquidRate: liq,
      pumpDisplacement: prod ? c.PDg : 0, fillage, pumpEff: prod ? c.pumpEff : 0,
      bottleneck: c.bottleneck, pprl: c.pprl, mprl: c.mprl,
      floatMargin: prod ? c.margin : 1, spmSafe: c.spmSafe, goodman: c.goodman,
      torquePct: prod ? c.torque : 0, motorKw: prod ? c.motorKw : 0, kwhPerBbl: kwhBbl,
      sor, steamTons, cumOil, co2PerBbl: co2, waterPerBbl: water, netPerDay: net,
      fluidLevel: level, submergence,
      couplingDividend: { inrPerCycle: coupling.inrPerCycle, oilPct: coupling.oilPct },
    };
    m.recommendation = this._recommend(m, coupling, prod);
    m.alerts = this._alerts(m, dep, steamRate, prod);
    this._m = m;
    this._dep = dep;
    return m;
  }

  _recommend(m, coupling, prod) {
    const p = this._p, b = this._b;
    const eval2 = (spm, kd) => core(b, spm, kdTable(kd));
    const mk = (title, detail, spm, kd, conf) => {
      const c2 = eval2(spm, kd), c0 = this._c;
      const e0 = c0.motorKw * 24 / Math.max(c0.oil, 0.5), e1 = c2.motorKw * 24 / Math.max(c2.oil, 0.5);
      return {
        title, detail, spm, kd, confidence: conf,
        deltas: { oil: fin((c2.oil - c0.oil) / Math.max(c0.oil, 0.5)), float: fin(c2.margin - c0.margin), energy: fin((e1 - e0) / Math.max(e0, 0.1)) },
      };
    };
    if (!prod) {
      return { title: m.phase === 'INJECTION' ? 'Hold: steaming' : 'Hold: soak', detail: `Pre-set production at ${coupling.jointSpm.toFixed(1)} SPM (joint optimum with ${coupling.jointSteam} t steam).`, spm: coupling.jointSpm, kd: p.kd, deltas: { oil: 0, float: 0, energy: 0 }, confidence: 0.7 };
    }
    if (p.spm > 0.95 * m.spmSafe) {
      const spm2 = clamp(Math.min(p.spm, 0.9 * eval2(p.spm, 0.62).spmSafe), 2, 9);
      return mk('Slow down and shape the stroke', `Rods are near float (margin ${(m.floatMargin * 100).toFixed(0)}%). Run ${spm2.toFixed(1)} SPM with kd 0.62 to restore margin.`, spm2, 0.62, 0.84);
    }
    if (m.fillage < 0.8) {
      const spm2 = clamp(p.spm * m.fillage / 0.92, 2, 9);
      return mk('Match pump speed to inflow', `Fillage ${(m.fillage * 100).toFixed(0)}%: the pump outruns the reservoir. Slow to ${spm2.toFixed(1)} SPM to cut fluid pound and power.`, spm2, p.kd, 0.76);
    }
    return { title: 'Hold settings', detail: 'Pump, rods and reservoir are balanced.', spm: p.spm, kd: p.kd, deltas: { oil: 0, float: 0, energy: 0 }, confidence: 0.9 };
  }

  _alerts(m, dep, steamRate, prod) {
    const a = [];
    if (m.phase === 'INJECTION') a.push({ level: 'ok', text: `Steam injection at ${steamRate.toFixed(0)} t/day; heated radius ${m.heatedRadius.toFixed(1)} m.` });
    if (m.phase === 'SOAK') a.push({ level: 'ok', text: `Soak: heat equalising near the well (${m.sandfaceT.toFixed(0)} C). Unit parked.` });
    if (prod) {
      if (m.floatMargin < 0) a.push({ level: 'crit', text: `Rod float: margin ${(m.floatMargin * 100).toFixed(0)}%. Rods lag on the downstroke; slow below ${m.spmSafe.toFixed(1)} SPM.` });
      else if (m.floatMargin < 0.2) a.push({ level: 'warn', text: `Float margin only ${(m.floatMargin * 100).toFixed(0)}% (safe limit ${m.spmSafe.toFixed(1)} SPM).` });
      if (m.fillage < 0.7) a.push({ level: 'warn', text: `Pump fillage ${(m.fillage * 100).toFixed(0)}%: fluid pound risk.` });
      if (m.goodman > 1) a.push({ level: 'crit', text: `Goodman ratio ${m.goodman.toFixed(2)}: rod fatigue limit exceeded.` });
      else if (m.goodman > 0.9) a.push({ level: 'warn', text: `Goodman ratio ${m.goodman.toFixed(2)}: rods near fatigue limit.` });
      if (m.torquePct > 1) a.push({ level: 'crit', text: `Gearbox torque ${(m.torquePct * 100).toFixed(0)}% of rating.` });
      if (dep.bot !== null) a.push({ level: 'warn', text: `Asphaltene deposition band ${dep.top.toFixed(0)}-${dep.bot.toFixed(0)} m (fluid below 62 C).` });
      if (m.daysToCutoff <= 0) a.push({ level: 'warn', text: 'Past economic cut-off: plan the next steam cycle.' });
    }
    if (!a.length || a.every((x) => x.level === 'ok' && prod)) a.push({ level: 'ok', text: 'All operating limits nominal.' });
    return a;
  }

  /* ---- cards ---- */

  dynoCard(n = 180) {
    n = Math.max(8, Math.floor(n));
    const c = this._c, kt = this._kt, m = this._lm, omega = TAU * this._p.spm / 60;
    const surface = [], downhole = [];
    let fMin = Infinity, fMax = -Infinity;
    for (let i = 0; i < n; i++) {
      const th = i === n - 1 ? TH_BOT : TH_BOT + TAU * i / (n - 1);
      const s = surfacePoint(m, kt, th, omega), d = downholePoint(m, kt, th);
      surface.push({ x: s.x, f: s.f }); downhole.push({ x: d.x, f: d.f });
      fMin = Math.min(fMin, s.f, d.f); fMax = Math.max(fMax, s.f, d.f);
    }
    surface[n - 1] = { ...surface[0] }; downhole[n - 1] = { ...downhole[0] };
    // classification
    const dragFrac = c.dDn / c.Wrf;
    let cls = 'NORMAL', conf = clamp(0.6 + (c.margin - 0.4) * 0.5, 0.55, 0.95);
    if (c.marginRaw < MARGIN_REQ) { cls = 'ROD FLOAT RISK'; conf = clamp(0.65 + (MARGIN_REQ - c.marginRaw), 0.6, 0.98); }
    else if (c.fill < 0.8) { cls = 'FLUID POUND'; conf = clamp(0.62 + (0.8 - c.fill) * 1.2, 0.6, 0.98); }
    else if (dragFrac > 0.35) { cls = 'VISCOUS DRAG'; conf = clamp(0.6 + (dragFrac - 0.35), 0.6, 0.95); }
    return { surface, downhole, xMax: S_M, fMin, fMax, cls, clsConf: conf };
  }

  /* ---- whole-cycle curves ---- */

  series() {
    const cyc = this._cycle(), cum = cyc.cum, steam = this._p.steam;
    const out = { day: [], T: [], mu: [], oil: [], oilP10: [], oilP90: [], spmSafe: [], floatMargin: [], sor: [] };
    for (let d = 0; d <= CYCLE_DAYS; d++) {
      const t = Math.max(0, d - SOAK_END), spread = 0.07 + 0.16 * Math.min(1, t / 102);
      out.day.push(d); out.T.push(cyc.T[d]); out.mu.push(cyc.mu[d]);
      out.oil.push(cyc.oil[d]);
      out.oilP10.push(cyc.oil[d] * (1 + spread)); out.oilP90.push(cyc.oil[d] * (1 - spread));
      out.spmSafe.push(cyc.spmSafe[d]); out.floatMargin.push(cyc.margin[d]);
      out.sor.push(d > SOAK_END && cum[d] > 5 ? clamp(steam * BBL_PER_T_CWE / cum[d], 0, 99) : null);
    }
    return out;
  }

  /* ---- depth tracks ---- */

  profile() {
    const p = this._p, b = this._b, c = this._c, th = b.th, kt = this._kt;
    const prod = this._phase === 'PRODUCTION';
    const m = this.metrics();
    const level = m.fluidLevel;
    const out = { depth: [], Tfluid: [], Tformation: [], mu: [], pressure: [], rodStress: [], depositionTop: null, depositionBot: null };
    const bf = 1 - 0.128 * c.Gfl;
    // cumulative drag below depth z, walking up from the pump on a 10 m grid
    const cBelow = new Map();
    let acc = 0;
    for (let z = 1060; z >= 0; z -= 10) {
      const Tf = tFluid(z + 5, th.exc, b.Lr);
      const mu = Math.min(viscosityCp(Tf), MU_CAP_CP) * KVIS / 1000;
      const sec = SECT.find((s) => z + 5 >= s.top && z + 5 < s.bot) || SECT[2];
      acc += TAU * mu * 10 / sec.lnr;
      cBelow.set(z, acc);
    }
    for (let z = 0; z <= 1250; z += 10) {
      out.depth.push(z);
      const Tf = tFluid(z, th.exc, b.Lr);
      out.Tfluid.push(Tf); out.mu.push(viscosityCp(Tf));
      const halo = smooth((z - 1055) / 25) * (1 - smooth((z - 1165) / 25));
      out.Tformation.push(Tgeo(z) + 0.6 * th.exc * halo);
      out.pressure.push(z < level ? 3 : 3 + 0.0912 * (z - level));
      let sMax = 0;
      if (z < PUMP_DEPTH) {
        const sec = SECT.find((s) => z >= s.top && z < s.bot) || SECT[2];
        const wb = wBelow(z), cb = cBelow.get(Math.floor(z / 10) * 10) || 0;
        sMax = (wb * bf + c.Fo + wb * c.alpha + cb * c.vUp) / sec.A;
      }
      out.rodStress.push(fin(sMax));
    }
    if (prod && this._dep) { out.depositionTop = this._dep.top; out.depositionBot = this._dep.bot; }
    void p; void kt;
    return out;
  }
}

// Asphaltene deposition band: fluid cooler than the 62 C onset, above the pump.
function deposition(exc, Lr) {
  let bot = null;
  for (let z = PUMP_DEPTH; z >= 0; z -= 10) {
    if (tFluid(z, exc, Lr) < 62) { bot = z; break; }
  }
  if (bot === null) return { top: null, bot: null };
  return { top: Math.max(20, bot - 220), bot };
}
