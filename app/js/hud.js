// Glass HUD for the Well View: telemetry, the value card, the steam-cycle ring, the advisor,
// the KPI row, the metric cards (cycle production, dynamometer card, heat-in-well profile,
// operating limits) and hover tooltips. Everything reads from the live WellSim.
import { CYCLE } from './sim.js';
import { WELLBORE } from './rig.js';

const $ = (id) => document.getElementById(id);
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const C = { text: '#f3efe9', mute: 'rgba(240,232,222,0.55)', grid: 'rgba(255,255,255,0.07)', heat: '#f0a04b', blue: '#7cc4ff', ok: '#5fe39a', warn: '#ffc35a', crit: '#ff6b6b', inj: '#ff7a3d' };
const FONT = '500 10px Inter, sans-serif';

export const inr = (v) => {
  const a = Math.abs(v), s = v < 0 ? '−' : '';
  if (a >= 1e7) return `${s}₹${(a / 1e7).toFixed(2)} Cr`;
  if (a >= 1e5) return `${s}₹${(a / 1e5).toFixed(2)} L`;
  if (a >= 1e3) return `${s}₹${(a / 1e3).toFixed(1)}k`;
  return `${s}₹${a.toFixed(0)}`;
};
const pct = (v) => `${(v * 100).toFixed(0)}`;
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

/* ------------------------------------------------------------------ KPI definitions */

const KPIS = [
  { id: 'oil', label: 'Oil rate', dot: C.heat, unit: 'BOPD', val: (m) => m.oilRate.toFixed(1), sub: (m) => `liquid ${m.liquidRate.toFixed(0)} bpd`, bar: (m) => [m.oilRate / 80, C.heat],
    tip: (m) => `<b>Oil rate</b><br>${m.oilRate.toFixed(1)} barrels of oil per day at cycle day ${m.cycleDay.toFixed(0)}.<br><span class="mut">Falls as the heated zone cools and the crude thickens again.</span>` },
  { id: 'wc', label: 'Water cut', dot: C.blue, unit: '%', val: (m) => pct(m.waterCut), sub: (m) => `condensed steam + brine`, bar: (m) => [m.waterCut, C.blue],
    tip: () => `<b>Water cut</b><br>Share of produced liquid that is water (condensed steam and formation brine).` },
  { id: 'fill', label: 'Pump fillage', dot: C.ok, unit: '%', val: (m) => pct(m.fillage), sub: (m) => `pump eff. ${pct(m.pumpEff)}%`, bar: (m) => [m.fillage, m.fillage < 0.7 ? C.warn : C.ok],
    tip: () => `<b>Pump fillage</b><br>How full the barrel gets each upstroke. Under ~70% the plunger slams into fluid (<i>fluid pound</i>).` },
  { id: 'float', label: 'Float margin', dot: C.ok, unit: '%', val: (m) => pct(m.floatMargin), sub: (m) => `safe below ${m.spmSafe.toFixed(1)} SPM`, bar: (m) => [clamp(m.floatMargin, 0, 1), m.floatMargin < 0 ? C.crit : m.floatMargin < 0.2 ? C.warn : C.ok],
    tip: (m) => `<b>Rod float margin</b><br>How much faster gravity can pull the rods down than the viscous crude holds them back. Negative means the rods lag the horsehead and the wire rope slackens.<br><span class="mut">Safe speed today: ${m.spmSafe.toFixed(1)} SPM.</span>` },
  { id: 'visc', label: 'Viscosity', dot: '#c98b5a', unit: 'cP', val: (m) => m.viscosity >= 1000 ? `${(m.viscosity / 1000).toFixed(1)}k` : m.viscosity.toFixed(0), sub: () => `at the pump intake`, bar: (m) => [clamp(Math.log10(m.viscosity) / 4, 0, 1), '#c98b5a'],
    tip: (m) => `<b>Crude viscosity at the pump</b><br>${m.viscosity.toFixed(0)} cP. Baghewala crude is ~10,000 cP cold; steam heat thins it by orders of magnitude.` },
  { id: 'temp', label: 'Sandface T', dot: C.inj, unit: '°C', val: (m) => m.sandfaceT.toFixed(0), sub: (m) => `heated r ${m.heatedRadius.toFixed(1)} m`, bar: (m) => [clamp((m.sandfaceT - 40) / 180, 0, 1), C.inj],
    tip: () => `<b>Sandface temperature</b><br>Formation temperature at the perforations; reservoir baseline is 47 °C.` },
  { id: 'energy', label: 'Lift energy', dot: '#b69cff', unit: 'kWh/bbl', val: (m) => m.kwhPerBbl.toFixed(1), sub: (m) => `motor ${m.motorKw.toFixed(1)} kW`, bar: (m) => [clamp(m.kwhPerBbl / 20, 0, 1), '#b69cff'],
    tip: () => `<b>Lift energy</b><br>Electricity spent per barrel of oil lifted.` },
  { id: 'sor', label: 'Steam–oil ratio', dot: '#e8e2d6', unit: '', val: (m) => (m.sor ? m.sor.toFixed(2) : '—'), sub: (m) => `${m.steamTons.toFixed(0)} t steam / cycle`, bar: (m) => [clamp(1 - (m.sor || 6) / 8, 0, 1), '#e8e2d6'],
    tip: () => `<b>Cumulative steam–oil ratio</b><br>Barrels of cold-water-equivalent steam per barrel of oil so far this cycle. Lower is better; under ~4 is economic.` },
  { id: 'co2', label: 'CO₂ intensity', dot: '#9fb0a0', unit: 'kg/bbl', val: (m) => (m.co2PerBbl ? m.co2PerBbl.toFixed(0) : '—'), sub: () => `steam + grid power`, bar: (m) => [clamp(m.co2PerBbl / 200, 0, 1), '#9fb0a0'],
    tip: () => `<b>CO₂ intensity</b><br>Gas burned for steam plus grid power for the pump, per barrel.` },
];

