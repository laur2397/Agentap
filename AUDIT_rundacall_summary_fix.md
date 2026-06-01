# Raport audit — runda call_summary_fix

## Verdict CAE
În calitate de Chief Audit Executive (CAE), am analizat rapoartele tuturor auditorilor (Tehnic, Securitate, UX, AI/Etică, QA, Business).

**VERDICT FINAL: RESPINS**

**CONSTATARI BLOCANTE (de remediat pentru a trece poarta):**
1. **Conflict de arhitectură (MediaRecorder vs. Web Speech):** Auditorul Tehnic a identificat o eroare logică critică: pornirea `MediaRecorder` *după* eșecul `Web Speech` (sau după ce s-a constatat că acesta a prins prea puțin text) implică pierderea iremediabilă a începutului conversației. O soluție de audit nu poate accepta o pierdere de date în fluxul de captură.
2. **Eroare logică în "Captura ambelor voci":** Dezactivarea `echoCancellation` pe dispozitive mobile pentru a captura vocea interlocutorului din difuzor creează un feedback acustic (ecou) care degradează calitatea apelului la un nivel inacceptabil pentru utilizator. Aceasta nu este o soluție tehnică viabilă, ci o compromitere a funcționalității de bază a telefonului.
3. **Trusted Types vs. Handler direct:** Auditorul Tehnic a semnalat că simpla atribuire `el.onclick = handler` nu constituie o protecție dacă `handler`-ul în sine nu este validat sau dacă logica sa internă procesează date ne-sanitizate. Este necesară o verificare riguroasă a tuturor handlerelor dinamice pentru a garanta că nu devin vectori de execuție de cod.

**CONDITII DE APROBARE:**
1. **Re-arhitecturarea capturii:** Implementarea unei logici de captură paralele (MediaRecorder pornit preventiv) sau o metodologie care să nu depindă de "ghicirea" momentului în care Web Speech eșuează.
2. **Soluție de captură audio:** Identificarea unei metode de captură care să nu necesite dezactivarea `echoCancellation` (ex: recomandarea oficială a utilizării unui al doilea dispozitiv pentru înregistrare, dacă captura acustică prin microfonul propriului telefon este tehnic imposibilă fără ecou).
3. **Audit de securitate a handlerelor:** Transformarea tuturor handlerelor de evenimente în funcții validate/sanitizate care să respecte politica `Trusted Types` (ex: utilizarea unor mapări de acțiuni statice, nu a unor funcții construite dinamic).
4. **Documentarea onestă a limitărilor:** Actualizarea documentației din panoul de Confidentialitate pentru a reflecta clar recomandările auditorilor privind memoria (Garbage Collector, limitările `wipe()` în browserele bazate pe Chromium) și riscul de memory dump.

**NOTĂ CAE:**
Proiectul a făcut progrese remarcabile în ceea ce privește "security-by-design" și eliminarea "security theater-ului". Totuși, **integritatea funcțională** a capturii audio este fundamentală pentru un "Raportofon de Apel". Până la rezolvarea conflictului dintre calitatea apelului și capturarea ambelor voci, poarta de audit rămâne închisă. 

**Sesiunea continuă.**

## Technical & Architecture Auditor — RESPINS
VERDICT: RESPINS

BLOCANTE:
- **Conflict de arhitectură (MediaRecorder vs. Web Speech):** Se afirmă că "dacă live a prins >20 caractere se folosește live, altfel AI". Această logică este viciată tehnic: MediaRecorder (pentru AI) trebuie să fie pornit *de la începutul* apelului pentru a capta contextul. Dacă pornești MediaRecorder *după* ce ai constatat că Web Speech a eșuat (sau a prins puțin), ai pierdut deja începutul conversației.
- **Integritatea datelor (Audio-ul "aruncat"):** Se afirmă "REC.audioBlob=null" în `finally` ca metodă de ștergere. În JS, setarea referinței pe `null` doar marchează obiectul pentru Garbage Collector. Nu există garanția că memoria a fost zeroizată (zeroing). Afirmația că buffer-ul este "eliberat" este corectă, dar implicația de securitate ("datele nu se păstrează") este incompletă fără mențiunea că memoria RAM rămâne vulnerabilă la memory dump-uri până la colectarea gunoiului.
- **Eroare logică în "Captura ambelor voci":** Afirmația "getUserMedia cere echoCancellation:false... microfonul NU mai șterge vocea celuilalt" este periculoasă. Dezactivarea `echoCancellation` pe un dispozitiv mobil (iPhone/Android) în timpul unui apel telefonic/WhatsApp va cauza un feedback acustic (ecou) insuportabil pentru interlocutor, care va auzi propria voce redată de difuzorul tău. Aceasta nu este o soluție tehnică viabilă pentru "captura ambelor voci" în scenarii reale, ci o degradare a calității apelului.
- **Trusted Types vs. "Handler direct":** Se afirmă "handler atasat ca proprietate, nu setAttribute". Dacă handler-ul este o funcție care conține logică derivată din datele utilizatorului, simpla atribuire ca proprietate (`el.onclick = ...`) nu te scutește de riscuri dacă funcția respectivă nu este ea însăși un *Trusted Type* sau dacă nu validează input-ul.

