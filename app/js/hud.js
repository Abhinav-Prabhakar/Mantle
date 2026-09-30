// Glass HUD for the Well View: drive telemetry, the value card (with its cost anatomy), the
// steam-cycle ring, the two-tab advisor (pump now / next-cycle recipe), the KPI row and the
// metric cards: cycle production vs history and plan, the dynamometer card, heat & pressure
// with depth, and rod & pump health drawn as pictograms.
// Every number comes from the Mantle API (via the RemoteTwin). Per-frame telemetry comes from the
// live WebSocket. Nothing is invented locally: when the API hasn't answered, values read "—".
import { CYCLE } from './sim.js';
import { WELLBORE } from './rig.js';
import { derived, fluid, health, plan, pastCycles, planCurve, provenance } from './twin-data.js';

const $ = (id) => document.getElementById(id);
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const C = { text: '#f3efe9', mute: 'rgba(240,232,222,0.55)', grid: 'rgba(255,255,255,0.07)', heat: '#f0a04b', blue: '#7cc4ff', ok: '#5fe39a', warn: '#ffc35a', crit: '#ff6b6b', inj: '#ff7a3d', violet: '#b69cff' };
const FONT = '500 10px Inter, sans-serif';
const DASH = '—';
const num = (v) => typeof v === 'number' && Number.isFinite(v);

export const inr = (v, sym = true) => {
  if (!num(v)) return DASH;
  const a = Math.abs(v), s = v < 0 ? '−' : '', p = sym ? '₹' : '';
  if (a >= 1e7) return `${s}${p}${(a / 1e7).toFixed(2)} Cr`;
  if (a >= 1e5) return `${s}${p}${(a / 1e5).toFixed(2)} L`;
  if (a >= 1e3) return `${s}${p}${(a / 1e3).toFixed(1)}k`;
  return `${s}${p}${a.toFixed(0)}`;
};
const pct = (v) => (num(v) ? `${(v * 100).toFixed(0)}` : DASH);
const k1 = (v) => (num(v) ? (v >= 1000 ? `${(v / 1000).toFixed(1)}k` : v.toFixed(0)) : DASH);
const fx = (v, d = 1) => (num(v) ? v.toFixed(d) : DASH);
const phaseName = (p) => (p === 'INJECTION' ? 'Steam injection' : p === 'SOAK' ? 'Soak' : 'Production');

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
function emptyCanvas(canvas, text) {
  const f = fit(canvas);
  if (!f) return;
  f.g.font = FONT; f.g.fillStyle = C.mute; f.g.textAlign = 'center';
  f.g.fillText(text, f.w / 2, f.h / 2);
}

// fatigue colour ramp for rods: calm neutral → amber → red
function fatigueColor(f) {
  if (!num(f)) return 'rgba(240,232,222,0.12)';
  if (f < 0.45) return `rgba(240,232,222,${0.22 + f * 0.5})`;
  const t = clamp((f - 0.45) / 0.55, 0, 1);
  const r = 240 + (255 - 240) * t, g = 196 - 90 * t, b = 90 - 10 * t;
  return `rgb(${r | 0},${g | 0},${b | 0})`;
}

/* ------------------------------------------------------------------ KPI definitions (ctx = { fluid }) */