const TIPS = {
  spm: (m, st) => `<b>Pumping speed</b><br>${(st?.spmActual ?? 0).toFixed(1)} strokes per minute (set ${m.spm.toFixed(1)}).<br><span class="mut">Unit parks at top of stroke during injection and soak.</span>`,
  load: () => `<b>Polished-rod load</b><br>Live load on the rod string at the carrier bar, in kilonewtons.`,
  sandface: TIPS_T,
  visc: (m) => KPIS[4].tip(m),
  level: (m) => `<b>Dynamic fluid level</b><br>${m.fluidLevel.toFixed(0)} m down the annulus; pump sits at ${WELLBORE.pumpTop} m, so ${m.submergence.toFixed(0)} m of submergence.`,
  net: (m) => `<b>Net value today</b><br>Oil revenue less amortised steam and lift power.<br><span class="mut">₹6,000/bbl · ₹2,800/t steam · ₹8/kWh (planning prices)</span>`,
  battery: (m) => `<b>Thermal battery</b><br>${pct(m.thermalBattery)}% of the injected heat is still in the rock near the well.`,
  rh: (m) => `<b>Heated radius</b><br>${m.heatedRadius.toFixed(1)} m: how far the steam's heat has pushed into the Jodhpur Sandstone.`,
  cutoff: (m) => `<b>Days to economic cut-off</b><br>When the daily margin drops below the best whole-cycle average, re-steam.`,
};
function TIPS_T(m) { return KPIS[5].tip(m); }

/* ------------------------------------------------------------------ HUD */

export class Hud {
  constructor({ getSim }) {
    this.getSim = getSim;
    this.m = null;
    this.series = null; this.seriesKey = '';
    this.dyno = null; this.dynoKey = '';
    this.profile = null; this.profileKey = '';
    this.buildKpis();
    this.setupTooltips();
    this.baseNet = null;
  }

