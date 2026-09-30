// Section A–A′: the cream "blueprint" view of the well. The 3D camera flattens into a
// near-orthographic elevation of the block's front face; this drawing crystallises over it on
// exactly the same world→screen mapping (a sweep from the surface down), then eases out to its
// working layout with depth tracks. Everything is live: the pumping unit strokes, the plunger and
// valves move, and the heated zone grows and decays as the steam cycle plays.
import { STRATA, WELLBORE, UNIT, BLOCK, KNOTS, PIT_DEPTH, depthToY, yToDepth, unitPose, STROKE } from './rig.js';
import { CYCLE, viscosityCp } from './sim.js';
import { fluid, plan, derived } from './twin-data.js';

const lerp = (a, b, t) => a + (b - a) * t;
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const smooth = (a, b, x) => { const t = clamp((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
const ease = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const INK = (a = 1) => `rgba(42,36,27,${a})`;
const BLUE = (a = 1) => `rgba(21,102,181,${a})`;
const HEAT = (a = 1) => `rgba(200,74,22,${a})`;
const PAPER = '#f1ebdf';
const FONT = (w, s) => `${w} ${s}px Inter, -apple-system, sans-serif`;
const R = WELLBORE.r;
const RES = STRATA.find((s) => s.reservoir);
const Y_RT = depthToY(RES.top), Y_RB = depthToY(RES.bot);
// world rectangle the drawing covers (the block's front face plus the surface equipment)
const WORLD = { x0: BLOCK.x0, x1: BLOCK.x1, y0: -PIT_DEPTH, y1: 9.5 };
const SPEEDS = [1, 2, 4, 8, 16];

const ICON = {
  first: '<svg viewBox="0 0 24 24" width="14" height="14"><path d="M6 5v14M19 5l-9 7 9 7z" fill="currentColor" stroke="currentColor" stroke-width="1.5"/></svg>',
  prev: '<svg viewBox="0 0 24 24" width="14" height="14"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  play: '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M7 5l12 7-12 7z" fill="currentColor"/></svg>',
  pause: '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M7 5h4v14H7zM13 5h4v14h-4z" fill="currentColor"/></svg>',
  next: '<svg viewBox="0 0 24 24" width="14" height="14"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  last: '<svg viewBox="0 0 24 24" width="14" height="14"><path d="M18 5v14M5 5l9 7-9 7z" fill="currentColor" stroke="currentColor" stroke-width="1.5"/></svg>',
};

/* ------------------------------------------------------------------ formation temperature (mirrors the 3D shader, minus its noise) */
function formationT(x, y, tPeak, rh) {
  const geo = 29 + 0.0152 * yToDepth(y);
  const mid = (Y_RT + Y_RB) / 2, half = (Y_RT - Y_RB) / 2;
  const dv = Math.max(Math.abs(y - mid) - half, 0);
  const vert = Math.exp(-(dv * dv) / 1.6);
  const rr = Math.abs(x) / Math.max(rh, 0.5);
  return geo + Math.max(tPeak - geo, 0) * Math.exp(-rr * rr * 1.6) * vert;
}

// marching squares → line segments for one iso-level over a regular grid
function isoSegments(F, nx, ny, lvl) {
  const segs = [];
  const at = (i, j) => F[j * nx + i];
  const interp = (i0, j0, i1, j1) => { const a = at(i0, j0), b = at(i1, j1), t = (lvl - a) / (b - a || 1e-9); return [i0 + (i1 - i0) * t, j0 + (j1 - j0) * t]; };
  for (let j = 0; j < ny - 1; j++) for (let i = 0; i < nx - 1; i++) {
    const c = (at(i, j) > lvl) | ((at(i + 1, j) > lvl) << 1) | ((at(i + 1, j + 1) > lvl) << 2) | ((at(i, j + 1) > lvl) << 3);
    if (c === 0 || c === 15) continue;
    const e = [interp(i, j, i + 1, j), interp(i + 1, j, i + 1, j + 1), interp(i, j + 1, i + 1, j + 1), interp(i, j, i, j + 1)];
    const T = { 1: [[3, 0]], 2: [[0, 1]], 3: [[3, 1]], 4: [[1, 2]], 5: [[3, 0], [1, 2]], 6: [[0, 2]], 7: [[3, 2]], 8: [[2, 3]], 9: [[0, 2]], 10: [[0, 1], [2, 3]], 11: [[1, 2]], 12: [[1, 3]], 13: [[0, 1]], 14: [[0, 3]] }[c];
    for (const [a, b] of T) segs.push([e[a], e[b]]);
  }
  return segs;
}

function hatchPattern(g, kind) {
  const c = document.createElement('canvas'), s = kind === 'brick' ? 24 : 14;
  c.width = s; c.height = kind === 'brick' ? 12 : s;
  const h = c.getContext('2d');
  h.strokeStyle = INK(0.5); h.fillStyle = INK(0.5); h.lineWidth = 0.8;
  if (kind === 'dots') { h.beginPath(); h.arc(3, 4, 0.9, 0, 7); h.arc(10, 11, 0.9, 0, 7); h.fill(); }
  else if (kind === 'dash') { h.beginPath(); h.moveTo(1, 4); h.lineTo(7, 4); h.moveTo(8, 11); h.lineTo(13, 11); h.stroke(); }
  else if (kind === 'brick') { h.beginPath(); h.moveTo(0, 0.5); h.lineTo(24, 0.5); h.moveTo(0, 6.5); h.lineTo(24, 6.5); h.moveTo(6, 0.5); h.lineTo(6, 6.5); h.moveTo(18, 6.5); h.lineTo(18, 12); h.stroke(); }
  else if (kind === 'cross') { h.beginPath(); h.moveTo(2, 3); h.lineTo(5, 6); h.moveTo(5, 3); h.lineTo(2, 6); h.moveTo(9, 10); h.lineTo(12, 13); h.moveTo(12, 10); h.lineTo(9, 13); h.stroke(); }
  return g.createPattern(c, 'repeat');
}

export class SectionView {
  constructor({ root, getSim, onPlayChange }) {
    this.root = root; this.getSim = getSim; this.onPlayChange = onPlayChange;
    this.canvas = document.createElement('canvas'); this.canvas.className = 'sec-canvas';
    this.g = this.canvas.getContext('2d');
    root.appendChild(this.canvas);
    this.buildUI();
    this.active = false;
    this.anim = { k: 0, from: 0, to: 0, t: 0, dur: 1, resolve: null };
    this.user = { zoom: 1, panX: 0, panY: 0 };
    this.overlay = 'heat'; this.showTracks = true; this.showLabels = true;
    this.playing = false; this.speedIdx = 2;
    this.fieldKey = ''; this.field = null;
    this.hoverPt = null;
    this.patterns = {};
    this.bindInput();
    this.resize();
    window.addEventListener('resize', () => this.active && this.resize());
  }

  /* ---------------------------------------------------------------- DOM */
  buildUI() {
    const ui = document.createElement('div'); ui.className = 'sec-ui'; this.ui = ui;
    ui.innerHTML = `
      <div class="sec-hud">
        <div class="brand"><span class="dot"></span>MANTLE <em>Well section</em></div>
        <h1>A–A′<small>BGW-17 · looking north</small></h1>
        <div class="sub">True-scale reservoir · overburden compressed · heat from the live cycle</div>
        <div class="sec-stats">
          <div><label>Cycle day</label><span data-k="day">0</span><small data-k="phase">—</small></div>
          <div><label>Sandface</label><span data-k="t">0</span><small>°C</small></div>
          <div><label>Heated r</label><span data-k="rh">0</span><small>m</small></div>
          <div><label>Viscosity</label><span data-k="mu">0</span><small>cP at pump</small></div>
          <div><label>Oil</label><span data-k="oil">0</span><small>BOPD</small></div>
        </div>
      </div>
      <div class="sec-legend lpanel">
        <div class="seg" data-seg="overlay"><button data-v="heat" class="active">Isotherms</button><button data-v="visc">Mobility</button><button data-v="none">Geology</button></div>
        <div class="seg" data-seg="zoom"><button data-v="full" class="active">Full section</button><button data-v="pump">Pump</button><button data-v="res">Reservoir</button></div>
        <div class="leg" data-k="legend" hidden></div>
        <div class="tblock">
          <div class="tb-row tb-2"><div><label>Well</label>BGW-17 · Baghewala</div><div><label>Sheet</label>A–A′ · rev B</div></div>
          <div class="tb-row tb-3"><div><label>Crude</label><span data-k="fApi">—</span></div><div><label>Asphaltene</label><span data-k="fAsph">—</span></div><div><label>Dead oil</label><span data-k="fDead">—</span></div></div>
          <div class="tb-row tb-3"><div><label>T res</label><span data-k="fT">—</span></div><div><label>P res</label><span data-k="fP">—</span></div><div><label>PIP</label><span data-k="pip">—</span></div></div>
        </div>
      </div>
      <div class="sec-dock">
        <div class="sec-timeline lpanel">
          <div class="tl-top">
            <div class="tl-move"><span class="tl-badge" data-k="badge">Production</span><b data-k="title">—</b><span data-k="detail"></span></div>
            <div class="tl-time"><b data-k="now">Day 0</b> / ${CYCLE.days} d</div>
          </div>
          <canvas class="tl-track"></canvas>
          <div class="tl-controls">
            <div class="tl-buttons">
              <button data-a="first" title="Start of cycle (Home)">${ICON.first}</button>
              <button data-a="prev" title="Back one day (←)">${ICON.prev}</button>
              <button data-a="play" class="primary" title="Play the cycle (Space)">${ICON.play}</button>
              <button data-a="next" title="Forward one day (→)">${ICON.next}</button>
              <button data-a="last" title="End of cycle (End)">${ICON.last}</button>
            </div>
            <div class="seg speed" data-seg="speed">${SPEEDS.map((s, i) => `<button data-v="${i}" class="${i === this.speedIdx ? 'active' : ''}">${s} d/s</button>`).join('')}</div>
            <div class="tl-toggles">
              <button data-t="tracks" class="on" title="Depth tracks">Tracks</button>
              <button data-t="labels" class="on" title="Callouts">Callouts</button>
            </div>
          </div>
        </div>
        <div class="sec-card lpanel">
          <div class="sc-head"><span>Thermal battery</span><b data-k="bat">0%</b></div>
          <canvas></canvas>
        </div>
      </div>`;
    this.root.appendChild(ui);
    this.k = {};
    ui.querySelectorAll('[data-k]').forEach((el) => (this.k[el.dataset.k] = el));
    this.track = ui.querySelector('.tl-track');
    this.cardCanvas = ui.querySelector('.sec-card canvas');
    this.btnPlay = ui.querySelector('[data-a="play"]');
    ui.querySelectorAll('[data-a]').forEach((b) => (b.onclick = () => this.action(b.dataset.a)));
    ui.querySelectorAll('[data-seg]').forEach((seg) => seg.querySelectorAll('button').forEach((b) => (b.onclick = () => {
      seg.querySelectorAll('button').forEach((x) => x.classList.toggle('active', x === b));
      const v = b.dataset.v, s = seg.dataset.seg;
      if (s === 'overlay') { this.overlay = v; this.syncLegend(); }
      if (s === 'speed') this.speedIdx = +v;
      if (s === 'zoom') this.zoomPreset(v);
    })));
    ui.querySelectorAll('[data-t]').forEach((b) => (b.onclick = () => {
      b.classList.toggle('on');
      if (b.dataset.t === 'tracks') { this.showTracks = b.classList.contains('on'); this.relayout(); }
      else this.showLabels = b.classList.contains('on');
    }));
    // timeline scrubbing
    let scrub = false;
    const toDay = (e) => { const r = this.track.getBoundingClientRect(); return clamp((e.clientX - r.left - 8) / (r.width - 16), 0, 1) * CYCLE.days; };
    this.track.addEventListener('pointerdown', (e) => { scrub = true; this.track.setPointerCapture(e.pointerId); this.setDay(toDay(e)); });
    this.track.addEventListener('pointermove', (e) => scrub && this.setDay(toDay(e)));
    this.track.addEventListener('pointerup', () => (scrub = false));
    this.syncLegend();
  }

  syncLegend() {
    const sw = STRATA.map((s) => `<span><i style="background:${s.color}"></i>${s.name}</span>`).join('');
    const grad = this.overlay === 'heat'
      ? `<div class="row"><span>47°</span><i class="grad" style="background:linear-gradient(90deg,rgba(255,200,120,0.25),#f08a3c,#c8401a)"></i><span>220 °C</span></div>`
      : this.overlay === 'visc'
        ? `<div class="row"><span>10k cP</span><i class="grad" style="background:linear-gradient(90deg,rgba(80,150,200,0.1),#4f9dde,#1566b5)"></i><span>50 cP</span></div>`
        : '';
    this.k.legend.innerHTML = grad;
    void sw;
  }

  action(a) {
    const sim = this.getSim(), d = sim.params().day;
    if (a === 'play') this.setPlaying(!this.playing);
    if (a === 'first') this.setDay(0);
    if (a === 'last') this.setDay(CYCLE.days);
    if (a === 'prev') this.setDay(Math.ceil(d) - 1);
    if (a === 'next') this.setDay(Math.floor(d) + 1);
  }
  setPlaying(on) {
    this.playing = on;
    this.btnPlay.innerHTML = on ? ICON.pause : ICON.play;
    this.onPlayChange?.(on);
  }
  setDay(d) { this.getSim().set({ cycleDay: clamp(d, 0, CYCLE.days) }); }

  zoomPreset(v) {
    const b = this.baseLayout();
    const target = v === 'pump'
      ? { zoom: 3.2, cx: 0, cy: depthToY(1080) + 1 }
      : v === 'res' ? { zoom: 1.9, cx: 3, cy: (Y_RT + Y_RB) / 2 } : { zoom: 1, cx: b.cx, cy: b.cy };
    this.zoomTo = { zoom: target.zoom, panX: target.cx - b.cx, panY: target.cy - b.cy };
  }

  bindInput() {
    const c = this.canvas;
    let drag = null;
    c.addEventListener('wheel', (e) => {
      e.preventDefault();
      const f = Math.exp(-e.deltaY * 0.0015);
      const before = this.toWorld(e.clientX, e.clientY);
      this.user.zoom = clamp(this.user.zoom * f, 0.6, 8);
      this.zoomTo = null;
      this.layoutNow();
      const after = this.toWorld(e.clientX, e.clientY);
      this.user.panX += before.x - after.x; this.user.panY += before.y - after.y;
    }, { passive: false });
    c.addEventListener('pointerdown', (e) => { drag = { x: e.clientX, y: e.clientY, px: this.user.panX, py: this.user.panY }; c.setPointerCapture(e.pointerId); this.zoomTo = null; });
    c.addEventListener('pointermove', (e) => {
      if (drag) { const ppm = this.view.ppm; this.user.panX = drag.px - (e.clientX - drag.x) / ppm; this.user.panY = drag.py + (e.clientY - drag.y) / ppm; }
      this.hoverPt = { sx: e.clientX, sy: e.clientY };
    });
    c.addEventListener('pointerup', () => (drag = null));
    c.addEventListener('pointerleave', () => { this.hoverPt = null; this.tip(null); });
    c.addEventListener('dblclick', () => { this.zoomTo = { zoom: 1, panX: 0, panY: 0 }; });
  }

  tip(html, x, y) {
    const t = document.getElementById('tooltip');
    if (!html) { t.classList.remove('show', 'light'); return; }
    t.innerHTML = html; t.classList.add('show', 'light');
    const r = t.getBoundingClientRect();
    t.style.left = `${x + r.width + 28 > innerWidth ? x - r.width - 28 : x}px`;
    t.style.top = `${y + r.height + 28 > innerHeight ? y - r.height - 28 : y}px`;
  }

  /* ---------------------------------------------------------------- layout */
  resize() {
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    this.w = window.innerWidth; this.h = window.innerHeight; this.dpr = dpr;
    this.canvas.width = this.w * dpr; this.canvas.height = this.h * dpr;
  }
  // The pose the 3D camera flattens into: the whole face, centred, generous margins.
  startLayout(w = window.innerWidth, h = window.innerHeight) {
    const ww = WORLD.x1 - WORLD.x0, wh = WORLD.y1 - WORLD.y0;
    const ppm = Math.min((w - 120) / ww, (h - 150) / wh);
    return { ppm, cx: (WORLD.x0 + WORLD.x1) / 2, cy: (WORLD.y0 + WORLD.y1) / 2 - 1.5 };
  }
  // Working layout: room for the header, the dock and (optionally) the depth tracks on the right.
  baseLayout() {
    const w = this.w, h = this.h;
    const left = 70, right = this.showTracks ? 372 : 70, top = 150, bottom = 214;
    const ww = WORLD.x1 - WORLD.x0, wh = WORLD.y1 - WORLD.y0;
    const ppm = Math.min((w - left - right) / ww, (h - top - bottom) / wh);
    const cxScreen = left + (w - left - right) / 2, cyScreen = top + (h - top - bottom) / 2;
    const cx = (WORLD.x0 + WORLD.x1) / 2 - (cxScreen - w / 2) / ppm;
    const cy = (WORLD.y0 + WORLD.y1) / 2 + (cyScreen - h / 2) / ppm;
    return { ppm, cx, cy };
  }
  relayout() { this.layoutNow(); }
  layoutNow() {
    const k = this.anim.k, mix = ease(smooth(0.45, 0.95, k));
    const f = this.from || this.startLayout(this.w, this.h), b = this.baseLayout();
    const ppm = lerp(f.ppm, b.ppm * this.user.zoom, mix);
    const cx = lerp(f.cx, b.cx + this.user.panX, mix), cy = lerp(f.cy, b.cy + this.user.panY, mix);
    this.view = { ppm, cx, cy, X: (x) => this.w / 2 + (x - cx) * ppm, Y: (y) => this.h / 2 - (y - cy) * ppm };
  }
  toWorld(sx, sy) { const v = this.view; return { x: v.cx + (sx - this.w / 2) / v.ppm, y: v.cy - (sy - this.h / 2) / v.ppm }; }

  /* ---------------------------------------------------------------- lifecycle */
  enter({ from, onCovered }) {
    this.active = true; this.root.classList.add('active');
    this.resize();
    this.from = from;
    this.user = { zoom: 1, panX: 0, panY: 0 }; this.zoomTo = null;
    this.ui.querySelectorAll('[data-seg="zoom"] button').forEach((b, i) => b.classList.toggle('active', i === 0));
    this.onCovered = onCovered;
    return this.animate(0, 1, 2.6);
  }
  exit({ to, onUncover }) {
    this.setPlaying(false);
    this.tip(null);
    // ease back to the camera's pose first, then dissolve upward
    this.from = to;
    this.onUncover = onUncover;
    return this.animate(1, 0, 2.0).then(() => { this.active = false; this.root.classList.remove('active'); });
  }
  animate(k0, k1, dur) {
    return new Promise((resolve) => { this.anim = { k: k0, from: k0, to: k1, t: 0, dur, resolve }; });
  }

  /* ---------------------------------------------------------------- per frame */
  frame(dt, theta) {
    if (!this.active) return;
    const a = this.anim;
    if (a.resolve) {
      a.t = Math.min(1, a.t + dt / a.dur);
      a.k = lerp(a.from, a.to, a.t);
      if (a.to === 1 && a.k >= 0.5 && this.onCovered) { this.onCovered(); this.onCovered = null; }
      if (a.to === 0 && a.k <= 0.5 && this.onUncover) { this.onUncover(); this.onUncover = null; }
      if (a.t >= 1) { const r = a.resolve; a.resolve = null; r(); }
    }
    const sim = this.getSim();
    if (this.playing && a.k > 0.95) {
      const d = sim.params().day + dt * SPEEDS[this.speedIdx];
      if (d >= CYCLE.days) { this.setDay(CYCLE.days); this.setPlaying(false); } else this.setDay(d);
    }
    if (this.zoomTo) {
      const z = this.zoomTo, e = 1 - Math.exp(-dt * 5);
      this.user.zoom = lerp(this.user.zoom, z.zoom, e); this.user.panX = lerp(this.user.panX, z.panX, e); this.user.panY = lerp(this.user.panY, z.panY, e);
      if (Math.abs(this.user.zoom - z.zoom) < 1e-3 && Math.abs(this.user.panX - z.panX) < 1e-3) this.zoomTo = null;
    }
    this.layoutNow();
    const m = sim.metrics();                              // API state; null until it answers
    this.draw(a.k, m, sim.state, theta);
    this.ui.style.opacity = smooth(0.7, 1, a.k);
    this.ui.style.pointerEvents = a.k > 0.95 ? 'auto' : 'none';
    this.updateFluid(sim);
    if (m) {
      this.updateHUD(m);
      this.drawTimeline(m, sim);
      this.drawCard(m, sim);
      if (this.hoverPt && a.k > 0.95) this.hover(m);
    } else this.hudUnavailable(sim);
  }

  updateFluid(sim) {
    const f = fluid(sim), k = this.k;
    k.fApi.textContent = f ? `${f.api}° API` : '—';
    k.fAsph.textContent = f ? `${f.asphaltene} wt%` : '—';
    k.fDead.textContent = f ? `${(f.deadOilCp / 1000).toFixed(1)}k cP` : '—';
    k.fT.textContent = f ? `${f.tRes} °C` : '—';
    k.fP.textContent = f ? `${f.pRes} MPa` : '—';
  }

  hudUnavailable(sim) {
    const k = this.k, off = !sim.api?.online;
    for (const id of ['day', 't', 'rh', 'mu', 'oil', 'bat', 'pip']) k[id].textContent = '—';
    k.phase.textContent = ''; k.now.textContent = '—';
    k.badge.className = 'tl-badge'; k.badge.textContent = off ? 'Offline' : 'Connecting';
    k.title.textContent = off ? 'Mantle API unavailable' : 'Connecting to the Mantle API…';
    k.detail.textContent = off ? 'No data is shown until the backend is reachable.' : '';
    for (const c of [this.track, this.cardCanvas]) { const g = c.getContext('2d'); g.clearRect(0, 0, c.width, c.height); }
  }

  updateHUD(m) {
    const k = this.k;
    k.day.textContent = m.cycleDay.toFixed(0);
    k.phase.textContent = m.phase === 'INJECTION' ? 'steaming' : m.phase === 'SOAK' ? 'soaking' : 'producing';
    k.t.textContent = m.sandfaceT.toFixed(0);
    k.rh.textContent = m.heatedRadius.toFixed(1);
    k.mu.textContent = m.viscosity >= 1000 ? `${(m.viscosity / 1000).toFixed(1)}k` : m.viscosity.toFixed(0);
    k.oil.textContent = m.oilRate.toFixed(1);
    k.now.textContent = `Day ${m.cycleDay.toFixed(1)}`;
    const cls = m.phase === 'INJECTION' ? 'inj' : m.phase === 'SOAK' ? 'soak' : 'prod';
    k.badge.className = `tl-badge ${cls}`;
    k.badge.textContent = m.phase === 'INJECTION' ? 'Injection' : m.phase === 'SOAK' ? 'Soak' : 'Production';
    k.title.textContent = m.phase === 'INJECTION' ? 'Steam into the sand' : m.phase === 'SOAK' ? 'Well shut in, heat spreading' : m.daysToCutoff > 0 ? 'Hot crude flowing to the pump' : 'Past the economic cut-off';
    k.detail.textContent = m.phase === 'PRODUCTION' ? `${m.oilRate.toFixed(1)} BOPD · ${m.daysToCutoff > 0 ? `${m.daysToCutoff.toFixed(0)} d to cut-off` : 're-steam now'}` : `${m.steamTons.toFixed(0)} t steam in · heated radius ${m.heatedRadius.toFixed(1)} m`;
    k.bat.textContent = `${(m.thermalBattery * 100).toFixed(0)}%`;
    const dv = derived(m);
    k.pip.textContent = dv && Number.isFinite(dv.pip) ? `${dv.pip.toFixed(1)} MPa` : '—';
  }

  hover(m) {
    const { sx, sy } = this.hoverPt, p = this.toWorld(sx, sy);
    if (p.x < WORLD.x0 || p.x > WORLD.x1 || p.y > 0.2 || p.y < -PIT_DEPTH) { this.tip(null); return; }
    const z = yToDepth(Math.min(0, p.y));
    const band = STRATA.find((s) => z >= s.top && z < s.bot) || STRATA[STRATA.length - 1];
    const T = formationT(p.x, p.y, m.sandfaceT, m.heatedRadius);
    let html = `<b>${band.name}</b> <span class="mut">· ${band.age}</span><br>${z.toFixed(0)} m below ground · ${T.toFixed(0)} °C`;
    if (band.reservoir) html += `<br><span class="mut">crude here ≈ ${Math.round(viscosityCp(T)).toLocaleString()} cP</span>`;
    if (Math.abs(p.x) < 1 && z > WELLBORE.pumpTop - 15 && z < WELLBORE.pumpBottom + 5) html = `<b>Insert rod pump</b><br>${WELLBORE.pumpTop}–${WELLBORE.pumpBottom} m · 1.25″ plunger<br><span class="mut">${m.phase === 'PRODUCTION' ? `fillage ${(m.fillage * 100).toFixed(0)}%` : 'parked'}</span>`;
    else if (Math.abs(p.x) < 1.3 && z >= WELLBORE.perfTop && z <= WELLBORE.perfBot) html = `<b>Perforations</b><br>${WELLBORE.perfTop}–${WELLBORE.perfBot} m, into the Jodhpur Sandstone<br><span class="mut">${m.phase === 'INJECTION' ? 'steam going out' : m.phase === 'SOAK' ? 'shut in' : 'hot crude coming in'}</span>`;
    this.tip(html, sx, sy);
  }

  /* ---------------------------------------------------------------- drawing */
  pattern(kind) { return (this.patterns[kind] ||= hatchPattern(this.g, kind)); }

  heatField(m) {
    const key = `${m.sandfaceT.toFixed(1)}|${m.heatedRadius.toFixed(2)}|${this.overlay}`;
    if (key === this.fieldKey) return this.field;
    const gx0 = -26, gx1 = 26, gy0 = Y_RB - 3, gy1 = Y_RT + 3, st = 0.25;
    const nx = Math.round((gx1 - gx0) / st) + 1, ny = Math.round((gy1 - gy0) / st) + 1;
    const F = new Float32Array(nx * ny);
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) F[j * nx + i] = formationT(gx0 + i * st, gy0 + j * st, m.sandfaceT, m.heatedRadius);
    // colour raster (drawn scaled with smoothing)
    const c = document.createElement('canvas'); c.width = nx; c.height = ny;
    const cg = c.getContext('2d'), img = cg.createImageData(nx, ny), d = img.data;
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const T = F[j * nx + i], k = ((ny - 1 - j) * nx + i) * 4;
      if (this.overlay === 'heat') {
        const h = clamp((T - 50) / 160, 0, 1);
        d[k] = 255 - h * 55; d[k + 1] = 190 - h * 125; d[k + 2] = 110 - h * 85; d[k + 3] = Math.pow(h, 0.8) * 190;
      } else if (this.overlay === 'visc') {
        const mob = clamp((Math.log10(10000) - Math.log10(viscosityCp(T))) / (Math.log10(10000) - Math.log10(50)), 0, 1);
        const inRes = T > 0 ? 1 : 0;
        d[k] = 80 - mob * 60; d[k + 1] = 150 - mob * 48; d[k + 2] = 200 - mob * 19; d[k + 3] = mob * 170 * inRes;
      }
    }
    cg.putImageData(img, 0, 0);
    const levels = this.overlay === 'heat' ? [60, 80, 100, 130, 160, 190] : this.overlay === 'visc' ? [3000, 1000, 300, 100] : [];
    const iso = levels.map((L) => {
      const lvl = this.overlay === 'visc' ? tempForViscosity(L) : L;
      return { L, segs: isoSegments(F, nx, ny, lvl) };
    });
    this.fieldKey = key;
    this.field = { c, gx0, gx1, gy0, gy1, st, iso };
    return this.field;
  }

  draw(k, m, st, theta) {
    const g = this.g, v = this.view, X = v.X, Y = v.Y, w = this.w, h = this.h;
    g.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
    g.clearRect(0, 0, w, h);
    // crystallisation front: sweeps from above the surface to below the basement
    const sweep = ease(smooth(0.02, 0.62, k));
    const frontY = lerp(Y(WORLD.y1) - 40, Y(WORLD.y0) + 40, sweep);
    const paperA = smooth(0.0, 0.5, k);
    g.save();
    // paper: fades in over the whole screen, fully opaque above the front
    g.globalAlpha = paperA * 0.3;
    g.fillStyle = PAPER; g.fillRect(0, 0, w, h);
    g.globalAlpha = 1;
    g.beginPath(); g.rect(0, 0, w, k >= 0.99 ? h : Math.max(0, frontY)); g.clip();
    g.globalAlpha = Math.max(paperA, 0.001) > 0 ? 1 : 0;
    g.fillStyle = PAPER; g.fillRect(0, 0, w, h);
    const vg = g.createRadialGradient(w / 2, h * 0.45, h * 0.2, w / 2, h * 0.5, h);
    vg.addColorStop(0, 'rgba(255,255,255,0.35)'); vg.addColorStop(1, 'rgba(120,95,60,0.10)');
    g.fillStyle = vg; g.fillRect(0, 0, w, h);
    this.drawGrid(g, v);
    this.drawStrata(g, v, m);
    if (m && this.overlay !== 'none') this.drawField(g, v, m);
    this.drawSurface(g, v, theta, m);
    if (m) this.drawWell(g, v, m, st);
    this.drawRuler(g, v);
    if (m && this.showLabels) this.drawCallouts(g, v, m, smooth(0.6, 0.95, k));
    if (m && this.showTracks) this.drawTracks(g, v, m, smooth(0.7, 1, k));
    if (!m && k > 0.9) {
      const off = !this.getSim().api?.online, cx = v.X(0), cy = v.Y(-PIT_DEPTH / 2);
      g.font = FONT(700, 13); g.textAlign = 'center';
      const msg = off ? 'Mantle API unavailable · live data hidden' : 'Connecting to the Mantle API…';
      const tw = g.measureText(msg).width;
      g.fillStyle = 'rgba(241,235,223,0.92)'; g.fillRect(cx - tw / 2 - 12, cy - 16, tw + 24, 28);
      g.fillStyle = INK(0.8); g.fillText(msg, cx, cy + 3);
    }
    g.restore();
    // the front itself: a thin ink-blue line with a soft glow
    if (k > 0.01 && k < 0.99 && sweep < 1) {
      const gr = g.createLinearGradient(0, frontY - 26, 0, frontY + 2);
      gr.addColorStop(0, 'rgba(21,102,181,0)'); gr.addColorStop(1, 'rgba(21,102,181,0.18)');
      g.fillStyle = gr; g.fillRect(0, frontY - 26, w, 28);
      g.fillStyle = BLUE(0.7); g.fillRect(0, frontY - 0.75, w, 1.5);
    }
  }

  drawGrid(g, v) {
    const { X, Y, ppm } = v;
    const minor = ppm >= 9 ? 1 : 5, x0 = Math.floor((v.cx - this.w / 2 / ppm) / minor) * minor, x1 = v.cx + this.w / 2 / ppm;
    const y0 = Math.floor((v.cy - this.h / 2 / ppm) / minor) * minor, y1 = v.cy + this.h / 2 / ppm;
    g.lineWidth = 1;
    for (let x = x0; x <= x1; x += minor) { const major = Math.abs(x % 5) < 1e-6; g.strokeStyle = major ? 'rgba(120,95,60,0.12)' : 'rgba(120,95,60,0.055)'; g.beginPath(); g.moveTo(Math.round(X(x)) + 0.5, 0); g.lineTo(Math.round(X(x)) + 0.5, this.h); g.stroke(); }
    for (let y = y0; y <= y1; y += minor) { const major = Math.abs(y % 5) < 1e-6; g.strokeStyle = major ? 'rgba(120,95,60,0.12)' : 'rgba(120,95,60,0.055)'; g.beginPath(); g.moveTo(0, Math.round(Y(y)) + 0.5); g.lineTo(this.w, Math.round(Y(y)) + 0.5); g.stroke(); }
  }

  drawStrata(g, v, m) {
    const { X, Y, ppm } = v;
    const xa = X(WORLD.x0), xb = X(WORLD.x1);
    for (const s of STRATA) {
      const ya = Y(depthToY(s.top)), yb = Y(depthToY(s.bot));
      g.globalAlpha = s.reservoir ? 0.5 : 0.3;
      g.fillStyle = s.color; g.fillRect(xa, ya, xb - xa, yb - ya);
      g.globalAlpha = s.reservoir ? 0.55 : 0.4;
      const p = this.pattern(s.hatch);
      p.setTransform(new DOMMatrix().translateSelf(X(0), Y(0)));
      g.fillStyle = p; g.fillRect(xa, ya, xb - xa, yb - ya);
      g.globalAlpha = 1;
      g.strokeStyle = INK(0.55); g.lineWidth = 1;
      g.beginPath(); g.moveTo(xa, Math.round(ya) + 0.5); g.lineTo(xb, Math.round(ya) + 0.5); g.stroke();
      // formation label, left
      if (yb - ya > 22) {
        g.font = FONT(700, 11); g.fillStyle = INK(0.85); g.textAlign = 'left';
        const lx = xa + 12, ly = ya + Math.min(18, (yb - ya) / 2 + 4);
        g.fillStyle = 'rgba(241,235,223,0.78)';
        const tw = Math.max(g.measureText(s.name).width, 90);
        g.fillRect(lx - 4, ly - 12, tw + 8, (yb - ya) > 36 ? 30 : 17);
        g.fillStyle = INK(0.88); g.fillText(s.name, lx, ly);
        if (yb - ya > 36) { g.font = FONT(500, 10); g.fillStyle = INK(0.55); g.fillText(`${s.age} · ${s.top}–${s.bot} m`, lx, ly + 13); }
      }
    }
    // block outline
    g.strokeStyle = INK(0.9); g.lineWidth = 1.6;
    g.strokeRect(xa, Y(0), xb - xa, Y(-PIT_DEPTH) - Y(0));
    // scale breaks on the block edges where the depth scale changes
    for (let i = 1; i < KNOTS.length - 1; i++) {
      const yy = Y(KNOTS[i][1]);
      for (const x of [xa, xb]) {
        g.fillStyle = PAPER; g.fillRect(x - 5, yy - 4, 10, 8);
        g.strokeStyle = INK(0.8); g.lineWidth = 1.2;
        g.beginPath(); g.moveTo(x - 7, yy - 3); g.lineTo(x - 2, yy - 5); g.lineTo(x + 2, yy + 5); g.lineTo(x + 7, yy + 3); g.stroke();
      }
    }
    void ppm; void m;
  }

  drawField(g, v, m) {
    const f = this.heatField(m), { X, Y } = v;
    g.save();
    g.beginPath(); g.rect(X(WORLD.x0), Y(0), X(WORLD.x1) - X(WORLD.x0), Y(-PIT_DEPTH) - Y(0)); g.clip();
    g.imageSmoothingEnabled = true;
    g.drawImage(f.c, X(f.gx0), Y(f.gy1), X(f.gx1) - X(f.gx0), Y(f.gy0) - Y(f.gy1));
    const col = this.overlay === 'heat' ? HEAT : BLUE;
    const gxX = (i) => X(f.gx0 + i * f.st), gyY = (j) => Y(f.gy0 + j * f.st);
    g.lineWidth = 1;
    f.iso.forEach(({ L, segs }, n) => {
      g.strokeStyle = col(0.35 + 0.1 * n);
      g.beginPath();
      for (const [a, b] of segs) { g.moveTo(gxX(a[0]), gyY(a[1])); g.lineTo(gxX(b[0]), gyY(b[1])); }
      g.stroke();
      // label on the left flank (the callouts own the right), stepping down per level
      const ly = (Y_RT + Y_RB) / 2 + 1.6 - n * 0.75;
      let best = null;
      for (const [a, b] of segs) {
        const ay = f.gy0 + a[1] * f.st, by = f.gy0 + b[1] * f.st;
        if ((ay - ly) * (by - ly) > 0) continue;
        const t = (ly - ay) / (by - ay || 1e-9), wx = f.gx0 + (a[0] + (b[0] - a[0]) * t) * f.st;
        if (wx < -0.8 && (!best || wx < best)) best = wx;
      }
      if (best != null) {
        const txt = this.overlay === 'heat' ? `${L}°` : `${L >= 1000 ? L / 1000 + 'k' : L} cP`;
        g.font = FONT(700, 9.5); const tw = g.measureText(txt).width;
        g.fillStyle = 'rgba(241,235,223,0.88)'; g.fillRect(X(best) - tw / 2 - 3, Y(ly) - 6, tw + 6, 12);
        g.fillStyle = col(0.95); g.textAlign = 'center'; g.fillText(txt, X(best), Y(ly) + 3.5);
      }
    });
    // heated-radius dimension
    const ym = Y_RB + 0.9, rh = m.heatedRadius;
    g.strokeStyle = HEAT(0.9); g.fillStyle = HEAT(0.9); g.lineWidth = 1.2;
    g.beginPath(); g.moveTo(X(-1.4), Y(ym)); g.lineTo(X(-rh), Y(ym)); g.stroke();
    for (const [x, dir] of [[-1.4, -1], [-rh, 1]]) { g.beginPath(); g.moveTo(X(x), Y(ym)); g.lineTo(X(x) + dir * 7, Y(ym) - 3.5); g.lineTo(X(x) + dir * 7, Y(ym) + 3.5); g.closePath(); g.fill(); }
    g.beginPath(); g.moveTo(X(-rh), Y(ym) - 8); g.lineTo(X(-rh), Y(ym) + 8); g.stroke();
    g.font = FONT(700, 10.5); g.textAlign = 'center';
    const lbl = `heated radius ${rh.toFixed(1)} m`, tw = g.measureText(lbl).width;
    const lx = X(-(1.4 + rh) / 2);
    g.fillStyle = 'rgba(241,235,223,0.9)'; g.fillRect(lx - tw / 2 - 4, Y(ym) - 17, tw + 8, 13);
    g.fillStyle = HEAT(1); g.fillText(lbl, lx, Y(ym) - 7);
    g.restore();
  }

  drawSurface(g, v, theta, m) {
    const { X, Y, ppm } = v;
    const lw = Math.max(1, ppm / 16);
    // ground line with the earth symbol
    g.strokeStyle = INK(0.95); g.lineWidth = 2;
    g.beginPath(); g.moveTo(X(WORLD.x0), Y(0)); g.lineTo(X(WORLD.x1), Y(0)); g.stroke();
    g.strokeStyle = INK(0.35); g.lineWidth = 1;
    for (let x = WORLD.x0 + 0.5; x < WORLD.x1; x += 1.2) { g.beginPath(); g.moveTo(X(x), Y(0)); g.lineTo(X(x - 0.5), Y(-0.5)); g.stroke(); }

    const P = unitPose(theta), S = UNIT.saddle, K = UNIT.crank;
    const fillW = 'rgba(255,250,240,0.95)';
    const poly = (pts, fill = fillW, stroke = INK(0.9), width = lw) => { g.beginPath(); pts.forEach(([x, y], i) => (i ? g.lineTo(X(x), Y(y)) : g.moveTo(X(x), Y(y)))); g.closePath(); if (fill) { g.fillStyle = fill; g.fill(); } g.strokeStyle = stroke; g.lineWidth = width; g.stroke(); };
    const line = (a, b, width = lw, col = INK(0.9)) => { g.beginPath(); g.moveTo(X(a[0]), Y(a[1])); g.lineTo(X(b[0]), Y(b[1])); g.strokeStyle = col; g.lineWidth = width; g.stroke(); };
    const circ = (x, y, r, fill = fillW, width = lw) => { g.beginPath(); g.arc(X(x), Y(y), r * ppm, 0, Math.PI * 2); if (fill) { g.fillStyle = fill; g.fill(); } g.strokeStyle = INK(0.9); g.lineWidth = width; g.stroke(); };
    // foundation + skid
    poly([[1.25, 0], [11.85, 0], [11.85, 0.36], [1.25, 0.36]], 'rgba(200,192,178,0.6)');
    const sk = UNIT.skid;
    poly([[sk.x0, sk.y0], [sk.x1, sk.y0], [sk.x1, sk.y1], [sk.x0, sk.y1]]);
    // samson post (front and rear legs)
    const topY = S.y - 0.28;
    line([3.55, sk.y1], [5.0, topY], lw * 1.6); line([7.55, sk.y1], [5.45, topY], lw * 1.6);
    line([4.1, 2.5], [6.8, 2.5]); line([4.55, 4.0], [6.25, 4.0]);
    line([4.1, 2.5], [6.25, 4.0], lw * 0.6); line([6.8, 2.5], [4.55, 4.0], lw * 0.6);
    // gearbox + motor + belt
    const gb = UNIT.gearbox, mo = UNIT.motor;
    poly([[gb.x0, gb.y0], [gb.x1, gb.y0], [gb.x1, gb.y1 - 0.4], [gb.x1 - 0.3, gb.y1], [gb.x0 + 0.3, gb.y1], [gb.x0, gb.y1 - 0.4]]);
    circ(mo.x, mo.y, mo.r);
    line([mo.x, mo.y + mo.r], [K.x + 0.2, K.y - 0.9], lw * 0.7, INK(0.5)); line([mo.x, mo.y - mo.r], [K.x + 0.2, K.y - 1.5], lw * 0.7, INK(0.5));
    // crank + counterweight (opposite the wrist pin)
    const ca = theta, cx = K.x, cy = K.y;
    const tail = [cx - Math.cos(ca) * 1.35, cy - Math.sin(ca) * 1.35];
    const nrm = [-Math.sin(ca), Math.cos(ca)];
    poly([[tail[0] + nrm[0] * 0.55, tail[1] + nrm[1] * 0.55], [tail[0] - nrm[0] * 0.55, tail[1] - nrm[1] * 0.55], [tail[0] - Math.cos(ca) * 0.5 - nrm[0] * 0.5, tail[1] - Math.sin(ca) * 0.5 - nrm[1] * 0.5], [tail[0] - Math.cos(ca) * 0.5 + nrm[0] * 0.5, tail[1] - Math.sin(ca) * 0.5 + nrm[1] * 0.5]], 'rgba(60,54,46,0.85)');
    line([P.crankPin.x, P.crankPin.y], tail, lw * 2.2);
    circ(cx, cy, 0.14, INK(0.9));
    circ(P.crankPin.x, P.crankPin.y, 0.08, fillW);
    // pitman
    line([P.crankPin.x, P.crankPin.y], [P.equalizer.x, P.equalizer.y], lw * 1.3);
    // walking beam
    const u = [Math.cos(P.beam), Math.sin(P.beam)], nb = [-u[1], u[0]], bh = 0.22;
    const b0 = UNIT.beamLen[0], b1 = UNIT.beamLen[1];
    const at = (t, o) => [S.x + u[0] * t + nb[0] * o, S.y + u[1] * t + nb[1] * o];
    poly([at(b0, bh), at(b1, bh), at(b1, -bh), at(b0, -bh)], 'rgba(233,190,70,0.55)');
    circ(P.equalizer.x, P.equalizer.y, 0.1, fillW);
    circ(S.x, S.y, 0.13, fillW);
    // horsehead: arc face of radius A about the saddle, spanning ±span
    const A = UNIT.A, span = UNIT.horseheadSpan, dep = UNIT.horseheadDepth;
    const hh = [];
    const base = Math.atan2(-u[1], -u[0]);
    for (let i = 0; i <= 16; i++) { const a = base - span + (2 * span * i) / 16; hh.push([S.x + Math.cos(a) * A, S.y + Math.sin(a) * A]); }
    for (let i = 16; i >= 0; i--) { const a = base - span * 0.55 + (1.1 * span * i) / 16; hh.push([S.x + Math.cos(a) * (A - dep), S.y + Math.sin(a) * (A - dep)]); }
    poly(hh, 'rgba(233,190,70,0.55)');
    // bridle, carrier bar, polished rod, wellhead
    const rx = P.ropeX;
    line([rx, S.y], [rx, P.carrierY], Math.max(0.8, lw * 0.6));
    poly([[rx - 0.32, P.carrierY - 0.05], [rx + 0.32, P.carrierY - 0.05], [rx + 0.32, P.carrierY + 0.05], [rx - 0.32, P.carrierY + 0.05]], INK(0.9));
    line([rx, P.carrierY + 0.5], [rx, UNIT.stuffingBoxY - 0.35], lw * 0.9, 'rgba(90,90,96,1)');
    const wh = (y0, y1, hw) => poly([[-hw, y0], [hw, y0], [hw, y1], [-hw, y1]]);
    wh(0, 0.5, 0.42); wh(0.5, 0.95, 0.26); wh(0.95, 1.35, 0.3); wh(1.35, 1.75, 0.22); wh(1.75, 2.05, 0.14);
    line([0.3, 1.15], [1.3, 1.15], lw * 1.2); line([-0.3, 0.72], [-3.2, 0.72], lw * 1.2);
    circ(1.0, 1.15, 0.12); circ(-1.2, 0.72, 0.12, m?.phase === 'INJECTION' ? HEAT(0.8) : fillW);
    // steam / flow arrows at the wellhead
    const flowArrow = (x0, x1, y, col) => { line([x0, y], [x1, y], lw, col); const d = Math.sign(x1 - x0); g.beginPath(); g.moveTo(X(x1), Y(y)); g.lineTo(X(x1) - d * 7, Y(y) - 3.5); g.lineTo(X(x1) - d * 7, Y(y) + 3.5); g.closePath(); g.fillStyle = col; g.fill(); };
    if (m?.phase === 'INJECTION') flowArrow(-3.2, -0.6, 0.72, HEAT(0.9)); else if (m?.phase === 'PRODUCTION') flowArrow(1.4, 3.4, 1.15, INK(0.8));
    // equipment silhouettes along the ground (steam generator, tanks) as light ghost outlines
    g.setLineDash([4, 3]);
    poly([[-27.5, 0], [-6.5, 0], [-6.5, 3.2], [-27.5, 3.2]], 'rgba(255,250,240,0.35)', INK(0.35), 1);
    poly([[-25.4, 3.2], [-23.6, 3.2], [-23.6, 22], [-25.4, 22]].map(([x, y]) => [x, Math.min(y, WORLD.y1 - 0.2)]), 'rgba(255,250,240,0.35)', INK(0.35), 1);
    for (const tx of [14, 23.5]) poly([[tx - 3.6, 0], [tx + 3.6, 0], [tx + 3.6, 7.3], [tx, 8], [tx - 3.6, 7.3]], 'rgba(255,250,240,0.35)', INK(0.35), 1);
    g.setLineDash([]);
    g.font = FONT(600, 10); g.fillStyle = INK(0.45); g.textAlign = 'center';
    g.fillText('STEAM GENERATOR (behind)', X(-17), Y(1.5));
    g.fillText('TANK BATTERY (behind)', X(18.75), Y(3.6));
  }

  drawWell(g, v, m, st) {
    const { X, Y, ppm } = v;
    const yTop = 0, yShoe = depthToY(WELLBORE.casingShoe), yTD = -PIT_DEPTH;
    const yTub = depthToY(WELLBORE.tubingBottom), yPT = depthToY(WELLBORE.pumpTop), yPB = depthToY(WELLBORE.pumpBottom);
    const yLev = depthToY(m.fluidLevel), yPfT = depthToY(WELLBORE.perfTop), yPfB = depthToY(WELLBORE.perfBot);
    const rect = (x0, x1, y0, y1, fill, stroke, lw = 1) => { g.beginPath(); g.rect(X(x0), Y(y1), X(x1) - X(x0), Y(y0) - Y(y1)); if (fill) { g.fillStyle = fill; g.fill(); } if (stroke) { g.strokeStyle = stroke; g.lineWidth = lw; g.stroke(); } };
    // open hole (paper cut through the rock)
    rect(-R.hole, R.hole, yTD, yTop, 'rgba(241,235,223,1)');
    // cement sheath
    const cem = this.pattern('dots');
    rect(-R.hole, -R.casing, yShoe, yTop, 'rgba(170,164,150,0.9)'); rect(R.casing, R.hole, yShoe, yTop, 'rgba(170,164,150,0.9)');
    g.globalAlpha = 0.5; rect(-R.hole, -R.casing, yShoe, yTop, cem); rect(R.casing, R.hole, yShoe, yTop, cem); g.globalAlpha = 1;
    // annulus fluid below the level: crude
    const crude = m.phase === 'INJECTION' ? 'rgba(255,255,255,0.9)' : 'rgba(58,38,20,0.85)';
    rect(-R.casingIn, -R.tubing, Math.max(yShoe, yPB), yLev, crude); rect(R.tubing, R.casingIn, Math.max(yShoe, yPB), yLev, crude);
    rect(-R.casingIn, R.casingIn, yShoe, yPB, crude);
    // casing walls (steel = solid ink in section)
    rect(-R.casing, -R.casingIn, yShoe, yTop, INK(0.85)); rect(R.casingIn, R.casing, yShoe, yTop, INK(0.85));
    // casing shoe
    g.fillStyle = INK(0.9);
    for (const s of [-1, 1]) { g.beginPath(); g.moveTo(X(s * R.casing), Y(yShoe)); g.lineTo(X(s * (R.casing + 0.35)), Y(yShoe)); g.lineTo(X(s * R.casing), Y(yShoe + 0.5)); g.closePath(); g.fill(); }
    // perforations: tunnels through casing + cement into the sand
    const perfIn = m.phase === 'PRODUCTION', perfOut = m.phase === 'INJECTION';
    for (let y = yPfB + 0.2; y <= yPfT - 0.1; y += 0.42) {
      for (const s of [-1, 1]) {
        g.strokeStyle = INK(0.9); g.lineWidth = Math.max(1, ppm * 0.06);
        g.beginPath(); g.moveTo(X(s * R.casingIn), Y(y)); g.lineTo(X(s * (R.hole + 0.9)), Y(y)); g.stroke();
      }
    }
    // tubing (VIT) and its contents
    const tubFill = m.phase === 'INJECTION' ? 'rgba(255,245,235,1)' : 'rgba(58,38,20,0.9)';
    rect(-R.tubingIn, R.tubingIn, yPT, yTop, tubFill);
    rect(-R.tubing, -R.tubingIn, yTub, yTop, 'rgba(90,92,98,0.95)'); rect(R.tubingIn, R.tubing, yTub, yTop, 'rgba(90,92,98,0.95)');
    // rod string (moves with the polished rod, scaled into the drawing)
    const rodOff = ((st.rodPos ?? 0) / STROKE.length) * 0.9;
    g.strokeStyle = 'rgba(140,140,146,1)'; g.lineWidth = Math.max(1.2, R.rod * 2 * ppm);
    g.beginPath(); g.moveTo(X(0), Y(UNIT.stuffingBoxY - 0.35)); g.lineTo(X(0), Y(yPT - 0.6 + rodOff)); g.stroke();
    for (let y = -1 + (rodOff % 1.3); y > yPT; y -= 1.3) rect(-R.coupling, R.coupling, y - 0.08 + rodOff * 0, y + 0.08, 'rgba(110,110,116,1)');
    // pump: barrel, plunger, travelling + standing valves
    rect(-R.barrel, R.barrel, yPB, yPT, 'rgba(255,250,240,0.95)', INK(0.9), 1.2);
    const pl0 = yPT - 1.6 + rodOff, pl1 = pl0 - 1.1;
    rect(-R.barrel + 0.04, R.barrel - 0.04, pl1, pl0, 'rgba(160,160,168,1)', INK(0.8));
    const up = (st.rodVel ?? 0) > 0;
    const valve = (y, open) => { g.beginPath(); g.arc(X(0), Y(y + (open ? 0.18 : 0)), Math.max(2, 0.09 * ppm), 0, Math.PI * 2); g.fillStyle = INK(0.9); g.fill(); g.strokeStyle = INK(0.9); g.lineWidth = 1; g.beginPath(); g.moveTo(X(-0.14), Y(y - 0.06)); g.lineTo(X(0.14), Y(y - 0.06)); g.stroke(); };
    valve(pl1 + 0.08, m.phase === 'PRODUCTION' && !up);
    valve(yPB + 0.15, m.phase === 'PRODUCTION' && up);
    // fluid level symbol
    g.strokeStyle = BLUE(0.9); g.lineWidth = 1.2;
    g.beginPath(); g.moveTo(X(-R.casingIn - 1.2), Y(yLev)); g.lineTo(X(R.casingIn + 1.2), Y(yLev)); g.stroke();
    g.fillStyle = BLUE(0.9); g.beginPath(); g.moveTo(X(-R.casingIn - 0.9), Y(yLev) - 1); g.lineTo(X(-R.casingIn - 0.9) - 5, Y(yLev) - 9); g.lineTo(X(-R.casingIn - 0.9) + 5, Y(yLev) - 9); g.closePath(); g.fill();
    // flow arrows: steam out, or crude in and up
    const t = performance.now() / 1000;
    if (perfOut || perfIn) {
      const col = perfOut ? HEAT(0.85) : INK(0.75);
      for (let i = 0; i < 4; i++) {
        const y = lerp(yPfB + 0.5, yPfT - 0.4, (i + 0.5) / 4);
        const ph = (t * 0.6 + i * 0.27) % 1;
        for (const s of [-1, 1]) {
          const r0 = perfOut ? 1.2 + ph * 2.4 : 3.6 - ph * 2.4, dir = perfOut ? s : -s;
          const x = s * r0;
          g.globalAlpha = Math.sin(ph * Math.PI);
          g.fillStyle = col; g.beginPath(); g.moveTo(X(x) + dir * 6, Y(y)); g.lineTo(X(x) - dir * 3, Y(y) - 4); g.lineTo(X(x) - dir * 3, Y(y) + 4); g.closePath(); g.fill();
        }
      }
      g.globalAlpha = 1;
    }
  }

  drawRuler(g, v) {
    const { X, Y } = v;
    const x = X(WORLD.x0) - 14;
    g.strokeStyle = INK(0.7); g.lineWidth = 1;
    g.beginPath(); g.moveTo(x, Y(0)); g.lineTo(x, Y(-PIT_DEPTH)); g.stroke();
    g.font = FONT(600, 9.5); g.textAlign = 'right'; g.fillStyle = INK(0.7);
    const ticks = [0, 30, 250, 500, 750, 1000, 1080, 1100, 1120, 1140, 1160, 1250];
    let lastY = -99;
    for (const d of ticks) {
      const y = Y(depthToY(d));
      g.beginPath(); g.moveTo(x - 5, y); g.lineTo(x, y); g.stroke();
      if (y - lastY > 11) { g.fillText(`${d}`, x - 7, y + 3); lastY = y; }
    }
    g.save(); g.translate(x - 38, (Y(0) + Y(-PIT_DEPTH)) / 2); g.rotate(-Math.PI / 2); g.textAlign = 'center'; g.font = FONT(700, 9); g.fillStyle = INK(0.5);
    g.fillText('TRUE DEPTH (m) · OVERBURDEN COMPRESSED', 0, 0); g.restore();
  }

  drawCallouts(g, v, m, a) {
    if (a <= 0) return;
    const { X, Y } = v;
    g.globalAlpha = a;
    const items = [
      [depthToY(40), 'Thermal wellhead', 'steam in / crude out'],
      [depthToY(m.fluidLevel), `Fluid level ${m.fluidLevel.toFixed(0)} m`, 'dynamic, in the annulus'],
      [depthToY(700), 'Vacuum-insulated tubing', 'keeps the crude hot on the way up'],
      [depthToY(WELLBORE.pumpTop + 8), 'Insert rod pump', `${WELLBORE.pumpTop} m · 1.25″ plunger`],
      [depthToY(1120), 'Perforations', `${WELLBORE.perfTop}–${WELLBORE.perfBot} m`],
      [depthToY(WELLBORE.casingShoe), 'Casing shoe', `${WELLBORE.casingShoe} m`],
    ];
    const lx = X(4.5);
    let lastY = -1e9;
    g.textAlign = 'left';
    for (const [wy, title, sub] of items) {
      let y = Math.max(Y(wy), lastY + 30);
      lastY = y;
      g.strokeStyle = INK(0.55); g.lineWidth = 0.9;
      g.beginPath(); g.moveTo(X(0.75), Y(wy)); g.lineTo(lx - 20, y); g.lineTo(lx - 4, y); g.stroke();
      g.fillStyle = INK(0.8); g.beginPath(); g.arc(X(0.75), Y(wy), 2, 0, 7); g.fill();
      g.font = FONT(700, 10.5); const tw = Math.max(g.measureText(title).width, (g.font = FONT(500, 9.5), g.measureText(sub).width));
      g.fillStyle = 'rgba(241,235,223,0.86)'; g.fillRect(lx - 3, y - 11, tw + 8, 25);
      g.font = FONT(700, 10.5); g.fillStyle = INK(0.9); g.fillText(title, lx, y);
      g.font = FONT(500, 9.5); g.fillStyle = INK(0.55); g.fillText(sub, lx, y + 11);
    }
    g.globalAlpha = 1;
  }

  drawTracks(g, v, m, a) {
    if (a <= 0) return;
    const prof = this.getSim().profile();
    if (!prof) return;
    const fl = fluid(this.getSim());
    const { X, Y } = v;
    const tx0 = X(WORLD.x1) + 34, tw = 98, gap = 10;
    const yTop = Y(0), yBot = Y(-PIT_DEPTH);
    g.globalAlpha = a;
    const track = (x0, title, unit, draw) => {
      g.fillStyle = 'rgba(255,252,244,0.75)'; g.fillRect(x0, yTop, tw, yBot - yTop);
      g.strokeStyle = INK(0.35); g.lineWidth = 1; g.strokeRect(x0 + 0.5, yTop + 0.5, tw, yBot - yTop);
      g.font = FONT(700, 9.5); g.fillStyle = INK(0.75); g.textAlign = 'left'; g.fillText(title.toUpperCase(), x0, yTop - 16);
      g.font = FONT(500, 9); g.fillStyle = INK(0.5); g.fillText(unit, x0, yTop - 5);
      g.save(); g.beginPath(); g.rect(x0, yTop, tw, yBot - yTop); g.clip(); draw(x0); g.restore();
    };
    const rowY = (i) => Y(depthToY(prof.depth[i]));
    const plot = (arr, fx, col, lw, dash) => { g.beginPath(); arr.forEach((val, i) => (i ? g.lineTo(fx(val), rowY(i)) : g.moveTo(fx(val), rowY(i)))); g.setLineDash(dash || []); g.strokeStyle = col; g.lineWidth = lw; g.stroke(); g.setLineDash([]); };
    const bands = (x0) => {
      g.fillStyle = 'rgba(240,160,75,0.12)'; g.fillRect(x0, Y(Y_RT), tw, Y(Y_RB) - Y(Y_RT));
      if (prof.depositionTop != null) { g.fillStyle = 'rgba(214,160,20,0.16)'; g.fillRect(x0, Y(depthToY(prof.depositionTop)), tw, Y(depthToY(prof.depositionBot)) - Y(depthToY(prof.depositionTop))); }
      g.strokeStyle = 'rgba(120,95,60,0.1)';
      for (const s of STRATA) { const y = Y(depthToY(s.top)); g.beginPath(); g.moveTo(x0, y); g.lineTo(x0 + tw, y); g.stroke(); }
    };
    track(tx0, 'Temperature', '20 — 240 °C', (x0) => {
      bands(x0);
      const fx = (t) => x0 + ((t - 20) / 220) * tw;
      plot(prof.Tformation, fx, INK(0.45), 1.1, [3, 3]);
      plot(prof.Tfluid, fx, HEAT(0.95), 1.8);
      if (prof.depositionTop != null) { g.font = FONT(600, 8.5); g.fillStyle = 'rgba(138,101,8,0.9)'; g.fillText('wax / asphaltene', x0 + 4, Y(depthToY(prof.depositionTop)) + 10); }
    });
    track(tx0 + tw + gap, 'Viscosity', '10 — 100k cP · log', (x0) => {
      bands(x0);
      const fx = (mu) => x0 + clamp((Math.log10(mu) - 1) / 4, 0, 1) * tw;
      plot(prof.mu, fx, 'rgba(120,70,30,0.9)', 1.8);
    });
    track(tx0 + 2 * (tw + gap), 'Pressure', '0 — 6 MPa', (x0) => {
      bands(x0);
      const fx = (mpa) => x0 + clamp(mpa / 6, 0, 1) * tw;
      // annulus pressure: gas cap above the fluid level, a liquid gradient below it
      plot(prof.pressure.map((b) => b / 10), fx, BLUE(0.9), 1.8);
      const yr = Y(depthToY(1120));
      if (fl) {
        g.fillStyle = BLUE(1); g.beginPath(); g.arc(fx(fl.pRes), yr, 3.5, 0, 7); g.fill();
        g.font = FONT(700, 9); g.textAlign = 'right'; g.fillText(`Pr ${fl.pRes}`, fx(fl.pRes) - 6, yr + 3);
      }
    });
    g.globalAlpha = 1;
  }

  /* ---------------------------------------------------------------- dock */
  drawTimeline(m, sim) {
    const c = this.track, dpr = this.dpr, w = c.clientWidth, h = c.clientHeight;
    if (!w) return;
    if (c.width !== w * dpr) { c.width = w * dpr; c.height = h * dpr; }
    const g = c.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, w, h);
    const x0 = 8, x1 = w - 8, X = (d) => x0 + (d / CYCLE.days) * (x1 - x0);
    const s = (this.series = sim.series());
    const yb = h - 34, yt = 6, oMax = s ? Math.max(...s.oilP10) * 1.05 : 1;
    g.fillStyle = 'rgba(226,96,32,0.14)'; g.fillRect(X(0), yt, X(CYCLE.injEnd) - X(0), yb - yt);
    g.fillStyle = 'rgba(214,160,20,0.16)'; g.fillRect(X(CYCLE.injEnd), yt, X(CYCLE.soakEnd) - X(CYCLE.injEnd), yb - yt);
    g.fillStyle = 'rgba(29,127,224,0.06)'; g.fillRect(X(CYCLE.soakEnd), yt, X(CYCLE.days) - X(CYCLE.soakEnd), yb - yt);
    if (s) {
      g.beginPath(); s.day.forEach((d, i) => (i ? g.lineTo(X(d), yb - (s.oil[i] / oMax) * (yb - yt)) : g.moveTo(X(d), yb)));
      g.lineTo(X(CYCLE.days), yb); g.closePath(); g.fillStyle = 'rgba(42,36,27,0.08)'; g.fill();
      g.beginPath(); s.day.forEach((d, i) => (i ? g.lineTo(X(d), yb - (s.oil[i] / oMax) * (yb - yt)) : g.moveTo(X(d), yb - (s.oil[i] / oMax) * (yb - yt))));
      g.strokeStyle = INK(0.55); g.lineWidth = 1.3; g.stroke();
    }
    g.font = FONT(600, 9.5); g.fillStyle = INK(0.55); g.textAlign = 'center';
    for (let d = 0; d <= CYCLE.days; d += 10) { g.fillRect(X(d) - 0.5, yb, 1, 4); if (d % 20 === 0) g.fillText(d, X(d), yb + 13); }
    // next cycle, as Mantle would run it: more steam (longer injection), longer soak, earlier cut-off
    const PL = plan(sim), py = h - 12, ph = 8;
    if (PL && Number.isFinite(PL.mantle.injDays)) {
      const P = PL.mantle, inj = P.injDays, soak = P.soak, cut = P.cutoff;
      const seg = (d0, d1, col) => { g.fillStyle = col; g.fillRect(X(d0), py - ph / 2, Math.max(1, X(d1) - X(d0) - 1), ph); };
      seg(0, inj, 'rgba(226,96,32,0.55)'); seg(inj, inj + soak, 'rgba(214,160,20,0.6)'); seg(inj + soak, cut, 'rgba(40,150,90,0.45)');
      g.fillStyle = 'rgba(60,46,25,0.06)'; g.fillRect(X(cut), py - ph / 2, X(CYCLE.days) - X(cut), ph);
      g.textAlign = 'left'; g.font = FONT(700, 8.5); g.fillStyle = 'rgba(20,110,60,0.95)';
      g.fillText(`NEXT CYCLE · MANTLE PLAN · ${Math.round(P.steam)} t · soak ${P.soak} d · cut-off d${cut}`, X(inj + soak) + 6, py + 3);
    } else {
      g.textAlign = 'left'; g.font = FONT(600, 8.5); g.fillStyle = INK(0.4);
      g.fillText('NEXT CYCLE · waiting for the planner…', X(0) + 4, py + 3);
    }
    g.textAlign = 'left'; g.font = FONT(700, 9); g.fillStyle = '#b3470f'; g.fillText('STEAM', X(0) + 4, yt + 11);
    g.fillStyle = '#1566b5'; g.fillText('PRODUCTION', X(CYCLE.soakEnd) + 4, yt + 11);
    if (m.phase === 'PRODUCTION') { const cd = Math.min(CYCLE.days, m.cycleDay + m.daysToCutoff); g.fillStyle = 'rgba(40,150,90,0.9)'; g.fillRect(X(cd) - 0.75, yt, 1.5, yb - yt); g.font = FONT(700, 8.5); g.textAlign = cd > 100 ? 'right' : 'left'; g.fillText('cut-off', X(cd) + (cd > 100 ? -4 : 4), yb - 4); }
    const px = X(m.cycleDay);
    g.fillStyle = INK(0.95); g.fillRect(px - 1, yt - 2, 2, yb - yt + 4);
    g.beginPath(); g.arc(px, yt - 2, 4.5, 0, 7); g.fill();
  }

  drawCard(m, sim) {
    const c = this.cardCanvas, dpr = this.dpr, w = c.clientWidth, h = c.clientHeight;
    if (!w || !h) return;
    if (c.width !== w * dpr) { c.width = w * dpr; c.height = h * dpr; }
    const g = c.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, w, h);
    const s = this.series || sim.series();
    if (!s) return;
    const X = (d) => 4 + (d / CYCLE.days) * (w - 8), Y = (t) => h - 12 - ((t - 40) / 200) * (h - 18);
    g.beginPath(); s.day.forEach((d, i) => (i ? g.lineTo(X(d), Y(s.T[i])) : g.moveTo(X(d), Y(s.T[i])))); g.lineTo(X(CYCLE.days), h - 12); g.lineTo(X(0), h - 12); g.closePath();
    const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, 'rgba(226,96,32,0.35)'); gr.addColorStop(1, 'rgba(226,96,32,0.02)'); g.fillStyle = gr; g.fill();
    g.beginPath(); s.day.forEach((d, i) => (i ? g.lineTo(X(d), Y(s.T[i])) : g.moveTo(X(d), Y(s.T[i])))); g.strokeStyle = '#b3470f'; g.lineWidth = 1.5; g.stroke();
    g.beginPath(); g.arc(X(m.cycleDay), Y(m.sandfaceT), 3.5, 0, 7); g.fillStyle = INK(0.95); g.fill();
    g.font = FONT(600, 9); g.fillStyle = INK(0.5); g.textAlign = 'left'; g.fillText(`sandface ${m.sandfaceT.toFixed(0)} °C`, 4, h - 1);
  }
}

// invert the viscosity law (monotone decreasing in T) by bisection
function tempForViscosity(mu) {
  let lo = 20, hi = 320;
  for (let i = 0; i < 40; i++) { const mid = (lo + hi) / 2; if (viscosityCp(mid) > mu) lo = mid; else hi = mid; }
  return (lo + hi) / 2;
}
