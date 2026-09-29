// ============================================================
// Mantle demo — app shell: router, screens, overlays, transition
// ============================================================
import { createTwin, depthToY } from './three-scene.js';
import { buildBlueprint } from './blueprint.js';
import * as S from './sim.js';
import { el, INK, BLUE, RED, AMB, GRN, DIM, TWIN, axes, line, txt, path, area, sparkline, donut, ring, dynoCard } from './charts.js';

const {clamp,lerp}=S;
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const easeIO=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
const easeOut=t=>1-Math.pow(1-t,3);
function tween(dur,fn,done){const t0=performance.now();function f(){const p=Math.min(1,(performance.now()-t0)/dur);fn(easeIO(p));if(p<1)requestAnimationFrame(f);else done&&done()}requestAnimationFrame(f)}
function toast(msg,cls='ok'){const t=document.createElement('div');t.className='toast '+cls;t.textContent=msg;$('#toasts').appendChild(t);setTimeout(()=>{t.style.opacity=0;setTimeout(()=>t.remove(),400)},2800)}

// ---------- global state ----------
const G={ t:41, playing:false, speed:1, screen:'well', mode:'twin', persona:'OP',
  scenario:null, prov:false, story:-1, tp:0, tpT:0 }; // tp: twin⇄blueprint progress
let simState=S.state(G.t,S.COND_FX);

// ---------- twin scene (graceful 2D fallback if WebGL unavailable) ----------
let twin;
try{ twin=createTwin($('#gl')); }
catch(err){
  console.warn('WebGL unavailable — falling back to Blueprint view',err);
  const noop=()=>{};
  twin={cam:{az:.62,azT:.62,el:.34,elT:.34,dist:44,distT:44,tx:0,ty:0,tz:0,txT:0,tyT:0,tzT:0,fov:38,fovT:38,auto:false},
    anchors:{},lens:'physical',xray:false,crankTheta:0,
    setLens:noop,setXray:noop,setClimate:noop,setFormation:noop,setSteamSource:noop,setStorm:noop,drain:noop,
    frame:noop,update:noop,project:()=>null,anchorScreen:()=>null,onPartClick:null,onPartHover:null};
  setTimeout(()=>{document.querySelector('#intro')?.remove();applyTP(1);toast('No WebGL — showing Blueprint view','warn')},800);
}
twin.onPartClick=part=>openSheet(sheetFor(part));
twin.onPartHover=(part,point,e)=>{ if(!part||!e)return hidePeek();
  showPeek(e.clientX,e.clientY,peekFor(part)); };

// ---------- blueprint ----------
const bpView=$('#blueprint-view'); const bp=buildBlueprint(bpView);

// ---------- router ----------
const ROUTES={well:'#screen-well',field:'#screen-field',arena:'#screen-arena',ledger:'#screen-ledger',impact:'#screen-impact',proof:'#screen-proof',play:'#screen-play',m:'#screen-mobile'};
function nav(screen){
  const wantBP=location.hash.includes('/bp'), tpQ=location.hash.match(/tp=([\d.]+)/);
  G.screen=screen; location.hash='#/'+screen+(wantBP&&screen==='well'?'/bp':'');
  $$('.screen').forEach(s=>s.classList.remove('active'));
  $(ROUTES[screen]).classList.add('active');
  $$('#screen-tabs .tab').forEach(b=>b.classList.toggle('on',b.dataset.nav===screen));
  const skin= screen==='well'?(G.mode==='twin'?'glass':'paper'): screen==='m'?'glass':'paper';
  document.body.dataset.skin=skin;
  $('#mode-toggle').style.display=screen==='well'?'':'none';
  $('#well-context').style.display=screen==='m'?'none':'';
  $('#timeline-dock').style.display=(screen==='m'||screen==='play')?'none':'';
  renderScreen(screen);
  // subtle screen fade-in
  const el=$(ROUTES[screen]);el.style.opacity=0;el.style.transform='translateY(6px)';
  requestAnimationFrame(()=>requestAnimationFrame(()=>{el.style.transition='opacity .35s,transform .35s';el.style.opacity=1;el.style.transform='none'}));
  // paper-wipe transition between non-well screens
  if(screen!=='well'&&prevScreen==='well')paperWipeNav();
  if(screen==='well'&&tpQ){applyTP(parseFloat(tpQ[1]));snapCam()} // debug: force a transition pose
  else if(screen==='well'&&wantBP){applyTP(1);snapCam()} else if(screen==='well'&&G.tp>0&&!bpState.on)applyTP(0);
  prevScreen=screen;
}
let prevScreen='well';
function snapCam(){const c=twin.cam;c.az=c.azT;c.el=c.elT;c.dist=c.distT;c.tx=c.txT;c.ty=c.tyT;c.tz=c.tzT;twin.camera.fov=c.fovT;twin.camera.updateProjectionMatrix()}
function paperWipeNav(){/* subtle: handled by CSS skin swap */ }
window.addEventListener('hashchange',()=>{const h=location.hash.replace('#/','')||'well';const r=h.split('/')[0];if(ROUTES[r]&&r!==G.screen)nav(r)});

// ---------- render dispatch ----------
const rendered={};
function renderScreen(s){
  if(s==='field')renderField();
  if(s==='arena')renderArena();
  if(s==='ledger')renderLedger();
  if(s==='impact')renderImpact();
  if(s==='proof')renderProof();
  if(s==='m')renderMobile();
}

// ---------- callouts ----------
const CALLOUT_SETS={
  PRODUCTION:[
    ['polished_rod','POLISHED ROD',st=>`${st.pprl.toFixed(0)} / ${st.mprl.toFixed(0)} <small>kN</small>`,st=>`margin ${(st.margins.float*100).toFixed(0)}%`],
    ['crank','CRANK',st=>`${st.spm.toFixed(1)} <small>SPM</small>`,st=>`torque ${st.torquePct.toFixed(0)}%`],
    ['motor','MOTOR·VFD',st=>`${st.powerKw.toFixed(1)} <small>kW</small>`,st=>`${st.freqHz.toFixed(0)} Hz`],
    ['flowline','FLOWLINE',st=>`${st.oilRate.toFixed(0)} <small>BOPD</small>`,st=>`WC ${st.waterCut}% · ${st.whT.toFixed(0)} °C`],
    ['fluid_level','FLUID LEVEL',st=>`${st.fluidLevel.toFixed(0)} <small>m</small>`,st=>`subm. ${st.submergence.toFixed(0)} m`],
    ['pump','PUMP',st=>`${(st.fillage*100).toFixed(0)}<small>%</small>`,st=>`η ${(st.fillage*92).toFixed(0)}% · HD 2.3×`],
    ['heated_zone','HEATED ZONE',st=>`${st.sandfaceT.toFixed(0)} <small>°C</small>`,st=>`${st.viscosity.toFixed(0)} cP · r_h ${st.heatedR.toFixed(1)} m`],
  ],
  INJECTION:[
    ['steam_inlet','STEAM INLET',st=>`${st.steamRate.toFixed(0)} <small>t/d</small>`,st=>`${st.whp.toFixed(1)} bar`],
    ['wellhead','WELLHEAD',st=>`${st.steamCum} / ${st.steamTgt} <small>t</small>`,st=>'cum. steam'],
    ['casing_upper','CASING',st=>`${st.casingStress.toFixed(0)}% <small>yield</small>`,st=>'thermal stress'],
    ['rod_mid','VIT',st=>`q_sf ${(68+ st.sandfaceT/20).toFixed(0)}%`,st=>'quality@depth'],
    ['perforations','PERFORATIONS',st=>`${st.sandfaceT.toFixed(0)} <small>°C</small>`,st=>'sandface'],
    ['heated_zone','HEATED ZONE',st=>`r_h ${st.heatedR.toFixed(1)} <small>m</small>`,st=>'growing'],
    ['caprock','CAPROCK LOSS',st=>`${(st.sandfaceT*0.05).toFixed(1)} <small>kW</small>`,st=>'to overburden'],
  ],
  SOAK:[
    ['wellhead','SHUT-IN',st=>`${(-G.t).toFixed(1)} <small>d</small>`,st=>'soak 6 d opt.'],
    ['heated_zone','HEATED ZONE',st=>`${st.heatedTavg.toFixed(0)} <small>°C avg</small>`,st=>'diffusing'],
    ['caprock','LOSS',st=>`${(st.sandfaceT*0.06).toFixed(1)} <small>kW</small>`,st=>'to caprock'],
    ['perforations','PERF PRESSURE',st=>`${st.pwp.toFixed(1)} <small>bar</small>`,st=>'building'],
  ],
};
CALLOUT_SETS.DECLINE=CALLOUT_SETS.PRODUCTION;
const coLayer=$('#callouts'), ldSvg=$('#leader-svg');
let coEls=[];
function buildCallouts(){
  coLayer.innerHTML='';ldSvg.innerHTML='';coEls=[];
  const set=CALLOUT_SETS[simState.phase]||CALLOUT_SETS.PRODUCTION;
  for(const [anchor,name,v1,v2] of set){
    const d=document.createElement('div');d.className='callout';
    d.innerHTML=`<div class="co-card"><div class="co-name">${name}</div><div class="co-val"><span class="v1"></span><br><span class="v2" style="opacity:.65;font-size:10px"></span></div></div>`;
    d.onclick=()=>openSheet(sheetFor(anchor));
    coLayer.appendChild(d);
    const ln=el('path',{fill:'none',stroke:'rgba(255,255,255,.45)','stroke-width':1},ldSvg);
    const dot=el('circle',{r:2.4,fill:'#fff'},ldSvg);
    coEls.push({anchor,d,ln,dot,v1:q=>d.querySelector('.v1').innerHTML=v1(q),v2:q=>d.querySelector('.v2').innerHTML=v2(q),v1f:v1,v2f:v2,name});
  }
}
function layoutCallouts(){
  const visible=G.screen==='well'&&G.tp<0.12;
  for(const c of coEls){
    if(!visible){c.d.classList.add('hidden-co');c.ln.style.opacity=0;c.dot.style.opacity=0;continue}
    const p=twin.anchorScreen(c.anchor);
    if(!p||p.behind){c.d.classList.add('hidden-co');c.ln.style.opacity=0;c.dot.style.opacity=0;continue}
    c.d.classList.remove('hidden-co');
    c.v1f(simState);c.v2f(simState);
    const r=c.d.getBoundingClientRect(),W=r.width||120,H=r.height||44;
    const dir=p.x<innerWidth/2?-1:1;
    const cx=clamp(p.x+dir*(70+W/2),W/2+8,innerWidth-W/2-360);
    const cy=clamp(p.y-40,70,innerHeight-160);
    c.d.style.left=cx+'px';c.d.style.top=cy+'px';
    c.d.classList.toggle('alarm',c.anchor==='polished_rod'&&simState.margins.float<0.25);
    const x1=cx-dir*W/2,y1=cy;
    c.ln.setAttribute('d',`M${p.x} ${p.y}L${p.x+dir*24} ${p.y}L${x1} ${y1}`);
    c.ln.style.opacity=1;
    c.dot.setAttribute('cx',p.x);c.dot.setAttribute('cy',p.y);c.dot.style.opacity=1;
    c.d.classList.toggle('min',twin.cam.dist>108||twin.cam.dist<26);
  }
}
function sheetFor(part){
  if(/steam|wellhead|stuffing/.test(part))return 'wellhead';
  if(/pump|rod|carrier/.test(part))return 'lift';
  if(/strat|heated|caprock|perforations|terrain/.test(part))return 'reservoir';
  if(/tubing|casing|fluid/.test(part))return 'wellbore';
  return 'unit';
}