  buildKpis() {
    $('kpis').innerHTML = KPIS.map((k) => `<div class="kpi" data-kpi="${k.id}"><label><i style="background:${k.dot}"></i>${k.label}</label><div class="kv"><span>—</span><small>${k.unit}</small></div><div class="ksub"></div><div class="kbar"><b></b></div></div>`).join('');
    this.kpiEls = KPIS.map((k) => {
      const el = document.querySelector(`[data-kpi="${k.id}"]`);
      return { k, v: el.querySelector('.kv span'), s: el.querySelector('.ksub'), b: el.querySelector('.kbar b') };
    });
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
    const bind = (el, fn) => {
      el.addEventListener('pointerenter', (e) => this.m && show(fn(this.m, this.getSim()?.state), e));
      el.addEventListener('pointermove', move);
      el.addEventListener('pointerleave', () => tip.classList.remove('show'));
    };
    document.querySelectorAll('#ui [data-tip]').forEach((el) => TIPS[el.dataset.tip] && bind(el, TIPS[el.dataset.tip]));
    this.kpiEls.forEach(({ k }) => bind(document.querySelector(`[data-kpi="${k.id}"]`), k.tip));
    // chart hovers
    const cyc = $('c-cycle');
    cyc.addEventListener('pointermove', (e) => {
      if (!this.series) return;
      const r = cyc.getBoundingClientRect(), L = this.cycLayout;
      if (!L) return;
      const day = clamp(Math.round((e.clientX - r.left - L.x0) / (L.x1 - L.x0) * CYCLE.days), 0, CYCLE.days);
      const s = this.series;
      this.hoverDay = day;
      const ph = day < CYCLE.injEnd ? 'Steam injection' : day < CYCLE.soakEnd ? 'Soak' : 'Production';
      show(`<b>Day ${day}</b> <span class="mut">· ${ph}</span><br>Oil ${s.oil[day].toFixed(1)} BOPD <span class="mut">(P90–P10 ${s.oilP90[day].toFixed(0)}–${s.oilP10[day].toFixed(0)})</span><br>Sandface ${s.T[day].toFixed(0)} °C · ${s.mu[day] >= 1000 ? (s.mu[day] / 1000).toFixed(1) + 'k' : s.mu[day].toFixed(0)} cP<br><span class="mut">Safe speed ${s.spmSafe[day].toFixed(1)} SPM</span>`, e);
    });
    cyc.addEventListener('pointerleave', () => { this.hoverDay = null; tip.classList.remove('show'); });
    cyc.addEventListener('click', () => this.hoverDay != null && this.onPickDay?.(this.hoverDay));
    cyc.style.cursor = 'pointer';
  }

