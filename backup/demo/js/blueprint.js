// ============================================================
// Mantle demo — Blueprint sheet (Paper skin). SVG line-art of
// the same well: elevation, depth tracks, plates 2–6, BOM, notes.
// ============================================================
import { el, INK, BLUE, RED, AMB, GRN, DIM, TWIN, axes, line, txt, path, hatchPattern, dynoCard } from './charts.js';
import { sandfaceT, heatedRadius, viscosity, nMax, fluidLevel, fillage, oilRate, clamp, lerp } from './sim.js';

const DP=[[0,0],[30,40],[1050,560],[1200,740]]; // schematic depth → px
const d2y=d=>{for(let i=1;i<DP.length;i++)if(d<=DP[i][0]){const[a,A]=DP[i-1],[b,B]=DP[i];return A+(d-a)/(b-a)*(B-A)}return 740};

// schematic four-bar (side elevation, sheet coords)
const S={x:118,y:52},LF=74,LR=58,CR={x:44,y:150},CRR=22;
const LP=Math.hypot(S.x-LR-CR.x,S.y-(CR.y+CRR));
let bAng=0;
function solve(theta){const px=CR.x+CRR*Math.cos(theta),py=CR.y+CRR*Math.sin(theta);let b=bAng;
  for(let i=0;i<10;i++){const ex=S.x-LR*Math.cos(b),ey=S.y-LR*Math.sin(b);const dx=ex-px,dy=ey-py;
    const f=dx*dx+dy*dy-LP*LP,df=2*dx*LR*Math.sin(b)-2*dy*LR*Math.cos(b);const nb=b-f/df;if(Math.abs(nb-b)<1e-7){b=nb;break}b=nb}
  bAng=b;return b}