// ---------- peek cards ----------
const peekEl=$('#peek');let peekTimer=null;
function showPeek(x,y,html){clearTimeout(peekTimer);peekTimer=setTimeout(()=>{peekEl.innerHTML=html;peekEl.style.left=Math.min(x+14,innerWidth-250)+'px';peekEl.style.top=Math.min(y+14,innerHeight-160)+'px';peekEl.classList.add('show')},300)}
function hidePeek(){clearTimeout(peekTimer);peekEl.classList.remove('show')}
document.addEventListener('mousemove',e=>{if(!peekEl.classList.contains('show'))return;const r=peekEl.getBoundingClientRect()});
document.addEventListener('mouseout',e=>{if(e.target===document.querySelector('#gl'))hidePeek()});
function peekFor(part){
  const st=simState;
  const map={
    'polished-rod':`<div class="pk-t">POLISHED ROD</div>${spark(`PPRL ${st.pprl.toFixed(0)} kN`)}<div class="pk-s">load · rod-float margin ${(st.margins.float*100).toFixed(0)}% · tension peaks at upstroke mid</div>`,
    'gearbox':`<div class="pk-t">GEARBOX</div>${spark(`torque ${st.torquePct.toFixed(0)}% rating`)}<div class="pk-s">peak ${(st.torquePct*1.9).toFixed(0)} kN·m · counterbalance −6%</div>`,
    'motor':`<div class="pk-t">MOTOR · VFD</div>${spark(`${st.powerKw.toFixed(1)} kW`)}<div class="pk-s">${st.freqHz.toFixed(0)} Hz · Stroke Shaper kd ${st.kd}</div>`,
    'wellhead':`<div class="pk-t">THERMAL WELLHEAD</div>${spark(`${st.whp.toFixed(1)} bar`)}<div class="pk-s">${st.whT.toFixed(0)} °C · casing stress ${st.casingStress.toFixed(0)}% yield</div>`,
    'steam-valve':`<div class="pk-t">STEAM INLET</div>${spark(`${st.steamRate.toFixed(0)} t/d`)}<div class="pk-s">OTSG ${S.COND.steam==='solar'?'solar-hybrid':'gas-fired'} · quality 80% surf / ${(68+st.sandfaceT/20).toFixed(0)}% sf</div>`,
    'flowline':`<div class="pk-t">FLOWLINE</div>${spark(`${st.oilRate.toFixed(0)} BOPD`)}<div class="pk-s">WC ${st.waterCut}% · WH temp ${st.whT.toFixed(0)} °C</div>`,
    'pump':`<div class="pk-t">INSERT PUMP 2¼″ RHBC</div>${spark(`fillage ${(st.fillage*100).toFixed(0)}%`)}<div class="pk-s">@1080 m · hold-down margin 2.3× · TV/SV healthy</div>`,
    'tubing':`<div class="pk-t">VIT TUBING 3½″</div>${spark('heat loss ↓')}<div class="pk-s">vacuum-insulated · steam quality preserved to sandface</div>`,
    'casing':`<div class="pk-t">PRODUCTION CASING 7″</div>${spark(`σ ${st.casingStress.toFixed(0)}% yield`)}<div class="pk-s">thermal grade · cement bonded to 700 m</div>`,
    'terrain':`<div class="pk-t">BAGHEWALA PAD</div>${spark('Thar desert')}<div class="pk-s">Bikaner district · illustrative layout</div>`,
  };
  if(/strat/.test(part))return `<div class="pk-t">${['AEOLIAN SAND','TERTIARY','NAGAUR SS','BILARA CAPROCK','UPPER CARB','JODHPUR SS — PAY','BASEMENT'][+part.slice(-1)]}</div>${spark('')}<div class="pk-s">k≈800 mD · φ .22 · ρc 2.4 MJ/m³K · schematic</div>`;
  return map[part]||`<div class="pk-t">${part.toUpperCase()}</div><div class="pk-s">part of BGW-17</div>`;
}
function spark(label){const pts=[.4,.5,.45,.6,.55,.7,.66,.62].map(v=>[0,v]);
  const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox','0 0 200 34');
  sparkline(svg,200,34,[3,5,4,6,5.4,7,6.2,5.8,6.6,7.4]);
  return `<b style="font-family:IBM Plex Mono;font-size:13px">${label}</b>`+new XMLSerializer().serializeToString(svg);}

// ---------- inspect sheets ----------
const SHEETS={
  unit:{title:'SURFACE UNIT · API C-320D',tabs:['Overview','Stroke Shaper','Energy'],body:t=>`
    ${kv('SPM',st=>st.spm.toFixed(1))}${kv('Stroke',()=> '120 in (144 avail)')}${kv('kd — downstroke share',st=>st.kd)}
    ${kv('Gearbox torque',st=>st.torquePct.toFixed(0)+' % rating')}${kv('Polished-rod HP',st=>(st.powerKw*0.62).toFixed(1)+' hp')}
    ${kv('Motor',st=>st.powerKw.toFixed(1)+' kW · '+st.freqHz.toFixed(0)+' Hz')}
    <h5>Stroke Shaper — in-stroke VFD profile</h5><svg viewBox="0 0 300 140" id="shaper-svg"></svg>
    <div class="kv"><span>kd (what-if)</span><b>0.50 – 0.70</b></div>`},
  wellhead:{title:'WELLHEAD & STEAM',tabs:['Injection','Heat balance','Casing'],body:t=>`
    ${kv('Steam rate',st=>st.steamRate.toFixed(0)+' t/d')}${kv('Wellhead P',st=>st.whp.toFixed(1)+' bar')}
    ${kv('Quality surf→sf',st=>`80% → ${(68+st.sandfaceT/20).toFixed(0)}%`)}${kv('Cumulative',st=>st.steamCum+' / '+st.steamTgt+' t')}
    <h5>Heat balance (Sankey)</h5><svg viewBox="0 0 300 120" id="sankey-svg"></svg>
    <h5>Casing thermal stress</h5>${kv('σ/σy',st=>st.casingStress.toFixed(0)+' %')}${kv('Ramp advice',()=>'≤ 40 °C/h')}`},
  wellbore:{title:'WELLBORE · VIT',tabs:['Profiles','Deposition','Fluid level'],body:t=>`
    ${kv('Fluid level',st=>st.fluidLevel.toFixed(0)+' m')}${kv('Submergence',st=>st.submergence.toFixed(0)+' m')}
    <h5>T / P / μ vs depth</h5><svg viewBox="0 0 300 200" id="prof-svg"></svg>
    <h5>Asphaltene band</h5><div class="kv"><span>onset T_ao</span><b>62 °C <span class="prov">ASSUM</span></b></div>
    <div class="kv"><span>risk interval</span><b>${(620+G.t*2).toFixed(0)}–1080 m</b></div>`},
  lift:{title:'PUMP & RODS — LIFT SHEET',tabs:['Card','Rod string','Risks','Schedule','Maint.'],body:t=>`
    <h5>Dynamometer cards</h5><svg viewBox="0 0 300 120" id="sheet-dyno"></svg>
    ${kv('Fillage',st=>(st.fillage*100).toFixed(0)+' %')}${kv('Diagnosis',st=>st.fillage<.7?'FLUID POUND':'NORMAL')}
    <h5>6 margins · time-to-limit</h5>${marginsHtml()}
    <h5>14-day SPM schedule</h5>${schedHtml()}`},
  reservoir:{title:'RESERVOIR — CSS SHEET',tabs:['Heat','Cycle','Cut-off','History'],body:t=>`
    ${kv('Sandface T',st=>st.sandfaceT.toFixed(0)+' °C')}${kv('Mean heated T',st=>st.heatedTavg.toFixed(0)+' °C')}
    ${kv('Heated radius',st=>st.heatedR.toFixed(1)+' m')}${kv('μ at sandface',st=>st.viscosity.toFixed(0)+' cP')}
    ${kv('Thermal battery',st=>(st.battery*100).toFixed(0)+' % · ~'+st.batDays+' d')}
    <h5>Marginal steam curve</h5><svg viewBox="0 0 300 110" id="marg-svg"></svg>
    <h5>Cut-off / re-steam window</h5><div class="kv"><span>marginal-value trigger</span><b>day ~${96+Math.round(G.t-41)}</b></div>
    <div class="kv"><span>cost of waiting +7 d</span><b class="mono">−₹0.9 L</b></div>`},
};
function kv(k,f){return `<div class="kv"><span>${k}</span><b class="mono" data-kf="${k}">${f(simState)}</b></div>`}
function marginsHtml(){const m=simState.margins;const names={float:'Rod float',pound:'Fluid pound',unsetting:'Unsetting',fatigue:'Fatigue',casing:'Casing',deposition:'Deposition'};
  return Object.entries(names).map(([k,n])=>{const v=m[k];const c=v>.5?GRN:v>.25?AMB:RED;
    return `<div class="kv"><span>${n}</span><b class="mono" style="color:${c}">${(v*100).toFixed(0)}% · ~${Math.max(1,Math.round(v*45))} d</b></div>`}).join('')}
