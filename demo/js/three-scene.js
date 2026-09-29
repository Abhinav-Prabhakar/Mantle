// ============================================================
// Mantle demo — the 3D Twin. Procedural block-diagram well:
// strata slab w/ quarter cutaway, beam pumping unit with
// four-bar kinematics, wellbore, heated zone, particles, lenses.
// ============================================================
import * as THREE from 'three';
import { state as wellState, sandfaceT, heatedRadius, viscosity, clamp, lerp } from './sim.js';
const easeIO=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;

// ---------- depth mapping (piecewise, per §8.1) ----------
const DP=[[0,0],[30,-3],[1050,-26],[1200,-40]];
export function depthToY(d){for(let i=1;i<DP.length;i++){if(d<=DP[i][0]){const[a,A]=DP[i-1],[b,B]=DP[i];return A+(d-a)/(b-a)*(B-A)}}return DP.at(-1)[1]}
export function yToDepth(y){for(let i=1;i<DP.length;i++){if(y>=DP[i][1]){const[a,A]=DP[i-1],[b,B]=DP[i];return a+(y-A)/(B-A)*(b-a)}}return 1200}

// ---------- thermal ramp (inferno-ish) ----------
const RAMP=[[0,'#14041f'],[0.25,'#4b1d5e'],[0.5,'#b3362c'],[0.7,'#e8763a'],[0.88,'#f0b429'],[1,'#ffe9a8']];
export function thermal(t){t=clamp(t,0,1);for(let i=1;i<RAMP.length;i++)if(t<=RAMP[i][0]){const[a,ca]=RAMP[i-1],[b,cb]=RAMP[i];return new THREE.Color(ca).lerp(new THREE.Color(cb),(t-a)/(b-a))}return new THREE.Color(RAMP.at(-1)[1])}