export function buildBlueprint(container){
  const W=1440,H=810;
  const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,preserveAspectRatio:'xMidYMid meet'},container);
  const defs=el('defs',{},svg);
  hatchPattern(defs,'h-red',RED); hatchPattern(defs,'h-ink',INK,45,4); hatchPattern(defs,'h-blue',BLUE,-45,6);
  hatchPattern(defs,'h-sand','#9a7b45',0,7); hatchPattern(defs,'h-brick',BLUE,0,8);
  const sheet=el('g',{},svg);
  el('rect',{x:10,y:10,width:W-20,height:H-20,class:'bp-plate'},sheet);
  el('rect',{x:16,y:16,width:W-32,height:H-32,class:'bp-inner'},sheet);

  // ---------- PLATE 1 · elevation ----------
  const P1={x:30,y:34,w:560,h:700};
  const p1=el('g',{class:'bp-slide'},sheet);
  el('rect',{x:P1.x,y:P1.y,width:P1.w,height:P1.h,class:'bp-plate'},p1);
  el('rect',{x:P1.x+4,y:P1.y+4,width:P1.w-8,height:P1.h-8,class:'bp-inner'},p1);
  txt(p1,P1.x+12,P1.y+18,'PLATE 1 · ELEVATION & SECTION — BGW-17 · CYCLE 6',{size:9,fill:INK,weight:600});
  // strata bands (section on right half of plate)
  const SX=P1.x+280, SW=200; // section x-range
  const bands=[[0,40,'AEOLIAN SAND','h-sand'],[40,250,'TERTIARY SEDS','h-ink'],[250,700,'NAGAUR SS','h-brick'],[700,1050,'BILARA CARB (CAP)','h-dash'],[1050,1100,'UPPER CARB','h-ink'],[1100,1150,'JODHPUR SS — PAY','h-sand'],[1150,1200,'BASEMENT','h-ink']];
  bands.forEach(([a,b,name,pat],i)=>{
    const y1=d2y(a),y2=d2y(b);
    const r=el('rect',{x:SX,y:y1+P1.y+24,width:SW,height:y2-y1,fill:i%2?'rgba(31,78,121,.05)':'rgba(30,42,51,.04)',stroke:INK,'stroke-width':.5},p1);
    if(pat==='h-dash'){el('rect',{x:SX,y:y1+P1.y+24,width:SW,height:y2-y1,fill:'url(#h-blue)',opacity:.25},p1)}
    const ty=y1+P1.y+24+Math.min(11,(y2-y1)/2+4);
    txt(p1,SX+4,ty,name,{size:6.4,fill:BLUE});
  });
  // depth ticks
  for(let d=0;d<=1200;d+=100){const y=d2y(d)+P1.y+24;line(p1,[[SX-8,y],[SX,y]],{w:.7});txt(p1,SX-11,y+2.5,String(d),{size:6.5,mono:true,anchor:'end',fill:DIM})}
  // wellbore in section
  const wx=SX+70;
  line(p1,[[wx-7,P1.y+24],[wx-7,d2y(1140)+P1.y+24]],{w:2.4,stroke:INK}); // casing
  line(p1,[[wx+7,P1.y+24],[wx+7,d2y(1140)+P1.y+24]],{w:2.4,stroke:INK});
  line(p1,[[wx-3,P1.y+24],[wx-3,d2y(1080)+P1.y+24]],{w:1.2,stroke:BLUE});
  line(p1,[[wx+3,P1.y+24],[wx+3,d2y(1080)+P1.y+24]],{w:1.2,stroke:BLUE});
  line(p1,[[wx,P1.y+24],[wx,d2y(1080)+P1.y+24]],{w:.7,stroke:INK,dash:'2 2'}); // rods
  // pump
  el('rect',{x:wx-4,y:d2y(1080)+P1.y+24,width:8,height:26,fill:'none',stroke:INK,'stroke-width':1.2},p1);
  // perforations
  for(let d=1105;d<=1145;d+=8){const y=d2y(d)+P1.y+24;line(p1,[[wx-7,y],[wx-12,y]],{w:1,stroke:RED});line(p1,[[wx+7,y],[wx+12,y]],{w:1,stroke:RED})}
  // fluid level line (animated)
  const flLine=line(p1,[[wx-7,300],[wx+7,300]],{w:1.4,stroke:BLUE,dash:'4 2'});
  const flTxt=txt(p1,wx+12,300,'FL',{size:6.5,fill:BLUE});
  // heated zone isotherms (animated)
  const isoG=el('g',{},p1);
  const isoEls=[0,1,2].map(i=>{const e=el('ellipse',{cx:wx,cy:d2y(1125)+P1.y+24,rx:10,ry:6,fill:'none',stroke:RED,'stroke-width':.8,'stroke-dasharray':i===2?'3 2':''},isoG);
    const t=txt(p1,wx+12,d2y(1125)+P1.y+24+ i*8,`${100-i*20}°`,{size:6,fill:RED});return{e,t}});
  // depth breaks
  [40,560].forEach(dy=>{const y=dy+P1.y+24;
    const zz=el('path',{d:`M${SX-10} ${y}`+Array.from({length:22},(_,i)=>`l${SW/22} ${i%2?-5:5}`).join(''),fill:'none',stroke:INK,'stroke-width':.8},p1);});

  // pumping unit line-art (left half)
  const LA={ox:P1.x+40,oy:P1.y+40};
  const puG=el('g',{transform:`translate(${LA.ox} ${LA.oy})`},p1);
  line(puG,[[-10,170],[170,170]],{w:1.4}); // ground
  line(puG,[[-4,168],[-4,172]],{w:.5});line(puG,[[160,168],[160,172]],{w:.5});
  // samson post
  line(puG,[[S.x-16,168],[S.x,S.y]],{w:1.4});line(puG,[[S.x+12,168],[S.x,S.y]],{w:1.4});
  line(puG,[[S.x-38,168],[S.x,S.y]],{w:.8,dash:'3 2'}); // rear leg
  line(puG,[[S.x-8,120],[S.x+4,120]],{w:.6});line(puG,[[S.x-11,95],[S.x+2,95]],{w:.6});
  // gearbox + motor
  el('rect',{x:CR.x-14,y:168-30,width:30,height:30,fill:'none',stroke:INK,'stroke-width':1.2},puG);
  el('rect',{x:4,y:140,width:26,height:20,fill:'none',stroke:INK,'stroke-width':1.1},puG); // motor
  line(puG,[[18,140],[CR.x-6,152]],{w:.7});line(puG,[[18,160],[CR.x-8,160]],{w:.7}); // belt
  // crank group (rotates)
  const crankG=el('g',{transform:`translate(${CR.x} ${CR.y})`},puG);
  el('circle',{cx:0,cy:0,r:3,fill:'none',stroke:INK,'stroke-width':1},crankG);
  const crankArm=el('g',{},crankG);
  line(crankArm,[[0,0],[0,-CRR]],{w:2});
  el('path',{d:`M${-CRR*.62} ${-CRR} A${CRR*.72} ${CRR*.72} 0 0 1 ${CRR*.62} ${-CRR}`,fill:'none',stroke:INK,'stroke-width':3},crankArm); // counterweight arc
  el('circle',{cx:0,cy:-CRR,r:2.6,fill:INK},crankArm);
  el('circle',{cx:0,cy:0,r:CRR,fill:'none',stroke:INK,'stroke-width':.4,'stroke-dasharray':'2 3'},crankG);
  // beam group
  const beamG=el('g',{transform:`translate(${S.x} ${S.y})`},puG);
  line(beamG,[[-LR,0],[LF,0]],{w:2.6});
  line(beamG,[[-LR+4,-5],[LF-4,-5]],{w:.7});
  line(beamG,[[-LR,0],[LF,0]],{w:.4,stroke:'#fff'});
  // horsehead arc
  el('path',{d:`M${LF-2} -14 A16 16 0 0 1 ${LF+8} 8`,fill:'none',stroke:INK,'stroke-width':2},beamG);
  line(beamG,[[LF,0],[LF+8,8]],{w:1.4});
  // pitman
  const pitL=line(puG,[[0,0],[0,0]],{w:1.3});
  // polished rod + bridle
  const prLine=line(puG,[[0,0],[0,0]],{w:1.6,stroke:BLUE});
  const brLine=line(puG,[[0,0],[0,0]],{w:.9});
  const carrierR=el('rect',{x:0,y:0,width:8,height:4,fill:'none',stroke:INK,'stroke-width':1},puG);
  // wellhead
  line(puG,[[wx-SX+SX*0+150,168],[150,140]],{w:0}); // noop placeholder
  const whX=150;
  el('rect',{x:whX-5,y:150,width:10,height:18,fill:'none',stroke:INK,'stroke-width':1.2},puG);
  line(puG,[[whX,150],[whX,168]],{w:3});
  line(puG,[[whX+5,158],[whX+16,158]],{w:.9});el('circle',{cx:whX+18,cy:158,r:2,fill:'none',stroke:INK},puG); // flowline + gauge
  // dimension lines
  function dim(x1,y1,x2,y2,label){line(p1,[[x1,y1],[x2,y2]],{w:.5,stroke:BLUE});
    line(p1,[[x1-3,y1],[x1+3,y1]],{w:.5,stroke:BLUE});line(p1,[[x2-3,y2],[x2+3,y2]],{w:.5,stroke:BLUE});
    txt(p1,(x1+x2)/2+4,(y1+y2)/2,label,{size:6.5,mono:true,fill:BLUE})}
  dim(SX+SW+14,d2y(0)+P1.y+24,SX+SW+14,d2y(1080)+P1.y+24,'PUMP @1080');
  dim(SX+SW+14,d2y(1100)+P1.y+24,SX+SW+14,d2y(1150)+P1.y+24,'PAY 50');
  // balloons
  const balloons=[[LA.ox+S.x+LF+14,LA.oy+S.y-16,'①',tip=>'Polished rod'],['seg',0,'②'],];
  const balloonPts=[[LA.ox+S.x+LF+10,LA.oy+S.y-4,1,'HORSEHEAD'],[LA.ox+S.x-10,LA.oy+S.y-14,2,'WALKING BEAM'],[LA.ox+CR.x,LA.oy+CR.y-30,3,'CRANK + CW'],[LA.ox+CR.x-2,LA.oy+168-16,4,'GEARBOX'],[LA.ox+17,LA.oy+134,5,'MOTOR+VFD'],[LA.ox+whX+8,LA.oy+146,6,'WELLHEAD'],[wx-16,d2y(600)+P1.y+24,7,'ROD STRING'],[wx+16,d2y(1080)+P1.y+24,8,'INSERT PUMP'],[wx+20,d2y(1127)+P1.y+24,9,'PERF + HEAT'],[SX+SW-30,d2y(1050)+P1.y+40,10,'CAPROCK']];
  const balloonEls=balloonPts.map(([x,y,n,name])=>{
    const g=el('g',{class:'bp-balloon',style:'cursor:pointer'},p1);
    el('circle',{cx:x,cy:y,r:8,fill:'#F3EEE2',stroke:INK,'stroke-width':1},g);
    const t=txt(g,x,y+3,String(n),{size:9,mono:true,anchor:'middle',fill:INK});
    g.dataset.name=name;return g;});

  // ---------- DEPTH TRACKS ----------
  const DT={x:P1.x+P1.w+10,y:P1.y+24,w:150,h:740-24};
  const tracks=el('g',{class:'bp-slide'},sheet);
  txt(tracks,DT.x,P1.y+10,'DEPTH TRACKS',{size:8,fill:DIM});
  const trackDefs=['T [°C]','P [bar]','μ [cP] log','σ ROD [MPa]'];
  const trackW=DT.w/4-4;
  trackDefs.forEach((n,i)=>{const x=DT.x+i*(trackW+4);
    el('rect',{x,y:DT.y,width:trackW,height:DT.h-DT.y+P1.y,fill:'none',stroke:INK,'stroke-width':.5},tracks);
    txt(tracks,x+trackW/2,DT.y-4,n,{size:6.5,anchor:'middle',fill:BLUE});});
  const trackLines=[0,1,2,3].map(i=>line(tracks,[],{w:1.1,stroke:[RED,BLUE,INK,GRN][i]}));
  const depG=el('rect',{x:DT.x+2*(trackW+4),y:DT.y,width:trackW,height:0,fill:'url(#h-red)',opacity:.35},tracks); // deposition band on μ track? place on T
  const xhair=line(tracks,[[DT.x,0],[DT.x+DT.w,0]],{w:.5,stroke:RED,dash:'3 3'});
  const xhairTxt=txt(tracks,DT.x+DT.w+4,0,'',{size:7,mono:true,fill:RED});
  svg.addEventListener('mousemove',e=>{ // crosshair across tracks
    const pt=svgPoint(svg,e); if(pt.x>DT.x&&pt.x<DT.x+DT.w&&pt.y>DT.y&&pt.y<DT.h){
      xhair.setAttribute('d',`M${DT.x} ${pt.y}H${DT.x+DT.w}`);xhair.style.opacity=1;
      const depth=1200*(pt.y-(P1.y+24))/(d2y(1200)-d2y(0)+P1.y+24); const dd=Math.max(0,Math.min(1200,depth));
      const T=prof.T(dd),P=prof.P(dd),mu=prof.mu(dd),sg=prof.sg(dd);
      xhairTxt.setAttribute('y',pt.y-4);xhairTxt.textContent=`@${dd.toFixed(0)}m · ${T.toFixed(0)}°C · ${P.toFixed(0)}bar · ${mu.toFixed(0)}cP · σ${sg.toFixed(0)}`;
    } else xhair.style.opacity=.0;
  });

  // ---------- small plates on the right ----------
  const PX=760;
  function plate(x,y,w,h,title,no){const g=el('g',{class:'bp-slide',transform:`translate(${x} ${y})`},sheet);
    el('rect',{x:0,y:0,width:w,height:h,class:'bp-plate'},g);el('rect',{x:4,y:4,width:w-8,height:h-8,class:'bp-inner'},g);
    txt(g,10,16,title,{size:8.5,fill:INK,weight:600});txt(g,w-10,16,no,{size:7,anchor:'end',fill:DIM,mono:true});return g}
  // Plate 2: dyno card
  const p2=plate(PX,34,330,220,'PLATE 2 · DYNAMOMETER CARD','LIVE');
  const ax2=axes(p2,330,220,{x:[0,1],y:[0,1],xt:4,yt:4,xl:'position',yl:'load',padL:34,padB:22,padT:24,padR:10});
  const ghostPts=[];for(let u=0;u<=1.001;u+=.02){const[p,l]=dynoCard(u);ghostPts.push([ax2.sx(p),ax2.sy(l*.98+.05)])}
  el('path',{d:path(ghostPts),fill:'url(#h-ink)',opacity:.15},p2);
  const surfPath=el('path',{d:'',fill:'none',stroke:INK,'stroke-width':1.4},p2);
  const downPath=el('path',{d:'',fill:'none',stroke:BLUE,'stroke-width':1.1,'stroke-dasharray':'4 2'},p2);
  const traceDot=el('circle',{r:2.4,fill:RED},p2);
  const diagTxt=txt(p2,PX? 44:0,44,'',{size:8,fill:RED,weight:600});diagTxt.setAttribute('x',44);
  // Plate 3: SPM envelope
  const p3=plate(1100,34,330,220,'PLATE 3 · SAFE-SPM ENVELOPE','N_max(t)');
  const ax3=axes(p3,330,220,{x:[0,120],y:[0,10],xt:6,yt:5,xl:'days since steam',yl:'spm',padL:34,padB:22,padT:24,padR:10});
  {const pts=[];for(let d=0;d<=120;d+=2)pts.push([ax3.sx(d),ax3.sy(nMax(d))]);
   const top=[...pts.map(p=>[p[0],24+ 0])].map((p,i)=>[pts[i][0],ax3.sy(10)]);
   el('path',{d:path(pts)+'L'+ax3.sx(120)+' '+ax3.sy(10)+'L'+ax3.sx(0)+' '+ax3.sy(10)+'Z',fill:'url(#h-red)',opacity:.3},p3);
   line(p3,pts,{stroke:RED,w:1.4});
   const cur=[];for(let d=0;d<=120;d+=2)cur.push([ax3.sx(d),ax3.sy(clamp(4.9+0.9*Math.exp(-d/60),0,10))]);
   line(p3,cur,{stroke:BLUE,w:1.2});
   const mantle=[];for(let d=0;d<=120;d+=2)mantle.push([ax3.sx(d),ax3.sy(Math.min(nMax(d)*.92,5.4))]);
   line(p3,mantle,{stroke:TWIN,w:1.6,dash:'6 3'});
   txt(p3,ax3.sx(60),ax3.sy(9.4),'FORBIDDEN — float',{size:7,fill:RED});
   txt(p3,ax3.sx(30),ax3.sy(3.2),'baseline',{size:7,fill:BLUE});
   txt(p3,ax3.sx(30),ax3.sy(7.4),'mantle plan',{size:7,fill:TWIN});}
  // Plate 4: IPR × pump
  const p4=plate(PX,266,330,200,'PLATE 4 · IPR × PUMP CAPACITY','INFLOW');
  const ax4=axes(p4,330,200,{x:[0,80],y:[0,60],xt:4,yt:3,xl:'q [bopd]',yl:'pwf [bar]',padL:34,padB:22,padT:24,padR:10});
  const iprLine=el('path',{fill:'none',stroke:INK,'stroke-width':1.4},p4);
  const iprGhost=el('path',{fill:'none',stroke:DIM,'stroke-width':.8,'stroke-dasharray':'3 3'},p4);
  const pumpLine=el('path',{fill:'none',stroke:BLUE,'stroke-width':1.2,'stroke-dasharray':'5 3'},p4);
  const opPt=el('g',{},p4);
  el('circle',{r:5,fill:'none',stroke:RED,'stroke-width':1.2},opPt);line(opPt,[[-8,0],[8,0]],{stroke:RED,w:.8});line(opPt,[[0,-8],[0,8]],{stroke:RED,w:.8});
  const limTxt=txt(p4,120,60,'RESERVOIR-LIMITED',{size:7,fill:RED,weight:600});
  // Plate 5: Walther
  const p5=plate(1100,266,330,200,'PLATE 5 · WALTHER ν–T','ASTM D341');
  const ax5=axes(p5,330,200,{x:[30,180],y:[0,5],xt:5,yt:5,xl:'T [°C]',yl:'log log ν',padL:34,padB:22,padT:24,padR:10});
  {const pts=[];for(let T=35;T<=175;T+=5){const mu=viscosity(T);const yy=Math.log10(Math.log10(mu+0.7));const vn=(yy-(-.2))/(0.65-(-.2));pts.push([ax5.sx(T),ax5.sy(vn*5)])}
   line(p5,pts,{stroke:INK,w:1.2});
   [48,97,160].forEach(T=>{const mu=viscosity(T);const yy=Math.log10(Math.log10(mu+0.7));const vn=(yy+0.2)/0.85;
     el('circle',{cx:ax5.sx(T),cy:ax5.sy(vn*5),r:2.4,fill:'none',stroke:RED,'stroke-width':1},p5)});
   txt(p5,ax5.sx(150),ax5.sy(4.6),'ASSUM anchors',{size:6.5,fill:RED});}
  const waltherNow=el('g',{},p5);el('circle',{r:3.4,fill:BLUE},waltherNow);
  // Plate 6: Goodman
  const p6=plate(PX,478,330,180,'PLATE 6 · GOODMAN','FATIGUE');
  const ax6=axes(p6,330,180,{x:[0,400],y:[0,300],xt:4,yt:3,xl:'σ mean [MPa]',yl:'σ alt',padL:34,padB:22,padT:24,padR:10});
  line(p6,[[ax6.sx(0),ax6.sy(280)],[ax6.sx(400),ax6.sy(0)]],{stroke:RED,w:1.2});
  const gmPts=[[190,80,'1"'],[240,95,'⅞"'],[300,110,'¾"']].map(([m,a,n])=>{
    el('circle',{cx:ax6.sx(m),cy:ax6.sy(a),r:3.4,fill:'#F3EEE2',stroke:BLUE,'stroke-width':1.2},p6);
    txt(p6,ax6.sx(m)+6,ax6.sy(a)+2,n,{size:7,mono:true,fill:BLUE});});
  // BOM + notes + title block
  const bom=plate(1100,666,330,124,'BILL OF MATERIALS','BOM');
  [['POLISHED ROD','1¼" Cr-Mo · 3.2 m'],['ROD STRING','1"·⅞"·¾" taper, D-grade'],['INSERT PUMP','2¼" RHBC · @1080 m'],['VIT TUBING','3½" vacuum-insulated'],['BEAM UNIT','API C-320D · stroke 120"'],['STEAM LINE','3" NPS · alu lagging']].forEach((r,i)=>{
    txt(bom,10,30+i*15,r[0],{size:7,fill:INK,ls:.6});txt(bom,320,30+i*15,r[1],{size:7,mono:true,anchor:'end',fill:DIM});});
  // notes + title block bottom-left region
  const nt=plate(30,744,560+150,56,'NOTES & TITLE BLOCK','REV 2');
  const noteTxt=txt(nt,12,34,'',{size:8,mono:true,fill:INK});
  const revTxt=txt(nt,560+150-10,22,'',{size:8,mono:true,anchor:'end',fill:BLUE});
  const tbTxt=txt(nt,560+150-10,38,'',{size:7,mono:true,anchor:'end',fill:DIM});

  // profiles (for tracks + crosshair)
  const prof={
    T:d=>{const Tf=sandfaceT(curT);return lerp(34,Tf,Math.pow(d/1100,.55))+2*Math.sin(d/90)},
    P:d=>2+ d/1100*34,
    mu:d=>viscosity(lerp(34,sandfaceT(curT),Math.pow(d/1100,.55))),
    sg:d=>118- 70*Math.pow(d/1100,.8)+ 8*Math.sin(d/300),
  };
  let curT=41;
  function drawTracks(){
    [0,1,2,3].forEach(i=>{
      const x0=DT.x+i*(trackW+4),pts=[];
      for(let d=0;d<=1200;d+=40){const y=d2y(d)+P1.y+24;let v;
        if(i===0)v=clamp(prof.T(d)/180,0,1);if(i===1)v=clamp(prof.P(d)/40,0,1);
        if(i===2)v=clamp((Math.log10(prof.mu(d))-0.5)/4,0,1);if(i===3)v=clamp(prof.sg(d)/160,0,1);
        pts.push([x0+4+v*(trackW-8),y])}
      trackLines[i].setAttribute('d',path(pts));});
    // deposition band on T track: where T < 62
    let d0=null,d1=null;for(let d=0;d<=1200;d+=20){if(prof.T(d)<62&&d0===null)d0=d;if(prof.T(d)<62)d1=d}
    if(d0!==null){depG.setAttribute('x',DT.x);depG.setAttribute('width',trackW);
      depG.setAttribute('y',d2y(d0)+P1.y+24);depG.setAttribute('height',d2y(d1)-d2y(d0));}
  }

  function update(st,theta,u){
    curT=st.t;
    const b=solve(theta);
    beamG.setAttribute('transform',`translate(${S.x} ${S.y}) rotate(${b*57.29})`);
    crankArm.setAttribute('transform',`rotate(${-(theta-Math.PI/2)*57.29})`);
    // pitman: crank pin → equalizer
    const px=CR.x+CRR*Math.cos(theta),py=CR.y+CRR*Math.sin(theta);
    const ex=S.x-LR*Math.cos(b),ey=S.y-LR*Math.sin(b);
    pitL.setAttribute('d',`M${px} ${py}L${ex} ${ey}`);
    // polished rod from head tip
    const tx=S.x+LF*Math.cos(b),ty=S.y+LF*Math.sin(b);
    const top=ty+8;
    prLine.setAttribute('d',`M${whX} ${top>150?150:top}L${whX} 168`);
    brLine.setAttribute('d',`M${tx+2} ${ty+6}L${whX} ${top}`);
    carrierR.setAttribute('x',whX-4);carrierR.setAttribute('y',top-2);
    // fluid level
    const fy=d2y(st.fluidLevel)+P1.y+24;
    flLine.setAttribute('d',`M${wx-7} ${fy}H${wx+7}`);flTxt.setAttribute('y',fy+2);
    // isotherms from heated radius
    const hr=st.heatedR;
    isoEls.forEach((o,i)=>{const rx=hr*(0.4+i*0.3)*4.4,ry=rx*.6;
      o.e.setAttribute('rx',clamp(rx,4,90));o.e.setAttribute('ry',clamp(ry,3,60));
      o.t.setAttribute('x',wx+clamp(rx,4,90)+4);o.t.setAttribute('y',d2y(1125)+P1.y+24);
      o.e.style.opacity=clamp((st.sandfaceT-48)/112+.15,0,1)});
    // dyno card trace
    const N=48,pts=[],dpts=[];
    for(let i=0;i<=N*u&&i<=N;i++){const[p,l]=dynoCard(i/N);pts.push([ax2.sx(p),ax2.sy(l)]);dpts.push([ax2.sx(p),ax2.sy(l*.88)])}
    surfPath.setAttribute('d',path(pts));downPath.setAttribute('d',path(dpts));
    if(pts.length){traceDot.setAttribute('cx',pts.at(-1)[0]);traceDot.setAttribute('cy',pts.at(-1)[1])}
    diagTxt.textContent=st.fillage<0.7?`FLUID POUND · fillage ${(st.fillage*100).toFixed(0)}% · conf .86`:`NORMAL · fillage ${(st.fillage*100).toFixed(0)}% · conf .92`;
    // IPR
    const mu=st.viscosity,J=62/Math.pow(400/mu,0.0)*1.0;
    const ipr=[],gh=[];
    for(let q=0;q<=78;q+=3){const pw=Math.max(0,44-q*(mu/400)*1.15);ipr.push([ax4.sx(q),ax4.sy(pw)]);gh.push([ax4.sx(q),ax4.sy(Math.max(0,44-q*(mu*1.4/400)*1.15))])}
    iprLine.setAttribute('d',path(ipr));iprGhost.setAttribute('d',path(gh));
    pumpLine.setAttribute('d',`M${ax4.sx(0)} ${ax4.sy(34)}L${ax4.sx(st.spm*14)} ${ax4.sy(6)}`);
    opPt.setAttribute('transform',`translate(${ax4.sx(st.oilRate)} ${ax4.sy(st.pwp)})`);
    limTxt.textContent=st.spm*14>st.oilRate?'RESERVOIR-LIMITED':'PUMP-LIMITED';
    // walther now point
    {const mu=st.viscosity;const yy=Math.log10(Math.log10(mu+0.7));const vn=(yy+0.2)/0.85;
     waltherNow.setAttribute('transform',`translate(${ax5.sx(st.sandfaceT)} ${ax5.sy(clamp(vn*5,0,5))})`)}
    // notes
    noteTxt.textContent=`3. Float margin ${(st.margins.float*100).toFixed(0)}% below 900 m — SPM ≤ ${st.nMax.toFixed(1)} or kd ≥ 0.6.  μ(wh) ${st.viscosity.toFixed(0)} cP.`;
    revTxt.textContent=`BGW-17 · C6 · DAY ${Math.max(0,st.t).toFixed(0)} · ${st.phase}`;
    tbTxt.textContent='DRAWN: Mantle twin v1.4 · NTS (depth piecewise) · SIM';
    drawTracks();
  }
  function drawOn(){ // stroke-draw animation (CSS 'translate' preserves the SVG transform attr)
    sheet.querySelectorAll('.bp-slide').forEach((g,i)=>{g.style.opacity=0;g.style.translate='16px 0';
      g.style.transition=`opacity .5s ${80*i}ms cubic-bezier(.2,.7,.1,1),translate .5s ${80*i}ms cubic-bezier(.2,.7,.1,1)`;
      requestAnimationFrame(()=>requestAnimationFrame(()=>{g.style.opacity=1;g.style.translate='0 0'}))});
  }
  return {svg,update,drawOn,el:container};
}
function svgPoint(svg,e){const pt=svg.createSVGPoint();pt.x=e.clientX;pt.y=e.clientY;return pt.matrixTransform(svg.getScreenCTM().inverse())}
