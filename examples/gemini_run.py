"""Motor multi-agent pe Google Gemini (gratis), cu rotatie pe mai multe chei.

Ruleaza cei 220 de agenti: ideatie -> peer review -> concept -> constructie,
distribuind apelurile pe toate cheile Gemini ca sa evite rate limit.

Chei: din variabila de mediu GEMINI_KEYS (separate prin virgula).
"""
from __future__ import annotations
import asyncio, json, os, re, sys, time, urllib.request, urllib.error, itertools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agentap.organizatie import ORGANIZATIE, nume_curat

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(f): return os.path.join(ROOT,f)
KEYS=[k.strip() for k in os.environ.get("GEMINI_KEYS","").split(",") if k.strip()]
_rr=itertools.cycle(KEYS)
FLASH="gemini-2.5-flash"
LOT=8  # paralelism (avem mai multe chei)

PRODUS=("Aplicatie mobila privata de business networking pentru un cerc de oameni de afaceri: "
  "aduna ce ofera/ce cauta fiecare, face potriviri si propune conexiuni cu dublu consimtamant si sursa citata.")

def _gen_sync(key, model, prompt, max_tokens):
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    body=json.dumps({"contents":[{"parts":[{"text":prompt}]}],
        "generationConfig":{"maxOutputTokens":max_tokens,"temperature":0.9}}).encode()
    req=urllib.request.Request(url,data=body,headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=120) as r:
        d=json.load(r)
    c=d["candidates"][0]
    if "content" not in c or "parts" not in c["content"]:
        return "[gol]"
    return "".join(p.get("text","") for p in c["content"]["parts"]).strip()

async def gen(sem, prompt, *, model=FLASH, max_tokens=200):
    async with sem:
        for a in range(6):
            key=next(_rr)
            try:
                return await asyncio.to_thread(_gen_sync,key,model,prompt,max_tokens)
            except urllib.error.HTTPError as e:
                if e.code==429:
                    await asyncio.sleep(2*(2**a)); continue
                return f"[HTTP{e.code}]"
            except Exception as e:
                return f"[{type(e).__name__}]"
        return "[rate limit]"

async def gather_prog(coros,label):
    res=[];done=0;tot=len(coros)
    for f in asyncio.as_completed(coros):
        res.append(await f);done+=1
        if done%20==0 or done==tot: print(f"   {label}: {done}/{tot}",flush=True)
    return res

def toti():
    out=[]
    for dep,data in ORGANIZATIE.items():
        for rol,nr,desc in data["roluri"]:
            for i in range(1,nr+1):
                out.append({"dep":nume_curat(dep),"rol":rol,"desc":desc,"id":f"{nume_curat(dep)[:10]}|{rol}|{i}"})
    return out

def research_digest():
    try: mr=json.load(open(P("market_research.json"),encoding="utf-8"))
    except: return ""
    return "\n".join(f"[{r['rol']}] "+r["research"].replace("\n"," ")[:350] for r in mr if not r["research"].startswith("["))[:5000]

async def faza_ideatie(sem,dig):
    print("IDEATIE — 220 agenti pe Gemini",flush=True)
    ang=toti()
    async def one(a):
        p=(f"Esti „{a['rol']}” in „{a['dep']}”. {a['desc']}\n\n{PRODUS}\n\n"
           f"CERCETARE DE PIATA:\n{dig}\n\nPropune O imbunatatire concreta si diferentiatoare "
           "fata de LinkedIn/Shapr/Raya, din expertiza ta. Max 30 cuvinte. Doar ideea.")
        return {**a,"idee":await gen(sem,p,max_tokens=120)}
    res=[x for x in await gather_prog([one(a) for a in ang],"idei") if not x["idee"].startswith("[")]
    json.dump(res,open(P("g_idei.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"   -> {len(res)} idei\n",flush=True)
    return res

async def faza_review(sem,idei):
    print("PEER REVIEW — agentii se verifica intre ei",flush=True)
    n=len(idei)
    async def one(i,a):
        peers=[idei[(i+k*37+11)%n] for k in (1,2,3)]
        bloc="\n".join(f"{j+1}. [{p['rol']}] {p['idee']}" for j,p in enumerate(peers))
        p=(f"Esti „{a['rol']}”, evaluator. Produs: {PRODUS}\n\nNoteaza fiecare idee 0-10 "
           f"(wow+fezabil+diferentiator). Format exact, o linie:\n1: nota\n2: nota\n3: nota\n\n{bloc}")
        return {"peers":[x['id'] for x in peers],"eval":await gen(sem,p,max_tokens=120)}
    res=await gather_prog([one(i,a) for i,a in enumerate(idei)],"reviews")
    score={}
    for r in res:
        for m in re.finditer(r"(\d)\s*[:.\)]\s*(\d+(?:[.,]\d+)?)",r["eval"]):
            k=int(m.group(1))-1
            if 0<=k<len(r["peers"]):
                try:score.setdefault(r["peers"][k],[]).append(float(m.group(2).replace(",",".")))
                except:pass
    by={a["id"]:a for a in idei};ranked=[]
    for pid,scs in score.items():
        if pid in by: ranked.append({**by[pid],"peer_score":round(sum(scs)/len(scs),2),"votes":len(scs)})
    ranked.sort(key=lambda x:x["peer_score"],reverse=True)
    json.dump(ranked,open(P("g_ranked.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"   -> {len(ranked)} idei punctate. TOP 8:",flush=True)
    for x in ranked[:8]: print(f"      {x['peer_score']} [{x['rol'][:20]}] {x['idee'][:66]}",flush=True)
    print("",flush=True)
    return ranked

async def faza_concept(sem,ranked,dig):
    print("CONCEPT — sinteza (CPO)",flush=True)
    top="\n".join(f"({x['peer_score']}) [{x['rol']}] {x['idee']}" for x in ranked[:40])
    p=(f"Esti CPO. {PRODUS}\n\nCERCETARE:\n{dig}\n\nTOP idei votate de cei 220:\n{top}\n\n"
       "Sintetizeaza un concept ambitios. Structura: 1.Propunere unica (vs LinkedIn/Raya) "
       "2.Nume+tagline 3.7 functii-cheie (construibile client-side) 4.Diferentiator 5.Design (negru+auriu, premium). Concret.")
    c=await gen(sem,p,max_tokens=2500)
    open(P("g_concept.md"),"w",encoding="utf-8").write("# Concept (220 agenti, Gemini)\n\n"+c)
    print("\n===== CONCEPT =====\n"+c[:1400]+"\n=====\n",flush=True)
    return c

async def main():
    if not KEYS: print("no GEMINI_KEYS"); sys.exit(1)
    print(f"Pornesc cu {len(KEYS)} chei Gemini, LOT={LOT}",flush=True)
    sem=asyncio.Semaphore(LOT); dig=research_digest(); t0=time.time()
    idei=await faza_ideatie(sem,dig)
    ranked=await faza_review(sem,idei)
    await faza_concept(sem,ranked,dig)
    print(f"\nGEMINI_DONE in {time.time()-t0:.0f}s — {len(idei)} agenti au muncit pe 3 faze.",flush=True)

if __name__=="__main__": asyncio.run(main())