const KPIS = [
  { id: 'oil', label: 'Oil rate', dot: C.heat, unit: 'BOPD', val: (m) => fx(m.oilRate), sub: (m) => `liquid ${fx(m.liquidRate, 0)} bpd · WC ${pct(m.waterCut)}%`, bar: (m) => [m.oilRate / 80, C.heat],
    tip: (m) => `<b>Oil rate</b><br>${fx(m.oilRate)} barrels of oil per day at cycle day ${fx(m.cycleDay, 0)}; water cut ${pct(m.waterCut)}%.<br><span class="mut">Falls as the heated zone cools and the crude thickens again.</span>` },
  { id: 'eff', label: 'Pump efficiency', dot: C.ok, unit: '%', val: (m) => pct(m.pumpEff), sub: (m) => `${m.bottleneck === 'PUMP' ? 'pump-limited' : 'reservoir-limited'} · ${fx(m.pumpDisplacement, 0)} bpd disp.`, bar: (m) => [m.pumpEff, m.pumpEff < 0.5 ? C.warn : C.ok],
    tip: (m) => `<b>Volumetric pump efficiency</b><br>Liquid lifted ÷ plunger displacement (${fx(m.liquidRate, 0)} of ${fx(m.pumpDisplacement, 0)} bpd).<br><span class="mut">Currently ${m.bottleneck === 'PUMP' ? 'the pump' : 'the reservoir inflow'} is the bottleneck.</span>` },
  { id: 'fill', label: 'Pump fillage', dot: C.ok, unit: '%', val: (m) => pct(m.fillage), sub: (m) => `submergence ${fx(m.submergence, 0)} m`, bar: (m) => [m.fillage, m.fillage < 0.7 ? C.warn : C.ok],
    tip: () => `<b>Pump fillage</b><br>How full the barrel gets each upstroke. Under ~70% the plunger slams into fluid (<i>fluid pound</i>).` },
  { id: 'float', label: 'Float margin', dot: C.ok, unit: '%', val: (m) => pct(m.floatMargin), sub: (m) => `safe below ${fx(m.spmSafe)} SPM`, bar: (m) => [clamp(m.floatMargin, 0, 1), m.floatMargin < 0 ? C.crit : m.floatMargin < 0.2 ? C.warn : C.ok],
    tip: (m) => `<b>Rod float margin</b><br>How much faster gravity can pull the rods down than the viscous crude holds them back. Negative means the rods lag the horsehead and the wire rope slackens.<br><span class="mut">Safe speed today: ${fx(m.spmSafe)} SPM.</span>` },
  { id: 'visc', label: 'Viscosity', dot: '#c98b5a', unit: 'cP', val: (m) => k1(m.viscosity), sub: (m, c) => (c.fluid ? `dead oil ${k1(c.fluid.deadOilCp)} cP at ${c.fluid.tRes} °C` : 'at the pump intake'), bar: (m) => [clamp(Math.log10(m.viscosity) / 4, 0, 1), '#c98b5a'],
    tip: (m, c) => `<b>Crude viscosity at the pump</b><br>${fx(m.viscosity, 0)} cP.${c.fluid ? ` Baghewala ${c.fluid.api}° API crude is ~${k1(c.fluid.deadOilCp)} cP at reservoir temperature; steam heat thins it by orders of magnitude.` : ''}` },
  { id: 'temp', label: 'Sandface T', dot: C.inj, unit: '°C', val: (m) => fx(m.sandfaceT, 0), sub: (m, c) => `heated r ${fx(m.heatedRadius)} m${c.fluid ? ` · base ${c.fluid.tRes} °C` : ''}`, bar: (m) => [clamp((m.sandfaceT - 40) / 180, 0, 1), C.inj],
    tip: (m, c) => `<b>Sandface temperature</b><br>Formation temperature at the perforations${c.fluid ? `; the reservoir baseline is ${c.fluid.tRes} °C` : ''}.` },
  { id: 'energy', label: 'Lift energy', dot: C.violet, unit: 'kWh/bbl', val: (m) => fx(m.kwhPerBbl), sub: (m) => `motor ${fx(m.motorKw)} kW`, bar: (m) => [clamp(m.kwhPerBbl / 20, 0, 1), C.violet],
    tip: () => `<b>Lift energy</b><br>Electricity spent per barrel of oil lifted.` },
  { id: 'sor', label: 'Steam–oil ratio', dot: '#e8e2d6', unit: '', val: (m) => (m.sor ? fx(m.sor, 2) : DASH), sub: (m) => `${fx(m.steamTons, 0)} t steam / cycle`, bar: (m) => [clamp(1 - (m.sor || 6) / 8, 0, 1), '#e8e2d6'],
    tip: () => `<b>Cumulative steam–oil ratio</b><br>Barrels of cold-water-equivalent steam per barrel of oil so far this cycle. Lower is better; under ~4 is economic.` },
  { id: 'co2', label: 'CO₂ intensity', dot: '#9fb0a0', unit: 'kg/bbl', val: (m) => (m.co2PerBbl ? fx(m.co2PerBbl, 0) : DASH), sub: () => `steam + grid power`, bar: (m) => [clamp(m.co2PerBbl / 200, 0, 1), '#9fb0a0'],
    tip: () => `<b>CO₂ intensity</b><br>Gas burned for steam plus grid power for the pump, per barrel.` },
];

// tooltips: (m, live, d, ctx) — any of them may be null
const TIPS = {
  spm: (m, live) => `<b>Pumping speed</b><br>${fx(live?.spmActual)} strokes per minute${m ? ` (set ${fx(m.spm)})` : ''}.<br><span class="mut">The unit parks at top of stroke during injection and soak.</span>`,
  stroke: (m) => `<b>Stroke length</b><br>${fx(m?.stroke, 2)} m polished-rod travel.<br><span class="mut">Longer stroke at lower SPM lifts the same fluid with fewer impacts.</span>`,
  vfd: (m, live) => `<b>VFD output</b><br>${fx(live?.hz)} Hz · speed profile shaped for the downstroke${m ? ` (kd ${fx(m.kd, 2)})` : ''}.`,
  amps: (m, live, d) => `<b>Motor current</b><br>${fx(live?.amps, 0)} A now${d ? `, ${fx(d.ampsAvg, 0)} A average` : ''}${m ? ` · ${fx(m.motorKw)} kW` : ''}.`,
  load: (m) => `<b>Polished-rod load</b><br>Live load at the carrier bar.${m ? ` This stroke: peak ${fx(m.pprl, 0)} kN, minimum ${fx(m.mprl, 0)} kN.` : ''}`,
  battery: (m) => `<b>Thermal battery</b><br>${pct(m?.thermalBattery)}% of the injected heat is still in the rock near the well.`,
  cum: (m, live, d) => `<b>Cumulative oil, this cycle</b><br>${num(m?.cumOil) ? Math.round(m.cumOil).toLocaleString() : DASH} bbl so far.${num(d?.recovery) ? `<br><span class="mut">Recovery to date ${(d.recovery * 100).toFixed(2)}% of drainage-area OOIP.</span>` : ''}`,
  cutoff: () => `<b>Days to economic cut-off</b><br>When the daily margin drops below the best whole-cycle average, re-steam.`,
};

/* ------------------------------------------------------------------ HUD */

