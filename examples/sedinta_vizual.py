"""Sedinta VIZUALA — panelul VEDE aplicatia (capturi reale via Gemini vision).
Designeri de top + psihologi + investitori + bord analizeaza partea VIZUALA. Apoi CDO sintetizeaza.
Output: VIZUAL_REVIEW.md (scor agregat, ce merge / ce strica, TOP imbunatatiri vizuale prioritizate).
Onest: feedback simulat (modele multimodale), stress-test vizual. Nimic nu trece de poarta de audit fara APROBAT.
"""
from __future__ import annotations
import asyncio, json, os, re, sys, base64, io, urllib.request, urllib.error, itertools
from PIL import Image
KEYS=[k.strip() for k in os.environ.get("GEMINI_KEYS","").split(",") if k.strip()]
_rr=itertools.cycle(KEYS); MODEL="gemini-flash-lite-latest"; LOT=3; PACE=7
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(f): return os.path.join(ROOT,f)
SHOTS_DIR=os.environ.get("SHOTS","/tmp/shots")
SHOTS=[("01_lock.png","Ecran de start / blocare"),("03_acasa.png","Acasă"),
       ("04_potriviri.png","Potriviri"),("05_retea.png","Rețea"),
       ("06_secretara.png","Secretara"),("07_profil.png","Profil")]

def load_imgs():
    parts=[]
    for fn,label in SHOTS:
        p=os.path.join(SHOTS_DIR,fn)
        if not os.path.exists(p): continue
        im=Image.open(p).convert("RGB")
        w=440; im=im.resize((w,int(im.height*w/im.width)))
        b=io.BytesIO(); im.save(b,format="JPEG",quality=82)
        parts.append((label,base64.b64encode(b.getvalue()).decode()))
    return parts
IMGS=load_imgs()

STARE=("PRODUS: 'Cercul EIE' — app mobila PREMIUM de business networking, confidentialitate-first (E2EE), "
 "design system 'Bloom' (fundal deschis, accent indigo, font Inter, light+dark). Atasez CAPTURI REALE ale "
 "ecranelor in ordine: "+", ".join(f"{i+1}) {l}" for i,(l,_) in enumerate(IMGS))+". "
 "Pozitionare: premium, de incredere, pentru profesionisti/antreprenori. Trebuie sa arate a produs serios, "
 "nu a prototip/hobby; sa comunice valoarea din 5 secunde; sa fie placut si usor de scanat.")

ARCH=[
 ("Director de Brand & Identitate vizuala","coerenta de brand, premium real, memorabilitate, prima impresie"),
 ("Lead UI Visual Designer","ierarhie vizuala, spacing/grila, aliniere, tipografie, contrast, densitate"),
 ("Specialist Design Systems","consistenta componente/tokens/stari, reutilizare, rigoare vizuala"),
 ("Motion & Interaction Designer","affordances, feedback, claritate a actiunilor, stari interactive"),
 ("Editorial & Typography Designer","tipografie, lizibilitate, ton editorial, lungime de rand"),
 ("Psiholog cognitiv","incarcatura cognitiva, claritate in 5s, scanabilitate, ce vede ochiul intai"),
 ("Psiholog al culorii si increderii","paleta, semnale de incredere, raspuns emotional, premium perceput"),
 ("Psiholog comportamental","prima impresie, fricitiune perceputa, atractie, dorinta de a continua"),
 ("Investitor (look fundabil)","arata a produs de scara / finantabil sau a hobby? diferentiere vizuala"),
 ("Investitor consumer/brand","diferentiere vizuala vs LinkedIn/incumbenti, apetit de adoptie"),
 ("Membru de bord / CEO","coerenta cu pozitionarea premium, incredere, maturitate vizuala"),
 ("Specialist Accesibilitate vizuala","contrast, dimensiuni de atingere, daltonism, lizibilitate"),
]

def _gen(key,prompt,mx):
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
    parts=[{"text":prompt}]+[{"inlineData":{"mimeType":"image/jpeg","data":d}} for _,d in IMGS]
    body=json.dumps({"contents":[{"parts":parts}],"generationConfig":{"maxOutputTokens":mx,"temperature":0.8}}).encode()
    with urllib.request.urlopen(urllib.request.Request(url,data=body,headers={"Content-Type":"application/json"}),timeout=180) as r: d=json.load(r)
    c=d["candidates"][0]
    if "content" not in c or "parts" not in c["content"]: return "[gol]"
    return "".join(p.get("text","") for p in c["content"]["parts"]).strip()
