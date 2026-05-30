"""Reia FAZA 3 (peer review) + FAZA 4 (concept) din ideile deja salvate.

Repara bug-urile din prima rulare:
  - max_tokens marit (BadRequestError venea din max_tokens prea mic + thinking)
  - paralelism redus la 3 + backoff mai lung (rate limit)
  - parser de scoruri mai tolerant

Foloseste idei2.json + market_research.json deja generate (nu reface fazele 1-2).
"""
from __future__ import annotations
import asyncio, json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import anthropic

MODEL="claude-opus-4-8"; LOT=3
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(f): return os.path.join(ROOT,f)
PRODUS=("O aplicatie mobila privata de business networking pentru un cerc de oameni de afaceri: "
  "aduna ce ofera/ce cauta fiecare, face potriviri si propune conexiuni cu dublu consimtamant si sursa citata.")

async def call(client,sem,sysp,user,*,max_tokens=900,effort="medium"):
    async with sem:
        for a in range(7):
            try:
                r=await client.messages.create(model=MODEL,max_tokens=max_tokens,
                    system=[{"type":"text","text":sysp,"cache_control":{"type":"ephemeral"}}],
                    output_config={"effort":effort},
                    messages=[{"role":"user","content":user}])
                return "".join(b.text for b in r.content if b.type=="text").strip()
            except anthropic.RateLimitError:
                await asyncio.sleep(4*(2**a))
            except anthropic.BadRequestError as e:
                return f"[BadRequest:{str(e)[:60]}]"
            except Exception as e:
                return f"[{type(e).__name__}]"
        return "[rate limit]"

async def gather_prog(coros,label):
    res=[];done=0;tot=len(coros)
    for f in asyncio.as_completed(coros):
        res.append(await f);done+=1
        if done%10==0 or done==tot: print(f"   {label}: {done}/{tot}",flush=True)
    return res

def research_digest(res):
    return "\n".join(f"[{r['rol']}] "+r["research"].replace("\n"," ")[:380] for r in res if not r["research"].startswith("["))

async def faza3(client,idei):
    print("FAZA 3 (reluat) — Peer review",flush=True)
    sem=asyncio.Semaphore(LOT); n=len(idei)
    async def one(i,a):
        peers=[idei[(i+k*37+11)%n] for k in (1,2,3)]
        bloc="\n".join(f"{j+1}. [{p['rol']}] {p['idee']}" for j,p in enumerate(peers))
        sysp=f"Esti „{a['rol']}”, evaluator critic dar constructiv de produs."
        u=(f"Produs: {PRODUS}\n\nEvalueaza aceste 3 idei. Pentru fiecare da scor 0-10 "
           "(wow + fezabil + diferentiator) si o critica scurta.\n"
           "Format EXACT, cate o linie:\n1: <scor> | <critica>\n2: <scor> | <critica>\n3: <scor> | <critica>\n\n"+bloc)
        ev=await call(client,sem,sysp,u,max_tokens=900,effort="medium")
        return {"reviewer":a["id"],"peers":[p["id"] for p in peers],"eval":ev}
    res=await gather_prog([one(i,a) for i,a in enumerate(idei)],"reviews")
    json.dump(res,open(P("reviews.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    # parser tolerant: "1: 8", "1: 8 |", "1) 8", "1. 8"
    score={}
    for r in res:
        for m in re.finditer(r"(\d)\s*[:.\)]\s*(\d+(?:[.,]\d+)?)",r["eval"]):
            k=int(m.group(1))-1
            if 0<=k<len(r["peers"]):
                try: score.setdefault(r["peers"][k],[]).append(float(m.group(2).replace(",",".")))
                except: pass
    by={a["id"]:a for a in idei}; ranked=[]
    for pid,scs in score.items():
        if pid in by: ranked.append({**by[pid],"peer_score":round(sum(scs)/len(scs),2),"n_votes":len(scs)})
    ranked.sort(key=lambda x:x["peer_score"],reverse=True)
    json.dump(ranked,open(P("idei_ranked.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"   -> {len(ranked)} idei punctate. TOP 8:",flush=True)
    for x in ranked[:8]:
        print(f"      {x['peer_score']} ({x['n_votes']}v) [{x['rol'][:20]}] {x['idee'][:72]}",flush=True)
    return ranked

async def faza4(client,ranked,research):
    print("\nFAZA 4 — Concept final",flush=True)
    top=ranked[:40]
    bloc="\n".join(f"({x['peer_score']}) [{x['dep']} · {x['rol']}] {x['idee']}" for x in top)
    dig=research_digest(research)[:3000]
    sysp="Esti Chief Product Officer, conduci sedinta de dezvoltare a firmei (220 oameni)."
    u=(f"PRODUS de baza: {PRODUS}\n\nCERCETARE DE PIATA (surse reale):\n{dig}\n\n"
       f"TOP idei votate de cei 220 angajati:\n{bloc}\n\n"
       "Sintetizeaza un CONCEPT DE PRODUS coerent si ambitios. Structura:\n"
       "1. PROPUNEREA UNICA: ce face revolutionar fata de LinkedIn/Shapr/Raya/Lunchclub\n"
       "2. NUME nou + tagline\n3. 6-8 FUNCTII-CHEIE (ce e + de ce e wow), construibile client-side\n"
       "4. DIFERENTIATORUL principal\n5. DESIGN: directie vizuala in 2 randuri\n"
       "Concret si indraznet — e munca a 220 de oameni.")
    concept=await call(client,asyncio.Semaphore(1),sysp,u,max_tokens=3500,effort="high")
    open(P("concept_final.md"),"w",encoding="utf-8").write("# Concept final (220 agenti)\n\n"+concept)
    print("\n===== CONCEPT FINAL =====",flush=True); print(concept[:2000],flush=True)
    return concept

async def main():
    if not os.environ.get("ANTHROPIC_API_KEY"): print("no key"); sys.exit(1)
    client=anthropic.AsyncAnthropic()
    idei=json.load(open(P("idei2.json"),encoding="utf-8"))
    research=json.load(open(P("market_research.json"),encoding="utf-8"))
    t0=time.time()
    ranked=await faza3(client,idei)
    if ranked: await faza4(client,ranked,research)
    print(f"\nP34_DONE in {time.time()-t0:.0f}s",flush=True)

if __name__=="__main__": asyncio.run(main())