export class Hud {
  constructor({ getSim }) {
    this.getSim = getSim;
    this.m = null; this.d = null; this.ctx = { fluid: null, prov: provenance(null) };
    this.series = null; this.dyno = null; this.profile = null;
    this.rodKey = ''; this.monthKey = '';
    this.strokes = [];                       // last per-stroke events from the live stream
    this.buildKpis();
    this.buildStrokes();
    this.setupTooltips();
    this.setupAdvisor();
    this.onApply = null; this.onSchedule = null;
    this.unavailable();
  }

  buildKpis() {
    $('kpis').innerHTML = KPIS.map((k) => `<div class="kpi" data-kpi="${k.id}"><label><i style="background:${k.dot}"></i>${k.label}</label><div class="kv"><span>—</span><small>${k.unit}</small></div><div class="ksub"></div><div class="kbar"><b></b></div></div>`).join('');
    this.kpiEls = KPIS.map((k) => {
      const el = document.querySelector(`[data-kpi="${k.id}"]`);
      return { k, v: el.querySelector('.kv span'), s: el.querySelector('.ksub'), b: el.querySelector('.kbar b') };
    });
  }
  buildStrokes() {
    $('strokes').innerHTML = Array.from({ length: 18 }, () => '<i class="stk"><b></b></i>').join('');
    this.strokeEls = [...$('strokes').children];
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
    const bind = (el, fn, needM = false) => {
      el.addEventListener('pointerenter', (e) => { if (needM && !this.m) return; show(fn(this.m, this.getSim()?.live ?? null, this.d, this.ctx), e); });
      el.addEventListener('pointermove', move);
      el.addEventListener('pointerleave', hide);
    };
    document.querySelectorAll('#ui [data-tip]').forEach((el) => TIPS[el.dataset.tip] && bind(el, TIPS[el.dataset.tip]));
    this.kpiEls.forEach(({ k }) => bind(document.querySelector(`[data-kpi="${k.id}"]`), (m) => k.tip(m, this.ctx), true));
    // rods
    $('rod-grid').addEventListener('pointermove', (e) => {
      const el = e.target.closest('.rod'); const h = health(this.getSim());
      if (!el || !h) { hide(); return; }
      const r = h.rods[+el.dataset.rod];
      const f = r.failed ? h.failures.find((ff) => ff.rod === r.index + 1) : null;
      show(f ? `<b>Rod #${r.index + 1} · ${f.size} · parted</b><br>${f.mode}, ${f.date}<br><span class="mut">${fx(r.depthM, 0)} m · ${f.cause}</span>`
        : `<b>Rod #${r.index + 1}</b> <span class="mut">· ${r.taper} · ${fx(r.depthM, 0)} m</span><br>Fatigue use ${pct(r.fatigue)}% of the Goodman limit`, e);
    });
    $('rod-grid').addEventListener('pointerleave', hide);
    $('months').addEventListener('pointermove', (e) => {
      const el = e.target.closest('.mo'); const h = health(this.getSim());
      if (!el || !h) { hide(); return; }
      const i = +el.dataset.mo, u = h.unseats, ev = u.events.includes(i);
      const detail = u.details?.find((x) => x.month === i);
      show(`<b>${u.months[i]}</b><br>${ev ? (detail ? `Pump unseated ${detail.date}: ${detail.action} (${detail.downtimeH ?? DASH} h lost)` : 'Pump unseated') : 'No unseat'}`, e);
    });
    $('months').addEventListener('pointerleave', hide);
    $('strokes').addEventListener('pointerenter', (e) => {
      const live = this.getSim()?.live, h = health(this.getSim());
      show(`<b>Last ${this.strokeEls.length} strokes</b><br>A burst marks a stroke where the plunger hit fluid (fluid pound), as reported by the live stream.${h ? `<br><span class="mut">Impact speed ≈ ${fx(h.impactVel, 2)} m/s · ${k1(h.impactsDay)} impacts/day</span>` : ''}${live ? '' : '<br><span class="mut">Live stream not connected.</span>'}`, e);
    });
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
      const pc = pastCycles(this.getSim());
      const hist = pc ? pc.map((c) => `C${c.n} ${fx(c.oil[day], 0)}`).join(' · ') : null;
      show(`<b>Day ${day}</b> <span class="mut">· ${ph}</span><br>Oil ${fx(s.oil[day])} BOPD <span class="mut">(P90–P10 ${fx(s.oilP90[day], 0)}–${fx(s.oilP10[day], 0)})</span>${hist ? `<br><span class="mut">Earlier cycles: ${hist}</span>` : ''}<br>Sandface ${fx(s.T[day], 0)} °C · ${k1(s.mu[day])} cP`, e);
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
    $('adv-apply').onclick = async () => {
      const r = this.m?.recommendation; if (!r || !this.onApply) return;
      const btn = $('adv-apply'); btn.disabled = true; btn.textContent = 'Applying…';
      const res = await this.onApply(r);
      btn.textContent = res?.applied ? 'Applied' : `Failed: ${res?.error ?? 'unknown error'}`;
    };
    $('plan-apply').onclick = async () => {
      const P = plan(this.getSim()); if (!P || !this.onSchedule) return;
      const btn = $('plan-apply'); btn.disabled = true; btn.textContent = 'Scheduling…';
      const res = await this.onSchedule(P.mantle);
      btn.textContent = res?.scheduled ? `Scheduled · cycle ${res.cycle ?? 'next'}` : `Failed: ${res?.error ?? 'unknown error'}`;
    };
  }

