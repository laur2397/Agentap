# Strategia Secretarei AI — sedinta de bord

# SECRETARA_STRATEGIE.md

## 1. VIZIUNE
Secretara AI a Cercului EIE devine **Chief-of-Staff-ul tău personal**, un sistem de suport digital care nu "gândește" în locul tău, ci îți organizează memoria și resursele. Este o extensie a voinței tale, transformând interacțiunile de business din simple conversații în active de rețea, totul într-un mediu securizat, local și 100% controlat de utilizator.

---

## 2. CAPABILITATI
*   **(a) Calendar & Întâlniri:** Vizualizarea ferestrelor de disponibilitate setate manual. Nu sincronizăm, ci gestionăm intern „sloturile de networking” marcate ca libere.
*   **(b) Idei & Notițe:** Jurnal de bord unde introduci manual insight-uri. Sistemul le indexează automat după etichete (keywords) pentru a fi regăsite instantaneu.
*   **(c) Remindere & Follow-up:** Sistem bazat pe task-uri cu deadline. Generare de text (fill-in-the-blanks) pentru mesaje de follow-up post-întâlnire, gata de copiat — **sanitizat strict (textContent), fără linkuri auto-generate**.
*   **(d) Agenda & Pregătire:** „Brief-ul de 1 minut” generat **DOAR din interacțiunile tale directe**: ce ai notat TU, ce ai căutat/oferit TU, ce acțiuni AI lăsat deschise. NU agregă profilul țintei fără consimțământul ei — afișează doar date publice asumate (ce oferă vizibil).
*   **(e) Programare între membri (Double-Opt-In):** Flux de cerere-confirmare **strict in-app** (fără QR/link extern cu date sensibile). Propui o fereastră, celălalt acceptă în aplicația sa; orice întâlnire **confirmată se scrie imuabil în Trust Ledger** (hash-chain) ca audit trail anti-dispută.

---

## 3. FEZABILITATE (Onestitate Tehnică)

| Funcționalitate | Status (Local/Single-file) | De ce amânăm (Backend/LLM) |
| :--- | :--- | :--- |
| **Matching Interese** | Deterministic (match pe keywords) | LLM-ul e necesar pt. sinonime/nuanțe. |
| **Calendar** | Manual (ferestre setate de user) | Integrarea API Google/Outlook cere server. |
| **Notificări** | UI-only (badge-uri în app) | Push notifications reale necesită server. |
| **Follow-up** | Template-uri tip „fill-in-the-blanks” | Generarea textului creativ necesită LLM. |
| **Sincronizare** | Manuală (Export/Import JSON) | Cloud sync-ul necesită backend securizat. |

---

## 4. UX: „Secretara AI”
*   **Ecranul „Secretara”:** Un dashboard minimalist, tip *feed de acțiuni*, nu un chatbot. Structura: „Pregătire pentru azi” (carduri cu membri), „Task-uri restanțe” și „Propune o întâlnire”.
*   **Limbaj:** Profesional, direct, non-robotizat. Fără „Sunt AI-ul tău și am calculat...”, ci „Iată detaliile din notițele tale pentru întâlnirea cu X”.
*   **Interfață:** Butoane de acțiune clare (ex: *„Generează mesaj follow-up”*, *„Trimite invitație”*).

---

## 5. ÎNCREDERE & LIMITĂRI (Declarație de Transparență)
*   **„Tu deții controlul”:** Datele tale părăsesc dispozitivul doar prin acțiunea ta explicită (export/share).
*   **„Fără Magie”:** Secretara nu ghicește ce vrei. Ea procesează strict ceea ce ai introdus. Dacă nu ai notat, nu există.
*   **„Erori de Human-Input”:** Acuratețea recomandărilor depinde de calitatea notițelor tale. Sistemul te încurajează să fii precis în cuvinte-cheie.
*   **„Brief doar despre tine”:** Brief-ul de întâlnire agregă DOAR interacțiunile tale directe, niciodată profilul privat al celuilalt fără consimțământ.
*   **„Fără artefacte externe”:** Programarea se face exclusiv prin consimțământul in-app; nu generăm QR/linkuri care ar putea scurge date.
*   **„Audit trail imuabil”:** Orice întâlnire confirmată intră în Trust Ledger (hash-chain HMAC), deci nu poate fi negată/alterată.
*   **Sanitizare:** Tot textul generat (follow-up, brief) trece prin `textContent` — fără vectori de injecție.

