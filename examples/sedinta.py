"""Sedinta generala cu toti cei 220 de agenti — regandirea aplicatiei.

Faze:
  A. Fiecare agent (cu fisa lui) contribuie din rolul lui la regandirea aplicatiei
     pentru standarde de firma IT de top. -> sedinta_contributii.json
  B. Fiecare departament: managerul sintetizeaza pozitia departamentului. -> sedinta_departamente.json
  C. Sinteza finala (CPO) -> REGANDIRE_APLICATIE.md

Foloseste fisele din fise/Dep_*.md (parsate pe rol). Gemini, multi-cheie, ritmat.
"""
from __future__ import annotations
import asyncio, json, os, re, sys, time, urllib.request, urllib.error, itertools, glob

KEYS=[k.strip() for k in os.environ.get("GEMINI_KEYS","").split(",") if k.strip()]
_rr=itertools.cycle(KEYS)
MODEL="gemini-flash-lite-latest"
LOT=5; PACE=8
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(f): return os.path.join(ROOT,f)

APP=("Aplicatie mobila B2C privata de business networking pentru un cerc de oameni de afaceri: "
  "aduna ce ofera / ce cauta fiecare membru, face potriviri inteligente si propune conexiuni "
  "cu dublu consimtamant si sursa mereu citata. Ecrane: Potriviri, Grupuri, Profil, Dicteaza dupa apel, Secretara AI.")

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
        # extrag misiunea + responsabilitatile pentru context (compact)
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

# ---- FAZA A: contributii individuale ----
async def faza_a(sem):
    print("FAZA A — toti cei 220 contribuie in sedinta",flush=True)
    agents=[]
    for md in sorted(glob.glob(P("fise/Dep_*.md"))):
        dep,roles=parse_roles(md)
        for r in roles:
            for idx in range(1,r["count"]+1):
                agents.append({**r,"idx":idx})
    print(f"   {len(agents)} agenti in sedinta",flush=True)
    async def one(a):
        p=(f"SEDINTA GENERALA de regandire a produsului.\n\nPRODUS:\n{APP}\n\n"
           f"Esti acest angajat (fisa ta):\n{a['ctx']}\n\n"
           "Ia-ti rolul in serios. Din expertiza ta specifica, da O contributie CONCRETA si "
           "profesionista la regandirea aplicatiei pentru a o ridica la standardele unei firme "
           "IT de top (200+ oameni). Max 45 cuvinte, la obiect, fara generalitati. "
           "Format: <contributia ta>.")
        txt=await call(sem,p,260)
        return {"cod":a["cod"],"rol":a["nume"],"dep":a["dep"],"idx":a["idx"],"contributie":txt,
                "ok":not txt.startswith("[")}
    res=await gather_prog([one(a) for a in agents],"contributii")
    json.dump(res,open(P("sedinta_contributii.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"   -> {sum(1 for x in res if x['ok'])}/{len(res)} contributii\n",flush=True)
    return res

# ---- FAZA B: sinteza pe departament ----
async def faza_b(sem,contrib):
    print("FAZA B — managerii sintetizeaza pe departament",flush=True)
    by_dep={}
    for x in contrib:
        if x["ok"]: by_dep.setdefault(x["dep"],[]).append(f"[{x['rol']}] {x['contributie']}")
    async def one(dep,items):
        bloc="\n".join(items[:40])
        p=(f"Esti managerul departamentului: {dep}.\nProdus: {APP}\n\n"
           f"Contributiile echipei tale in sedinta:\n{bloc}\n\n"
           "Sintetizeaza POZITIA departamentului: cele mai importante 4-6 propuneri concrete "
           "ale departamentului tau pentru ca aplicatia sa fie la standarde de firma de top. "
           "Lista scurta, profesionista.")
        return {"dep":dep,"sinteza":await call(sem,p,700)}
    res=await gather_prog([one(d,i) for d,i in by_dep.items()],"departamente")
    json.dump(res,open(P("sedinta_departamente.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"   -> {len(res)} pozitii de departament\n",flush=True)
    return res

# ---- FAZA C: sinteza finala ----
async def faza_c(sem,depts):
    print("FAZA C — sinteza finala (CPO)",flush=True)
    bloc="\n\n".join(f"### {d['dep']}\n{d['sinteza']}" for d in depts if not d['sinteza'].startswith("["))
    p=(f"Esti CPO-ul unei firme IT de top (200+ oameni). Ai condus o sedinta generala de "
       f"regandire a produsului.\n\nPRODUS:\n{APP}\n\nPOZITIILE TUTUROR DEPARTAMENTELOR:\n{bloc}\n\n"
       "Sintetizeaza REGANDIREA APLICATIEI la standardele unei firme IT de top. Structura:\n"
       "1. VIZIUNE (3-4 randuri): ce devine produsul, de ce e la nivel de top\n"
       "2. ARHITECTURA & TEHNOLOGIE (input Engineering/DevOps/AI/Securitate)\n"
       "3. EXPERIENTA & PRODUS (Produs/Design/Behavioral - etic, premium)\n"
       "4. INCREDERE & CONFORMITATE (Securitate/Legal/Privacy)\n"
       "5. CRESTERE & OPERARE (Marketing/Sales/CS/Data/Finance/Ops)\n"
       "6. CELE 8 FUNCTII-CHEIE ale aplicatiei regandite\n"
       "7. STANDARDE DE CALITATE adoptate (din QA/SRE/PMO)\n"
       "Concret si ambitios — reflecta munca a 220 de profesionisti.")
    txt=await call(sem,p,4000)
    open(P("REGANDIRE_APLICATIE.md"),"w",encoding="utf-8").write("# Regandirea aplicatiei — sedinta cu 220 de agenti\n\n"+txt)
    print("\n===== REGANDIRE (extras) =====\n"+txt[:1600]+"\n=====",flush=True)
    return txt

async def main():
    if not KEYS: print("no GEMINI_KEYS"); sys.exit(1)
    print(f"Sedinta cu {len(KEYS)} chei Gemini\n",flush=True)
    sem=asyncio.Semaphore(LOT); t0=time.time()
    contrib=await faza_a(sem)
    depts=await faza_b(sem,contrib)
    await faza_c(sem,depts)
    print(f"\nSEDINTA_DONE in {time.time()-t0:.0f}s",flush=True)

if __name__=="__main__": asyncio.run(main())
