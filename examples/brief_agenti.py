"""Briefing al agentilor cu fisa lor de post completa, pe Gemini (gratis).

Pentru fiecare fisier fise/Dep_XX.md:
  - parseaza sectiunile de rol (## N.N Nume + **Antet:** K persoane)
  - pentru fiecare persoana din rol, trimite fisa completa unui agent Gemini
    si cere confirmare de intelegere (rezumat in 2-3 propozitii)
  - salveaza confirmarile in fise/confirmari_DepXX.json

NU porneste proiectul. Doar briefing + confirmare.

Folosire:
    GEMINI_KEYS='k1,k2,k3' python examples/brief_agenti.py fise/Dep_01_Engineering.md
"""
from __future__ import annotations
import asyncio, json, os, re, sys, time, urllib.request, urllib.error, itertools

KEYS=[k.strip() for k in os.environ.get("GEMINI_KEYS","").split(",") if k.strip()]
_rr=itertools.cycle(KEYS)
MODEL="gemini-2.0-flash"   # free tier are RPM mai mare, fara overhead de thinking
LOT=3                       # cate o cerere per cheie, ritmat
PACE=4.5                    # secunde minim per slot (ramane sub limita RPM)

def parse_roles(md_path):
    """Extrage (cod, nume, count, fisa) din fisierul de departament."""
    text=open(md_path,encoding="utf-8").read()
    dep_m=re.search(r"## (Departamentul .+)", text)
    dep=dep_m.group(1).strip() if dep_m else os.path.basename(md_path)
    # imparte pe sectiuni de rol: "## N.N Nume"
    parts=re.split(r"\n## (\d+\.\d+)\s+(.+)\n", text)
    roles=[]
    # parts[0] e antetul; apoi triplete (cod, nume, corp)
    for i in range(1,len(parts),3):
        cod=parts[i].strip(); nume=parts[i+1].strip(); corp=parts[i+2]
        m=re.search(r"\*\*Antet:\*\*\s*(\d+)\s+persoan", corp)
        count=int(m.group(1)) if m else 1
        fisa=f"## {cod} {nume}\n{corp}".strip()
        roles.append({"cod":cod,"nume":nume,"count":count,"fisa":fisa,"dep":dep})
    return dep, roles

def _gen_sync(key, prompt, max_tokens=400):
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
    body=json.dumps({"contents":[{"parts":[{"text":prompt}]}],
        "generationConfig":{"maxOutputTokens":max_tokens,"temperature":0.4}}).encode()
    req=urllib.request.Request(url,data=body,headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=120) as r:
        d=json.load(r)
    c=d["candidates"][0]
    if "content" not in c or "parts" not in c["content"]: return "[gol]"
    return "".join(p.get("text","") for p in c["content"]["parts"]).strip()

async def brief_one(sem, dep, rol, idx):
    prompt=(
        f"Esti angajat intr-o firma IT care dezvolta o aplicatie mobila B2C. "
        f"{dep}. Mai jos este FISA TA DE POST completa. Citeste-o cu atentie.\n\n"
        f"{rol['fisa']}\n\n"
        "Confirma ca ai inteles rolul tau. Raspunde STRICT in formatul:\n"
        "CONFIRM. Rol: <numele rolului>. Voi: <2-3 propozitii cu ce vei face si "
        "care e contributia ta principala, plus 1 KPI dupa care vei fi masurat>."
    )
    async with sem:
        result=None
        for a in range(9):
            key=next(_rr)
            try:
                txt=await asyncio.to_thread(_gen_sync,key,prompt,500)
                ok=txt.upper().startswith("CONFIRM")
                result={"rol":rol['nume'],"cod":rol['cod'],"persoana":idx,"confirmare":txt,"ok":ok}
                break
            except urllib.error.HTTPError as e:
                if e.code==429: await asyncio.sleep(min(60,4*(1.7**a))); continue
                result={"rol":rol['nume'],"cod":rol['cod'],"persoana":idx,"confirmare":f"[HTTP{e.code}]","ok":False}; break
            except Exception as e:
                result={"rol":rol['nume'],"cod":rol['cod'],"persoana":idx,"confirmare":f"[{type(e).__name__}]","ok":False}; break
        if result is None:
            result={"rol":rol['nume'],"cod":rol['cod'],"persoana":idx,"confirmare":"[rate limit]","ok":False}
        await asyncio.sleep(PACE)  # ritmare ca sa ramanem sub limita
        return result

async def run(md_path):
    dep, roles=parse_roles(md_path)
    total=sum(r["count"] for r in roles)
    print(f"{dep}: {len(roles)} roluri, {total} persoane",flush=True)
    sem=asyncio.Semaphore(LOT)
    tasks=[]
    for r in roles:
        for idx in range(1,r["count"]+1):
            tasks.append(brief_one(sem,dep,r,idx))
    res=[];done=0
    for f in asyncio.as_completed(tasks):
        res.append(await f);done+=1
        if done%10==0 or done==len(tasks): print(f"   briefati: {done}/{len(tasks)}",flush=True)
    out=md_path.replace(".md","_confirmari.json")
    json.dump(res,open(out,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    ok=sum(1 for x in res if x["ok"])
    print(f"   -> {ok}/{len(res)} au CONFIRMAT. Salvat: {out}",flush=True)
    return res

def main():
    if not KEYS: print("no GEMINI_KEYS"); sys.exit(1)
    if len(sys.argv)<2: print("dai calea catre fisierul Dep_XX.md"); sys.exit(1)
    asyncio.run(run(sys.argv[1]))
    print("BRIEF_DONE",flush=True)

if __name__=="__main__": main()
