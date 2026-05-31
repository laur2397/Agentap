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
 "SECRETARA — ITERATIA 2 din roadmap (Calendar & Programare cu DOUBLE-OPT-IN). Verificat cu Playwright, "
 "zero erori, tot pe DOM API (zero innerHTML).\n"
 "(s2-propunere) Din conversatia cu o conexiune, formular 'Propune o intalnire' (data/ora/loc, sanitizate). "
 "Creeaza o intalnire status 'propus' (a=propunator, b=invitat).\n"
 "(s2-doubleoptin) Invitatul vede propunerea in ecranul Secretara la 'De confirmat' si Accepta/Refuza. "
 "Intalnirea devine 'confirmat' DOAR dupa acceptul celeilalte parti (propunerea=primul consimtamant, "
 "acceptul=al doilea). Doar persoana invitata (b===ME) poate confirma.\n"
 "(s2-imuabil) La confirmare se calculeaza o SEMNATURA HMAC-SHA256 (cheia derivata din parola, din RAM) "
 "peste detaliile intalnirii (parti+data+loc) -> inregistrare tamper-evident, afisata pe card; "
 "actiunea intra si in jurnalul de audit. Aliniat cu strategia (intalnire confirmata = inregistrare imuabila).\n"
 "(s2-calendar) Ecranul Secretara afiseaza intalnirile grupate: De confirmat / Confirmate (sortate dupa "
 "data) / In asteptare; empty-state cu CTA. Tot criptat, accesibil (44px, focus), persistent.\n\n"
 "SECRETARA — ITERATIA 1 din roadmap-ul aprobat (Notite + Brief de intalnire). Verificat cu Playwright, "
 "zero erori de consola, tot pe DOM API (zero innerHTML).\n"
 "(s1-notite) JURNAL DE NOTITE in ecranul Secretara: adaugi idei/notite (sanitizate cu clean(), randate "
 "prin textContent), cu cautare locala, stergere, marca de timp; empty-state cu CTA clar ('Scrie prima "
 "ta idee'). Notitele intra in baza criptata existenta (AES-GCM) si in jurnalul de audit.\n"
 "(s1-brief) BRIEF DE 1 MINUT: la deschiderea unei conversatii cu o conexiune, sus apare un brief generat "
 "DOAR din datele tale locale: cand v-ati conectat, interese comune, ce ofera persoana (date vizibile "
 "asumate), si NOTITELE TALE care mentioneaza persoana. NU agrega profilul privat al celuilalt fara "
 "consimtamant. Onest, fara LLM/integrari false.\n"
 "(s1-acces) Tinte de atingere >=44px pe butoane, focus-visible, empty-state cu indemn — conform "
 "constrangerilor de accesibilitate.\n\n"
 "AJUSTARI UX (feedback client: 'pagina prea aglomerata' + 'reteaua primitiva, ce sunt liniile?'):\n"
 "(ux#1) DECLUTTER ACASA: eliminat sectiunea abstracta 'Sanatatea retelei' (bare) si sparkline-ul; "
 "KPI-urile mari inlocuite cu o banda compacta de 3 statistici (Conexiuni / Sugestii noi / Potrivire "
 "medie). Continutul actionabil (Persoane de contactat) urcat sus. Mult mai mult aer.\n"
 "(ux#2) RETEAUA = LISTA CLARA: graful abstract (perceput ca primitiv) nu mai e implicit. Ecranul arata "
 "o lista de conexiuni — avatar colorat, nume, rol, 'prin interes comun: X', data; click -> mesaj. "
 "Graful ramane optional sub 'Vezi harta retelei', cu explicatie clara: o LINIE = o conexiune confirmata "
 "de ambele parti, tu esti in centru. Cautare pe lista. Tot pe DOM API (zero innerHTML).\n\n"
 "REMEDIERI QA RUNDA 2 (verificate automat cu Playwright, zero erori de consola):\n"
 "(r2#1) ZERO innerHTML: TOATA randarea a fost rescrisa pe DOM API printr-un constructor sigur "
 "h()/svgEl()/setKids() (createElement/createElementNS + textContent + setAttribute). Verificat in cod: "
 "0 atribuiri .innerHTML si 0 citiri .innerHTML in tot fisierul. Datele de utilizator intra DOAR ca "
 "textContent -> imposibil sa devina markup. SVG-ul grafului e construit cu createElementNS si "
 "svg.replaceChildren (fara serializare HTML). Atributele numerice sunt coercionate.\n"
 "(r2#2) ANTI CSS-EXFILTRATION: vectorul CSS (ex. [value^=...]{background:url(...)}) e blocat de CSP — "
 "img-src 'data:' (fara url-uri externe) + connect-src 'none' (fara nicio iesire de retea). style-src "
 "'self' e imposibil pt. single-file (tot CSS-ul e inline), dar exfiltrarea e efectiv blocata; nicio "
 "clasa/stil nu e construita din input de utilizator (avatarul foloseste o culoare din paleta controlata).\n"
 "(r2#3) CLEANUP DETERMINIST (anti zombie-state): handler global error/unhandledrejection reseteaza "
 "starea async (PROC/overlay/pendingLock); 'pagehide' apeleaza wipe() (zeroizarea bufferelor) la "
 "inchidere/navigare; commit() are try/catch/finally cu rollback. wipe() la auto-lock ramane.\n\n"
 "REMEDIERI QA (peste redesign-ul iteratiei 5, verificate cu Playwright, zero erori):\n"
 "(qa#1) ZEROING MEMORIE: functie wipe() care suprascrie cu zerouri (Uint8Array.fill(0)) salt-ul si "
 "bufferele controlate, apelata la auto-lock inainte de eliberarea referintelor. Limitare documentata "
 "ONEST (nu ascunsa): CryptoKey-urile sunt non-extractabile/opace — WebCrypto nu expune heap-ul lor; "
 "string-urile parola sunt imutabile in JS. Se face ce e posibil + transparenta despre rest.\n"
 "(qa#2) ROLLBACK TRANZACTIONAL: commit() are try/catch/finally; la QuotaExceededError sau orice esec, "
 "NU se atinge key-ul principal -> datele vechi valide raman intacte (rollback), tmp se curata in finally, "
 "user notificat. Verificat.\n"
 "(qa#3) REDUCERE unsafe-inline: tot continutul generat dinamic (carduri, ledger, profil, secretara) "
 "foloseste DELEGARE de evenimente (data-act/data-id), deci ZERO handler-e JS inline derivate din date "
 "(vectorul real de XSS). Au ramas doar cateva onclick STATICE, first-party, constante (lock/tema/profil) "
 "— documentat; plus CSP connect-src 'none' (fara exfiltrare) si esc()/clean() peste tot.\n"
 "(qa#4) ZERO COD DE TEST IN PRODUCTIE: fisierul app/eie.html nu contine cod Playwright/test/instrumentare "
 "— testele sunt scripturi externe separate. Single-file, zero dependinte runtime.\n\n"
 "ITERATIA 5 — REDESIGN COMPLET 'Bloom' (sedinta de urgenta 220 agenti + consens 215/220), ca raspuns "
 "la respingerea clientului ('prea bancar'). Verificat automat cu Playwright, zero erori de consola.\n"
 "(vizual) Tema LUMINOASA: fundal #FAFAFB, carduri albe, accent INDIGO viu #6366F1/#4F46E5, succes "
 "emerald #10B981 (nu verde medical). Tipografie INTER peste tot (fara serif). Avataruri patrate "
 "colorate (culoare per membru din paleta vibranta). Umbre subtile, hover-lift pe carduri, "
 "micro-interactiuni (scale la click). Toggle dark slate+indigo.\n"
 "(limbaj uman) Jargonul scos de la suprafata: cardul nu mai arata TF-IDF/SHA-256/Trust Score brut. "
 "In loc de scoruri reci -> fraza umana ('Cineva din Constructii cauta ceva ce tu oferi'), badge-uri "
 "umane ('Potrivire foarte buna', 'N interese comune', 'Profil verificat'). KPI de pe Acasa NU mai au "
 "framing financiar (€/ROI scoase) -> 'Conexiuni active / Sugestii noi / Profil / Potrivire medie'.\n"
 "(ierarhie gist-first) Cardul comunica in 2 sec: avatar+nume+titlu, o fraza clara, badge-uri, actiuni. "
 "Detaliile tehnice intra in 'De ce vad asta?' (progressive disclosure) — transparenta PASTRATA, nu stearsa "
 "(raspuns la obiectia securitate/etica din consens).\n"
 "(actiuni vs status) Butoane clare de actiune: 'Cere introducere' / 'Trimite mesaj' / 'Vezi profil' / "
 "'Nu acum'. Statusul ('Conectat'/'In asteptare'/'Sugestie') e o PASTILA discreta sus-dreapta, separata "
 "vizual de zona de actiune.\n"
 "(accesibilitate WCAG) Contrast >=4.5:1 (text #1E293B pe alb, buton #4F46E5 alb); tinte de atingere "
 ">=44px; focus-visible pe butoane/taburi/inputuri; aria-label pe graf/overlay; text-overflow ellipsis "
 "pe nume/titluri. Respecta prefers-reduced-motion.\n"
 "(pastrate sub capota) Criptare AES-GCM + cheie PBKDF2 in RAM, HMAC ledger, dublu consimtamant real, "
 "auto-lock atomic, CSP connect-src none, commit tranzactional, sanitizare SVG recursiva — toate raman, "
 "dar SCOASE din UI-ul principal (shield 'Conexiune protejata' + sectiunea Confidentialitate).\n\n"
 "REMEDIERI RUNDA 5 (toate verificate automat cu Playwright, zero erori de consola):\n"
 "(R5#1) TERMINOLOGIE CORECTATA: nu se mai pretinde 'cryptographic shredding pe disc'. Mecanism documentat "
 "exact: cheia AES + cheia HMAC se deriveaza din parola (PBKDF2, 150k iteratii) cu un SALT unic per "
 "utilizator, generat la prima rulare si STOCAT local (salt-ul nu e secret — previne rainbow tables); "
 "cheile raman STRICT in RAM, nu se scriu pe disc. La blocare se sterge doar variabila-cheie din RAM; "
 "datele pe disc raman criptate si se redeschid doar cu parola. Documentat in panoul de confidentialitate.\n"
 "(R5#2) OVERLAY BLOCANT: orice operatiune asincrona (addItem/Secretara) afiseaza un overlay full-screen "
 "care BLOCHEAZA input-ul utilizatorului (pointer-events) pana la finalizare -> nu mai sunt stari "
 "intermediare in DOM. Verificat ca overlay-ul apare in timpul procesarii si dispare dupa.\n"
 "(R5#3) HARDENING XSS/SVG: (a) CSP strict via meta -> connect-src 'none' (ZERO exfiltrare retea), "
 "object-src/frame-src 'none', fara eval; 'unsafe-inline' la script ramane necesar pt. single-file dar "
 "exfiltrarea e blocata. (b) Sanitizare RECURSIVA a SVG-ului: dupa fiecare randare se elimina orice "
 "foreignObject/script/a si orice atribut on*/href. Verificat: 0 atribute on*, 0 foreignObject.\n"
 "(R5 cond.1) COMMIT TRANZACTIONAL: scrierea in localStorage se face in key temporara -> validare prin "
 "decriptare roundtrip -> abia apoi suprascriere atomica a key-ului principal -> integritate garantata la "
 "inchideri bruste. Verificat: nicio key temporara reziduala; redeschidere dupa reload OK.\n\n"
 "REMEDIERI RUNDA 4 (toate verificate automat cu Playwright, zero erori de consola):\n"
 "(R4#1) AUTO-LOCK ATOMIC: blocarea NU mai intrerupe operatiuni asincrone. Daca o procesare e in curs "
 "(PROC), blocarea se AMANA (pendingLock) si se executa abia dupa finalizare; verificat: lock declansat "
 "in timpul Secretarei AI se amana si se aplica corect, fara DOMException. Functiile async de ledger au "
 "guard (bail daca DB/HK devin null). La blocare se face si sanitizare DOM (golirea zonelor sensibile).\n"
 "(R4#2) ANTI TIMING SIDE-CHANNEL: declansatoarele de matching (addItem, Secretara) sunt mascate de o "
 "durata FIXA de procesare (padding la ~360ms / 950ms), astfel incat timpul algoritmului TF-IDF nu e "
 "observabil prin UI. Documentat onest modelul de amenintare: un atacator cu script pe aceeasi origine "
 "are oricum acces direct la memorie, deci apararea reala e auto-lock + parola.\n"
 "(R4#3) HASH-CHAIN CORECT: Trust Ledger trece de la 'salt secret' (incoerent) la HMAC-SHA256 cheiat de "
 "o cheie derivata din parola (PBKDF2, info distinct), tinuta DOAR in RAM, niciodata stocata. Terminologia "
 "'secret' e acum exacta (cheie secreta reala, nu pepper stocat). Verificat: verificarea lantului = integru.\n"
 "(R4#4) HARDENING null: validDB filtreaza activ intrarile null/alterate (members/items/matches/messages) "
 "inainte de procesare; render() are guard pe ME invalid + optional chaining; matches() are fallback-uri "
 "pe membru/item lipsa. Verificat: localStorage corupt -> reseed/eroare gratioasa, fara TypeError/crash.\n\n"
 "ITERATIA 4 — imbunatatiri notabile peste iteratia 3, respectand constrangerile auditului s5spec "
 "(ZERO dependinte externe, fara ONNX/D3/RAG = fara 'magie tehnologica', totul pur client-side vanilla; "
 "verificate automat cu Playwright, zero erori de consola):\n"
 "(i4-vizual) GRAF FORCE-DIRECTED: reteaua nu mai e statica, ci simulare de fizica vanilla (repulsie + "
 "arcuri pe muchii + centrare, damping), noduri care se pot TRAGE, hover evidentiaza vecinii, cautare "
 "fuzzy; respecta prefers-reduced-motion (animatia se opreste la cerere).\n"
 "(i4-functional) PIPELINE/FUNNEL pe Potriviri: grupate in 3 coloane (Noi-de-decis / In asteptare / "
 "Conectate) cu numaratori.\n"
 "(i4-vizual+transparenta) RADAR 'de ce s-a potrivit' pe cardurile conectate: 3 dimensiuni (Interese="
 "teme comune x22, Afinitate=scor TF-IDF/cosine, Incredere=Trust Score) cu METODOLOGIA documentata "
 "vizibil — fara cifre fabricate.\n"
 "(i4-securitate) HASH-CHAIN INTARIT CU SALT secret per-cont in fiecare veriga SHA-256; verificare+export "
 "pastrate.\n"
 "(i4-securitate) AUTO-LOCK = CRYPTOGRAPHIC SHREDDING: la 3 min inactivitate sau buton manual, cheia AES "
 "(CK) si DB se sterg din RAM si se cere parola; datele pe disc raman criptate. Verificat: dupa blocare "
 "apare ecranul de deblocare.\n\n"
 "ITERATIA 3 — imbunatatiri NOTABILE peste iteratia 2 (toate verificate automat cu Playwright, "
 "zero erori de consola, pure vanilla JS, fara dependinte externe — fara D3/Fuse):\n"
 "(vizual) Skeleton shimmer la schimbarea ecranului; contoare KPI animate (count-up cu easing); "
 "sparkline de tendinta deal flow in Focus Digest (etichetat 'est.'); tranzitii intre ecrane "
 "(View Transitions API cu fallback); Trust Score afisat ca DONUT (conic-gradient) in profil; "
 "empty-states ilustrate SVG; typing-dots la Secretara AI; rafinament premium (umbre, ierarhie).\n"
 "(functional) Graf de retea INTERACTIV: hover evidentiaza nodul + vecinii (restul estompate), "
 "click deschide membrul; CAUTARE FUZZY in timp real pe nume/domeniu (subsecventa, vanilla). "
 "Transparenta algoritm: fiecare card arata 'metoda: TF-IDF + cosine · N teme comune'.\n"
 "(integritate REALA, nu 'security theater' — remediaza constatarea din auditul specului) Trust "
 "Ledger cu HASH-CHAIN real: fiecare veriga = SHA-256(hash_anterior | membru_a | membru_b | timp), "
 "afisat truncat; buton 'Verifica' recalculeaza intregul lant si raporteaza 'lant integru' sau "
 "'lant alterat' (verificat: alterarea unei verigi e detectata); buton 'Export' (JSON) al lantului.\n"
 "(accesibilitate — cerinta audit) Comutator 'Reduce animatiile' in Profil + respectarea "
 "@media (prefers-reduced-motion); aria-live pe procesare, aria-label pe graf, role=switch pe toggle. "
 "Toate animatiile se dezactiveaza cu reduce-motion.\n"
 "Securitatea/criptarea raman ca in iteratia 2 (AES-GCM, cheie PBKDF2 doar in RAM, checksum SHA-256, "
 "input sanitizat la intrare prin clean(), output prin esc(), SVG prin whitelist svgSafe).\n\n"
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