  /* per metrics tick (4 Hz) */
  update(m) {
    this.m = m;
    const sim = this.getSim();
    const st = sim.state;
    $('t-spm').textContent = st.spmActual.toFixed(1);
    $('t-temp').textContent = m.sandfaceT.toFixed(0);
    $('t-visc').textContent = m.viscosity >= 1000 ? `${(m.viscosity / 1000).toFixed(1)}k` : m.viscosity.toFixed(0);
    $('t-level').textContent = m.fluidLevel.toFixed(0);
    $('phase-sub').textContent = phaseName(m.phase);
    const dot = $('live-dot');
    dot.classList.toggle('steam', m.phase === 'INJECTION'); dot.classList.toggle('soak', m.phase === 'SOAK');

    $('v-net').textContent = inr(m.netPerDay);
    if (this.baseNet == null && m.phase === 'PRODUCTION') this.baseNet = m.netPerDay;
    const d = $('v-delta');
    if (m.phase !== 'PRODUCTION') { d.textContent = m.phase === 'INJECTION' ? 'steaming' : 'soaking'; d.className = 'delta'; }
    else {
      const lift = this.baseNet ? (m.netPerDay - this.baseNet) / Math.abs(this.baseNet) : 0;
      d.textContent = Math.abs(lift) < 0.005 ? 'baseline' : `${lift > 0 ? '▲' : '▼'} ${Math.abs(lift * 100).toFixed(1)}% vs start`;
      d.className = `delta ${lift > 0.005 ? 'up' : lift < -0.005 ? 'down' : ''}`;
    }

    // cycle panel
    const prodLen = CYCLE.days - CYCLE.soakEnd;
    $('cycle-sum').textContent = `Day ${m.cycleDay.toFixed(0)} / ${CYCLE.days}`;
    $('ring-phase').textContent = phaseName(m.phase);
    $('ring-day').textContent = m.cycleDay.toFixed(0);
    $('ring-sub').textContent = m.phase === 'INJECTION' ? `day ${m.dayInPhase.toFixed(0)} of ${CYCLE.injEnd}` : m.phase === 'SOAK' ? `day ${m.dayInPhase.toFixed(0)} of ${CYCLE.soakEnd - CYCLE.injEnd}` : `day ${m.dayInPhase.toFixed(0)} of ${prodLen}`;
    $('s-battery').textContent = `${pct(m.thermalBattery)}%`;
    $('s-rh').textContent = `${m.heatedRadius.toFixed(1)} m`;
    $('s-cutoff').textContent = m.phase === 'PRODUCTION' ? (m.daysToCutoff > 0 ? `${m.daysToCutoff.toFixed(0)} d` : 'now') : '—';
    this.drawRing(m);

    // advisor
    const r = m.recommendation;
    $('adv-title').textContent = r.title;
    $('adv-detail').textContent = r.detail;
    $('adv-conf').textContent = `${pct(r.confidence)}% conf.`;
    const dl = [];
    const chip = (v, label, goodIfUp) => { if (Math.abs(v) < 0.005) return; const good = goodIfUp ? v > 0 : v < 0; dl.push(`<span class="${good ? 'good' : 'bad'}">${v > 0 ? '+' : '−'}${Math.abs(v * 100).toFixed(0)}% ${label}</span>`); };
    chip(r.deltas.oil, 'oil', true); chip(r.deltas.float, 'float', true); chip(r.deltas.energy, 'kWh/bbl', false);
    $('adv-deltas').innerHTML = dl.join('');
    const can = m.phase === 'PRODUCTION' && (Math.abs(r.spm - m.spm) > 0.05 || Math.abs(r.kd - m.kd) > 0.001);
    $('adv-apply').disabled = !can;
    $('adv-apply').textContent = can ? `Apply · ${r.spm.toFixed(1)} SPM` : 'Settings optimal';

    // KPIs
    for (const { k, v, s, b } of this.kpiEls) {
      v.textContent = k.val(m); s.textContent = k.sub(m);
      const [f, col] = k.bar(m);
      b.style.width = `${clamp(f, 0, 1) * 100}%`; b.style.background = col;
    }
    // limits + alerts
    const lim = [
      ['Float margin', m.floatMargin, `${pct(m.floatMargin)}%`, (v) => 1 - clamp(v, -0.2, 1), 0.85],
      ['Goodman', m.goodman, m.goodman.toFixed(2), (v) => clamp(v / 1.2, 0, 1), 0.75],
      ['Gearbox torque', m.torquePct, `${pct(m.torquePct)}%`, (v) => clamp(v / 1.2, 0, 1), 0.833],
      ['Fillage', m.fillage, `${pct(m.fillage)}%`, (v) => 1 - clamp(v, 0, 1), 0.3],
    ];
    $('limits').innerHTML = lim.map(([l, v, txt, f, redAt]) => {
      const x = f(v), col = x > redAt ? C.crit : x > redAt - 0.15 ? C.warn : C.ok;
      return `<div class="lim"><label>${l}<b>${m.phase === 'PRODUCTION' ? txt : '—'}</b></label><div class="meter"><b style="width:${m.phase === 'PRODUCTION' ? x * 100 : 0}%;background:${col}"></b><i style="left:${redAt * 100}%"></i></div></div>`;
    }).join('');
    const lc = { ok: C.ok, warn: C.warn, crit: C.crit };
    $('alerts').innerHTML = m.alerts.map((a) => `<li><i style="background:${lc[a.level]}"></i><span>${a.text}</span></li>`).join('');

    // cached curve sets
    const sk = `${m.spm.toFixed(2)}|${m.kd}`;
    if (sk !== this.seriesKey) { this.series = sim.series(); this.seriesKey = sk; }
    const dk = `${m.spm.toFixed(2)}|${m.kd}|${m.cycleDay.toFixed(1)}`;
    if (dk !== this.dynoKey) { this.dyno = m.phase === 'PRODUCTION' ? sim.dynoCard(160) : null; this.dynoKey = dk; }
    const pk = `${m.cycleDay.toFixed(1)}|${m.spm.toFixed(2)}`;
    if (pk !== this.profileKey) { this.profile = sim.profile(); this.profileKey = pk; }
    $('dyno-cls').textContent = this.dyno ? `${this.dyno.cls} · ${pct(this.dyno.clsConf)}%` : 'unit parked';
    $('dyno-cls').style.color = !this.dyno ? C.mute : this.dyno.cls === 'NORMAL' ? C.ok : this.dyno.cls === 'ROD FLOAT RISK' ? C.crit : C.warn;
    this.drawCycle(m); this.drawProfile(m);
  }

