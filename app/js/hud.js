// Glass HUD for the Well View: drive telemetry, the value card (with its cost anatomy), the
// steam-cycle ring, the two-tab advisor (pump now / next cycle recipe), the KPI row and the
// metric cards: cycle production vs history and plan, the dynamometer card, heat & pressure
// with depth, and rod & pump health drawn as pictograms. Live values come from the WellSim;
// anything the sim doesn't model yet comes from mock.js.
import { CYCLE } from './sim.js';
import { WELLBORE } from './rig.js';
import { derive, ROD, UNSEATS, PAST_CYCLES, PLAN, FLUID } from './mock.js';

const $ = (id) => document.getElementById(id);
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const C = { text: '#f3efe9', mute: 'rgba(240,232,222,0.55)', grid: 'rgba(255,255,255,0.07)', heat: '#f0a04b', blue: '#7cc4ff', ok: '#5fe39a', warn: '#ffc35a', crit: '#ff6b6b', inj: '#ff7a3d', violet: '#b69cff' };
const FONT = '500 10px Inter, sans-serif';

export const inr = (v) => {
  const a = Math.abs(v), s = v < 0 ? '−' : '';
  if (a >= 1e7) return `${s}₹${(a / 1e7).toFixed(2)} Cr`;
  if (a >= 1e5) return `${s}₹${(a / 1e5).toFixed(2)} L`;
  if (a >= 1e3) return `${s}₹${(a / 1e3).toFixed(1)}k`;
  return `${s}₹${a.toFixed(0)}`;
};
const pct = (v) => `${(v * 100).toFixed(0)}`;
const k1 = (v) => (v >= 1000 ? `${(v / 1000).toFixed(1)}k` : v.toFixed(0));
const phaseName = (p) => (p === 'INJECTION' ? 'Steam injection' : p === 'SOAK' ? 'Soak' : 'Production');
const hash = (i) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

function fit(canvas) {
  const dpr = Math.min(2, window.devicePixelRatio || 1);
  const w = canvas.clientWidth, h = canvas.clientHeight;
  if (!w || !h) return null;
  if (canvas.width !== Math.round(w * dpr) || canvas.height !== Math.round(h * dpr)) { canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr); }
  const g = canvas.getContext('2d');
  g.setTransform(dpr, 0, 0, dpr, 0, 0);
  g.clearRect(0, 0, w, h);
  return { g, w, h };
}

// fatigue colour ramp for rods: calm neutral → amber → red
function fatigueColor(f) {
  if (f < 0.45) return `rgba(240,232,222,${0.22 + f * 0.5})`;
  const t = clamp((f - 0.45) / 0.55, 0, 1);
  const r = 240 + (255 - 240) * t, g = 196 - 90 * t, b = 90 - 10 * t;
  return `rgb(${r | 0},${g | 0},${b | 0})`;
}

/* ------------------------------------------------------------------ KPI definitions */

const KPIS = [
  { id: 'oil', label: 'Oil rate', dot: C.heat, unit: 'BOPD', val: (m) => m.oilRate.toFixed(1), sub: (m) => `liquid ${m.liquidRate.toFixed(0)} bpd · WC ${pct(m.waterCut)}%`, bar: (m) => [m.oilRate / 80, C.heat],
    tip: (m) => `<b>Oil rate</b><br>${m.oilRate.toFixed(1)} barrels of oil per day at cycle day ${m.cycleDay.toFixed(0)}; water cut ${pct(m.waterCut)}%.<br><span class="mut">Falls as the heated zone cools and the crude thickens again.</span>` },
  { id: 'eff', label: 'Pump efficiency', dot: C.ok, unit: '%', val: (m) => pct(m.pumpEff), sub: (m) => `${m.bottleneck === 'PUMP' ? 'pump-limited' : 'reservoir-limited'} · ${m.pumpDisplacement.toFixed(0)} bpd disp.`, bar: (m) => [m.pumpEff, m.pumpEff < 0.5 ? C.warn : C.ok],
    tip: (m) => `<b>Volumetric pump efficiency</b><br>Liquid lifted ÷ plunger displacement (${m.liquidRate.toFixed(0)} of ${m.pumpDisplacement.toFixed(0)} bpd).<br><span class="mut">Currently ${m.bottleneck === 'PUMP' ? 'the pump' : 'the reservoir inflow'} is the bottleneck.</span>` },
  { id: 'fill', label: 'Pump fillage', dot: C.ok, unit: '%', val: (m) => pct(m.fillage), sub: (m) => `submergence ${m.submergence.toFixed(0)} m`, bar: (m) => [m.fillage, m.fillage < 0.7 ? C.warn : C.ok],
    tip: () => `<b>Pump fillage</b><br>How full the barrel gets each upstroke. Under ~70% the plunger slams into fluid (<i>fluid pound</i>).` },
  { id: 'float', label: 'Float margin', dot: C.ok, unit: '%', val: (m) => pct(m.floatMargin), sub: (m) => `safe below ${m.spmSafe.toFixed(1)} SPM`, bar: (m) => [clamp(m.floatMargin, 0, 1), m.floatMargin < 0 ? C.crit : m.floatMargin < 0.2 ? C.warn : C.ok],
    tip: (m) => `<b>Rod float margin</b><br>How much faster gravity can pull the rods down than the viscous crude holds them back. Negative means the rods lag the horsehead and the wire rope slackens.<br><span class="mut">Safe speed today: ${m.spmSafe.toFixed(1)} SPM.</span>` },
  { id: 'visc', label: 'Viscosity', dot: '#c98b5a', unit: 'cP', val: (m) => k1(m.viscosity), sub: () => `dead oil ${k1(FLUID.deadOilCp)} cP at ${FLUID.tRes} °C`, bar: (m) => [clamp(Math.log10(m.viscosity) / 4, 0, 1), '#c98b5a'],
    tip: (m) => `<b>Crude viscosity at the pump</b><br>${m.viscosity.toFixed(0)} cP. Baghewala ${FLUID.api}° API crude is ~${k1(FLUID.deadOilCp)} cP at reservoir temperature; steam heat thins it by orders of magnitude.` },
  { id: 'temp', label: 'Sandface T', dot: C.inj, unit: '°C', val: (m) => m.sandfaceT.toFixed(0), sub: (m) => `heated r ${m.heatedRadius.toFixed(1)} m · base ${FLUID.tRes} °C`, bar: (m) => [clamp((m.sandfaceT - 40) / 180, 0, 1), C.inj],
    tip: () => `<b>Sandface temperature</b><br>Formation temperature at the perforations; the reservoir baseline is ${FLUID.tRes} °C.` },
  { id: 'energy', label: 'Lift energy', dot: C.violet, unit: 'kWh/bbl', val: (m) => m.kwhPerBbl.toFixed(1), sub: (m) => `motor ${m.motorKw.toFixed(1)} kW`, bar: (m) => [clamp(m.kwhPerBbl / 20, 0, 1), C.violet],
    tip: () => `<b>Lift energy</b><br>Electricity spent per barrel of oil lifted.` },
  { id: 'sor', label: 'Steam–oil ratio', dot: '#e8e2d6', unit: '', val: (m) => (m.sor ? m.sor.toFixed(2) : '—'), sub: (m) => `${m.steamTons.toFixed(0)} t steam / cycle`, bar: (m) => [clamp(1 - (m.sor || 6) / 8, 0, 1), '#e8e2d6'],
    tip: () => `<b>Cumulative steam–oil ratio</b><br>Barrels of cold-water-equivalent steam per barrel of oil so far this cycle. Lower is better; under ~4 is economic.` },
  { id: 'co2', label: 'CO₂ intensity', dot: '#9fb0a0', unit: 'kg/bbl', val: (m) => (m.co2PerBbl ? m.co2PerBbl.toFixed(0) : '—'), sub: () => `steam + grid power`, bar: (m) => [clamp(m.co2PerBbl / 200, 0, 1), '#9fb0a0'],
    tip: () => `<b>CO₂ intensity</b><br>Gas burned for steam plus grid power for the pump, per barrel.` },
];