function schedHtml(){let h='';for(let d=0;d<14;d++){const sp=clamp(4.9+0.9*Math.exp(-(G.t+d)/60),2,9);h+=`<div class="sched-row"><span class="sd">+${d}d</span><div class="sbar"><i style="left:0;width:${sp/9*100}%"></i></div><b>${sp.toFixed(1)}</b></div>`}return h}
function openSheet(id){
  const s=SHEETS[id];if(!s)return;
  $('#sheet-title').textContent=s.title;
  $('#sheet-tabs').innerHTML=s.tabs.map((t,i)=>`<button class="${i===0?'on':''}">${t}</button>`).join('');
  $('#sheet-body').innerHTML=s.body(G.t);
  $('#inspect-sheet').classList.add('open');
  drawSheetExtras();
}
$('#sheet-close').onclick=()=>$('#inspect-sheet').classList.remove('open');
$('#sheet-tabs').addEventListener('click',e=>{if(e.target.tagName==='BUTTON'){$$('#sheet-tabs button').forEach(b=>b.classList.remove('on'));e.target.classList.add('on')}});
$('.sheet-foot').addEventListener('click',e=>{const a=e.target.dataset?.act;if(a==='arena')nav('arena');if(a==='fork')fork();if(a==='ask')openPalette()});
function drawSheetExtras(){
  const dyno=$('#sheet-dyno');if(dyno){const ax=axes(dyno,300,120,{x:[0,1],y:[0,1],xt:2,yt:2,padL:24,padB:16,padT:6,padR:6});
    const pts=[],dpts=[];for(let u=0;u<=1;u+=.02){const[p,l]=dynoCard(u);pts.push([ax.sx(p),ax.sy(l)]);dpts.push([ax.sx(p),ax.sy(l*.88)])}
    line(dyno,pts,{stroke:INK,w:1.3});line(dyno,dpts,{stroke:BLUE,w:1,dash:'4 2'});txt(dyno,150,110,'surface —  downhole - -',{size:7,anchor:'middle'})}
  const sg=$('#shaper-svg');if(sg){const ax=axes(sg,300,140,{x:[0,360],y:[0,1.6],xt:4,yt:4,xl:'crank °',yl:'speed ×',padL:26,padB:18,padT:6,padR:6});
    const pts=[];for(let a=0;a<=360;a+=5){const ph=a*Math.PI/180;pts.push([ax.sx(a),ax.sy(1+(simState.kd-.5)*1.4*Math.sin(ph))])}
    line(sg,pts,{stroke:TWIN,w:1.6});txt(sg,150,14,'kd 0.62 — slow downstroke',{size:7,anchor:'middle',fill:TWIN})}
  const sk=$('#sankey-svg');if(sk){const y0=10;const flows=[['STEAM IN',100,INK],['surface loss',8,DIM],['wellbore loss',11,DIM],['TO RESERVOIR',81,BLUE],['caprock loss',14,RED],['produced heat',30,AMB],['retained',37,GRN]];
    let y=y0;flows.slice(0,4).forEach(([n,w,c])=>{el('rect',{x:4,y,width:8,height:w*.9,fill:c,opacity:.7},sk);txt(sk,16,y+8,n,{size:7});y+=w*.9+3});
    let y2=y0+19*.9+3+11*.9+3;flows.slice(4).forEach(([n,w,c])=>{el('rect',{x:120,y:y2,width:8,height:w*.9,fill:c,opacity:.7},sk);txt(sk,132,y2+8,n,{size:7});y2+=w*.9+3});
    el('path',{d:`M12 ${y0+19*.9} C60 ${y0+19*.9}, 60 ${y0+19*.9+11*.9+3}, 120 ${y0+19*.9+11*.9+3}`,stroke:BLUE,fill:'none','stroke-width':2,opacity:.5},sk)}
  const pf=$('#prof-svg');if(pf){const ax=axes(pf,300,200,{x:[0,3],y:[0,1200],xt:3,yt:4,xl:'',yl:'depth m',padL:40,padB:14,padT:6,padR:6});
    const T=[],P=[],mu=[];for(let d=0;d<=1200;d+=50){const y=ax.sy(d);T.push([ax.sx(S.sandfaceT(G.t)/180*2.4*Math.pow(d/1100,.55)+.1),y]);P.push([ax.sx(d/1100*1.2+.1),y]);mu.push([ax.sx((Math.log10(S.viscosity(lerp(34,S.sandfaceT(G.t),Math.pow(d/1100,.55))))-0.5)/4*2.8+.1),y])}
    line(pf,T,{stroke:RED,w:1.2});line(pf,P,{stroke:BLUE,w:1.2});line(pf,mu,{stroke:INK,w:1.2});
    txt(pf,ax.sx(2.6),16,'T', {size:8,fill:RED});txt(pf,ax.sx(1.6),16,'P',{size:8,fill:BLUE});txt(pf,ax.sx(.8),16,'μ',{size:8})}
  const mg=$('#marg-svg');if(mg){const ax=axes(mg,300,110,{x:[0,400],y:[0,30],xt:4,yt:3,xl:'+steam t',yl:'Δoil bbl',padL:30,padB:18,padT:6,padR:6});
    const pts=[];for(let x=0;x<=400;x+=20)pts.push([ax.sx(x),ax.sy(28*Math.exp(-x/140))]);
    line(mg,pts,{stroke:INK,w:1.3});
    const xp=ax.sx(210);line(mg,[[xp,ax.sy(0)],[xp,ax.sy(28*Math.exp(-210/140))]],{stroke:RED,w:1,dash:'3 3'});
    txt(mg,xp+4,ax.sy(6),'econ. stop',{size:7,fill:RED})}
}

// ---------- glass stack update ----------
const RISKS=[['float','Rod float'],['pound','Fluid pound'],['unsetting','Unsetting'],['fatigue','Fatigue'],['casing','Casing temp'],['deposition','Deposition']];
function buildRiskBars(){$('#risk-bars').innerHTML=RISKS.map(([k,n])=>`<div class="risk-row" data-r="${k}"><span class="r-name">${n}</span><div class="r-bar"><div class="r-fill"></div></div><span class="r-val"></span></div>`).join('');
  $$('#risk-bars .risk-row').forEach(r=>r.onclick=()=>openExplain(r.dataset.r))}
function updateGlass(){
  const st=simState;
  $('#rec-title').textContent=st.margins.float<.25?'Slow the downstroke':st.fillage<.7?'Prevent fluid pound':'Hold current plan';
  $('#rec-set').textContent=st.margins.float<.25?`SPM ${st.spm.toFixed(1)} → ${(st.spm*0.9).toFixed(1)} · kd 0.55 → 0.62`:`SPM ${st.spm.toFixed(1)} · stroke 120 · VFD on`;
  $('#rec-deltas').innerHTML=`<div class="d"><b>+${(st.oilRate*0.04).toFixed(1)}</b><span>BOPD</span></div><div class="d"><b>+${Math.max(2,st.margins.float*30|0)}</b><span>float margin %</span></div><div class="d neg"><b>${st.powerKw>16?'+':'−'}${(st.powerKw*.03).toFixed(1)}</b><span>kWh/bbl</span></div>`;
  $$('#risk-bars .risk-row').forEach(r=>{const v=st.margins[r.dataset.r];const f=r.querySelector('.r-fill');
    f.style.width=clamp(v*100,0,100)+'%';f.style.background=v>.5?'#3F9D5E':v>.25?'#C98A1B':'#B3362C';
    r.querySelector('.r-val').textContent=(v*100).toFixed(0)+'%';r.classList.toggle('alarm',v<.2)});
  const fc=S.forecast(G.t,30);drawForecast(fc);
  $('#econ-nums').innerHTML=`<div class="en"><b>${(st.netRsDay/1000).toFixed(1)}k</b><span>₹ net/day</span></div><div class="en"><b>${st.sor.toFixed(1)}</b><span>SOR cwe</span></div><div class="en"><b>${st.kwhBbl.toFixed(1)}</b><span>kWh/bbl</span></div><div class="en"><b>${st.co2Bbl}</b><span>kg CO₂/bbl</span></div>`;
  $('#b-fill').style.width=(st.battery*100)+'%';$('#b-pct').textContent=(st.battery*100).toFixed(0)+'%';
  $('#b-days').textContent=`cut-off in ~${st.batDays} d`;
  $('#cd-sub').textContent=`+6.8% oil · SOR −0.4 vs sequential`;
  $('#wc-day').textContent=Math.max(0,st.t).toFixed(0);
  $('#wc-phase').textContent=st.phase;
  $('#tl-t').textContent=st.t<0?`Day ${st.t.toFixed(0)}`:`Day ${st.t.toFixed(0)}`;
  $('#tl-phase').textContent=st.phase;
}
let fcDrawn=false;
function drawForecast(fc){const svg=$('#forecast-svg');if(!svg)return;svg.innerHTML='';
  const W=300,H=96,mx=Math.max(...fc.p90)*1.05;
  const p90=fc.p90.map((v,i)=>[10+i/30*(W-20),H-14-v/mx*(H-24)]);
  const p10=fc.p10.map((v,i)=>[10+i/30*(W-20),H-14-v/mx*(H-24)]);
  const p50=fc.p50.map((v,i)=>[10+i/30*(W-20),H-14-v/mx*(H-24)]);
  const gh=fc.ghost.map((v,i)=>[10+i/30*(W-20),H-14-v/mx*(H-24)]);
  area(svg,p90,p10,'#5B83F0',.22);line(svg,p50,{stroke:'#5B83F0',w:1.6});line(svg,gh,{stroke:'#B3362C',w:1,dash:'4 3'});
  txt(svg,W-10,12,'P10–P90',{size:7,anchor:'end',fill:'#8fa0b8'});txt(svg,10,H-2,'now',{size:7,fill:'#8fa0b8'});txt(svg,W-40,H-2,'+30 d',{size:7,anchor:'end',fill:'#8fa0b8'});
  txt(svg,W-8,p50.at(-1)[1]-4,fc.p50.at(-1).toFixed(0)+' BOPD',{size:7.5,anchor:'end',fill:'#fff',mono:true})}

// ---------- explain dialog ----------
function openExplain(risk){
  const m=simState.margins[risk];
  modal(`WHY — ${risk.toUpperCase()} MARGIN`,`
    <div class="kv"><span>margin now</span><b class="mono">${(m*100).toFixed(0)}%</b></div>
    <div class="kv"><span>time to limit</span><b class="mono">~${Math.max(1,Math.round(m*45))} d</b></div>
    <div class="kv"><span>P(event, 7 d)</span><b class="mono">${(0.4*(1-m)+0.05).toFixed(2)} ± .06</b></div>
    <h5 style="margin-top:10px">Top drivers (SHAP + physics)</h5>
    ${[['viscosity @900 m',0.42],['SPM',0.31],['kd downstroke share',0.18],['fluid level',0.09]].map(([n,w])=>`
      <div class="wf-step"><span class="wv">${(w*100).toFixed(0)}%</span><div class="wf-bar" style="width:${w*220}px"></div><span>${n}</span></div>`).join('')}
    <div style="margin-top:10px"><button class="btn sm" onclick="document.querySelector('#modal-wrap').classList.remove('open')">Close</button>
    <button class="btn sm" id="ex-causal">Causal trace →</button></div>`);
  $('#ex-causal')?.addEventListener('click',()=>modal('CAUSAL TRACE',`<div style="font-family:IBM Plex Mono;font-size:11px;line-height:2">
    steam design → reservoir T(r,z) → μ(z,t)<br>→ downstroke drag @900m → float margin → <b style="color:${RED}">recommendation</b><br><br>
    provenance: enkf state r12 · wave-solver v3 · card-cnn 0.4 · SIM</div>`));
}

