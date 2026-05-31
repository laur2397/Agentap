# SPRINT_LOG_HYBRID — loop 4 (raspuns la investitori, fara server)

- 2026-05-31 · Item 3 (Reminder backup) · nudge bland pe Acasa cand nu exista backup sau au trecut >14 zile; dismissable (tacut 7 zile dupa "Mai tarziu"); dispare dupa un backup recent; neintruziv, fara dark-pattern; validat Playwright (apare fresh, ascuns dupa dismiss, ascuns dupa backup recent), 0 erori.
- 2026-05-31 · Item 1+2 (Backup criptat .eie + Restore/transfer) · export .eie criptat cu o parola de backup separata (deriveKey PBKDF2-150k + AES-GCM), restore cu validare schema + confirmare + backupRaw anti-pierdere; raspunde obiectiilor investitorilor #2 (multi-device) si #5 (pierdere date) FARA server; validat Playwright round-trip (backup criptat -> nota stearsa -> restaurata; token NU apare in clar), 0 erori.
- 2026-05-31 · Panel 100 investitori -> INVESTOR_REPORT.md (0/100 investesc). Decizie: hibrid fara server. Backlog de 9 itemi (BACKLOG_HYBRID.md).
