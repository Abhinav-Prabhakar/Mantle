// ============================================================
// Mantle demo — tiny SVG chart helpers (drafting conventions)
// ============================================================
const NS='http://www.w3.org/2000/svg';
export function el(tag,attrs={},parent){const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);if(parent)parent.appendChild(e);return e}
export const INK='#1E2A33',BLUE='#1F4E79',RED='#B3362C',AMB='#C98A1B',GRN='#3F7D4E',TWIN='#2F5BD3',DIM='#8A8A80';
export const scaleX=(v,a,b,W,pad=8)=>pad+(v-a)/(b-a)*(W-2*pad);
export const scaleY=(v,a,b,H,pad=8)=>H-pad-(v-a)/(b-a)*(H-2*pad);
export function path(pts){return pts.length?'M'+pts.map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join('L'):'M0 0'}

export function axes(svg,W,H,{x=[0,1],y=[0,1],xt=5,yt=4,xl='',yl='',padL=38,padB=22,padT=8,padR=8}={}){
  const f=el('g',{},svg);
  el('rect',{x:padL,y:padT,width:W-padL-padR,height:H-padT-padB,fill:'none',stroke:INK,'stroke-width':1},f);
  for(let i=0;i<=xt;i++){const v=x[0]+(x[1]-x[0])*i/xt;const px=scaleX(v,x[0],x[1],W-padR,padL);
    el('line',{x1:px,y1:H-padB,x2:px,y2:H-padB+4,stroke:INK,'stroke-width':.7},f);
    const t=el('text',{x:px,y:H-padB+13,'text-anchor':'middle','font-size':7.5,fill:DIM,'font-family':'IBM Plex Mono'},f);t.textContent=+v.toFixed(0)===v?v:v.toFixed(1);}
  for(let i=0;i<=yt;i++){const v=y[0]+(y[1]-y[0])*i/yt;const py=scaleY(v,y[0],y[1],H-padT,padB);
    el('line',{x1:padL-4,y1:py,x2:padL,y2:py,stroke:INK,'stroke-width':.7},f);
    const t=el('text',{x:padL-6,y:py+2.5,'text-anchor':'end','font-size':7.5,fill:DIM,'font-family':'IBM Plex Mono'},f);t.textContent=v.toFixed(v<10?1:0);}
  if(xl){const t=el('text',{x:(W+padL-padR)/2,y:H-3,'text-anchor':'middle','font-size':7.5,fill:DIM,'letter-spacing':1.2,'font-family':'IBM Plex Sans Condensed'},f);t.textContent=xl.toUpperCase()}
  if(yl){const t=el('text',{x:8,y:(H+padT-padB)/2,'text-anchor':'middle','font-size':7.5,fill:DIM,'letter-spacing':1.2,'font-family':'IBM Plex Sans Condensed',transform:`rotate(-90 10 ${(H+padT-padB)/2})`},f);t.textContent=yl.toUpperCase()}
  return {sx:v=>scaleX(v,x[0],x[1],W-padR,padL), sy:v=>scaleY(v,y[0],y[1],H-padT,padB), x0:padL,x1:W-padR,y0:padT,y1:H-padB};
}
export function line(svg,pts,{stroke=INK,w=1.2,dash='',op=1}={}){return el('path',{d:path(pts),fill:'none',stroke,'stroke-width':w,'stroke-dasharray':dash,opacity:op},svg)}
export function area(svg,top,bot,fill,op=.15){const d=path(top)+'L'+bot.map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).reverse().join('L')+'Z';return el('path',{d,fill,opacity:op,stroke:'none'},svg)}
export function txt(svg,x,y,s,{size=8.5,fill=DIM,anchor='start',mono=false,rot=0,weight=400,ls=1}={}){const t=el('text',{x,y,'text-anchor':anchor,'font-size':size,fill,'font-family':mono?'IBM Plex Mono':'IBM Plex Sans Condensed','letter-spacing':ls,'font-weight':weight,transform:rot?`rotate(${rot} ${x} ${y})`:''},svg);t.textContent=s;return t}
export function hatchPattern(defs,id,color=RED,angle=45,gap=5){
  const p=el('pattern',{id,width:gap,height:gap,patternUnits:'userSpaceOnUse',patternTransform:`rotate(${angle})`},defs);
  el('line',{x1:0,y1:0,x2:0,y2:gap,stroke:color,'stroke-width':.7,'stroke-opacity':.55},p); return id;
}
export function sparkline(svg,W,H,data,{stroke='#5B83F0',band=null}={}){
  const mn=Math.min(...data),mx=Math.max(...data),sp=(mx-mn)||1;
  const pts=data.map((v,i)=>[i/(data.length-1)*(W-4)+2,(H-3)-(v-mn)/sp*(H-6)]);
  if(band){const p1=band[0].map((v,i)=>[i/(band[0].length-1)*(W-4)+2,(H-3)-(v-mn)/sp*(H-6)]);
    const p2=band[1].map((v,i)=>[i/(band[1].length-1)*(W-4)+2,(H-3)-(v-mn)/sp*(H-6)]);
    area(svg,p2,p1,stroke,.18)}
  line(svg,pts,{stroke,w:1.4});
}
export function donut(svg,cx,cy,r,parts){ // parts: [value,color,label]
  const tot=parts.reduce((s,p)=>s+p[0],0);let a=-Math.PI/2;
  for(const [v,c,l] of parts){const a2=a+v/tot*Math.PI*2;
    const large=a2-a>Math.PI?1:0;
    el('path',{d:`M${cx} ${cy} L${cx+r*Math.cos(a)} ${cy+r*Math.sin(a)} A${r} ${r} 0 ${large} 1 ${cx+r*Math.cos(a2)} ${cy+r*Math.sin(a2)} Z`,fill:c,opacity:.85},svg);
    a=a2}
  el('circle',{cx,cy,r:r*.55,fill:'#F3EEE2'},svg);
}
export function ring(svg,cx,cy,r,frac,color){ // progress ring
  el('circle',{cx,cy,r,fill:'none',stroke:'rgba(30,42,51,.15)','stroke-width':6},svg);
  const c=2*Math.PI*r;
  el('circle',{cx,cy,r,fill:'none',stroke:color,'stroke-width':6,'stroke-dasharray':`${frac*c} ${c}`,'stroke-linecap':'round',transform:`rotate(-90 ${cx} ${cy})`},svg);
}
export function dynoCard(u){ // returns card pts [pos, load] for stroke angle — used by blueprint + peek
  // u∈[0,1] crank cycle; load shape with pound dip
  const th=u*Math.PI*2;
  const pos=.5-.5*Math.cos(th);
  let load=.62+.28*Math.sin(th)+ .10*Math.sin(2*th);
  if(u>.5&&u<.68)load-= (u-.5)/.18*.22; // pound dip
  return [pos,load];
}
