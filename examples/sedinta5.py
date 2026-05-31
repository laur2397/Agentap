"""Sedinta 5 — cei 220 de agenti, NEMULTUMIRI + IMBUNATATIRI pentru iteratia 3.
Accent maxim pe FUNCTIONALITATE si ASPECT VIZUAL. Auditorii nu inchid pana nu exista
o imbunatatire clar notabila si buna (poarta de audit obligatorie la final).

Faze:
  A. Fiecare din 220 da NEMULTUMIRE + IMBUNATATIRE (functional si/sau vizual). -> sedinta5_contributii.json
  B. 18 manageri sintetizeaza top imbunatatiri prioritizate. -> sedinta5_departamente.json
  C. CPO scrie ITERATIA_4.md (spec de imbunatatiri notabile).
  D. Poarta de audit pe spec — RESPINS daca imbunatatirea nu e clar notabila/implementabila.
"""
from __future__ import annotations
import asyncio, json, os, re, sys, time, urllib.request, urllib.error, itertools, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audit import audit_gate

KEYS=[k.strip() for k in os.environ.get("GEMINI_KEYS","").split(",") if k.strip()]
_rr=itertools.cycle(KEYS)
MODEL="gemini-flash-lite-latest"
LOT=8; PACE=6  # 6 chei -> concurenta mai mare
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(f): return os.path.join(ROOT,f)

# Starea ACTUALA (iteratia 2, dupa ce a trecut poarta de audit in 3 runde).
STARE=(
 "STARE ACTUALA — app/eie.html, iteratia 3 (a trecut auditul unanim 6/6). Aplicatie mobila premium "
 "single-file HTML/JS, Local-Only, criptata AES-GCM cu cheie PBKDF2 din parola (doar in RAM), "
 "integritate prin hash-chain SHA-256 vizibil si verificabil in Trust Ledger (buton Verifica + Export). "
 "Paleta 'Executive Hybrid' Light/Soft-Dark. IMBUNATATIRI deja livrate in iteratia 3: skeleton "
 "shimmer la tranzitii, contoare KPI animate (count-up), sparkline de tendinta in Focus Digest, "
 "Trust Score ca donut SVG, graf de retea INTERACTIV (hover evidentiaza vecinii) + cautare fuzzy in "
 "retea, empty-states SVG, micro-interactiuni, comutator reduce-animatii + prefers-reduced-motion, "
 "transparenta metodei de matching ('TF-IDF + cosine · N teme comune'). 5 ecrane (Acasa, Potriviri, "
 "Retea, Secretara AI, Profil), onboarding 3 pasi, 20 membri seed. LIMITARI RAMASE: fara backend; "
 "matching euristic (nu embeddings/LLM real); Secretara pe cuvinte-cheie; fara teste automate; "
 "fara mesagerie reala intre membri; fara notificari; fara filtrare avansata pe Potriviri; "
 "fara profil bogat (foto, istoric, recomandari); fara onboarding ghidat in app dupa prima rulare.")

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
        roles.append({"cod":cod,"nume":nume,"count":count,"ctx":corp[:1100],"dep":dep})
    return dep, roles

def _gen(key, prompt, max_tokens):
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
    body=json.dumps({"contents":[{"parts":[{"text":prompt}]}],
        "generationConfig":{"maxOutputTokens":max_tokens,"temperature":0.85}}).encode()
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

