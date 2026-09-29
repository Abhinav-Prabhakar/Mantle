// Inspect mode: the camera flies in close, the machine comes apart (walking beam lifts, cranks swing
// out, the wellhead rises, the whole completion slides out of the rock with the rod string
// travelling furthest) and each part sends out a glass tag on a leader line with its own numbers.
// Two stops: the pumping unit at surface, and the downhole pump / rod string at depth.
import * as THREE from 'three';
import { UNIT, WELL, WELLBORE, depthToY } from './rig.js';
import { derive, ROD, UNSEATS, FLUID } from './mock.js';

const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const TAG_W = 214;
const k1 = (v) => (v >= 1000 ? `${(v / 1000).toFixed(1)}k` : v.toFixed(0));
const pips = (n, on, cls = 'on') => `<div class="pips">${Array.from({ length: n }, (_, i) => `<i class="${i < on ? cls : ''}"></i>`).join('')}</div>`;
function sparkline(vals, col = '#7cc4ff') {
  const lo = Math.min(...vals), hi = Math.max(...vals), n = vals.length;
  const pts = vals.map((v, i) => `${(i / (n - 1)) * 190 + 1},${24 - ((v - lo) / (hi - lo || 1)) * 20}`).join(' ');
  return `<svg class="spark-line" viewBox="0 0 192 26" preserveAspectRatio="none"><polyline points="${pts}" fill="none" stroke="${col}" stroke-width="1.6"/><line x1="96" y1="0" x2="96" y2="26" stroke="rgba(255,255,255,0.15)"/></svg>`;
}

export class Inspect {
  constructor({ camera, pumpjack, well, getSim, flyTo, onChange }) {
    Object.assign(this, { camera, pumpjack, well, getSim, flyTo, onChange });
    this.root = document.getElementById('inspect');
    this.svg = document.getElementById('insp-lines');
    this.tagLayer = document.getElementById('insp-tags');
    this.active = false; this.stop = null;
    this.ex = { unit: 0, head: 0, down: 0 }; this.exTarget = { unit: 0, head: 0, down: 0 };
    this.tags = [];
    this.v = new THREE.Vector3();
    document.querySelectorAll('#insp-stops button').forEach((b) => (b.onclick = () => this.go(b.dataset.stop)));
    document.getElementById('insp-exit').onclick = () => this.exit();
    this.addFailureMarks();
    this.defineStops();
  }

  // glowing rings on the rod string at the depths where rods have parted
  addFailureMarks() {
    this.marks = ROD.failures.map((f) => {
      const g = new THREE.Group();
      const ring = new THREE.Mesh(new THREE.TorusGeometry(0.13, 0.022, 8, 32), new THREE.MeshStandardMaterial({ color: 0x551010, emissive: 0xff3b2f, emissiveIntensity: 2.2, roughness: 0.4 }));
      ring.rotation.x = Math.PI / 2;
      const halo = new THREE.Mesh(new THREE.TorusGeometry(0.2, 0.008, 6, 32), new THREE.MeshBasicMaterial({ color: 0xff6b6b, transparent: true, opacity: 0.6 }));
      halo.rotation.x = Math.PI / 2;
      g.add(ring, halo);
      g.position.set(0, depthToY(f.depth), 0);
      g.visible = false;
      this.well.rods.add(g);
      return { g, halo, f };
    });
  }

