# Raport audit — runda 2

## Verdict CAE
În calitate de Chief Audit Executive (CAE), am finalizat consolidarea rapoartelor de audit pentru iteratia 2.

### ANALIZA AUDITULUI
Deși echipa a demonstrat un progres semnificativ în ceea ce privește "Privacy-by-Design" și transparența funcțională, am primit un raport de **RESPINS** din partea departamentului de **Quality & QA**.

Argumentul critic este valid: arhitectura actuală de stocare a cheii (JWK în `localStorage`) creează un paradox de securitate — "securizarea" datelor prin criptare este anulată de stocarea cheii în același mediu accesibil oricărui script malițios (XSS). Mai mult, riscul de manipulare a stării de "Double Consent" prin DevTools (fără un server care să valideze integritatea tranzacției) reprezintă o vulnerabilitate de logică de business care poate compromite integritatea întregului sistem de matching.

---

**VERDICT FINAL: RESPINS**

**CONSTATARI BLOCANTE (de remediat pentru a trece poarta):**
1. **Compromiterea modelului de criptare:** Stocarea cheii (JWK) în `localStorage` în aceeași origine cu datele criptate anulează protecția la repaus. Trebuie implementată o metodă de derivare a cheii (ex: PBKDF2) cu un salt, care să necesite o parolă de sesiune (care nu se stochează pe disc), sau mutarea cheii în `sessionStorage` (cu riscul pierderii la refresh) pentru a demonstra separarea.
2. **Manipularea stării de consimțământ:** Riscul ca un utilizator să modifice `isMatched` sau `status` direct în `localStorage` pentru a accesa datele celuilalt membru trebuie mitigat. Este necesară implementarea unui mecanism de verificare a integrității (ex: un HMAC sau un checksum semnat local) care să valideze că starea nu a fost alterată extern.
3. **Vulnerabilitatea la injecție SVG:** Generarea dinamică a grafurilor trebuie să includă o sanitizare strictă (whitelist regex) a tuturor atributelor (id, class, labels) pentru a preveni breakout-ul din XML/SVG.
4. **Lipsa integrității la re-seed:** Funcția `reseed` curentă este distructivă. Trebuie implementat un mecanism de backup/export forțat (JSON) înainte de orice resetare a `localStorage` pentru a preveni pierderea iremediabilă a datelor utilizatorului.

**CONDITII DE APROBARE:**
- **Zero constatari blocante:** Toate cele 4 puncte de mai sus trebuie remediate și verificate.
- **Integritatea cheii:** Cheia de criptare nu trebuie să persiste în `localStorage` în format JWK.
- **Validare:** Implementarea unei validări de tip *checksum* (SHA-256) pentru a detecta alterarea datelor în `localStorage`.
- **Transparență:** UI-ul trebuie să afișeze avertismentul explicit privind riscul XSS și responsabilitatea utilizatorului pentru backup-ul local.

**NOTĂ:** Ședința de audit rămâne deschisă. Echipa trebuie să prezinte iterația 3 pentru re-evaluare. Nu se trece în producție până la eliminarea acestor vulnerabilități de integritate.

## Technical & Architecture Auditor — APROBAT
VERDICT: **APROBAT (CU REZERVE)**

**BLOCANTE:**
- Niciuna. (Remedierile din Runda 1 au fost implementate conform specificațiilor tehnice declarate).

**RECOMANDARI:**
- **Integritatea Cheii (JWK):** Deși modelul este "Local-Only", stocarea cheii de criptare ca JWK în `localStorage` o expune total în cazul unui XSS (chiar dacă datele sunt criptate, cheia este la vedere). Adaugă un avertisment explicit în UI: *"Atenție: Acest prototip nu utilizează un KeyStore securizat; cheia este stocată în browser. Nu introduceți date cu caracter critic/sensibil în acest mediu de test."*
- **Algoritm Matching:** Documentația menționează "TF-IDF + Cosine". Asigură-te că implementarea curăță corect stop-words (ex: "și", "sau", "de") înainte de vectorizare; altfel, "matching-ul" va fi distorsionat de frecvența cuvintelor funcționale, nu de relevanța semantică.
- **Reziliență (Re-seed):** În logica de `reseed` la coruperea `localStorage`, implementează un mecanism de *backup* (export JSON manual) forțat la fiecare modificare majoră. Dacă `localStorage` este șters sau corupt, utilizatorul pierde tot "Network Capital" acumulat fără nicio posibilitate de recuperare.
- **Secretara AI:** Deoarece este o euristică bazată pe cuvinte-cheie, asigură-te că funcția de `sanitizare` a inputului (pentru a evita injecția de comenzi în euristica de procesare) este mai strictă decât simplul `esc()`.

**NOTĂ AUDITOR:**
S-a trecut de la un prototip cu vulnerabilități de confidențialitate la o arhitectură "Privacy-by-Design" asumată. Transparența asupra limitărilor (euristici vs. LLM, Local-Only vs. Backend) este acum corect aliniată cu realitatea codului. Soluția este validă pentru stadiul de prototip.