async def faza_a(sem):
    print("FAZA A — toti cei 220 dau nemultumiri + imbunatatiri",flush=True)
    agents=[]
    for md in sorted(glob.glob(P("fise/Dep_*.md"))):
        dep,roles=parse_roles(md)
        for r in roles:
            for idx in range(1,r["count"]+1): agents.append({**r,"idx":idx})
    print(f"   {len(agents)} agenti",flush=True)
    async def one(a):
        p=(f"SEDINTA 5 — vrem IMBUNATATIRI NOTABILE pentru iteratia 3.\n\n{STARE}\n\n"
           f"Esti acest angajat (fisa ta):\n{a['ctx']}\n\n"
           "Chinuie-te sa gasesti ce e cel mai slab si propune cea mai buna imbunatatire posibila din "
           "rolul tau, cu accent pe FUNCTIONALITATE si ASPECT VIZUAL. Fii pretentios. Raspunde STRICT:\n"
           "NEMULTUMIRE: <ce te deranjeaza concret azi>\n"
           "IMBUNATATIRE: <cea mai buna solutie concreta, implementabila intr-un singur fisier HTML/JS>\n"
           "TIP: <functional | vizual | ambele>\n"
           "Max 45 de cuvinte. Fara generalitati.")
        txt=await call(sem,p,300)
        return {"cod":a["cod"],"rol":a["nume"],"dep":a["dep"],"idx":a["idx"],"text":txt,"ok":not txt.startswith("[")}
    res=await gather_prog([one(a) for a in agents],"idei")
    json.dump(res,open(P("sedinta5_contributii.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"   -> {sum(1 for x in res if x['ok'])}/{len(res)} contributii\n",flush=True)
    return res

async def faza_b(sem,contrib):
    print("FAZA B — managerii sintetizeaza",flush=True)
    by_dep={}
    for x in contrib:
        if x["ok"]: by_dep.setdefault(x["dep"],[]).append(f"[{x['rol']}] {x['text']}")
    async def one(dep,items):
        bloc="\n".join(items[:40])
        p=(f"Esti managerul departamentului: {dep}.\n\n{STARE}\n\n"
           f"Nemultumirile si ideile echipei tale:\n{bloc}\n\n"
           "Sintetizeaza pentru ITERATIA 4 cele mai NOTABILE 4-6 imbunatatiri concrete cerute de "
           "departamentul tau, cu accent pe functionalitate si vizual. Prioritizate, specifice.")
        return {"dep":dep,"sinteza":await call(sem,p,700)}
    res=await gather_prog([one(d,i) for d,i in by_dep.items()],"departamente")
    json.dump(res,open(P("sedinta5_departamente.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"   -> {len(res)} pozitii\n",flush=True)
    return res

async def faza_c(sem,depts):
    print("FAZA C — CPO scrie ITERATIA_4.md",flush=True)
    bloc="\n\n".join(f"### {d['dep']}\n{d['sinteza']}" for d in depts if not d['sinteza'].startswith("["))
    p=(f"Esti CPO. Ai condus sedinta 4 de imbunatatire.\n\n{STARE}\n\n"
       f"PROPUNERILE DEPARTAMENTELOR:\n{bloc}\n\n"
       "Scrie SPECIFICATIA ITERATIEI 3 — imbunatatiri CLAR NOTABILE, implementabile intr-un singur "
       "fisier HTML/JS, fara backend. Structura:\n"
       "1. TOP 10 IMBUNATATIRI prioritizate (fiecare: ce, de ce conteaza, cum se vede in UI)\n"
       "2. IMBUNATATIRI VIZUALE (animatii, micro-interactiuni, stari goale, skeleton, ierarhie, "
       "rafinament premium) — concret\n"
       "3. IMBUNATATIRI FUNCTIONALE (matching, Secretara, retea, filtrare, cautare etc.) — concret\n"
       "4. CRITERIU DE SUCCES: cum se vede ca imbunatatirea e NOTABILA\n"
       "Ambitios dar implementabil. Reflecta munca a 220 de profesionisti.")
    txt=await call(sem,p,4000)
    open(P("ITERATIA_4.md"),"w",encoding="utf-8").write("# Iteratia 4 — spec din sedinta de imbunatatire (220 agenti)\n\n"+txt)
    print("\n===== ITERATIA 4 (extras) =====\n"+txt[:1500]+"\n=====",flush=True)
    return txt

async def main():
    if not KEYS: print("no GEMINI_KEYS"); sys.exit(1)
    print(f"Sedinta 5 cu {len(KEYS)} chei Gemini\n",flush=True)
    sem=asyncio.Semaphore(LOT); t0=time.time()
    contrib=await faza_a(sem)
    depts=await faza_b(sem,contrib)
    txt=await faza_c(sem,depts)
    # FAZA D — poarta de audit pe specul de imbunatatire
    print("FAZA D — poarta de audit pe specul iteratiei 4",flush=True)
    g=await audit_gate(sem, solutie=("SPEC DE IMBUNATATIRE PROPUS (evalueaza daca imbunatatirea e CLAR "
        "NOTABILA, concreta si implementabila; RESPINGE daca e vaga sau slaba):\n"+txt), runda="s5spec")
    print(("SEDINTA5_DONE — AUDIT APROBAT specul" if g["aprobat"] else
           "SEDINTA5 — AUDIT RESPINS specul (vezi AUDIT_rundas5spec.md)")+f" in {time.time()-t0:.0f}s",flush=True)

if __name__=="__main__": asyncio.run(main())
