"""Poarta de audit — corpul de audit (cei mai exigenti auditori) valideaza o solutie.

Regula: nicio sedinta/iteratie nu se incheie pana cand Chief Audit Executive (CAE) nu
emite verdict APROBAT. Auditorii sunt adversariali; o constatare blocanta nerezolvata =>
RESPINS din partea CAE.

Folosire:
  python examples/audit.py runda1            # ruleaza o runda pe SOLUTIE si scrie raportul
  (din alt script)  from audit import audit_gate; verdict=await audit_gate(sem, solutie)

Citeste rolurile din fise/AUDIT.md. Gemini, multi-cheie, ritmat.
"""
from __future__ import annotations
import asyncio, json, os, re, sys, time, urllib.request, urllib.error, itertools

KEYS=[k.strip() for k in os.environ.get("GEMINI_KEYS","").split(",") if k.strip()]
_rr=itertools.cycle(KEYS)
MODEL="gemini-flash-lite-latest"
LOT=4; PACE=8
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(f): return os.path.join(ROOT,f)

# Descrierea EXACTA a solutiei auditate (iteratia 2). Se actualizeaza cand se schimba solutia.
SOLUTIE=(
 "SOLUTIE AUDITATA — app/eie.html, iteratia 2 ('Network Capital / EIE'). Single-file HTML/JS, "
 "localStorage, fara backend. Paleta 'Executive Hybrid': Light 'Quiet Luxury Sand' (#F7F4EF, "
 "carduri albe, text antracit #1A202C, accent bronz #B88E56, navy #1A2B3C) implicit + comutator "
 "Soft-Dark navy (#121625, primary #D4AF37). Contrast text/fundal raportat 8.4:1.\n"
 "Functii: (1) Onboarding wizard 3 pasi (nume+domeniu / ofer / caut) creeaza membru real cu "
 "trust 75. (2) Matching TF-IDF + cosine similarity intre 'ce caut' si 'ce ofer' vizibil, scor "
 "afinitate 52-99, lista 'common tokens' afisata ca 'de ce v-am potrivit'. (3) Dublu consimtamant: "
 "'Prezinta-ma'/'Refuz', conexiunea se deschide doar dupa ambele consimtaminte; sursa citata pe "
 "fiecare card. (4) Secretara AI: extrage intentii din text dupa cuvinte-cheie (caut/ofer...), "
 "indicator de procesare (spinner) ~950ms. (5) Trust Ledger pe Acasa (conexiuni confirmate + data). "
 "(6) Jurnal de audit read-only in Profil (actiuni cu marca de timp). (7) KPI Exec-Concierge: "
 "Network Capital '€Xk deal flow estimat', ROI 'X.Xx', Trust Score, Afinitate medie. (8) Graf SVG "
 "retea. Escapare HTML prin functia esc() pe text de utilizator.\n"
 "LIMITARI: fara backend/auth real; date doar in localStorage local; 'ce caut' (privat) este totusi "
 "folosit in motorul de matching care e vizibil celeilalte parti pe card; criptarea AES-GCM din "
 "ITERATIA_2.md NU e inca implementata; nu exista teste automate; KPI sunt estimari euristice.")

def parse_audit():
    text=open(P("fise/AUDIT.md"),encoding="utf-8").read()
    parts=re.split(r"\n## (A\.\d+)\s+(.+)\n", text)
    roles=[]
    for i in range(1,len(parts),3):
        cod=parts[i].strip(); nume=parts[i+1].strip(); corp=parts[i+2][:1000]
        roles.append({"cod":cod,"nume":nume,"ctx":corp})
    return roles

def _gen(key, prompt, max_tokens):
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
    body=json.dumps({"contents":[{"parts":[{"text":prompt}]}],
        "generationConfig":{"maxOutputTokens":max_tokens,"temperature":0.55}}).encode()
    with urllib.request.urlopen(urllib.request.Request(url,data=body,headers={"Content-Type":"application/json"}),timeout=120) as r:
        d=json.load(r)
    c=d["candidates"][0]
    if "content" not in c or "parts" not in c["content"]: return "[gol]"
    return "".join(p.get("text","") for p in c["content"]["parts"]).strip()

