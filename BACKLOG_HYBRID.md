# BACKLOG HYBRID — loop 4 (raspuns la raportul investitorilor, FARA server)

Sursa: INVESTOR_REPORT.md (panel 100 investitori, verdict 0/100 investesc).
Decizie fondator: HIBRID FARA SERVER — pastram Local-Only/single-file/etica, dar atacam top-obiectiile
cu mijloace fara backend. NU implementam: backend, conturi cloud, sync server-side, gamificare/dark-patterns.

Maparea pe obiectii:
- #1 Zero network effects / discovery  -> cod de conexiune + QR, schimb fata-in-fata (P2P manual, fara server)
- #2 Multi-device / #5 pierdere date    -> backup criptat (.eie) + restore + transfer pe alt dispozitiv
- #9 Frictiune intrare date             -> template-uri notite + import/export mai usor
- #10 'Privacy-only'                     -> pozitionare Local-Only clara + ICP

Reguli per item: schimbare mica, izolata; ZERO innerHTML (DOM API); criptare/CSP/TrustedTypes/WCAG pastrate;
fara backend, fara integrari false, fara dark-patterns. Validare: node --check + smoke Playwright zero erori.
Audit (examples/audit.py) la fiecare al 3-lea item.

## Prioritizat
1. [x] Backup criptat dedicat (.eie): export al datelor criptat cu o parola de backup (PBKDF2+AES-GCM).
2. [x] Restore din backup criptat: import fisier .eie + parola -> restaureaza (si transfer pe alt dispozitiv).
3. [x] Reminder bland de backup pe Acasa daca au trecut >14 zile de la ultimul backup (neintruziv, dismissable).
4. [x] Cod de conexiune: genereaza un cod partajabil cu cardul tau PUBLIC (nume, domeniu, ce oferi — NU ce cauti).
5. [x] Adauga o conexiune prin cod: lipesti codul cuiva -> apare ca persoana cunoscuta in reteaua ta.
6. [x] QR pentru codul de conexiune: randare QR (encoder vanilla, fara biblioteci) pentru schimb fata-in-fata.
7. [x] Ecran „Schimba contacte la intalnire": genereaza codul/QR-ul tau + camp de lipit codul celuilalt, intr-un loc.
8. [x] Template-uri de notite (dupa apel / follow-up / idee) — un click insereaza structura.
9. [x] Pozitionare Local-Only clara: onboarding scurt „de ce datele raman la tine" + nota ICP in „Despre".