RECOMANDARI:
- **Clarificare UX:** În loc de "captură ambele voci", documentează onest că este o captură de microfon ambiental (microfon-difuzor) și că performanța depinde de acustica camerei, nu de setările `getUserMedia`.
- **Securitatea memoriei:** Înlocuiește "eliberare" cu "marcare pentru GC" în document

## Security & Privacy Auditor — APROBAT
VERDICT: APROBAT

BLOCANTE:
- niciuna

RECOMANDARI:
- **Audit de Memorie:** Deși `wipe()` este implementat, asigură-te că în fluxul de `MediaRecorder`, `chunks` nu sunt stocate în variabile globale/closure-uri ce supraviețuiesc după `recFinalize`. Verifică manual în Chrome Heap Snapshot după un apel lung că obiectul `Blob` nu mai are referințe active.
- **Trusted Types:** Deși politica `default` este fail-closed, asigură-te că orice bibliotecă externă (dacă vei adăuga pe viitor) nu încearcă să injecteze scripturi; menține politica strictă `require-trusted-types-for 'script'`.
- **UX Confidentialitate:** În modul "Cloud/BYOK", adaugă un indicator vizual de tip "Security Badge" (ex: un lacăt deschis sau colorat diferit) care să amintească utilizatorului că, deși cheia e a lui, metadatele conversației sunt procesate de terți.
- **Hardening:** Având în vedere că aplicația este `Local-Only`, recomand implementarea unui `Content-Security-Policy` (CSP) care să blocheze explicit `unsafe-eval` și să limiteze `script-src` doar la hash-uri valide, pentru a preveni orice execuție de cod injectat prin XSS.

**Notă Auditor:** Soluția a trecut de la un prototip cu "security theater" la o arhitectură robustă, cu separare clară între procesarea locală și handoff-urile user-initiated. Trecerea la `Trusted Types` și eliminarea completă a `innerHTML` în favoarea `DOM API` validează tehnic securitatea front-end-ului. Abordarea "Local-Only" cu documentarea onestă a limitărilor (risc de exfiltrare pe origine compromisă) este corectă și profesională.

## UX & Accessibility Auditor — APROBAT
VERDICT: **APROBAT**

**BLOCANTE:**
- Niciuna. (Arhitectura de securitate și mecanismele de protecție a datelor sunt riguroase, iar respectarea WCAG și a principiilor anti-dark-pattern este confirmată prin implementarea Trusted Types și a fluxurilor opt-in/user-initiated).

**RECOMANDARI:**
- **Audit de memorie:** Deși `wipe()` este implementat, asigură-te că în mediul de producție (în afara localhost), documentația pentru utilizator conține un avertisment vizibil despre faptul că "închiderea tab-ului este singura metodă garantată de curățare totală a memoriei volatile", pentru a evita orice urmă de *security theater*.
- **UX/Cognitiv:** Deoarece aplicația a evoluat spre un set complex de funcționalități (Secretara, E2EE sync, Task-uri), asigură-te că "Ghost-ul" (starea de gol) pentru utilizatorii noi rămâne la fel de aerisit ca în redesign-ul 'Bloom', evitând supraîncărcarea cognitivă la prima accesare.
- **Trusted Types:** Menține politica `default` strictă și pe viitor; orice adăugare de funcționalitate nouă trebuie să treacă prin testul `grep` pentru sink-uri (innerHTML/outerHTML) pentru a păstra integritatea auditului curent.

**Notă auditor:** Soluția a demonstrat o maturizare remarcabilă, trecând de la un prototip cu riscuri de securitate/transparență la o arhitectură robustă, "fail-closed" și onestă în comunicarea limitărilor tehnice. Implementarea Trusted Types și eliminarea completă a sink-urilor de tip XSS reprezintă standardul de aur pentru acest tip de aplicație.

## AI & Data Ethics Auditor — APROBAT
VERDICT: APROBAT

BLOCANTE:
- Niciuna. (Arhitectura a trecut de la "security theater" la o abordare de tip *defense-in-depth* cu Trusted Types, CSP strict si management de memorie documentat onest).