// ---------- FIELD screen ----------
let fieldDrawn=false;
function renderField(){
  const svg=$('#field-map');svg.innerHTML='';
  const defs=el('defs',{},svg);
  // desert base
  el('rect',{x:0,y:0,width:820,height:470,fill:'#EFE6D0'},svg);
  for(let i=0;i<24;i++){el('path',{d:`M${i*36-20} ${(i*97)%470} q20 -8 40 0`,stroke:'#D9C9A0','stroke-width':6,fill:'none',opacity:.5},svg)}
  // pads + steam header
  const pads={};S.WELLS.forEach(w=>{pads[w.pad]=pads[w.pad]||[];pads[w.pad].push(w)});
  const padXY={};
  Object.entries(pads).forEach(([p,ws])=>{const x=ws[0].x-16,y=ws[0].y-14;padXY[p]=[x,y];
    el('rect',{x,y,width:74,height:52,fill:'#DCCFB2',stroke:INK,'stroke-width':.6,rx:2},svg);
    txt(svg,x+4,y+10,`PAD ${p}`,{size:6.5,fill:DIM});});
  // steam header polyline
  const hx=Object.values(padXY).map(p=>p[0]+30);const hline=el('path',{d:'M20 20 '+Object.values(padXY).map(p=>`L${p[0]+30} ${p[1]-8}`).join(' '),stroke:'#B34A3A','stroke-width':2.4,fill:'none','stroke-dasharray':'6 3',opacity:.8},svg);
  el('rect',{x:8,y:8,width:24,height:24,fill:'#C9805A',stroke:INK,'stroke-width':.8},svg);txt(svg,44,24,'OTSG ×3',{size:7.5,fill:INK});
  // wells
  S.WELLS.forEach(w=>{
    const g=el('g',{style:'cursor:pointer'},svg);
    const c=w.margin<.2?RED:w.margin<.45?AMB:GRN;
    el('circle',{cx:w.x,cy:w.y,r:7,fill:c,opacity:.9},g);
    el('circle',{cx:w.x,cy:w.y,r:10,fill:'none',stroke:c,'stroke-width':1,'stroke-dasharray':`${w.margin*63} 63`,transform:`rotate(-90 ${w.x} ${w.y})`},g);
    if(w.phase==='INJECTION')el('circle',{cx:w.x,cy:w.y,r:12,fill:'none',stroke:'#2F8FA8','stroke-width':1.6},g);
    txt(svg,w.x+12,w.y+3,w.id,{size:7,mono:true,fill:INK},g);
    g.addEventListener('mouseenter',e=>showPeek(e.clientX,e.clientY,
      `<div class="pk-t">${w.id} · ${w.phase}</div><div class="pk-s">oil ${w.oil} BOPD · float margin ${(w.margin*100).toFixed(0)}%<br>cut-off in ${w.cutoffIn} d · opportunity ₹${w.opp}k/d</div>`));
    g.addEventListener('mouseleave',hidePeek);
    g.addEventListener('click',()=>{$('#well-context .wc-name').textContent=w.id;nav('well')});
  });
  txt(svg,810,460,'ILLUSTRATIVE — Baghewala-S synthetic field',{size:8,anchor:'end',fill:DIM});
  // triage
  S.api.fieldTriage().then(rows=>{
    $('#triage-list').innerHTML=rows.map((w,i)=>`<div class="tr" data-w="${w.id}">
      <span class="rank">${i+1}</span><span class="tw">${w.id}</span>
      <span class="treason">${w.margin<.2?'float margin near limit':w.cutoffIn<25?'re-steam window opens':'fillage falling — pound risk'}</span>
      <span class="tval">₹${w.opp}k</span></div>`).join('');
    $$('#triage-list .tr').forEach(r=>r.onclick=()=>{$('#well-context .wc-name').textContent=r.dataset.w;nav('well')});
  });
  // gantt
  const g=$('#steam-gantt');g.innerHTML='';
  txt(g,4,10,'GEN-1', {size:7});txt(g,4,40,'GEN-2',{size:7});txt(g,4,70,'GEN-3',{size:7});txt(g,4,105,'CREW',{size:7});
  for(let i=0;i<3;i++){line(g,[[44,6+i*30],[376,6+i*30]],{w:.5,stroke:DIM});
    let x=44;for(let k=0;k<3+i;k++){const w=40+((i*37+k*53)%50);const wid=S.WELLS[(i*5+k*3)%30].id;
      el('rect',{x,y:2+i*30-4,width:w,height:12,fill:i%2?'#2F8FA8':'#B34A3A',opacity:.75,rx:1},g);
      txt(g,x+3,2+i*30+5,wid,{size:6,fill:'#fff',mono:true});x+=w+8}}
  for(let d=0;d<=30;d+=5)txt(g,44+d*11,120,`+${d}d`,{size:6.5,mono:true,fill:DIM});
  // kpis
  S.api.fieldSummary().then(s=>{$('#field-kpis').innerHTML=`
    <div class="kf"><b>${s.bopd}</b><span>BOPD field</span></div><div class="kf"><b>${s.sor}</b><span>SOR cwe</span></div>
    <div class="kf"><b>${s.kwh}</b><span>kWh/bbl</span></div><div class="kf"><b>${s.co2}</b><span>kg CO₂/bbl</span></div>
    <div class="kf"><b>${s.wells-3}/${s.wells}</b><span>wells healthy</span></div><div class="kf"><b style="color:${RED}">${s.alarms}</b><span>open alerts</span></div>`});
}
$('#fleet-btn')?.addEventListener('click',()=>{
  modal('FLEET — ALL 30 WELLS',`<table class="fleet-table"><tr><th>well</th><th>phase</th><th>oil</th><th>margin</th><th>SOR</th><th>cut-off</th><th>₹ opp</th></tr>
  ${S.WELLS.map(w=>`<tr data-w="${w.id}"><td>${w.id}</td><td>${w.phase}</td><td>${w.oil}</td><td>${(w.margin*100).toFixed(0)}%</td><td>${w.sor}</td><td>${w.cutoffIn}d</td><td>${w.opp}k</td></tr>`).join('')}</table>`);
  $$('#modal .fleet-table tr[data-w]').forEach(r=>r.onclick=()=>{closeModal();$('#well-context .wc-name').textContent=r.dataset.w;nav('well')});
});
$('#sched-btn')?.addEventListener('click',()=>modal('STEAM SCHEDULER · CP-SAT',`
  <div class="kv"><span>3 generators · 190 t/d capacity</span><b class="mono">30-d horizon</b></div>
  <div class="kv"><span>shadow price +1 generator-day</span><b class="mono">₹18.4k</b></div>
  <div class="kv"><span>GEN-2 down 10 d what-if</span><b class="mono" style="color:${RED}">−3 wells slip · −₹2.1 L</b></div>
  <p style="margin-top:8px;font-size:11px;color:#8A8A80">Drag slots in the real build; demo shows the solved plan on the map plate.</p>`));

// ---------- ARENA screen ----------
let arenaDrawn=false;
function renderArena(){
  if(arenaDrawn)return;arenaDrawn=true;
  const svg=$('#arena-chart');svg.innerHTML='';
  const ax=axes(svg,900,340,{x:[0,360],y:[0,80],xt:9,yt:4,xl:'day',yl:'BOPD',padL:44,padB:26,padT:14,padR:10});
  S.api.arenaSeries().then(series=>{
    // cycle dividers + failure markers
    [120,240].forEach(d=>line(svg,[[ax.sx(d),ax.y0],[ax.sx(d),ax.y1]],{stroke:DIM,w:.6,dash:'3 4'}));
    S.STRATS.forEach(st=>{
      const pts=series[st.id].map((v,d)=>[ax.sx(d),ax.sy(v)]);
      line(svg,pts,{stroke:st.color,w:st.bold?2.6:1.2,dash:st.dash||'',op:st.id==='S0'?.9:1});
    });
    // failure markers for greedy & static
    [58,172,290].forEach(d=>{el('path',{d:`M${ax.sx(d)} ${ax.sy(4)} l5 -8 l5 8 Z`,fill:RED},svg)});
    [212].forEach(d=>el('path',{d:`M${ax.sx(d)} ${ax.sy(4)} l5 -8 l5 8 Z`,fill:'#9a9484'},svg));
    // legend
    S.STRATS.forEach((st,i)=>{const x=60+(i%5)*165,y=24+Math.floor(i/5)*14;
      line(svg,[[x,y],[x+18,y]],{stroke:st.color,w:st.bold?2.6:1.4,dash:st.dash||''});
      txt(svg,x+22,y+3,st.name,{size:7.5,fill:INK,weight:st.bold?600:400});});
    txt(svg,ax.sx(330),ax.sy(66),'oracle ceiling',{size:7.5,fill:DIM});
  });
  // scoreboard
  S.api.scoreboard().then(rows=>{
    $('#score-table').innerHTML=`<tr><th>strategy</th><th>Δ oil</th><th>Δ net ₹L</th><th>ΔSOR</th><th>fails</th><th>% oracle</th><th>win</th></tr>`+
      rows.map(r=>`<tr class="${r[0].includes('Mantle')?'mantle':''}"><td>${r[0]}</td>${r.slice(1).map(v=>`<td>${v}</td>`).join('')}</tr>`).join('')+
      `<tr class="dq"><td>S7 − SafetyGate</td><td>+26.1</td><td>+6.9</td><td>−0.8</td><td>DQ: 14 viol.</td><td>—</td><td>—</td></tr>`;
  });
  // coupling dividend waterfall
  const cd=$('#cd-waterfall');cd.innerHTML='';
  const parts=[['CSS-side',1.6,BLUE],['SRP-side',1.2,GRN],['Interaction',0.9,TWIN],['StrokeShaper',0.4,AMB]];
  let cum=0;const sc=v=>160-v*22;
  parts.forEach(([n,v,c],i)=>{const x=40+i*88;
    el('rect',{x,y:sc(cum+v),width:56,height:v*22,fill:c,opacity:.85},cd);
    txt(cd,x+28,sc(cum+v)-5,'+'+v.toFixed(1),{size:8,mono:true,anchor:'middle',fill:INK});
    txt(cd,x+28,172,n,{size:7,anchor:'middle',fill:DIM});cum+=v;
    if(i<3)line(cd,[[x+56,sc(cum)],[x+88,sc(cum)]],{stroke:DIM,w:.6,dash:'2 2'})});
  txt(cd,40,20,'COUPLING DIVIDEND = +₹4.1 L/cycle',{size:9,weight:600,fill:INK});
  // race (static frame; play animates)
  drawRace(0.35);
  // value vs risk scatter
  const vr=$('#vr-svg');vr.innerHTML='';
  const axv=axes(vr,400,180,{x:[0,1],y:[0,10],xt:4,yt:4,xl:'float hours / cycle',yl:'net ₹L/180d',padL:36,padB:22,padT:8,padR:8});
  const rng=(i,salt)=>{const x=Math.sin(i*127.1+salt*311.7)*43758.545;return x-Math.floor(x)};
  S.STRATS.forEach(st=>{if(st.id==='S8')return;const salt=st.id.charCodeAt(1);for(let i=0;i<26;i++){
    const base={S7:[5.8,6.5],S6:[5.2,9],S5:[4.6,10],S4:[2.8,26],S3:[4.0,13],S2:[3.8,14],S1:[3.3,15],S0:[2.6,17]}[st.id];
    el('circle',{cx:axv.sx((base[1]+(rng(i,salt)-.5)*8)/60),cy:axv.sy(base[0]+(rng(i,salt+9)-.5)*2),r:2.2,fill:st.color,opacity:.6},vr)}});
  txt(vr,axv.sx(.06),axv.sy(6.6),'Mantle',{size:7.5,fill:TWIN,weight:600});
  // ablation
  const ab=$('#ablation-svg');ab.innerHTML='';
  [['full Mantle',6.1,TWIN],['− EnKF (open loop)',4.9,BLUE],['− Stroke Shaper',5.4,BLUE],['− joint→sequential',2.0,AMB],['− Safety Gate','DQ',RED]].forEach(([n,v,c],i)=>{
    const y=20+i*30;txt(ab,8,y+10,n,{size:8,fill:INK});
    if(v==='DQ'){el('rect',{x:150,y:y,width:210,height:12,fill:'none',stroke:RED,'stroke-dasharray':'3 2'},ab);txt(ab,255,y+10,'disqualified — 14 violations',{size:7.5,anchor:'middle',fill:RED})}
    else{el('rect',{x:150,y:y,width:v/7*210,height:12,fill:c,opacity:.85},ab);txt(ab,150+v/7*210+6,y+10,'+₹'+v+'L',{size:7.5,mono:true,fill:INK})}});
}
function drawRace(f){ // f = progress 0..1
  const svg=$('#race-svg');svg.innerHTML='';
  const cum={S8:9200,S7:8600,S6:8100,S5:7300,S4:6100,S3:7000,S2:6800,S1:6600,S0:6200};
  const order=S.STRATS.filter(s=>s.id!=='S8').map(s=>[s,cum[s.id]*f]);
  order.sort((a,b)=>b[1]-a[1]);
  order.forEach(([s,v],i)=>{const y=10+i*20;
    el('rect',{x:8,y,width:v/9200*300,height:13,fill:s.color,opacity:.9},svg);
    txt(svg,12,y+10,s.id,{size:7,fill:'#fff',mono:true});
    txt(svg,8+v/9200*300+6,y+10,Math.round(v).toLocaleString()+' bbl',{size:7,mono:true,fill:INK})});
}
$('#race-play')?.addEventListener('click',()=>{let p=0;const iv=setInterval(()=>{p+=.02;drawRace(Math.min(1,p));if(p>=1)clearInterval(iv)},40)});
$('#run-arena')?.addEventListener('click',()=>{
  const stEl=$('#run-status');stEl.textContent='running 3 wells × 3 seeds × 1 cycle…';
  const msgs=['S4 greedy: rod failure on BGW-07 day 58','S6 RL: evaluating policy…','S7 Mantle: EnKF assimilating','done — Mantle +22% vs S0 (n=9, illustrative)'];
  msgs.forEach((m,i)=>setTimeout(()=>stEl.textContent=m,(i+1)*1600));
});

