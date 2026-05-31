"""Panel de 100 de INVESTITORI (stil Dragons' Den) — extrem de duri si critici.
Fiecare evalueaza aplicatia 'Cercul EIE' si da feedback brutal + verdict de investitie.
Output: INVESTOR_REPORT.md (verdict agregat, obiectii recurente, adevaruri dure, decizii prioritizate).
Onest: feedback simulat de modele, NU investitori reali. Folosit ca instrument de stress-test.
"""
from __future__ import annotations
import asyncio, json, os, re, sys, urllib.request, urllib.error, itertools, collections
KEYS=[k.strip() for k in os.environ.get("GEMINI_KEYS","").split(",") if k.strip()]
_rr=itertools.cycle(KEYS); MODEL="gemini-flash-lite-latest"; LOT=6; PACE=5
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(f): return os.path.join(ROOT,f)
N=int(os.environ.get("PANEL_N","100"))

STARE=(
 "PRODUS evaluat: 'Cercul EIE / Network Capital' — aplicatie mobila premium de business networking. "
 "ARHITECTURA: single-file HTML/JS, 100% client-side, Local-Only, criptata (AES-GCM, cheie in RAM, "
 "PBKDF2 150k), CSP strict (connect-src 'none'), zero backend, zero LLM real (potrivire euristica locala pe "
 "cuvinte-cheie). FUNCTII DE BAZA: profil 'ce ofer / ce caut'; sugestii de conexiuni cu dublu consimtamant; "
 "harta retelei; Secretara (calendar, intalniri cu remindere, task-uri, jurnal de notite cu SABLOANE, brief de 1 min, "
 "mod focus, quick-add); export Google Calendar/.ics/email initiat de user; design system 'Bloom'; "
 "control de ordonare relevanta<->diversitate; pagina de transparenta anti dark-pattern. "
 "IMBUNATATIRI RECENTE (raspuns la un panel anterior care a dat 0/100), TOATE FARA server: "
 "(1) BACKUP CRIPTAT PORTABIL .eie cu parola proprie + restaurare + TRANSFER pe alt dispozitiv (multi-device MANUAL, fara cloud) — atenueaza pierderea datelor; "
 "(2) SCHIMB DE CONTACTE P2P FARA SERVER: 'cod de conexiune' (doar cardul public: nume/domeniu/ce oferi, niciodata 'ce caut') partajabil ca text SI ca QR generat IN-APP (encoder QR propriu, verificat scanabil) — celalalt il scaneaza/lipeste si te adauga in retea; discovery MANUAL la intalniri fata-in-fata; "
 "(3) reminder bland anti-pierdere de backup; (4) suport 'Add to Home Screen' pe iOS (se comporta ca un app); "
 "(5) pozitionare ICP clara ('pentru cine e' + 'de ce Local-Only'). "
 "CE RAMANE NEREZOLVAT, ONEST: MODEL DE AFACERI inca NEDEFINIT (fara monetizare clara); networking-ul e MANUAL, "
 "1-la-1 (NU exista masa critica server-side, NU exista discovery automat al strainilor, NU exista viralitate); "
 "sincronizarea intre dispozitive e manuala (export/import), nu automata; fara canal de achizitie de useri. "
 "Pozitionare: 'cerc privat' premium, confidentialitate radicala (datele nu parasesc dispozitivul).")

# arhetipuri de investitori — fiecare cu lentila lui dura
ARCH=[
 ("Partener VC growth","unit economics, TAM, viteza de crestere, defensibilitate"),
 ("Angel investor serial","fondator, executie, tractiune timpurie, risc de abandon"),
 ("Private Equity","cash-flow, marja, scalabilitate operationala, exit"),
 ("Specialist fintech/securitate","model de amenintare real, conformitate, raspundere, KYC/GDPR"),
 ("VC B2B SaaS","ACV, churn, GTM, ciclu de vanzare, retentie neta"),
 ("Investitor consumer/social","network effects, viralitate, retentie D30, cost de achizitie"),
 ("Sceptic al efectelor de retea","de ce ar adera userii fara masa critica; cold-start problem"),
 ("Vanator de unit-economics","CAC vs LTV, cost server=0 dar cost de distributie, monetizare"),
 ("Sceptic de moat","ce impiedica un competitor (LinkedIn/Clay/Bloom) sa copieze in 3 luni"),
 ("Critic de go-to-market","cum ajungi la primii 1000 de useri platitori; canal de distributie"),
 ("Sceptic de retentie","de ce s-ar intoarce omul; valoare fara reteaua altora; single-player value"),
 ("Hawk de monetizare","cine plateste, cat, de ce; willingness-to-pay; pret"),
 ("Investitor regulatoriu/compliance","date personale, consimtamant, raspundere juridica, EU AI Act"),
 ("Due-diligence tehnic","Local-Only = pieri datele la stergere cache; lipsa sync = dealbreaker?"),
 ("Investitor de piata/positioning","cui vinzi exact; ICP; 'premium' fata de ce alternativa"),
]

