"""Sedinta 3 — BOARD VIZUAL. Doar directorii de departamente + nivelul Cxx.
Scop: regandirea CULORILOR si a psihologiei vizuale a aplicatiei pentru o varianta
mult mai atractiva, placuta ochiului, care sa capteze cat mai multi utilizatori.

Participanti: cei 18 sefi de departament (rolul X.1 din fiecare fisa) = directori + Cxx.
Design Lead si Behavioral Science Lead au rol special in faza B.

Faze:
  A. Fiecare director da directia vizuala din unghiul lui (conversie, incredere, brand...). -> sedinta3_directori.json
  B. Design Lead + Behavioral Science Lead propun 3 PALETE concrete (hex), pe baza inputului. -> sedinta3_palete.json
  C. CPO/CEO alege si scrie specul final -> PALETA_VIZUALA.md (tokens hex + psihologie + utilizare).
"""
from __future__ import annotations
import asyncio, json, os, re, sys, time, urllib.request, urllib.error, itertools, glob

KEYS=[k.strip() for k in os.environ.get("GEMINI_KEYS","").split(",") if k.strip()]
_rr=itertools.cycle(KEYS)
MODEL="gemini-flash-lite-latest"
LOT=5; PACE=8
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(f): return os.path.join(ROOT,f)

APP=("'Network Capital / EIE' — aplicatie mobila premium de business networking pentru un cerc "
  "privat de oameni de afaceri (potriviri inteligente, Secretara AI, Trust Score, dublu consimtamant).")

# Paleta ACTUALA a prototipului (app/eie.html) — punct de plecare pentru regandire.
PALETA_ACTUALA=(
 "PALETA ACTUALA (dark+gold, prototip): fundal aproape negru #0a0b0f / #0f1118, carduri #14161f, "
 "linii #262a39, text #f2efe7, accent auriu #c9a227 / #e0c463, accente secundare teal #54c2a0, "
 "albastru #6ea8fe, rosu #e0736b. Fonturi: Cormorant Garamond (serif) + Jost (sans). "
 "FEEDBACK: prea intunecata si 'grea', auriul pe negru pare elitist dar rece; vrem o varianta "
 "mult mai placuta ochiului, primitoare, care sa atraga si sa retina cat mai multi utilizatori, "
 "fara sa piarda aerul premium de business.")

def parse_roles(md_path):
    text=open(md_path,encoding="utf-8").read()
    dep_m=re.search(r"## (Departamentul .+)", text)
    dep=dep_m.group(1).strip() if dep_m else os.path.basename(md_path)
    parts=re.split(r"\n## (\d+\.\d+)\s+(.+)\n", text)
    roles=[]
    for i in range(1,len(parts),3):
        cod=parts[i].strip(); nume=parts[i+1].strip(); corp=parts[i+2]
        ctx=corp[:900]
        roles.append({"cod":cod,"nume":nume,"ctx":ctx,"dep":dep})
    return dep, roles

def leaders():
    """Sefii de departament = rolul X.1 din fiecare fisa (directori + Cxx)."""
    out=[]
    for md in sorted(glob.glob(P("fise/Dep_*.md"))):
        dep,roles=parse_roles(md)
        for r in roles:
            if r["cod"].endswith(".1"):
                out.append(r)
    return out

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
        if done%5==0 or done==tot: print(f"   {label}: {done}/{tot}",flush=True)
    return res

