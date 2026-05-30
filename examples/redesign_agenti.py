"""Pune agentii din Design + Behavioral Science sa gandeasca un redesign luxury.

Doar cele 2 departamente relevante (Design/UX si Behavioral Science), in paralel
cu backoff. Apoi un director de design sintetizeaza un brief de redesign concret.
"""
from __future__ import annotations
import asyncio, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import anthropic
from agentap.organizatie import ORGANIZATIE, nume_curat

MODEL="claude-opus-4-8"; LOT=4
DEPS=["7. Design / UX","7b. Behavioral Science & Ethical Product Design"]

def agentii():
    out=[]
    for dep in DEPS:
        for rol,nr,desc in ORGANIZATIE[dep]["roluri"]:
            for i in range(1,nr+1):
                out.append((dep,rol,desc))
    return out

async def idee(client,sem,dep,rol,desc):
    sysp=f"Esti „{rol}” in „{nume_curat(dep)}”. {desc}"
    user=("Reproiectam o aplicatie de networking pentru oameni de afaceri de top. "
        "Directie vizata: LUXURY PREMIUM GOLD BUSINESS — elegant, scump, exclusivist.\n\n"
        "Din rolul tau, da O recomandare CONCRETA si actionabila (max 30 cuvinte) pentru redesign. "
        "Daca esti designer: culori/fonturi/spatiere/detalii vizuale specifice. "
        "Daca esti din psihologie: un principiu cognitiv concret de aplicat (etic, fara dark patterns). "
        "Doar recomandarea, la obiect.")
    async with sem:
        for a in range(5):
            try:
                r=await client.messages.create(model=MODEL,max_tokens=120,
                    system=[{"type":"text","text":sysp,"cache_control":{"type":"ephemeral"}}],
                    output_config={"effort":"low"},
                    messages=[{"role":"user","content":user}])
                return {"dep":nume_curat(dep),"rol":rol,"idee":"".join(b.text for b in r.content if b.type=="text").strip(),"ok":True}
            except anthropic.RateLimitError:
                await asyncio.sleep(2*(2**a))
            except Exception as e:
                return {"dep":nume_curat(dep),"rol":rol,"idee":f"[{type(e).__name__}]","ok":False}
        return {"dep":nume_curat(dep),"rol":rol,"idee":"[rate limit]","ok":False}

async def run(client,lst):
    sem=asyncio.Semaphore(LOT); res=[]; done=0
    for f in asyncio.as_completed([idee(client,sem,*x) for x in lst]):
        res.append(await f); done+=1
        if done%4==0 or done==len(lst): print(f"   ...{done}/{len(lst)}")
    return res

def main():
    if not os.environ.get("ANTHROPIC_API_KEY"): print("no key"); sys.exit(1)
    lst=agentii(); print(f"Pun {len(lst)} agenti (Design + Psihologie) la redesign...")
    res=asyncio.run(run(anthropic.AsyncAnthropic(),lst))
    json.dump(res,open(os.path.join(os.path.dirname(__file__),"..","redesign_idei.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    ok=[x for x in res if x["ok"]]
    print(f"\n{len(ok)}/{len(res)} recomandari. REDESIGN_DONE")
    for x in ok: print(f"  [{x['rol'][:24]}] {x['idee'][:80]}")

if __name__=="__main__": main()
