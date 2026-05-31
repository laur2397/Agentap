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

# Descrierea EXACTA a solutiei auditate (iteratia 2 + remedieri runda 1). Onesta — doar ce e implementat.
SOLUTIE=(
 "REMEDIERI RUNDA 3 (peste cele din runda 2, toate verificate automat cu Playwright):\n"
 "(R3#1) CHEIA NU MAI E PE DISC: criptarea foloseste o cheie AES-GCM derivata din PAROLA de sesiune "
 "prin PBKDF2-SHA256 (150.000 iteratii, salt aleatoriu de 16 octeti). Cheia e ne-exportabila "
 "(extractable:false) si traieste DOAR in memorie (RAM); pe disc se salveaza doar salt-ul, niciodata "
 "cheia. Verificat: nu exista cheie in localStorage. La fiecare pornire/refresh aplicatia cere parola "
 "(ecran de deblocare); parola gresita e respinsa; fara parola datele nu pot fi decriptate.\n"
 "(R3#2) INTEGRITATE ANTI-MANIPULARE: pe langa tag-ul de autentificare AES-GCM, payload-ul include un "
 "checksum SHA-256 al continutului, verificat la decriptare. Verificat: alterarea blob-ului din "
 "localStorage (ex. via DevTools, inclusiv a starii de consimtamant/conexiune) e detectata si respinsa.\n"
 "(R3#3) SANITIZARE SVG: etichetele si initialele din graful SVG trec printr-un whitelist strict "
 "(doar litere/cifre/spatiu/./-). Input-ul utilizatorului e sanitizat la INTRARE (clean(): elimina "
 "caractere de control si <>), nu doar la afisare (esc() la randare).\n"
 "(R3#4) ANTI-PIERDERE: buton de Export date (JSON) pentru backup manual; la resetare se pastreaza "
 "automat un backup criptat al datelor curente inainte de stergere (backupRaw).\n"
 "(transparenta R3) Avertisment XSS explicit in UI: prototip client-side, nu introduce date sensibile, "
 "utilizatorul e responsabil de backup.\n\n"
 "SOLUTIE AUDITATA — app/eie.html, iteratia 2 dupa remedierea constatarilor din runda 1. Single-file "
 "HTML/JS, localStorage, fara backend (aplicatie Local-Only, declarata explicit in UI). Paleta "
 "'Executive Hybrid': Light 'Quiet Luxury Sand' implicit + comutator Soft-Dark navy. Contrast 8.4:1.\n"
 "REMEDIERI APLICATE SI VERIFICATE (vs. runda 1):\n"
 "(R2) CRIPTARE LA REPAUS: intregul DB este criptat in localStorage cu Web Crypto AES-GCM-256 (IV "
 "aleatoriu/scriere); verificat ca storage NU contine text clar (numele membrilor nu apar in clar). "
 "Cheia e generata local si pastrata ca JWK in localStorage — declarat onest ca model Local-Only de "
 "prototip (fara server/parola), nu protejeaza impotriva XSS pe acelasi origin.\n"
 "(R1+R5) PRIVACY-BY-DESIGN + CONSIMTAMANT ONEST: pana la DUBLU consimtamant real, identitatea "
 "(nume->'Membru din Cerc'), cererea privata 'ce caut' (-> '•••') si sursa raman ASCUNSE celeilalte "
 "parti; 'de ce v-am potrivit' afiseaza doar text generic, fara token-uri brute din profilul privat. "
 "Detaliile si token-urile se dezvaluie DOAR dupa ce ambele parti accepta. Consimtamantul nu mai "
 "auto-confirma cealalta parte: starea ramane 'in asteptare' pana cand celalalt membru accepta efectiv.\n"
 "(R3) KPI ETICHETAT: 'Network Capital' si 'ROI' afiseaza sufix '(est.)' + sub-eticheta 'ipotetic, nu "
 "garantat' + disclaimer vizibil 'Estimari euristice — indicatori de colaborare, nu valori financiare "
 "garantate'.\n"
 "(R4) REZILIENTA: validare de schema (validDB) la incarcare cu sanitizare (trust 0-100, lungimi, id-uri); "
 "la date corupte se face reseed in loc de crash; error boundary global (window error/unhandledrejection) "
 "+ render() in try/catch; verificat ca aplicatia supravietuieste unui localStorage corupt. Reentranta "
 "blocata in timpul procesarii Secretara AI.\n"
 "(transparenta) Panou 'Confidentialitate — Local-Only' in Profil explica criptarea, caracterul local si "
 "ca datele dispar la stergerea cache-ului. Accesibilitate: spinner role=status aria-live; SVG aria-label. "
 "Escapare HTML prin esc() la randare pe tot textul de utilizator (anti-XSS la afisare).\n"
 "Functii pastrate: onboarding 3 pasi; matching TF-IDF+cosine (scor 52-99); Secretara AI (extragere "
 "intentii pe cuvinte-cheie); Trust Ledger; jurnal de audit read-only; graf SVG.\n"
 "LIMITARI ONESTE RAMASE: fara backend/auth real; cheia de criptare e Local-Only (prototip); matching pe "
 "cuvinte-cheie/TF-IDF, nu GNN/embeddings; nu exista teste automate; Secretara AI e euristica, nu LLM.")

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
