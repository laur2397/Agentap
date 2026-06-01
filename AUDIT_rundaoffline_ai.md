# Raport audit — runda offline_ai

## Verdict CAE
În calitate de Chief Audit Executive, am analizat rapoartele tuturor auditorilor (Tehnic, Securitate/Privacy, UX, AI/Etică, QA și Business).

**VERDICT FINAL: RESPINS**

**CONSTATARI BLOCANTE (de remediat pentru a trece poarta):**

1. **Eroare de logică privind confidențialitatea terțului:** Auditorul de Securitate a identificat o breșă de conformitate: captura acustică (necesară pentru WhatsApp/Signal) înregistrează vocea interlocutorului fără consimțământul acestuia. În lipsa unui mecanism de notificare (ex: avertisment sonor/vizual la începutul sesiunii), soluția încalcă normele GDPR/ePrivacy.
2. **Suprafața de atac AI (Managed Mode):** Există o contradicție arhitecturală nerezolvată între promisiunea "Local-Only" și funcționalitatea "Managed AI". Permiterea trimiterii contextului local (note/jurnal) către un releu, chiar și prin opt-in, creează un vector de exfiltrare care subminează integritatea întregului sistem de securitate documentat.
3. **Riscul de Stored XSS via localStorage:** Deși `textContent` este utilizat, parsarea datelor din `localStorage` prin `JSON.parse` fără o re-validare riguroasă a schemei la fiecare citire (nu doar la scriere) lasă o fereastră de vulnerabilitate dacă stocarea locală este alterată extern.

**CONDITII DE APROBARE:**
1. **Implementarea mecanismului de consimțământ:** Adăugarea unui flux obligatoriu (UI/Audio) de informare a interlocutorului înainte de activarea microfonului pentru captură acustică.
2. **Air-Gap Logic pentru AI:** Implementarea unei separări fizice în cod: dacă modul "Managed AI" este activat, accesul la Jurnalul local de note trebuie să fie programatic blocat/dezactivat, pentru a garanta că datele private nu pot fi incluse în prompturi.
3. **Hardening de citire:** Implementarea unui validator de schemă (JSON Schema) strict la fiecare `JSON.parse(localStorage.getItem())` pentru a preveni injecția de obiecte malițioase.
4. **Separarea vizuală a riscului:** Implementarea indicatorului vizual (ex: scut colorat) care să reflecte în timp real profilul de risc (Local vs. Managed) conform recomandărilor auditorului de Etică.

**NOTĂ:** Iteratia NU se încheie. Echipa de dezvoltare trebuie să prezinte remedierea acestor puncte blocante pentru o nouă rundă de audit. Nu se trece în producție cu riscuri de conformitate neacoperite.

## Technical & Architecture Auditor — APROBAT
VERDICT: **APROBAT**

**BLOCANTE:**
- Niciuna. (Arhitectura de securitate și mecanismele de protecție a datelor sunt coerente cu modelul de amenințare declarat; Trusted Types și CSP-ul sunt implementate corect pentru a preveni injecția de cod.)

**RECOMANDARI:**
- **Zeroing Memorie:** Deși documentat ca "best-effort", asigură-te că în `wipe()` apelezi `buffer.fill(0)` nu doar pentru `Uint8Array`, ci și pentru orice `ArrayBuffer` care a stocat chei derivate (dacă sunt accesibile), pentru a minimiza fereastra de viață a secretelor în heap.
- **Trusted Types:** Menține politica `fail-closed` și în viitoarele iterații; orice adăugare de funcționalitate (ex: vizualizări noi de graf) trebuie să treacă prin `h()`-ul securizat pentru a evita regresia la `innerHTML`.
- **UX/AI:** În interfața de "Secretară", adaugă un indicator vizual de "stare AI" (ex: "Model local activ" vs "Releu activ") care să fie vizibil permanent în timpul sesiunii, pentru a preveni utilizarea accidentală a modului Managed când se dorește Local-Only.
- **Audio:** Deoarece Web Speech API pe iOS este limitat și poate produce text-gunoi, păstrează fallback-ul de MediaRecorder ca sursă primară de adevăr pentru AI, așa cum ai configurat în v3.2. Documentația pentru utilizator (UI) este onestă și corectă.

**NOTĂ AUDITOR:** Soluția a trecut de la un prototip cu "security theater" la o arhitectură robustă, cu transparență totală asupra limitărilor tehnice. Implementarea Trusted Types și a mecanismului de rollback tranzacțional demonstrează o maturitate tehnică ridicată. Riscul rezidual (exfiltrarea prin XSS pe origine compromisă) este corect asumat și comunicat utilizatorului.

## Security & Privacy Auditor — RESPINS
VERDICT: RESPINS

