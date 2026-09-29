// ============================================================
// Mantle demo — mock backend ("Baghewala-S" synthetic field)
// Mimics the §19 API surface; deterministic via seeded RNG.
// ============================================================

function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function fnv(str){let h=0x811c9dc5;for(let i=0;i<str.length;i++){h^=str.charCodeAt(i);h=Math.imul(h,0x01000193)}return('0000000'+ (h>>>0).toString(16)).slice(-8)}

const R = mulberry32(20260929);
const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
const lerp=(a,b,t)=>a+(b-a)*t;

// ---------- fluid / thermal physics (simplified, plausible) ----------
const WAL_A=11.569, WAL_B=4.371;                       // Walther fit: μ(48°C)=12000cP, μ(160°C)=12cP
export function viscosity(Tc){const Tk=Tc+273.15;const v=Math.pow(10,Math.pow(10,WAL_A-WAL_B*Math.log10(Tk)))-0.7;return clamp(v,1,20000)}
export function sandfaceT(t){ // °C vs production day (incl. inj/soak for t<0)
  if(t<-7) return lerp(48,162,(t+21)/14);              // injection ramp
  if(t<0)  return 162-4*(-t/7);                        // soak: slight core cooling
  return 48+112*Math.exp(-t/50);                       // production decay
}
export function heatedRadius(t){ // m — Marx–Langenheim-ish growth then shrink
  const grown=13.5*(1-Math.exp(-(t+21)/9));
  return t<0?grown: grown*Math.exp(-t/260)+1.2;
}
export function oilRate(t){ // BOPD — peaks ~62 right after soak, declines as μ climbs
  if(t<0) return 0;
  const mu=viscosity(sandfaceT(t));
  const q=Math.min(62, 46*Math.pow(200/mu,0.45))*Math.exp(-t/260);
  return clamp(q,4,80);
}
export function nMax(t){ // safe SPM ceiling — the chart that explains the PS
  const mu=viscosity(sandfaceT(Math.max(0,t)));
  return clamp(2.53*Math.pow(2000/mu,0.28),2.2,9);
}
export function fluidLevel(t){return t<0?1180:clamp(1150-640*(1-Math.exp(-t/26))+0.2*t,560,1180)} // m from surface (down)
export function fillage(t){return t<0?0:clamp(0.55+0.38*Math.exp(-t/38)-t*0.0011,0.4,0.97)}

const COND={formation:'jodhpur',crude:'api17',climate:'dusk',completion:'vit',steam:'gas',faults:[],preset:'golden'};
const COND_FX={ // physics modifiers per condition
  viscosityMul:1, injectivityMul:1, energyMul:1, co2Mul:1, telemetry:true, solarShare:0,
};

function state(t,cond=COND_FX){
  const T=sandfaceT(t), mu=viscosity(T)*cond.viscosityMul;
  const spm = t<0?0:clamp(4.9+0.9*Math.exp(-t/60),2,9)* (t>110?0.85:1);   // mantle schedule ~
  const q = oilRate(t)*cond.injectivityMul*(t<0?0:1);
  const fill=fillage(t);
  // rod float margin: drag vs buoyant weight — falls as μ climbs and SPM rises
  const drag = 0.111*Math.sqrt(mu)*spm*(1+0.15*Math.sin(t*0.5));
  const floatM = clamp(1-drag/9.4, -0.3, 1);
  const poundM = clamp((fill-0.62)/0.3,0,1);
  const unsetM = clamp(1.4-0.008*t-mu*0.00002,0,1.4);
  const fatigue = clamp(1-(0.35+t*0.0035+ (spm>6?(spm-6)*0.12:0)),0,1);
  const casing = clamp(1-(T-48)/140*0.9,0,1);
  const deposition = clamp(1-((T-62)/30),0,1); // asphaltene band grows as T falls
  const battery = clamp((T-48)/112,0,1);
  const batDays = t<0? 60 : Math.max(0,Math.round(-50*Math.log(0.30)-t)); // days till battery hits 30%
  const pprl = 34+0.28*mu*spm/10+ (t<0?0: 8*(1-fill));
  const mprl = 11+0.10*mu*spm/10;
  return {
    t, phase: t<-7?'INJECTION':t<0?'SOAK':(t<95?'PRODUCTION':'DECLINE'),
    sandfaceT:T, viscosity:mu, oilRate:q, waterCut:22,
    spm, stroke:120, kd:0.58, torquePct:clamp(52+spm*4.2,0,98), powerKw:8+spm*2.1, freqHz:20+spm*4.1,
    fluidLevel:fluidLevel(t), submergence:Math.max(0,1150-fluidLevel(t)- 60), fillage:fill,
    pprl, mprl, heatedR:heatedRadius(t), heatedTavg:48+(T-48)*0.62,
    margins:{float:floatM,pound:poundM,unsetting:clamp(unsetM,0,1),fatigue,casing,deposition},
    floatDays: floatM<=0?0:Math.round(floatM/0.021),
    sor: 3.1+0.006*t, kwhBbl: 9.4+0.05*t*(cond.energyMul), co2Bbl: Math.round((84+0.5*t)*cond.co2Mul),
    waterBbl: 0.42, netRsDay: Math.round(q*6150-8200-spm*900),
    coupling: {rs:4.1, oil:6.8, dsor:-0.4},
    battery, batDays:clamp(batDays,0,99), nMax:nMax(t),
    pwp: 38+ 6*Math.exp(-t/40), whT: Math.max(34, T-38), steamRate: t<-7? 62:0, whp: t<-7? 11.5:2.2,
    steamCum: t<-7? Math.round(62*(t+21)):870, steamTgt:900,
    casingStress: clamp((T-48)/114*62,0,99), solar:cond.solarShare,
  };
}