# ---- FAZA A: directia vizuala de la fiecare director ----
async def faza_a(sem):
    print("FAZA A — directorii dau directia vizuala",flush=True)
    L=leaders()
    print(f"   {len(L)} directori in board",flush=True)
    async def one(a):
        p=(f"BOARD VIZUAL. Produs: {APP}\n\n{PALETA_ACTUALA}\n\n"
           f"Esti acest director (fisa ta):\n{a['ctx']}\n\n"
           "Din unghiul departamentului tau, ce DIRECTIE CROMATICA si vizuala face aplicatia "
           "mult mai atractiva si placuta ochiului, ca sa captam cat mai multi utilizatori, "
           "pastrand aerul premium de business? Raspunde STRICT:\n"
           "DIRECTIE: <ton/atmosfera dorita>\n"
           "CULORI: <2-3 culori cheie, ideal cu hex aproximativ>\n"
           "DE CE (din rolul meu): <argument scurt, masurabil daca se poate>\n"
           "Max 45 de cuvinte total.")
        txt=await call(sem,p,300)
        return {"cod":a["cod"],"rol":a["nume"],"dep":a["dep"],"input":txt,"ok":not txt.startswith("[")}
    res=await gather_prog([one(a) for a in L],"directori")
    json.dump(res,open(P("sedinta3_directori.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"   -> {sum(1 for x in res if x['ok'])}/{len(res)} directori\n",flush=True)
    return res

# ---- FAZA B: Design Lead + Behavioral propun 3 palete concrete ----
async def faza_b(sem,directori):
    print("FAZA B — Design Lead + Behavioral propun 3 palete (hex)",flush=True)
    bloc="\n".join(f"[{x['rol']}] {x['input']}" for x in directori if x["ok"])
    async def one(expert,lentila):
        p=(f"Esti {expert} intr-o firma IT de top. Produs: {APP}\n\n{PALETA_ACTUALA}\n\n"
           f"Inputul board-ului de directori:\n{bloc}\n\n"
           f"{lentila}\n"
           "Propune 3 PALETE concrete, fiecare in format EXACT:\n"
           "PALETA <nume>:\n"
           "  bg=#hex; surface=#hex; primary=#hex; accent=#hex; text=#hex; text2=#hex; success=#hex\n"
           "  psihologie: <1 rand — ce emotie/perceptie induce si de ce atrage utilizatori>\n"
           "  mod: <light / dark / soft-dark>\n"
           "Culori placute ochiului, contrast bun, premium dar primitoare.")
        return {"expert":expert,"palete":await call(sem,p,1400)}
    experts=[
      ("Design Lead","Lentila ta: estetica, ierarhie vizuala, contrast accesibil (WCAG), coerenta de brand premium."),
      ("Behavioral Science Lead","Lentila ta: psihologia culorii, incredere, reducerea fricii, atractie si retentie (capteaza utilizatori)."),
    ]
    res=await gather_prog([one(e,l) for e,l in experts],"experti")
    json.dump(res,open(P("sedinta3_palete.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"   -> {len(res)} seturi de palete\n",flush=True)
    return res

# ---- FAZA C: decizia finala (CPO/CEO) ----
async def faza_c(sem,directori,palete):
    print("FAZA C — decizia finala (CPO/CEO)",flush=True)
    dblock="\n".join(f"[{x['rol']}] {x['input']}" for x in directori if x["ok"])
    pblock="\n\n".join(f"### Propunerile {x['expert']}\n{x['palete']}" for x in palete if not x['palete'].startswith("["))
    p=(f"Esti CPO/CEO. Ai condus board-ul vizual. Produs: {APP}\n\n{PALETA_ACTUALA}\n\n"
       f"DIRECTIA DIRECTORILOR:\n{dblock}\n\nPROPUNERILE EXPERTILOR:\n{pblock}\n\n"
       "DECIDE paleta finala (poti combina). Scrie specul de implementare. Structura:\n"
       "1. DECIZIE: numele directiei alese + de ce capteaza utilizatori\n"
       "2. TOKENS (valori hex EXACTE, gata de pus in CSS):\n"
       "   --bg, --bg2, --card, --card2, --line, --ink, --ink2, --muted, --primary, --accent, "
       "--success, --warn — fiecare cu hex\n"
       "3. PSIHOLOGIE: ce induce fiecare culoare cheie (incredere, caldura, premium, actiune)\n"
       "4. UTILIZARE: unde se foloseste fiecare (fundal, carduri, butoane, scoruri, alerte)\n"
       "5. ACCESIBILITATE: contrast text/fundal, mod (light/soft-dark)\n"
       "Concret, gata de implementat intr-un singur fisier HTML/CSS.")
    txt=await call(sem,p,3000)
    open(P("PALETA_VIZUALA.md"),"w",encoding="utf-8").write("# Paleta vizuala — board directori + Cxx\n\n"+txt)
    print("\n===== PALETA (extras) =====\n"+txt[:1600]+"\n=====",flush=True)
    return txt

async def main():
    if not KEYS: print("no GEMINI_KEYS"); sys.exit(1)
    print(f"Board vizual cu {len(KEYS)} chei Gemini\n",flush=True)
    sem=asyncio.Semaphore(LOT); t0=time.time()
    directori=await faza_a(sem)
    palete=await faza_b(sem,directori)
    await faza_c(sem,directori,palete)
    print(f"\nSEDINTA3_DONE in {time.time()-t0:.0f}s",flush=True)

if __name__=="__main__": asyncio.run(main())