  defineStops() {
    const pj = this.pumpjack, wl = this.well, WZ = WELL.z;
    const world = (obj, x, y, z) => obj.localToWorld(this.v.set(x, y, z)).clone();
    const d = () => this.d, m = () => this.m, st = () => this.getSim().state;
    this.stops = {
      surface: {
        pos: new THREE.Vector3(-7.5, 8.2, 17.5), target: new THREE.Vector3(4.6, 3.4, -1.6),
        explode: { unit: 1, head: 1, down: 0 },
        tags: [
          { id: 'rod', side: 'L', at: () => new THREE.Vector3(0, st().rodPos + UNIT.stuffingBoxY + 0.6, WZ), html: () => {
            const M = m(), lf = clamp(st().load / 120, 0, 1);
            return `<div class="it-k">Polished rod<em>${st().load.toFixed(0)} kN now</em></div><div class="it-v"><b>${M.pprl.toFixed(0)}</b><small>kN peak · ${M.mprl.toFixed(0)} min</small></div><div class="it-s">Stroke <b>${M.stroke.toFixed(2)} m</b> · ${st().spmActual.toFixed(1)} SPM</div>${pips(12, Math.round(lf * 12), lf > 0.85 ? 'warn' : 'on')}`; } },
          { id: 'beam', side: 'L', at: () => world(pj.parts.beam, -2.6, 0.4, 0), html: () => {
            const b = d().beamLoad;
            return `<div class="it-k">Walking beam</div><div class="it-v"><b>${(b * 100).toFixed(0)}</b><small>% of rated load</small></div><div class="it-s">Horsehead ${UNIT.A.toFixed(1)} m arm · saddle bearing OK</div>${pips(12, Math.round(b * 12), b > 0.85 ? 'warn' : 'on')}`; } },
          { id: 'head', side: 'L', at: () => world(wl.wellhead, 0, 1.55, 0), html: () => {
            const D = d();
            return `<div class="it-k">Thermal wellhead</div><div class="it-v"><b>${D.thp.toFixed(2)}</b><small>MPa tubing</small></div><div class="it-s">Casing <b>${D.chp.toFixed(2)} MPa</b> · flowline <b>${D.flowT.toFixed(0)} °C</b></div>`; } },
          { id: 'cw', side: 'R', at: () => world(pj.parts.cranks[1], -1.3, 0, 0), html: () => {
            const cb = d().counterbalance;
            return `<div class="it-k">Cranks &amp; counterweights</div><div class="it-v"><b>${(cb * 100).toFixed(0)}</b><small>% balanced</small></div><div class="it-s">4 blocks · 2 arms · ideal ≥ 95%</div>${pips(12, Math.round(cb * 12), cb < 0.9 ? 'warn' : 'on')}`; } },
          { id: 'gear', side: 'R', at: () => world(pj.root, (UNIT.gearbox.x0 + UNIT.gearbox.x1) / 2, UNIT.gearbox.y1 - 0.2, 0), html: () => {
            const t = m().torquePct;
            return `<div class="it-k">Gear reducer</div><div class="it-v"><b>${(t * 100).toFixed(0)}</b><small>% of 320k in-lb</small></div><div class="it-s">Peak net torque on the upstroke</div>${pips(12, Math.round(clamp(t, 0, 1) * 12), t > 1 ? 'bad' : t > 0.85 ? 'warn' : 'on')}`; } },
          { id: 'motor', side: 'R', at: () => world(pj.root, UNIT.motor.x, UNIT.motor.y + 0.4, 0), html: () => {
            const D = d(), M = m();
            return `<div class="it-k">Motor &amp; VFD<em>${M.motorKw.toFixed(1)} kW</em></div><div class="it-v"><b>${(st().spmActual * 50 / 9).toFixed(1)}</b><small>Hz · ${D.amps.toFixed(0)} A</small></div><div class="it-s">Speed across one stroke (kd ${M.kd.toFixed(2)})</div>${sparkline(D.profile)}`; } },
        ],
      },
      downhole: {
        pos: new THREE.Vector3(11, -11.5, 17), target: new THREE.Vector3(0.6, -16.6, -0.2),
        explode: { unit: 0, head: 0, down: 1 },
        tags: [
          { id: 'string', side: 'L', at: () => world(wl.rods, 0, depthToY(ROD.failures[1].depth), 0), html: () => {
            const M = m();
            return `<div class="it-k">Rod string<em>Goodman ${M.goodman.toFixed(2)}</em></div><div class="it-v"><b>${ROD.failures.length}</b><small>parted in 18 months</small></div><div class="it-s">${ROD.failures.map((f) => `<b>${f.size}</b> at ${f.depth} m`).join(' · ')}<br>MTBF <b>${ROD.mtbfDays} d</b> → ${ROD.mtbfMantle} d with Mantle</div>`; } },
          { id: 'pump', side: 'R', at: () => world(wl.rods, 0, depthToY(WELLBORE.pumpTop) + 0.2, 0), html: () => {
            const M = m(), D = d();
            return `<div class="it-k">Insert pump<em>1.25″</em></div><div class="it-v"><b>${(M.fillage * 100).toFixed(0)}</b><small>% fillage</small></div><div class="it-s"><b>${k1(D.impactsDay)}</b> impacts/day at ${D.impactVel.toFixed(2)} m/s</div>${pips(12, Math.round(M.fillage * 12), M.fillage < 0.7 ? 'warn' : 'on')}`; } },
          { id: 'hold', side: 'R', at: () => world(wl.sub, 0, depthToY(WELLBORE.pumpBottom) - 0.42, 0), html: () => {
            const D = d();
            return `<div class="it-k">Hold-down &amp; seat</div><div class="it-v"><b>${D.upliftMargin.toFixed(1)}×</b><small>uplift margin</small></div><div class="it-s">30-day unseat risk <b>${(D.unseatRisk * 100).toFixed(0)}%</b> · ${UNSEATS.events.length} unseats / 12 mo</div>`; }, level: () => (this.d.unseatRisk > 0.25 ? 'warn' : '') },
          { id: 'intake', side: 'L', at: () => world(wl.sub, -0.3, depthToY(WELLBORE.pumpBottom) - 0.8, 0), html: () => {
            const D = d(), M = m();
            return `<div class="it-k">Pump intake</div><div class="it-v"><b>${D.pip.toFixed(2)}</b><small>MPa intake pressure</small></div><div class="it-s">Submergence <b>${M.submergence.toFixed(0)} m</b> · crude <b>${k1(M.viscosity)} cP</b></div>`; } },
          { id: 'res', side: 'R', at: () => new THREE.Vector3(4.2, depthToY(1128), 0.02), html: () => {
            const M = m();
            return `<div class="it-k">Jodhpur Sandstone</div><div class="it-v"><b>${FLUID.pRes}</b><small>MPa · low pressure</small></div><div class="it-s"><b>${M.sandfaceT.toFixed(0)} °C</b> at sandface · base ${FLUID.tRes} °C · ${FLUID.api}° API · ${FLUID.asphaltene} wt% asphaltene</div>`; } },
        ],
      },
    };
  }

