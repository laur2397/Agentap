"""Sedinta 2 — cei 220 de agenti REVIZUIESC prototipul construit (app/eie.html)
si fiecare propune, din rolul lui, imbunatatiri concrete pentru ITERATIA 2.

Faze:
  A. Fiecare agent (cu fisa lui) primeste descrierea EXACTA a prototipului construit
     si da O critica + O imbunatatire concreta din expertiza lui. -> sedinta2_contributii.json
  B. Fiecare departament: managerul sintetizeaza top fix-uri pentru iteratia 2. -> sedinta2_departamente.json
  C. Sinteza finala (CPO) -> ITERATIA_2.md (spec concreta de reconstructie)

Gemini, multi-cheie, ritmat. Reuseste parse_roles din logica sedinta.py.
"""
from __future__ import annotations
import asyncio, json, os, re, sys, time, urllib.request, urllib.error, itertools, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audit import audit_gate  # poarta de audit obligatorie la final

KEYS=[k.strip() for k in os.environ.get("GEMINI_KEYS","").split(",") if k.strip()]
_rr=itertools.cycle(KEYS)
MODEL="gemini-flash-lite-latest"
LOT=5; PACE=8
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(f): return os.path.join(ROOT,f)

# Descrierea EXACTA a prototipului construit (app/eie.html) — ce sa critice agentii.
PROTOTIP=(
 "PROTOTIP CONSTRUIT (app/eie.html) — 'Network Capital / EIE', aplicatie mobila premium "
 "dark+gold, single-file HTML/JS, localStorage, fara backend. 5 ecrane:\n"
 "1) ACASA: Focus Digest (rezumat zilnic oportunitati) + carduri KPI Exec-Concierge "
 "(Network Capital in EUR, ROI, Trust Score) + Network Health Pulse (bare de stare retea).\n"
 "2) POTRIVIRI: Graph Matchmaker — scor de afinitate, Verified Trust Score, motiv (why), "
 "sursa citata, flux de dublu consimtamant (accept/refuz ambele parti).\n"
 "3) RETEA: graf SVG simplu cu noduri/membri.\n"
 "4) SECRETARA AI: dictezi dupa apel -> extrage 'intentii de business' -> propune potriviri.\n"
 "5) PROFIL: ce ofer / ce caut + Trust Score.\n"
 "Date: 20 membri seed cu trust scores. Matching: overlap de cuvinte cheie (client-side). "
 "LIMITARI ACTUALE: fara backend real, fara auth, fara AI real (matching pe keyword overlap, "
 "nu graph/semantic), graf static, fara persistenta intre dispozitive, fara onboarding, "
 "fara securitate/criptare, fara teste, fara accesibilitate verificata.")

def parse_roles(md_path):
    text=open(md_path,encoding="utf-8").read()
    dep_m=re.search(r"## (Departamentul .+)", text)
    dep=dep_m.group(1).strip() if dep_m else os.path.basename(md_path)
    parts=re.split(r"\n## (\d+\.\d+)\s+(.+)\n", text)
    roles=[]
    for i in range(1,len(parts),3):
        cod=parts[i].strip(); nume=parts[i+1].strip(); corp=parts[i+2]
        m=re.search(r"\*\*Antet:\*\*\s*(\d+)\s+persoan", corp)
        count=int(m.group(1)) if m else 1
        ctx=corp[:1100]
        roles.append({"cod":cod,"nume":nume,"count":count,"ctx":ctx,"dep":dep})
    return dep, roles

def _gen(key, prompt, max_tokens):
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
    body=json.dumps({"contents":[{"parts":[{"text":prompt}]}],
        "generationConfig":{"maxOutputTokens":max_tokens,"temperature":0.8}}).encode()
    with urllib.request.urlopen(urllib.request.Request(url,data=body,headers={"Content-Type":"application/json"}),timeout=120) as r:
        d=json.load(r)
    c=d["candidates"][0]
    if "content" not in c or "parts" not in c["content"]: return "[gol]"
    return "".join(p.get("text","") for p in c["content"]["parts"]).strip()

async def call(sem, prompt, max_tokens=300):
    async with sem:
        res="[rate limit]"
        for a in range(3):
            key=next(_rr)
            try:
                res=await asyncio.to_thread(_gen,key,prompt,max_tokens); break
            except urllib.error.HTTPError as e:
                if e.code==429: await asyncio.sleep(min(50,4*(1.7**a))); continue
                res=f"[HTTP{e.code}]"; break
            except Exception as e:
                res=f"[{type(e).__name__}]"; break
        await asyncio.sleep(PACE)
        return res

async def gather_prog(coros,label):
    res=[];done=0;tot=len(coros)
    for f in asyncio.as_completed(coros):
        res.append(await f);done+=1
        if done%15==0 or done==tot: print(f"   {label}: {done}/{tot}",flush=True)
    return res

