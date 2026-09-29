// Mantle · Well View — entry point. Renderer, scene assembly, time of day, the live sim,
// HUD wiring and the Well ⇄ Section (3D → 2D) transition.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { SkySystem } from './sky.js';
import { buildTerrain } from './terrain.js';
import { buildPumpjack } from './pumpjack.js';
import { buildWell } from './well.js';
import { WELL, UNIT, STROKE, rodPosition } from './rig.js';
import { Hud } from './hud.js';
import { SectionView } from './section.js';
import { Inspect } from './inspect.js';
import { CYCLE } from './sim.js';

const $ = (id) => document.getElementById(id);
const params = new URLSearchParams(location.search);

/* ------------------------------------------------------------------ renderer */
const renderer = new THREE.WebGLRenderer({ antialias: false, powerPreference: 'high-performance', preserveDrawingBuffer: params.has('capture') });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.6;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
$('viewport').appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0xc8b8a0, 0.0011);
const camera = new THREE.PerspectiveCamera(36, window.innerWidth / window.innerHeight, 0.1, 30000);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true; controls.dampingFactor = 0.06;
controls.minDistance = 6; controls.maxDistance = 420;
controls.maxPolarAngle = Math.PI * 0.62;
controls.zoomToCursor = true;

const DEFAULT_TARGET = new THREE.Vector3(1, -7, -14);
const defaultCam = () => new THREE.Vector3(-50, 30, 96);
camera.position.copy(defaultCam());
controls.target.copy(DEFAULT_TARGET);
if (params.has('cam')) camera.position.fromArray(params.get('cam').split(',').map(Number));
if (params.has('tgt')) controls.target.fromArray(params.get('tgt').split(',').map(Number));
controls.update();

/* ------------------------------------------------------------------ world */
const sky = new SkySystem(renderer, scene);
const terrain = buildTerrain(scene);
const pumpjack = buildPumpjack();
scene.add(pumpjack.root);
const well = buildWell(scene);

let props = null;
try { props = (await import('./props.js')).buildProps(scene); } catch (e) { console.warn('props unavailable', e); }

/* ------------------------------------------------------------------ simulation (sim.js is optional while it's being written) */
let sim = null;
try { const { WellSim } = await import('./sim.js'); sim = new WellSim({ spm: 5.4, cycleDay: 41 }); } catch (e) { console.warn('sim unavailable', e); }
let fallbackTheta = 0;
let live = null, metricsTimer = 0, thermalLens = params.has('thermal');
let onMetrics = null;
if (sim && params.has('day')) sim.set({ cycleDay: parseFloat(params.get('day')) });

/* ------------------------------------------------------------------ post */
const composer = new EffectComposer(renderer, new THREE.WebGLRenderTarget(1, 1, { type: THREE.HalfFloatType, samples: 4 }));
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(256, 256), 0.15, 0.6, 1.3);
composer.addPass(bloom);
composer.addPass(new OutputPass());

function onResize() {
  const w = window.innerWidth, h = window.innerHeight;
  camera.aspect = w / h; camera.updateProjectionMatrix();
  renderer.setSize(w, h); composer.setSize(w, h);
  const pr = renderer.getPixelRatio();
  bloom.setSize(w * pr * 0.5, h * pr * 0.5);
}
window.addEventListener('resize', onResize);
onResize();

/* ------------------------------------------------------------------ time of day */
const ENV = { dayTime: 16.75, nightTime: 21.6, transitionSeconds: 6 };
let tod = params.has('t') ? parseFloat(params.get('t')) : params.has('night') ? ENV.nightTime : ENV.dayTime;
let todAnim = null;
const ease = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
function setTimeOfDay(h) { todAnim = null; tod = ((h % 24) + 24) % 24; sky.setTime(tod); }
function animateTo(target) {
  let end = target;
  while (end <= tod) end += 24;
  todAnim = { from: tod, to: end, t: 0, dur: ENV.transitionSeconds * Math.min(1.4, Math.max(0.6, (end - tod) / 8)) };
}
sky.setTime(tod);