  enter(stop = 'surface') {
    if (this.active) { this.go(stop); return; }
    this.active = true;
    this.saved = { pos: this.camera.position.clone() };
    this.root.classList.add('active');
    document.body.classList.add('inspecting');
    this.onChange?.(true);
    this.go(stop);
  }

  go(stop) {
    this.stop = stop;
    document.querySelectorAll('#insp-stops button').forEach((b) => b.classList.toggle('active', b.dataset.stop === stop));
    const S = this.stops[stop];
    this.exTarget = { ...S.explode };
    this.buildTags(S);
    this.flyTo(S.pos, S.target, 1.8);
  }

  exit() {
    if (!this.active) return Promise.resolve();
    this.active = false;
    this.exTarget = { unit: 0, head: 0, down: 0 };
    this.clearTags();
    this.root.classList.remove('active');
    document.body.classList.remove('inspecting');
    this.onChange?.(false);
    return this.flyTo(null, null, 1.6);
  }

  buildTags(S) {
    this.clearTags();
    this.tags = S.tags.map((t, i) => {
      const el = document.createElement('div');
      el.className = 'itag';
      this.tagLayer.appendChild(el);
      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle'); dot.setAttribute('r', 3);
      const ring = document.createElementNS('http://www.w3.org/2000/svg', 'circle'); ring.setAttribute('r', 7); ring.setAttribute('class', 'ring');
      this.svg.append(path, ring, dot);
      return { ...t, el, path, dot, ring, born: performance.now() + 700 + i * 130, y: null };
    });
    this.refreshTags();
  }
  clearTags() {
    for (const t of this.tags) { t.el.remove(); t.path.remove(); t.dot.remove(); t.ring.remove(); }
    this.tags = [];
  }
  refreshTags() {
    if (!this.m) return;
    for (const t of this.tags) {
      t.el.innerHTML = t.html();
      t.el.className = `itag ${t.level?.() || ''} ${t.el.dataset.in ? 'in' : ''}`;
    }
  }