function forecast(t0,horizon=30){
  const p50=[],p10=[],p90=[],ghost=[];
  for(let d=0;d<=horizon;d++){
    const q=oilRate(t0+d);
    p50.push(q); p10.push(q*0.86); p90.push(q*1.1);
    ghost.push(oilRate(t0+d)*(1-0.003*d)); // do-nothing drifts lower
  }
  return {p50,p10,p90,ghost};
}

// ---------- field (30 synthetic wells) ----------
const WELLS=(()=>{const w=[];const padPos=[[70,70],[300,60],[540,80],[710,70],[140,220],[380,190],[640,220],[90,360],[330,350],[580,370],[740,340]];
  const phases=['PRODUCTION','PRODUCTION','PRODUCTION','DECLINE','INJECTION','SOAK','PRODUCTION','PRODUCTION','DECLINE','PRODUCTION','PRODUCTION'];
  let i=0;
  for(let p=0;p<11;p++)for(let k=0;k<3&&i<30;k++){
    const id='BGW-'+String(i+1).padStart(2,'0');
    const day=10+Math.floor(R()*80), cyc=2+Math.floor(R()*6);
    const T=sandfaceT(day), margin=clamp(0.1+R()*0.7+(R()<0.12?-0.15:0),-0.1,1);
    w.push({id,pad:p+1,x:padPos[p][0]+28+ ((k%2)*46)+(R()*14-7),y:padPos[p][1]+20+Math.floor(k/2)*40+(R()*12-6),
      phase:i===16?'INJECTION':phases[(i*7)%phases.length],day,cycle:cyc,
      oil:Math.round(oilRate(day)*(0.7+R()*0.6)),margin,T:Math.round(T),spm:+(3.5+R()*3).toFixed(1),
      cutoffIn:Math.round(clamp((margin)*90+20,2,90)),opp:Math.round(R()*42+4),
      sor:+(2.4+R()*2.2).toFixed(1)});
    i++;}
  return w;})();

