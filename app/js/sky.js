// Desert atmosphere: Preetham daylight scattering with a dusty (high-turbidity) horizon,
// high cirrus, and a night sky (stars, Milky Way, moon). One setTime(h) drives the sun,
// moon and hemisphere lights, fog, exposure, bloom and the PMREM environment.
import * as THREE from 'three';

const VERT = /* glsl */`
uniform vec3 uSunDir;
uniform float uRayleigh, uTurbidity, uMie;
varying vec3 vWorld;
varying float vSunE;
varying vec3 vBetaR, vBetaM;
const vec3 totalRayleigh = vec3(5.804542996261093E-6, 1.3562911419845635E-5, 3.0265902468824876E-5);
const vec3 MieConst = vec3(1.8399918514433978E14, 2.7798023919660528E14, 4.0790479543861094E14);
void main() {
  vec4 wp = modelMatrix * vec4(position, 1.0);
  vWorld = wp.xyz;
  gl_Position = projectionMatrix * viewMatrix * wp;
  gl_Position.z = gl_Position.w;
  float zc = clamp(uSunDir.y, -1.0, 1.0);
  vSunE = 1000.0 * max(0.0, 1.0 - exp(-((1.6110731556870734 - acos(zc)) / 1.5)));
  vBetaR = totalRayleigh * uRayleigh;
  vBetaM = 0.434 * (0.2 * uTurbidity) * 10E-18 * MieConst * uMie;
}`;