  /* per frame: live bits */
  frame() {
    const sim = this.getSim();
    if (!sim || !this.m) return;
    $('t-load').textContent = sim.state.load.toFixed(0);
    if (!document.getElementById('metrics').classList.contains('open')) return;
    this.drawDyno(sim.state);
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
    // cut-off tick
    if (m.phase === 'PRODUCTION') {
      const cd = Math.min(CYCLE.days, d + m.daysToCutoff), a = A(cd);
      g.beginPath(); g.moveTo(cx + Math.cos(a) * (R - 9), cy + Math.sin(a) * (R - 9)); g.lineTo(cx + Math.cos(a) * (R + 5), cy + Math.sin(a) * (R + 5));
      g.strokeStyle = C.ok; g.lineWidth = 2; g.stroke();
    }
    // thermal battery inner arc
    arc(0, CYCLE.days * m.thermalBattery, 'rgba(240,160,75,0.55)', 2, R - 12);
    const a = A(d);
    g.beginPath(); g.arc(cx + Math.cos(a) * R, cy + Math.sin(a) * R, 5, 0, Math.PI * 2); g.fillStyle = '#fff'; g.fill();
    g.shadowColor = 'rgba(0,0,0,0.4)';
  }

  drawCycle(m) {
    const f = fit($('c-cycle'));
    if (!f || !this.series) return;
    const { g, w, h } = f, s = this.series;
    const x0 = 30, x1 = w - 30, y0 = 8, y1 = h - 16;
    this.cycLayout = { x0, x1 };
    const X = (d) => x0 + (d / CYCLE.days) * (x1 - x0);
    const oMax = Math.max(20, ...s.oilP10) * 1.08;
    const Y = (o) => y1 - (o / oMax) * (y1 - y0);
    const YT = (t) => y1 - ((t - 40) / 220) * (y1 - y0);
    // phase shading
    g.fillStyle = 'rgba(255,122,61,0.1)'; g.fillRect(X(0), y0, X(CYCLE.injEnd) - X(0), y1 - y0);
    g.fillStyle = 'rgba(255,195,90,0.08)'; g.fillRect(X(CYCLE.injEnd), y0, X(CYCLE.soakEnd) - X(CYCLE.injEnd), y1 - y0);
    g.font = FONT; g.fillStyle = C.mute; g.textAlign = 'center';
    g.fillText('STEAM', (X(0) + X(CYCLE.injEnd)) / 2, y0 + 11);
    // grid
    g.strokeStyle = C.grid; g.lineWidth = 1;
    for (let o = 0; o <= oMax; o += 20) { g.beginPath(); g.moveTo(x0, Y(o)); g.lineTo(x1, Y(o)); g.stroke(); g.textAlign = 'right'; g.fillText(o, x0 - 5, Y(o) + 3); }
    g.textAlign = 'center';
    for (let d = 0; d <= CYCLE.days; d += 20) g.fillText(d, X(d), h - 3);
    g.textAlign = 'left'; g.fillStyle = 'rgba(240,160,75,0.7)';
    for (const t of [100, 200]) g.fillText(`${t}°`, x1 + 4, YT(t) + 3);
    // P10–P90 band
    g.beginPath();
    s.day.forEach((d, i) => (i ? g.lineTo(X(d), Y(s.oilP10[i])) : g.moveTo(X(d), Y(s.oilP10[i]))));
    for (let i = s.day.length - 1; i >= 0; i--) g.lineTo(X(s.day[i]), Y(s.oilP90[i]));
    g.closePath(); g.fillStyle = 'rgba(255,255,255,0.09)'; g.fill();
    // temperature
    g.beginPath(); s.day.forEach((d, i) => (i ? g.lineTo(X(d), YT(s.T[i])) : g.moveTo(X(d), YT(s.T[i]))));
    g.setLineDash([4, 3]); g.strokeStyle = 'rgba(240,160,75,0.8)'; g.lineWidth = 1.3; g.stroke(); g.setLineDash([]);
    // oil, with the elapsed part brighter
    const line = (from, to, col, lw) => { g.beginPath(); let first = true; s.day.forEach((d, i) => { if (d < from || d > to) return; first ? g.moveTo(X(d), Y(s.oil[i])) : g.lineTo(X(d), Y(s.oil[i])); first = false; }); g.strokeStyle = col; g.lineWidth = lw; g.stroke(); };
    line(0, CYCLE.days, 'rgba(255,255,255,0.35)', 1.6);
    line(0, Math.ceil(m.cycleDay), '#fff', 2);
    // cut-off
    if (m.phase === 'PRODUCTION') {
      const cd = Math.min(CYCLE.days, m.cycleDay + m.daysToCutoff);
      g.setLineDash([3, 3]); g.strokeStyle = 'rgba(95,227,154,0.8)'; g.beginPath(); g.moveTo(X(cd), y0); g.lineTo(X(cd), y1); g.stroke(); g.setLineDash([]);
      g.fillStyle = C.ok; g.textAlign = cd > 100 ? 'right' : 'left'; g.fillText('cut-off', X(cd) + (cd > 100 ? -4 : 4), y0 + 11);
    }
    // now marker
    const di = clamp(Math.round(m.cycleDay), 0, CYCLE.days);
    g.strokeStyle = 'rgba(255,255,255,0.5)'; g.beginPath(); g.moveTo(X(m.cycleDay), y0); g.lineTo(X(m.cycleDay), y1); g.stroke();
    g.beginPath(); g.arc(X(m.cycleDay), Y(m.oilRate || s.oil[di]), 4, 0, Math.PI * 2); g.fillStyle = '#fff'; g.fill();
    if (this.hoverDay != null) { g.strokeStyle = 'rgba(255,255,255,0.25)'; g.beginPath(); g.moveTo(X(this.hoverDay), y0); g.lineTo(X(this.hoverDay), y1); g.stroke(); }
  }