// ---------- LEDGER ----------
function renderLedger(){
  const dl=$('#decision-list');dl.innerHTML='';
  S.LEDGER.forEach(d=>{
    const c=document.createElement('div');c.className='dec-card';
    c.innerHTML=`<div class="d-id"><span>${d.id} · day ${d.day}</span><span class="stamp ${d.status}">${d.status.toUpperCase()}</span></div>
      <div class="d-act">${d.action}</div><div class="d-hash">#${d.hash} ← ${d.prev.slice(0,8)}</div>`;
    c.onclick=()=>{$$('.dec-card').forEach(x=>x.classList.remove('sel'));c.classList.add('sel');showECN(d)};
    dl.appendChild(c)});
  showECN(S.LEDGER[0]);
  // calibration scatter
  const svg=$('#calib-svg');svg.innerHTML='';
  const ax=axes(svg,400,220,{x:[0,80],y:[0,80],xt:4,yt:4,xl:'predicted bbl/d',yl:'realised bbl/d',padL:38,padB:22,padT:10,padR:8});
  line(svg,[[ax.sx(0),ax.sy(0)],[ax.sx(80),ax.sy(80)]],{stroke:DIM,w:.7,dash:'4 3'});
  const rr=(s=>()=>{s=Math.imul(s+0x6D2B79F5|0^s>>>15,1);return ((s>>>8)/16777216)%1})(3);
  for(let i=0;i<42;i++){const p=18+((i*37)%55);const r=p*(0.86+((i*53)%29)/100);el('circle',{cx:ax.sx(p),cy:ax.sy(r),r:2.6,fill:'none',stroke:BLUE,'stroke-width':1,opacity:.8},svg)}
  $('#calib-note').textContent='P10–P90 coverage: 0.83 (target .80–.90) · vs Baghewala-S held-out wells · SIM';
}
function showECN(d){
  $('#ecn-id').textContent=d.id;
  $('#ecn-body').innerHTML=`
    <div class="ecn-row"><span>Well / time</span><b>BGW-17 · cycle 6 · day ${d.day}</b></div>
    <div class="ecn-row"><span>Action</span><b>${d.action}</b></div>
    <div class="ecn-row"><span>Reason</span><b>${d.why}</b></div>
    <div class="ecn-row"><span>Binding limit</span><b>rod float @ 900 m</b></div>
    <div class="ecn-row"><span>Models</span><b>${d.models}</b></div>
    <div class="ecn-row"><span>Approver</span><b>${d.approver}</b></div>
    <div class="ecn-row"><span>Status</span><b>${d.status.toUpperCase()}</b></div>
    <div class="ecn-row"><span>Outcome score (T+7d)</span><b>${d.score??'—'} ${d.score?'· pred 48.2 → real 46.9 BOPD':''}</b></div>
    <div style="display:flex;gap:8px;margin-top:10px">
      <button class="btn sm" id="ecn-trace">Provenance trace</button>
      <button class="btn sm" id="ecn-replay">Replay in Twin</button></div>`;
  $('#ecn-trace').onclick=()=>modal('PROVENANCE TRACE — '+d.id,`<div style="font-family:IBM Plex Mono;font-size:11px;line-height:1.9">
    plan → joint-optimiser (pymoo NSGA-II→MPC)<br>→ enkf state r12 (N=64)<br>→ inputs: WH-gauge TT-114(EXCLUDED), FL-echo, power-meter<br>→ assumptions: μ(T) anchors ASSUM-07 · emulsion ASSUM-12<br>→ evidence: bench/run-2026-09-27<br>hash ${d.hash} ← ${d.prev}</div>`);
  $('#ecn-replay').onclick=()=>{G.t=d.day;nav('well');toast('Replaying day '+d.day+' state in Twin')};
}
$('#verify-btn')?.addEventListener('click',()=>S.api.verify().then(v=>toast(v.ok?'Ledger chain verified — '+S.LEDGER.length+' entries intact':'TAMPER at '+v.at,v.ok?'ok':'err')));
$('#chain-stamp')?.addEventListener('click',()=>S.api.verify().then(v=>toast(v.ok?'CHAIN VERIFIED ✓':'BROKEN',v.ok?'ok':'err')));

// ---------- IMPACT ----------
let impScope=0,impBase=0;
function renderImpact(){
  const mul=[1,1/30,33/30][impScope], baseF=[1,.7,.55][impBase];
  const econ=[['+₹6.1 L','Δ net value / 180 d','±0.9 · '+['field (30 wells)','per well','×33 illustrative'][impScope]],['+24.6%','incremental oil','CI 95%'],['₹412','lifting cost / bbl','was ₹536 static'],['₹1.9 L','avoided failure cost','workovers + deferred']];
  const env=[['−0.7','Δ SOR (CWE)','3.8 → 3.1'],['−310 t','steam avoided / 180 d','equal oil'],['−21 kg','CO₂e / bbl','CEA grid factor'],['−0.31 m³','fresh water / bbl','Thar framing']];
  const soc=[['−62 h','high-risk states','float / impact / overload'],['−41','site visits / 180 d','heat-stress weighted'],['9','emergency workovers avoided','per field-year'],['38 h','engineer training (Challenge)','simulator hours']];
  const fill=(id,rows)=>{$(id).innerHTML=rows.map(([v,l,b])=>`<div class="hn"><div class="hn-v">${v}<small> ·±</small></div><div class="hn-l">${l}</div><div class="hn-b">${b} · SIM</div></div>`).join('');
    $$(id+' .hn').forEach(h=>h.onclick=()=>modal('HOW COMPUTED','<div style="font-family:IBM Plex Mono;font-size:11px;line-height:1.8">value = mean(Mantle) − mean(baseline), paired over 30 wells × 20 seeds<br>CI: paired bootstrap, B=2000<br>prices: ₹6,150/bbl oil · ₹8.4/m³ gas · ₹9.1/kWh (ASSUM)<br>source: bench/run-official-v3 · SIM</div>'))};
  fill('#imp-econ',econ);fill('#imp-env',env);fill('#imp-soc',soc);
  const svg=$('#impact-chart');svg.innerHTML='';
  const ax=axes(svg,1200,220,{x:[0,180],y:[0,8],xt:9,yt:4,xl:'day',yl:'Δ net ₹L',padL:44,padB:24,padT:10,padR:10});
  const mk=(f,c,dash)=>{const pts=[];for(let d=0;d<=180;d+=3)pts.push([ax.sx(d),ax.sy(7.2*f*(1-Math.exp(-d/55)))]);line(svg,pts,{stroke:c,w:1.6,dash})};
  mk(1,TWIN);mk(.7,GRN,'6 3');mk(.55,'#9a9484','3 3');
  txt(svg,ax.sx(160),ax.sy(7.3),'vs Static',{size:8,fill:TWIN});
  txt(svg,ax.sx(160),ax.sy(5.2),'vs Pump-off',{size:8,fill:GRN});
  txt(svg,ax.sx(160),ax.sy(4.1),'vs Sequential',{size:8,fill:DIM});
}
$('#scope-seg')?.addEventListener('click',e=>{const i=[...e.currentTarget.children].indexOf(e.target);if(i>=0){impScope=i;[...e.currentTarget.children].forEach((b,j)=>b.classList.toggle('on',j===i));renderImpact()}});
$('#base-seg')?.addEventListener('click',e=>{const i=[...e.currentTarget.children].indexOf(e.target);if(i>=0){impBase=i;[...e.currentTarget.children].forEach((b,j)=>b.classList.toggle('on',j===i));renderImpact()}});
$('#receipt-btn')?.addEventListener('click',()=>modal('CYCLE 6 RECEIPT — BGW-17',`<pre style="font-family:IBM Plex Mono;font-size:11.5px;line-height:1.9;background:repeating-linear-gradient(#fff,#fff 22px,#f6f2e8 22px,#f6f2e8 24px);padding:14px">
  MANTLE ENERGY CO. — CYCLE RECEIPT
  ----------------------------------------
  steam (CWE)          870 t    −310 vs base
  fuel (gas)        61,400 m³   −18%
  fresh water           366 m³  −31%
  power              9,640 kWh  −12%
  oil               4,392 bbl   +24.6%
  CO₂e                144 t     −21 kg/bbl
  ----------------------------------------
  net value          ₹6.1 L    coupling +4.1
                        SIM · Baghewala-S</pre>`));

// ---------- PROOF ----------
function renderProof(){
  const g=$('#proof-grid');g.innerHTML='';
  const card=(title,body,btn,fn)=>{const d=document.createElement('div');d.className='plate proof-card';
    d.innerHTML=`<div class="plate-head"><span>${title}</span></div><div class="pc-body">${body}</div><div class="pc-act"><button class="btn sm">${btn}</button></div>`;
    d.querySelector('button').onclick=fn;g.appendChild(d);return d};
  card('SIH26120 TRACEABILITY',`
    ${[['CSS params → joint optimiser','arena'],['SRP reactive → schedule + Shaper','well'],['rod float/impact → margins+cards','well'],['joint optimisation → Coupling Dividend','arena'],['SOR/energy ↓ → Impact','impact'],['real-time → EnKF twin + P10–90','proof'],['7 data categories → canonical schema','proof']].map(([a,b])=>`<div class="trace-line"><span>${a}</span><span class="ok">✓ ${b}</span></div>`).join('')}`,
    '↗ demo each',()=>nav('arena'));
  card('MODEL CARDS',`
    ${[['EnKF state','cov .83','held-out wells'],['card classifier (CNN+GBM)','F1 .91','synthetic cards'],['surrogate (LightGBM)','R² .97','vs physics sim'],['hazard (PPO-eval)','AUC .88','trajectories']].map(([a,b,c])=>`<div class="trace-line"><span>${a}</span><span class="ok">${b} · ${c}</span></div>`).join('')}
    <div class="plate-note" style="margin-top:6px">Metrics vs Baghewala-S simulator, time-ordered split — never field data.</div>`,
    'open model card',()=>modal('MODEL CARD — EnKF','<div style="font-family:IBM Plex Mono;font-size:11px;line-height:1.8">purpose: state estimation T(r,z), fluid level, k<br>data: synthetic SCADA 1Hz→5min<br>split: time-ordered, held-out wells<br>coverage P10–90: 0.83 · innovation χ² ok<br>limits: OOD → advisory downgrade<br>status: SIM only</div>'));
  const prCard=card('DATA PROVENANCE','<div class="donut-row"><svg id="prov-donut" width="90" height="90" viewBox="0 0 90 90"></svg><div class="donut-legend"><i style="background:#2F5BD3"></i>SIM 61%<br><i style="background:#8A6BC9"></i>EST 22%<br><i style="background:#B3362C"></i>ASSUM 11%<br><i style="background:#3F7D4E"></i>PUB 6%</div></div><div class="plate-note">Toggle <b>.</b> to tint numbers by source anywhere.</div>',
    'source registry',()=>modal('SOURCE REGISTRY',`${['Baghewala-S generator v3 (SIM)','OIL public anchors: API 17–19°, μ 10–13k cP (PUB)','ASTM D341 Walther fit (ASSUM)','CEA grid CO₂ factor (PUB)','RP11L card geometry (PUB)'].map(s=>`<div class="trace-line"><span>${s}</span></div>`).join('')}`));
  requestAnimationFrame(()=>{const d=$('#prov-donut');if(d)donut(d,45,45,38,[[.61,TWIN],[.22,'#8A6BC9'],[.11,RED],[.06,GRN]])});
  card('ASSUMPTION REGISTRY',`
    ${[['μ(T) anchors','12k cP @50°C','replace: OIL PVT lab'],['T_ao onset','62 °C','replace: deposition tests'],['emulsion mult.','Richardson','replace: rheology'],['OTSG η','85%','replace: vendor curve'],['workover cost','₹9 L','replace: OIL finance']].map(([a,b,c])=>`<div class="assume-row"><b>${a}</b> · ${b}<div class="a-rep">${c}</div></div>`).join('')}`,
    'full registry',()=>modal('ASSUMPTIONS','<div class="plate-note">Every ASSUM constant ships with a value, a basis and a "replace with…" path. 47 registered.</div>'));
  card('REAL-DATA READINESS',`
    <div style="font-family:IBM Plex Mono;font-size:11px;line-height:2">SCADA → MQTT/OPC-UA → adapter → auditor → twin<br><br>
    <span style="border:1.4px solid #3F7D4E;color:#3F7D4E;padding:2px 8px;border-radius:3px">SIM MODE</span>
    <span style="border:1px solid #8A8A80;color:#8A8A80;padding:2px 8px;border-radius:3px">FIELD MODE 🔒</span></div>
    <div class="plate-note" style="margin-top:8px">Import CSV → auditor runs live (gaps, dupes, unit mismatch, drift).</div>`,
    'import CSV live',()=>importCsv());
  card('TWIN HEALTH','<div class="health-rings"><div id="hr1"></div><div id="hr2"></div><div id="hr3"></div></div><div class="plate-note" style="margin-top:6px">physics≈ML disagreement 3.2% · in-distribution ✓</div>',
    'health detail',()=>modal('TWIN HEALTH','<div class="kv"><span>sensor integrity</span><b>96%</b></div><div class="kv"><span>calibration coverage</span><b>.83</b></div><div class="kv"><span>freshness</span><b>4 s</b></div><div class="kv"><span>in-distribution</span><b>yes</b></div><div class="kv"><span>physics–ML gap</span><b>3.2%</b></div>'));
  requestAnimationFrame(()=>{
    [['#hr1',.96,'sensors'],['#hr2',.83,'calib'],['#hr3',.97,'fresh']].forEach(([id,v,l])=>{
      const host=$(id);if(!host)return;host.className='hring';
      host.innerHTML=`<svg viewBox="0 0 76 76" width="76" height="76"><circle cx="38" cy="38" r="30" fill="none" stroke="rgba(30,42,51,.15)" stroke-width="6"/><circle cx="38" cy="38" r="30" fill="none" stroke="${v>.9?GRN:AMB}" stroke-width="6" stroke-dasharray="${v*188} 188"/></svg><div class="hr-v">${Math.round(v*100)}<span>${l}</span></div>`});
  });
}
function importCsv(){modal('CSV IMPORT — AUDIT',`<div id="aud" style="font-family:IBM Plex Mono;font-size:11px;line-height:2">reading…</div>`);
  const rows=['✓ 14,204 rows · 6 channels','⚠ 312 gaps > 5 min (3.4%)','⚠ 7 impossible values (T<0)','⚠ unit mismatch: psi→bar on P-114','✓ drift check ok','→ flagged rows quarantined, EST coverage maintained'];
  rows.forEach((r,i)=>setTimeout(()=>{const a=$('#aud');if(a)a.innerHTML+='<br>'+r},600*(i+1)))}
