"""Sedinta de review SECRETARA — board (18 directori) + CPO.
Output: SECRETARA_REVIEW.md (ce merge / ce nu merge / TOP 20 imbunatatiri prioritizate).
"""
from __future__ import annotations
import asyncio, json, os, re, sys, time, urllib.request, urllib.error, itertools, glob
KEYS=[k.strip() for k in os.environ.get("GEMINI_KEYS","").split(",") if k.strip()]
_rr=itertools.cycle(KEYS); MODEL="gemini-flash-lite-latest"; LOT=6; PACE=6
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(f): return os.path.join(ROOT,f)

STARE=(
 "SECRETARA AI din app/eie.html (Local-Only, criptat). Functii EXISTENTE acum:\n"
 "- Jurnal de notite: adaugi/cauti/stergi notite, #tag-uri + filtrare pe tag, marca de timp.\n"
 "- Brief de 1 minut la deschiderea unei conversatii: cand v-ati conectat, interese comune, ce ofera "
 "persoana, notitele tale despre ea, task-urile deschise legate de ea.\n"
 "- Intalniri: propui din conversatie (data/ora/loc), dublu consimtamant, confirmare cu semnatura HMAC; "
 "grupate De confirmat / Confirmate / In asteptare; pe Acasa apare 'urmatoarea intalnire'.\n"
 "- Export intalnire: Google Calendar (URL precompletat) / .ics / email (mailto) — user-initiated.\n"
 "- Follow-up: 3 sabloane (multumire/pas urmator/reprogramare), copiere in clipboard.\n"
 "- Task-uri: cu termen, filtru Toate/Active/Scadente, scadente evidentiate, badge reminder pe tab.\n"
 "- 'Noteaza dupa apel': extrage intentii (caut/ofer) pe cuvinte-cheie -> potriviri.\n"
 "CONSTRANGERI: single-file HTML/JS, fara backend, fara LLM real, fara integrari OAuth. Tot onest.")

def leaders():
    out=[]
    for md in sorted(glob.glob(P("fise/Dep_*.md"))):
        text=open(md,encoding="utf-8").read()
        for m in re.finditer(r"\n## (\d+\.1)\s+(.+)\n", text):
            out.append({"cod":m.group(1),"nume":m.group(2).strip(),"dep":md})
    return out
def _gen(key,prompt,mx):
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
    body=json.dumps({"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"maxOutputTokens":mx,"temperature":0.85}}).encode()
    with urllib.request.urlopen(urllib.request.Request(url,data=body,headers={"Content-Type":"application/json"}),timeout=120) as r: d=json.load(r)
    c=d["candidates"][0]
    if "content" not in c or "parts" not in c["content"]: return "[gol]"
    return "".join(p.get("text","") for p in c["content"]["parts"]).strip()
async def call(sem,prompt,mx=400):
    async with sem:
        res="[rate limit]"
        for a in range(3):
            key=next(_rr)
            try: res=await asyncio.to_thread(_gen,key,prompt,mx);break
            except urllib.error.HTTPError as e:
                if e.code in(429,503): await asyncio.sleep(min(40,4*(1.7**a)));continue
                res=f"[HTTP{e.code}]";break
            except Exception as e: res=f"[{type(e).__name__}]";break
        await asyncio.sleep(PACE);return res
async def gprog(coros,label):
    res=[];d=0;t=len(coros)
    for f in asyncio.as_completed(coros):
        res.append(await f);d+=1
        if d%6==0 or d==t: print(f"   {label}: {d}/{t}",flush=True)
    return res

async def main():
    if not KEYS: print("no GEMINI_KEYS"); sys.exit(1)
    L=leaders();print(f"Review Secretara — {len(L)} directori",flush=True)
    sem=asyncio.Semaphore(LOT)
    async def one(a):
        p=(f"REVIEW al Secretarei AI.\n\n{STARE}\n\nEsti directorul: {a['nume']}.\n"
           "Din rolul tau, raspunde STRICT:\n"
           "MERGE: <ce functioneaza bine si trebuie pastrat>\n"
           "NU MERGE / LIPSESTE: <un defect real sau o lipsa concreta>\n"
           "IMBUNATATIRE: <o imbunatatire concreta, fezabila single-file>\nMax 50 cuvinte.")
        return {"rol":a["nume"],"text":await call(sem,p,360)}
    res=await gprog([one(a) for a in L],"directori")
    json.dump(res,open(P("secretara_review_directori.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    bloc="\n".join(f"[{x['rol']}] {x['text']}" for x in res if not x['text'].startswith("["))
    print("CPO sintetizeaza...",flush=True)
    cp=(f"Esti CPO. Ai condus un review al Secretarei AI.\n\n{STARE}\n\nFEEDBACK DIRECTORI:\n{bloc}\n\n"
        "Scrie SECRETARA_REVIEW.md cu structura:\n"
        "## CE MERGE (5-7 puncte)\n## CE NU MERGE / LIPSESTE (5-7 puncte concrete)\n"
        "## TOP 20 IMBUNATATIRI (lista numerotata 1-20, fiecare o linie scurta, concreta, fezabila "
        "single-file, prioritizate). Format exact: 'N. <imbunatatire>'.\n"
        "Onest, fara magie/integrari false.")
    txt=await call(sem,cp,3500)
    open(P("SECRETARA_REVIEW.md"),"w",encoding="utf-8").write("# Review Secretara AI — board\n\n"+txt)
    print("\n===== REVIEW (extras) =====\n"+txt[:1400]+"\n=====",flush=True)
    print("SECRETARA_REVIEW_DONE",flush=True)
if __name__=="__main__": asyncio.run(main())
