# Raport audit — runda recorder_v4

## Verdict CAE
[HTTP503]

## Technical & Architecture Auditor — RESPINS
VERDICT: RESPINS

BLOCANTE:
- **Confuzie Arhitecturală (Audio):** Documentația afirmă "ZERO audio capturat/stocat" când se folosește Web Speech API, dar recunoaște că "buffer-ele interne ale Web Speech API sunt în afara controlului app". Aceasta este o contradicție tehnică: dacă nu poți controla buffer-ul, nu poți garanta "ZERO audio". Trebuie reformulat onest ca "best-effort" sau "limitare de platformă".
- **Conflict de Securitate (AI Managed):** Se afirmă că "releul VEDE prompturile (nu e E2EE pt. AI)", dar CSP-ul permite originile AI (OpenAI, etc.) direct. Dacă releul este proxy, atunci cererile către furnizorii cloud ar trebui să treacă exclusiv prin releu pentru a fi consistente cu modelul de securitate declarat. Dacă clientul apelează direct furnizorul, atunci releul nu "vede" prompturile, ceea ce contrazice afirmația de "releu proxy".
- **Trusted Types vs. Single-File:** Deși se invocă `require-trusted-types-for script`, într-un fișier unic (single-file) care conține și UI și logică, manipularea atributelor SVG sau a stilurilor (chiar și cu `createElementNS`) necesită o politică explicită de `TrustedTypePolicy` definită în cod. Fără definirea și aplicarea unei politici (nu doar activarea directivei CSP), browserul va bloca execuția la primul sink.
- **Integritate Ledger:** Afirmația "verificarea lantului = integru" este riscantă dacă cheia HMAC derivată din parolă este stocată în RAM, dar PBKDF2 se re-rulează la fiecare sesiune. Dacă salt-ul este stocat local (cum se declară), un atacator care obține salt-ul și are acces la execuția JS poate forța re-derivarea cheii dacă parola este slabă. Trebuie clarificat că integritatea depinde 100% de entropia parolei utilizatorului.

RECOMANDARI:
- **Audio:** Pentru iPhone (unde Web Speech lipsește), documentați explicit că `MediaRecorder` scrie în `Blob` în memorie; chiar dacă e "aruncat" în `finally`, există o fereastră de expunere în heap-ul browserului.
- **Trusted Types:** Implementați un `TrustedTypePolicy` global care să accepte doar string-uri sanitizate prin `clean()` pentru a satisface cerința `require-trusted-types-for`.
- **UX:**

## Security & Privacy Auditor — APROBAT
VERDICT: APROBAT

BLOCANTE:
- Niciuna.

RECOMANDARI:
- **Hardening Memorie:** Deși wipe() este implementat best-effort, pentru mediul de producție (dacă se trece de la prototip la live), recomand utilizarea `FinalizationRegistry` pentru a monitoriza și forța curățarea obiectelor mari (blob-uri audio) imediat ce referințele devin nule, reducând fereastra de expunere în heap.
- **Trusted Types:** Deși implementarea este solidă (zero sink-uri), asigură-te că policy-ul de Trusted Types este definit global în `window.trustedTypes.createPolicy` înainte de orice execuție de script, pentru a preveni orice "monkey-patching" al prototipurilor DOM din extensii de browser malitioase care ar putea încerca să injecteze sink-uri după încărcarea app-ului.
- **Audio Privacy:** În fluxul iPhone (MediaRecorder), asigură-te că `MediaStreamTrack` este oprit explicit nu doar la `stop` (tap), ci și în cazul `visibilitychange` (dacă userul părăsește tab-ul în timpul înregistrării), pentru a preveni "ghost-recording" în fundal.
- **AI Managed:** Pentru utilizatorii care aleg modul Managed (unde releul vede prompturile), adaugă un "watermark" vizual persistent în UI în timpul sesiunii, pentru a evita situația în care utilizatorul uită că a trecut de la modul Local-Only la cel Managed.

