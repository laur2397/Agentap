# Strategia Secretarei AI — sedinta de bord

# SECRETARA_STRATEGIE.md

## 1. VIZIUNE
Secretara AI a Cercului EIE devine **Chief-of-Staff-ul tău personal**, un sistem de suport digital care nu "gândește" în locul tău, ci îți organizează memoria și resursele. Este o extensie a voinței tale, transformând interacțiunile de business din simple conversații în active de rețea, totul într-un mediu securizat, local și 100% controlat de utilizator.

---

## 2. CAPABILITATI
*   **(a) Calendar & Întâlniri:** Vizualizarea ferestrelor de disponibilitate setate manual. Nu sincronizăm, ci gestionăm intern „sloturile de networking” marcate ca libere.
*   **(b) Idei & Notițe:** Jurnal de bord unde introduci manual insight-uri. Sistemul le indexează automat după etichete (keywords) pentru a fi regăsite instantaneu.
*   **(c) Remindere & Follow-up:** Sistem bazat pe task-uri cu deadline. Generare de text (fill-in-the-blanks) pentru mesaje de follow-up post-întâlnire, gata de copiat în orice canal extern.
*   **(d) Agenda & Pregătire:** „Brief-ul de 1 minut” generat din istoricul local: ce ai căutat/oferit data trecută, ce acțiuni au rămas deschise, care sunt punctele comune cu partenerul.
*   **(e) Programare între membri (Double-Opt-In):** Flux de cerere-confirmare. Propui o fereastră, celălalt acceptă în aplicația sa; ambele părți primesc confirmarea în „Jurnalul de Întâlniri”.

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

---

## 6. ROADMAP
1. **Iterația 1: „Sistemul de Indexare”** — Implementarea sistemului de notițe structurate și extragere de cuvinte-cheie (keywords) pentru crearea brief-ului de întâlnire.
2. **Iterația 2: „Brokerul de Conexiuni”** — Implementarea fluxului de double-opt-in (schimbul de disponibilitate între membri prin QR/Link local).
3. **Iterația 3: „Dashboard-ul de Management”** — Consolidarea tuturor funcțiilor în ecranul unic „Secretara”, adăugând logica de task-uri cu deadline și template-urile de follow-up.