const FRAG = /* glsl */`
uniform vec3 uSunDir, uMoonDir;
uniform float uMieG, uNight, uTime, uCloudCover, uSunDisk, uDust;
uniform vec2 uCloudShift;
uniform vec3 uCloudSun, uCloudAmb, uDustCol, uVoid, uVoidHaze;
varying vec3 vWorld;
varying float vSunE;
varying vec3 vBetaR, vBetaM;
const float pi = 3.141592653589793;

float hash12(vec2 p){ vec3 p3 = fract(vec3(p.xyx)*0.1031); p3 += dot(p3, p3.yzx+33.33); return fract((p3.x+p3.y)*p3.z); }
float hash13(vec3 p3){ p3 = fract(p3*0.1031); p3 += dot(p3, p3.zyx+31.32); return fract((p3.x+p3.y)*p3.z); }
float vnoise(vec2 p){ vec2 i=floor(p), f=fract(p); vec2 u=f*f*(3.0-2.0*f);
  return mix(mix(hash12(i),hash12(i+vec2(1,0)),u.x), mix(hash12(i+vec2(0,1)),hash12(i+vec2(1,1)),u.x), u.y); }
float fbm(vec2 p){ float s=0.0,a=0.5; mat2 r=mat2(0.8,0.6,-0.6,0.8); for(int i=0;i<6;i++){ s+=a*vnoise(p); p=r*p*2.03+11.7; a*=0.5; } return s; }

vec3 preetham(vec3 dir){
  float zen = acos(max(0.0, dir.y));
  float inv = 1.0 / (cos(zen) + 0.15 * pow(93.885 - ((zen*180.0)/pi), -1.253));
  vec3 Fex = exp(-(vBetaR*8.4E3*inv + vBetaM*1.25E3*inv));
  float ct = dot(dir, uSunDir);
  float rPh = 0.05968310365946075 * (1.0 + pow(ct*0.5+0.5, 2.0));
  float g2 = uMieG*uMieG;
  float mPh = 0.07957747154594767 * ((1.0-g2) / pow(1.0 - 2.0*uMieG*ct + g2, 1.5));
  vec3 bt = vBetaR*rPh + vBetaM*mPh;
  vec3 Lin = pow(vSunE * (bt/(vBetaR+vBetaM)) * (1.0-Fex), vec3(1.5));
  Lin *= mix(vec3(1.0), pow(vSunE*(bt/(vBetaR+vBetaM))*Fex, vec3(0.5)), clamp(pow(1.0-uSunDir.y, 5.0), 0.0, 1.0));
  vec3 L0 = vec3(0.1)*Fex;
  float disk = smoothstep(0.99995, 0.99997, ct);
  L0 += (vSunE*19000.0*Fex) * disk * uSunDisk;
  vec3 c = (Lin + L0) * 0.04 + vec3(0.0, 0.0003, 0.00075);
  return pow(c, vec3(1.0/2.4));
}

void main(){
  vec3 dir = normalize(vWorld - cameraPosition);
  float below = smoothstep(0.0, -0.2, dir.y);
  vec3 hd = normalize(vec3(dir.x, max(dir.y, 0.0), dir.z));
  vec3 col = preetham(hd);

  // desert dust: a warm ochre veil hugging the horizon, brightest toward the sun
  float h = max(dir.y, 0.0);
  float band = exp(-h * 9.0);
  float toward = pow(max(dot(hd, uSunDir), 0.0), 3.0);
  col = mix(col, uDustCol * (0.75 + 0.6 * toward), band * uDust);

  // night
  vec3 nightCol = mix(vec3(0.030, 0.038, 0.062), vec3(0.004, 0.007, 0.018), pow(h, 0.42));
  nightCol += vec3(0.04, 0.03, 0.025) * exp(-h * 14.0);          // faint sodium/sky glow at the horizon
  col = mix(col, nightCol + col * 0.2, uNight);

  // moon
  float md = dot(dir, uMoonDir);
  float moonR = 0.0105;
  float disk = smoothstep(cos(moonR*1.04), cos(moonR*0.96), md);
  vec3 mcol = vec3(0.0);
  if (disk > 0.0) {
    vec3 t1 = normalize(cross(uMoonDir, vec3(0,1,0))), t2 = cross(t1, uMoonDir);
    vec2 mp = vec2(dot(dir,t1), dot(dir,t2)) / moonR;
    float maria = fbm(mp*2.2 + 4.0);
    float limb = sqrt(max(0.0, 1.0 - dot(mp,mp)));
    mcol = vec3(1.0,0.97,0.9) * (0.55+0.45*limb) * (1.05 - smoothstep(0.45,0.75,maria)*0.45) * 3.0 * disk;
  }
  float halo = pow(max(md,0.0), 900.0)*0.35 + pow(max(md,0.0), 60.0)*0.04;
  mcol += vec3(0.75,0.82,1.0) * halo;

  // stars (dense desert sky) + Milky Way
  vec3 sp = dir * 360.0; vec3 cell = floor(sp);
  float sh = hash13(cell), star = 0.0;
  if (sh > 0.9955) {
    vec3 c = cell + 0.5 + (vec3(hash13(cell+1.3), hash13(cell+7.1), hash13(cell+3.7)) - 0.5) * 0.7;
    float d = length(sp - c), mag = pow(hash13(cell+5.5), 3.0);
    float tw = 0.7 + 0.3 * sin(uTime * (2.0 + mag*5.0) + sh*90.0);
    star = smoothstep(0.34 + mag*0.25, 0.0, d) * (0.35 + mag*3.8) * tw;
  }
  vec3 mwAxis = normalize(vec3(0.35, 0.5, -0.79));
  float mwD = dot(dir, mwAxis);
  float mw = exp(-mwD*mwD*14.0) * (0.35 + fbm(dir.xz*7.0 + dir.y*2.0)) * (1.0 - 0.6*smoothstep(0.55,0.8,fbm(dir.xy*14.0 + 3.0)));
  vec3 starTint = mix(vec3(1.0,0.85,0.7), vec3(0.75,0.85,1.0), hash13(cell+9.1));
  vec3 stars = (starTint*star + vec3(0.07,0.07,0.09)*mw) * smoothstep(0.0, 0.16, dir.y);
  col += (stars + mcol) * uNight;

  // high cirrus: thin, streaky, silver-lined toward the sun
  if (dir.y > 0.0 && uCloudCover > 0.0) {
    vec2 cp = dir.xz / (dir.y + 0.08);
    cp = cp * vec2(0.35, 0.9) + uCloudShift;
    float n = fbm(cp);
    float streak = fbm(cp * vec2(0.3, 4.5) + 20.0);
    float c0 = 1.0 - uCloudCover;
    float dens = smoothstep(c0, c0 + 0.35, n * 0.55 + streak * 0.55);
    float silver = pow(max(dot(dir, uSunDir), 0.0), 8.0) * 2.2;
    vec3 cc = uCloudSun * (0.85 + silver) + uCloudAmb;
    cc += vec3(0.8,0.85,1.0) * halo * 3.0 * uNight;
    dens *= smoothstep(0.0, 0.2, dir.y) * 0.8;
    col = mix(col, cc, dens);
  }

  // below the horizon: the diorama floats in a calm void; a soft haze band keeps the horizon
  float dn = max(-dir.y, 0.0);
  vec3 voidCol = mix(uVoidHaze, uVoid, smoothstep(0.0, 0.32, dn));
  col = mix(col, voidCol, smoothstep(0.035, -0.06, dir.y));
  gl_FragColor = vec4(col, 1.0);
  #include <tonemapping_fragment>
  #include <colorspace_fragment>
}`;

