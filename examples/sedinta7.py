"""Sedinta 7 — URGENTA. Toti cei 220, grupuri de lucru, schimb de idei intre grupuri,
vot de consens (absolut toti) si AUDIT mai dur ca niciodata. Tinta: redesign social,
luminos, modern (nu bancar), pe baza unui exemplu vizual + cele 7 reprosuri ale clientului.

Faze:
  A. 220 agenti: fiecare 2-3 imbunatatiri concrete aliniate la tinta. -> sedinta7_idei.json
  B. 18 grupuri de lucru (manageri): sinteza grupului. -> sedinta7_grupuri.json
  C. Schimb de idei INTRE grupuri: fiecare grup reactioneaza la digestul celorlalte. -> sedinta7_schimb.json
  D. CPO: spec redesign. -> ITERATIA_5.md
  E. Consens: toti 220 voteaza DE ACORD / OBIECTIE. -> sedinta7_consens.json
  F. Poarta de audit (mai dura) pe spec. -> AUDIT_rundas7spec.md
"""
from __future__ import annotations
import asyncio, json, os, re, sys, time, urllib.request, urllib.error, itertools, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit as AUD
from audit import audit_gate

KEYS=[k.strip() for k in os.environ.get("GEMINI_KEYS","").split(",") if k.strip()]
_rr=itertools.cycle(KEYS)
MODEL="gemini-flash-lite-latest"
LOT=8; PACE=5
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(f): return os.path.join(ROOT,f)

VIZUAL=(
 "TINTA VIZUALA (exemplu aprobat de client — stil 'Bloom/Clay CRM'): tema LUMINOASA, fundaluri "
 "albe/aproape-albe, mult spatiu alb (airy), carduri curate cu colturi rotunjite si umbre foarte "
 "subtile; accent VIU indigo-violet (~#5B5BD6/#6366F1) folosit cu masura; avataruri/logo-uri de "
 "organizatii colorate (patrate rotunjite, fiecare cu culoarea si glyph-ul ei); tipografie SANS "
 "MODERNA (Inter/SF-like), titluri compacte si bold, NU serif mare; statusuri ca pastile cu bulina "
 "colorata (Prospect, Meeting); navigatie jos cu iconite; ecrane de tip: timeline 'Upcoming' cu "
 "banda de zile + intalniri/apeluri, profil persoana (avatar, nume, titlu, actiuni clare), liste de "
 "organizatii, detaliu intalnire. Senzatie: prietenos, social, energic, clar, contemporan — opusul "
 "unui portal bancar/audit sepia.")

CLIENT=(
 "REPROSURILE CLIENTULUI (nemultumit total de varianta actuala):\n"
 "1. Arata prea 'bancar', nu social — paleta crem/maro/gri pare private-banking/compliance, distanta. "
 "Vrem energie, claritate, apropiere.\n"
 "2. Prea mult text tehnic la suprafata (TF-IDF, SHA-256, Trust Ledger, deal flow, ROI, '1 semnale', "
 "dublu consimtamant). Traduce in limbaj uman, actionabil. Ex: in loc de 'metoda: TF-IDF+cosine·1 teme "
 "comune' -> 'Aveti interese complementare in energie si infrastructura'.\n"
 "3. Ierarhie vizuala neclara — cardul incearca sa spuna totul deodata. In 2 secunde sa transmita: "
 "'Bogdan cauta furnizor de carbune. Tu ai legatura relevanta. Merita contactat.' Restul, in detalii.\n"
 "4. Carduri prea mari si pasive — actiuni clare: Trimite mesaj / Cere introducere / Vezi profil / "
 "Salveaza / Ignora. 'Conectat' e STATUS, nu actiune — tratat vizual diferit de un buton.\n"
 "5. Fonturile elegante dar nu moderne — mai putin serif, sans modern pt interfata, serif doar pt brand; "
 "titluri compacte; claritate in cifre si statusuri.\n"
 "6. Culori prea 'prafuite'/sepia — lipsesc accent puternic, gradient contemporan, stari vizuale clare, "
 "micro-interactiuni. Verdele de Trust pare medical, nu premium.\n"
 "7. Prea multa 'incredere calculata', prea putina relatie umana — oamenii par active financiare. "
 "Adauga context personal, motiv concret de introducere, cine garanteaza, ce poate iesi, de ce acum. "
 "In loc de 'Afinitate 68' -> 'Potrivire buna: aveti 3 interese comune si o conexiune verificata'.")

STARE=("STARE ACTUALA — app/eie.html iteratia 4: tema dark+sepia 'Executive Hybrid', mult jargon vizibil, "
 "carduri mari pasive, serif mare, scoruri peste tot (Trust/Afinitate/Network Capital/ROI/Health Pulse). "
 "Functii: potriviri (TF-IDF), graf force-directed, Secretara AI, Trust Ledger HMAC, profil. "
 "Tot client-side, criptat. Trebuie REGANDIT vizual si ca limbaj catre tinta luminoasa/sociala de mai sus.")