  drawDyno(st) {
    const f = fit($('c-dyno'));
    if (!f) return;
    const { g, w, h } = f, d = this.dyno;
    const x0 = 30, x1 = w - 8, y0 = 6, y1 = h - 14;
    if (!d) {
      g.font = FONT; g.fillStyle = C.mute; g.textAlign = 'center';
      g.fillText(this.m.phase === 'INJECTION' ? 'Unit parked while steam is injected' : 'Unit parked during the soak', w / 2, h / 2);
      return;
    }
    const fMin = Math.min(0, d.fMin), fMax = d.fMax * 1.08;
    const X = (x) => x0 + (x / d.xMax) * (x1 - x0), Y = (v) => y1 - ((v - fMin) / (fMax - fMin)) * (y1 - y0);
    g.strokeStyle = C.grid; g.lineWidth = 1; g.font = FONT; g.fillStyle = C.mute;
    const step = fMax > 120 ? 40 : 20;
    for (let v = 0; v <= fMax; v += step) { g.beginPath(); g.moveTo(x0, Y(v)); g.lineTo(x1, Y(v)); g.stroke(); g.textAlign = 'right'; g.fillText(v, x0 - 5, Y(v) + 3); }
    g.textAlign = 'center'; g.fillText('stroke →', (x0 + x1) / 2, h - 2);
    const loop = (pts, col, lw, fill) => {
      g.beginPath(); pts.forEach((p, i) => (i ? g.lineTo(X(p.x), Y(p.f)) : g.moveTo(X(p.x), Y(p.f)))); g.closePath();
      if (fill) { g.fillStyle = fill; g.fill(); }
      g.strokeStyle = col; g.lineWidth = lw; g.stroke();
    };
    loop(d.downhole, C.blue, 1.4, 'rgba(124,196,255,0.08)');
    loop(d.surface, '#fff', 1.8, 'rgba(255,255,255,0.05)');
    // live rod position on the surface card
    g.beginPath(); g.arc(X(clamp(st.rodPos, 0, d.xMax)), Y(st.load), 4, 0, Math.PI * 2); g.fillStyle = C.heat; g.fill();
    g.beginPath(); g.arc(X(clamp(st.rodPos, 0, d.xMax)), Y(st.load), 8, 0, Math.PI * 2); g.strokeStyle = 'rgba(240,160,75,0.4)'; g.lineWidth = 1; g.stroke();
  }