  /* no data from the API (yet): every value reads "—", charts say why */
  unavailable() {
    const sim = this.getSim?.();
    this.ctx.prov = provenance(sim);
    const msg = this.ctx.prov.mode === 'offline' ? 'Mantle API unavailable' : 'Connecting to the Mantle API…';
    document.body.classList.toggle('no-data', true);
    document.body.classList.toggle('api-offline', this.ctx.prov.mode === 'offline');
    for (const id of ['t-spm', 't-stroke', 't-hz', 't-amps', 't-load', 'v-net', 'ring-day', 's-battery', 's-cum', 's-cutoff']) $(id).textContent = DASH;
    $('phase-sub').textContent = msg;
    $('v-delta').textContent = ''; $('cycle-sum').textContent = ''; $('ring-phase').textContent = ''; $('ring-sub').textContent = '';
    $('c-bbl').textContent = DASH; $('c-bar').innerHTML = ''; $('c-rows').innerHTML = '';
    $('adv-title').textContent = msg; $('adv-detail').textContent = ''; $('adv-drive').innerHTML = ''; $('adv-deltas').innerHTML = '';
    $('adv-apply').disabled = true; $('adv-apply').textContent = 'Waiting for the optimiser';
    $('levers').innerHTML = `<div class="h-note">${msg}</div>`; $('dividend').innerHTML = '';
    $('plan-apply').disabled = true;
    for (const { v, s, b } of this.kpiEls) { v.textContent = DASH; s.textContent = ''; b.style.width = '0%'; }
    for (const id of ['c-cycle', 'c-dyno', 'c-profile']) emptyCanvas($(id), msg);
    const f = fit($('c-ring')); if (f) { f.g.beginPath(); f.g.arc(f.w / 2, f.h / 2, f.w / 2 - 8, 0, 7); f.g.strokeStyle = 'rgba(255,255,255,0.1)'; f.g.lineWidth = 6; f.g.stroke(); }
    this.renderHealth(null, null);
    $('alert-line').innerHTML = `<i style="background:${C.mute}"></i><span>${msg}</span>`;
    $('tab-alert').hidden = true;
    $('dyno-cls').textContent = DASH; $('dyno-torque').innerHTML = '';
  }

  /* per metrics tick (4 Hz); m is the API's state (null → unavailable) */
  update(m) {
    const sim = this.getSim();
    this.ctx.prov = provenance(sim);
    if (!m) { this.m = null; this.unavailable(); return; }
    document.body.classList.remove('no-data', 'api-offline');
    this.m = m;
    this.ctx.fluid = fluid(sim);
    const d = (this.d = derived(m));
    const prod = m.phase === 'PRODUCTION';
    $('t-stroke').textContent = fx(m.stroke, 2);
    $('phase-sub').textContent = phaseName(m.phase) + (m.stale ? ' · updating…' : '');
    const dot = $('live-dot');
    dot.classList.toggle('steam', m.phase === 'INJECTION'); dot.classList.toggle('soak', m.phase === 'SOAK');

    // value + cost anatomy
    $('v-net').textContent = inr(m.netPerDay, false);
    const dl = $('v-delta'); dl.className = 'delta';
    const c = d?.cost;
    if (!prod) dl.textContent = m.phase === 'INJECTION' ? 'steaming' : 'soaking';
    else dl.textContent = num(c?.costBbl) ? `₹${k1(c.costBbl)}/bbl cost` : DASH;
    if (c) {
      const parts = [['Steam', c.steamDay, C.inj], ['Power', c.powerDay, C.violet], ['Maintenance', c.maintDay, C.crit], ['Chemicals', c.chemDay, 'rgba(240,232,222,0.5)']].filter(([, v]) => num(v));
      $('c-bbl').textContent = num(c.costBbl) ? `₹${Math.round(c.costBbl).toLocaleString()} / bbl` : 'not producing';
      $('c-bar').innerHTML = parts.map(([, v, col]) => `<i style="flex:${v};background:${col}"></i>`).join('');
      $('c-rows').innerHTML = parts.map(([l, v, col]) => `<span><i style="background:${col}"></i>${l}<b>${inr(v)}</b></span>`).join('') + (num(c.revenueDay) ? `<span class="tot">Revenue<b>${inr(c.revenueDay)}</b></span>` : '');
    }

    // cycle panel
    const prodLen = CYCLE.days - CYCLE.soakEnd;
    $('cycle-sum').textContent = `Day ${fx(m.cycleDay, 0)} / ${CYCLE.days}`;
    $('ring-phase').textContent = phaseName(m.phase);
    $('ring-day').textContent = fx(m.cycleDay, 0);
    $('ring-sub').textContent = m.phase === 'INJECTION' ? `day ${fx(m.dayInPhase, 0)} of ${CYCLE.injEnd}` : m.phase === 'SOAK' ? `day ${fx(m.dayInPhase, 0)} of ${CYCLE.soakEnd - CYCLE.injEnd}` : `day ${fx(m.dayInPhase, 0)} of ${prodLen}`;
    $('s-battery').textContent = `${pct(m.thermalBattery)}%`;
    $('s-cum').textContent = prod ? k1(m.cumOil) : DASH;
    $('s-cutoff').textContent = prod ? (m.daysToCutoff > 0 ? `${fx(m.daysToCutoff, 0)} d` : 'now') : DASH;
    this.drawRing(m);

    this.updateAdvisor(m, d);

    for (const { k, v, s, b } of this.kpiEls) {
      v.textContent = k.val(m, this.ctx); s.textContent = k.sub(m, this.ctx);
      const [f, col] = k.bar(m, this.ctx);
      b.style.width = `${num(f) ? clamp(f, 0, 1) * 100 : 0}%`; b.style.background = col;
    }

    // curve sets straight from the API (null → the card says it's waiting)
    this.series = sim.series(); this.dyno = prod ? sim.dynoCard() : null; this.profile = sim.profile();
    $('dyno-cls').textContent = this.dyno ? `${this.dyno.cls} · ${pct(this.dyno.clsConf)}%` : prod ? DASH : 'unit parked';
    $('dyno-cls').style.color = !this.dyno ? C.mute : this.dyno.cls === 'NORMAL' ? C.ok : this.dyno.cls === 'ROD FLOAT RISK' ? C.crit : C.warn;
    $('dyno-torque').innerHTML = prod ? `gearbox torque <b style="color:${m.torquePct > 1 ? C.crit : m.torquePct > 0.85 ? C.warn : C.text}">${pct(m.torquePct)}%</b>` : '';
    this.drawCycle(m);
    if (this.profile) this.drawProfile(m, d); else emptyCanvas($('c-profile'), 'Waiting for the depth profile…');
    if (!this.dyno && prod) emptyCanvas($('c-dyno'), 'Waiting for the dynamometer card…');
    this.renderHealth(m, health(sim));
    this.renderAlerts(m);
  }