def parse_roles(md_path):
    text=open(md_path,encoding="utf-8").read()
    dep_m=re.search(r"## (Departamentul .+)", text)
    dep=dep_m.group(1).strip() if dep_m else os.path.basename(md_path)
    parts=re.split(r"\n## (\d+\.\d+)\s+(.+)\n", text); roles=[]
    for i in range(1,len(parts),3):
        cod=parts[i].strip(); nume=parts[i+1].strip(); corp=parts[i+2]
        m=re.search(r"\*\*Antet:\*\*\s*(\d+)\s+persoan", corp); count=int(m.group(1)) if m else 1
        roles.append({"cod":cod,"nume":nume,"count":count,"ctx":corp[:900],"dep":dep})
    return dep, roles

def _gen(key, prompt, mx):
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
    body=json.dumps({"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"maxOutputTokens":mx,"temperature":0.9}}).encode()
    with urllib.request.urlopen(urllib.request.Request(url,data=body,headers={"Content-Type":"application/json"}),timeout=120) as r:
        d=json.load(r)
    c=d["candidates"][0]
    if "content" not in c or "parts" not in c["content"]: return "[gol]"
    return "".join(p.get("text","") for p in c["content"]["parts"]).strip()

async def call(sem, prompt, mx=320):
    async with sem:
        res="[rate limit]"
        for a in range(3):
            key=next(_rr)
            try: res=await asyncio.to_thread(_gen,key,prompt,mx); break
            except urllib.error.HTTPError as e:
                if e.code in(429,503): await asyncio.sleep(min(50,4*(1.7**a))); continue
                res=f"[HTTP{e.code}]"; break
            except Exception as e: res=f"[{type(e).__name__}]"; break
        await asyncio.sleep(PACE); return res

async def gprog(coros,label):
    res=[];done=0;tot=len(coros)
    for f in asyncio.as_completed(coros):
        res.append(await f);done+=1
        if done%20==0 or done==tot: print(f"   {label}: {done}/{tot}",flush=True)
    return res

def all_agents():
    ags=[]
    for md in sorted(glob.glob(P("fise/Dep_*.md"))):
        dep,roles=parse_roles(md)
        for r in roles:
            for idx in range(1,r["count"]+1): ags.append({**r,"idx":idx})
    return ags

async def faza_a(sem):
    ags=all_agents();print(f"FAZA A — {len(ags)} agenti, fiecare 2-3 imbunatatiri",flush=True)
    async def one(a):
        p=(f"SEDINTA DE URGENTA — redesign. Clientul e nemultumit total.\n\n{VIZUAL}\n\n{CLIENT}\n\n{STARE}\n\n"
           f"Esti acest angajat:\n{a['ctx']}\n\nDin rolul tau, propune 2-3 imbunatatiri CONCRETE, "
           "revolutionare dar implementabile (single-file HTML/JS), aliniate la tinta luminoasa/sociala. "
           "Fii specific (culori hex, microcopy uman, layout, actiuni). NU design de copii. Format:\n"
           "- <imbunatatire 1>\n- <imbunatatire 2>\n- <imbunatatire 3 optional>\nMax 60 cuvinte total.")
        t=await call(sem,p,360)
        return {"cod":a["cod"],"rol":a["nume"],"dep":a["dep"],"idx":a["idx"],"idei":t,"ok":not t.startswith("[")}
    res=await gprog([one(a) for a in ags],"idei")
    json.dump(res,open(P("sedinta7_idei.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"   -> {sum(1 for x in res if x['ok'])}/{len(res)} idei\n",flush=True);return res

async def faza_b(sem,ideas):
    by={}
    for x in ideas:
        if x["ok"]: by.setdefault(x["dep"],[]).append(f"[{x['rol']}] {x['idei']}")
    print(f"FAZA B — {len(by)} grupuri de lucru sintetizeaza",flush=True)
    async def one(dep,items):
        p=(f"Esti liderul grupului de lucru: {dep}.\n\n{VIZUAL}\n\n{CLIENT}\n\nIdeile echipei:\n"+"\n".join(items[:40])+
           "\n\nSintetizeaza POZITIA grupului: top 5 imbunatatiri concrete (vizual + limbaj uman + actiuni), "
           "aliniate la tinta. Specifice, fara generalitati.")
        return {"dep":dep,"sinteza":await call(sem,p,800)}
    res=await gprog([one(d,i) for d,i in by.items()],"grupuri")
    json.dump(res,open(P("sedinta7_grupuri.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"   -> {len(res)} grupuri\n",flush=True);return res

async def faza_c(sem,grupuri):
    print("FAZA C — schimb de idei INTRE grupuri",flush=True)
    digest="\n\n".join(f"### {g['dep']}\n{g['sinteza'][:500]}" for g in grupuri if not g['sinteza'].startswith("["))
    async def one(g):
        altele=digest.replace(f"### {g['dep']}\n","### "+g['dep']+" (GRUPUL TAU)\n")
        p=(f"Esti liderul grupului: {g['dep']}. Ai vazut sintezele TUTUROR grupurilor:\n{altele[:6000]}\n\n"
           "Schimb de idei: ce ADOPTI de la alte grupuri, ce CONTESTI, si ce 2-3 imbunatatiri RAMAN "
           "prioritare pentru tine dupa dezbatere. Scurt, la obiect.")
        return {"dep":g["dep"],"reactie":await call(sem,p,600)}
    res=await gprog([one(g) for g in grupuri],"schimb")
    json.dump(res,open(P("sedinta7_schimb.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"   -> {len(res)} reactii\n",flush=True);return res

async def faza_d(sem,grupuri,schimb):
    print("FAZA D — CPO scrie ITERATIA_5.md (spec redesign)",flush=True)
    g="\n\n".join(f"### {x['dep']}\n{x['sinteza']}" for x in grupuri if not x['sinteza'].startswith("["))
    s="\n\n".join(f"### {x['dep']}\n{x['reactie']}" for x in schimb if not x['reactie'].startswith("["))
    p=(f"Esti CPO. Sedinta de urgenta de redesign.\n\n{VIZUAL}\n\n{CLIENT}\n\nSINTEZE GRUPURI:\n{g[:7000]}\n\n"
       f"SCHIMB INTRE GRUPURI:\n{s[:4000]}\n\nScrie SPEC REDESIGN (iteratia 5), single-file HTML/JS. Structura:\n"
       "1. DIRECTIA VIZUALA: paleta hex completa (light, accent viu indigo, stari), tipografie (sans modern), "
       "spatiere, carduri, umbre, micro-interactiuni\n"
       "2. LIMBAJ UMAN: tabel 'inainte (jargon) -> dupa (uman)' pentru min 8 termeni\n"
       "3. CARD DE POTRIVIRE REGANDIT: ce se vede in 2 sec, ce intra in detalii, actiuni clare "
       "(Trimite mesaj/Cere introducere/Vezi profil/Salveaza/Ignora), status vs actiune\n"
       "4. ECRANE: cum se transforma fiecare (Acasa/Potriviri/Retea/Secretara/Profil) catre tinta\n"
       "5. CE PASTRAM tehnic (criptare/consimtamant/audit) dar ASCUNDEM din UI\n"
       "Revolutionar, implementabil, NU design de copii.")
    txt=await call(sem,p,4000)
    open(P("ITERATIA_5.md"),"w",encoding="utf-8").write("# Iteratia 5 — redesign social/luminos (sedinta de urgenta, 220 agenti)\n\n"+txt)
    print("\n===== ITERATIA 5 (extras) =====\n"+txt[:1400]+"\n=====",flush=True);return txt

async def faza_e(sem,spec):
    ags=all_agents();print(f"FAZA E — consens: toti {len(ags)} voteaza",flush=True)
    sm=spec[:1500]
    async def one(a):
        p=(f"Esti {a['nume']} ({a['dep']}). Specul de redesign aprobat de leadership:\n{sm}\n\n"
           "Esti DE ACORD sa trecem la implementare? Raspunde STRICT:\n"
           "VOT: DE ACORD | OBIECTIE\n"
           "MOTIV: <o propozitie scurta>")
        t=await call(sem,p,120)
        acord = "DE ACORD" in t.upper() and "OBIECTIE" not in t.upper().split("MOTIV")[0]
        return {"rol":a["nume"],"dep":a["dep"],"vot":t,"acord":acord,"ok":not t.startswith("[")}
    res=await gprog([one(a) for a in ags],"vot")
    json.dump(res,open(P("sedinta7_consens.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    ok=[x for x in res if x["ok"]];ac=sum(1 for x in ok if x["acord"])
    print(f"   -> CONSENS: {ac}/{len(ok)} de acord ({100*ac/max(1,len(ok)):.0f}%)\n",flush=True)
    obj=[f"[{x['rol']}] {x['vot']}" for x in ok if not x["acord"]][:25]
    if obj: print("   OBIECTII:\n   "+"\n   ".join(obj),flush=True)
    return res

async def main():
    if not KEYS: print("no GEMINI_KEYS"); sys.exit(1)
    print(f"SEDINTA 7 (urgenta) cu {len(KEYS)} chei\n",flush=True)
    sem=asyncio.Semaphore(LOT);t0=time.time()
    ideas=await faza_a(sem)
    grupuri=await faza_b(sem,ideas)
    schimb=await faza_c(sem,grupuri)
    spec=await faza_d(sem,grupuri,schimb)
    consens=await faza_e(sem,spec)
    print("FAZA F — poarta de audit (mai dura) pe spec",flush=True)
    harsh=("AUDIT EXTREM DE DUR — clientul a respins deja varianta anterioara ca fiind prea bancara. "
           "Fii nemilos: respinge orice ramane sepia/serif greoi/jargon vizibil/carduri pasive/scoruri "
           "neumanizate. Aproba DOAR daca specul atinge clar tinta luminoasa/sociala/moderna.\n\n"+spec)
    g=await audit_gate(sem, solutie=harsh, runda="s7spec")
    ac=sum(1 for x in consens if x.get("ok") and x.get("acord"))
    print(f"\nSEDINTA7_DONE in {time.time()-t0:.0f}s | consens {ac} | audit {'APROBAT' if g['aprobat'] else 'RESPINS'}",flush=True)

if __name__=="__main__": asyncio.run(main())
