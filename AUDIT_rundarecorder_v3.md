# Raport audit — runda recorder_v3

## Verdict CAE
În calitate de Chief Audit Executive (CAE), am analizat rapoartele auditorilor și starea tehnică a soluției (iteratia 5 + remedieri).

### VERDICT FINAL: RESPINS

**CONSTATARI BLOCANTE (de remediat pentru a trece poarta):**

1.  **Eroare de Arhitectură (Privacy-by-Design):** Contradicția dintre promisiunea "Local-Only" și modul "AI-Managed" (proxy extern) rămâne un risc critic. Un sistem care pretinde confidențialitate totală nu poate expune datele utilizatorului către un releu server-side fără a compromite integritatea modelului de amenințare.
2.  **Risc de Exfiltrare prin CSP:** Extinderea CSP-ului pentru a permite `api.openai.com` și alte endpoint-uri externe în modul "Managed" creează o suprafață de atac pentru exfiltrarea datelor locale (chiar și criptate), invalidând izolarea "Local-Only".
3.  **Gestionarea Resurselor Audio (Memory Leak/Security):** Lipsa apelului explicit `Blob.close()` și a `MediaRecorder.stop()` corelat cu `stream.getTracks().forEach(t => t.stop())` lasă datele audio în heap-ul browserului. În cazul unei erori de rețea (ex: 429), datele rămân stocate, ceea ce constituie o scurgere de date sensibile.
4.  **Insecuritate la Delegarea Evenimentelor:** Utilizarea `setAttribute` pentru handler-ele de evenimente în `Secretara` și `Jurnal` reprezintă un vector de risc. Chiar dacă nu este un sink direct de markup, manipularea atributelor de tip `data-act` prin interpolare de string-uri permite manipularea logicii de delegare a evenimentelor de către un atacator.
5.  **Race Condition (VisibilityChange):** Lipsa unui mecanism de *debouncing* la repornirea STT-ului pe iOS/Android provoacă instanțe multiple de `MediaRecorder`, ducând la `NotAllowedError` și pierderea controlului asupra stream-ului (stare incertă a memoriei).

**CONDITII DE APROBARE:**
- **Izolare Totală:** Separarea strictă a codului pentru modul "Local-Only" (fără nicio conexiune externă) de cel "Managed/Cloud" (build-uri separate sau izolare CSP radicală).
- **Hardening Memorie:** Implementarea `Blob.close()` și oprirea forțată a tuturor track-urilor audio în blocul `finally` al oricărei operațiuni de transcriere, indiferent de succesul sau eșecul procesării.
- **Securizarea Evenimentelor:** Migrarea completă a logicii de delegare de la `setAttribute` la utilizarea exclusivă a `dataset` și a unui Map de handlere pre-definite (fără interpolare de string-uri în atribute).
- **Debouncing:** Implementarea unui mecanism de stare (state-machine) care să blocheze repornirea STT-ului până la confirmarea închiderii instanței anterioare.
- **Audit de Stocare:** Eliminarea JWK-ului din `localStorage` și utilizarea `sessionStorage` sau a unei variabile de memorie (dacă este posibil) pentru cheia de sesiune, pentru a reduce riscul de exfiltrare la nivel de origine.

**NOTĂ:** Ședința de audit rămâne deschisă. Soluția este aproape de maturitate, dar "security theater"-ul rezidual din modul "Managed" și riscurile de gestionare a memoriei în fluxul audio trebuie eliminate pentru a atinge KPI-ul de 0 defecte blocante. Aștept remedierea acestor puncte.

## Technical & Architecture Auditor — APROBAT
VERDICT: APROBAT

BLOCANTE: 
- Niciuna. (Arhitectura a trecut prin iterații riguroase de hardening: eliminarea sink-urilor DOM, implementarea Trusted Types, izolarea CSP, și onestitatea privind limitările criptografice/memory-zeroing).

RECOMANDARI:
- **Audit de entropie:** Deși `crypto.getRandomValues` este utilizat, recomand o verificare a distribuției IV-urilor în producție pentru a preveni coliziuni în scenariul multi-device (deși puțin probabil cu 96-bit IV, o verificare de integritate a counter-ului de mesaje este recomandată).
- **Hardening-ul "Best-Effort":** Deoarece ați documentat onest limitările V8/GC, asigurați-vă că documentația de utilizator (panoul de confidențialitate) menționează explicit că "Închiderea tab-ului" este singura metodă de a garanta ștergerea cheilor din memoria volatilă (RAM), pentru a evita orice confuzie legată de "securitatea hardware".
- **Evoluție CSP:** Pe măsură ce treceți de la localhost la producție, asigurați-vă că `connect-src` rămâne "pin-uit" strict pe originile AI/releu, fără a introduce wildcard-uri, pentru a menține imunitatea la exfiltrare.

NOTĂ AUDITOR: Soluția prezintă un nivel de maturitate tehnică ridicat, în special prin tranziția de la "security theater" la "transparență onestă". Implementarea Trusted Types și eliminarea completă a sink-urilor DOM (innerHTML/outerHTML) transformă aplicația într-un model de referință pentru interfețe web sigure (Client-Side Only).