const TIPS = {
  sim: () => `<b>Simulated data</b><br>Every value on screen comes from Mantle's physics model and mock fixtures, not field telemetry yet.<br><span class="mut">Swap in historian feeds (production, CSS records, VFD/SRP logs) without changing the UI.</span>`,
  spm: (m, st) => `<b>Pumping speed</b><br>${(st?.spmActual ?? 0).toFixed(1)} strokes per minute (set ${m.spm.toFixed(1)}).<br><span class="mut">The unit parks at top of stroke during injection and soak.</span>`,
  stroke: (m) => `<b>Stroke length</b><br>${m.stroke.toFixed(2)} m polished-rod travel (crank hole 2 of 3).<br><span class="mut">Longer stroke at lower SPM lifts the same fluid with fewer impacts.</span>`,
  vfd: (m, st, d) => `<b>VFD output</b><br>${d.hz.toFixed(1)} Hz · speed profile shaped for the downstroke (kd ${m.kd.toFixed(2)}).`,
  amps: (m, st, d) => `<b>Motor current</b><br>${d.amps.toFixed(0)} A now, ${d.ampsAvg.toFixed(0)} A average · ${m.motorKw.toFixed(1)} kW.`,
  load: (m) => `<b>Polished-rod load</b><br>Live load at the carrier bar. This stroke: peak ${m.pprl.toFixed(0)} kN, minimum ${m.mprl.toFixed(0)} kN.`,
  net: () => `<b>Net value today</b><br>Oil revenue less steam, power, maintenance and chemicals. Hover to see the cost anatomy.<br><span class="mut">₹6,000/bbl · ₹2,800/t steam · ₹8/kWh (planning prices)</span>`,
  battery: (m) => `<b>Thermal battery</b><br>${pct(m.thermalBattery)}% of the injected heat is still in the rock near the well.`,
  cum: (m, st, d) => `<b>Cumulative oil, cycle 4</b><br>${Math.round(m.cumOil).toLocaleString()} bbl so far.<br><span class="mut">Recovery to date ${(d.recovery * 100).toFixed(2)}% of drainage-area OOIP (cycles 1–4).</span>`,
  cutoff: () => `<b>Days to economic cut-off</b><br>When the daily margin drops below the best whole-cycle average, re-steam.`,
};

/* ------------------------------------------------------------------ HUD */

export class Hud {
  constructor({ getSim }) {
    this.getSim = getSim;
    this.m = null; this.d = null;
    this.series = null; this.seriesKey = '';
    this.dyno = null; this.dynoKey = '';
    this.profile = null; this.profileKey = '';
    this.buildKpis();
    this.buildHealth();
    this.setupTooltips();
    this.setupAdvisor();
    this.baseNet = null;
    this.strokeCount = 0; this.lastTheta = null;
  }

  buildKpis() {
    $('kpis').innerHTML = KPIS.map((k) => `<div class="kpi" data-kpi="${k.id}"><label><i style="background:${k.dot}"></i>${k.label}</label><div class="kv"><span>—</span><small>${k.unit}</small></div><div class="ksub"></div><div class="kbar"><b></b></div></div>`).join('');
    this.kpiEls = KPIS.map((k) => {
      const el = document.querySelector(`[data-kpi="${k.id}"]`);
      return { k, v: el.querySelector('.kv span'), s: el.querySelector('.ksub'), b: el.querySelector('.kbar b') };
    });
  }