/* ------------------------------------------------------------------ HUD + section view */
const hud = new Hud({ getSim: () => sim });
onMetrics = (m) => { hud.update(m); inspect.setMetrics(m); };
hud.onPickDay = (d) => setDay(d);
const section = new SectionView({ root: $('section'), getSim: () => sim, onPlayChange: () => {} });

/* ------------------------------------------------------------------ inspect mode (exploded machine) */
let inspectSaved = null;
function flyTo(pos, target, dur) {
  if (!pos) { if (!inspectSaved) return Promise.resolve(); pos = inspectSaved.pos; target = inspectSaved.target; inspectSaved = null; }
  sph.setFromVector3(pos.clone().sub(target));
  return tweenCamera({ toTarget: target.clone(), toTheta: sph.theta, toPhi: sph.phi, toFov: 36, toDist: sph.radius, dur });
}
const inspect = new Inspect({
  camera, pumpjack, well, getSim: () => sim, flyTo,
  onChange: (on) => {
    if (on && !inspectSaved) inspectSaved = { pos: camera.position.clone(), target: controls.target.clone() };
    $('btn-inspect').classList.toggle('on', on);
    $('tooltip').classList.remove('show');
  },
});
$('btn-inspect').onclick = () => (inspect.active ? inspect.exit() : inspect.enter('surface'));
// click the machine to inspect it: the pumping unit, or the completion below ground
{
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2();
  let down = null;
  renderer.domElement.addEventListener('pointerdown', (e) => (down = { x: e.clientX, y: e.clientY }));
  renderer.domElement.addEventListener('pointerup', (e) => {
    if (!down || Math.hypot(e.clientX - down.x, e.clientY - down.y) > 5 || screen !== 'well' || busy) return;
    ndc.set((e.clientX / innerWidth) * 2 - 1, -(e.clientY / innerHeight) * 2 + 1);
    ray.setFromCamera(ndc, camera);
    const hit = ray.intersectObjects([pumpjack.root, well.root], true)[0];
    if (!hit) return;
    inspect.enter(hit.point.y < -1 ? 'downhole' : 'surface');
  });
}

function setDay(d) { if (!sim) return; sim.set({ cycleDay: Math.min(CYCLE.days, Math.max(0, d)) }); metricsTimer = 0; syncDaySlider(); }
function syncDaySlider() { const d = sim.metrics().cycleDay; $('r-day').value = d; $('v-day').textContent = d.toFixed(0); }
let cyclePlaying = false;
function setCyclePlaying(on) {
  cyclePlaying = on;
  $('btn-play').classList.toggle('on', on);
  $('btn-play').innerHTML = on ? '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M7 5h4v14H7zM13 5h4v14h-4z" fill="currentColor"/></svg>' : '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M7 5l12 7-12 7z" fill="currentColor"/></svg>';
}

/* ------------------------------------------------------------------ controls */
const fmtTime = (h) => `${String(Math.floor(h) % 24).padStart(2, '0')}:${String(Math.floor((h % 1) * 60)).padStart(2, '0')}`;
function syncTod() {
  const night = sky.state.night > 0.5;
  $('btn-day').classList.toggle('active', !night); $('btn-night').classList.toggle('active', night);
  $('r-time').value = tod; $('v-time').textContent = fmtTime(tod);
}
$('btn-day').onclick = () => animateTo(ENV.dayTime);
$('btn-night').onclick = () => animateTo(ENV.nightTime);
$('r-time').oninput = (e) => { setTimeOfDay(parseFloat(e.target.value)); syncTod(); };
$('r-day').oninput = (e) => setDay(parseFloat(e.target.value));
$('r-spm').oninput = (e) => { const v = parseFloat(e.target.value); sim?.set({ spm: v }); $('v-spm').textContent = `${v.toFixed(1)} SPM`; metricsTimer = 0; };
const setLens = (on) => { thermalLens = on; $('btn-thermal').classList.toggle('active', on); $('btn-natural').classList.toggle('active', !on); };
$('btn-natural').onclick = () => setLens(false);
$('btn-thermal').onclick = () => setLens(true);
$('btn-play').onclick = () => setCyclePlaying(!cyclePlaying);
$('btn-cam').onclick = () => resetCamera();
$('adv-apply').onclick = () => {
  const r = hud.m?.recommendation; if (!r) return;
  sim.set({ spm: r.spm, kd: r.kd }); $('r-spm').value = r.spm; $('v-spm').textContent = `${r.spm.toFixed(1)} SPM`; metricsTimer = 0;
};
const drawer = $('metrics');
// drawer: 'peek' (KPI row only, the default so the section stays in view) or 'open' (all cards)
let drawerState = params.get('drawer') || 'peek';
function setDrawer(state) {
  drawerState = state;
  drawer.classList.toggle('open', state === 'open'); drawer.classList.toggle('peek', state === 'peek');
  $('ui').classList.toggle('drawer-open', state === 'open'); $('ui').classList.toggle('drawer-peek', state === 'peek');
}
$('metrics-tab').onclick = () => setDrawer(drawerState === 'open' ? 'peek' : 'open');
setDrawer(drawerState);
setLens(thermalLens);