async def call(sem, prompt, max_tokens=500):
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

async def audit_gate(sem, solutie=SOLUTIE, runda=1):
    """Ruleaza o runda de audit. Returneaza dict: {verdict, blocante[], findings[], raport}."""
    auditori=[r for r in parse_audit() if r["cod"]!="A.1"]  # toti minus CAE
    async def one(a):
        p=(f"AUDIT INDEPENDENT SI ADVERSARIAL (runda {runda}). Esti acest auditor:\n{a['ctx']}\n\n"
           f"SOLUTIA DE AUDITAT:\n{solutie}\n\n"
           "Fii EXIGENT la maximum. Nu acorda credit pe intentii, doar pe dovezi din solutie. "
           "Raspunde STRICT in format:\n"
           "VERDICT: APROBAT | RESPINS\n"
           "BLOCANTE: <constatari care TREBUIE remediate, una pe linie cu '- '; sau 'niciuna'>\n"
           "RECOMANDARI: <imbunatatiri ne-blocante, scurt>\n"
           "Din unghiul tau specific. La obiect.")
        txt=await call(sem,p,600)
        resp="RESPINS" in txt.upper().split("VERDICT")[-1][:40] if "VERDICT" in txt.upper() else False
        return {"cod":a["cod"],"rol":a["nume"],"raport":txt,"respins":resp,"ok":not txt.startswith("[")}
    print(f"AUDIT runda {runda} — {len(auditori)} auditori",flush=True)
    res=await asyncio.gather(*[one(a) for a in auditori])
    for r in res: print(f"   {r['cod']} {r['rol']}: {'RESPINS' if r['respins'] else 'APROBAT'}",flush=True)
    # CAE consolideaza
    bloc="\n\n".join(f"### {r['rol']}\n{r['raport']}" for r in res if r["ok"])
    cae=parse_audit()[0]
    pc=(f"Esti {cae['nume']}.\n{cae['ctx']}\n\nSOLUTIA:\n{solutie}\n\n"
        f"RAPOARTELE AUDITORILOR TAI:\n{bloc}\n\n"
        "Consolideaza. Emite verdictul portii de audit. APROBAT DOAR daca exista 0 constatari "
        "blocante. Format STRICT:\n"
        "VERDICT FINAL: APROBAT | RESPINS\n"
        "CONSTATARI BLOCANTE (de remediat pentru a trece poarta):\n- <...>\n"
        "CONDITII DE APROBARE: <ce trebuie sa fie adevarat>\n"
        "Daca RESPINS, sedinta/iteratia NU se incheie.")
    verdict_txt=await call(sem,pc,1200)
    aprobat=("APROBAT" in verdict_txt.upper().split("VERDICT FINAL")[-1][:30]) and not any(r["respins"] for r in res)
    raport=(f"# Raport audit — runda {runda}\n\n## Verdict CAE\n{verdict_txt}\n\n"
            +"\n\n".join(f"## {r['rol']} — {'RESPINS' if r['respins'] else 'APROBAT'}\n{r['raport']}" for r in res if r["ok"]))
    open(P(f"AUDIT_runda{runda}.md"),"w",encoding="utf-8").write(raport)
    print(f"\n   VERDICT CAE: {'APROBAT ✓' if aprobat else 'RESPINS ✗'}  -> AUDIT_runda{runda}.md\n",flush=True)
    return {"aprobat":aprobat,"verdict":verdict_txt,"res":res,"raport":raport}

async def main():
    if not KEYS: print("no GEMINI_KEYS"); sys.exit(1)
    runda=int(re.sub(r"\D","",sys.argv[1])) if len(sys.argv)>1 else 1
    sem=asyncio.Semaphore(LOT)
    r=await audit_gate(sem,runda=runda)
    print("="*60);print(r["verdict"][:1400]);print("="*60)
    print("AUDIT_DONE",("APROBAT" if r["aprobat"] else "RESPINS"))

if __name__=="__main__": asyncio.run(main())