  updateAdvisor(m, d) {
    const r = m.recommendation;
    if (!r) { $('adv-title').textContent = 'Waiting for the optimiser…'; $('adv-apply').disabled = true; }
    else {
      $('adv-title').textContent = r.title;
      $('adv-detail').textContent = r.detail;
      const chips = [];
      const chip = (v, label, goodIfUp) => { if (!num(v) || Math.abs(v) < 0.005) return; const good = goodIfUp ? v > 0 : v < 0; chips.push(`<span class="${good ? 'good' : 'bad'}">${v > 0 ? '+' : '−'}${Math.abs(v * 100).toFixed(0)}% ${label}</span>`); };
      chip(r.deltas?.oil, 'oil', true); chip(r.deltas?.float, 'float', true); chip(r.deltas?.energy, 'kWh/bbl', false); chip(r.deltas?.impacts, 'impacts', false);
      $('adv-deltas').innerHTML = chips.join('');
      $('adv-drive').innerHTML = m.phase === 'PRODUCTION' && d
        ? `<span><label>VFD</label><div>${fx(d.hz)}<i>→</i><b>${fx(r.hz)}</b> Hz</div></span><span><label>Speed profile</label><div>${fx(m.kd, 2)}<i>→</i><b>${fx(r.kd, 2)}</b></div></span><span><label>Stroke</label><div><b>${fx(r.stroke ?? m.stroke, 2)}</b> m</div></span>`
        : '';
      const can = m.phase === 'PRODUCTION' && (Math.abs(r.spm - m.spm) > 0.05 || Math.abs(r.kd - m.kd) > 0.001);
      const btn = $('adv-apply');
      if (btn.textContent !== 'Applying…') { btn.disabled = !can; btn.textContent = can ? `Apply · ${fx(r.spm)} SPM · ${fx(r.hz, 0)} Hz` : 'Settings optimal'; }
    }

    // next-cycle recipe (O2): today's practice (hollow) vs Mantle (solid) on each lever's range
    const P = plan(this.getSim());
    if (!P) { $('levers').innerHTML = '<div class="h-note">Waiting for the cycle planner…</div>'; $('dividend').innerHTML = ''; $('plan-apply').disabled = true; return; }
    const L = [['Steam volume', 'steam', 't', 0], ['Injection pressure', 'pInj', 'MPa', 1], ['Soak time', 'soak', 'd', 0], ['Production cut-off', 'cutoff', 'day', 0]];
    $('levers').innerHTML = L.map(([label, key, unit, dp]) => {
      const [lo, hi] = P.ranges[key], a = P.practice[key], b = P.mantle[key];
      const X = (v) => clamp((v - lo) / (hi - lo), 0, 1) * 100;
      const l = Math.min(X(a), X(b)), w = Math.abs(X(b) - X(a));
      return `<div class="lever"><div class="lv-top"><span>${label}</span><em>${fx(a, dp)} <i>→</i> <b>${fx(b, dp)}</b> ${unit}</em></div>
        <div class="lv-track"><i class="lv-span" style="left:${l}%;width:${w}%"></i><i class="lv-ghost" style="left:${X(a)}%"></i><i class="lv-dot" style="left:${X(b)}%"></i></div></div>`;
    }).join('');
    const joint = P.inrPerCycle > 0 ? clamp(P.jointShare / P.inrPerCycle, 0, 1) : 0;
    const horizon = P.basis?.inrPerCycleHorizonDays, pc = P.perCycle;
    const per = num(horizon) ? `per ${Math.round(horizon)} days vs today` : 'per cycle vs today';
    $('dividend').innerHTML = `<div class="dv-top"><b>${P.inrPerCycle >= 0 ? '+' : ''}${inr(P.inrPerCycle)}</b><span>${per}</span></div>
      <div class="dv-bars"><div><label>Today</label><i style="width:${100 / (1 + Math.max(0, P.oilLift)) - 0.5}%"></i></div><div><label>Mantle</label><i style="width:${100 * (1 - joint * Math.max(0, P.oilLift))}%"></i><i class="joint" style="width:${100 * joint * Math.max(0, P.oilLift) + 0.6}%"></i></div></div>
      <div class="dv-sub">${P.oilLift >= 0 ? '+' : ''}${(P.oilLift * 100).toFixed(0)}% oil per day${pc && num(pc.practiceInrPerDay) ? ` · ${inr(pc.practiceInrPerDay)} → ${inr(pc.mantleInrPerDay)}/day` : ''} · SOR ${fx(P.sor[0], 2)} → ${fx(P.sor[1], 2)} · <span class="jt">${inr(P.jointShare)}</span> only from tuning steam &amp; pump together</div>`;
    const pb = $('plan-apply');
    if (!pb.textContent.startsWith('Scheduled') && pb.textContent !== 'Scheduling…') { pb.disabled = false; pb.textContent = 'Schedule for next cycle'; }
  }