$('#import-btn')?.addEventListener('click',importCsv);
$('#golden-btn')?.addEventListener('click',()=>toast('Golden scenarios: 6/6 pass (float, pound, cutoff, sensor-fault, storm, solar)'));

// ---------- PLAY (/play) ----------
let playRuns=0;
$('#play-start')?.addEventListener('click',()=>{
  const spm=+$('#play-spm').value, rd=+$('#play-rd').value;
  const svg=$('#play-chart');svg.innerHTML='';
  const ax=axes(svg,640,260,{x:[0,60],y:[0,70],xt:6,yt:4,xl:'day',yl:'BOPD',padL:38,padB:24,padT:10,padR:8});
  // mantle reference
  const mpts=[];for(let d=0;d<=60;d++)mpts.push([ax.sx(d),ax.sy(S.oilRate(d))]);
  line(svg,mpts,{stroke:TWIN,w:1.6,dash:'6 3'});
  // player's run: spm too high → float events; resteam too late → oil gap
  let failDay=spm>S.nMax(20)? Math.round(20+ (spm-S.nMax(20))*4): -1;
  const upts=[];for(let d=0;d<=60;d++){let q=S.oilRate(d)*(spm>6?1.02:spm<3.5?.82:1);
    if(failDay>0&&d>failDay&&d<failDay+9)q*=.12;
    if(d>rd&&d<rd+14)q*=.55;
    upts.push([ax.sx(d),ax.sy(q)]);}
  line(svg,upts,{stroke:INK,w:1.4});
  if(failDay>0)el('path',{d:`M${ax.sx(failDay)} ${ax.sy(6)} l5 -9 l5 9 Z`,fill:RED},svg);
  const you=upts.reduce((s,p)=>s+(70-p[1]/(ax.sy(0)-ax.sy(1))*1)*0,0); // (unused)
  const youOil=upts.length*  (upts.reduce((s,p)=>s+ (ax.y1-p[1])/(ax.y1-ax.sy(70))*70,0)/upts.length);
  const mOil=mpts.reduce((s,p)=>s+(ax.y1-p[1])/(ax.y1-ax.sy(70))*70,0)/mpts.length;
  const dmg=failDay>0? (spm-S.nMax(20)*0+.4):0;
  playRuns++;
  $('#play-score').innerHTML=`<div>your oil: <b>${Math.round(youOil*6)} bbl</b></div><div>Mantle: <b>${Math.round(mOil*6)} bbl</b></div>
    <div>rod damage: <b class="${dmg?'lose':'win'}">${dmg?failDay?`failure day ${failDay}`:'wear': 'none'}</b></div>
    <div>verdict: <b class="${youOil>=mOil*.97?'win':'lose'}">${youOil>=mOil*.97?'MATCHED MANTLE':'Mantle wins'}</b></div>`;
  const lb=$('#lb-table');if(lb){const names=['Judge A','Judge B','R. Sharma','You'];
    const rows=[['Mantle',Math.round(mOil*6)],['Judge A',Math.round(mOil*5.4)],['R. Sharma',Math.round(mOil*5.7)],['You',Math.round(youOil*6)],['Judge B',Math.round(mOil*4.6)]].sort((a,b)=>b[1]-a[1]);
    lb.innerHTML='<tr><th>#</th><th>pilot</th><th>bbl/60d</th></tr>'+rows.map((r,i)=>`<tr><td>${i+1}</td><td>${r[0]}</td><td>${r[1]}</td></tr>`).join('')}
});
$('#play-spm')?.addEventListener('input',e=>$('#play-spm-v').textContent=e.target.value);
$('#play-rd')?.addEventListener('input',e=>$('#play-rd-v').textContent=e.target.value==='60'?'—':e.target.value);

// ---------- MOBILE card ----------
function renderMobile(){
  const st=simState;const c=2*Math.PI*52;
  $('#m-ring-arc').setAttribute('stroke-dasharray',`${st.margins.float*c} ${c}`);
  $('#m-margin').textContent=(st.margins.float*100).toFixed(0)+'%';
  $('#m-nums').innerHTML=[['oil',st.oilRate.toFixed(0)+' BOPD'],['SPM',st.spm.toFixed(1)],['fluid level',st.fluidLevel.toFixed(0)+' m'],['last decision','SPM→4.9 (D-0412)'],['alerts','2 open']].map(([k,v])=>`<div class="mr"><span>${k}</span><b>${v}</b></div>`).join('');
}
$('#m-ack')?.addEventListener('click',()=>toast('Acknowledged — logged to ledger'));

// ---------- TIMELINE DOCK ----------
function drawTimeline(){
  const svg=$('#tl-svg');const w=svg.clientWidth||800,h=48;svg.setAttribute('viewBox',`0 0 ${w} ${h}`);svg.innerHTML='';
  const x=d=> (d+21)/201*w;
  const bands=[[-21,-7,'INJECTION','#2F8FA8'],[-7,0,'SOAK','#8a8a80'],[0,95,'PRODUCTION','#3F7D4E'],[95,140,'DECLINE','#C98A1B'],[140,154,'INJ 7','#2F8FA8'],[154,160,'SOAK','#8a8a80'],[160,180,'PROD 7','#3F7d4e']];
  bands.forEach(([a,b,n,c])=>{el('rect',{x:x(a),y:18,width:x(b)-x(a),height:16,fill:c,opacity:.22},svg);
    if(x(b)-x(a)>44)txt(svg,(x(a)+x(b))/2,29,n,{size:6.5,anchor:'middle',fill:document.body.dataset.skin==='paper'?'#8A8A80':'rgba(244,241,234,.6)'})});
  // forecast fan
  area(svg,[[x(G.t),8],[x(Math.min(180,G.t+30)),8]],[[x(G.t),44],[x(Math.min(180,G.t+30)),44]],'rgba(91,131,240,.18)',1);
  // pins
  S.LEDGER.slice(0,8).forEach(d=>{el('circle',{cx:x(d.day),cy:14,r:2.2,fill:d.status==='applied'?GRN:AMB},svg)});
  // cut-off window ring
  el('rect',{x:x(95),y:18,width:4,height:16,fill:RED,opacity:.6},svg);
  // now marker
  line(svg,[[x(G.t),4],[x(G.t),46]],{stroke:document.body.dataset.skin==='paper'?INK:'#fff',w:1.4});
  el('path',{d:`M${x(G.t)-4} 2h8l-4 6Z`,fill:document.body.dataset.skin==='paper'?INK:'#fff'},svg);
}
$('#tl-scrub').addEventListener('input',e=>{G.t=+e.target.value;G.playing=false;$('#tl-play').textContent='▶'});
$('#tl-play').onclick=()=>{G.playing=!G.playing;$('#tl-play').textContent=G.playing?'⏸':'▶'};
$('#tl-speed').onchange=e=>G.speed=+e.target.value;
$('#tl-fork').onclick=()=>fork();
function fork(){G.scenario='fork@day'+Math.round(G.t);$('#scen-name').textContent=G.scenario;$('#scenario-ribbon').classList.add('on');toast('Forked scenario at day '+Math.round(G.t)+' — reality ribbon on','warn')}
$('#scen-exit').onclick=()=>{G.scenario=null;$('#scenario-ribbon').classList.remove('on')};

