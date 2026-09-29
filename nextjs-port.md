# Prompt: port Mantle's Well View from plain HTML/CSS/JS to Next.js

> Hand this whole file to the agent doing the port. Run it only after the backend wiring (backend.md §9 step 7)
> has been merged, so the API client is ported too.

---

You are porting **Mantle**, a digital-twin web app for a heavy-oil well (Oil India, Baghewala field, SIH 2026
PS SIH26120), from a no-framework page in `app/` to a **Next.js (App Router) + React 19 + TypeScript** app in a
new `web/` directory. The current app is visually finished and heavily interactive. Your job is a **lossless
port**: every feature, animation, number, hover, keyboard shortcut and transition must survive, and it must
look pixel-identical. Performance must be equal or better. Do not redesign anything.

Do **not** read `README.md`, `plan.md`, `plan.pdf` or anything in `docs/`; they are outdated. The source of truth
is the code in `app/`, plus `backend.md` for the API.

## Ground rules

1. **Preserve the original.** Before changing anything, copy `app/` to `backup/app-html/` (commit that alone
   first). Never edit `backup/`. Keep `app/` working until the port is verified; the Docker `web` service
   switches to `web/` only at the end.
2. **Package manager:** pnpm. Node 22. Next.js latest stable, React 19, TypeScript strict. No UI kit, no
   Tailwind: move `app/style.css` over as global CSS (then optionally split into CSS modules without changing
   any rule's effect). Keep the Inter / JetBrains Mono fonts via `next/font`.
3. **three.js:** keep the vendored version (0.170) or pin `three@0.170.0` exactly; same addons. The 3D scene
   code in `app/js/{terrain,sky,pumpjack,well,props,vegetation,textures,util3d,rig,sim,section,inspect}.js` is
   imperative and tuned: **port it as TypeScript modules with the same logic** and mount it once from a
   client component (`'use client'`, dynamic import with `ssr: false`). You may move pieces to
   `@react-three/fiber` **only** where it is provably lossless (same frame order, same post-processing chain:
   RenderPass → UnrealBloom → OutputPass, same shadow settings, same tone mapping/exposure logic, same
   `setViewOffset` drawer shift). When in doubt keep it imperative. The renderer, scene, camera, the section
   canvas and the inspect overlay must be created once and survive route/state changes; never re-create the
   WebGL context on re-render.
4. **State:** one small store (Zustand) for UI state (screen, drawer state, lens, time of day, inspect stop,
   cycle playing, advisor tab) plus the API data. The 60 fps loop must not trigger React renders: the loop
   writes to DOM refs or canvases directly exactly as today (telemetry numbers, dyno canvas, stroke strip,
   inspect tags). React owns structure; the loop owns per-frame values.
5. **API:** port `app/js/api.js` (the backend client with offline fallback to the local sim) to typed
   TypeScript, types generated from `backend/openapi.json` (`openapi-typescript`). Same endpoints, same
   fallback behaviour, same "Simulated" provenance display. Next.js must proxy `/api/*` to the FastAPI service
   (`rewrites` → `http://api:8000` in Docker, `http://localhost:8000` in dev).
6. **No SSR of the scene.** The page shell can be server-rendered; everything WebGL/canvas is client-only.
   The loader overlay must still cover the first paint until the scene is ready.
7. **Commit in small steps** (each step builds, tests pass) and push to the current branch.

## Feature inventory — every item must work identically after the port

**Boot**: loader overlay ("MANTLE", bar, text), fades out when the scene is ready; error text if a module fails.

**3D Well View**
- Cut-block diorama (terrain slab, strata cut faces with heat shader, slot to the wellbore), sky with sun,
  moon, stars, Milky Way, cirrus, fog scaled to camera distance, PMREM environment, bloom per time of day.
- Pumping unit animation driven by the sim's crank angle; rods, plunger, valves, fluid column, oil particles,
  steam particles; props (steam generator + plume, tanks, cabin, VFD, masts with night spotlights, power
  line, fence, vegetation, stones, oil stains).
- OrbitControls with damping, limits and zoom-to-cursor; `C` / reset button tweens back to the default view.
- Drawer-aware framing: the scene lifts via `camera.setViewOffset` when the metrics drawer peeks/opens.
- Day/Night buttons, time slider, `N` key; animated time transitions; lights/windows/beacons follow.
- Thermal lens (Natural/Thermal, `T` key), eased in the shader.
- Cycle day slider (phase-coloured track), pump-speed slider, cycle play (`Space`), auto-stop at day 120.
- Click the machine (pumping unit or completion) to enter Inspect.

**HUD (glass)**
- Top-left: brand, SIMULATED pill (tooltip), well name, phase subtitle, live drive telemetry (SPM, stroke,
  VFD Hz, motor A, rod load) updated every frame.
- Value card (₹/day, ₹/bbl) with a hover cost-anatomy dropdown (stacked bar + rows + revenue).
- Steam-cycle panel: canvas ring (phases, progress, cut-off tick, thermal-battery arc), day, phase, stats.
- Advisor with Pump / Next-cycle tabs: recommendation, drive changes (VFD Hz, speed profile, stroke),
  delta chips, Apply (sets SPM/kd); next-cycle levers (hollow = today, glowing = Mantle), dividend with bars,
  "Schedule for cycle 5".
- Control deck; hint bar; screen switch with sliding glider.
- Metrics drawer with three states (closed/peek/open), `M` key, alert dot on its tab; KPI row (9 KPIs with
  hover tooltips and bars); cards: cycle production (history, P10–P90, Mantle plan, temperature, cut-off,
  hover + click-to-jump day), dynamometer card (live dot, PPRL/MPRL, impact burst, classification, torque),
  heat & pressure vs depth, rod & pump health (140-rod fatigue grid with failed rods and per-rod tooltips,
  live stroke/impact strip, 12-month unseat calendar, MTBF, alert line).
- Tooltips everywhere they exist today, same text, same positioning/flip logic.
- Responsive rules at 1300 px and 900 px.

**Inspect mode** (`I`, button, or click the model; `Esc`/Done exits)
- Camera fly-in; exploded pumping unit (beam lift, cranks spread, pitmans follow, wellhead lift); downhole
  stop slides the completion out of the rock with the rod string travelling further; perforations stay in
  the rock; parted-rod rings glow on the rods.
- Glass tags on SVG leader lines, cascading in with stagger, de-overlapped per side, following the camera
  while orbiting; tag contents refresh with live metrics. The HUD fades except the header; the inspect bar
  (stops + Done) replaces the deck. Exiting restores the camera exactly.

**Section (cream blueprint)** (`2` / tab; `1` back)
- Dolly-zoom camera flatten to an orthographic-looking elevation; the canvas drawing crystallises top-down
  with the blue sweep line exactly aligned with the 3D face; then eases to its working layout. Reverse on exit.
- Drawing: grid, hatched strata with labels, scale-break marks, ruler, wellbore (cement, casing, tubing,
  rods moving with the rod position, pump with valves opening/closing, perforations, fluid level), live
  pumping-unit elevation from the linkage solver, ghost equipment, callouts, isotherms / mobility contours
  with labels and heated-radius dimension, depth tracks (temperature, viscosity, pressure).
- Legend panel: overlay seg (Isotherms / Mobility / Geology), zoom presets (Full / Pump / Reservoir), title
  block (fluid properties + live PIP). Pan (drag), zoom (wheel, about the cursor), double-click reset,
  hover tooltips by formation / component.
- Dock: timeline (phases, oil curve, cut-off, playhead, scrub), next-cycle plan row, transport buttons,
  speed seg, Tracks / Callouts toggles, keyboard (Space, ←, →, Home, End); thermal-battery card.

## Performance (do after parity is confirmed)

Measure before/after with the Chrome performance panel and `renderer.info`: target a steady 60 fps on an
M-series laptop at 1600×1000, first meaningful paint < 2 s from cache. Allowed: code-splitting, texture
generation moved to a Web Worker / OffscreenCanvas (the procedural textures are the main boot cost), instancing,
fewer draw calls, `frameloop` throttling while the tab is hidden, avoiding layout thrash in the per-frame DOM
writes. Not allowed: lowering visual quality without asking.

## Verification you must do

1. Side-by-side screenshots (Puppeteer) of `backup/app-html` and `web/` at the same URL params
   (`?capture`, `&night`, `&screen=section`, `&inspect=surface`, `&inspect=downhole`, `&drawer=open`,
   `&thermal`) — diff them; explain any pixel difference.
2. A written checklist of every inventory item above, ticked with how you verified it.
3. `pnpm build` clean, `pnpm lint` clean, Playwright e2e covering: boot, day/night, drawer states, tabs,
   apply recommendation, inspect both stops, section enter/exit, timeline scrub, offline fallback.
4. Update `docker-compose.yml` so the `web` service builds and serves `web/` (Next standalone output)
   and still proxies `/api` to the API service. `docker compose up` must work from a clean clone.
