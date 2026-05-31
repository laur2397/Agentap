# BACKLOG — dezvoltare continua (sprint loop)

Reguli pentru fiecare item:
- Schimbare MICA, izolata, reversibila. Pastreaza: zero innerHTML (DOM API h()/svgEl()), criptare,
  dublu consimtamant, CSP/TrustedTypes, accesibilitate (44px, focus, contrast).
- Valideaza: `node --check` pe script + smoke test Playwright cu ZERO erori de consola.
- Commit + push DOAR daca validarea trece. Logheaza in SPRINT_LOG.md.
- La fiecare 3 itemi, ruleaza board-ul de audit (examples/audit.py) si remediaza daca RESPINS.

## Prioritizat
1. [x] Sortare/filtrare task-uri: comutator „Toate / Active / Scadente”.
2. [x] Intalniri viitoare evidentiate pe Acasa (urmatoarea intalnire confirmata, sus).
3. [x] Reminder badge si pentru intalniri „De confirmat” (nu doar task-uri).
4. [x] Follow-up: 3 sabloane (multumire / propunere pas urmator / reprogramare).
5. [x] Brief de intalnire: include si task-urile deschise legate de persoana.
6. [x] Cautare globala (header): peste persoane, notite, task-uri.
7. [x] Empty-states ilustrate consistente (SVG) pe toate ecranele goale.
8. [x] Export complet (toate datele) + Import cu validare de schema + confirmare.
9. [x] Profil: editare nume/domeniu (nu doar onboarding).
10. [ ] Potriviri: filtru pe industrie (chips).
11. [ ] Notite: tag-uri simple (#client, #idee) + filtrare pe tag.
12. [ ] Setari: alegerea zilei de inceput (luni/duminica) pt. afisarea datelor.
13. [ ] Accesibilitate: trecere completa cu tastatura pe carduri (Enter/Space).
14. [ ] Pulse de retea reintrodus, dar compact si onest (1 rand).
15. [ ] Confirmare la stergere (task/nota/conexiune) — anti-accident.
16. [ ] „Ultima activitate” per conexiune in lista din Reteaua.
17. [ ] Dark mode: rafinare contraste pe carduri noi (task/meet).
18. [ ] Performanta: debounce la cautari.
19. [ ] Onboarding: pas optional „adauga prima notita/task”.
20. [ ] Documentatie: README scurt pt. app (cum se ruleaza, ce face, limitari).