  buildHealth() {
    // one glyph per rod, surface → pump, 14 across; a hairline gap where the taper changes
    const rodDepth = (i) => (i + 0.5) * ROD.lengthM;
    const taperOf = (z) => ROD.tapers.findIndex((t) => z <= t.to);
    let html = '';
    for (let i = 0; i < ROD.count; i++) {
      const failed = ROD.failures.find((f) => f.rod === i + 1);
      html += `<i class="rod${failed ? ' failed' : ''}${taperOf(rodDepth(i)) !== taperOf(rodDepth(i + 1)) ? ' taper' : ''}" data-rod="${i}"></i>`;
    }
    $('rod-grid').innerHTML = html;
    this.rodEls = [...$('rod-grid').children];
    $('rods-sum').textContent = `${ROD.count} rods`;
    $('rods-note').innerHTML = `<span class="x">✕</span> ${ROD.failures.length} parted in 18 mo`;
    // strokes strip + month calendar
    $('strokes').innerHTML = Array.from({ length: 18 }, () => '<i class="stk"><b></b></i>').join('');
    this.strokeEls = [...$('strokes').children];
    $('months').innerHTML = UNSEATS.months.map((mo, i) => `<i class="mo${UNSEATS.events.includes(i) ? ' ev' : ''}" data-mo="${i}"><span>${mo[0]}</span></i>`).join('');
    $('uns-sum').textContent = `${UNSEATS.events.length} in 12 mo`;
  }

  setupTooltips() {
    const tip = $('tooltip');
    const show = (html, e) => { tip.innerHTML = html; tip.classList.add('show'); move(e); };
    const move = (e) => {
      const r = tip.getBoundingClientRect();
      let x = e.clientX, y = e.clientY;
      if (x + 14 + r.width > innerWidth - 8) x -= r.width + 28;
      if (y + 14 + r.height > innerHeight - 8) y -= r.height + 28;
      tip.style.left = `${x}px`; tip.style.top = `${y}px`;
    };
    const hide = () => tip.classList.remove('show');
    this.showTip = show; this.hideTip = hide;
    const bind = (el, fn) => {
      el.addEventListener('pointerenter', (e) => this.m && show(fn(this.m, this.getSim()?.state, this.d), e));
      el.addEventListener('pointermove', move);
      el.addEventListener('pointerleave', hide);
    };
    document.querySelectorAll('#ui [data-tip]').forEach((el) => TIPS[el.dataset.tip] && bind(el, TIPS[el.dataset.tip]));
    this.kpiEls.forEach(({ k }) => bind(document.querySelector(`[data-kpi="${k.id}"]`), k.tip));
    // rods
    $('rod-grid').addEventListener('pointermove', (e) => {
      const el = e.target.closest('.rod'); if (!el || !this.m) { hide(); return; }
      const i = +el.dataset.rod, z = (i + 0.5) * ROD.lengthM, t = ROD.tapers.find((tt) => z <= tt.to) || ROD.tapers[ROD.tapers.length - 1];
      const f = ROD.failures.find((ff) => ff.rod === i + 1);
      const fat = this.rodFatigue?.[i] ?? 0;
      show(f ? `<b>Rod #${i + 1} · ${f.size} · parted</b><br>${f.mode}, ${f.date}<br><span class="mut">${z.toFixed(0)} m · ${f.cause}</span>`
        : `<b>Rod #${i + 1}</b> <span class="mut">· ${t.label} · ${z.toFixed(0)} m</span><br>Fatigue use ${(fat * 100).toFixed(0)}% of the Goodman limit`, e);
    });
    $('rod-grid').addEventListener('pointerleave', hide);
    $('months').addEventListener('pointermove', (e) => {
      const el = e.target.closest('.mo'); if (!el) { hide(); return; }
      const i = +el.dataset.mo, ev = UNSEATS.events.includes(i);
      show(`<b>${UNSEATS.months[i]}</b><br>${ev ? 'Pump unseated: pulled rods and reseated (1 day lost)' : 'No unseat'}`, e);
    });
    $('months').addEventListener('pointerleave', hide);
    $('strokes').addEventListener('pointerenter', (e) => this.d && show(`<b>Last 18 strokes</b><br>A burst marks a stroke where the plunger hit fluid (fluid pound).<br><span class="mut">Impact speed ≈ ${this.d.impactVel.toFixed(2)} m/s · ${k1(this.d.impactsDay)} impacts/day</span>`, e));
    $('strokes').addEventListener('pointerleave', hide);
    // chart hovers
    const cyc = $('c-cycle');
    cyc.addEventListener('pointermove', (e) => {
      if (!this.series || !this.cycLayout) return;
      const r = cyc.getBoundingClientRect(), L = this.cycLayout;
      const day = clamp(Math.round((e.clientX - r.left - L.x0) / (L.x1 - L.x0) * CYCLE.days), 0, CYCLE.days);
      const s = this.series;
      this.hoverDay = day;
      const ph = day < CYCLE.injEnd ? 'Steam injection' : day < CYCLE.soakEnd ? 'Soak' : 'Production';
      const hist = PAST_CYCLES.map((c) => `C${c.n} ${(s.oil[day] * c.k).toFixed(0)}`).join(' · ');
      show(`<b>Day ${day}</b> <span class="mut">· ${ph}</span><br>Oil ${s.oil[day].toFixed(1)} BOPD <span class="mut">(P90–P10 ${s.oilP90[day].toFixed(0)}–${s.oilP10[day].toFixed(0)})</span><br><span class="mut">Earlier cycles: ${hist}</span><br>Sandface ${s.T[day].toFixed(0)} °C · ${k1(s.mu[day])} cP`, e);
    });
    cyc.addEventListener('pointerleave', () => { this.hoverDay = null; hide(); });
    cyc.addEventListener('click', () => this.hoverDay != null && this.onPickDay?.(this.hoverDay));
    cyc.style.cursor = 'pointer';
  }