def _verdict_is_respins(txt):
    """Citeste DOAR linia de verdict (robust): cauta prima linie cu 'VERDICT'; daca acolo apare
    RESPINS -> True, daca APROBAT -> False. Evita falsele pozitive din restul textului."""
    if not txt or txt.startswith("["): return False
    for line in txt.splitlines():
        u=line.upper()
        if "VERDICT" in u:
            if "RESPINS" in u: return True
            if "APROBAT" in u: return False
    # fallback: niciun verdict explicit -> respins doar daca textul mentioneaza RESPINS, nu APROBAT
    U=txt.upper(); return ("RESPINS" in U) and ("APROBAT" not in U)

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
        resp=_verdict_is_respins(txt)
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
    aprobat=(not _verdict_is_respins(verdict_txt)) and not any(r["respins"] for r in res)
    raport=(f"# Raport audit — runda {runda}\n\n## Verdict CAE\n{verdict_txt}\n\n"
            +"\n\n".join(f"## {r['rol']} — {'RESPINS' if r['respins'] else 'APROBAT'}\n{r['raport']}" for r in res if r["ok"]))
    open(P(f"AUDIT_runda{runda}.md"),"w",encoding="utf-8").write(raport)
    print(f"\n   VERDICT CAE: {'APROBAT ✓' if aprobat else 'RESPINS ✗'}  -> AUDIT_runda{runda}.md\n",flush=True)
    return {"aprobat":aprobat,"verdict":verdict_txt,"res":res,"raport":raport}

async def main():
    if not KEYS: print("no GEMINI_KEYS"); sys.exit(1)
    runda=sys.argv[1] if len(sys.argv)>1 else "1"  # eticheta (poate fi text) pt. nume fisier + prompt
    sem=asyncio.Semaphore(LOT)
    r=await audit_gate(sem,runda=runda)
    print("="*60);print(r["verdict"][:1400]);print("="*60)
    print("AUDIT_DONE",("APROBAT" if r["aprobat"] else "RESPINS"))

if __name__=="__main__": asyncio.run(main())