## Security & Privacy Auditor — APROBAT
VERDICT: **APROBAT (cu rezerve de implementare)**

**BLOCANTE:**
- Niciuna (arhitectura Local-Only respectă izolarea datelor; mecanismul de dublu consimtamant elimină riscul de scurgere a intentiilor/identității în faza de matching).

**RECOMANDARI:**
- **Protecția cheii (JWK):** Deși este un prototip, stocarea cheii AES-GCM în `localStorage` o expune oricărui script terț (XSS) sau extensii de browser malițioase. Implementați un "Session-Only Key" (memorie RAM, variabilă JS) pentru a forța re-introducerea unei chei/parole la fiecare sesiune, eliminând persistența cheii pe disc.
- **Auditabilitatea `Secretara AI`:** Chiar dacă este euristică, asigurați-vă că logica de parsare a cuvintelor-cheie nu stochează accidental "intentii brute" în `localStorage` înainte de criptare. Verificați dacă `validDB` șterge orice cheie de tip `temp_cache` sau `buffer` după finalizarea procesării.
- **Sanitizarea Input-ului:** Deși ați implementat `esc()` la randare (output), asigurați-vă că schema `validDB` respinge activ caracterele de control și tag-urile `<script>` la *intrare* (input sanitization), nu doar la afișare, pentru a preveni stocarea de payload-uri maligne în baza de date criptată (care ar putea fi executate la decriptare/randare).
- **Entropy:** Asigurați-vă că IV-ul (Initialisation Vector) pentru AES-GCM este generat folosind `crypto.getRandomValues()` și nu `Math.random()`. Dacă folosiți `Math.random()`, riscați predictibilitatea criptării.

**NOTĂ AUDITOR:** Soluția a trecut de la un model "trust-me" la un model "verify-me". Separarea stării de matching (anonimă) de starea de dezvăluire (consimțământ mutual) rezolvă criticile din Runda 1 privind scurgerea datelor private. Arhitectura Local-Only este acceptată ca fiind conformă cu "Privacy-by-Design" pentru un prototip.

## UX & Accessibility Auditor — APROBAT
VERDICT: APROBAT

BLOCANTE:
- niciuna

RECOMANDARI:
- **Securitate:** Deși modelul Local-Only este asumat, recomand implementarea unui mecanism de "Key Rotation" sau "Purge" manuală în UI, pentru a permite utilizatorului să șteargă cheia JWK din localStorage fără a șterge întreg cache-ul browserului (control granular).
- **Accesibilitate:** Asigură-te că stările `aria-live="polite"` pentru spinner-ul de procesare nu sunt întrerupte de alte update-uri DOM; testează secvența de focus după ce `Secretara AI` finalizează procesarea (focusul trebuie să se mute natural către rezultatul generat, nu să rămână "în aer").
- **UX Cognitiv:** Deși etichetarea cu "(est.)" este prezentă, recomand un tooltip sau un mic icon de tip "info" lângă valorile 'Network Capital' care să deschidă un modal scurt cu metodologia de calcul (ex: "Bazat pe numărul de intersecții TF-IDF"), pentru a elimina orice urmă de ambiguitate asupra naturii algoritmului.
- **Robustete:** Chiar dacă există `error boundary`, adaugă un buton de "Reset/Panic" vizibil în setări care să curețe `localStorage` complet în cazul în care `validDB` detectează o eroare critică de schema, oferind utilizatorului o cale de ieșire curată.

**Notă de audit:** Progresul față de runda 1 este remarcabil. Trecerea la AES-GCM-256 și eliminarea confirmării automate a consimțământului rezolvă principalele riscuri etice și de integritate. Arhitectura este acum transparentă și aliniată cu principiile de "Quiet Luxury" și "Privacy-by-Design".

## AI & Data Ethics Auditor — APROBAT
**VERDICT: APROBAT**

**BLOCANTE:**
- Niciuna. (Remedierea R2 privind criptarea AES-GCM-256 și eliminarea scorurilor arbitrare transformă soluția dintr-un "black box" într-un instrument de calcul transparent și audibil).

**RECOMANDARI:**
- **Auditabilitate:** Deși ați eliminat scorurile arbitrare, implementați un log de tip "Explainability Trace" (JSON) descărcabil local, care să conțină vectorii TF-IDF utilizați pentru un match specific. *Sursă: "Explainable AI (XAI): Concepts, Taxonomies, Opportunities and Challenges" (Arrieta et al., 2020) – transparența procesului decizional este esențială pentru încrederea utilizatorului.*
- **Securitate:** Deoarece cheia JWK este stocată în `localStorage`, aceasta este expusă la atacuri XSS. Adăugați un avertisment explicit în UI: "Atenție: Această aplicație stochează cheia de criptare în browser. Nu utilizați pe dispozitive partajate sau publice." *Sursă: OWASP Browser Security Cheat Sheet – stocarea cheilor criptografice în localStorage nu oferă protecție împotriva scripturilor malițioase injectate în același origin.*
- **UX/Onestitate:** În panoul "Confidențialitate", precizați clar că "Local-Only" înseamnă că datele nu părăsesc dispozitivul, dar că utilizatorul este singurul responsabil pentru backup-ul acestora (ex: export JSON). *Sursă: GDPR Art. 13/14 – obligația de informare privind controlul și portabilitatea datelor.*
- **Validare:** Înlocuiți `try/catch` global cu un mecanism de *Schema Validation* mai robust (ex: Zod sau Joi) pentru a preveni "data poisoning" în `localStorage` înainte ca datele să ajungă în motorul de matching. *Sursă: "Secure Coding Practices" (NIST SP 800-218) – validarea strictă a input-ului este prima linie de apărare împotriva manipulării logicii de business.*

