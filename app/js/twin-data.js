// Read-only accessors over the RemoteTwin's API answers. There is no fallback data anywhere: when the API
// hasn't answered, every getter returns null and the view renders its "unavailable" state.
const call = (sim, fn) => (sim && typeof sim[fn] === 'function' ? sim[fn]() : null);

export function derived(m) { return m?.derived ?? null; }
export function fluid(sim) { return call(sim, 'well')?.fluid ?? null; }
export function health(sim) { return call(sim, 'health'); }
export function plan(sim) { const p = call(sim, 'plan'); return p && p.practice && p.mantle ? p : null; }
export function pastCycles(sim) { const pc = call(sim, 'pastCycles'); return pc && pc.length ? pc : null; }
export function planCurve(sim) { const pc = call(sim, 'planCurve'); return pc && pc.day && pc.oil ? pc : null; }
export function rodMeta(sim) { return call(sim, 'well')?.rods ?? null; }

export function provenance(sim) {
  if (!sim || !sim.api?.online) return { mode: 'offline', label: 'Mantle API unavailable — no data is shown until it connects.' };
  const meta = sim.api.meta;
  const models = meta?.models?.map((x) => x.id).join(' · ');
  const srcs = meta?.sources?.map((x) => `${x.id} (${x.kind})`).join(', ');
  return {
    mode: sim.status === 'live' ? 'live' : 'connecting',
    label: `Live from the Mantle API${models ? ` · models ${models}` : ''}`,
    source: meta?.dataSource ?? null,
    sources: srcs ?? null,
  };
}