// ---------- arena ----------
const STRATS=[
  {id:'S8',name:'Oracle',color:'#8a8a80',dash:'4 3'},
  {id:'S7',name:'Mantle (joint MPC)',color:'#2F5BD3',bold:true},
  {id:'S6',name:'Shielded RL (PPO)',color:'#8A6BC9'},
  {id:'S5',name:'Sequential optimum',color:'#2F8FA8'},
  {id:'S4',name:'Greedy',color:'#B3362C'},
  {id:'S3',name:'Pump-off ctrl',color:'#3F7D4E'},
  {id:'S2',name:'Heuristic playbook',color:'#C98A1B'},
  {id:'S1',name:'Tuned static',color:'#6B8E6B'},
  {id:'S0',name:'Static (practice)',color:'#9a9484'},
];
function arenaCurve(sid,days=360){ // characteristic curve per strategy over 3 cycles
  const st={S8:[64,.0068,0],S7:[61,.0072,0],S6:[58,.0078,0],S5:[57,.0082,0],S4:[66,.011,0],S3:[52,.0088,0],S2:[50,.0092,0],S1:[51,.0096,0],S0:[48,.0102,0]}[sid];
  const cycLen=120, out=[]; let fail={S4:[58,172,290],S0:[212],S2:[250],S1:[180]}[sid]||[];
  for(let d=0;d<days;d++){
    const cd=d%cycLen; let q;
    if(cd<20){q=st[0]*(cd/20)*(sid==='S4'?1.06:1);} // soak+early
    else q=st[0]*Math.exp(-(cd-20)*st[1])*(sid==='S4'&&cd<50?1.08:1);
    if(fail.includes(d)){q=0;} // failure marker day
    const prevFail=fail.filter(f=>d>f&&d<f+12).length; if(prevFail) q*=0.15; // downtime
    if(sid==='S4'&&cd>80)q*=0.55; // greedy burns the well
    out.push(+clamp(q,0,80).toFixed(1));
  }
  return out;
}
const SCORE=[
  // name, Δoil%, Δ₹L, SORΔ, failures, %oracle, winrate
  ['S8 Oracle','+38.2 ±3.1','+9.8 ±1.2','−0.9','0.0','100','—'],
  ['S7 Mantle','+24.6 ±2.4','+6.1 ±0.9','−0.7','0.1','91.4','84%'],
  ['S6 RL (PPO)','+19.8 ±3.0','+4.7 ±1.1','−0.5','0.4','85.2','71%'],
  ['S5 Sequential','+14.1 ±2.6','+2.0 ±0.8','−0.3','0.3','79.8','62%'],
  ['S4 Greedy','+3.2 ±4.4','−1.8 ±1.4','+0.4','3.8','61.0','41%'],
  ['S3 Pump-off','+9.6 ±2.2','+1.4 ±0.7','−0.4','0.6','74.1','55%'],
  ['S2 Heuristic','+7.8 ±2.5','+1.1 ±0.8','−0.2','0.9','71.3','52%'],
  ['S1 Tuned static','+4.4 ±1.9','+0.5 ±0.6','−0.1','1.2','68.6','47%'],
  ['S0 Static','0','0','0','1.6','66.0','—'],
];

// ---------- ledger ----------
function buildLedger(){
  const acts=[
    ['D-0412','Slow downstroke to 4.9 SPM','applied','float margin −9%→+18%', 41],
    ['D-0407','Advance re-steam window to day 96','pending','cut-off economics', 40],
    ['D-0398','kd 0.55→0.62 via Stroke Shaper','applied','float margin +6%', 38],
    ['D-0391','Hold SPM 5.4 through T dip','applied','net +₹1.9k/d vs cut', 33],
    ['D-0385','Exclude drifting T-sensor TT-114','applied','EnKF innovation 4.1σ', 29],
    ['D-0379','Reduce SPM 5.6→5.1 (pound risk)','applied','fillage 64%→78%', 24],
    ['D-0371','Reject early re-steam (day 78)','rejected','marginal steam < cost', 19],
    ['D-0364','Stroke 120→144 in equivalent','applied','SPM −0.6 same PD', 15],
    ['D-0357','Start production after 6 d soak','applied','vs 4 d practice', 0],
    ['D-0349','Steam slug 870 t @ 62 t/d','applied','joint optimum w/ SRP plan', -7],
  ];
  let prev='GENESIS';
  const list=[...acts].reverse().map(a=>{const h=fnv(prev+a[0]+a[1]); const s={id:a[0],action:a[1],status:a[2],why:a[3],day:a[4],hash:h,prev,approver:a[2]==='applied'?'eng. R. Sharma':'—',
    models:'twin v1.4 · enkf r12 · opt pymoo-0.6', score:a[2]==='applied'?+(0.72+R()*0.25).toFixed(2):null};
    prev=h; return s;});
  return list.reverse();
}
const LEDGER=buildLedger();

// ---------- alerts ----------
const ALERTS=[
  {pri:'P1',t:'Rod float margin 18% · falling',d:'BGW-17 · downstroke drag nearing buoyant weight below 900 m',day:41},
  {pri:'P2',t:'Forecast: fillage < 70% in ~9 d',d:'BGW-17 · fluid pound risk; pump-off timer candidate',day:41},
  {pri:'P3',t:'TT-114 sensor drift excluded',d:'BGW-17 · EnKF innovation 4.1σ; EST values shown',day:40},
  {pri:'P3',t:'BGW-12 tracking BGW-04 pre-failure path',d:'similarity 0.87 · float margin falling',day:41},
  {pri:'P2',t:'Generator 2 slot conflict day 47–49',d:'steam schedule · 3 wells in window',day:41},
];