  drawProfile(m) {
    const f = fit($('c-profile'));
    if (!f || !this.profile) return;
    const { g, w, h } = f, p = this.profile;
    const x0 = 26, x1 = w - 6, y0 = 4, y1 = h - 14;
    const Y = (z) => y0 + (z / 1250) * (y1 - y0), X = (t) => x0 + ((t - 20) / 220) * (x1 - x0);
    g.font = FONT; g.fillStyle = C.mute; g.strokeStyle = C.grid;
    for (const z of [0, 500, 1000]) { g.beginPath(); g.moveTo(x0, Y(z)); g.lineTo(x1, Y(z)); g.stroke(); g.textAlign = 'right'; g.fillText(z ? `${z / 1000}k` : '0', x0 - 4, Y(z) + 3); }
    g.textAlign = 'center';
    for (const t of [50, 150]) g.fillText(`${t}°`, X(t), h - 2);
    // reservoir band
    g.fillStyle = 'rgba(240,160,75,0.08)'; g.fillRect(x0, Y(1080), x1 - x0, Y(1160) - Y(1080));
    if (p.depositionTop != null) { g.fillStyle = 'rgba(255,195,90,0.14)'; g.fillRect(x0, Y(p.depositionTop), x1 - x0, Y(p.depositionBot) - Y(p.depositionTop)); }
    const line = (arr, col, lw, dash) => { g.beginPath(); arr.forEach((t, i) => (i ? g.lineTo(X(t), Y(p.depth[i])) : g.moveTo(X(t), Y(p.depth[i])))); g.setLineDash(dash || []); g.strokeStyle = col; g.lineWidth = lw; g.stroke(); g.setLineDash([]); };
    line(p.Tformation, 'rgba(255,255,255,0.4)', 1.2, [3, 3]);
    line(p.Tfluid, C.heat, 1.8);
    // pump + level
    g.strokeStyle = 'rgba(124,196,255,0.7)'; g.beginPath(); g.moveTo(x0, Y(m.fluidLevel)); g.lineTo(x1, Y(m.fluidLevel)); g.stroke();
    g.fillStyle = C.blue; g.textAlign = 'right'; g.fillText('fluid', x1, Y(m.fluidLevel) - 3);
    g.fillStyle = '#fff'; g.fillRect(x0 + 2, Y(WELLBORE.pumpTop) - 2, 8, 4);
  }
}
