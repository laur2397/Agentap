# SPRINT_LOG_SECRETARA — loop 2 (Secretara)

- 2026-05-31 · Item 1 (Ecran Azi) · sus pe Secretara: intalnirile de azi + task-urile scadente azi; validat, 0 erori.
- 2026-05-31 · Item 2 (Editare task) · buton ✎ -> inputuri text+termen inline -> Salveaza/Renunta; validat, 0 erori.
- 2026-05-31 · Item 3 (Editare notita) · buton ✎ -> input inline -> Salveaza; reactualizeaza #tag-urile; validat, 0 erori.
- 2026-05-31 · AUDIT item 3 (secloop3): APROBAT 6/6 + CAE.
- 2026-05-31 · Item 4 (Prioritate task) · stea ☆/★ pe task; importantele sus la sortare; validat, 0 erori.
- 2026-05-31 · Item 5 (Snooze task) · buton ⏰ -> termen +1 zi (min. maine); validat, 0 erori.
- 2026-05-31 · Item 6 (Quick-add cu data) · parseDue() detecteaza azi/maine/poimaine/zi-saptamana/'in N zile' din text si seteaza termenul; validat, 0 erori.
- 2026-05-31 · AUDIT item 6 (secloop6): APROBAT 6/6 + CAE.
- 2026-05-31 · Item 7 (Pin notite) · buton 📌 fixeaza notita sus (sort pin desc), marcaj vizual; validat, 0 erori.
- 2026-05-31 · Item 8 (Status relatie) · pastila Rece/Activ/Prioritar pe conexiune (tap cicleaza, nu deschide conversatia) + chips de filtrare in Reteaua; validat, 0 erori.
- 2026-05-31 · Item 9 (Mini-calendar saptamanal) · banda 7 zile cu azi evidentiat + bulina/numar pe zilele cu intalniri; tap -> toast cu intalnirile zilei; validat, 0 erori.
- 2026-05-31 · AUDIT item 9 (secloop9): APROBAT 6/6 + CAE.
- 2026-05-31 · Item 10 (Rezultat intalnire) · notita 'cum a mers' atasata intalnirilor confirmate (adauga/editeaza/afiseaza); validat, 0 erori.
- 2026-05-31 · Item 14 (Timeline persoana) · in brief-ul de 1 minut, sectiune "Istoric": notite + task-uri + intalniri legate de persoana, cronologic (recent->vechi), max 6, cu marca de timp relativa; validat Playwright (3 randuri: notita+task+intalnire), 0 erori.
- 2026-05-31 · Item 13 (Rezumat antet) · doua pastile sub titlul Secretarei: N task-uri active · M intalniri viitoare (acord gramatical singular/plural); se actualizeaza la fiecare render; validat Playwright (eticheta + actualizare la adaugare task), 0 erori.
- 2026-05-31 · AUDIT item 12 (secloop12): APROBAT 6/6 + CAE ("poarta de audit inchisa cu succes"; recomandari neblocante notate: PBKDF2 600k, frame-ancestors, indicator auto-lock).
- 2026-05-31 · Item 12 (Quick-add global) · buton ＋ in antet + tasta "n" (ignorata in campuri) -> sheet de jos cu toggle Notita/Task, input + termen optional (parseDue pt. task), salveaza din orice ecran; validat Playwright (deschidere buton+tasta, toggle, due ascuns/afisat, task & notita adaugate, "n" ignorat in input), 0 erori.
- 2026-05-31 · Item 11 (Mod Focus) · buton 🎯 Focus ascunde tot pe Secretara (CSS .focusing), lasa captura rapida (#focusQuick, Enter/+) + task-urile scadente azi + ultimele 3 notite; toggle iesire; validat Playwright (FOCUS_BTN/FOCUSING_CLASS/QUICK_VISIBLE/NOTE_IN_PANEL/WEEKCAL_HIDDEN/WEEKCAL_BACK toate OK), 0 erori JS (doar fontul offline ERR_CERT, de mediu).