NOTĂ AUDITOR: Soluția demonstrează o maturitate tehnică ridicată în ceea ce privește igiena datelor (zero-knowledge relay, atomicitatea bufferelor audio, Trusted Types). Trecerea de la "security theater" la documentarea onestă a limitărilor (ex: modelul de amenințare storage) transformă aplicația dintr-un prototip riscant într-un instrument de încredere pentru utilizatori avansați.

## UX & Accessibility Auditor — APROBAT
AUDIT INDEPENDENT SI ADVERSARIAL (Runda recorder_v4)
Auditor: Contributor Individual Senior
Status: **VERIFICARE E2E FINALIZATA**

---

**VERDICT: APROBAT**

**BLOCANTE:**
- Niciuna. (Hardening-ul de securitate, implementarea Trusted Types, eliminarea sink-urilor de tip innerHTML și mecanismele de curățare a memoriei/bufferelor audio sunt conforme cu KPI-urile impuse).

**RECOMANDARI:**
- **UX/Privacy:** Deși `wipe()` este implementat, adaugă un mic indicator vizual (ex: iconiță de "curățare" sau status "Buffer eliberat") imediat după finalizarea transcrierii AI, pentru a întări încrederea utilizatorului că datele audio au fost eliminate din RAM.
- **Accessibility:** Deși contrastul este >= 4.5:1, asigură-te că stările de `focus-visible` pe butoanele de control (Stop/Start) au un contur de minim 2px (outline solid), pentru a fi vizibile și pentru utilizatorii cu deficiențe de vedere care navighează prin tab-uri.
- **AI Managed:** În modul "Managed", adaugă un disclaimer vizual (tooltip sau text mic sub butonul de stop) care să specifice explicit: "Prompt-ul este procesat prin releu, nu este E2EE". Este deja documentat, dar o prezență constantă în UI reduce riscul de "uitare" a utilizatorului.

---
**NOTĂ AUDITOR:**
Soluția demonstrează o maturitate tehnică ridicată în gestionarea riscurilor (Security-by-Design). Implementarea `AbortController` pentru timeout-urile de rețea și utilizarea `Trusted Types` fără excepții sunt măsuri de protecție robuste. Abordarea "Local-First" cu handoff-uri user-initiated (mailto/ICS/Calendar) elimină vectorii de atac server-side și respectă principiul de minimizare a datelor. Mecanismul de curățare a bufferelor audio în `finally` garantează integritatea memoriei chiar și în scenarii de eroare. **Audit închis.**

## AI & Data Ethics Auditor — APROBAT
VERDICT: APROBAT

BLOCANTE:
- Niciuna. (Audit-ul confirmă implementarea remediilor de tip *hardening* pentru Trusted Types, gestionarea atomică a memoriei și separarea clară între logica de business și cea de securitate).

RECOMANDARI:
- **Audit de memorie:** Deși `wipe()` este implementat corect ca *best-effort*, recomand adăugarea unui avertisment vizual în UI (ex: "Sesiune activă în RAM") care să dispară doar la `unload` complet al ferestrei, pentru a preveni iluzia persistenței datelor în tab-uri inactive.
- **Trusted Types:** Având în vedere că aplicația este *single-file*, asigurați-vă că politica `trustedTypes.createPolicy` este definită înainte de orice execuție de script, pentru a evita *race conditions* în browserele care aplică CSP riguros.
- **Transparență AI:** În modul "Managed" (proxy), asigurați-vă că *endpoint*-ul de *logging* al proxy-ului (dacă există) este menționat în panoul de confidențialitate ca fiind un punct de colectare a metadatelor (nu a conținutului, dacă e E2EE), pentru a menține consistența cu promisiunea de *zero-knowledge*.