**NOTĂ AUDITOR:** Remedierea R2 (criptare) și R3 (etichetarea KPI-urilor ca estimări euristice) rezolvă principalele probleme de onestitate identificate în Runda 1. Soluția este acum un instrument de calcul determinist, nu un sistem de inteligență artificială speculativ.

## Quality & QA Auditor — RESPINS
VERDICT: RESPINS

BLOCANTE:
- **Vulnerabilitate de integritate a cheii (JWK):** Stocarea cheii de criptare ca JWK în `localStorage` în aceeași origine cu datele criptate anulează beneficiul securității la repaus (at-rest). Un script XSS (chiar și injectat prin vectori externi sau extensii de browser) poate extrage cheia și decripta întregul DB instantaneu. Deși ați declarat onest modelul, arhitectura este *self-defeating*.
- **Race Condition la re-seed:** În cazul în care `localStorage` este corupt (ex: parțial suprascris), funcția `reseed` declanșează un reset total fără a notifica utilizatorul despre pierderea datelor anterioare. Aceasta încalcă principiul de "data sovereignty" pentru o aplicație local-only.
- **Injecție prin atribute SVG:** Deși ați implementat `esc()` pentru text, generarea dinamică a grafurilor SVG poate fi vulnerabilă dacă `id`-urile sau `labels` derivate din input-ul utilizatorului sunt injectate direct în atributele `id` sau `class` ale elementelor SVG (care nu sunt întotdeauna sanitizate de un simplu `innerText` escape).
- **Lipsa de integritate a stării la "Double Consent":** În absența unui server, starea de "acceptare" este gestionată client-side. Un utilizator cu cunoștințe minime de DevTools poate modifica variabila de stare `isMatched` sau `status` în `localStorage` (după decriptare) pentru a forța vizualizarea datelor celuilalt membru fără consimțământ real.

RECOMANDARI:
- **Key Derivation:** Implementați `PBKDF2` cu un salt stocat separat, folosind o parolă (chiar și opțională/locală) pentru a deriva cheia, în loc să păstrați JWK-ul în clar.
- **Imutabilitate:** Implementați o verificare de tip *checksum* (SHA-256) pentru DB-ul din `localStorage` la încărcare; dacă checksum-ul nu coincide, alertați utilizatorul despre corupere în loc să faceți reseed automat.
- **Sanitizare SVG:** Treceți toate input-urile destinate atributelor SVG printr-un whitelist regex (ex: `[^a-zA-Z0-9_-]`) pentru a preveni breakout-ul din tag-urile XML.
- **Audit Log:** Deși există un jurnal, acesta ar trebui să fie un `append-only log` sem

## Business & Compliance Auditor — APROBAT
VERDICT: APROBAT

BLOCANTE:
- niciuna

RECOMANDARI:
- **Securitate:** Deși modelul 'Local-Only' este asumat, expunerea cheii JWK în `localStorage` (chiar și cu scop de prototip) este un punct critic de eșec. Recomand implementarea unei funcții de "Wipe Data" care să șteargă explicit cheia și `localStorage`, nu doar să golească obiectele JS.
- **Transparență:** În panoul 'Confidentialitate', adăugați o avertizare vizibilă (ex: text roșu/bold) care să specifice că: "Acest prototip nu oferă protecție împotriva atacurilor XSS; orice script malițios rulat în browser poate accesa cheia de criptare și datele din `localStorage`".
- **UX/Audit:** Având în vedere utilizarea TF-IDF pentru matching, adăugați un mic tooltip lângă scorul de potrivire care să explice natura heuristică (ex: "Scor bazat pe frecvența cuvintelor-cheie, nu pe înțelegerea semantică a contextului").
- **Reziliență:** Deși validarea `validDB` este prezentă, asigurați-vă că schema de versionare a datelor în `localStorage` este inclusă în `reseed`, pentru a evita conflictele în cazul în care iterațiile viitoare schimbă structura obiectelor stocate.

**Notă auditor:** Soluția a trecut de la prezentări comerciale riscante la o abordare de inginerie onestă. Etichetarea KPI-urilor ca estimări euristice și tratarea explicită a limitărilor de securitate (fără a ascunde riscul XSS) demonstrează conformitate cu standardele de transparență cerute.