  setupAdvisor() {
    const tabs = $('adv-tabs');
    tabs.querySelectorAll('button').forEach((b) => (b.onclick = () => {
      tabs.querySelectorAll('button').forEach((x) => x.classList.toggle('active', x === b));
      document.querySelectorAll('.adv-body').forEach((el) => (el.hidden = el.dataset.body !== b.dataset.tab));
    }));
    $('plan-apply').onclick = () => { $('plan-apply').textContent = 'Scheduled · cycle 5 starts day 120'; $('plan-apply').disabled = true; };
  }

  /* per metrics tick (4 Hz) */
  update(m) {
    this.m = m;
    const sim = this.getSim();
    const st = sim.state;
    const d = (this.d = derive(m, st));
    const prod = m.phase === 'PRODUCTION';
    $('t-spm').textContent = st.spmActual.toFixed(1);
    $('t-stroke').textContent = m.stroke.toFixed(2);
    $('phase-sub').textContent = phaseName(m.phase);
    const dot = $('live-dot');
    dot.classList.toggle('steam', m.phase === 'INJECTION'); dot.classList.toggle('soak', m.phase === 'SOAK');

    // value + cost anatomy
    $('v-net').textContent = inr(m.netPerDay);
    const dl = $('v-delta');
    if (!prod) { dl.textContent = m.phase === 'INJECTION' ? 'steaming' : 'soaking'; dl.className = 'delta'; }
    else { dl.textContent = d.cost.costBbl ? `₹${k1(d.cost.costBbl)}/bbl cost` : '—'; dl.className = 'delta'; }
    const c = d.cost, parts = [['Steam', c.steamDay, C.inj], ['Power', c.powerDay, C.violet], ['Maintenance', c.maintDay, C.crit], ['Chemicals', c.chemDay, 'rgba(240,232,222,0.5)']];
    $('c-bbl').textContent = c.costBbl ? `₹${Math.round(c.costBbl).toLocaleString()} / bbl` : 'not producing';
    $('c-bar').innerHTML = parts.map(([, v, col]) => `<i style="flex:${v};background:${col}"></i>`).join('');
    $('c-rows').innerHTML = parts.map(([l, v, col]) => `<span><i style="background:${col}"></i>${l}<b>${inr(v)}</b></span>`).join('') + `<span class="tot">Revenue<b>${inr(prod ? m.oilRate * 6000 : 0)}</b></span>`;

    // cycle panel
    const prodLen = CYCLE.days - CYCLE.soakEnd;
    $('cycle-sum').textContent = `Day ${m.cycleDay.toFixed(0)} / ${CYCLE.days}`;
    $('ring-phase').textContent = phaseName(m.phase);
    $('ring-day').textContent = m.cycleDay.toFixed(0);
    $('ring-sub').textContent = m.phase === 'INJECTION' ? `day ${m.dayInPhase.toFixed(0)} of ${CYCLE.injEnd}` : m.phase === 'SOAK' ? `day ${m.dayInPhase.toFixed(0)} of ${CYCLE.soakEnd - CYCLE.injEnd}` : `day ${m.dayInPhase.toFixed(0)} of ${prodLen}`;
    $('s-battery').textContent = `${pct(m.thermalBattery)}%`;
    $('s-cum').textContent = prod ? k1(m.cumOil) : '—';
    $('s-cutoff').textContent = prod ? (m.daysToCutoff > 0 ? `${m.daysToCutoff.toFixed(0)} d` : 'now') : '—';
    this.drawRing(m);

    this.updateAdvisor(m, d);

    for (const { k, v, s, b } of this.kpiEls) {
      v.textContent = k.val(m); s.textContent = k.sub(m);
      const [f, col] = k.bar(m);
      b.style.width = `${clamp(f, 0, 1) * 100}%`; b.style.background = col;
    }

    // cached curve sets
    const sk = `${m.spm.toFixed(2)}|${m.kd}`;
    if (sk !== this.seriesKey) { this.series = sim.series(); this.seriesKey = sk; }
    const dk = `${m.spm.toFixed(2)}|${m.kd}|${m.cycleDay.toFixed(1)}`;
    if (dk !== this.dynoKey) { this.dyno = prod ? sim.dynoCard(160) : null; this.dynoKey = dk; }
    const pk = `${m.cycleDay.toFixed(1)}|${m.spm.toFixed(2)}`;
    if (pk !== this.profileKey) { this.profile = sim.profile(); this.profileKey = pk; }
    $('dyno-cls').textContent = this.dyno ? `${this.dyno.cls} · ${pct(this.dyno.clsConf)}%` : 'unit parked';
    $('dyno-cls').style.color = !this.dyno ? C.mute : this.dyno.cls === 'NORMAL' ? C.ok : this.dyno.cls === 'ROD FLOAT RISK' ? C.crit : C.warn;
    $('dyno-torque').innerHTML = prod ? `gearbox torque <b style="color:${m.torquePct > 1 ? C.crit : m.torquePct > 0.85 ? C.warn : C.text}">${pct(m.torquePct)}%</b>` : '';
    this.drawCycle(m); this.drawProfile(m, d);
    this.updateHealth(m, d);
  }