function resetCamera() {
  const off = defaultCam().sub(DEFAULT_TARGET); sph.setFromVector3(off);
  tweenCamera({ toTarget: DEFAULT_TARGET.clone(), toTheta: sph.theta, toPhi: sph.phi, toFov: 36, toDist: sph.radius, dur: 1.4 });
}

window.addEventListener('keydown', (e) => {
  if (e.target.closest('input, textarea, select') || e.metaKey || e.ctrlKey) return;
  const k = e.key.toLowerCase();
  if (k === '1') switchScreen('well');
  if (k === '2') switchScreen('section');
  if (screen === 'section') {
    if (k === ' ') { e.preventDefault(); section.action('play'); }
    if (k === 'arrowleft') section.action('prev');
    if (k === 'arrowright') section.action('next');
    if (k === 'home') section.action('first');
    if (k === 'end') section.action('last');
    return;
  }
  if (busy) return;
  if (k === 'i') inspect.active ? inspect.exit() : inspect.enter('surface');
  if (k === 'escape' && inspect.active) inspect.exit();
  if (k === 'n') animateTo(sky.state.night > 0.5 ? ENV.dayTime : ENV.nightTime);
  if (k === 't') setLens(!thermalLens);
  if (k === 'm') setDrawer(drawerState === 'open' ? 'peek' : 'open');
  if (k === 'h') $('ui').classList.toggle('hidden');
  if (k === 'c') resetCamera();
  if (k === ' ') { e.preventDefault(); setCyclePlaying(!cyclePlaying); }
});

/* ------------------------------------------------------------------ screens: well <-> section */
let screen = 'well', busy = false, render3D = true, savedView = null;
function placeGlider() {
  const nav = $('screen-switch'), b = nav.querySelector('button.active'), gl = nav.querySelector('.glider');
  gl.style.left = `${b.offsetLeft}px`; gl.style.width = `${b.offsetWidth}px`;
}
document.querySelectorAll('#screen-switch button').forEach((b) => (b.onclick = () => switchScreen(b.dataset.screen)));
requestAnimationFrame(placeGlider);
window.addEventListener('resize', placeGlider);