def _gen(key,prompt,mx):
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
    body=json.dumps({"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"maxOutputTokens":mx,"temperature":0.95}}).encode()
    with urllib.request.urlopen(urllib.request.Request(url,data=body,headers={"Content-Type":"application/json"}),timeout=120) as r: d=json.load(r)
    c=d["candidates"][0]
    if "content" not in c or "parts" not in c["content"]: return "[gol]"
    return "".join(p.get("text","") for p in c["content"]["parts"]).strip()
async def call(sem,prompt,mx=320):
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
        if d%10==0 or d==t: print(f"   {label}: {d}/{t}",flush=True)
    return res

VERD_RE=re.compile(r"VERDICT\s*[:\-]\s*(INVESTESC|NU INVESTESC|POATE)",re.I)
def parse_verdict(t):
    m=VERD_RE.search(t or "")
    if not m: return "NECLAR"
    v=m.group(1).upper()
    return {"INVESTESC":"INVESTESC","NU INVESTESC":"NU INVESTESC","POATE":"POATE"}[v]

async def main():
    if not KEYS: print("no GEMINI_KEYS"); sys.exit(1)
    print(f"Panel investitori — {N} evaluatori (stil Dragons' Den, duri)",flush=True)
    sem=asyncio.Semaphore(LOT)
    async def one(i):
        arch,lens=ARCH[i%len(ARCH)]
        p=(f"Esti INVESTITOR #{i+1} intr-un panel stil 'Dragons' Den'. Profil: {arch}. Lentila ta: {lens}.\n\n"
           f"{STARE}\n\n"
           "Esti EXTREM DE DUR si critic. Cauta motivele REALE pentru care ai refuza sa investesti. "
           "Fara complezenta, fara incurajari de politete. Raspunde STRICT in formatul:\n"
           "VERDICT: <INVESTESC|NU INVESTESC|POATE>\n"
           "OBIECTIE-UCIGASA: <cel mai grav motiv, o propozitie>\n"
           "CRITICI: <2 critici concrete, taioase>\n"
           "CE TE-AR CONVINGE: <o singura schimbare care ti-ar muta acul>\nMax 70 de cuvinte total.")
        return {"i":i+1,"arch":arch,"text":await call(sem,p,320)}
    res=await gprog([one(i) for i in range(N)],"investitori")
    json.dump(res,open(P("investor_panel_raw.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    ok=[r for r in res if not r["text"].startswith("[")]
    tally=collections.Counter(parse_verdict(r["text"]) for r in ok)
    print("\nVERDICTE:",dict(tally),f"(raspunsuri valide: {len(ok)}/{N})",flush=True)
    # bloc pentru chair (esantion reprezentativ pentru a incadra promptul)
    bloc="\n\n".join(f"[#{r['i']} {r['arch']}]\n{r['text']}" for r in ok)
    if len(bloc)>22000: bloc=bloc[:22000]
    chair=(f"Esti PARTENERUL PRINCIPAL care moderează un panel de {len(ok)} investitori duri care au evaluat "
        f"acest produs.\n\n{STARE}\n\nVERDICTE NUMARATE: {dict(tally)}.\n\nFEEDBACK INVESTITORI (esantion):\n{bloc}\n\n"
        "Scrie INVESTOR_REPORT.md, ONEST si fara complezenta, cu structura EXACTA:\n"
        "## VERDICT AGREGAT (procentaj investesc/poate/nu si concluzia in 2 fraze)\n"
        "## TOP 10 OBIECTII RECURENTE (numerotat, fiecare: obiectia + cat de des a aparut, dur)\n"
        "## ADEVARURI DURE (5 lucruri pe care fondatorul nu vrea sa le auda)\n"
        "## RISCURI DE MOARTE (3 lucruri care ucid produsul daca nu se rezolva)\n"
        "## DECIZII RECOMANDATE (lista numerotata 1-12, prioritizata, concreta si fezabila — "
        "ce sa schimbam STRICT pe baza feedbackului; marcheaza care sunt fezabile in actualul "
        "model single-file/Local-Only si care cer schimbare de model de afaceri). Format: 'N. <decizie>'.\n"
        "## CE PASTRAM (3 puncte forte reale, daca exista)\nFara magie, fara optimism nejustificat.")
    print("Partenerul principal sintetizeaza raportul...",flush=True)
    txt=await call(sem,chair,4000)
    head=f"# INVESTOR_REPORT — panel de {len(ok)} investitori (stress-test, feedback simulat)\n\nVerdicte: {dict(tally)}\n\n"
    open(P("INVESTOR_REPORT.md"),"w",encoding="utf-8").write(head+txt)
    print("\n===== RAPORT (extras) =====\n"+txt[:1800]+"\n=====",flush=True)
    print("INVESTOR_REPORT_DONE",flush=True)
if __name__=="__main__": asyncio.run(main())