async def call(sem,prompt,mx=420):
    async with sem:
        res="[rate limit]"
        for a in range(4):
            key=next(_rr)
            try: res=await asyncio.to_thread(_gen,key,prompt,mx);break
            except urllib.error.HTTPError as e:
                if e.code in(429,503): await asyncio.sleep(min(50,5*(1.8**a)));continue
                res=f"[HTTP{e.code}]";break
            except Exception as e: res=f"[{type(e).__name__}]";break
        await asyncio.sleep(PACE);return res
async def gprog(coros,label):
    out=[];d=0;t=len(coros)
    for f in asyncio.as_completed(coros):
        out.append(await f);d+=1
        if d%3==0 or d==t: print(f"   {label}: {d}/{t}",flush=True)
    return out
SCORE_RE=re.compile(r"SCOR\s*[:\-]?\s*(\d+(?:[.,]\d+)?)",re.I)
def parse_score(t):
    m=SCORE_RE.search(t or "");
    if not m: return None
    try: return float(m.group(1).replace(",","."))
    except: return None

async def main():
    if not KEYS: print("no GEMINI_KEYS"); sys.exit(1)
    if not IMGS: print("no screenshots in "+SHOTS_DIR); sys.exit(1)
    print(f"Sedinta VIZUALA — {len(ARCH)} experti vad {len(IMGS)} ecrane",flush=True)
    sem=asyncio.Semaphore(LOT)
    async def one(i):
        rol,lens=ARCH[i]
        p=(f"Esti '{rol}'. Lentila ta: {lens}.\n\n{STARE}\n\n"
           "PRIVESTE CU ATENTIE capturile atasate si evalueaza STRICT partea VIZUALA (nu functiile). "
           "Fii exigent, la nivel de top mondial. Raspunde STRICT:\n"
           "SCOR: <0-10, cat de bine arata vizual>\n"
           "VERDICT VIZUAL: GATA | REFACERE\n"
           "CE MERGE: <ce arata bine, concret, ce ai vazut>\n"
           "CE STRICA: <cel mai mare defect vizual concret pe care l-ai VAZUT>\n"
           "TOP FIX: <o singura schimbare vizuala concreta, fezabila>\nMax 75 cuvinte.")
        return {"rol":rol,"text":await call(sem,p,420)}
    res=await gprog([one(i) for i in range(len(ARCH))],"experti")
    json.dump(res,open(P("vizual_panel_raw.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    ok=[r for r in res if not r["text"].startswith("[")]
    scores=[s for s in (parse_score(r["text"]) for r in ok) if s is not None]
    avg=round(sum(scores)/len(scores),2) if scores else None
    gata=sum(1 for r in ok if re.search(r"VERDICT\s*VIZUAL\s*[:\-]?\s*GATA",r["text"],re.I))
    print(f"\nSCOR MEDIU: {avg}/10 | GATA: {gata}/{len(ok)} | refacere: {len(ok)-gata}",flush=True)
    bloc="\n\n".join(f"[{r['rol']}]\n{r['text']}" for r in ok)
    if len(bloc)>20000: bloc=bloc[:20000]
    cdo=(f"Esti CHIEF DESIGN OFFICER. Ai condus o sedinta VIZUALA in care {len(ok)} experti (designeri, psihologi, "
        f"investitori, bord) au VAZUT capturile reale.\n\n{STARE}\n\nSCOR MEDIU: {avg}/10. GATA: {gata}/{len(ok)}.\n\n"
        f"FEEDBACK:\n{bloc}\n\nScrie VIZUAL_REVIEW.md, ONEST, structura EXACTA:\n"
        "## SCOR VIZUAL AGREGAT (nota /10 + concluzie in 2 fraze)\n"
        "## CE MERGE VIZUAL (5-7 puncte)\n## CE STRICA VIZUAL (5-7 defecte concrete, prioritizate)\n"
        "## TOP 15 IMBUNATATIRI VIZUALE (numerotat 1-15, fiecare o linie scurta, concreta, fezabila "
        "single-file HTML/CSS, prioritizate dupa impact vizual). Format: 'N. <fix>'.\n"
        "## VERDICT (GATA DE LANSARE VIZUAL / MAI E DE LUCRU + ce anume blocheaza)\nFara complezenta.")
    print("CDO sintetizeaza...",flush=True)
    txt=await call(sem,cdo,4000)
    head=f"# VIZUAL_REVIEW — {len(ok)} experti au vazut aplicatia (scor mediu {avg}/10, GATA {gata}/{len(ok)})\n\n"
    open(P("VIZUAL_REVIEW.md"),"w",encoding="utf-8").write(head+txt)
    print("\n===== VIZUAL_REVIEW (extras) =====\n"+txt[:1800]+"\n=====",flush=True)
    print("VIZUAL_REVIEW_DONE",flush=True)
if __name__=="__main__": asyncio.run(main())
