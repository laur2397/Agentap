# BACKLOG SECRETARA — loop de 20 (din review-ul de board)

Note: din review, urmatoarele erau DEJA implementate (nu le refac): persistenta localStorage criptata,
export/import JSON, cautare fuzzy globala, badge-uri pt. task-uri scadente, backup criptat AES-GCM,
sortare task-uri dupa termen, jurnal de audit, confirmare la stergere. Mai jos sunt 20 NOI.

Reguli: schimbare mica, izolata; zero innerHTML (DOM API); criptare/CSP/TrustedTypes/accesibilitate pastrate.
Validare: node --check + smoke Playwright zero erori. Audit (examples/audit.py) la fiecare al 3-lea item.

## Prioritizat
1. [x] Ecran „Azi”: task-urile scadente azi + intalnirile de azi, intr-un singur loc pe Secretara.
2. [x] Editare task (text + termen), nu doar adaugare/stergere.
3. [x] Editare notita existenta (inline), nu doar adaugare/stergere.
4. [x] Prioritate task (normal/important) + sortare cu importantele sus.
5. [x] „Snooze” task: buton care impinge termenul cu +1 zi.
6. [x] Quick-add task cu detectie de data in text („maine”, „luni”, „in 3 zile”).
7. [x] Pin la notite: notitele fixate apar sus in jurnal.
8. [x] Status relatie per conexiune (Rece / Activ / Prioritar) + filtrare in Reteaua.
9. [x] Vizualizare saptamanala a intalnirilor (mini-calendar pe 7 zile).
10. [x] Notita de rezultat atasata unei intalniri confirmate („cum a mers”).
11. [x] Mod Focus: ascunde tot, lasa doar notita activa + input rapid.
12. [x] Quick-add global (buton + / tasta) pentru notita sau task de oriunde.
13. [x] Rezumat in antetul Secretarei: N task-uri active · M intalniri viitoare.
14. [x] Timeline per persoana: notite + task-uri + intalniri, cronologic, in brief.
15. [x] Remindere intalniri: evidentiaza intalnirile din urmatoarele 24h.
16. [ ] Notificari browser (opt-in, Notification API) pentru task-uri scadente — onest despre permisiune.
17. [ ] Filtrare jurnal pe interval de timp (azi / saptamana / tot).
18. [ ] Duplicare task (sablon rapid pentru sarcini recurente).
19. [ ] Marcaj „toate task-urile vizibile ca finalizate” (bulk done) cu confirmare.
20. [ ] Export doar al intalnirilor confirmate ca un singur fisier .ics (agenda completa).