BLOCANTE:
- **Eroare de logică în "Zero-Audio":** Documentația susține "audio aruncat garantat (finally)", dar Web Speech API și MediaRecorder pe iOS/Android au buffere de sistem opace care pot persista în memoria browserului după `track.stop()`. Documentarea acestui aspect drept "best-effort" este o recunoaștere a eșecului KPI-ului de confidențialitate (0 expuneri).
- **Suprafața de atac AI (Managed Mode):** Chiar și cu "opt-in", trimiterea prompturilor către un releu (chiar și cu etichetă) creează un vector de exfiltrare a datelor private (note/jurnal) care contrazice arhitectura "Local-Only". Un utilizator care bifează "context local" în AI-ul managed își expune datele de jurnal către un terț.
- **Trusted Types vs. Single-File:** Deși politica este definită, utilizarea `textContent` pentru randare este corectă, dar injectarea de configurări/prompturi în `localStorage` care ulterior sunt parsate prin `JSON.parse` și redate în UI reprezintă un risc de tip "Stored XSS" dacă sanitizarea la intrare (`clean()`) nu este aplicată riguros la fiecare update de stare.
- **Conflict de interes în "One-Tap":** Captura acustică prin microfon (necesară pentru WhatsApp/Signal) captează inevitabil și vocea interlocutorului. În multe jurisdicții (GDPR/ePrivacy), stocarea chiar și temporară (în RAM) a vocii unei terțe părți fără consimțământul acesteia este o încălcare gravă. UI-ul nu oferă un mecanism de consimțământ pentru terț.

RECOMANDARI:
- **Separare fizică:** Implementează un "Air-Gap" logic: dacă modul AI Managed este activat, dezactivează complet accesul la Jurnalul local de note pentru a preveni scurgerea accidentală.
- **Hardening RAM:** În loc de `wipe()`, care este ineficient în JS, utilizează `Blob` cu `URL.createObjectURL` și `revokeObjectURL` imediat după procesare pentru a forța GC-ul să elibereze memoria mai agresiv.
- **Consimțământ terț:** Adaugă un "Avertisment de înregistrare" audio (beep sau notificare vizuală) care să ruleze în primele secunde ale apelului, pentru a acoperi obligațiile legale de notificare a interlocutorului.
- **Audit

## UX & Accessibility Auditor — APROBAT
VERDICT: **APROBAT**

**BLOCANTE:**
- Niciuna. (Arhitectura a trecut de la prototip nesigur la o implementare robustă, cu Trusted Types, CSP strict, eliberare deterministă a resurselor și transparență totală asupra limitărilor).

**RECOMANDARI:**
- **UX/Accesibilitate:** Deși contrastul este confirmat la 8.4:1, asigură-te că stările de `focus-visible` pe butoanele din graful interactiv (SVG) au un contur (outline) suficient de gros (min 2px) pentru a fi vizibile pe fundalul "Quiet Luxury Sand".
- **Memorie:** Deoarece `wipe()` este o operațiune `best-effort` în JavaScript, adaugă un mic mesaj de tip "Footer" în panoul de Confidentialitate care să instruiască utilizatorul: *"Pentru o curățare completă a memoriei, închide tab-ul browserului după ce ai activat Auto-Lock."*
- **Erori AI:** În cazul în care `AbortController` declanșează timeout-ul la transcriere, asigură-te că mesajul de eroare afișat utilizatorului oferă un buton de "Retry" care reinițializează doar fluxul de transcriere, nu întreaga sesiune, pentru a menține fluiditatea.
- **Trusted Types:** Menține politica `fail-closed` în producție; orice modificare viitoare a UI-ului trebuie să treacă prin aceleași funcții `h()`/`setKids()` verificate în acest audit.

**NOTĂ AUDITOR:** Soluția a demonstrat o maturizare remarcabilă, trecând de la un model "bancar/opac" la unul "onest/transparent". Implementarea `Trusted Types` combinată cu eliminarea completă a sink-urilor de tip `innerHTML` și gestionarea atomică a bufferelor audio/memorie validează cerințele de securitate și etică. Designul "Bloom" respectă ierarhia vizuală și WCAG AA/AAA.

## AI & Data Ethics Auditor — APROBAT
VERDICT: APROBAT

BLOCANTE: 
- Niciuna. (Arhitectura a trecut de la "security theater" la o abordare defensivă onestă, cu Trusted Types, CSP strict și separarea clară a responsabilităților între UI și procesare).