export function createTwin(canvas){
  const renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true});
  renderer.setPixelRatio(Math.min(devicePixelRatio,2));
  renderer.shadowMap.enabled=true; renderer.shadowMap.type=THREE.PCFSoftShadowMap;
  const scene=new THREE.Scene();
  const camera=new THREE.PerspectiveCamera(38,1,0.1,4000);
  const clocks={t0:performance.now()};

  // ---------- lighting & sky ----------
  const hemi=new THREE.HemisphereLight(0xcfd8ff,0x8a6a45,0.85); scene.add(hemi);
  const sun=new THREE.DirectionalLight(0xffd9a8,2.1); sun.position.set(-38,26,34); sun.castShadow=true;
  sun.shadow.mapSize.set(2048,2048); sun.shadow.camera.left=-30;sun.shadow.camera.right=30;sun.shadow.camera.top=25;sun.shadow.camera.bottom=-20;sun.shadow.camera.far=160; sun.shadow.bias=-0.0004;
  scene.add(sun);
  const fill=new THREE.DirectionalLight(0x8090c0,0.35); fill.position.set(30,20,-20); scene.add(fill);
  scene.fog=new THREE.Fog(0x1a2030,90,380);

  // big backdrop sphere (gradient sky)
  const skyGeo=new THREE.SphereGeometry(1600,24,16);
  const skyMat=new THREE.ShaderMaterial({side:THREE.BackSide,depthWrite:false,fog:false,
    uniforms:{top:{value:new THREE.Color('#232c4e')},mid:{value:new THREE.Color('#4a4058')},bot:{value:new THREE.Color('#c9805a')},glow:{value:new THREE.Color('#e8a35c')}},
    vertexShader:`varying vec3 vP;void main(){vP=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}`,
    fragmentShader:`varying vec3 vP;uniform vec3 top,mid,bot,glow;void main(){float h=normalize(vP).y;vec3 c=h>0.?mix(mid,top,pow(h,.7)):mix(mid,bot,pow(-h,.5));c+=glow*pow(max(0.,1.-abs(h+.02)*5.),2.)*.55;gl_FragColor=vec4(c,1.0);}`});
  const sky=new THREE.Mesh(skyGeo,skyMat); scene.add(sky);
  const stars=(()=>{const g=new THREE.BufferGeometry();const p=[];for(let i=0;i<400;i++){const v=new THREE.Vector3().randomDirection().multiplyScalar(300);v.y=Math.abs(v.y)*0.8+20;p.push(v.x,v.y,v.z)}g.setAttribute('position',new THREE.Float32BufferAttribute(p,3));const m=new THREE.PointsMaterial({color:0xffffff,size:1.1,sizeAttenuation:false,transparent:true,opacity:0,fog:false});const s=new THREE.Points(g,m);scene.add(s);return s})();

  // ---------- materials registry ----------
  const MATS={};
  const M=(n,o)=>MATS[n]=new THREE.MeshStandardMaterial(o);
  M('sand',{color:'#c9a46a',roughness:.96}); M('pad',{color:'#a89878',roughness:.95});
  M('concrete',{color:'#9a9a94',roughness:.9}); M('gravel',{color:'#8d8577',roughness:1});
  M('paintY',{color:'#d9a012',roughness:.55,metalness:.25}); M('paintG',{color:'#4a4e55',roughness:.6,metalness:.35});
  M('steel',{color:'#7d8288',roughness:.45,metalness:.7}); M('chrome',{color:'#cfd4d9',roughness:.18,metalness:.95});
  M('rope',{color:'#2e2a26',roughness:.9}); M('belt',{color:'#22201d',roughness:.85});
  M('alu',{color:'#b8bcc0',roughness:.35,metalness:.8}); M('blanket',{color:'#8f8474',roughness:.9});
  M('tubular',{color:'#6e747a',roughness:.4,metalness:.75}); M('vit',{color:'#3f7d8c',roughness:.35,metalness:.6});
  M('rod',{color:'#9aa0a6',roughness:.3,metalness:.85}); M('guide',{color:'#ddd8cc',roughness:.7});
  M('oil',{color:'#1d0f04',roughness:.25,metalness:.1}); M('water',{color:'#2c5f9e',roughness:.3});
  M('cement',{color:'#b5b0a4',roughness:.95}); M('hazard',{color:'#e8c018',roughness:.6});
  M('valveRed',{color:'#b3362c',roughness:.5,metalness:.3}); M('brass',{color:'#a8842c',roughness:.4,metalness:.7});
  M('glasshmi',{color:'#0c2030',roughness:.1,metalness:.4,emissive:'#1a5a78',emissiveIntensity:.5});
  M('led',{color:'#33ff77',emissive:'#33ff77',emissiveIntensity:1.4});
  const strataColors=['#dcc08c','#b5977a','#a0573c','#7e8188','#5f5648','#c99f6e','#2e2a2a'];
  const strataRough=[1,.95,.9,.85,.9,.9,1];
  for(let i=0;i<7;i++) M('strat'+i,{color:strataColors[i],roughness:strataRough[i]});
  // subtle diagonal hatch on the caprock (Bilara) — reads like drafting fill
  const hatchTex=(()=>{const c=document.createElement('canvas');c.width=c.height=64;const g=c.getContext('2d');
    g.strokeStyle='rgba(255,255,255,.10)';g.lineWidth=2;
    for(let i=-64;i<96;i+=9){g.beginPath();g.moveTo(i,0);g.lineTo(i+64,64);g.stroke()}
    const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.repeat.set(8,2);return t})();
  MATS.strat3.map=hatchTex; MATS.strat3.needsUpdate=true;
  // radial blob shadow texture for grounding
  const blobTex=(()=>{const c=document.createElement('canvas');c.width=c.height=64;const g=c.getContext('2d');
    const r=g.createRadialGradient(32,32,4,32,32,31);r.addColorStop(0,'rgba(30,20,10,.5)');r.addColorStop(1,'rgba(30,20,10,0)');
    g.fillStyle=r;g.fillRect(0,0,64,64);return new THREE.CanvasTexture(c)})();
  const blobMat=new THREE.MeshBasicMaterial({map:blobTex,transparent:true,depthWrite:false});
  function blob(x,z,rx=3,rz=3){const m=new THREE.Mesh(new THREE.PlaneGeometry(rx*2,rz*2),blobMat);m.rotation.x=-Math.PI/2;m.position.set(x,.025,z);return m}

  const world=new THREE.Group(); scene.add(world);
  const pickables=[]; // {mesh, name}
  const P=(mesh,part)=>{mesh.userData.part=part;pickables.push(mesh);return mesh};

  // ---------- strata slab w/ quarter cutaway ----------
  // notch: x∈[0,13], z∈[0,20] removed; well axis at (0,0) inside corner
  const STRAT_D=[0,40,250,700,1050,1100,1150,1200];
  const strata=new THREE.Group(); world.add(strata);
  const NX=13, NZ=20; // notch extent
  const stratMeshes=[];
  const edgeMat=new THREE.LineBasicMaterial({color:'#3a3428',transparent:true,opacity:.5});
  for(let s=0;s<7;s++){
    const yT=depthToY(STRAT_D[s]), yB=depthToY(STRAT_D[s+1]), h=yT-yB, cy=(yT+yB)/2;
    const mat=MATS['strat'+s];
    // three boxes covering slab minus notch: west (x<0 all z), east-south (x∈[0,30],z∈[-20,0]), east-north beyond notch? notch covers z 0..20 x 0..13 → east-north strip x∈[13,30],z∈[0,20]
    const b1=new THREE.Mesh(new THREE.BoxGeometry(30,h,40),mat); b1.position.set(-15,cy,0);
    const b2=new THREE.Mesh(new THREE.BoxGeometry(30,h,20),mat); b2.position.set(15,cy,-10);
    const b3=new THREE.Mesh(new THREE.BoxGeometry(17,h,20),mat); b3.position.set(13+8.5,cy,10);
    const g=new THREE.Group(); g.add(b1,b2,b3); g.userData.stratum=s;
    b1.castShadow=b2.castShadow=b3.castShadow=true;
    [b1,b2,b3].forEach(b=>{b.receiveShadow=true;stratMeshes.push(b);P(b,'stratum-'+s);
      const e=new THREE.LineSegments(new THREE.EdgesGeometry(b.geometry,40),edgeMat);e.position.copy(b.position);g.add(e)});
    strata.add(g);
  }
  // depth-break ribbons: thin seam + small zigzag symbol on the cut faces
  [[30,depthToY(30)],[1050,depthToY(1050)]].forEach(([d,y])=>{
    const seam=new THREE.Mesh(new THREE.BoxGeometry(60,.09,.05),new THREE.MeshBasicMaterial({color:'#241f18'}));
    seam.position.set(0,y,20.01);strata.add(seam);
    const seam2=new THREE.Mesh(new THREE.BoxGeometry(.05,.09,40),new THREE.MeshBasicMaterial({color:'#241f18'}));
    seam2.position.set(30.01,y,0);strata.add(seam2);
    // small zigzag glyph near the front-left of the seam (break symbol)
    const zzg=new THREE.Group();
    for(let i=0;i<7;i++){const s1=new THREE.Mesh(new THREE.BoxGeometry(.55,.07,.06),new THREE.MeshBasicMaterial({color:'#3a3428'}));
      s1.position.set(-28+i*.42,y+(i%2?.12:-.12),20.03);s1.rotation.z=(i%2?-.65:.65);zzg.add(s1)}
    strata.add(zzg);
  });
  // depth ticks on front cut edge
  for(let d=100;d<=1200;d+=100){
    const y=depthToY(d); const tick=new THREE.Mesh(new THREE.BoxGeometry(.8,.08,.06),MATS.paintG);
    tick.position.set(-.6,y,.03); strata.add(tick);
  }
  // strata name labels on the two inner cut faces — ink tags that survive the drain
  function faceLabel(text,x,y,z,face){ // face: 'z' = inner z=0 wall, 'x' = inner x=0 wall
    const c=document.createElement('canvas');c.width=512;c.height=56;const g=c.getContext('2d');
    g.font='600 30px "IBM Plex Sans Condensed",system-ui,sans-serif';g.fillStyle='#2a2620';g.textBaseline='middle';
    g.fillText(text.toUpperCase(),8,28);
    const tex=new THREE.CanvasTexture(c);tex.anisotropy=4;
    const m=new THREE.Mesh(new THREE.PlaneGeometry(5.5,.6),new THREE.MeshBasicMaterial({map:tex,transparent:true,opacity:.92,depthWrite:false}));
    m.position.set(x,y,z);if(face==='x')m.rotation.y=Math.PI/2;strata.add(m);return m;
  }
  const STRAT_NAMES=['AEOLIAN SAND','TERTIARY SEDS','NAGAUR SS','BILARA — CAPROCK','UPPER CARB','JODHPUR — PAY','BASEMENT'];
  for(let s=0;s<7;s++){const yM=depthToY((STRAT_D[s]+STRAT_D[s+1])/2);
    if(s!==0)faceLabel(STRAT_NAMES[s],6.4,yM+.15,.045,'z');
    if(s>=2&&s!==4)faceLabel(STRAT_NAMES[s],.045,yM+.15,10.5,'x');
  }

  // ---------- surface ----------
  const sand=new THREE.Mesh(new THREE.BoxGeometry(60,1.2,40),MATS.sand); sand.position.y=-0.6; sand.receiveShadow=true; world.add(sand); P(sand,'terrain');
  // ripples: thin darker strips
  for(let i=0;i<14;i++){const r=new THREE.Mesh(new THREE.BoxGeometry(8+Math.sin(i)*4,.06,.5),MATS.pad);r.position.set(-26+i*4.2,.03,-16+((i*37)%30));r.rotation.y=Math.sin(i*2)*.4;world.add(r)}
  const pad=new THREE.Mesh(new THREE.BoxGeometry(22,.35,17),MATS.gravel); pad.position.set(-5,.18,-1); pad.receiveShadow=true; world.add(pad);
  const plinth=new THREE.Mesh(new THREE.BoxGeometry(13,.9,4.4),MATS.concrete); plinth.position.set(-7,.7,0); plinth.castShadow=plinth.receiveShadow=true; world.add(plinth);
  const stain=new THREE.Mesh(new THREE.CylinderGeometry(2.2,2.2,.06,24),MATS.oil); stain.position.set(0,.4,0); world.add(stain);
  // pad curb ring + gravel collar at wellhead + tire tracks + blob shadows
  [[-5,-1,22.6,'x',-8.5],[-5,-1,22.6,'x',8.5],[-5,-1,17.6,'z',-16.2],[-5,-1,17.6,'z',6.2]].forEach(([cx,cz,len,ax,off])=>{
    const curb=new THREE.Mesh(new THREE.BoxGeometry(ax==='x'?len:.14,.16,ax==='x'?.14:len),MATS.concrete);
    curb.position.set(ax==='x'?cx:cx+off,.42,ax==='x'?cz+off:cz);world.add(curb)});
  const collar=new THREE.Mesh(new THREE.CylinderGeometry(2.9,3.1,.14,24),MATS.gravel);collar.position.set(0,.42,0);world.add(collar);
  for(let i=0;i<2;i++){const tr=new THREE.Mesh(new THREE.BoxGeometry(26,.04,.9),new THREE.MeshStandardMaterial({color:'#8a7a5c',roughness:1}));
    tr.position.set(-8,.42,6+i*1.6);tr.rotation.y=.12;world.add(tr)}
  world.add(blob(-7,.4,7,3));world.add(blob(0,.4,1.6,1.6));world.add(blob(8,-7,1.2,1.2));world.add(blob(-12.5,2.4,1,1));
  // oil drums + safety cones by the flowline
  for(let i=0;i<3;i++){const d=new THREE.Mesh(new THREE.CylinderGeometry(.34,.34,.9,10),i%2?MATS.valveRed:MATS.paintG);d.position.set(-20+i*.9,.85,5.6);d.castShadow=true;world.add(d)}
  for(let i=0;i<2;i++){const cone=new THREE.Mesh(new THREE.ConeGeometry(.24,.7,8),MATS.hazard);cone.position.set(-2.4+i*1.1,.75,-2.6);world.add(cone)}
  // scrub bushes
  for(let i=0;i<5;i++){const b=new THREE.Group();for(let k=0;k<4;k++){const br=new THREE.Mesh(new THREE.ConeGeometry(.5,1.6,5),new THREE.MeshStandardMaterial({color:'#6a7040',roughness:1}));br.position.set(Math.sin(k*2)*.4,.7,Math.cos(k*2)*.4);b.add(br)}b.position.set([-24,18,-14,24,-27][i],0,[14,-18,17,-16,6][i]);world.add(b)}
  // fence (two sides)
  const fenceMat=new THREE.MeshStandardMaterial({color:'#666',roughness:.8,transparent:true,opacity:.5,side:THREE.DoubleSide});
  for(let i=0;i<10;i++){const post=new THREE.Mesh(new THREE.CylinderGeometry(.05,.05,1.6),MATS.steel);post.position.set(-27+i*6,.8,-14);world.add(post)}
  const fm=new THREE.Mesh(new THREE.PlaneGeometry(56,1.4),fenceMat);fm.position.set(0,.9,-14);world.add(fm);
  // RTU pole
  const rtu=new THREE.Group();
  const pole=new THREE.Mesh(new THREE.CylinderGeometry(.07,.09,4),MATS.paintG);pole.position.y=2;rtu.add(pole);
  const cab=new THREE.Mesh(new THREE.BoxGeometry(.7,.9,.3),MATS.alu);cab.position.y=2.4;rtu.add(cab);
  const panel=new THREE.Mesh(new THREE.BoxGeometry(1,.05,.7),new THREE.MeshStandardMaterial({color:'#1c2f4a',roughness:.2,metalness:.6}));panel.position.set(0,3.6,0);panel.rotation.x=-.5;rtu.add(panel);
  const led=new THREE.Mesh(new THREE.SphereGeometry(.06),MATS.led);led.position.set(.4,2.75,.16);rtu.add(led);
  rtu.position.set(8,0,-7);world.add(rtu);P(cab,'rtu');
  // power cable RTU → VFD (catenary)
  {const curve=new THREE.QuadraticBezierCurve3(new THREE.Vector3(8,2.2,-7),new THREE.Vector3(-2,1.2,-2.4),new THREE.Vector3(-12.5,2.4,2.2));
   const cable=new THREE.Mesh(new THREE.TubeGeometry(curve,24,.035,5),MATS.rope);world.add(cable)}
  // steam line + flowline
  const steamLine=new THREE.Group();
  const sl=new THREE.Mesh(new THREE.CylinderGeometry(.22,.26,26),MATS.alu);sl.rotation.z=Math.PI/2;sl.position.set(17,.8,2);steamLine.add(sl);
  for(let i=0;i<7;i++){const band=new THREE.Mesh(new THREE.CylinderGeometry(.24,.24,.12),MATS.paintG);band.rotation.z=Math.PI/2;band.position.set(4+i*3.6,.8,2);steamLine.add(band)}
  const valveW=new THREE.Mesh(new THREE.CylinderGeometry(.5,.5,.08),MATS.valveRed);valveW.position.set(2.4,1.5,2);valveW.rotation.x=Math.PI/2;steamLine.add(P(valveW,'steam-valve'));
  // pipe supports + end flange
  for(let i=0;i<4;i++){const sup=new THREE.Mesh(new THREE.BoxGeometry(.18,.8,.5),MATS.concrete);sup.position.set(6+i*6.4,.4,2);steamLine.add(sup)}
  const flng=new THREE.Mesh(new THREE.CylinderGeometry(.34,.34,.1,12),MATS.steel);flng.rotation.z=Math.PI/2;flng.position.set(29.5,.8,2);steamLine.add(flng);
  world.add(steamLine);P(sl,'steamline');
  const flowline=new THREE.Group();
  const flow=new THREE.Mesh(new THREE.CylinderGeometry(.14,.14,22),MATS.alu);flow.rotation.z=Math.PI/2;flow.position.set(-14,.7,4);flowline.add(P(flow,'flowline'));
  const flValve=new THREE.Mesh(new THREE.CylinderGeometry(.24,.24,.5),MATS.paintG);flValve.position.set(-6,.8,4);flowline.add(flValve);
  const flWheel=new THREE.Mesh(new THREE.TorusGeometry(.22,.05,6,14),MATS.valveRed);flWheel.position.set(-6,1.25,4);flWheel.rotation.x=Math.PI/2;flowline.add(flWheel);
  const flDial=new THREE.Mesh(new THREE.CylinderGeometry(.14,.14,.06,10),MATS.brass);flDial.position.set(-3.4,1.05,4);flowline.add(flDial);
  for(let i=0;i<3;i++){const sup=new THREE.Mesh(new THREE.BoxGeometry(.14,.7,.3),MATS.concrete);sup.position.set(-19+i*7,.35,4);flowline.add(sup)}
  world.add(flowline);

  // ---------- wellhead ----------
  const wh=new THREE.Group(); wh.position.set(0,.35,0);
  const casingHead=new THREE.Mesh(new THREE.CylinderGeometry(.42,.48,.9),MATS.tubular);casingHead.position.y=.45;wh.add(P(casingHead,'wellhead'));
  const flange1=new THREE.Mesh(new THREE.CylinderGeometry(.58,.58,.14,14),MATS.steel);flange1.position.y=.95;wh.add(flange1);
  const tubingHead=new THREE.Mesh(new THREE.CylinderGeometry(.36,.4,.7),MATS.tubular);tubingHead.position.y=1.35;wh.add(tubingHead);
  const flange2=new THREE.Mesh(new THREE.CylinderGeometry(.5,.5,.12,14),MATS.steel);flange2.position.y=1.75;wh.add(flange2);
  const master=new THREE.Mesh(new THREE.CylinderGeometry(.2,.2,.5),MATS.paintG);master.position.y=2.05;wh.add(master);
  const stuffing=new THREE.Mesh(new THREE.CylinderGeometry(.16,.16,.5),MATS.steel);stuffing.position.y=2.45;wh.add(P(stuffing,'stuffing-box'));
  const wing=new THREE.Mesh(new THREE.CylinderGeometry(.09,.09,1.1),MATS.tubular);wing.rotation.z=Math.PI/2;wing.position.set(.6,1.35,0);wh.add(wing);
  const wingValve=new THREE.Mesh(new THREE.TorusGeometry(.18,.05,6,12),MATS.valveRed);wingValve.position.set(1.1,1.35,0);wingValve.rotation.y=Math.PI/2;wh.add(wingValve);
  const gauge=new THREE.Mesh(new THREE.CylinderGeometry(.16,.16,.05),MATS.brass);gauge.rotation.x=Math.PI/2;gauge.position.set(-.45,1.7,.3);wh.add(gauge);
  const gaugeFace=new THREE.Mesh(new THREE.CircleGeometry(.12,12),new THREE.MeshBasicMaterial({color:'#f0ead0'}));gaugeFace.position.set(-.45,1.7,.34);wh.add(gaugeFace);
  const insul=new THREE.Mesh(new THREE.CylinderGeometry(.46,.5,.8),MATS.blanket);insul.position.y=.95;wh.add(insul);
  world.add(wh);

  // ---------- pumping unit (four-bar rig) ----------
  const pu=new THREE.Group(); world.add(pu); pu.scale.setScalar(1.22); // exaggerated for readability per §8.1
  const S={x:-4,y:7.6};          // saddle pivot
  const Lf=4.2, Lr=3.3;          // beam front/rear lengths
  const CR={x:-7.7,y:2.6};       // crank shaft centre
  const CRANK_R=1.25;
  const LPIT=5.0; // pitman length — Grashof-checked for full crank rotation
  // base skid
  const skid=new THREE.Mesh(new THREE.BoxGeometry(11,.5,3.4),MATS.paintG);skid.position.set(-7,1.35,0);pu.add(skid);
  const skidRailL=new THREE.Mesh(new THREE.BoxGeometry(11.4,.3,.5),MATS.steel);skidRailL.position.set(-7,1.12,-1.5);pu.add(skidRailL);
  const skidRailR=skidRailL.clone();skidRailR.position.z=1.5;pu.add(skidRailR);
  // samson post A-frame
  const samson=new THREE.Group();
  const legGeo=new THREE.CylinderGeometry(.14,.18,7.8);
  [[0,-1.1],[0,1.1]].forEach(([_,z])=>{const leg=new THREE.Mesh(legGeo,MATS.paintY);leg.position.set(S.x,S.y/2+0.9,z);leg.rotation.x=(z>0?-.11:.11);samson.add(leg)});
  const leg3=new THREE.Mesh(legGeo,MATS.paintY);leg3.position.set(S.x-2.6,S.y/2+0.4,0);leg3.rotation.z=.62;samson.add(leg3);
  const cross=new THREE.Mesh(new THREE.BoxGeometry(.1,5.6,2.1),MATS.paintG);cross.position.set(S.x-1.2,4,0);cross.rotation.z=.5;samson.add(cross);
  // cross-braces between legs (X lattice)
  [[-1],[1]].forEach(([sgn])=>{
    const br1=new THREE.Mesh(new THREE.BoxGeometry(.07,3.4,.07),MATS.paintG);br1.position.set(S.x-1.3,3.4,sgn*.55);br1.rotation.z=.7;samson.add(br1);
    const br2=new THREE.Mesh(new THREE.BoxGeometry(.07,3.4,.07),MATS.paintG);br2.position.set(S.x-1.3,3.4,sgn*.55);br2.rotation.z=-.7;samson.add(br2);});
  // ladder with rungs
  const ladder=new THREE.Mesh(new THREE.BoxGeometry(.5,6,.08),MATS.steel);ladder.position.set(S.x+0.55,3.8,1.25);samson.add(ladder);
  for(let i=0;i<8;i++){const rung=new THREE.Mesh(new THREE.BoxGeometry(.46,.05,.12),MATS.paintG);rung.position.set(S.x+0.55,1.2+i*.7,1.29);samson.add(rung)}
  pu.add(samson);
  // gearbox + motor + belt
  const gearbox=new THREE.Mesh(new THREE.BoxGeometry(1.8,1.9,2),MATS.paintG);gearbox.position.set(CR.x,1.9,0);pu.add(P(gearbox,'gearbox'));
  const sight=new THREE.Mesh(new THREE.CylinderGeometry(.09,.09,.05),MATS.glasshmi);sight.rotation.x=Math.PI/2;sight.position.set(CR.x+.3,1.7,1.02);pu.add(sight);
  const gbShaft=new THREE.Mesh(new THREE.CylinderGeometry(.22,.22,2.6,12),MATS.steel);gbShaft.rotation.x=Math.PI/2;gbShaft.position.set(CR.x,2.6,0);pu.add(gbShaft);
  const gbBolts=new THREE.Group();for(let i=0;i<6;i++){const bt=new THREE.Mesh(new THREE.CylinderGeometry(.06,.06,.08),MATS.brass);bt.rotation.x=Math.PI/2;bt.position.set(CR.x+Math.cos(i*1.05)*.75,1.9+Math.sin(i*1.05)*.75,1.02);gbBolts.add(bt)}pu.add(gbBolts);
  const brake=new THREE.Mesh(new THREE.BoxGeometry(.08,1.1,.08),MATS.valveRed);brake.position.set(CR.x-.9,2.6,.9);brake.rotation.z=.5;pu.add(brake);
  const motor=new THREE.Mesh(new THREE.CylinderGeometry(.55,.55,1.3),MATS.paintG);motor.rotation.z=Math.PI/2;motor.position.set(-11.4,2.1,0);pu.add(P(motor,'motor'));
  for(let i=0;i<4;i++){const fin=new THREE.Mesh(new THREE.BoxGeometry(1.3,.07,.1),MATS.steel);fin.position.set(-11.4,2.1,.6);fin.rotation.x=i*Math.PI/4;pu.add(fin)}
  const pulley=new THREE.Mesh(new THREE.CylinderGeometry(.3,.3,.2),MATS.steel);pulley.rotation.x=Math.PI/2;pulley.position.set(-10.6,2.1,0);pu.add(pulley);
  const beltG=new THREE.Mesh(new THREE.BoxGeometry(2.6,1.5,1.6),new THREE.MeshStandardMaterial({color:'#3a3d42',roughness:.7,transparent:true,opacity:.85}));beltG.position.set(-9.6,2.3,0);pu.add(beltG);
  // VFD cabinet
  const vfd=new THREE.Mesh(new THREE.BoxGeometry(1,1.7,.6),MATS.alu);vfd.position.set(-12.5,1.6,2.2);pu.add(P(vfd,'vfd'));
  const hmi=new THREE.Mesh(new THREE.PlaneGeometry(.5,.35),MATS.glasshmi);hmi.position.set(-12.5,2,2.51);pu.add(hmi);
  // cranks + counterweights (two sides)
  const crankGroupL=new THREE.Group(), crankGroupR=new THREE.Group();
  crankGroupL.position.set(CR.x,CR.y,-1.0); crankGroupR.position.set(CR.x,CR.y,1.0);
  const mkCrank=(g)=>{const arm=new THREE.Mesh(new THREE.BoxGeometry(.5,CRANK_R*2,.18),MATS.paintG);arm.position.y=CRANK_R/2-0.05;g.add(arm);
    const cw=new THREE.Mesh(new THREE.CylinderGeometry(.95,.95,.26,20,1,false,Math.PI,Math.PI),MATS.hazard);cw.rotation.z=Math.PI/2;cw.rotation.y=Math.PI/2;cw.position.y=CRANK_R-0.1;g.add(cw);
    const cwf=new THREE.Mesh(new THREE.CylinderGeometry(.97,.97,.05,20,1,false,Math.PI,Math.PI),MATS.paintG);cwf.rotation.z=Math.PI/2;cwf.rotation.y=Math.PI/2;cwf.position.y=CRANK_R-0.1;cwf.position.z=.15;g.add(cwf);
    for(let i=0;i<4;i++){const bl=new THREE.Mesh(new THREE.CylinderGeometry(.05,.05,.3),MATS.brass);bl.rotation.x=Math.PI/2;bl.position.set(Math.cos(Math.PI+i*.7)*.6,CRANK_R-.1+Math.sin(Math.PI+i*.7)*.6,0);g.add(bl)}
    const pin=new THREE.Mesh(new THREE.CylinderGeometry(.09,.09,.5),MATS.chrome);pin.rotation.x=Math.PI/2;pin.position.y=CRANK_R;g.add(pin);return g};
  mkCrank(crankGroupL); mkCrank(crankGroupR);
  pu.add(crankGroupL,crankGroupR);
  // walking beam + horsehead + equalizer
  const beam=new THREE.Group(); beam.position.set(S.x,S.y,0); pu.add(beam);
  const beamMesh=new THREE.Mesh(new THREE.BoxGeometry(Lf+Lr+.6,.62,.5),MATS.paintY);beamMesh.position.x=(Lf-Lr)/2+0.05;beam.add(P(beamMesh,'beam'));
  const web=new THREE.Mesh(new THREE.BoxGeometry(Lf+Lr,.2,.56),MATS.paintG);web.position.x=(Lf-Lr)/2;web.position.y=-.34;beam.add(web);
  const saddle=new THREE.Mesh(new THREE.CylinderGeometry(.2,.2,.9),MATS.steel);saddle.rotation.x=Math.PI/2;beam.add(saddle);
  const head=new THREE.Group(); head.position.x=Lf; beam.add(head);
  const arc=new THREE.Mesh(new THREE.CylinderGeometry(1.05,1.05,.5,20,1,false,-Math.PI/2-.6,1.9),MATS.paintY);arc.rotation.x=Math.PI/2;head.add(P(arc,'horsehead'));
  const nose=new THREE.Mesh(new THREE.BoxGeometry(.24,1.1,.5),MATS.paintY);nose.position.set(.75,-.35,0);head.add(nose);
  const eq=new THREE.Mesh(new THREE.BoxGeometry(.5,.5,.5),MATS.paintG);eq.position.x=-Lr;beam.add(eq);
  // pitmans
  const pitGeo=new THREE.CylinderGeometry(.07,.07,1);pitGeo.translate(0,.5,0); // pivot at bottom
  const pitL=new THREE.Mesh(pitGeo,MATS.steel), pitR=new THREE.Mesh(pitGeo.clone(),MATS.steel);
  pitL.position.z=-1.0;pitR.position.z=1.0;pu.add(pitL,pitR);
  // bridle + carrier bar + polished rod
  const carrier=new THREE.Mesh(new THREE.BoxGeometry(.5,.28,.4),MATS.paintG);world.add(P(carrier,'carrier-bar'));
  const prclamp=new THREE.Mesh(new THREE.BoxGeometry(.3,.22,.3),MATS.steel);world.add(prclamp);
  const polishedRod=new THREE.Mesh(new THREE.CylinderGeometry(.07,.07,9),MATS.chrome);world.add(P(polishedRod,'polished-rod'));
  const bridleMat=new THREE.LineBasicMaterial({color:'#2e2a26'});
  const bridleGeo=new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(),new THREE.Vector3(),new THREE.Vector3(),new THREE.Vector3(),new THREE.Vector3()]);
  const bridle=new THREE.Line(bridleGeo,bridleMat); world.add(bridle);

  // ---------- wellbore (quarter section) ----------
  const wb=new THREE.Group(); world.add(wb);
  const pumpDepth=1080, pumpY=depthToY(pumpDepth), resT=depthToY(1100), resB=depthToY(1150);
  // quarter-section: remove the +X+Z quadrant (theta 0..90°) so the well shows on the cut faces
  const QS=Math.PI/2, QL=Math.PI*1.5;
  const casing=new THREE.Mesh(new THREE.CylinderGeometry(.26,.26,-depthToY(1140),14,1,true,QS,QL),MATS.tubular);
  casing.position.y=depthToY(1140)/2;wb.add(P(casing,'casing'));
  const cement=new THREE.Mesh(new THREE.CylinderGeometry(.34,.34,-depthToY(1140),14,1,true,QS,QL),MATS.cement);cement.position.y=depthToY(1140)/2;wb.add(cement);
  const tubing=new THREE.Mesh(new THREE.CylinderGeometry(.13,.13,-pumpY,10,1,true,QS,QL),MATS.vit);tubing.position.y=pumpY/2;wb.add(P(tubing,'tubing'));
  // bright bore core line so the well reads at block scale
  const boreGlow=new THREE.Mesh(new THREE.CylinderGeometry(.055,.055,-depthToY(1140),8),new THREE.MeshBasicMaterial({color:'#dfe8f4'}));
  boreGlow.position.y=depthToY(1140)/2;wb.add(boreGlow);
  // rod string: 24 segments
  const rodSegs=[];
  const NSEG=24, segLen=-pumpY/NSEG;
  for(let i=0;i<NSEG;i++){
    const seg=new THREE.Mesh(new THREE.CylinderGeometry(.045,.045,segLen*.96),MATS.rod.clone());
    seg.position.y=-(i+.5)*segLen; wb.add(seg); rodSegs.push(seg);
    if(i%4===1){const gd=new THREE.Mesh(new THREE.CylinderGeometry(.09,.09,.18),MATS.guide);gd.position.y=-(i+.5)*segLen;wb.add(gd)}
  }
  // pump assembly
  const pump=new THREE.Group(); pump.position.y=pumpY; wb.add(pump);
  const barrel=new THREE.Mesh(new THREE.CylinderGeometry(.14,.14,1.1,10,1,true,QS,QL),new THREE.MeshStandardMaterial({color:'#8a929a',roughness:.3,metalness:.7,transparent:true,opacity:.85}));pump.add(P(barrel,'pump'));
  const plunger=new THREE.Mesh(new THREE.CylinderGeometry(.09,.09,.55),MATS.chrome);pump.add(plunger);
  const svBall=new THREE.Mesh(new THREE.SphereGeometry(.05),MATS.steel);svBall.position.y=-.5;pump.add(svBall);
  const fluidInBarrel=new THREE.Mesh(new THREE.CylinderGeometry(.1,.1,.5),MATS.oil);fluidInBarrel.position.y=-.25;pump.add(fluidInBarrel);
  // perforations
  const perfGroup=new THREE.Group();
  for(let i=0;i<10;i++){const pf=new THREE.Mesh(new THREE.ConeGeometry(.06,.3,6),MATS.oil);
    const yy=depthToY(1105+i*4.5); pf.position.set(.3,yy,(i%2?.12:-.05));pf.rotation.z=-Math.PI/2;perfGroup.add(pf)}
  wb.add(perfGroup);
  // glowing perf ports — read through the quarter-section cut
  const perfDots=[];
  for(let i=0;i<7;i++){const d=new THREE.Mesh(new THREE.SphereGeometry(.06,6,6),new THREE.MeshBasicMaterial({color:'#ff6a35'}));
    d.position.set(.12,depthToY(1106+i*6),.12);wb.add(d);perfDots.push(d)}
  // annulus fluid level surface
  const fluidLevelM=new THREE.Mesh(new THREE.CylinderGeometry(.24,.24,.03,12),new THREE.MeshStandardMaterial({color:'#2c5f9e',emissive:'#2c5f9e',emissiveIntensity:.4,transparent:true,opacity:.9}));
  wb.add(fluidLevelM);
  // tubing fluid column (temperature gradient via vertex colors)
  const tubFluidGeo=new THREE.CylinderGeometry(.09,.09,-pumpY,8,24,true);
  {const pos=tubFluidGeo.attributes.position;const col=[];for(let i=0;i<pos.count;i++){const t=1-(pos.getY(i)/pumpY+0.5);const c=thermal(t*.8+.1);col.push(c.r,c.g,c.b)}tubFluidGeo.setAttribute('color',new THREE.Float32BufferAttribute(col,3))}
  const tubFluid=new THREE.Mesh(tubFluidGeo,new THREE.MeshBasicMaterial({vertexColors:true,transparent:true,opacity:.85,side:THREE.DoubleSide}));
  tubFluid.position.y=pumpY/2; tubFluid.visible=false; wb.add(tubFluid);

  // ---------- heated zone (hero) ----------
  const heatGroup=new THREE.Group(); heatGroup.position.set(0,depthToY(1127),0); world.add(heatGroup);
  const heatShells=[];
  for(let i=0;i<4;i++){
    const sh=new THREE.Mesh(new THREE.SphereGeometry(1,24,16),new THREE.MeshBasicMaterial({color:'#e8763a',transparent:true,opacity:.16-(i*.03),blending:THREE.AdditiveBlending,depthWrite:false}));
    sh.scale.set(1.4+i*.9,.9+i*.55,1.4+i*.9); heatGroup.add(sh); heatShells.push(sh);
  }
  const heatCore=new THREE.Mesh(new THREE.SphereGeometry(1.2,24,16),new THREE.MeshBasicMaterial({color:'#f0b429',transparent:true,opacity:.85,blending:THREE.AdditiveBlending,depthWrite:false}));
  heatCore.scale.y=.65; heatGroup.add(heatCore);
  // disc slices on the two cut faces
  const sliceF=new THREE.Mesh(new THREE.CircleGeometry(1,32,0,Math.PI),new THREE.MeshBasicMaterial({color:'#e8763a',transparent:true,opacity:.55,blending:THREE.AdditiveBlending,depthWrite:false,side:THREE.DoubleSide}));
  sliceF.position.set(0,depthToY(1127),.02); sliceF.scale.set(3.4,2.4,1); world.add(sliceF);
  const sliceS=sliceF.clone(); sliceS.rotation.y=Math.PI/2; sliceS.position.set(.02,depthToY(1127),0); world.add(sliceS);
  // cap-rock heat loss glow
  const capGlow=new THREE.Mesh(new THREE.PlaneGeometry(8,.5),new THREE.MeshBasicMaterial({color:'#b3362c',transparent:true,opacity:.3,blending:THREE.AdditiveBlending,depthWrite:false}));
  capGlow.position.set(0,depthToY(1100)+.3,.02);world.add(capGlow);
  // isotherm contour rings on the two cut faces — drafting-style heat contours
  const isoRings=[];
  for(let i=0;i<4;i++){
    const curve=new THREE.EllipseCurve(0,0,1.8+i*1.7,(1.8+i*1.7)*.58);
    const g=new THREE.BufferGeometry().setFromPoints(curve.getPoints(64));
    const mat=new THREE.LineBasicMaterial({color:'#e8763a',transparent:true,opacity:.75});
    const r1=new THREE.LineLoop(g,mat);r1.position.set(0,depthToY(1127),.05);world.add(r1);
    const r2=new THREE.LineLoop(g,mat.clone());r2.rotation.y=Math.PI/2;r2.position.set(.05,depthToY(1127),0);world.add(r2);
    isoRings.push(r1,r2);
  }

  // ---------- particles ----------
  function makePoints(n,size,color,op){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(new Float32Array(n*3),3));const m=new THREE.PointsMaterial({color,size,transparent:true,opacity:op,depthWrite:false,blending:THREE.AdditiveBlending});const p=new THREE.Points(g,m);p.frustumCulled=false;world.add(p);return p}
  const oilPts=makePoints(260,.16,'#e8933a',.9);
  const oilData=new Float32Array(260*4); // r,theta,z frac, speed
  for(let i=0;i<260;i++){oilData[i*4]=2.4+Math.random()*7;oilData[i*4+1]=Math.random()*Math.PI/2;oilData[i*4+2]=depthToY(1100)+Math.random()*(resB-resT);oilData[i*4+3]=.4+Math.random()}
  const steamPts=makePoints(160,.13,'#cfe8ef',.75);
  const steamData=new Float32Array(160*3);for(let i=0;i<160;i++)steamData[i*3]=Math.random();
  const dustPts=makePoints(120,.09,'#e0c28e',.3);
  const dustData=new Float32Array(120*3);for(let i=0;i<120;i++){dustData[i*3]=(Math.random()-.5)*60;dustData[i*3+1]=Math.random()*12;dustData[i*3+2]=(Math.random()-.5)*40}

  // ---------- anchors for callouts ----------
  // anchors parented to moving meshes track the actual stroke
  const anchors={};
  const AN=(name,x,y,z)=>{const o=new THREE.Object3D();o.position.set(x,y,z);world.add(o);anchors[name]=o;return o};
  const ANP=(name,parent,x,y,z)=>{const o=new THREE.Object3D();o.position.set(x,y,z);parent.add(o);anchors[name]=o;return o};
  ANP('polished_rod',polishedRod,0,4,0); ANP('crank',crankGroupL,0,0,0); ANP('motor',motor,0,.8,0); ANP('vfd',vfd,0,1.1,0);
  AN('wellhead',0,2.9,0); ANP('steam_inlet',valveW,0,.4,0); ANP('flowline',flDial,0,.5,0);
  AN('fluid_level',.3,depthToY(620),.1); AN('rod_mid',0,depthToY(600),0); AN('pump',.3,pumpY,.1);
  AN('casing_upper',.3,depthToY(260),.1);
  AN('perforations',.4,depthToY(1127),.1); AN('heated_zone',0,depthToY(1127),0); AN('caprock',-4,depthToY(1050),0);
  ANP('gearbox',gearbox,0,1.3,0); ANP('horsehead',head,.5,.9,0); ANP('beam',beamMesh,0,.5,0);

  // ---------- four-bar solver ----------
  let beamAngle=-0.2;
  function solveBeam(theta){
    const px=CR.x+CRANK_R*Math.cos(theta), py=CR.y+CRANK_R*Math.sin(theta);
    let b=beamAngle;
    for(let i=0;i<10;i++){
      const ex=S.x-Lr*Math.cos(b), ey=S.y-Lr*Math.sin(b);
      const dx=ex-px, dy=ey-py;
      const f=dx*dx+dy*dy-LPIT*LPIT;
      const df=2*dx*Lr*Math.sin(b)-2*dy*Lr*Math.cos(b);
      const nb=b-f/df; if(Math.abs(nb-b)<1e-7){b=nb;break} b=nb;
    }
    beamAngle=b; return b;
  }

  // ---------- camera control (custom orbit) ----------
  const cam={az:.62, el:.26, dist:92, tx:-2,ty:-14,tz:0, azT:.62,elT:.26,distT:92,txT:-2,tyT:-14,tzT:0,fov:38,fovT:38,auto:true};
  let drag=null;
  canvas.addEventListener('pointerdown',e=>{drag={x:e.clientX,y:e.clientY,az:cam.azT,el:cam.elT};cam.auto=false;canvas.setPointerCapture(e.pointerId)});
  canvas.addEventListener('pointermove',e=>{if(!drag)return;cam.azT=drag.az-(e.clientX-drag.x)*.006;cam.elT=clamp(drag.el+(e.clientY-drag.y)*.004,.05,1.25)});
  canvas.addEventListener('pointerup',()=>{drag=null;setTimeout(()=>cam.auto=true,6000)});
  canvas.addEventListener('wheel',e=>{e.preventDefault();cam.distT=clamp(cam.distT*(1+e.deltaY*.001),14,130);cam.auto=false;setTimeout(()=>cam.auto=true,6000)},{passive:false});
  canvas.addEventListener('dblclick',e=>{ // fly to hovered part
    const hit=raycast(e); if(!hit)return;
    const p=new THREE.Vector3(); hit.getWorldPosition?hit.getWorldPosition(p):p.copy(hit.position||new THREE.Vector3());
    if(hit.point)p.copy(hit.point);
    cam.txT=clamp(p.x,-20,10);cam.tyT=clamp(p.y,-50,4);cam.tzT=clamp(p.z,-10,10);cam.distT=clamp(cam.distT*.5,15,60);cam.auto=false;
    setTimeout(()=>cam.auto=true,7000);
  });
  const raycaster=new THREE.Raycaster(); const mouse=new THREE.Vector2();
  function raycast(e){const r=canvas.getBoundingClientRect();mouse.set(((e.clientX-r.left)/r.width)*2-1,-((e.clientY-r.top)/r.height)*2+1);raycaster.setFromCamera(mouse,camera);const hits=raycaster.intersectObjects(pickables,false);return hits[0]||null}
  canvas.addEventListener('click',e=>{const h=raycast(e);if(h&&api.onPartClick)api.onPartClick(h.object.userData.part)});
  let hoverPart=null;
  canvas.addEventListener('pointermove',e=>{if(drag)return;const h=raycast(e);const p=h?h.object.userData.part:null;
    if(p!==hoverPart){hoverPart=p;canvas.style.cursor=p?'pointer':'grab';if(api.onPartHover)api.onPartHover(p,h?h.point:null,e)}});

  // ---------- lens / mode state ----------
  let lens='physical', xray=false;
  const savedColors=new Map();
  function setLens(l){
    lens=l;
    const dim=(mat,c)=>{mat.color.set(c)};
    // reset
    for(let s=0;s<7;s++){const m=MATS['strat'+s];m.color.set(strataColors[s]);m.emissive=new THREE.Color(0)}
    [MATS.paintY,MATS.paintG,MATS.steel,MATS.alu,MATS.sand,MATS.gravel,MATS.concrete,MATS.tubular].forEach(m=>{m.emissive=new THREE.Color(0);m.emissiveIntensity=0});
    rodSegs.forEach(s=>s.material.color.set('#9aa0a6'));
    tubFluid.visible=false; heatGroup.visible=true; sliceF.visible=sliceS.visible=capGlow.visible=true;
    oilPts.visible=(l==='flow'||l==='physical'); steamPts.visible=false;
    if(l==='thermal'){
      for(let s=0;s<7;s++)MATS['strat'+s].color.set(strataColors[s]).multiplyScalar(.35);
      tubFluid.visible=true;
      steamLine.children.forEach(c=>{if(c.material.emissive){c.material.emissive=new THREE.Color('#e8763a');c.material.emissiveIntensity=.5}});
    }
    if(l==='mech'){ rodSegs.forEach((s,i)=>s.material.color.set('#5B83F0')); }
    if(l==='pressure'){ for(let s=0;s<7;s++)MATS['strat'+s].color.set(strataColors[s]).lerp(new THREE.Color('#2c5f9e'),.35); fluidLevelM.material.emissiveIntensity=1.2; }
    if(l==='risk'){ for(let s=0;s<7;s++)MATS['strat'+s].color.set(strataColors[s]).multiplyScalar(.55);
      [MATS.paintY,MATS.paintG].forEach(m=>m.color.multiplyScalar(.6)); }
    if(l==='flow'){/*oilPts handled*/}
    if(l==='physical'){MATS.paintY.color.set('#d9a012');MATS.paintG.color.set('#4a4e55')}
    if(l!=='physical'&&l!=='risk'){MATS.paintY.color.set('#d9a012');MATS.paintG.color.set('#4a4e55')}
  }
  function setXray(v){xray=v;[MATS.tubular,MATS.vit,MATS.cement].forEach(m=>{m.transparent=v;m.opacity=v?.16:1;m.depthWrite=!v});fluidInBarrel.visible=true}

  // ---------- climate / conditions ----------
  const SKIES={
    dusk:{top:'#232c4e',mid:'#4a4058',bot:'#c9805a',sun:'#ffd9a8',sunI:2.1,sunPos:[-38,26,34],stars:0,fog:['#1a2030',120,400],hemi:.85},
    noon:{top:'#3d5a80',mid:'#98b4d4',bot:'#e8d9b0',sun:'#fff4e0',sunI:2.8,sunPos:[-10,60,18],stars:0,fog:['#c9b98f',90,350],hemi:1.1},
    night:{top:'#060814',mid:'#101527',bot:'#1c2030',sun:'#7a90c0',sunI:.4,sunPos:[30,40,-20],stars:.85,fog:['#0a0e18',90,320],hemi:.4},
    storm:{top:'#4a4034',mid:'#8a7555',bot:'#b09468',sun:'#e0c090',sunI:1.2,sunPos:[-20,35,30],stars:0,fog:['#8a7555',18,120],hemi:.7},
    monsoon:{top:'#3a4450',mid:'#6a7580',bot:'#9aa098',sun:'#c8d0d8',sunI:1.4,sunPos:[0,55,10],stars:0,fog:['#7a8590',40,220],hemi:.85},
  };
  function setClimate(k){const s=SKIES[k]||SKIES.dusk;
    skyMat.uniforms.top.value.set(s.top);skyMat.uniforms.mid.value.set(s.mid);skyMat.uniforms.bot.value.set(s.bot);
    sun.color.set(s.sun);sun.intensity=s.sunI;sun.position.set(...s.sunPos);
    scene.fog.color.set(s.fog[0]);scene.fog.near=s.fog[1];scene.fog.far=s.fog[2];
    stars.material.opacity=s.stars;hemi.intensity=s.hemi;
    MATS.led.emissiveIntensity=k==='night'?3:1.4;
  }
  function setFormation(k){MATS.strat5.color.set({jodhpur:'#c99f6e',tight:'#8f7355',hiperm:'#e0b884',carb:'#7a7268',sand:'#d9b987'}[k]||'#c99f6e')}
  function setSteamSource(k){/* solar ghost field */
    if(k==='solar'&&!world.getObjectByName('solarField')){
      const sf=new THREE.Group();sf.name='solarField';
      for(let i=0;i<8;i++){const mir=new THREE.Mesh(new THREE.BoxGeometry(1.6,.04,1),new THREE.MeshStandardMaterial({color:'#9ab8d4',roughness:.15,metalness:.8,transparent:true,opacity:.55}));
        mir.position.set(-22+i*3,1,-17);mir.rotation.x=-.6;sf.add(mir)}
      world.add(sf);
    } else {const sf=world.getObjectByName('solarField');if(sf)sf.visible=(k==='solar')}
  }

  // ---------- per-frame update ----------
  let crankTheta=0, slack=0, lastFlash=0;
  function update(st,dt,simSpeed){
    const now=performance.now()/1000;
    // pumping unit
    const spm=st.spm;
    if(st.phase==='PRODUCTION'||st.phase==='DECLINE'){
      // stroke shaper: slower downstroke when kd>0.5 — approximate with sinusoidal speed mod
      const w=spm*Math.PI/30; // rad/s for theta
      const kd=st.kd||0.5;
      const wEff=w*(1+(kd-.5)*1.6*Math.sin(crankTheta));
      crankTheta+=wEff*dt*Math.min(simSpeed,40);
    }
    const b=solveBeam(crankTheta);
    beam.rotation.z=b;
    crankGroupL.rotation.z=crankTheta-Math.PI/2; crankGroupR.rotation.z=crankTheta-Math.PI/2;
    // pitmans: from crank pin to equalizer
    const eqP=new THREE.Vector3(); eq.getWorldPosition(eqP);
    [[pitL,crankGroupL,-1.0],[pitR,crankGroupR,1.0]].forEach(([pit,cg,z])=>{
      const pinLocal=new THREE.Vector3(0,CRANK_R,0); const pinW=cg.localToWorld(pinLocal.clone());
      pit.position.set(pinW.x,pinW.y,z);
      const target=new THREE.Vector3(eqP.x,eqP.y,z);
      const len=pinW.distanceTo(target);
      pit.scale.y=len;
      pit.lookAt(target); pit.rotateX(Math.PI/2);
      pit.position.copy(pinW); pit.translateY?0:0;
    });
    // polished rod / carrier: horsehead tip
    const tipLocal=new THREE.Vector3(Lf,0,0); const tipW=beam.localToWorld(tipLocal.clone());
    const rodTopY=tipW.y-1.0, rodX=0.05;
    const st_float=(lens==='risk'||st.margins.float<0.06)&& (st.phase==='PRODUCTION'||st.phase==='DECLINE');
    slack=st_float? clamp(.5+.5*Math.sin(now*3),0,1):Math.max(0,slack-dt*4);
    carrier.position.set(rodX,rodTopY-0.1,0);
    prclamp.position.set(rodX,rodTopY-0.05,0);
    polishedRod.position.set(rodX,rodTopY-4.5,0);
    // bridle: from head arc edges → carrier (sag when slack)
    const hp=bridleGeo.attributes.position;
    const hx=tipW.x-.15, hy=tipW.y+.35;
    const sag=slack*1.4;
    hp.setXYZ(0,hx-.5,hy-.3,-.28); hp.setXYZ(1,rodX-.3,(hy+rodTopY)/2-sag,-.28); hp.setXYZ(2,rodX,rodTopY,-.28);
    hp.setXYZ(3,rodX,rodTopY,.28); hp.setXYZ(4,hx-.5,hy-.3,.28);
    hp.needsUpdate=true;
    // rod string follows carrier top (subtle stretch wave)
    const stretch=Math.sin(crankTheta)*.35;
    rodSegs.forEach((s,i)=>{s.position.x=0;s.position.y=-(i+.5)*segLen + (rodTopY-1.55)*(1-i/NSEG)*0.06 + stretch*0.05*(1-i/NSEG)});
    plunger.position.y=.2+ Math.sin(crankTheta)*.18;
    fluidInBarrel.scale.y=clamp(st.fillage,.2,1);
    fluidLevelM.position.y=depthToY(st.fluidLevel);
    anchors.fluid_level.position.y=fluidLevelM.position.y;
    // heat
    const tT=clamp((st.sandfaceT-48)/112,0,1);
    const hr=st.heatedR;
    heatShells.forEach((sh,i)=>{const s=hr*(0.5+i*.28)/6;sh.scale.set(s*1.3,s*.85,s*1.3);sh.material.color.copy(thermal(tT*(1-i*.15)));sh.material.opacity=(.16-i*.03)*(0.4+tT)});
    heatCore.material.color.copy(thermal(tT)); heatCore.scale.set(hr*.16,hr*.10,hr*.16);
    sliceF.material.color.copy(thermal(tT)); sliceS.material.color.copy(thermal(tT));
    const rs=hr*.34; sliceF.scale.set(rs,rs*.7,1); sliceS.scale.set(rs,rs*.7,1);
    isoRings.forEach((r,i)=>{const rr=hr*(.16+i*.09)/6;const sc=Math.max(.05,rr);r.scale.set(sc,sc,1);r.material.color.copy(thermal(tT*(1-i*.06)));r.material.opacity=.2+tT*.55});
    perfDots.forEach((d,i)=>d.scale.setScalar(.8+.5*Math.sin(now*3.5+i*1.3)));
    capGlow.material.opacity=.15+tT*.3;
    if(lens==='thermal'){heatShells.forEach(s=>s.material.opacity*1.4)}
    // mechanical lens: stress wave on rods
    if(lens==='mech'){rodSegs.forEach((s,i)=>{const w=Math.sin(now*2.2-i*.55);const c=thermal(.5+w*.35);s.material.color.copy(c);s.material.emissive=c.clone().multiplyScalar(.4)})}
    // risk lens: pulse hotspots
    if(lens==='risk'){const pl=.5+.5*Math.sin(now*4);
      rodSegs.forEach((s,i)=>{const bad=i>14;s.material.emissive=new THREE.Color(bad?'#b3362c':'#000000');s.material.emissiveIntensity=bad?pl*.8:0});
      barrel.material.emissive=new THREE.Color('#b3362c');barrel.material.emissiveIntensity=pl*.5;
    } else {rodSegs.forEach(s=>{s.material.emissive=new THREE.Color(0);s.material.emissiveIntensity=0});barrel.material.emissive=new THREE.Color(0)}
    // steam particles during injection
    if(st.phase==='INJECTION'){steamPts.visible=true;
      const pp=steamPts.geometry.attributes.position;
      for(let i=0;i<160;i++){let f=steamData[i*3]+dt*2.2*Math.min(simSpeed,8);if(f>1)f-=1;steamData[i*3]=f;
        const y=lerp(2.2,pumpY,f); pp.setXYZ(i,(Math.random()-.5)*.05+.0,y,(Math.random()-.5)*.05)}
      pp.needsUpdate=true;
    }
    // oil particles
    if(oilPts.visible){const pp=oilPts.geometry.attributes.position;const speed=clamp(st.oilRate/46,0.1,2);
      for(let i=0;i<260;i++){let r=oilData[i*4],th=oilData[i*4+1],z=oilData[i*4+2],v=oilData[i*4+3];
        r-=dt*speed*v*2.2;if(r<.4){r=2.4+Math.random()*7;th=Math.random()*Math.PI/2;z=resT+Math.random()*(resB-resT)}
        oilData[i*4]=r;oilData[i*4+1]=th;oilData[i*4+2]=z;
        pp.setXYZ(i,Math.cos(th)*r*.9,z,Math.sin(th)*r*.9)}
      pp.needsUpdate=true; oilPts.material.opacity=lens==='flow'?.95:.35;
    }
    // dust
    {const pp=dustPts.geometry.attributes.position;
      for(let i=0;i<120;i++){let x=dustData[i*3]+dt*(1.2+Math.sin(i));if(x>30)x-=60;dustData[i*3]=x;
        pp.setXYZ(i,x,dustData[i*3+1]+Math.sin(now+i)*.3,dustData[i*3+2])}
      pp.needsUpdate=true; dustPts.material.opacity=stormVis? .8:.25;}
    // impact flash on float
    if(st_float&&Math.abs(Math.sin(crankTheta))>.98&&now-lastFlash>2){
      lastFlash=now;flash.position.set(0,rodTopY-0.4,0);flash.material.opacity=.9;flash.scale.setScalar(1);
    }
    flash.material.opacity=Math.max(0,flash.material.opacity-dt*3);
    flash.scale.addScalar(dt*8);
  }
  // impact flash sprite
  const flash=new THREE.Mesh(new THREE.RingGeometry(.2,.5,20),new THREE.MeshBasicMaterial({color:'#fff',transparent:true,opacity:0,side:THREE.DoubleSide,depthWrite:false}));
  world.add(flash);
  let stormVis=false;

  // ---------- render loop ----------
  function resize(){const w=canvas.clientWidth,h=canvas.clientHeight;if(canvas.width!==w*renderer.getPixelRatio()){renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix()}}
  window.addEventListener('resize',resize);

  const api={
    scene,camera,renderer,anchors,MATS,setLens,setXray,setClimate,setFormation,setSteamSource,
    get lens(){return lens}, get xray(){return xray},
    depthToY,yToDepth,
    setStorm:v=>stormVis=v,
    cam,
    onPartClick:null,onPartHover:null,
    update,
    get crankTheta(){return crankTheta},
    frame(dt,st,simSpeed){
      resize();
      // camera idle drift
      if(cam.auto){cam.azT=.62+Math.sin(performance.now()/40000)*.05;cam.elT=.34}
      cam.az=lerp(cam.az,cam.azT,.08);cam.el=lerp(cam.el,cam.elT,.08);cam.dist=lerp(cam.dist,cam.distT,.08);
      cam.tx=lerp(cam.tx,cam.txT,.08);cam.ty=lerp(cam.ty,cam.tyT,.08);cam.tz=lerp(cam.tz,cam.tzT,.08);
      camera.fov=lerp(camera.fov,cam.fovT,.12);camera.updateProjectionMatrix();
      const cx=cam.tx+cam.dist*Math.cos(cam.el)*Math.cos(cam.az);
      const cz=cam.tz+cam.dist*Math.cos(cam.el)*Math.sin(cam.az);
      const cy=cam.ty+cam.dist*Math.sin(cam.el);
      camera.position.set(cx,cy,cz);camera.lookAt(cam.tx,cam.ty,cam.tz);
      update(st,dt,simSpeed);
      renderer.render(scene,camera);
    },
    project(v3){const v=v3.clone().project(camera);const r=canvas.getBoundingClientRect();return{x:(v.x*.5+.5)*r.width,y:(-v.y*.5+.5)*r.height,behind:v.z>1}},
    anchorScreen(name){const o=anchors[name];if(!o)return null;const p=new THREE.Vector3();o.getWorldPosition(p);return api.project(p)},
    // material drain for transition: 0..1 — colours wash out to paper, ink edges appear
    drain:t=>{
      for(let s=0;s<7;s++){const m=MATS['strat'+s];if(!m.userData.base)m.userData.base=new THREE.Color(strataColors[s]);m.color.copy(m.userData.base).lerp(new THREE.Color('#f5f2ea'),t)}
      const objs=[MATS.paintY,MATS.paintG,MATS.steel,MATS.alu,MATS.sand,MATS.gravel,MATS.concrete,MATS.tubular,MATS.vit,MATS.rod,MATS.chrome,MATS.blanket,MATS.hazard,MATS.rope,MATS.belt,MATS.guide,MATS.oil,MATS.water,MATS.valveRed,MATS.brass,MATS.pad];
      objs.forEach(m=>{if(!m.userData.base)m.userData.base=m.color.clone();m.color.copy(m.userData.base).lerp(new THREE.Color('#faf8f2'),t)});
      edgeMat.opacity=lerp(.5,1,t);edgeMat.color.set(t>.4?'#26221a':'#3a3428');
      skyMat.uniforms.top.value.lerpColors(new THREE.Color(SKYBASE.top),new THREE.Color('#f3eee2'),t);
      skyMat.uniforms.mid.value.lerpColors(new THREE.Color(SKYBASE.mid),new THREE.Color('#f3eee2'),t);
      skyMat.uniforms.bot.value.lerpColors(new THREE.Color(SKYBASE.bot),new THREE.Color('#f3eee2'),t);
      skyMat.uniforms.glow.value.lerpColors(new THREE.Color(SKYBASE.bot),new THREE.Color('#f3eee2'),t);
      stars.material.opacity=(SKYBASE.stars||0)*(1-clamp(t*2,0,1));
      hemi.intensity=lerp(.85,1.6,t); sun.intensity=lerp(2.1,.4,t);
      heatGroup.visible=sliceF.visible=sliceS.visible=capGlow.visible=t<0.7;
      isoRings.forEach(r=>r.visible=t<0.85);
      perfDots.forEach(d=>d.visible=t<0.7);
      oilPts.visible=steamPts.visible=dustPts.visible=t<0.4;
      fluidLevelM.visible=true;
      scene.fog.color.set(new THREE.Color('#1a2030').lerp(new THREE.Color('#f3eee2'),t));
      scene.fog.near=lerp(120,4000,t);scene.fog.far=lerp(400,6000,t);
    },
    // flatten world depth into a card during Twin→Blueprint: 0..1
    flatten:t=>{world.scale.z=lerp(1,.045,easeIO(t))},
  };
  let SKYBASE={top:'#232c4e',mid:'#4a4058',bot:'#c9805a'};
  const _setClimate=setClimate;
  api.setClimate=k=>{const s=SKIES[k]||SKIES.dusk;SKYBASE={top:s.top,mid:s.mid,bot:s.bot,stars:s.stars};_setClimate(k)};
  setClimate('dusk');
  return api;
}