---

## 6bis. PROTOCOALE DE SIGURANTA (cerute de audit — integrate in arhitectura existenta)
*   **Terminologie corecta „Trust Ledger”:** Este un **jurnal local tamper-evident** (lant HMAC-SHA256 cheiat de parola), **NU** un blockchain cu consens/semnaturi asimetrice. Revocarea **nu sterge verigi** (asta ar rupe lantul) — adauga o **veriga noua de tip „revocare”**, pastrand integritatea. Verificarea lantului ruleaza la fiecare deschidere.
*   **Import/Export semnat digital (anti „sync poisoning”):** Pe langa validarea de schema, fisierele exportate se **semneaza ECDSA P-256** (WebCrypto, cheie a membrului, fara backend); la import se verifica **semnatura + schema** inainte de acceptare -> un JSON modificat/malitios e respins ca sursa neincrezatoare.
*   **Recuperare („Master Key”):** La setup se genereaza o **fraza de recuperare** (afisata o singura data, pastrata OFFLINE de utilizator) care permite re-derivarea cheii daca uita parola. Fara ea, pierderea parolei = pierdere de date (declarat onest). Elimina „blocarea permanenta dintr-o greseala de tastare”.
*   **Upgrade criptografic:** Iteratii **PBKDF2 ridicate la 600.000** (OWASP 2023) pentru cheia derivata din parola.
*   **Criptare la repaus:** Toate datele Secretarei (notite, intalniri, task-uri) se stocheaza in aceeasi baza criptata **AES-GCM** cu cheie **PBKDF2 (150k)** derivata din parola, doar in RAM (auto-lock + `wipe()`).
*   **Sanitizare input (anti-XSS):** Orice text introdus trece prin `clean()` la intrare si e randat exclusiv prin `textContent`/DOM API (zero `innerHTML`). Follow-up-urile/brief-urile nu contin markup.
*   **Validare schema la import:** Fisierele JSON importate (sync manual) trec printr-un validator de schema (`validDB` extins pt. notite/intalniri/task-uri) care filtreaza intrarile null/alterate; la esec -> respingere cu backup, fara coruperea bazei.
*   **Error handling & stocare:** Scriere tranzactionala (temp->validare->commit) cu rollback la `QuotaExceededError`; error boundary global; reset determinist al starii async.
*   **First Run:** Fluxul de initializare cand nu exista date — ecran de setare parola -> seed gol -> onboarding 3 pasi; toate functiile Secretarei trateaza starea goala (empty-states).
*   **Revocarea consimtamantului & „dreptul de a fi uitat” (P2P) — cu limitare ONESTA:** Revocarea (a) sterge datele local, (b) opreste orice partajare viitoare, (c) marcheaza in Trust Ledger un eveniment de revocare (imuabil) si (d) trimite o CERERE de stergere celeilalte parti. **Limitare declarata explicit: intr-un model P2P fara server NU putem GARANTA tehnic stergerea copiei deja ajunse la celalalt** — putem doar cere si inregistra cererea. Promitem doar ce putem impune; restul e declarat ca limita, nu ascuns.
*   **Integritate cronologica la sincronizare (limitare ONESTA):** Trust Ledger-ul actual e **single-writer** (un singur dispozitiv scrie) -> nu exista fork/race in stadiul curent. Sincronizarea multi-dispozitiv reala (care ar introduce evenimente concurente offline) e AMANATA si are ca **prerechizita** un mecanism de ordonare cauzala (Lamport timestamp / vector clock) + reconciliere de lant — fara el nu activam sync P2P automat, ca sa nu bifurcam/corupem lantul de hash.
*   **Jurnal de audit local:** Fiecare actiune a Secretarei (creare task, propunere intalnire, follow-up, revocare) se scrie in jurnalul read-only existent, cu marca de timp.

## 6. ROADMAP
1. **Iterația 1: „Sistemul de Indexare”** — Implementarea sistemului de notițe structurate și extragere de cuvinte-cheie (keywords) pentru crearea brief-ului de întâlnire.
2. **Iterația 2: „Brokerul de Conexiuni”** — Implementarea fluxului de double-opt-in (schimbul de disponibilitate între membri prin QR/Link local).
3. **Iterația 3: „Dashboard-ul de Management”** — Consolidarea tuturor funcțiilor în ecranul unic „Secretara”, adăugând logica de task-uri cu deadline și template-urile de follow-up.