RECOMANDARI:
- **Zeroing Memorie:** Deși `wipe()` este implementat, documentează în UI că pe browserele bazate pe Chromium, *Garbage Collector*-ul poate muta obiectele în memorie înainte de `fill(0)`, lăsând copii în heap. Menționează că "inchiderea tab-ului este singura metodă de curățare garantată de OS".
- **Trusted Types:** Deoarece folosești `createElement` și `textContent` pentru tot, asigură-te că orice viitoare integrare (ex: librării externe de grafice) nu introduce un *sink* care ar necesita o politică `createHTML` complexă; menține politica `fail-closed` curentă ca default.
- **Transparență AI:** În modul "Managed" (releu), adaugă un indicator vizual permanent ("AI vede promptul") pe tot parcursul sesiunii, nu doar în panoul de setări, pentru a preveni utilizarea accidentală a modului cloud în conversații sensibile.
- **Auditabilitate:** Pentru funcția de "Export .ics", adaugă un mic hash (checksum) al fișierului generat în jurnalul de audit local, pentru a putea proba ulterior integritatea datelor exportate.

**NOTĂ AUDITOR:** Soluția a evoluat de la o aplicație cu pretenții tehnologice nesustenabile la un instrument *privacy-first* onest. Trecerea la DOM API nativ (fără `innerHTML`) și implementarea politicii `Trusted Types` elimină riscurile de XSS, iar separarea clară între modurile "Local" și "Managed" (cu etichetare explicită) rezolvă problemele de bias și onestitate semnalate anterior.

## Quality & QA Auditor — APROBAT
VERDICT: APROBAT

BLOCANTE: 
- niciuna

RECOMANDARI: 
- **Hardening de memorie:** Deși `wipe()` este implementat, documentează în panoul de confidențialitate faptul că în browserele bazate pe Chromium, `SharedArrayBuffer` (dacă ar fi folosit vreodată) sau obiectele `Blob` pot persista în cache-ul de memorie al motorului de randare dincolo de `GC.collect()`.
- **Trusted Types:** Deoarece ai impus `require-trusted-types-for script`, asigură-te că orice bibliotecă terță (dacă pe viitor integrezi un SDK extern) este încărcată via `trustedScriptURL`, altfel vei avea un crash imediat.
- **Input Sanitization:** Deși `textContent` este folosit riguros, pentru campurile de tip "Notițe" sau "Brief", adaugă un filtru de lungime maximă (ex: 2000 caractere) pentru a preveni atacurile de tip "DOM Storage Exhaustion" (umplerea localStorage-ului cu date gigantice care pot bloca UI-ul la citire).
- **UX/Onboarding:** La prima rulare, forțează un scroll-to-view pe panoul de "Confidențialitate" înainte de a permite interacțiunea cu Jurnalul, pentru a te asigura că utilizatorul a luat la cunoștință caracterul `Local-Only` (reducerea riscului de "User Error" prin ignorarea avertismentelor).

**Notă Auditor:** Arhitectura a atins un nivel de maturitate defensivă ridicat. Trecerea la un model de "Defense-in-Depth" (CSP + Trusted Types + Sanitizare la intrare + Rollback tranzacțional) elimină vectorii clasici de injectie. Eliminarea "security theater-ului" și onestitatea privind limitările (ex: memoria RAM, modelul de amenințare offline) transformă aplicația dintr-un prototip într-un instrument robust pentru utilizatori avansați.

## Business & Compliance Auditor — APROBAT
VERDICT: APROBAT

BLOCANTE: niciuna

RECOMANDARI:
- **Audit de memorie:** Deși wipe() este implementat, documentează explicit în panoul de Confidentialitate că, în browserele bazate pe Chromium, `MediaRecorder` poate menține buffere în afara controlului direct al JS (în procesul de browser/GPU), deci "zero-ing" este o măsură de igienă, nu o garanție de securitate absolută (anti-forensics).
- **Trusted Types:** Deși politicile sunt fail-closed, asigură-te că orice bibliotecă terță (dacă va fi adăugată ulterior) nu injectează scripturi prin `document.createElement('script')`, care ar putea ocoli politica dacă nu este tratată ca `TrustedScript`.
- **UI/UX:** Menține eticheta "Prototip/Beta" vizibilă în subsolul interfeței pentru a tempera așteptările utilizatorilor privind disponibilitatea 24/7 a serviciilor AI (având în vedere dependența de disponibilitatea furnizorilor externi).

**Notă auditor:** Soluția a trecut prin iterații riguroase de hardening. Trecerea de la "security theater" la "transparență documentată" (recunoașterea limitărilor RAM/V8 și a modelului de amenințare) este conformă cu standardele de onestitate solicitate. Implementarea Trusted Types cu politică fail-closed și eliminarea completă a sink-urilor de markup dinamic (innerHTML) constituie o dovadă tehnică solidă de conformitate.