  // rod & pump health (M4) — pictograms rebuilt only when the API's answer changes
  renderHealth(m, h) {
    if (!h) {
      if (this.rodKey !== 'none') {
        this.rodKey = 'none';
        $('rod-grid').innerHTML = Array.from({ length: 140 }, (_, i) => `<i class="rod" data-rod="${i}" style="background:${fatigueColor(null)}"></i>`).join('');
        $('months').innerHTML = Array.from({ length: 12 }, () => '<i class="mo"><span></span></i>').join('');
      }
      for (const id of ['rods-sum', 'imp-sum', 'uns-sum']) $(id).textContent = DASH;
      $('rods-note').innerHTML = ''; $('imp-note').innerHTML = ''; $('uns-note').innerHTML = '';
      $('health-sum').innerHTML = DASH;
      return;
    }
    const key = `${h.rods.length}|${h.rods.map((r) => (r.failed ? 'x' : r.fatigue.toFixed(3))).join(',')}`;
    if (key !== this.rodKey) {
      this.rodKey = key;
      $('rod-grid').innerHTML = h.rods.map((r, i) => {
        const nextTaper = h.rods[i + 1] && h.rods[i + 1].taper !== r.taper;
        return `<i class="rod${r.failed ? ' failed' : ''}${nextTaper ? ' taper' : ''}" data-rod="${i}"${r.failed ? '' : ` style="background:${fatigueColor(r.fatigue)}"`}></i>`;
      }).join('');
    }
    const mk = JSON.stringify(h.unseats);
    if (mk !== this.monthKey) {
      this.monthKey = mk;
      $('months').innerHTML = h.unseats.months.map((mo, i) => `<i class="mo${h.unseats.events.includes(i) ? ' ev' : ''}" data-mo="${i}"><span>${mo[0]}</span></i>`).join('');
    }
    const worst = Math.max(...h.rods.map((r) => r.fatigue));
    $('rods-sum').textContent = `Goodman ${fx(worst, 2)}`;
    $('rods-note').innerHTML = `<span class="x">✕</span> ${h.failures.length} parted${h.failureWindowMonths ? ` in ${h.failureWindowMonths} mo` : ''}`;
    $('health-sum').innerHTML = `MTBF <b>${fx(h.mtbfDays, 0)} d</b> <i>→</i> ${fx(h.mtbfMantleDays, 0)} d`;
    $('uns-sum').textContent = `${h.unseats.events.length} in ${h.unseats.months.length} mo`;
    const prod = m?.phase === 'PRODUCTION';
    $('imp-sum').textContent = prod ? `${k1(h.impactsDay)}/day` : 'parked';
    const recSpm = m?.recommendation?.spm;
    $('imp-note').innerHTML = !prod ? DASH : h.impactsDay > 50 ? (h.impactsMantle < 50 ? `<b>none</b> at ${fx(recSpm)} SPM` : `<b>${k1(h.impactsMantle)}/day</b> at ${fx(recSpm)} SPM`) : 'no fluid pound';
    $('uns-note').innerHTML = `uplift margin <b>${fx(h.upliftMargin)}×</b> · 30-day risk <b class="${h.unseatRisk30d > 0.25 ? 'w' : ''}">${pct(h.unseatRisk30d)}%</b>`;
  }

  renderAlerts(m) {
    const alerts = m.alerts || [];
    const bad = alerts.filter((a) => a.level !== 'ok');
    const lc = { ok: C.ok, warn: C.warn, crit: C.crit };
    const top = bad.find((a) => a.level === 'crit') || bad[0] || alerts[0];
    $('alert-line').innerHTML = top ? `<i style="background:${lc[top.level]}"></i><span>${top.text}</span>${bad.length > 1 ? `<em>+${bad.length - 1}</em>` : ''}` : '';
    $('alert-line').title = alerts.map((a) => a.text).join('\n');
    $('tab-alert').hidden = !bad.length;
    $('tab-alert').style.background = bad.some((a) => a.level === 'crit') ? C.crit : C.warn;
  }