const smooth = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
const lerp = (a, b, t) => a + (b - a) * t;
const ramp = (stops, x) => {
  if (x <= stops[0][0]) return stops[0][1].slice();
  for (let i = 1; i < stops.length; i++) if (x <= stops[i][0]) {
    const t = (x - stops[i - 1][0]) / (stops[i][0] - stops[i - 1][0]);
    return stops[i - 1][1].map((v, k) => lerp(v, stops[i][1][k], t));
  }
  return stops[stops.length - 1][1].slice();
};

export class SkySystem {
  constructor(renderer, scene) {
    this.renderer = renderer; this.scene = scene;
    this.uniforms = {
      uSunDir: { value: new THREE.Vector3(0, 1, 0) },
      uMoonDir: { value: new THREE.Vector3(0.42, 0.34, -0.84).normalize() },
      uRayleigh: { value: 1.45 }, uTurbidity: { value: 4.6 }, uMie: { value: 0.006 }, uMieG: { value: 0.83 },
      uNight: { value: 0 }, uTime: { value: 0 }, uCloudCover: { value: 0.3 },
      uCloudShift: { value: new THREE.Vector2() },
      uCloudSun: { value: new THREE.Color(1, 1, 1) }, uCloudAmb: { value: new THREE.Color(0.4, 0.45, 0.55) },
      uSunDisk: { value: 1 }, uVoid: { value: new THREE.Color() }, uVoidHaze: { value: new THREE.Color() }, uDust: { value: 0.55 }, uDustCol: { value: new THREE.Color(0.85, 0.7, 0.52) },
    };
    this.material = new THREE.ShaderMaterial({ uniforms: this.uniforms, vertexShader: VERT, fragmentShader: FRAG, side: THREE.BackSide, depthWrite: false });
    this.mesh = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), this.material);
    this.mesh.scale.setScalar(20000); this.mesh.frustumCulled = false; this.mesh.renderOrder = -10;
    scene.add(this.mesh);

    // reflection/IBL probe scene (no sun disk)
    this.envScene = new THREE.Scene();
    const envMat = this.material.clone();
    envMat.uniforms = Object.assign({}, this.uniforms, { uSunDisk: { value: 0 } });
    const envSky = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), envMat);
    envSky.scale.setScalar(100);
    this.envScene.add(envSky);
    // a warm ground plane in the probe so the lower hemisphere reflects sand, not void
    this.envGround = new THREE.Mesh(new THREE.PlaneGeometry(400, 400).rotateX(-Math.PI / 2), new THREE.MeshBasicMaterial({ color: 0x8a6a48 }));
    this.envGround.position.y = -2;
    this.envScene.add(this.envGround);
    this.pmrem = new THREE.PMREMGenerator(renderer);
    this.envRT = null; this.lastKey = null; this.envTimer = 0;

    this.sun = new THREE.DirectionalLight(0xffffff, 5);
    this.sun.castShadow = true;
    this.sun.shadow.mapSize.set(4096, 4096);
    const sc = this.sun.shadow.camera;
    sc.left = -62; sc.right = 62; sc.top = 62; sc.bottom = -62; sc.near = 1; sc.far = 400;
    this.sun.shadow.bias = -0.00018; this.sun.shadow.normalBias = 0.035; this.sun.shadow.radius = 3;
    scene.add(this.sun, this.sun.target);

    this.moon = new THREE.DirectionalLight(0x9fb4ff, 0);
    this.moon.castShadow = true;
    this.moon.shadow.mapSize.set(2048, 2048);
    Object.assign(this.moon.shadow.camera, { left: -40, right: 40, top: 40, bottom: -40, near: 1, far: 400 });
    this.moon.shadow.bias = -0.0003; this.moon.shadow.normalBias = 0.04;
    scene.add(this.moon, this.moon.target);

    this.hemi = new THREE.HemisphereLight(0xa9c2e6, 0x6b4f33, 0.4);
    scene.add(this.hemi);

    this.state = {};
    this.cloudShift = new THREE.Vector2();
    this.setTime(16.75);
  }

  sunDirection(hours, out = new THREE.Vector3()) {
    // Rajasthan (~28°N): sun rises in the east (−z here is north, +x east), culminates in the south (+z).
    const dayT = (hours - 6.1) / 12.6;
    const elev = THREE.MathUtils.degToRad(66) * Math.sin(Math.PI * dayT);
    const az = THREE.MathUtils.degToRad(-100 + dayT * 200);        // east → south → west
    out.set(Math.cos(elev) * Math.sin(-az) * 1, Math.sin(elev), Math.cos(elev) * Math.cos(az));
    return out.normalize();
  }

  setTime(hours) {
    this.time = ((hours % 24) + 24) % 24;
    const u = this.uniforms, s = this.state;
    const sunDir = this.sunDirection(this.time, u.uSunDir.value);
    const elev = THREE.MathUtils.radToDeg(Math.asin(sunDir.y));
    const night = smooth(1.0, -10, elev);
    s.elevation = elev; s.night = night; s.lightsOn = smooth(6, -2, elev); s.sunDir = sunDir; s.moonDir = u.uMoonDir.value;
    u.uNight.value = night;

    const sc = ramp([[-2, [1.0, 0.32, 0.1]], [2, [1.0, 0.48, 0.22]], [8, [1.0, 0.7, 0.46]], [20, [1.0, 0.87, 0.72]], [45, [1.0, 0.95, 0.88]]], elev);
    const si = 6.6 * smooth(-1.2, 5, elev) * (0.55 + 0.45 * smooth(4, 35, elev));
    this.sun.color.setRGB(sc[0], sc[1], sc[2]);
    this.sun.intensity = si; this.sun.visible = si > 0.002;
    s.sunColor = new THREE.Color(sc[0], sc[1], sc[2]).multiplyScalar(si);

    this.moon.intensity = 0.34 * night; this.moon.visible = night > 0.05;
    const hs = ramp([[-12, [0.09, 0.12, 0.2]], [-3, [0.35, 0.3, 0.42]], [4, [0.8, 0.62, 0.55]], [20, [0.72, 0.8, 0.95]]], elev);
    const hg = ramp([[-12, [0.03, 0.03, 0.04]], [0, [0.3, 0.2, 0.14]], [20, [0.55, 0.4, 0.26]]], elev);
    this.hemi.color.setRGB(hs[0], hs[1], hs[2]); this.hemi.groundColor.setRGB(hg[0], hg[1], hg[2]);
    this.hemi.intensity = lerp(0.32, 0.9, night);

    const cs = ramp([[-8, [0.03, 0.035, 0.05]], [-2, [0.4, 0.16, 0.1]], [3, [1.1, 0.5, 0.25]], [10, [1.2, 0.9, 0.65]], [30, [1.3, 1.25, 1.18]]], elev);
    const ca = ramp([[-8, [0.02, 0.025, 0.04]], [-2, [0.14, 0.1, 0.14]], [4, [0.34, 0.26, 0.28]], [20, [0.45, 0.5, 0.6]]], elev);
    u.uCloudSun.value.setRGB(cs[0], cs[1], cs[2]); u.uCloudAmb.value.setRGB(ca[0], ca[1], ca[2]);

    const dc = ramp([[-10, [0.02, 0.022, 0.03]], [-2, [0.35, 0.2, 0.14]], [3, [0.95, 0.52, 0.28]], [12, [0.95, 0.74, 0.52]], [40, [0.9, 0.82, 0.7]]], elev);
    u.uDustCol.value.setRGB(dc[0], dc[1], dc[2]);
    u.uDust.value = lerp(0.55, 0.2, night);
    const vd = ramp([[-12, [0.012, 0.014, 0.022]], [-3, [0.05, 0.042, 0.05]], [4, [0.2, 0.15, 0.13]], [20, [0.24, 0.225, 0.21]]], elev);
    const vh = ramp([[-12, [0.03, 0.034, 0.05]], [-3, [0.2, 0.12, 0.1]], [4, [0.62, 0.42, 0.3]], [20, [0.6, 0.55, 0.5]]], elev);
    u.uVoid.value.setRGB(vd[0], vd[1], vd[2]); u.uVoidHaze.value.setRGB(vh[0], vh[1], vh[2]);

    const fog = ramp([[-10, [0.018, 0.022, 0.034]], [-3, [0.16, 0.11, 0.12]], [2, [0.72, 0.46, 0.3]], [8, [0.82, 0.66, 0.5]], [20, [0.8, 0.74, 0.66]], [50, [0.74, 0.76, 0.78]]], elev);
    s.fogColor = new THREE.Color(fog[0], fog[1], fog[2]);
    s.exposure = lerp(0.52, 1.05, night);
    s.bloomStrength = lerp(0.1, 0.7, s.lightsOn);
    s.bloomThreshold = lerp(1.4, 0.62, s.lightsOn);
    s.envIntensity = lerp(0.62, 0.28, night);
    this.envGround.material.color.setRGB(lerp(0.54, 0.03, night), lerp(0.4, 0.03, night), lerp(0.28, 0.04, night));
  }

  update(dt, elapsed, focus) {
    const u = this.uniforms;
    u.uTime.value = elapsed;
    this.cloudShift.x += dt * 0.0016; this.cloudShift.y += dt * 0.0005;
    u.uCloudShift.value.copy(this.cloudShift);
    this.sun.position.copy(focus).addScaledVector(this.state.sunDir, 180);
    this.sun.target.position.copy(focus);
    this.moon.position.copy(focus).addScaledVector(this.state.moonDir, 180);
    this.moon.target.position.copy(focus);

    this.envTimer -= dt;
    const key = `${this.state.elevation.toFixed(1)}|${this.time.toFixed(2)}`;
    if (key !== this.lastKey && this.envTimer <= 0) {
      this.lastKey = key; this.envTimer = 0.25;
      const rt = this.pmrem.fromScene(this.envScene, 0.02, 0.1, 1000);
      if (this.envRT) this.envRT.dispose();
      this.envRT = rt; this.scene.environment = rt.texture;
    }
    this.scene.environmentIntensity = this.state.envIntensity;
  }
}
