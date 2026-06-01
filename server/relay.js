#!/usr/bin/env node
/* Cercul EIE — releu de referinta ZERO-KNOWLEDGE (loop5 / pivot E2EE).
 * Rol: "postas prost". Stocheaza si transporta DOAR ciphertext, pe mailbox-uri opace.
 * NU detine chei, NU poate decripta. Append-only. Fara dependinte externe (doar Node built-in).
 *
 * API:
 *   POST /m/:mailbox     body = ciphertext brut (text/plain, base64)   -> {seq}
 *   GET  /m/:mailbox?since=N                                           -> {items:[{seq,ct}], last}
 *   GET  /health                                                       -> {ok:true}
 *
 * Limite: mailbox = 64 hex; payload <= MAXBYTES; pana la MAXITEMS per mailbox (inel).
 * Stocare: in-memory implicit; daca RELAY_FILE e setat, persista periodic JSON pe disc.
 * Pornire: node server/relay.js   (PORT, RELAY_FILE, CORS_ORIGIN din env)
 */
"use strict";
const http=require("http"),fs=require("fs"),url=require("url"),crypto=require("crypto");
// Entitlement (loop5 R3): token Pro semnat HMAC -> enforcement REAL server-side (nu se poate pirata fara secret).
// In productie /entitlement/grant e apelat de webhook-ul de plata (Stripe); aici e stub de dezvoltare.
const SECRET=process.env.RELAY_SECRET||crypto.randomBytes(32).toString("hex");
function signPro(pub){const exp=Date.now()+30*864e5,payload=pub+"|pro|"+exp;
  const sig=crypto.createHmac("sha256",SECRET).update(payload).digest("hex");
  return Buffer.from(payload).toString("base64")+"."+sig;}
function verifyPro(token){try{const[b,sig]=String(token||"").split(".");if(!b||!sig)return false;
  const payload=Buffer.from(b,"base64").toString("utf8"),[pub,tier,exp]=payload.split("|");
  const good=crypto.createHmac("sha256",SECRET).update(payload).digest("hex");
  if(sig.length!==good.length||!crypto.timingSafeEqual(Buffer.from(sig),Buffer.from(good)))return false;
  return tier==="pro"&&Date.now()<+exp;}catch(_){return false;}}
const RATE=Object.create(null); // ip -> [timestamps] pentru /dir (anti-spam/Sybil)
function rateOk(ip){const now=Date.now(),w=RATE[ip]=(RATE[ip]||[]).filter(t=>now-t<600000);
  if(w.length>=10)return false;w.push(now);return true;}
const PORT=+(process.env.PORT||8787);
const MAXBYTES=+(process.env.RELAY_MAXBYTES||65536);   // 64KB / mesaj
const MAXITEMS=+(process.env.RELAY_MAXITEMS||500);     // inel per mailbox
const FILE=process.env.RELAY_FILE||"";
const CORS=process.env.CORS_ORIGIN||"*";
const MBOX=/^[0-9a-f]{16,128}$/;                       // id opac (hex)

let store=Object.create(null);                          // mailbox -> {seq, items:[{seq,ct,t}]}
let dir=Object.create(null);                            // pub -> {pub, card, t}  (DIRECTOR public, NU E2EE — opt-in)
if(FILE){try{const o=JSON.parse(fs.readFileSync(FILE,"utf8"));store=o.store||o;dir=o.dir||Object.create(null);}catch(_){}}
const PUBRE=/^[A-Za-z0-9+/=]{40,200}$/;
function readBody(req,res,cb){let len=0;const ch=[];req.on("data",c=>{len+=c.length;if(len>MAXBYTES)res.destroy();else ch.push(c);});req.on("end",()=>cb(Buffer.concat(ch).toString("utf8")));}
function dirText(e){const c=e.card||{};return [c.n,c.d,c.r,(c.o||[]).join(" ")].join(" ").toLowerCase();}
let dirty=false;
if(FILE)setInterval(()=>{if(dirty){try{fs.writeFileSync(FILE,JSON.stringify({store,dir}));dirty=false;}catch(_){}}},2000).unref();

function send(res,code,obj){const b=Buffer.from(JSON.stringify(obj));
  res.writeHead(code,{"Content-Type":"application/json","Access-Control-Allow-Origin":CORS,
    "Access-Control-Allow-Methods":"GET,POST,OPTIONS","Access-Control-Allow-Headers":"Content-Type, X-Pro"});
  res.end(b);}

