// Backend client + RemoteTwin.
//
// The browser keeps its local WellSim for 60 fps animation (crank angle, rod position, live load) and for
// instant response while scrubbing. The Mantle API is authoritative for every displayed number: physics
// metrics (identical to the local sim by construction), and everything the ML/optimiser layer adds —
// forecast bands, dyno classification, failure risk, the pump recommendation and the next-cycle plan.
// RemoteTwin exposes the same interface as WellSim, so the HUD and section view don't care which side
// answered. If the API is unreachable the twin runs fully offline on the local sim + mock fixtures.

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
  if (params.has('offline')) return new Api(null);
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
    if (api.online) { this.refresh('all'); this.loadStatic(); }
  }

  get online() { return this.api.online && this.api.errors < 3; }
  // scenario = the parameters every derived number depends on
  params() { const p = this.local._p; return { day: +p.day.toFixed(2), spm: +p.spm.toFixed(3), kd: +p.kd.toFixed(3), steam: Math.round(p.steam) }; }
  key(p = this.params()) { return `${p.day}|${p.spm}|${p.kd}|${p.steam}`; }
  curveKey(p = this.params()) { return `${p.spm}|${p.kd}|${p.steam}`; }

  /* WellSim interface ------------------------------------------------ */
  get theta() { return this.local.theta; }
  get state() { return this.local.state; }
  get _p() { return this.local._p; }
  step(dt) { this.local.step(dt); }
  set(p) {
    this.local.set(p);
    if (!this.api.online) return;
    // curves only change with the operating policy; the rest with the day too
    const which = (p.spm !== undefined || p.kd !== undefined || p.steam !== undefined) ? 'all' : 'day';
    this.schedule(which);
  }
  // metrics: local physics immediately, overlaid by the API's answer for the same scenario
  metrics() {
    const m = this.local.metrics();
    const r = this.fresh('state');
    if (!r) return m;
    if (r !== this._mergedFrom) {                         // merge once per response
      this._mergedFrom = r;
      this._merged = { ...m, ...r.metrics, recommendation: r.recommendation ?? m.recommendation, alerts: r.metrics?.alerts ?? m.alerts, derived: r.derived, source: r.source };
    }
    return this._merged;
  }
  series() { const r = this.freshCurve('series'); return r ? r : this.local.series(); }
  profile() { const r = this.fresh('profile'); return r ? r : this.local.profile(); }
  dynoCard(n) { const r = this.fresh('dyno'); return r && r.surface ? r : this.local.dynoCard(n); }

  /* extras the local sim can't produce ------------------------------- */
  health() { return this.fresh('health', true); }
  plan() { return this.fresh('plan', true); }
  pastCycles() { return this.remote.series?.pastCycles ?? null; }
  planCurve() { return this.remote.series?.planCurve ?? null; }
  well() { return this.remote.well ?? null; }

  /* API plumbing ----------------------------------------------------- */
  fresh(kind, loose = false) { const r = this.remote[kind]; if (!r) return null; return loose || this.keys[kind] === this.key() ? r : null; }
  freshCurve(kind) { const r = this.remote[kind]; return r && this.keys[kind] === this.curveKey() ? r : null; }

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
    if (!this.online) { this.status = 'offline'; this.onUpdate?.('status'); }
  }

  // actions ---------------------------------------------------------
  async applyRecommendation(rec) {
    this.set({ spm: rec.spm, kd: rec.kd });
    if (!this.api.online) return { applied: true, offline: true };
    try { return camel(await this.api.post(`/wells/${this.wellId}/apply`, { spm: rec.spm, kd: rec.kd })); } catch (e) { this.fail(e); return { applied: true, offline: true }; }
  }
  async schedulePlan(plan) {
    if (!this.api.online) return { scheduled: true, offline: true };
    try { return camel(await this.api.post(`/wells/${this.wellId}/plan/schedule`, plan?.mantle ?? {})); } catch (e) { this.fail(e); return { scheduled: true, offline: true }; }
  }

  // live telemetry over WebSocket (anomaly score etc.); animation still comes from the local sim
  openLive(onMsg) {
    if (!this.api.online || this.ws) return;
    const url = this.api.base.replace(/^http/, 'ws') + `/wells/${this.wellId}/live`;
    try {
      this.ws = new WebSocket(url);
      this.ws.onmessage = (ev) => { try { const m = camel(JSON.parse(ev.data)); this.live = m; onMsg?.(m); } catch { /* ignore */ } };
      this.ws.onclose = () => { this.ws = null; setTimeout(() => this.api.online && this.openLive(onMsg), 3000); };
    } catch { this.ws = null; }
  }
}