  updateAdvisor(m, d) {
    const r = m.recommendation;
    $('adv-title').textContent = r.title;
    $('adv-detail').textContent = r.detail;
    const chips = [];
    const chip = (v, label, goodIfUp) => { if (Math.abs(v) < 0.005) return; const good = goodIfUp ? v > 0 : v < 0; chips.push(`<span class="${good ? 'good' : 'bad'}">${v > 0 ? '+' : '−'}${Math.abs(v * 100).toFixed(0)}% ${label}</span>`); };
    chip(r.deltas.oil, 'oil', true); chip(r.deltas.float, 'float', true); chip(r.deltas.energy, 'kWh/bbl', false);
    if (m.phase === 'PRODUCTION' && d.impactsDay > 50) chips.push(`<span class="good">${d.impactsMantle < 50 ? 'no fluid pound' : `−${pct(1 - d.impactsMantle / d.impactsDay)}% impacts`}</span>`);
    $('adv-deltas').innerHTML = chips.join('');
    const hz2 = r.spm * 50 / 9;
    $('adv-drive').innerHTML = m.phase === 'PRODUCTION'
      ? `<span><label>VFD</label><div>${d.hz.toFixed(1)}<i>→</i><b>${hz2.toFixed(1)}</b> Hz</div></span><span><label>Speed profile</label><div>${m.kd.toFixed(2)}<i>→</i><b>${r.kd.toFixed(2)}</b></div></span><span><label>Stroke</label><div><b>${m.stroke.toFixed(2)}</b> m</div></span>`
      : '';
    const can = m.phase === 'PRODUCTION' && (Math.abs(r.spm - m.spm) > 0.05 || Math.abs(r.kd - m.kd) > 0.001);
    $('adv-apply').disabled = !can;
    $('adv-apply').textContent = can ? `Apply · ${r.spm.toFixed(1)} SPM · ${hz2.toFixed(0)} Hz` : 'Settings optimal';

    // next-cycle recipe: today's practice (hollow) vs Mantle (solid) on each lever's range
    const cut = Math.round(Math.min(CYCLE.days, m.phase === 'PRODUCTION' ? m.cycleDay + m.daysToCutoff : 96));
    PLAN.mantle.cutoff = cut;
    const L = [
      ['Steam volume', 'steam', 't', 0], ['Injection pressure', 'pInj', 'MPa', 1], ['Soak time', 'soak', 'd', 0], ['Production cut-off', 'cutoff', 'day', 0],
    ];
    $('levers').innerHTML = L.map(([label, key, unit, dp]) => {
      const [lo, hi] = PLAN.ranges[key], a = PLAN.practice[key], b = PLAN.mantle[key];
      const X = (v) => clamp((v - lo) / (hi - lo), 0, 1) * 100;
      const l = Math.min(X(a), X(b)), w = Math.abs(X(b) - X(a));
      return `<div class="lever"><div class="lv-top"><span>${label}</span><em>${a.toFixed(dp)} <i>→</i> <b>${b.toFixed(dp)}</b> ${unit}</em></div>
        <div class="lv-track"><i class="lv-span" style="left:${l}%;width:${w}%"></i><i class="lv-ghost" style="left:${X(a)}%"></i><i class="lv-dot" style="left:${X(b)}%"></i></div></div>`;
    }).join('');
    const joint = PLAN.jointShare / PLAN.inrPerCycle;
    $('dividend').innerHTML = `<div class="dv-top"><b>+${inr(PLAN.inrPerCycle)}</b><span>per cycle vs today</span></div>
      <div class="dv-bars"><div><label>Today</label><i style="width:${100 / (1 + PLAN.oilLift) - 0.5}%"></i></div><div><label>Mantle</label><i style="width:${100 * (1 - joint * PLAN.oilLift)}%"></i><i class="joint" style="width:${100 * joint * PLAN.oilLift + 0.6}%"></i></div></div>
      <div class="dv-sub">+${(PLAN.oilLift * 100).toFixed(0)}% oil · SOR ${PLAN.sor[0]} → ${PLAN.sor[1]} · <span class="jt">${inr(PLAN.jointShare)}</span> only from tuning steam &amp; pump together</div>`;
  }

  updateHealth(m, d) {
    const prod = m.phase === 'PRODUCTION';
    // rod fatigue by depth, scaled so the worst rod reads the string's Goodman ratio
    const p = this.profile;
    if (p && this.rodKey !== this.profileKey) {
      this.rodKey = this.profileKey;
      const maxS = Math.max(...p.rodStress, 1e-9);
      this.rodFatigue = this.rodEls.map((_, i) => {
        const z = (i + 0.5) * ROD.lengthM, j = clamp(Math.round(z / 10), 0, p.rodStress.length - 1);
        return m.goodman * (p.rodStress[j] / maxS);
      });
      this.rodEls.forEach((el, i) => { if (!el.classList.contains('failed')) el.style.background = fatigueColor(this.rodFatigue[i]); });
    }
    $('health-sum').innerHTML = `MTBF <b>${ROD.mtbfDays} d</b> <i>→</i> ${ROD.mtbfMantle} d`;
    const worst = Math.max(...(this.rodFatigue || [0]));
    $('rods-sum').textContent = `Goodman ${worst.toFixed(2)}`;
    $('imp-sum').textContent = prod ? `${k1(d.impactsDay)}/day` : 'parked';
    $('imp-note').innerHTML = prod ? (d.impactsDay > 50 ? (d.impactsMantle < 50 ? `<b>none</b> at ${m.recommendation.spm.toFixed(1)} SPM` : `<b>${k1(d.impactsMantle)}/day</b> at ${m.recommendation.spm.toFixed(1)} SPM`) : 'no fluid pound') : '—';
    $('uns-note').innerHTML = `uplift margin <b>${d.upliftMargin.toFixed(1)}×</b> · 30-day risk <b class="${d.unseatRisk > 0.25 ? 'w' : ''}">${pct(d.unseatRisk)}%</b>`;
    // alerts: one line in the card, a dot on the drawer tab
    const bad = m.alerts.filter((a) => a.level !== 'ok');
    const lc = { ok: C.ok, warn: C.warn, crit: C.crit };
    const top = bad.find((a) => a.level === 'crit') || bad[0] || m.alerts[0];
    $('alert-line').innerHTML = `<i style="background:${lc[top.level]}"></i><span>${top.text}</span>${bad.length > 1 ? `<em>+${bad.length - 1}</em>` : ''}`;
    $('alert-line').title = m.alerts.map((a) => a.text).join('\n');
    $('tab-alert').hidden = !bad.length;
    $('tab-alert').style.background = bad.some((a) => a.level === 'crit') ? C.crit : C.warn;
  }

