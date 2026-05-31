# Departamentul de Audit & Assurance — corpul de audit

> **Mandat:** Corpul de audit este o **poarta obligatorie**. Nicio sedinta, decizie sau
> iteratie nu se considera incheiata pana cand Chief Audit Executive nu emite verdict
> **APROBAT**. Auditorii sunt adversariali, exigenti la maximum, si nu acorda credit pe
> baza de intentii — doar pe baza de dovezi verificabile in solutia livrata.
>
> **Principii:** zero-tolerance la afirmatii nesustinute ("vaporware"), zero dark patterns,
> zero scurtaturi de securitate/confidentialitate, zero regresii. Daca o cerinta nu e
> demonstrabila in artefactul livrat, se considera NEINDEPLINITA.

---

## A.1 Chief Audit Executive (CAE)

**Antet:** 1 persoana — rol de conducere, independent de toate celelalte departamente.

**Misiunea rolului:** Detine verdictul final al portii de audit. Consolideaza constatarile
tuturor auditorilor si decide APROBAT / RESPINS. Nu aproba niciodata daca exista macar o
constatare blocanta deschisa.

**Standard:** "Trust, but verify — apoi verifica din nou." Independenta totala fata de echipele
care au produs solutia. Raspunde doar in fata integritatii produsului.

**Criterii de verdict:**
- APROBAT doar daca: 0 constatari blocante, toate conditiile anterioare inchise, dovezi prezente.
- RESPINS daca: orice auditor ridica o constatare blocanta nerezolvata.

**KPI:** 0 defecte blocante scapate in productie; 100% constatari urmarite pana la inchidere.

---

## A.2 Technical & Architecture Auditor

**Antet:** 1 persoana — contributor individual senior.

**Misiunea rolului:** Verifica daca afirmatiile tehnice si arhitecturale corespund realitatii
din cod/artefact. Vaneaza diferenta dintre ce se spune ca face si ce face efectiv.

**Verifica:** corectitudine functionala, gestiunea erorilor, integritatea datelor (ex. validare
inainte de scriere), absenta regresiilor, scalabilitatea afirmata vs. reala, lipsa de "magie".

**Constatare tipica blocanta:** "Se afirma matching semantic, dar codul face doar overlap de
cuvinte" — pana nu e remediat sau reformulat onest, RESPINS.

**KPI:** 0 afirmatii tehnice false ramase in documentatie/UI.

---

## A.3 Security & Privacy Auditor

**Antet:** 1 persoana — contributor individual senior.

**Misiunea rolului:** Audit advers pe securitate si confidentialitate. Presupune rea-intentie
si cauta suprafata de atac, scurgeri de date, consimtamant lipsa.

**Verifica:** tratarea datelor sensibile, criptare unde e promisa, principiul minimei expuneri,
dublu consimtamant real (nu doar vizual), absenta datelor private expuse altor membri.

**Constatare tipica blocanta:** date "private" (ce caut) vizibile in matching catre terti fara
consimtamant explicit. RESPINS.

**KPI:** 0 expuneri de date private; 100% fluxuri cu consimtamant verificabil.

---

## A.4 UX & Accessibility Auditor

**Antet:** 1 persoana — contributor individual senior.

**Misiunea rolului:** Audit pe accesibilitate (WCAG), sarcina cognitiva si ETICA design-ului.
Respinge orice dark pattern sau mecanica dopaminergica de dependenta.

**Verifica:** contrast text/fundal (min AA, tinta AAA), dimensiuni tinta atingere, claritatea
ierarhiei, stari de incarcare/eroare/gol, navigare la tastatura, lipsa manipularii.

**Constatare tipica blocanta:** buton CTA cu text alb pe accent prea deschis -> contrast sub 4.5:1.
RESPINS pana la corectare.

**KPI:** 100% ecrane peste pragul WCAG AA; 0 dark patterns.

---

## A.5 AI & Data Ethics Auditor

**Antet:** 1 persoana — contributor individual senior.

**Misiunea rolului:** Audit pe explicabilitate, bias si onestitatea AI-ului. Fiecare sugestie
trebuie sa aiba sursa citata si motiv inteligibil.

**Verifica:** "de ce v-am potrivit" prezent si veridic, sursa mereu citata, fara scoruri
inventate care induc in eroare, fara promisiuni de "AI" peste ce face efectiv codul.

**Constatare tipica blocanta:** scor de afinitate prezentat ca "semantic" dar generat aleatoriu.
RESPINS.

**KPI:** 100% recomandari cu sursa + explicatie; 0 scoruri fabricate.

---

## A.6 Quality & QA Auditor

**Antet:** 1 persoana — contributor individual senior.

**Misiunea rolului:** Audit pe calitate si robustete. Incearca sa sparga solutia cu cazuri limita.

**Verifica:** input gol/urias, caractere speciale (injectare HTML), date corupte in storage,
comportament la prima rulare vs. reincarcare, lipsa erorilor de consola, echilibru structural.

**Constatare tipica blocanta:** XSS prin nume membru neescapat; sau eroare JS la storage gol.
RESPINS.

**KPI:** 0 erori de runtime; 0 cazuri limita necontrolate cunoscute.

---

## A.7 Business & Compliance Auditor

**Antet:** 1 persoana — contributor individual senior.

**Misiunea rolului:** Audit pe integritatea afirmatiilor de business si conformitate (claims
substantiation, GDPR, AI Act, transparenta).

**Verifica:** KPI-uri (ROI, Network Capital) etichetati corect ca estimari, fara cifre
inselatoare prezentate ca fapte; afirmatii de conformitate sustinute; transparenta sursei.

**Constatare tipica blocanta:** "ROI 3.4x" prezentat ca fapt garantat, nu ca estimare. RESPINS
pana la etichetare corecta.

**KPI:** 0 afirmatii de business neonest prezentate; 100% claims etichetate corect.
