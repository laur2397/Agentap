"""Sedinta 8 — BORD (directori + Cxx). Strategie pentru SECRETARA AI:
planificator de intalniri, idei, calendar, meet-uri, follow-up, agenda — tot ce face
o secretara intr-o firma. Output: SECRETARA_STRATEGIE.md. Poarta de audit la final.

Faze:
  A. Cei 18 directori: ce trebuie sa faca Secretara, din unghiul fiecaruia. -> sedinta8_directori.json
  B. Experti cheie (Product / AI / Behavioral) sintetizeaza capabilitatile. -> sedinta8_experti.json
  C. CPO: SECRETARA_STRATEGIE.md (viziune, capabilitati, roadmap onest single-file, securitate).
  D. Poarta de audit pe strategie (onestitate: fara 'magie' / integrari false).
"""
from __future__ import annotations
import asyncio, json, os, re, sys, time, urllib.request, urllib.error, itertools, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audit import audit_gate

KEYS=[k.strip() for k in os.environ.get("GEMINI_KEYS","").split(",") if k.strip()]
_rr=itertools.cycle(KEYS)
MODEL="gemini-flash-lite-latest"
LOT=6; PACE=6
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(f): return os.path.join(ROOT,f)

CONTEXT=(
 "PRODUS: 'Cercul EIE' — app mobila de business networking (Local-Only, criptata, client-side). "
 "Secretara AI ACTUALA face putin: scrii un text dupa o intalnire si extrage 'ce caut / ce ofer' pe "
 "cuvinte-cheie, apoi recalculeaza potriviri. Vrem sa o transformam intr-o SECRETARA COMPLETA, ca "
 "intr-o firma: planificator de intalniri, calendar, idei/notite, meet-uri, remindere, agenda inainte "
 "de intalnire, follow-up dupa, programare intre membri (cu dublu consimtamant). "
 "CONSTRANGERI: single-file HTML/JS, fara backend, fara integrari reale email/Google Calendar, fara LLM "
 "real (euristici locale). Orice capabilitate trebuie sa fie ONESTA — fara 'magie tehnologica'.")

def parse_roles(md_path):
    text=open(md_path,encoding="utf-8").read()
    dep_m=re.search(r"## (Departamentul .+)", text)
    dep=dep_m.group(1).strip() if dep_m else os.path.basename(md_path)
    parts=re.split(r"\n## (\d+\.\d+)\s+(.+)\n", text);roles=[]
    for i in range(1,len(parts),3):
        cod=parts[i].strip();nume=parts[i+1].strip();corp=parts[i+2][:900]
        roles.append({"cod":cod,"nume":nume,"ctx":corp,"dep":dep})
    return dep,roles
def leaders():
    out=[]
    for md in sorted(glob.glob(P("fise/Dep_*.md"))):
        _,roles=parse_roles(md)
        for r in roles:
            if r["cod"].endswith(".1"):out.append(r)
    return out