  // per-stroke events from the live stream: {n, pounded, severity}
  pushStroke(ev) {
    if (!ev || ev.n === this.lastStrokeN) return;
    this.lastStrokeN = ev.n;
    this.strokes.push(ev);
    if (this.strokes.length > this.strokeEls.length) this.strokes.shift();
    const off = this.strokeEls.length - this.strokes.length;
    this.strokeEls.forEach((el, i) => {
      const s = this.strokes[i - off];
      el.classList.toggle('hit', !!s?.pounded);
      el.style.setProperty('--sev', num(s?.severity) ? (0.55 + 0.45 * clamp(s.severity, 0, 1)).toFixed(2) : '0.8');
      el.classList.toggle('now', i === this.strokeEls.length - 1 && !!s);
    });
  }

  /* per frame: telemetry from the live stream, the live dyno marker */
  frame() {
    const sim = this.getSim();
    const live = sim?.live;
    $('t-spm').textContent = fx(live?.spmActual);
    $('t-hz').textContent = fx(live?.hz);
    $('t-amps').textContent = fx(live?.amps, 0);
    $('t-load').textContent = fx(live?.load, 0);
    if (live?.lastStroke) this.pushStroke(live.lastStroke);
    if (!this.m || !document.getElementById('metrics').classList.contains('open')) return;
    if (this.dyno) this.drawDyno(live);
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
    const cv = $('c-cycle');
    if (!this.series) { emptyCanvas(cv, 'Waiting for the cycle forecast…'); return; }
    const f = fit(cv);
    if (!f) return;
    const { g, w, h } = f, s = this.series, sim = this.getSim();
    const pc = pastCycles(sim), pcurve = planCurve(sim);
    const x0 = 30, x1 = w - 30, y0 = 8, y1 = h - 16;
    this.cycLayout = { x0, x1 };
    const X = (d) => x0 + (d / CYCLE.days) * (x1 - x0);
    const all = [...s.oilP10, ...(pc ? pc.flatMap((c) => c.oil) : []), ...(pcurve ? pcurve.oil : [])].filter(num);
    const oMax = Math.max(20, ...all) * 1.04;
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
    const path = (vals, from = 0, to = CYCLE.days) => { g.beginPath(); let first = true; s.day.forEach((d, i) => { if (d < from || d > to || !num(vals[i])) return; const y = Y(vals[i]); first ? g.moveTo(X(d), y) : g.lineTo(X(d), y); first = false; }); };
    // earlier cycles of this well (history from the database)
    if (pc) pc.forEach((c, n) => { path(c.oil, CYCLE.soakEnd); g.strokeStyle = `rgba(255,255,255,${0.1 + n * 0.04})`; g.lineWidth = 1; g.stroke(); });
    // P10–P90 band (M2)
    g.beginPath();
    s.day.forEach((d, i) => (i ? g.lineTo(X(d), Y(s.oilP10[i])) : g.moveTo(X(d), Y(s.oilP10[i]))));
    for (let i = s.day.length - 1; i >= 0; i--) g.lineTo(X(s.day[i]), Y(s.oilP90[i]));
    g.closePath(); g.fillStyle = 'rgba(255,255,255,0.07)'; g.fill();
    g.beginPath(); s.day.forEach((d, i) => (i ? g.lineTo(X(d), YT(s.T[i])) : g.moveTo(X(d), YT(s.T[i]))));
    g.setLineDash([4, 3]); g.strokeStyle = 'rgba(240,160,75,0.75)'; g.lineWidth = 1.2; g.stroke(); g.setLineDash([]);
    // Mantle plan curve (O2)
    if (pcurve) {
      g.beginPath(); pcurve.day.forEach((d, i) => (i ? g.lineTo(X(d), Y(pcurve.oil[i])) : g.moveTo(X(d), Y(pcurve.oil[i]))));
      g.setLineDash([5, 4]); g.strokeStyle = 'rgba(95,227,154,0.85)'; g.lineWidth = 1.6; g.stroke(); g.setLineDash([]);
      const li = pcurve.day.length - 1;
      g.fillStyle = C.ok; g.beginPath(); g.arc(X(pcurve.day[li]), Y(pcurve.oil[li]), 3, 0, 7); g.fill();
    }
    // this cycle
    path(s.oil); g.strokeStyle = 'rgba(255,255,255,0.35)'; g.lineWidth = 1.6; g.stroke();
    path(s.oil, 0, Math.ceil(m.cycleDay)); g.strokeStyle = '#fff'; g.lineWidth = 2; g.stroke();
    if (m.phase === 'PRODUCTION') {
      const cd = Math.min(CYCLE.days, m.cycleDay + m.daysToCutoff);
      g.setLineDash([3, 3]); g.strokeStyle = 'rgba(95,227,154,0.5)'; g.beginPath(); g.moveTo(X(cd), y0); g.lineTo(X(cd), y1); g.stroke(); g.setLineDash([]);
      g.fillStyle = C.ok; g.textAlign = cd > 100 ? 'right' : 'left'; g.fillText('cut-off', X(cd) + (cd > 100 ? -4 : 4), y0 + 11);
    }
    g.strokeStyle = 'rgba(255,255,255,0.5)'; g.beginPath(); g.moveTo(X(m.cycleDay), y0); g.lineTo(X(m.cycleDay), y1); g.stroke();
    if (num(m.oilRate)) { g.beginPath(); g.arc(X(m.cycleDay), Y(m.oilRate), 4, 0, Math.PI * 2); g.fillStyle = '#fff'; g.fill(); }
    if (this.hoverDay != null) { g.strokeStyle = 'rgba(255,255,255,0.25)'; g.beginPath(); g.moveTo(X(this.hoverDay), y0); g.lineTo(X(this.hoverDay), y1); g.stroke(); }
  }