  /* per frame: live bits */
  frame() {
    const sim = this.getSim();
    if (!sim || !this.m) return;
    const st = sim.state, m = this.m, d = this.d;
    $('t-load').textContent = st.load.toFixed(0);
    const hz = st.spmActual * 50 / 9;
    $('t-hz').textContent = hz.toFixed(1);
    const lf = m.pprl > 0 ? clamp(st.load / m.pprl, 0, 1.2) : 0;
    $('t-amps').textContent = m.phase === 'PRODUCTION' ? (d.ampsAvg * (0.55 + 0.9 * lf)).toFixed(0) : '0';
    // stroke counter drives the impact strip: a new glyph per completed stroke
    if (this.lastTheta != null && st.theta < this.lastTheta - 1) this.strokeCount++;
    this.lastTheta = st.theta;
    if (this.strokeCount !== this.drawnStrokes && d) {
      this.drawnStrokes = this.strokeCount;
      const pound = m.phase === 'PRODUCTION' ? clamp((0.85 - m.fillage) / 0.35, 0, 1) : 0;
      this.strokeEls.forEach((el, i) => {
        const n = this.strokeCount - (this.strokeEls.length - 1 - i);
        const hit = hash(n) < pound;
        el.classList.toggle('hit', hit);
        el.style.setProperty('--sev', (0.55 + hash(n + 7) * 0.45 * d.impactVel).toFixed(2));
        el.classList.toggle('now', i === this.strokeEls.length - 1);
      });
    }
    if (!document.getElementById('metrics').classList.contains('open')) return;
    this.drawDyno(st);
  }

  drawRing(m) {
    const cv = $('c-ring'), f = fit(cv);
    if (!f) return;
    const { g, w, h } = f, cx = w / 2, cy = h / 2, R = w / 2 - 8;
    const a0 = -Math.PI / 2, A = (d) => a0 + (d / CYCLE.days) * Math.PI * 2;
    const arc = (d0, d1, col, lw, r = R) => { g.beginPath(); g.arc(cx, cy, r, A(d0), A(d1)); g.strokeStyle = col; g.lineWidth = lw; g.lineCap = 'butt'; g.stroke(); };
    arc(0, CYCLE.injEnd - 0.6, 'rgba(255,122,61,0.28)', 6);
    arc(CYCLE.injEnd, CYCLE.soakEnd - 0.6, 'rgba(255,195,90,0.28)', 6);
    arc(CYCLE.soakEnd, CYCLE.days - 0.6, 'rgba(255,255,255,0.12)', 6);
    const d = m.cycleDay;
    const seg = (s0, s1, col) => { if (d > s0) arc(s0, Math.min(d, s1 - 0.6), col, 6); };
    seg(0, CYCLE.injEnd, C.inj); seg(CYCLE.injEnd, CYCLE.soakEnd, C.warn); seg(CYCLE.soakEnd, CYCLE.days, '#f3efe9');
    if (m.phase === 'PRODUCTION') {
      const cd = Math.min(CYCLE.days, d + m.daysToCutoff), a = A(cd);
      g.beginPath(); g.moveTo(cx + Math.cos(a) * (R - 9), cy + Math.sin(a) * (R - 9)); g.lineTo(cx + Math.cos(a) * (R + 5), cy + Math.sin(a) * (R + 5));
      g.strokeStyle = C.ok; g.lineWidth = 2; g.stroke();
    }
    arc(0, CYCLE.days * m.thermalBattery, 'rgba(240,160,75,0.55)', 2, R - 12);
    const a = A(d);
    g.beginPath(); g.arc(cx + Math.cos(a) * R, cy + Math.sin(a) * R, 5, 0, Math.PI * 2); g.fillStyle = '#fff'; g.fill();
  }