// Camera tween in spherical coordinates with a dolly-zoom (fov + distance) that keeps apparent scale
// continuous, flattening the perspective into a near-orthographic elevation of the section face.
let camTween = null;
const sph = new THREE.Spherical();
function tweenCamera({ toTarget, toTheta, toPhi, toFov, toPpm, toDist, dur = 2.2 }) {
  return new Promise((resolve) => {
    const h = window.innerHeight;
    sph.setFromVector3(camera.position.clone().sub(controls.target));
    const fromPpm = h / (2 * sph.radius * Math.tan(THREE.MathUtils.degToRad(camera.fov) / 2));
    let dTheta = toTheta - sph.theta; dTheta = Math.atan2(Math.sin(dTheta), Math.cos(dTheta));
    const endPpm = toPpm ?? h / (2 * toDist * Math.tan(THREE.MathUtils.degToRad(toFov) / 2));
    camTween = { t: 0, dur, resolve, fromTarget: controls.target.clone(), toTarget, theta0: sph.theta, dTheta, phi0: sph.phi, toPhi, fov0: camera.fov, fov1: toFov, ppm0: fromPpm, ppm1: endPpm };
  });
}
function stepCamTween(dt) {
  const c = camTween;
  c.t = Math.min(1, c.t + dt / c.dur);
  const k = ease(c.t), h = window.innerHeight;
  const target = c.fromTarget.clone().lerp(c.toTarget, k);
  const fov = Math.exp(THREE.MathUtils.lerp(Math.log(c.fov0), Math.log(c.fov1), k));
  const ppm = Math.exp(THREE.MathUtils.lerp(Math.log(c.ppm0), Math.log(c.ppm1), k));
  const dist = h / (2 * ppm * Math.tan(THREE.MathUtils.degToRad(fov) / 2));
  camera.fov = fov; camera.updateProjectionMatrix();
  sph.set(dist, THREE.MathUtils.lerp(c.phi0, c.toPhi, k), c.theta0 + c.dTheta * k);
  camera.position.setFromSpherical(sph).add(target);
  camera.lookAt(target); controls.target.copy(target);
  if (c.t >= 1) { camTween = null; c.resolve(); }
}
const flatArgs = (L) => ({ toTarget: new THREE.Vector3(L.cx, L.cy, 0), toTheta: 0, toPhi: Math.PI / 2, toFov: 4, toPpm: L.ppm });
const setMode = (m) => document.body.classList.toggle('mode-section', m === 'section');

async function switchScreen(to) {
  if (busy || to === screen) return;
  busy = true;
  $('screen-switch').classList.add('busy');
  document.querySelectorAll('#screen-switch button').forEach((b) => b.classList.toggle('active', b.dataset.screen === to));
  placeGlider();
  $('tooltip').classList.remove('show', 'light');
  if (inspect.active) await inspect.exit();
  if (to === 'section') {
    savedView = { pos: camera.position.clone(), target: controls.target.clone() };
    controls.enabled = false;
    $('ui').classList.add('away');
    setCyclePlaying(false);
    const layout = section.startLayout(window.innerWidth, window.innerHeight);
    await tweenCamera({ ...flatArgs(layout), dur: 2.4 });
    screen = 'section';
    await section.enter({ from: layout, onCovered: () => { render3D = false; setMode('section'); } });
  } else {
    const layout = section.startLayout(window.innerWidth, window.innerHeight);
    await section.exit({ to: layout, onUncover: () => { render3D = true; clock.getDelta(); setMode(null); } });
    screen = 'well';
    const back = savedView || { pos: defaultCam(), target: DEFAULT_TARGET.clone() };
    sph.setFromVector3(back.pos.clone().sub(back.target));
    await tweenCamera({ toTarget: back.target.clone(), toTheta: sph.theta, toPhi: sph.phi, toFov: 36, toDist: sph.radius, dur: 2.3 });
    $('ui').classList.remove('away');
    controls.enabled = true; controls.update();
  }
  $('screen-switch').classList.remove('busy');
  busy = false;
}