## Security & Privacy Auditor — RESPINS
VERDICT: RESPINS

BLOCANTE:
- **Eroare de arhitectură privind "Privacy-by-Design":** Documentația afirmă că aplicația este "Local-Only", dar introduce un mod "AI-Managed" (proxy) care trimite prompturile către un server extern (AI_KEY). Aceasta este o contradicție directă cu promisiunea de confidențialitate și creează un punct unic de eșec (releul vede datele în clar).
- **Riscul "Secretara AI" (Context Injection):** Deși randarea este securizată prin `textContent`, procesul de "Follow-up" care generează text în clipboard poate fi victima unui atac de tip "Prompt Injection" dacă sursa datelor (notițele) conține comenzi malitioase care, odată copiate și lipite de utilizator în altă parte, pot compromite fluxul de lucru al acestuia.
- **Lipsa izolării pentru "Managed Proxy":** CSP-ul extins pentru a permite `api.openai.com` etc., în timp ce se pretinde "Local-Only", creează o suprafață de atac pentru exfiltrarea datelor locale (chiar dacă sunt criptate, un script compromis poate trimite cheia sau datele decriptate către aceste endpoint-uri permise în CSP).
- **Dependența de "Best-Effort" în memorie:** Utilizarea `wipe()` pe bufferele Web Speech API este declarată ca fiind în afara controlului aplicației. În contextul unui audit de securitate, a te baza pe "best-effort" pentru date sensibile de apel (transcrieri) fără o garanție de ștergere este un risc inacceptabil de scurgere de date în swap/memory dump.

RECOMANDARI:
- **Separare de mediu:** Izolați complet modul "Local-Only" de cel "Cloud/Managed" prin două build-uri diferite sau prin segregarea strictă a permisiunilor CSP (nu permiteți AI-uri cloud în modul Local-Only).
- **Hardening pentru Clipboard:** Sanitizați agresiv textul generat pentru "Follow-up" înainte de a-l plasa în clipboard pentru a preveni injectarea de comenzi în aplicații terțe (ex: Gmail/Outlook).
- **Audit de memorie:** Implementați `Blob.close()` pentru toate instanțele de `MediaRecorder` imediat după transcriere pentru a forța eliberarea resurselor la nivel de browser, dincolo de simplul `null` pe variabilă.
- **Transparență:** În panoul de confidențialitate, afișați un "Security Score" dinamic care să

## UX & Accessibility Auditor — APROBAT
VERDICT: APROBAT

BLOCANTE:
- niciuna

RECOMANDARI:
- **Hardening de memorie:** Deși wipe() este implementat, documentează în panoul de Confidențialitate că utilizatorii cu nevoi de securitate extremă (ex. jurnaliști în zone de risc) ar trebui să utilizeze un profil de browser "Ephemeral" (sau InPrivate/Incognito) pentru a preveni persistența fragmentelor de date în swap-ul sistemului de operare.
- **UX Handoff:** La exportul `.ics`, adaugă o notificare de tip "toast" care să reamintească utilizatorului că fișierul descărcat conține date necriptate și trebuie gestionat conform politicii sale locale de securitate (ex. ștergere după import).
- **Accessibility:** Deși țintele de atingere sunt 44px, asigură-te că în modul "graf" (rețea), distanța dintre noduri (hit-zones) permite selectarea precisă fără "fat-finger error" pe ecrane mici; implementează un mod de selecție tip listă ca alternativă de accesibilitate pentru utilizatorii cu deficiențe motorii fine.
- **Transparență:** În panoul de AI, adaugă un link direct către "Ghidul de configurare Ollama" pentru a reduce rata de abandon a utilizatorilor care nu știu cum să seteze endpoint-ul local.

**Notă auditor:** Soluția a trecut de la un prototip cu "security theater" la o arhitectură robustă, cu zero sink-uri DOM-XSS și un model de amenințare documentat onest. Implementarea Trusted Types și renunțarea la innerHTML în favoarea DOM API reprezintă standardul de aur pentru acest tip de aplicație. Efortul de "decluttering" a adus interfața la un nivel de utilizabilitate profesional.

## AI & Data Ethics Auditor — APROBAT
VERDICT: **APROBAT** (cu rezerve de monitorizare)

**BLOCANTE:**
- Niciuna. (Arhitectura a trecut de la "security theater" la o abordare de *defense-in-depth* cu Trusted Types, CSP strict și model de amenințare documentat onest).

**RECOMANDARI:**
- **Analiza stării de memorie:** Deși `wipe()` este implementat corect, recomand adăugarea unui avertisment vizual în UI (ex: "Sesiune activă în RAM") care să dispară doar la `wipe()` complet, pentru a întări conștientizarea utilizatorului asupra persistenței datelor în timpul sesiunii.
- **Limitarea rate-limiting:** Pentru endpoint-ul `/dir` (discovery), asigură-te că implementarea server-side (Node) loghează erorile de tip 429 fără a stoca IP-ul în clar, pentru a menține postura de *zero-knowledge* a releului.
- **Handoff-uri:** Deoarece exportul (Google/ICS) este *user-initiated*, recomand adăugarea unui "check-list" de securitate (ex: "Verifică dacă ești pe dispozitivul tău personal") chiar înainte de deschiderea tab-ului extern, pentru a preveni scurgerea accidentală a datelor pe calculatoare publice.
- **Documentație:** Menține fișierul `confidentialitate.md` (sau echivalentul din UI) sincronizat cu orice modificare a modului de procesare AI; orice schimbare în prompt-ul trimis către furnizorii externi (chiar și prin BYOK) trebuie să declanșeze o actualizare a etichetei de privacy.

