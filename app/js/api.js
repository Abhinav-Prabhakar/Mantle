// Backend client + RemoteTwin.
//
// Every number the UI displays comes from the Mantle API: physics, the database and the ML/optimiser layer
// (forecast bands, dyno classification, failure risk, the pump recommendation, the next-cycle plan).
// The browser keeps a local WellSim for one job only: driving the 60 fps animation (crank angle, rod
// position, how fast the oil particles move). Its numbers are never shown.
// There is no fallback data: until the API answers, getters return null and the views show an explicit
// "unavailable" state. The twin keeps probing and reconnects on its own.

const TIMEOUT_MS = 2500;

async function fetchJson(url, opts = {}, timeout = TIMEOUT_MS) {
  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), timeout);
  try {
    const r = await fetch(url, { ...opts, signal: ctl.signal, headers: { 'Content-Type': 'application/json', ...(opts.headers || {}) } });
    if (!r.ok) throw new Error(`${r.status} ${r.statusText} for ${url}`);
    return await r.json();
  } finally { clearTimeout(t); }
}

// Find the API: ?api=<base> wins; then same-origin /api (nginx / Docker); then the dev server on :8000.
export async function connectApi() {
  const params = new URLSearchParams(location.search);
  const candidates = [];
  if (params.get('api')) candidates.push(params.get('api').replace(/\/$/, ''));
  candidates.push(`${location.origin}/api`, `${location.protocol}//${location.hostname}:8000/api`);
  for (const base of [...new Set(candidates)]) {
    try {
      const h = await fetchJson(`${base}/health`, {}, 1500);
      if (h && h.status === 'ok') {
        const api = new Api(base);
        api.health = h;
        try { api.meta = await fetchJson(`${base}/meta`); } catch { api.meta = null; }
        return api;
      }
    } catch { /* try the next one */ }
  }
  return new Api(null);
}

export class Api {
  constructor(base) { this.base = base; this.online = !!base; this.health = null; this.meta = null; this.errors = 0; }
  qs(params) { const u = new URLSearchParams(); for (const [k, v] of Object.entries(params || {})) if (v !== undefined && v !== null) u.set(k, typeof v === 'number' ? +v.toFixed(4) : v); const s = u.toString(); return s ? `?${s}` : ''; }
  async get(path, params) {
    if (!this.online) throw new Error('offline');
    try { const r = await fetchJson(`${this.base}${path}${this.qs(params)}`); this.errors = 0; return r; }
    catch (e) { this.errors++; throw e; }
  }
  async post(path, body) {
    if (!this.online) throw new Error('offline');
    return fetchJson(`${this.base}${path}`, { method: 'POST', body: JSON.stringify(body || {}) });
  }
}

// snake_case → camelCase, recursively (the wire format is snake_case; the UI speaks camelCase)
export function camel(o) {
  if (Array.isArray(o)) return o.map(camel);
  if (o && typeof o === 'object') {
    const out = {};
    for (const [k, v] of Object.entries(o)) out[k.replace(/_([a-z0-9])/g, (_, c) => c.toUpperCase())] = camel(v);
    return out;
  }
  return o;
}

/* ------------------------------------------------------------------ RemoteTwin */

export class RemoteTwin {
  constructor({ api, local, wellId = 'BGW-17', onUpdate }) {
    this.api = api; this.local = local; this.wellId = wellId; this.onUpdate = onUpdate;
    this.remote = {};            // latest responses, keyed by kind
    this.keys = {};              // the scenario key each response belongs to
    this.pending = null; this.timer = null;
    this.status = api.online ? 'connecting' : 'offline';
    this.lastError = null;
    if (api.online) this.start(); else this.retry();
  }

  start() { this.status = 'connecting'; this.refresh('all'); this.loadStatic(); this.onUpdate?.('status'); }
  // keep probing until the API is reachable, then swap it in
  retry() {
    clearTimeout(this.retryTimer);
    this.retryTimer = setTimeout(async () => {
      const api = await connectApi();
      if (api.online) { this.api = api; this.start(); if (this._liveCb) this.openLive(this._liveCb); } else this.retry();
    }, 4000);
  }

  get online() { return this.api.online && this.api.errors < 3; }
  // scenario = the parameters every derived number depends on
  params() { const p = this.local._p; return { day: +p.day.toFixed(2), spm: +p.spm.toFixed(3), kd: +p.kd.toFixed(3), steam: Math.round(p.steam) }; }
  key(p = this.params()) { return `${p.day}|${p.spm}|${p.kd}|${p.steam}`; }
  curveKey(p = this.params()) { return `${p.spm}|${p.kd}|${p.steam}`; }