/* ------------------------------------------------------------------ loop */
const clock = new THREE.Clock();
let elapsed = 0, viewShift = 0;
const focus = new THREE.Vector3(1, 0, -12);
let todSync = 0;
function loop() {
  const dt = Math.min(0.05, clock.getDelta());
  elapsed += dt;
  if (todAnim) {
    todAnim.t = Math.min(1, todAnim.t + dt / todAnim.dur);
    tod = (todAnim.from + (todAnim.to - todAnim.from) * ease(todAnim.t)) % 24;
    sky.setTime(tod);
    if (todAnim.t >= 1) todAnim = null;
  }
  if ((todSync -= dt) <= 0) { todSync = 0.1; syncTod(); }
  const env = sky.state;

  let theta, st = null;
  if (sim) {
    if (cyclePlaying && screen === 'well') {
      const d = sim.metrics().cycleDay + dt * 2;
      if (d >= CYCLE.days) { setDay(CYCLE.days); setCyclePlaying(false); } else sim.set({ cycleDay: d });
    }
    sim.step(dt); theta = sim.theta; st = sim.state;
  } else { fallbackTheta += dt * (2 * Math.PI * 5.4 / 60); theta = fallbackTheta; }
  metricsTimer -= dt;
  if (sim && metricsTimer <= 0) {
    metricsTimer = 0.25; live = sim.metrics(); onMetrics?.(live);
    if (document.activeElement !== $('r-day')) syncDaySlider();
  }

  if (camTween) stepCamTween(dt);
  // lift the scene above the metrics drawer (a view offset keeps the orbit pivot untouched)
  const shiftTarget = screen === 'well' && !busy && !inspect.active && !inspectSaved && !$('ui').classList.contains('hidden') ? (drawerState === 'open' ? drawer.offsetHeight * 0.4 : 70) : 0;
  viewShift += (shiftTarget - viewShift) * Math.min(1, dt * 5);
  if (Math.abs(viewShift) > 0.5) camera.setViewOffset(window.innerWidth, window.innerHeight, 0, viewShift, window.innerWidth, window.innerHeight);
  else if (camera.view && camera.view.enabled) camera.clearViewOffset();

  if (render3D) {
    sky.update(dt, elapsed, focus);
    scene.fog.color.copy(env.fogColor);
    // the dolly-zoom parks the camera far away; keep the haze tied to the framing, not the metres
    scene.fog.density = 0.0011 * Math.min(1, 110 / camera.position.distanceTo(controls.target));
    renderer.toneMappingExposure = env.exposure;
    bloom.strength = env.bloomStrength; bloom.threshold = env.bloomThreshold;
    inspect.frame(dt);
    pumpjack.update(theta);
    const rp = st ? st.rodPos : rodPosition(theta);
    const mu = live?.viscosity ?? 400;
    const mobility = Math.min(1, Math.max(0, (Math.log10(6000) - Math.log10(mu)) / (Math.log10(6000) - Math.log10(25))));
    const phase = st?.phase ?? 'PRODUCTION';
    const pxr = renderer.getPixelRatio() * window.innerHeight / 900;
    well.update({ dt, time: elapsed, rodPos: rp, fillage: live?.fillage ?? 0.78, phase, mobility, heatedRadius: live?.heatedRadius ?? 9, steamRate: phase === 'INJECTION' ? 1 : 0, pxRatio: pxr, lightLevel: 1 - env.night * 0.7 });
    const hu = terrain.heatUniforms;
    hu.uNightGlow.value = env.night;
    hu.uTPeak.value += ((live?.sandfaceT ?? 150) - hu.uTPeak.value) * Math.min(1, dt * 3);
    hu.uRh.value += ((live?.heatedRadius ?? 9) - hu.uRh.value) * Math.min(1, dt * 3);
    hu.uThermal.value += ((thermalLens ? 1 : 0) - hu.uThermal.value) * Math.min(1, dt * 4);
    hu.uTime.value = elapsed;
    hu.uMob.value = mobility;
    props?.update?.({ dt, time: elapsed, env, steamOn: phase === 'INJECTION' ? 1 : 0.25, pxRatio: pxr });
    if (controls.enabled) controls.update();
    composer.render();
    hud.frame();
  }
  section.frame(dt, theta);
  requestAnimationFrame(loop);
}

window.mantle = { THREE, scene, camera, controls, renderer, sky, pumpjack, well, terrain, section, hud, inspect, setTimeOfDay, animateTo, switchScreen, setDay, get sim() { return sim; } };
if (sim) { syncDaySlider(); hud.update(sim.metrics()); }
syncTod();
$('loader')?.classList.add('done');
loop();
if (params.get('screen') === 'section') setTimeout(() => switchScreen('section'), 600);
if (params.get('inspect')) setTimeout(() => inspect.enter(params.get('inspect')), 600);