  drawDyno(live) {
    const f = fit($('c-dyno'));
    if (!f) return;
    const { g, w, h } = f, d = this.dyno, m = this.m;
    const x0 = 30, x1 = w - 34, y0 = 6, y1 = h - 14;
    const fMin = Math.min(0, d.fMin), fMax = Math.max(d.fMax, m.pprl) * 1.08;
    const X = (x) => x0 + (x / d.xMax) * (x1 - x0), Y = (v) => y1 - ((v - fMin) / (fMax - fMin)) * (y1 - y0);
    g.strokeStyle = C.grid; g.lineWidth = 1; g.font = FONT; g.fillStyle = C.mute;
    const step = fMax > 120 ? 40 : 20;
    for (let v = 0; v <= fMax; v += step) { g.beginPath(); g.moveTo(x0, Y(v)); g.lineTo(x1, Y(v)); g.stroke(); g.textAlign = 'right'; g.fillText(v, x0 - 5, Y(v) + 3); }
    g.textAlign = 'center'; g.fillText('stroke →', (x0 + x1) / 2, h - 2);
    for (const [v, lbl] of [[m.pprl, 'PPRL'], [m.mprl, 'MPRL']]) {
      if (!num(v)) continue;
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
    // impact point (M5), as located by the API
    if (d.impact && num(d.impact.x)) {
      const bx = X(d.impact.x), by = Y(d.impact.f);
      const pulse = 0.6 + 0.4 * Math.sin(performance.now() / 180);
      g.strokeStyle = `rgba(255,195,90,${pulse})`; g.lineWidth = 1.4;
      g.beginPath(); for (let k = 0; k < 8; k++) { const a = (k / 8) * Math.PI * 2, r0 = 4, r1 = k % 2 ? 7 : 10; g.moveTo(bx + Math.cos(a) * r0, by + Math.sin(a) * r0); g.lineTo(bx + Math.cos(a) * r1, by + Math.sin(a) * r1); } g.stroke();
    }
    // live position/load marker from the telemetry stream
    if (live && num(live.rodPos) && num(live.load)) {
      g.beginPath(); g.arc(X(clamp(live.rodPos, 0, d.xMax)), Y(live.load), 4, 0, Math.PI * 2); g.fillStyle = C.heat; g.fill();
      g.beginPath(); g.arc(X(clamp(live.rodPos, 0, d.xMax)), Y(live.load), 8, 0, Math.PI * 2); g.strokeStyle = 'rgba(240,160,75,0.4)'; g.lineWidth = 1; g.stroke();
    }
  }

  drawProfile(m, d) {
    const f = fit($('c-profile'));
    if (!f) return;
    const { g, w, h } = f, p = this.profile, fl = this.ctx.fluid;
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
    const line = (arr, fxn, col, lw, dash) => { g.beginPath(); arr.forEach((t, i) => (i ? g.lineTo(fxn(t), Y(p.depth[i])) : g.moveTo(fxn(t), Y(p.depth[i])))); g.setLineDash(dash || []); g.strokeStyle = col; g.lineWidth = lw; g.stroke(); g.setLineDash([]); };
    line(p.Tformation, X, 'rgba(255,255,255,0.35)', 1.1, [3, 3]);
    line(p.pressure.map((b) => b / 10), XP, C.blue, 1.5);
    line(p.Tfluid, X, C.heat, 1.8);
    if (fl && num(fl.pRes)) {
      g.fillStyle = C.blue; g.beginPath(); g.arc(XP(fl.pRes), Y(1120), 3, 0, 7); g.fill();
      g.textAlign = 'left'; g.fillText(`Pr ${fl.pRes} MPa`, XP(fl.pRes) + 6, Y(1120) + 3);
    }
    g.strokeStyle = 'rgba(255,255,255,0.3)'; g.setLineDash([2, 3]); g.beginPath(); g.moveTo(x0, Y(m.fluidLevel)); g.lineTo(x1, Y(m.fluidLevel)); g.stroke(); g.setLineDash([]);
    g.fillStyle = C.mute; g.textAlign = 'right'; g.fillText('fluid level', x1, Y(m.fluidLevel) - 3);
    g.fillStyle = '#fff'; g.fillRect(x0 + 2, Y(WELLBORE.pumpTop) - 2, 8, 4);
    if (d && num(d.pip)) { g.textAlign = 'left'; g.fillStyle = C.mute; g.fillText(`PIP ${d.pip.toFixed(1)}`, x0 + 13, Y(WELLBORE.pumpTop) + 3); }
  }
}