  setMetrics(m) {
    this.m = m; this.d = derive(m, this.getSim().state);
    if (this.active) this.refreshTags();
  }

  /* per frame: ease the explode, place tags on their projected anchors */
  frame(dt) {
    const e = 1 - Math.exp(-dt * 3.2);
    for (const k of ['unit', 'head', 'down']) this.ex[k] += (this.exTarget[k] - this.ex[k]) * e;
    const smooth = (x) => x * x * (3 - 2 * x);
    this.pumpjack.setExplode(smooth(clamp(this.ex.unit, 0, 1)));
    this.well.setExplode({ head: smooth(clamp(this.ex.head, 0, 1)), down: smooth(clamp(this.ex.down, 0, 1)) });
    const showMarks = this.ex.down > 0.3;
    for (const mk of this.marks) {
      mk.g.visible = showMarks;
      const p = 1 + 0.25 * Math.sin(performance.now() / 260);
      mk.halo.scale.setScalar(p); mk.halo.material.opacity = 0.7 * (1.25 - p) * 2;
    }
    if (!this.active || !this.tags.length) return;

    const w = window.innerWidth, h = window.innerHeight, now = performance.now();
    const top = 150, bottom = h - 110;
    const placed = { L: [], R: [] };
    for (const t of this.tags) {
      const p = t.at().project(this.camera);
      t.sx = (p.x * 0.5 + 0.5) * w; t.sy = (-p.y * 0.5 + 0.5) * h; t.vis = p.z < 1;
      t.h = t.el.offsetHeight || 90;
      placed[t.side].push(t);
    }
    for (const side of ['L', 'R']) {
      const list = placed[side].sort((a, b) => a.sy - b.sy);
      let y = top;
      for (const t of list) { t.ty = Math.max(y, t.sy - t.h / 2); y = t.ty + t.h + 10; }
      // if the column overflows the bottom, slide it back up (never above the header)
      const over = Math.min(y - 10 - bottom, list.length ? list[0].ty - top : 0);
      if (over > 0) for (const t of list) t.ty -= over;
    }
    for (const t of this.tags) {
      const left = t.side === 'L';
      let tx = left ? t.sx - TAG_W - 110 : t.sx + 110;
      tx = clamp(tx, 24, w - TAG_W - 24);
      if (t.y == null) t.y = t.ty; else t.y += (t.ty - t.y) * 0.25;
      const born = now >= t.born;
      if (born && !t.el.dataset.in) { t.el.dataset.in = '1'; t.el.classList.add('in'); }
      const k = born ? clamp((now - t.born) / 450, 0, 1) : 0, ek = 1 - Math.pow(1 - k, 3);
      // tags slide out from their part as they cascade in
      const ox = (1 - ek) * (left ? 40 : -40);
      t.el.style.transform = `translate(${tx + ox}px, ${t.y}px)`;
      const edgeX = left ? tx + TAG_W : tx, midY = t.y + 18;
      const elbowX = edgeX + (left ? 22 : -22);
      const ax = t.sx, ay = t.sy;
      const draw = ek * (t.vis ? 1 : 0);
      t.path.setAttribute('d', `M${ax},${ay} L${ax + (elbowX - ax) * draw},${ay + (midY - ay) * draw} L${elbowX + (edgeX - elbowX) * draw},${midY}`);
      t.path.style.opacity = draw;
      t.dot.setAttribute('cx', ax); t.dot.setAttribute('cy', ay); t.dot.style.opacity = t.vis ? Math.min(1, ek * 2) : 0;
      t.ring.setAttribute('cx', ax); t.ring.setAttribute('cy', ay);
      t.ring.setAttribute('r', 5 + 4 * ((now / 900 + t.born / 1000) % 1)); t.ring.style.opacity = t.vis ? (1 - ((now / 900 + t.born / 1000) % 1)) * ek : 0;
    }
  }
}