const srv=http.createServer((req,res)=>{
  const u=url.parse(req.url,true);
  if(req.method==="OPTIONS")return send(res,204,{});
  if(u.pathname==="/health")return send(res,200,{ok:true,mailboxes:Object.keys(store).length,directory:Object.keys(dir).length});
  // ---- DIRECTOR public (discovery opt-in; NU E2EE — doar carduri publice) ----
  if(u.pathname==="/dir/search"&&req.method==="GET"){const q=String(u.query.q||"").trim().toLowerCase();
    let out=Object.values(dir);
    if(q)out=out.filter(e=>dirText(e).includes(q));
    out=out.sort((a,b)=>b.t-a.t).slice(0,30).map(e=>({pub:e.pub,card:e.card}));
    return send(res,200,{results:out});}
  // ---- ENTITLEMENT Pro (token semnat HMAC) ----
  if(u.pathname==="/entitlement/grant"&&req.method==="POST")return readBody(req,res,body=>{
    let o;try{o=JSON.parse(body);}catch(_){return send(res,400,{error:"json"});}
    if(!o||!PUBRE.test(o.pub||""))return send(res,400,{error:"pub invalid"});
    return send(res,200,{token:signPro(o.pub),tier:"pro"});}); // (in prod: doar dupa plata confirmata)
  if(u.pathname==="/entitlement/verify"&&req.method==="GET")
    return send(res,200,{valid:verifyPro(u.query.token)});
  if(u.pathname==="/dir"&&req.method==="POST")return readBody(req,res,body=>{
    const ip=(req.headers["x-forwarded-for"]||req.socket.remoteAddress||"?").split(",")[0].trim();
    if(!rateOk(ip))return send(res,429,{error:"prea multe publicari — reincearca mai tarziu"});
    let o;try{o=JSON.parse(body);}catch(_){return send(res,400,{error:"json"});}
    if(!o||!PUBRE.test(o.pub||"")||!o.card||typeof o.card!=="object")return send(res,400,{error:"invalid"});
    const c=o.card,card={n:String(c.n||"").slice(0,80),d:String(c.d||"").slice(0,60),r:String(c.r||"").slice(0,80),
      o:Array.isArray(c.o)?c.o.slice(0,5).map(x=>String(x).slice(0,140)):[]};
    if(!card.n)return send(res,400,{error:"nume gol"});
    dir[o.pub]={pub:o.pub,card,t:Date.now()};dirty=true;return send(res,200,{ok:true});});
  if(u.pathname==="/dir/del"&&req.method==="POST")return readBody(req,res,body=>{
    let o;try{o=JSON.parse(body);}catch(_){return send(res,400,{error:"json"});}
    if(o&&o.pub&&dir[o.pub]){delete dir[o.pub];dirty=true;}return send(res,200,{ok:true});});
  // MAILBOX: /m/:id (sync pereche) sau /self/:id (multi-device Pro -> necesita token Pro VALID, altfel 402)
  const m=u.pathname.match(/^\/(m|self)\/([^/]+)$/);
  if(!m)return send(res,404,{error:"not found"});
  if(m[1]==="self"&&!verifyPro(req.headers["x-pro"]))return send(res,402,{error:"pro necesar (multi-device)"});
  const id=m[2];
  if(!MBOX.test(id))return send(res,400,{error:"mailbox invalid"});

  if(req.method==="GET"){
    const since=Math.max(0,+u.query.since||0);
    const box=store[id];
    if(!box)return send(res,200,{items:[],last:0});
    const items=box.items.filter(x=>x.seq>since).map(x=>({seq:x.seq,ct:x.ct}));
    return send(res,200,{items,last:box.seq});
  }
  if(req.method==="POST"){
    let len=0;const chunks=[];
    req.on("data",c=>{len+=c.length;if(len>MAXBYTES){res.destroy();}else chunks.push(c);});
    req.on("end",()=>{
      const ct=Buffer.concat(chunks).toString("utf8");
      if(!ct)return send(res,400,{error:"empty"});
      const box=store[id]||(store[id]={seq:0,items:[]});
      box.seq++;
      box.items.push({seq:box.seq,ct,t:Date.now()});
      if(box.items.length>MAXITEMS)box.items.splice(0,box.items.length-MAXITEMS); // inel
      dirty=true;
      send(res,200,{seq:box.seq});
    });
    return;
  }
  send(res,405,{error:"method"});
});
srv.listen(PORT,()=>console.log("relay zero-knowledge pe http://127.0.0.1:"+PORT+" (maxbytes="+MAXBYTES+", file="+(FILE||"in-memory")+")"));