RECOMANDARI:
- **Hardening Memorie:** Deși `wipe()` este implementat, documentează în `OFFLINE_AI.md` că `Web Speech API` (pe Android/Chrome) poate stoca buffere audio în cache-ul browserului în afara controlului direct al JS; recomandă utilizatorului să curețe cache-ul browserului periodic pentru o igienă completă a datelor.
- **UX Onestitate:** În secțiunea "Secretara", adaugă un indicator vizual de tip "Offline-First" (ex: un icon de scut verde) care să devină gri/galben în momentul în care utilizatorul activează modul "Cloud/Managed AI", pentru a reaminti vizual schimbarea profilului de risc fără a citi textul de disclaimer.
- **Trusted Types:** Menține politica `fail-closed` și în producție; asigură-te că orice bibliotecă externă (dacă va fi adăugată pe viitor) nu forțează un sink de tip `innerHTML` prin `import` dinamic.
- **Documentația de risc:** Menține mențiunea explicită că, în cazul unei extensii de browser maligne, stocarea locală (chiar și criptată) poate fi citită prin `localStorage.getItem()`; este un model de amenintare corect asumat pentru un tool de tip client-side.

*Notă de audit:* Soluția a demonstrat o evoluție remarcabilă prin eliminarea "magiei" (scoruri fabricate) în favoarea unor indicatori euristici documentați și a unei arhitecturi de securitate (Trusted Types + CSP + AES-GCM) care validează tehnic afirmațiile de confidențialitate.

## Quality & QA Auditor — APROBAT
VERDICT: **APROBAT**

**BLOCANTE:**
- Niciuna.

**RECOMANDARI:**
- **Audit de memorie:** Deși `wipe()` este implementat, asigură-te că în `finally` orice referință către `MediaStream` sau `AudioBlob` este setată explicit la `null` pentru a forța colectarea gunoiului (GC) în browserele cu implementări agresive de caching.
- **Trusted Types:** Deși politica `default` este definită, verifică dacă bibliotecile externe (dacă vor fi adăugate pe viitor) nu încearcă să injecteze scripturi; menține politica `fail-closed` ca standard de aur.
- **UX iPhone:** Având în vedere comportamentul agresiv al iOS de a suspenda microfonul în fundal, recomandă în UI utilizatorului activarea "Airplane Mode" pe al doilea dispozitiv (dacă e folosit pentru captură) pentru a preveni notificările care pot întrerupe fluxul audio.
- **Hardening:** CSP-ul este robust, dar asigură-te că `connect-src` rămâne strict la nivel de domeniu (ex: `api.openai.com`) și nu la nivel de wildcard (ex: `*.openai.com`), pentru a preveni redirecționări prin subdomenii compromise.

**NOTĂ AUDITOR:**
Soluția a trecut de la un prototip experimental la un sistem de procesare audio/text defensiv, cu o arhitectură care respectă principiul "defense-in-depth". Utilizarea `Trusted Types` combinată cu `DOM API` pur elimină vectorii de XSS. Tratarea audio-ului prin clauze `finally` și limitarea `visibilitychange` la `SpeechRecognition` (fără a atinge `MediaRecorder`) rezolvă problemele de stare orfană și memory leaks. Documentarea onestă a limitărilor de platformă (iOS/Web Speech) transformă limitările tehnice în specificații de utilizare corecte.

## Business & Compliance Auditor — APROBAT
**VERDICT: APROBAT**

**BLOCANTE:**
- Niciuna. (Soluția a integrat riguros remedierea sink-urilor HTML prin Trusted Types, eliminarea stocării cheilor pe disc, etichetarea onestă a estimărilor și controlul atomic al bufferelor audio).

**RECOMANDARI:**
- **Audit de Securitate/Memory:** Deși `wipe()` este implementat, documentează explicit în `Confidentialitate` că `MediaRecorder` pe iOS poate menține buffere în afara controlului direct al JS (la nivel de OS/Browser), deci "eliberarea" este limitată la ceea ce API-ul expune.
- **UX/Onboarding:** La prima utilizare a modului "Managed AI", adaugă un "tooltip" sau un pas de onboarding care să explice vizual că, deși datele sunt criptate, *promptul* (nu neapărat notele întregi) este procesat de furnizorul ales; menține distincția clară față de modul "Local-Only".
- **Hardening:** Deoarece folosești `Trusted Types` cu `default` policy, asigură-te că orice bibliotecă externă (dacă va fi adăugată pe viitor) este testată pentru compatibilitate, deoarece orice `innerHTML` sau `eval` va bloca execuția aplicației imediat — ceea ce este un comportament dorit (fail-closed).
- **Consistență:** Verifică dacă `visibilitychange` (care repornește STT) nu poate fi declanșat în buclă infinită pe dispozitive iOS cu setări de economisire a energiei agresive; adaugă un "debounce" de 500ms la repornire.

**Notă Auditor:** Soluția a trecut de la un prototip cu riscuri de "security theater" la o arhitectură robustă, cu model de amenințare documentat onest și mecanisme de apărare (Trusted Types, CSP, crypto-in-RAM) verificate. Afirmațiile de business sunt acum corect încadrate ca estimări/euristici.