  drawCycle(m) {
    const f = fit($('c-cycle'));
    if (!f || !this.series) return;
    const { g, w, h } = f, s = this.series;
    const x0 = 30, x1 = w - 30, y0 = 8, y1 = h - 16;
    this.cycLayout = { x0, x1 };
    const X = (d) => x0 + (d / CYCLE.days) * (x1 - x0);
    const oMax = Math.max(20, ...s.oilP10.map((v) => v * PAST_CYCLES[0].k)) * 1.04;
    const Y = (o) => y1 - (o / oMax) * (y1 - y0);
    const YT = (t) => y1 - ((t - 40) / 220) * (y1 - y0);
    g.fillStyle = 'rgba(255,122,61,0.1)'; g.fillRect(X(0), y0, X(CYCLE.injEnd) - X(0), y1 - y0);
    g.fillStyle = 'rgba(255,195,90,0.08)'; g.fillRect(X(CYCLE.injEnd), y0, X(CYCLE.soakEnd) - X(CYCLE.injEnd), y1 - y0);
    g.font = FONT; g.fillStyle = C.mute; g.textAlign = 'center';
    g.fillText('STEAM', (X(0) + X(CYCLE.injEnd)) / 2, y0 + 11);
    g.strokeStyle = C.grid; g.lineWidth = 1;
    for (let o = 0; o <= oMax; o += 20) { g.beginPath(); g.moveTo(x0, Y(o)); g.lineTo(x1, Y(o)); g.stroke(); g.textAlign = 'right'; g.fillText(o, x0 - 5, Y(o) + 3); }
    g.textAlign = 'center';
    for (let d = 0; d <= CYCLE.days; d += 20) g.fillText(d, X(d), h - 3);
    g.textAlign = 'left'; g.fillStyle = 'rgba(240,160,75,0.7)';
    for (const t of [100, 200]) g.fillText(`${t}°`, x1 + 4, YT(t) + 3);
    const path = (fn, from = 0, to = CYCLE.days) => { g.beginPath(); let first = true; s.day.forEach((d, i) => { if (d < from || d > to) return; const y = fn(i); first ? g.moveTo(X(d), y) : g.lineTo(X(d), y); first = false; }); };
    // earlier cycles: the same well a little stronger each time back
    PAST_CYCLES.forEach((c, n) => { path((i) => Y(s.oil[i] * c.k), CYCLE.soakEnd); g.strokeStyle = `rgba(255,255,255,${0.1 + n * 0.04})`; g.lineWidth = 1; g.stroke(); });
    // P10–P90 band
    g.beginPath();
    s.day.forEach((d, i) => (i ? g.lineTo(X(d), Y(s.oilP10[i])) : g.moveTo(X(d), Y(s.oilP10[i]))));
    for (let i = s.day.length - 1; i >= 0; i--) g.lineTo(X(s.day[i]), Y(s.oilP90[i]));
    g.closePath(); g.fillStyle = 'rgba(255,255,255,0.07)'; g.fill();
    path((i) => YT(s.T[i])); g.setLineDash([4, 3]); g.strokeStyle = 'rgba(240,160,75,0.75)'; g.lineWidth = 1.2; g.stroke(); g.setLineDash([]);
    // Mantle plan for the same cycle: longer soak, more steam, earlier cut-off
    const shift = PLAN.mantle.soak - PLAN.practice.soak, cut = PLAN.mantle.cutoff || 96;
    g.beginPath(); let first = true;
    for (let d = CYCLE.soakEnd + shift; d <= cut; d++) { const v = s.oil[d - shift] * (1 + PLAN.oilLift * 1.4); first ? g.moveTo(X(d), Y(v)) : g.lineTo(X(d), Y(v)); first = false; }
    g.setLineDash([5, 4]); g.strokeStyle = 'rgba(95,227,154,0.85)'; g.lineWidth = 1.6; g.stroke(); g.setLineDash([]);
    g.fillStyle = C.ok; g.beginPath(); g.arc(X(cut), Y(s.oil[cut - shift] * (1 + PLAN.oilLift * 1.4)), 3, 0, 7); g.fill();
    // this cycle
    path((i) => Y(s.oil[i])); g.strokeStyle = 'rgba(255,255,255,0.35)'; g.lineWidth = 1.6; g.stroke();
    path((i) => Y(s.oil[i]), 0, Math.ceil(m.cycleDay)); g.strokeStyle = '#fff'; g.lineWidth = 2; g.stroke();
    if (m.phase === 'PRODUCTION') {
      const cd = Math.min(CYCLE.days, m.cycleDay + m.daysToCutoff);
      g.setLineDash([3, 3]); g.strokeStyle = 'rgba(95,227,154,0.5)'; g.beginPath(); g.moveTo(X(cd), y0); g.lineTo(X(cd), y1); g.stroke(); g.setLineDash([]);
      g.fillStyle = C.ok; g.textAlign = cd > 100 ? 'right' : 'left'; g.fillText('cut-off', X(cd) + (cd > 100 ? -4 : 4), y0 + 11);
    }
    const di = clamp(Math.round(m.cycleDay), 0, CYCLE.days);
    g.strokeStyle = 'rgba(255,255,255,0.5)'; g.beginPath(); g.moveTo(X(m.cycleDay), y0); g.lineTo(X(m.cycleDay), y1); g.stroke();
    g.beginPath(); g.arc(X(m.cycleDay), Y(m.oilRate || s.oil[di]), 4, 0, Math.PI * 2); g.fillStyle = '#fff'; g.fill();
    if (this.hoverDay != null) { g.strokeStyle = 'rgba(255,255,255,0.25)'; g.beginPath(); g.moveTo(X(this.hoverDay), y0); g.lineTo(X(this.hoverDay), y1); g.stroke(); }
  }