**NOTĂ AUDITOR:**
Soluția a evoluat de la un prototip cu riscuri de securitate (XSS, lipsa criptării la repaus, terminologie înșelătoare) la o arhitectură robustă. Trecerea la `Trusted Types` și eliminarea completă a sink-urilor de tip `innerHTML` demonstrează o înțelegere matură a vectorilor de atac. Onestitatea privind limitările (ex: `best-effort` pentru ștergerea din RAM, modelul de amenințare pentru extensii compromise) transformă aplicația dintr-un produs "magic" într-un instrument tehnic predictibil și transparent.

## Quality & QA Auditor — RESPINS
VERDICT: RESPINS

BLOCANTE:
- **Lipsa izolării contextuale în `MediaRecorder`:** În scenariul iPhone (fără STT live), buffer-ul audio `REC.audioBlob` este stocat în memorie. Deși se menționează `wipe()`, nu există o garanție de *atomicitate* între finalizarea transcrierii și eliberarea memoriei în cazul în care procesul `Whisper` (AI) returnează o eroare sau se blochează (ex: 429 Too Many Requests). O eroare de rețea lasă datele audio în heap pe termen nedeterminat.
- **Trusted Types vs. `textContent`:** Deși `textContent` este sigur, utilizarea `setAttribute` pentru handler-ele de evenimente (ex: `onclick`) pe elemente dinamice în `Secretara` și `Jurnal` reprezintă un vector de risc dacă valorile atributelor sunt construite prin interpolare de string-uri. Chiar dacă s-a eliminat `innerHTML`, un atacator care injectează un string în `data-id` sau `data-act` poate manipula logica de delegare a evenimentelor (`event delegation`).
- **Race condition la `visibilitychange`:** Repornirea automată a STT-ului la revenirea în tab pe iOS/Android fără un mecanism de *debouncing* sau *state-check* riguros poate duce la multiple instanțe de `MediaRecorder` active simultan, cauzând `NotAllowedError` sau pierderea referinței către stream-ul curent (memory leak de stream-uri).
- **Model de amenințare `localStorage`:** Documentarea onestă nu scutește soluția de vulnerabilitatea critică: stocarea cheii de criptare (chiar și derivată) în `localStorage` (chiar și ca JWK) pe o origine partajată/compromisă. Dacă `localStorage` este accesibil, atacatorul poate exfiltra `salt`-ul și `ciphertext`-ul, iar PBKDF2 (150k iterații) este trivial de spart pe GPU-uri moderne dacă parola utilizatorului nu este extrem de lungă (entropie > 80 biți).

RECOMANDARI:
- **Implementare `Blob.close()`:** Apelați explicit `.close()` pe `MediaRecorder` și pe stream-urile audio imediat după transcriere pentru a forța eliberarea resurselor la nivel de browser, nu doar setarea `null` pe variabilă.
- **Hardening delegare evenimente:** Înlocuiți `setAttribute` cu `dataset` pentru stocarea ID-urilor și folosiți un map

## Business & Compliance Auditor — APROBAT
VERDICT: APROBAT

BLOCANTE:
- Niciuna.

RECOMANDARI:
- **Audit de Memorie:** Deși `wipe()` este implementat, reține că în mediul browser, `Uint8Array.fill(0)` nu garantează ștergerea referințelor din *garbage collector* (GC) dacă obiectele au fost copiate prin *closures* sau *closures-scope*. Pentru o rigoare absolută, asigură-te că variabilele care conțin chei sunt `null`-uite explicit imediat după `wipe()`.
- **Hardening AI:** Deși `connect-src` este strict, asigură-te că în modul "Managed" (proxy), releul implementează un *header* de securitate `Content-Security-Policy: sandbox` pentru răspunsurile primite, pentru a preveni orice execuție accidentală în cazul în care un furnizor AI ar fi compromis și ar injecta *payload*-uri în răspunsul JSON.
- **Documentare:** Panoul de "Confidentialitate" este exemplar. Adaugă o notă scurtă despre faptul că "Best-effort memory wiping" este o măsură de igienă, nu o barieră împotriva atacurilor de tip *cold-boot* sau *DMA*, pentru a menține standardul de "zero security theater".

**Notă auditor:** Soluția a trecut de la un prototip cu riscuri de *security theater* la o arhitectură defensivă solidă (Trusted Types, CSP strict, model de amenințare documentat, eliminarea sink-urilor DOM). Integritatea afirmațiilor de business este acum corect etichetată, iar distincția între procesarea locală și cea prin releu este clară și onestă.