// ---------- CONDITION DECK ----------
function buildDeck(){
  const cols=$('#cd-cols');cols.innerHTML='';
  Object.entries(S.DECK).forEach(([col,opts])=>{
    const c=document.createElement('div');c.className='cd-col';
    c.innerHTML=`<h5>${col}</h5>`+opts.map(([id,t,d,fx])=>`<div class="cd-opt ${col==='Faults'?'fault':''}" data-col="${col}" data-id="${id}"><div class="co-t">${t}</div><div class="co-d">${d}${fx?` · <b>${fx}</b>`:''}</div></div>`).join('');
    cols.appendChild(c)});
  $('#cd-presets').innerHTML='<h5 style="width:100%;font:600 10px IBM Plex Sans Condensed;letter-spacing:1.6px;color:var(--g-dim);margin-bottom:4px">PRESETS</h5>'+S.PRESETS.map(([id,n])=>`<span class="cd-preset ${id===S.COND.preset?'on':''}" data-id="${id}">${n}</span>`).join('');
  $$('.cd-opt').forEach(o=>o.onclick=()=>applyCondition(o.dataset.col,o.dataset.id,o));
  $$('.cd-preset').forEach(p=>p.onclick=()=>applyPreset(p.dataset.id));
}
const condSel={Formation:'jodhpur',Crude:'api17','Climate & time':'dusk','Completion & lift':'vit','Steam source':'gas'};
function recalcFX(){const F=S.COND_FX;
  F.viscosityMul={api19:.7,api17:1,api14:1.4,wc60:1.2,asph:1.05}[condSel.Crude]??1;
  if(condSel.Formation==='carb')F.viscosityMul*=3.2;
  F.injectivityMul={tight:.5,hiperm:1.4}[condSel.Formation]??1;
  if(condSel['Completion & lift']==='bare')F.injectivityMul*=.85;
  F.energyMul=condSel['Climate & time']==='noon'?1.12:1;
  F.co2Mul={gas:1,diesel:1.4,solar:.55,recycle:1}[condSel['Steam source']]??1;
  F.solarShare=condSel['Steam source']==='solar'?.62:0;
}
function applyCondition(col,id,elx){
  if(!builtDeck){buildDeck();builtDeck=true}
  if(elx){$$('.cd-opt[data-col="'+col+'"]').forEach(o=>o.classList.remove('on'));elx.classList.add('on')}
  condSel[col]=id;
  if(col==='Formation')twin.setFormation(id);
  if(col==='Climate & time'){twin.setClimate({noon:'noon',dusk:'dusk',night:'night',storm:'storm',monsoon:'monsoon'}[id]||'dusk');twin.setStorm(id==='storm')}
  if(col==='Steam source')twin.setSteamSource(id);
  if(col==='Faults'){applyFault(id)}
  recalcFX();
  if(elx)$('#cond-name').textContent=elx.querySelector('.co-t').textContent;
  simState=S.state(G.t,S.COND_FX);updateGlass();
  toast('Condition applied — scene + physics updated','ok');
}
function applyFault(id){
  if(id==='f_float'){S.COND_FX.viscosityMul*=1.6;toast('Fault: rod float event — watch bridle slack + impact flash','warn')}
  if(id==='f_pound'){toast('Fault: fluid pound — fillage drops','warn')}
  if(id==='f_temp'){toast('Fault: TT-114 stuck — EnKF flags innovation, sensor excluded (EST)','warn')}
  if(id==='f_drop'){toast('Fault: telemetry dropout — virtual sensors take over','warn')}
  if(id==='f_cool'){toast('Fault: sudden cooling — re-forecast, envelope tightens','warn')}
  if(id==='f_unset'){toast('Fault: pump unsetting — hold-down margin < 1','err')}
}
function applyPreset(id){
  S.COND.preset=id;$$('.cd-preset').forEach(p=>p.classList.toggle('on',p.dataset.id===id));
  if(id==='summer'){applyCondition('Climate & time','noon',$(`.cd-opt[data-id="noon"]`));applyCondition('Crude','api14',$(`.cd-opt[data-id="api14"]`))}
  else if(id==='carbonate'){applyCondition('Formation','carb',$(`.cd-opt[data-id="carb"]`))}
  else if(id==='solarsteam'){applyCondition('Steam source','solar',$(`.cd-opt[data-id="solar"]`))}
  else if(id==='sandstorm'){applyCondition('Climate & time','storm',$(`.cd-opt[data-id="storm"]`));applyFault('f_drop');applyFault('f_temp')}
  else if(id==='barevit'){applyCondition('Completion & lift','bare',$(`.cd-opt[data-id="bare"]`))}
  else{S.COND_FX.viscosityMul=1;S.COND_FX.injectivityMul=1;S.COND_FX.co2Mul=1;S.COND_FX.energyMul=1;S.COND_FX.solarShare=0;
    Object.assign(condSel,{Formation:'jodhpur',Crude:'api17','Climate & time':'dusk','Completion & lift':'vit','Steam source':'gas'});
    twin.setClimate('dusk');twin.setStorm(false);twin.setSteamSource('gas');$('#cond-name').textContent='Thar · Dusk';simState=S.state(G.t,S.COND_FX);updateGlass()}
}
$('#conditions-chip').onclick=()=>{$('#condition-deck').classList.add('open');if(!builtDeck){buildDeck();builtDeck=true;$$('.cd-opt').forEach(o=>{const map={Formation:S.COND.formation,Crude:S.COND.crude,'Climate & time':S.COND.climate,'Completion & lift':S.COND.completion,'Steam source':S.COND.steam};if(o.dataset.id===map[o.dataset.col])o.classList.add('on')})}};
let builtDeck=false;
document.addEventListener('click',e=>{if(e.target.id==='condition-deck'||e.target.dataset?.close==='cd')$('#condition-deck').classList.remove('open')});

// ---------- PALETTE (Ask Mantle) ----------
const COMMANDS=[
  ['Go to Well / Field / Arena / Ledger / Impact / Proof','nav'],
  ['Toggle Blueprint (B)','b'],['Condition Deck (C)','c'],['X-ray (X)','x'],['Fork scenario (F)','f'],
  ['Inject fault: rod float','fault:f_float'],['Inject fault: fluid pound','fault:f_pound'],['Inject fault: telemetry dropout','fault:f_drop'],
  ['Preset: Summer squeeze','preset:summer'],['Preset: Solar steam','preset:solarsteam'],['Preset: Sandstorm','preset:sandstorm'],
  ['Run Story Mode (S)','story'],['Open Judge Challenge','play'],['Provenance tint (.)','prov'],
];
const QA=[
  [/why.*(slow|spm|downstroke|recommend)/i,'Recommendation: SPM 5.4→4.9 with kd 0.62.<br>Drivers: viscosity @900 m <b>1,140 cP</b> (rising), float margin <b>18%</b> trending −2.1%/d.<br>Binding limit: rod float below 900 m. Source: enkf r12 + wave-solver · EST',1],
  [/coupling|dividend|together|joint/i,'Coupling Dividend <b>+₹4.1 L/cycle</b> = V(joint) − V(sequential).<br>Shapley split: CSS +1.6 · SRP +1.2 · interaction +0.9 · Shaper +0.4. That interaction term is the PS thesis.',3],
  [/cut.?off|re.?steam|when/i,'Marginal-value trigger fires ~<b>day 96</b>: Δoil from +100 t steam falls below steam cost.<br>Cost of waiting +7 d: −₹0.9 L. Cost of early start: −₹0.6 L.',4],
  [/heat|battery|temperature|hot/i,'Thermal battery <b>61%</b> — sandface 96 °C, mean heated zone 87 °C, r_h 12.1 m.<br>Days to cut-off ~54. Heat delivered 81% of fuel (VIT on).',4],
  [/rod float|float/i,'Float margin = 1 − (downstroke drag + dynamic) / buoyant weight = <b>18%</b> @900 m.<br>P(float, 7d) = 0.31±.06. Lever: kd↑ via Stroke Shaper lifts N_max without steam.',1],
  [/sor|steam oil/i,'Cycle SOR (CWE) <b>3.4</b>, vs 3.8 static practice. Solar hybrid would cut CO₂/bbl ~45% for daytime injection.',5],
  [/safe|limit|gate/i,'Safety Gate: deterministic — hard limits on float margin, fillage, casing stress, torque. The no-Gate ablation gains +₹0.8 L but is disqualified (14 violations).',3],
];
let palIdx=0,palItems=[];
function openPalette(){$('#palette').classList.add('open');const i=$('#pal-input');i.value='';filterPal('');setTimeout(()=>i.focus(),50)}
$('#palette-btn').onclick=openPalette;
$('#pal-input').addEventListener('input',e=>filterPal(e.target.value));
$('#pal-input').addEventListener('keydown',e=>{
  if(e.key==='ArrowDown'){palIdx=Math.min(palIdx+1,palItems.length-1);paintPal()}
  if(e.key==='ArrowUp'){palIdx=Math.max(palIdx-1,0);paintPal()}
  if(e.key==='Enter'&&palItems[palIdx])palItems[palIdx][2]();
  if(e.key==='Escape')$('#palette').classList.remove('open')});
function filterPal(q){
  palItems=[];
  for(const [re,ans] of QA)if(q&&re.test(q)){palItems.push([q,'answer',()=>palAnswer(ans)]);break}
  for(const [n,c] of COMMANDS)if(!q||n.toLowerCase().includes(q.toLowerCase()))palItems.push([n,'cmd',()=>runCmd(c,n)]);
  palIdx=0;paintPal();
}
function palAnswer(html){$('#pal-list').innerHTML=`<div class="pal-answer">${html}<div class="pa-src">verified numbers from tools · <a onclick="document.getElementById('palette').classList.remove('open')">Show me ↗</a></div></div>`;palItems=[]}
function runCmd(c,n){
  $('#palette').classList.remove('open');
  if(c==='nav')return;if(c==='b')toggleMode();if(c==='c')$('#conditions-chip').click();if(c==='x')toggleXray();
  if(c==='f')fork();if(c==='story')storyToggle();if(c==='play')nav('play');if(c==='prov')toggleProv();
  if(c.startsWith('fault:'))applyFault(c.slice(6));if(c.startsWith('preset:'))applyPreset(c.slice(7));
  toast(n,'ok');
}
function paintPal(){$('#pal-list').innerHTML=palItems.map((it,i)=>`<div class="pal-item ${i===palIdx?'sel':''}"><span>${it[0]}</span><span class="pi-k">${it[1]}</span></div>`).join('');
  $$('#pal-list .pal-item').forEach((d,i)=>d.onclick=()=>palItems[i][2]())}
$('#palette').addEventListener('click',e=>{if(e.target.id==='palette')$('#palette').classList.remove('open')});

// ---------- ALERTS ----------
function renderAlerts(){
  $('#alerts-list').innerHTML=S.ALERTS.map(a=>`<div class="alert-item"><span class="a-pri ${a.pri.toLowerCase()}">${a.pri}</span><div><div class="a-t">${a.t}</div><div class="a-d">${a.d}</div></div></div>`).join('');
  $('#alert-count').textContent=S.ALERTS.length;
}
$('#alerts-btn').onclick=()=>{renderAlerts();$('#alerts-drawer').classList.toggle('open')};
document.addEventListener('click',e=>{if(e.target.dataset?.close==='alerts')$('#alerts-drawer').classList.remove('open')});

// ---------- MODAL ----------
function modal(title,html){$('#modal').innerHTML=`<div class="m-head"><span>${title}</span><button class="sheet-x" id="m-x">✕</button></div><div class="m-body">${html}</div>`;
  $('#modal-wrap').classList.add('open');$('#m-x').onclick=closeModal}
function closeModal(){$('#modal-wrap').classList.remove('open')}
$('#modal-wrap').addEventListener('click',e=>{if(e.target.id==='modal-wrap')closeModal()});