def _gen(key,prompt,mx):
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
    body=json.dumps({"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"maxOutputTokens":mx,"temperature":0.85}}).encode()
    with urllib.request.urlopen(urllib.request.Request(url,data=body,headers={"Content-Type":"application/json"}),timeout=120) as r:
        d=json.load(r)
    c=d["candidates"][0]
    if "content" not in c or "parts" not in c["content"]:return "[gol]"
    return "".join(p.get("text","") for p in c["content"]["parts"]).strip()
async def call(sem,prompt,mx=400):
    async with sem:
        res="[rate limit]"
        for a in range(3):
            key=next(_rr)
            try:res=await asyncio.to_thread(_gen,key,prompt,mx);break
            except urllib.error.HTTPError as e:
                if e.code in(429,503):await asyncio.sleep(min(50,4*(1.7**a)));continue
                res=f"[HTTP{e.code}]";break
            except Exception as e:res=f"[{type(e).__name__}]";break
        await asyncio.sleep(PACE);return res
async def gprog(coros,label):
    res=[];done=0;tot=len(coros)
    for f in asyncio.as_completed(coros):
        res.append(await f);done+=1
        if done%6==0 or done==tot:print(f"   {label}: {done}/{tot}",flush=True)
    return res

async def faza_a(sem):
    L=leaders();print(f"FAZA A — {len(L)} directori despre Secretara",flush=True)
    async def one(a):
        p=(f"SEDINTA DE BORD — strategie pentru SECRETARA AI.\n\n{CONTEXT}\n\nEsti acest director:\n{a['ctx']}\n\n"
           "Din unghiul departamentului tau, ce ar trebui sa faca Secretara (planificator intalniri, "
           "calendar, idei, meet-uri, remindere, agenda, follow-up)? Da 3 capabilitati CONCRETE si "
           "prioritizate, fezabile single-file, fara integrari false. Format:\n- <capabilitate: ce face + de ce conteaza>\nMax 55 cuvinte.")
        return {"rol":a["nume"],"dep":a["dep"],"input":await call(sem,p,420),"ok":True}
    res=await gprog([one(a) for a in L],"directori")
    json.dump(res,open(P("sedinta8_directori.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    return res

async def faza_b(sem,directori):
    print("FAZA B — experti (Product/AI/Behavioral) sintetizeaza",flush=True)
    bloc="\n".join(f"[{x['rol']}] {x['input']}" for x in directori if x["ok"] and not x["input"].startswith("["))
    experts=[("Head of Product","prioritizare, flux, valoare pt utilizator"),
             ("Head of AI","ce e fezabil cu euristici locale vs. ce ar cere LLM/backend; onestitate"),
             ("Behavioral Science Lead","reducerea efortului, remindere ne-intruzive, incredere")]
    async def one(e,lent):
        p=(f"Esti {e}. {CONTEXT}\n\nInputul bordului:\n{bloc}\n\nLentila ta: {lent}.\n"
           "Sintetizeaza capabilitatile Secretarei in 5-7 puncte concrete, marcand clar [FEZABIL ACUM single-file] "
           "vs [VIITOR necesita backend/LLM]. Onest, fara magie.")
        return {"expert":e,"sinteza":await call(sem,p,900)}
    res=await gprog([one(e,l) for e,l in experts],"experti")
    json.dump(res,open(P("sedinta8_experti.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    return res

async def faza_c(sem,directori,experti):
    print("FAZA C — CPO scrie SECRETARA_STRATEGIE.md",flush=True)
    d="\n".join(f"[{x['rol']}] {x['input']}" for x in directori if not x['input'].startswith("["))
    e="\n\n".join(f"### {x['expert']}\n{x['sinteza']}" for x in experti if not x['sinteza'].startswith("["))
    p=(f"Esti CPO. Ai condus bordul pe strategia Secretarei AI.\n\n{CONTEXT}\n\nINPUT DIRECTORI:\n{d[:4000]}\n\n"
       f"SINTEZE EXPERTI:\n{e[:4000]}\n\nScrie SECRETARA_STRATEGIE.md. Structura:\n"
       "1. VIZIUNE: ce devine Secretara (un chief-of-staff personal), in 3-4 randuri\n"
       "2. CAPABILITATI — grupate: (a) Calendar & Intalniri, (b) Idei & Notite, (c) Remindere & Follow-up, "
       "(d) Agenda & Pregatire, (e) Programare intre membri (cu dublu consimtamant). Pt fiecare: ce face concret.\n"
       "3. CE E FEZABIL ACUM (single-file, euristici locale) vs CE AMANAM (backend/LLM) — tabel onest\n"
       "4. UX: cum apare in app (ecranul Secretara + calendar), limbaj uman, ne-intruziv\n"
       "5. INCREDERE & LIMITARI declarate transparent\n"
       "6. ROADMAP: 3 pasi (iteratia urmatoare -> ...).\nConcret, onest, ambitios.")
    txt=await call(sem,p,4000)
    open(P("SECRETARA_STRATEGIE.md"),"w",encoding="utf-8").write("# Strategia Secretarei AI — sedinta de bord\n\n"+txt)
    print("\n===== STRATEGIE (extras) =====\n"+txt[:1500]+"\n=====",flush=True)
    return txt

async def main():
    if not KEYS:print("no GEMINI_KEYS");sys.exit(1)
    print(f"SEDINTA 8 (bord) cu {len(KEYS)} chei\n",flush=True)
    sem=asyncio.Semaphore(LOT);t0=time.time()
    directori=await faza_a(sem)
    experti=await faza_b(sem,directori)
    strat=await faza_c(sem,directori,experti)
    print("FAZA D — poarta de audit pe strategie",flush=True)
    g=await audit_gate(sem,solutie=("STRATEGIE DE EVALUAT (verifica ONESTITATEA: respinge orice 'magie' / "
        "integrari false / promisiuni nefezabile single-file; cere etichetare clara fezabil-acum vs viitor):\n"+strat),runda="s8strat")
    print(f"\nSEDINTA8_DONE in {time.time()-t0:.0f}s | audit {'APROBAT' if g['aprobat'] else 'RESPINS'}",flush=True)

if __name__=="__main__":asyncio.run(main())
