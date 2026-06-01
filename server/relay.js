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
const http=require("http"),fs=require("fs"),url=require("url");
const PORT=+(process.env.PORT||8787);
const MAXBYTES=+(process.env.RELAY_MAXBYTES||65536);   // 64KB / mesaj
const MAXITEMS=+(process.env.RELAY_MAXITEMS||500);     // inel per mailbox
const FILE=process.env.RELAY_FILE||"";
const CORS=process.env.CORS_ORIGIN||"*";
const MBOX=/^[0-9a-f]{16,128}$/;                       // id opac (hex)

let store=Object.create(null);                          // mailbox -> {seq, items:[{seq,ct,t}]}
if(FILE){try{store=JSON.parse(fs.readFileSync(FILE,"utf8"));}catch(_){}}
let dirty=false;
if(FILE)setInterval(()=>{if(dirty){try{fs.writeFileSync(FILE,JSON.stringify(store));dirty=false;}catch(_){}}},2000).unref();

function send(res,code,obj){const b=Buffer.from(JSON.stringify(obj));
  res.writeHead(code,{"Content-Type":"application/json","Access-Control-Allow-Origin":CORS,
    "Access-Control-Allow-Methods":"GET,POST,OPTIONS","Access-Control-Allow-Headers":"Content-Type"});
  res.end(b);}

const srv=http.createServer((req,res)=>{
  const u=url.parse(req.url,true);
  if(req.method==="OPTIONS")return send(res,204,{});
  if(u.pathname==="/health")return send(res,200,{ok:true,mailboxes:Object.keys(store).length});
  const m=u.pathname.match(/^\/m\/([^/]+)$/);
  if(!m)return send(res,404,{error:"not found"});
  const id=m[1];
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