# ---- FAZA A: review individual al prototipului ----
async def faza_a(sem):
    print("FAZA A — toti cei 220 revizuiesc prototipul",flush=True)
    agents=[]
    for md in sorted(glob.glob(P("fise/Dep_*.md"))):
        dep,roles=parse_roles(md)
        for r in roles:
            for idx in range(1,r["count"]+1):
                agents.append({**r,"idx":idx})
    print(f"   {len(agents)} agenti in review",flush=True)
    async def one(a):
        p=(f"SEDINTA 2 — REVIEW PE PROTOTIP pentru iteratia 2.\n\n{PROTOTIP}\n\n"
           f"Esti acest angajat (fisa ta):\n{a['ctx']}\n\n"
           "Ia-ti rolul in serios. Din expertiza ta SPECIFICA, analizeaza prototipul de mai sus "
           "si raspunde STRICT in formatul:\n"
           "PROBLEMA: <un defect concret pe care il vezi tu, din rolul tau>\n"
           "FIX: <o imbunatatire concreta, implementabila in iteratia 2>\n"
           "Max 40 de cuvinte total. Fara generalitati, fara laude. La obiect.")
        txt=await call(sem,p,260)
        return {"cod":a["cod"],"rol":a["nume"],"dep":a["dep"],"idx":a["idx"],"review":txt,
                "ok":not txt.startswith("[")}
    res=await gather_prog([one(a) for a in agents],"review")
    json.dump(res,open(P("sedinta2_contributii.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"   -> {sum(1 for x in res if x['ok'])}/{len(res)} review-uri\n",flush=True)
    return res

# ---- FAZA B: sinteza pe departament ----
async def faza_b(sem,contrib):
    print("FAZA B — managerii sintetizeaza top fix-uri pe departament",flush=True)
    by_dep={}
    for x in contrib:
        if x["ok"]: by_dep.setdefault(x["dep"],[]).append(f"[{x['rol']}] {x['review']}")
    async def one(dep,items):
        bloc="\n".join(items[:40])
        p=(f"Esti managerul departamentului: {dep}.\n\n{PROTOTIP}\n\n"
           f"Review-urile echipei tale pe prototip:\n{bloc}\n\n"
           "Sintetizeaza pentru ITERATIA 2: cele mai importante 4-6 fix-uri/imbunatatiri "
           "concrete si implementabile pe care le cere departamentul tau. Prioritizate, "
           "specifice, fara generalitati.")
        return {"dep":dep,"sinteza":await call(sem,p,700)}
    res=await gather_prog([one(d,i) for d,i in by_dep.items()],"departamente")
    json.dump(res,open(P("sedinta2_departamente.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"   -> {len(res)} pozitii de departament\n",flush=True)
    return res

# ---- FAZA C: spec iteratia 2 ----
async def faza_c(sem,depts):
    print("FAZA C — spec iteratia 2 (CPO)",flush=True)
    bloc="\n\n".join(f"### {d['dep']}\n{d['sinteza']}" for d in depts if not d['sinteza'].startswith("["))
    p=(f"Esti CPO. Ai condus sedinta 2 — review pe prototipul construit.\n\n{PROTOTIP}\n\n"
       f"FIX-URILE CERUTE DE FIECARE DEPARTAMENT:\n{bloc}\n\n"
       "Scrie SPECIFICATIA ITERATIEI 2 — concreta si implementabila intr-un singur fisier "
       "HTML/JS imbunatatit. Structura:\n"
       "1. CE PASTRAM (ce merge bine in prototip)\n"
       "2. TOP 10 IMBUNATATIRI prioritizate (fiecare: ce, de ce, cum se vede in UI)\n"
       "3. SCHIMBARI DE EXPERIENTA & DESIGN (onboarding, fluiditate, accesibilitate)\n"
       "4. INCREDERE & DATE (ce facem credibil chiar si fara backend real)\n"
       "5. CE AMANAM explicit pentru iteratia 3 (si de ce)\n"
       "Concret, implementabil, reflecta munca a 220 de profesionisti.")
    txt=await call(sem,p,4000)
    open(P("ITERATIA_2.md"),"w",encoding="utf-8").write("# Iteratia 2 — spec din sedinta de review (220 agenti)\n\n"+txt)
    print("\n===== ITERATIA 2 (extras) =====\n"+txt[:1600]+"\n=====",flush=True)
    return txt

async def main():
    if not KEYS: print("no GEMINI_KEYS"); sys.exit(1)
    print(f"Sedinta 2 cu {len(KEYS)} chei Gemini\n",flush=True)
    sem=asyncio.Semaphore(LOT); t0=time.time()
    contrib=await faza_a(sem)
    depts=await faza_b(sem,contrib)
    txt=await faza_c(sem,depts)
    # FAZA D — poarta de audit: sedinta NU se incheie pana cand CAE nu aproba
    print("FAZA D — poarta de audit pe rezultatul sedintei",flush=True)
    g=await audit_gate(sem, solutie="SPEC PROPUS DE SEDINTA (de evaluat critic):\n"+txt, runda="s2")
    print(("SEDINTA2_DONE — AUDIT APROBAT" if g["aprobat"] else
           "SEDINTA2_INCHISA_NU — AUDIT RESPINS (vezi AUDIT_rundas2.md)")+f" in {time.time()-t0:.0f}s",flush=True)

if __name__=="__main__": asyncio.run(main())