// ---------- condition deck ----------
const DECK={
  Formation:[['jodhpur','Jodhpur Ss · clean','k≈800 mD · φ .22','baseline'],['tight','Jodhpur Ss · shaly','k≈150 mD · steep decline','inj ×0.5'],['hiperm','High-perm channel','k≈2000 mD · breakthrough risk',''],['carb','Upper carbonate','38,000 cP · fractured','μ ×3.2'],['sand','Sand-prone','plunger wear ↑','']],
  Crude:[['api19','API 19°','μ₅₀ ≈ 8,000 cP','μ ×0.7'],['api17','API 17–18°','μ₅₀ ≈ 11,000 cP','baseline'],['api14','API 14°','μ₅₀ ≈ 15,000 cP','μ ×1.4'],['wc60','Water cut 60%','emulsion viscosity ↑','μ ×1.2'],['asph','High asphaltene','deposition band ↑','']],
  'Climate & time':[['noon','Summer noon 48 °C','heat haze · motor derate',''],['dusk','Late-Oct dusk','golden hour · nominal','baseline'],['night','Winter night 4 °C','flowline cooling ↑',''],['storm','Sandstorm (andhi)','telemetry loss demo',''],['monsoon','Monsoon shower','access delays','']],
  'Completion & lift':[['vit','VIT tubing','low wellbore loss','baseline'],['bare','Bare tubing','steam quality ↓ at depth','heat ×0.8'],['hyd','Hydraulic long-stroke','SPM ↓ same PD',''],['rodB','Rod design B','heavier string',''],['novfd','No VFD','Stroke Shaper off','']],
  'Steam source':[['gas','Gas-fired OTSG','η 85% · CO₂ baseline','baseline'],['diesel','Crude-fired','CO₂/t ↑ 40%','co₂ ×1.4'],['solar','Solar + gas hybrid','day steam solar · CO₂/bbl ↓','co₂ ×0.55'],['recycle','+ Water recycling','fresh water/bbl ↓','']],
  Faults:[['f_temp','T sensor stuck','EnKF should catch it','fault'],['f_cool','Sudden cooling','re-forecast · tighten envelope','fault'],['f_float','Rod float event','P1 · card dx','fault'],['f_pound','Fluid pound','fillage < 70%','fault'],['f_unset','Pump unsetting','hold-down margin < 1','fault'],['f_drop','Telemetry dropout','virtual sensors → EST','fault']],
};
const PRESETS=[['golden','Golden-hour baseline'],['summer','Summer squeeze'],['carbonate','The carbonate problem'],['solarsteam','Sun-powered steam'],['sandstorm','Night of the sandstorm'],['barevit','Bare tubing vs VIT']];

// provenance tags for numbers
export const PROV={meas:'MEAS',est:'EST',sim:'SIM',assum:'ASSUM',pub:'PUB'};

// ---------- API shim (mirrors §19 shapes, ~80ms latency) ----------
const delay=(ms=60+Math.random()*60)=>new Promise(r=>setTimeout(r,ms));
export const api={
  async wellState(id,t){await delay(30);return state(t)},
  async forecast(id,t,h){await delay();return forecast(t,h)},
  async fieldSummary(){await delay();return {bopd:Math.round(WELLS.reduce((s,w)=>s+w.oil,0)),sor:3.4,kwh:11.2,co2:96,wells:WELLS.length,alarms:ALERTS.length}},
  async fieldTriage(){await delay();return [...WELLS].sort((a,b)=>b.opp*(1.6-b.margin)-a.opp*(1.6-a.margin)).slice(0,5)},
  async arenaSeries(){await delay();return Object.fromEntries(STRATS.map(s=>[s.id,arenaCurve(s.id)]))},
  async scoreboard(){await delay();return SCORE},
  async decisions(){await delay(20);return LEDGER},
  async alerts(){await delay(20);return ALERTS},
  async verify(){await delay(200);let prev='GENESIS';for(const d of [...LEDGER].reverse()){if(fnv(prev+d.id+d.action)!==d.hash)return{ok:false,at:d.id};prev=d.hash}return{ok:true}},
};
export {state,forecast,WELLS,STRATS,SCORE,LEDGER,ALERTS,DECK,PRESETS,COND,COND_FX,arenaCurve,clamp,lerp,fnv};