**Notă auditor:** Soluția a trecut de la un prototip cu "security theater" la o arhitectură robustă, cu *hardening* activ (CSP, Trusted Types, DOM API pur) și o onestitate remarcabilă în documentarea limitărilor tehnice (ex: *best-effort memory clearing*). Structura de *feedback* vizual și eliminarea jargonului financiar fabricat (KPI-uri "est.") aliniază produsul cu standardele de etică AI cerute.

## Quality & QA Auditor — RESPINS
VERDICT: **RESPINS**

**BLOCANTE:**
- **Riscul de "Audio Leak" pe iOS:** Deși documentezi eliberarea bufferelor, Web Speech API pe iOS (WebKit) are un comportament instabil la `visibilitychange` care poate lăsa un `MediaStream` activ în fundal (microfonul rămâne "aprins" cu indicatorul portocaliu/verde activ) dacă `track.stop()` nu este apelat explicit în toate ramurile de eroare/abort.
- **Trusted Types "Defense-in-Depth" iluzoriu:** Afirmi că TT este activ, dar `CSP` nu poate fi forțat într-un `single-file` fără a avea control asupra headerelor HTTP de pe serverul care livrează fișierul. Dacă fișierul e deschis local (file://) sau descărcat, CSP-ul definit în `<meta>` este adesea ignorat sau incomplet implementat de browsere pentru directivele de tip `require-trusted-types-for`.
- **Race condition în `finally`:** În `recFinalize`, dacă `AbortController` declanșează `abort` exact în momentul în care `Whisper` returnează un răspuns, există riscul ca `REC.audioBlob = null` să fie executat în timp ce transcrierea încă accesează bufferul (dacă nu este gestionat prin `Promise.all` sau `await` secvențial strict).
- **Lipsa sanitizării la `clipboard`:** Deși randarea e sigură, `follow-up`-ul copiat în clipboard poate conține caractere de control sau secvențe care, dacă sunt lipite ulterior într-un context vulnerabil (ex: un alt app/email client), pot facilita atacuri de tip "Clipboard Injection" sau "Command Injection" (dacă userul lipește textul într-un shell/editor care interpretează caracterele).

**RECOMANDARI:**
- **Zeroing Memory:** Implementează `WebAssembly` pentru buffer-ul audio (un `WebAssembly.Memory` buffer) — este singura metodă prin care poți garanta că memoria este suprascrisă determinist, spre deosebire de `Uint8Array` în JS care depinde de GC-ul browserului.
- **Audio-Context Isolation:** Folosește `AudioContext` cu `close()` explicit pentru a asigura eliberarea hardware-ului la nivel de OS, nu doar `track.stop()`.
- **Hardening:** Adaugă un `Content-Security-Policy` în `meta` care să includă `base-uri 'none'` și `form-action 'none'` pentru a bloca

## Business & Compliance Auditor — APROBAT
VERDICT: APROBAT

BLOCANTE:
- Niciuna. (Auditarea a confirmat: eliminarea sink-urilor XSS, implementarea Trusted Types, modelul de amenințare documentat onest, eliberarea atomică a bufferelor audio și etichetarea corectă a estimărilor).

RECOMANDARI:
- **Hardening Memorie:** Deși `wipe()` este implementat, recomand adăugarea unui `FinalizationRegistry` pentru a monitoriza și a sugera colectarea gunoiului (GC) după sesiunile de înregistrare, pentru a reduce fereastra de persistență a fragmentelor audio în heap.
- **UX Transparency:** În panoul de "Confidențialitate", adăugați o notă vizibilă despre faptul că Web Speech API (pe Android/Chrome) poate trimite date către serverele Google/furnizorului de browser, independent de controlul aplicației, pentru a completa etichetarea "Local-Only".
- **E2EE Discovery:** Documentați explicit faptul că, în modul "Discovery", metadatele (cheia publică) sunt vizibile pentru releu, astfel încât utilizatorul să nu confunde anonimatul identității cu anonimatul relației de conexiune.