  drawDyno(st) {
    const f = fit($('c-dyno'));
    if (!f) return;
    const { g, w, h } = f, d = this.dyno, m = this.m;
    const x0 = 30, x1 = w - 34, y0 = 6, y1 = h - 14;
    if (!d) {
      g.font = FONT; g.fillStyle = C.mute; g.textAlign = 'center';
      g.fillText(m.phase === 'INJECTION' ? 'Unit parked while steam is injected' : 'Unit parked during the soak', w / 2, h / 2);
      return;
    }
    const fMin = Math.min(0, d.fMin), fMax = Math.max(d.fMax, m.pprl) * 1.08;
    const X = (x) => x0 + (x / d.xMax) * (x1 - x0), Y = (v) => y1 - ((v - fMin) / (fMax - fMin)) * (y1 - y0);
    g.strokeStyle = C.grid; g.lineWidth = 1; g.font = FONT; g.fillStyle = C.mute;
    const step = fMax > 120 ? 40 : 20;
    for (let v = 0; v <= fMax; v += step) { g.beginPath(); g.moveTo(x0, Y(v)); g.lineTo(x1, Y(v)); g.stroke(); g.textAlign = 'right'; g.fillText(v, x0 - 5, Y(v) + 3); }
    g.textAlign = 'center'; g.fillText('stroke →', (x0 + x1) / 2, h - 2);
    // peak / minimum polished-rod load
    for (const [v, lbl] of [[m.pprl, 'PPRL'], [m.mprl, 'MPRL']]) {
      g.setLineDash([2, 3]); g.strokeStyle = 'rgba(255,255,255,0.3)'; g.beginPath(); g.moveTo(x0, Y(v)); g.lineTo(x1, Y(v)); g.stroke(); g.setLineDash([]);
      g.textAlign = 'left'; g.fillStyle = C.mute; g.fillText(lbl, x1 + 4, Y(v) + 3);
    }
    const loop = (pts, col, lw, fill) => {
      g.beginPath(); pts.forEach((p, i) => (i ? g.lineTo(X(p.x), Y(p.f)) : g.moveTo(X(p.x), Y(p.f)))); g.closePath();
      if (fill) { g.fillStyle = fill; g.fill(); }
      g.strokeStyle = col; g.lineWidth = lw; g.stroke();
    };
    loop(d.downhole, C.blue, 1.4, 'rgba(124,196,255,0.08)');
    loop(d.surface, '#fff', 1.8, 'rgba(255,255,255,0.05)');
    // impact: the steepest load drop on the downstroke of the pump card is where the plunger hits fluid
    if (m.fillage < 0.85) {
      let best = -1, drop = 0;
      const n = d.downhole.length;
      for (let i = Math.floor(n / 2); i < n - 1; i++) { const dd = d.downhole[i].f - d.downhole[i + 1].f; if (dd > drop) { drop = dd; best = i; } }
      if (best > 0) {
        const p = d.downhole[best], bx = X(p.x), by = Y(p.f);
        const pulse = 0.6 + 0.4 * Math.sin(performance.now() / 180);
        g.strokeStyle = `rgba(255,195,90,${pulse})`; g.lineWidth = 1.4;
        g.beginPath(); for (let k = 0; k < 8; k++) { const a = (k / 8) * Math.PI * 2, r0 = 4, r1 = k % 2 ? 7 : 10; g.moveTo(bx + Math.cos(a) * r0, by + Math.sin(a) * r0); g.lineTo(bx + Math.cos(a) * r1, by + Math.sin(a) * r1); } g.stroke();
      }
    }
    g.beginPath(); g.arc(X(clamp(st.rodPos, 0, d.xMax)), Y(st.load), 4, 0, Math.PI * 2); g.fillStyle = C.heat; g.fill();
    g.beginPath(); g.arc(X(clamp(st.rodPos, 0, d.xMax)), Y(st.load), 8, 0, Math.PI * 2); g.strokeStyle = 'rgba(240,160,75,0.4)'; g.lineWidth = 1; g.stroke();
  }

  drawProfile(m, d) {
    const f = fit($('c-profile'));
    if (!f || !this.profile) return;
    const { g, w, h } = f, p = this.profile;
    const x0 = 26, x1 = w - 6, y0 = 14, y1 = h - 14;
    const Y = (z) => y0 + (z / 1250) * (y1 - y0), X = (t) => x0 + ((t - 20) / 220) * (x1 - x0), XP = (mpa) => x0 + (mpa / 6) * (x1 - x0);
    g.font = FONT; g.fillStyle = C.mute; g.strokeStyle = C.grid;
    for (const z of [0, 500, 1000]) { g.beginPath(); g.moveTo(x0, Y(z)); g.lineTo(x1, Y(z)); g.stroke(); g.textAlign = 'right'; g.fillText(z ? `${z / 1000}k` : '0', x0 - 4, Y(z) + 3); }
    g.textAlign = 'center';
    for (const t of [50, 150]) g.fillText(`${t}°`, X(t), h - 2);
    g.fillStyle = 'rgba(124,196,255,0.75)';
    for (const mp of [2, 4]) g.fillText(`${mp} MPa`, XP(mp), 9);
    g.fillStyle = 'rgba(240,160,75,0.08)'; g.fillRect(x0, Y(1080), x1 - x0, Y(1160) - Y(1080));
    if (p.depositionTop != null) { g.fillStyle = 'rgba(255,195,90,0.14)'; g.fillRect(x0, Y(p.depositionTop), x1 - x0, Y(p.depositionBot) - Y(p.depositionTop)); }
    const line = (arr, fx, col, lw, dash) => { g.beginPath(); arr.forEach((t, i) => (i ? g.lineTo(fx(t), Y(p.depth[i])) : g.moveTo(fx(t), Y(p.depth[i])))); g.setLineDash(dash || []); g.strokeStyle = col; g.lineWidth = lw; g.stroke(); g.setLineDash([]); };
    line(p.Tformation, X, 'rgba(255,255,255,0.35)', 1.1, [3, 3]);
    line(p.pressure.map((b) => b / 10), XP, C.blue, 1.5);
    line(p.Tfluid, X, C.heat, 1.8);
    // reservoir pressure + fluid level + pump
    g.fillStyle = C.blue; g.beginPath(); g.arc(XP(d.pRes), Y(1120), 3, 0, 7); g.fill();
    g.textAlign = 'left'; g.fillText(`Pr ${d.pRes} MPa`, XP(d.pRes) + 6, Y(1120) + 3);
    g.strokeStyle = 'rgba(255,255,255,0.3)'; g.setLineDash([2, 3]); g.beginPath(); g.moveTo(x0, Y(m.fluidLevel)); g.lineTo(x1, Y(m.fluidLevel)); g.stroke(); g.setLineDash([]);
    g.fillStyle = C.mute; g.textAlign = 'right'; g.fillText('fluid level', x1, Y(m.fluidLevel) - 3);
    g.fillStyle = '#fff'; g.fillRect(x0 + 2, Y(WELLBORE.pumpTop) - 2, 8, 4);
    g.textAlign = 'left'; g.fillStyle = C.mute; g.fillText(`PIP ${d.pip.toFixed(1)}`, x0 + 13, Y(WELLBORE.pumpTop) + 3);
  }
}