  /* motion (local sim, never displayed) ------------------------------ */
  get theta() { return this.local.theta; }
  get state() { return this.local.state; }
  get _p() { return this.local._p; }
  step(dt) { this.local.step(dt); }
  animMetrics() { return this.local.metrics(); }       // drives 3D animation only

  set(p) {
    this.local.set(p);
    const which = (p.spm !== undefined || p.kd !== undefined || p.steam !== undefined) ? 'all' : 'day';
    if (this.api.online) this.schedule(which);
  }

  /* displayed data: API only. Stale-but-real answers are kept while a newer scenario is in flight. */
  metrics() {
    const r = this.remote.state;
    if (!r) return null;
    if (r !== this._mergedFrom) {
      this._mergedFrom = r;
      this._merged = { ...r.metrics, recommendation: r.recommendation ?? r.metrics.recommendation, derived: r.derived, source: r.source, stale: false };
    }
    this._merged.stale = this.keys.state !== this.key();
    return this._merged;
  }
  series() { return this.remote.series ?? null; }
  profile() { return this.remote.profile ?? null; }
  dynoCard() { return this.remote.dyno && this.remote.dyno.surface ? this.remote.dyno : null; }
  health() { return this.remote.health ?? null; }
  plan() { return this.remote.plan ?? null; }
  pastCycles() { return this.remote.series?.pastCycles ?? null; }
  planCurve() { return this.remote.series?.planCurve ?? null; }
  well() { return this.remote.well ?? null; }
  hasData() { return !!this.remote.state; }

  /* API plumbing ----------------------------------------------------- */

  schedule(which) {
    this.pending = this.pending === 'all' || which === 'all' ? 'all' : 'day';
    clearTimeout(this.timer);
    this.timer = setTimeout(() => { const w = this.pending; this.pending = null; this.refresh(w); }, 120);
  }

  async loadStatic() {
    try { this.remote.well = camel(await this.api.get(`/wells/${this.wellId}`)); this.onUpdate?.('well'); } catch (e) { this.fail(e); }
  }

  async refresh(which = 'day') {
    const p = this.params(), key = this.key(p), ck = this.curveKey(p), id = this.wellId;
    const q = { day: p.day, spm: p.spm, kd: p.kd, steam: p.steam };
    const jobs = [
      ['state', `/wells/${id}/state`, q, key],
      ['profile', `/wells/${id}/profile`, q, key],
      ['dyno', `/wells/${id}/dyno`, q, key],
      ['health', `/wells/${id}/health`, q, key],
      ['plan', `/wells/${id}/plan/next-cycle`, q, key],
    ];
    if (which === 'all' || !this.remote.series) jobs.push(['series', `/wells/${id}/series`, { spm: p.spm, kd: p.kd, steam: p.steam }, ck]);
    await Promise.all(jobs.map(async ([kind, path, params, k]) => {
      try {
        const r = camel(await this.api.get(path, params));
        if (k !== (kind === 'series' ? this.curveKey() : this.key())) return;   // superseded while in flight
        this.remote[kind] = r; this.keys[kind] = k;
        this.status = 'live'; this.lastError = null;
        this.onUpdate?.(kind);
      } catch (e) { this.fail(e); }
    }));
  }

  fail(e) {
    this.lastError = e;
    if (!this.online && this.status !== 'offline') { this.status = 'offline'; this.api.online = false; this.onUpdate?.('status'); this.retry(); }
  }

  // actions ---------------------------------------------------------
  async applyRecommendation(rec) {
    if (!this.api.online) return { applied: false, error: 'API unavailable' };
    try {
      const r = camel(await this.api.post(`/wells/${this.wellId}/apply`, { spm: rec.spm, kd: rec.kd }));
      this.set({ spm: rec.spm, kd: rec.kd });
      return r;
    } catch (e) { this.fail(e); return { applied: false, error: String(e.message || e) }; }
  }
  async schedulePlan(mantle) {
    if (!this.api.online) return { scheduled: false, error: 'API unavailable' };
    try { return camel(await this.api.post(`/wells/${this.wellId}/plan/schedule`, mantle ?? {})); } catch (e) { this.fail(e); return { scheduled: false, error: String(e.message || e) }; }
  }

  // live telemetry over WebSocket (anomaly score etc.); animation still comes from the local sim
  openLive(onMsg) {
    this._liveCb = onMsg;
    if (!this.api.online || this.ws) return;
    const url = this.api.base.replace(/^http/, 'ws') + `/wells/${this.wellId}/live`;
    try {
      this.ws = new WebSocket(url);
      this.ws.onmessage = (ev) => { try { const m = camel(JSON.parse(ev.data)); this.live = m; onMsg?.(m); } catch { /* ignore */ } };
      this.ws.onclose = () => { this.ws = null; this.live = null; setTimeout(() => this.api.online && this.openLive(onMsg), 3000); };
    } catch { this.ws = null; }
  }
}