// ---------- MODE: Twin ⇄ Blueprint ----------
const bpState={on:false};
function applyTP(p){ // p:0 twin → 1 blueprint — parametric, fully reversible
  G.tp=p;
  const camSeg=clamp((p-.05)/.42,0,1), zoomSeg=clamp((p-.32)/.42,0,1),
        flatSeg=clamp((p-.5)/.38,0,1), wipeSeg=clamp((p-.58)/.34,0,1), bpSeg=clamp((p-.76)/.2,0,1);
  twin.cam.auto=p<0.04;
  // orbit to a true side elevation (looking -Z): unit profile left, cut section right
  twin.cam.azT=lerp(.62,Math.PI/2-.015,easeIO(camSeg));
  twin.cam.elT=lerp(.26,.05,easeIO(camSeg));
  twin.cam.txT=lerp(-2,-3.5,easeIO(camSeg));
  twin.cam.tyT=lerp(-14,-12.5,easeIO(camSeg));
  twin.cam.tzT=lerp(0,2,easeIO(camSeg));
  // dolly-zoom → near-orthographic; end framing ~50 units tall so the slab fills the sheet
  const fov=lerp(38,2.6,easeIO(zoomSeg));
  twin.cam.fovT=fov;
  twin.cam.distT=lerp(92,72,easeIO(camSeg))*Math.tan(19*Math.PI/180)/Math.tan(fov/2*Math.PI/180);
  twin.drain(easeIO(zoomSeg));       // colour → paper, ink edges emerge
  twin.flatten(flatSeg);             // depth collapses: the world becomes the drawing
  // ui retract
  $('#glass-stack').classList.toggle('away',p>.03);
  $('#lens-bar').style.opacity=clamp(1-(p-.06)/.07,0,1);$('#lens-bar').style.pointerEvents=p<.06?'':'none';
  // paper wipe expanding from the wellhead's live screen position
  const pw=$('#paper-wipe');pw.classList.toggle('wiping',wipeSeg>0);
  const wh=twin.anchorScreen('wellhead');
  const ox=wh&&!wh.behind?wh.x/innerWidth*100:38, oy=wh&&!wh.behind?wh.y/innerHeight*100:42;
  pw.style.clipPath=`circle(${easeOut(wipeSeg)*140}% at ${ox}% ${oy}%)`;
  // blueprint sheet fades in over the paper — plates draw on with a cascade
  const bpOn=bpSeg>0;
  if(bpOn!==bpState.on){bpState.on=bpOn;bpView.classList.toggle('on',bpOn);if(bpOn)bp.drawOn()}
  if(bpState.on)bpView.style.opacity=clamp(bpSeg*1.5,0,1);
  document.body.dataset.mode=bpSeg>.6?'blueprint':'twin';
  if(G.screen==='well')document.body.dataset.skin=bpSeg>.4?'paper':'glass';
  $('#mode-toggle [data-mode="twin"]').classList.toggle('on',!bpState.on);
  $('#mode-toggle [data-mode="blueprint"]').classList.toggle('on',bpState.on);
}
let tpAnim=null;
function toggleMode(){
  if(G.screen!=='well')return;
  const target=bpState.on||G.tp>.5?0:1;
  G.tpT=target;
  history.replaceState(null,'','#/well'+(target?'/bp':''));
  const from=G.tp,dur=2200*Math.abs(target-from);
  const t0=performance.now();
  if(tpAnim)cancelAnimationFrame(tpAnim);
  function f(){
    const p=Math.min(1,(performance.now()-t0)/dur);
    applyTP(lerp(from,target,easeIO(p)));
    if(p<1)tpAnim=requestAnimationFrame(f);else{tpAnim=null;if(!bpState.on)document.body.dataset.skin='glass'}
  }
  tpAnim=requestAnimationFrame(f);
}
$('#mode-toggle').addEventListener('click',e=>{if(e.target.dataset.mode)toggleMode()});

// ---------- X-RAY / LENS ----------
function toggleXray(){twin.setXray(!twin.xray);$('#xray-btn').classList.toggle('on',twin.xray)}
$('#xray-btn').onclick=toggleXray;
$$('.lens[data-lens]').forEach(b=>b.onclick=()=>{$$('.lens[data-lens]').forEach(x=>x.classList.remove('on'));b.classList.add('on');twin.setLens(b.dataset.lens)});

// ---------- STORY MODE ----------
const BEATS=[
  ['The well: BGW-17, a CSS heavy-oil well mid-cycle',()=>{nav('well')}],
  ['Thermal lens — the heat you cannot see',()=>{twin.setLens('thermal');$$('.lens').forEach(x=>x.classList.toggle('on',x.dataset.lens==='thermal'))}],
  ['The rods are a 1.1 km spring — mechanical lens',()=>{twin.setLens('mech');$$('.lens').forEach(x=>x.classList.toggle('on',x.dataset.lens==='mech'))}],
  ['Risk lens: float margin is shrinking',()=>{twin.setLens('risk');$$('.lens').forEach(x=>x.classList.toggle('on',x.dataset.lens==='risk'))}],
  ['The same well as an engineering drawing (B)',()=>{twin.setLens('physical');toggleMode()}],
  ['The evidence: 9 strategies race',()=>{toggleMode();nav('arena')}],
  ['Coupling Dividend: joint beats silo by ₹4.1 L',()=>{}],
  ['Proof: every number has a source',()=>nav('proof')],
];
function storyToggle(){
  if(G.story<0){G.story=0;$('#story-mode').classList.add('on');BEATS[0][1]()}
  else{G.story=-1;$('#story-mode').classList.remove('on')}
  paintBeat();
}
function paintBeat(){if(G.story>=0)$('#story-beat').textContent=`${G.story+1}/${BEATS.length} · ${BEATS[G.story][0]}`}
function storyNext(){if(G.story<0)return;G.story=(G.story+1)%BEATS.length;BEATS[G.story][1]();paintBeat()}

// ---------- keyboard ----------
document.addEventListener('keydown',e=>{
  if(e.target.tagName==='INPUT'||e.target.tagName==='SELECT')return;
  const k=e.key.toLowerCase();
  if((e.metaKey||e.ctrlKey)&&k==='k'){e.preventDefault();openPalette();return}
  if(e.key==='Escape'){$('#palette').classList.remove('open');$('#condition-deck').classList.remove('open');$('#alerts-drawer').classList.remove('open');$('#inspect-sheet').classList.remove('open');closeModal();return}
  const scr={1:'well',2:'field',3:'arena',4:'ledger',5:'impact',6:'proof'}[k];if(scr){nav(scr);return}
  if(k==='b')toggleMode();if(k==='c')$('#conditions-chip').click();if(k==='x'&&G.screen==='well')toggleXray();
  if(k===' '){e.preventDefault();$('#tl-play').click()}if(k==='f')fork();if(k==='s')storyToggle();
  if(k==='arrowright')storyNext()|| (G.t=Math.min(180,G.t+1));
  if(k==='arrowleft')G.t=Math.max(-21,G.t-1);
  if(k==='l'&&G.screen==='well'){const lenses=['physical','thermal','mech','flow','pressure','risk'];const cur=lenses.indexOf(twin.lens);const nx=lenses[(cur+1)%6];twin.setLens(nx);$$('.lens[data-lens]').forEach(x=>x.classList.toggle('on',x.dataset.lens===nx))}
  if(k==='.')toggleProv();
  if(k==='?')modal('KEYBOARD',`<div class="kv"><span>1–6 screens</span><b>navigate</b></div><div class="kv"><span>B</span><b>Twin ⇄ Blueprint</b></div><div class="kv"><span>C</span><b>Condition Deck</b></div><div class="kv"><span>⌘K</span><b>Ask Mantle</b></div><div class="kv"><span>Space</span><b>play/pause time</b></div><div class="kv"><span>←→</span><b>step / story</b></div><div class="kv"><span>L</span><b>cycle lens</b></div><div class="kv"><span>X</span><b>x-ray</b></div><div class="kv"><span>F</span><b>fork</b></div><div class="kv"><span>S</span><b>story mode</b></div><div class="kv"><span>.</span><b>provenance tint</b></div>`);
});
function toggleProv(){G.prov=!G.prov;document.body.classList.toggle('show-prov',G.prov);toast(G.prov?'Provenance tint on':'Provenance tint off')}

// ---------- persona ----------
const PERSONAS=['OP','EN','MG','VW'];
$('#persona-btn').onclick=()=>{G.persona=PERSONAS[(PERSONAS.indexOf(G.persona)+1)%4];$('#persona-btn').textContent=G.persona;toast('Persona: '+{OP:'Operator',EN:'Engineer',MG:'Manager',VW:'Viewer'}[G.persona])};
$('#well-context').onclick=()=>{modal('SWITCH WELL',`<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:6px">${S.WELLS.map(w=>`<button class="btn sm" data-w="${w.id}">${w.id.replace('BGW-','')}</button>`).join('')}</div>`);
  $$('#modal [data-w]').forEach(b=>b.onclick=()=>{closeModal();$('#well-context .wc-name').textContent=b.dataset.w;})};

// ---------- recommendation actions ----------
$('#rec-approve').onclick=()=>{toast('Applied (sim) — ledger entry D-0413 sealed','ok');$('#rec-title').textContent='Applied (sim)'};
$('#rec-modify').onclick=()=>{modal('MODIFY PLAN',`<div class="kv"><span>SPM</span><b><input type="range" min="2" max="9" step=".1" value="4.9" id="mod-spm"> <span id="mod-spm-v" class="mono">4.9</span></b></div><div class="kv"><span>kd</span><b><input type="range" min=".5" max=".7" step=".01" value=".62" id="mod-kd"> <span id="mod-kd-v" class="mono">0.62</span></b></div><div style="margin-top:10px"><button class="btn primary sm" id="mod-ok">Approve modified</button></div>`);
  $('#mod-spm').oninput=e=>$('#mod-spm-v').textContent=e.target.value;
  $('#mod-kd').oninput=e=>$('#mod-kd-v').textContent=e.target.value;
  $('#mod-ok').onclick=()=>{closeModal();toast('Modified plan approved — ledger sealed','ok')}};
$('#rec-why').onclick=()=>openExplain('float');

// ---------- intro ----------
function playIntro(){
  const svg=$('#intro-svg');
  // a little self-drawing beam unit line-art
  const paths=[
    'M40 160 h220','M150 160 v-30','M120 40 l30 120 M180 40 l-30 120','M120 40 h60',
    'M120 40 L200 30 M200 30 a14 14 0 0 1 10 18','M100 160 v-34 a16 16 0 0 1 32 0 v34',
    'M116 126 a16 16 0 1 1 .1 0','M210 48 v96','M204 44 h12 v6 h-12z',
    'M40 160 q40 -10 80 0 q40 10 80 0','M30 168 h240'];
  let d=0;
  paths.forEach((p,i)=>{const pe=el('path',{d:p,fill:'none',stroke:'#5B83F0','stroke-width':1.4,'stroke-linecap':'round'},svg);
    const len=pe.getTotalLength();pe.style.strokeDasharray=len;pe.style.strokeDashoffset=len;
    setTimeout(()=>{pe.style.transition=`stroke-dashoffset .7s cubic-bezier(.2,.7,.1,1)`;pe.style.strokeDashoffset=0},200+i*160)});
  setTimeout(()=>{$('#intro-sub').textContent='→ THE DRAWING COMES ALIVE'},2200);
  setTimeout(()=>{$('#intro').classList.add('done')},2900);
  setTimeout(()=>{$('#intro').remove()},3600);
}

// ---------- MAIN LOOP ----------
let frameCount=0, lastPhase='PRODUCTION';
(function loop(now){requestAnimationFrame(loop);now=now||performance.now();
  const dt=Math.min(.1,(now-(loop.last||now))/1000);loop.last=now;
  if(G.playing){G.t+=dt*G.speed/24;$('#tl-scrub').value=G.t;if(G.t>180)G.t=-21}
  simState=S.state(G.t,S.COND_FX);
  if(G.screen==='well'){
    twin.frame(dt,simState,G.playing?G.speed:1);
    if(simState.phase!==lastPhase){lastPhase=simState.phase;buildCallouts()}
    layoutCallouts();
    if(bpState.on||G.tp>.9)bp.update(simState,twin.crankTheta,(now/1000*simState.spm/60)%1);
    // depth gauge appears when diving close
    $('#depth-gauge').classList.toggle('show',twin.cam.dist<26);
    const dfrac=clamp(-twin.cam.ty/55,0,1);
    $('#dg-fill').style.height=(dfrac*100)+'%';$('#dg-marker').style.top=(dfrac*280-1)+'px';
    $('#dg-read').textContent=Math.round(Math.max(0,1200*dfrac))+' m';
  }
  if(frameCount++%20===0){updateGlass();drawTimeline()}
})();

// ---------- boot ----------
buildRiskBars();buildCallouts();updateGlass();renderAlerts();drawTimeline();
nav(location.hash.replace('#/','').split('/')[0] in ROUTES?location.hash.replace('#/','').split('/')[0]:'well');
playIntro();
window.addEventListener('resize',drawTimeline);
