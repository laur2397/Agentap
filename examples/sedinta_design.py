"""Sedinta LOOP 3 — Design + Psihologie & Cognitiv (engagement ETIC).
Board (18 directori) + lead-uri (Design / Behavioral Science / Product / Marketing) -> CPO.
Output: DESIGN_PSIHO_REVIEW.md (ce merge / ce nu merge / TOP 20 imbunatatiri etice de engagement & claritate).
Reguli: fara dark patterns, fara manipulare dopaminergica; retentie SANATOASA, valoare reala, claritate.
"""
from __future__ import annotations
import asyncio, json, os, re, sys, urllib.request, urllib.error, itertools, glob
KEYS=[k.strip() for k in os.environ.get("GEMINI_KEYS","").split(",") if k.strip()]
_rr=itertools.cycle(KEYS); MODEL="gemini-flash-lite-latest"; LOT=6; PACE=6
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(f): return os.path.join(ROOT,f)

STARE=(
 "PRODUS: 'Cercul EIE / Network Capital' — app mobila premium de business networking, Local-Only, "
 "criptata, client-side (single-file HTML/JS, fara backend, fara LLM real). Design system 'Bloom': "
 "fundal deschis #FAFAFB, carduri albe, accent indigo #6366F1, succes emerald, font Inter, light+dark. "
 "Ecrane: Acasa (rezumat, urmatoarea intalnire, conexiuni), Potriviri (carduri persoana 'gist-first'), "
 "Reteaua (lista + harta), Secretara (Azi, calendar saptamanal, intalniri cu remindere<24h, task-uri cu "
 "prioritate/snooze/duplicare/bulk-done, jurnal de notite cu tag-uri si filtre, brief de 1 minut cu istoric, "
 "mod Focus, quick-add global, notificari opt-in oneste), Profil (ce ofer/ce caut, audit, setari). "
 "OBIECTIV LOOP: app ATRACTIVA, placuta la folosire, care comunica CLAR necesitatea/valoarea din prima, "
 "maxim de utilitate si retentie SANATOASA. "
 "CONSTRANGERE ETICA ABSOLUTA: ZERO dark patterns, zero manipulare dopaminergica, zero vanity-metrics "
 "inselatoare, zero notificari intruzive. Recompense INTRINSECI (progres real), nu artificiale. "
 "CONSTRANGERI TEHNICE: single-file, zero innerHTML (DOM API), criptare/CSP/TrustedTypes/WCAG pastrate.")

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
    L=leaders();print(f"Sedinta Design+Psihologie — {len(L)} directori",flush=True)
    sem=asyncio.Semaphore(LOT)
    async def one(a):
        p=(f"SEDINTA pe DESIGN + PSIHOLOGIE & COGNITIV (engagement ETIC).\n\n{STARE}\n\n"
           f"Esti directorul: {a['nume']}.\nDin unghiul tau, raspunde STRICT:\n"
           "MERGE: <ce atrage/place deja si trebuie pastrat>\n"
           "NU MERGE / LIPSESTE: <un blocaj real de claritate, valoare perceputa sau placere a folosirii>\n"
           "IMBUNATATIRE ETICA: <o imbunatatire concreta, fezabila single-file, care creste claritatea/"
           "valoarea/retentia SANATOS, fara dark patterns>\nMax 55 cuvinte.")
        return {"rol":a["nume"],"text":await call(sem,p,380)}
    res=await gprog([one(a) for a in L],"directori")
    json.dump(res,open(P("design_psiho_directori.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    bloc="\n".join(f"[{x['rol']}] {x['text']}" for x in res if not x['text'].startswith("["))
    # lead-uri de specialitate
    async def lead(rol,unghi):
        p=(f"Esti {rol}.\n\n{STARE}\n\nSINTEZA COLEGILOR:\n{bloc[:3500]}\n\n"
           f"Din specialitatea ta ({unghi}), da 3 recomandari ETICE, concrete, fezabile single-file, "
           "care fac app-ul mai clar/placut/util si cresc retentia SANATOS (fara manipulare). Max 90 cuvinte.")
        return {"rol":rol,"text":await call(sem,p,420)}
    print("Lead-uri de specialitate...",flush=True)
    leads=await gprog([
        lead("Design Lead","ierarhie vizuala, claritate, micro-interactiuni placute, prima impresie"),
        lead("Behavioral Science Lead","psihologie cognitiva: reducere efort, momentul 'aha', recompense intrinseci, habit sanatos"),
        lead("Product Lead","valoare perceputa, onboarding cu valoare imediata, next-step ghidat"),
        lead("Marketing Lead","comunicarea necesitatii/valorii din prima, limbaj cald, pozitionare"),
    ],"lead-uri")
    json.dump(leads,open(P("design_psiho_lead.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    leadbloc="\n".join(f"[{x['rol']}] {x['text']}" for x in leads if not x['text'].startswith("["))
    print("CPO sintetizeaza...",flush=True)
    cp=(f"Esti CPO. Ai condus o sedinta pe DESIGN + PSIHOLOGIE & COGNITIV (engagement ETIC).\n\n{STARE}\n\n"
        f"FEEDBACK DIRECTORI:\n{bloc}\n\nLEAD-URI DE SPECIALITATE:\n{leadbloc}\n\n"
        "Scrie DESIGN_PSIHO_REVIEW.md cu structura:\n"
        "## CE MERGE (5-7 puncte)\n## CE NU MERGE / LIPSESTE (5-7 puncte concrete)\n"
        "## PRINCIPII ETICE (5 reguli: ce NU facem — dark patterns interzise)\n"
        "## TOP 20 IMBUNATATIRI (lista numerotata 1-20, fiecare o linie scurta, concreta, fezabila "
        "single-file, prioritizate, ETICE — claritate/valoare/placere/retentie sanatoasa). "
        "Format exact: 'N. <imbunatatire>'.\nOnest, fara magie/integrari false, fara manipulare.")
    txt=await call(sem,cp,3800)
    open(P("DESIGN_PSIHO_REVIEW.md"),"w",encoding="utf-8").write("# Review Design + Psihologie & Cognitiv (engagement etic)\n\n"+txt)
    print("\n===== REVIEW (extras) =====\n"+txt[:1500]+"\n=====",flush=True)
    print("DESIGN_PSIHO_REVIEW_DONE",flush=True)
if __name__=="__main__": asyncio.run(main())
