# Firma IT (aplicatie mobila B2C) — Fise de post
## Departamentul 3. QA / Asigurarea calitatii (14 persoane, 6 roluri)

---

## 3.1 QA Lead

**Antet:** 1 persoana — rol de conducere a functiei QA.

**Misiunea rolului:** Defineste strategia de testare si standardele de calitate la nivel de companie, astfel incat fiecare release sa ajunga la utilizator stabil si previzibil.

**De ce conteaza rolul:** Aplicatia mobila B2C este judecata public: bug-urile devin recenzii negative. QA Lead-ul este garantia ca strategia de testare scaleaza odata cu produsul si ca echipa de calitate functioneaza ca un partener, nu ca un gatekeeper.

**Rezumat:** Conduce echipa QA, defineste strategia si raporteaza calitatea catre leadership.

**Responsabilitati principale:**
- Strategia de testare (piramida, manual vs. automat, mobile vs. backend).
- Standarde si politici de calitate.
- Coaching pentru QA Engineers si Testers.
- Raportarea calitatii catre Engineering si Product.
- Definirea criteriilor de release.
- Investitie in framework-uri si infrastructura de testare.
- Plan de capacitate QA.

**Activitati zilnice si saptamanale:** Sync cu Engineering Managers si Product, review de metrici de calitate, 1:1 cu echipa QA, audit pe procese, decizii pe testare release majore.

**Provocari tipice:** Presiunea pentru livrari rapide cu testare insuficienta, mentinerea unei suite automate stabile, gestionarea testarii pe foarte multe device-uri reale, evitarea ca QA sa devina blocaj.

**Livrabile cheie:**
- Plan de testare anual.
- Politici si template-uri.
- Raport trimestrial de calitate.

**Colaborare:** Engineering Managers, PMs, SRE, Mobile Lead, DevOps Lead.

**Instrumente si tehnologii:** TestRail / Xray, Jira, BrowserStack / Sauce Labs, Playwright, Appium, Postman, Jenkins / GitHub Actions.

**Indicatori de succes / KPI:**
- Escape defect rate (bugs ajunse in productie).
- Acoperire testare automata.
- Stabilitate suite (flakiness).
- Timp de cycle testing per release.
- Crash-free users in productie.

**Cum arata succesul:** Echipele livreaza rapid cu putine regresii, QA este partener al ingineriei iar utilizatorii nu mai observa probleme de baza.

**Competente necesare:** Experienta solida in QA, intelegere DevOps, leadership, comunicare cu stakeholder-i, gandire analitica.

**Parcurs de dezvoltare:** Director of Quality, Head of Engineering Quality, tranzitie spre Engineering Lead.

---

## 3.2 Senior QA Automation Engineer

**Antet:** 3 persoane — rol senior, contributor individual.

**Misiunea rolului:** Construieste si mentine framework-urile de testare automata, integreaza testele in CI/CD si asigura stabilitatea regresiei la scala.

**De ce conteaza rolul:** Fara automatizari stabile, fiecare release devine periculos. Seniorul de automatizare permite livrari rapide si sigure prin teste care chiar prind regresii.

**Rezumat:** Owner tehnic al automatizarii de testare, mentoreaza echipa.

**Responsabilitati principale:**
- Arhitectura framework-urilor de testare (UI, API, mobile).
- Integrare suite in CI/CD cu paralelizare.
- Reducerea flakiness-ului.
- Suport pentru echipele de dezvoltare in scrierea testelor.
- Mentorat QA Automation mid si junior.
- Acoperire pe scenarii critice pentru produs mobil (login, plata, onboarding).

**Activitati zilnice si saptamanale:** Cod pe framework, debugging teste instabile, review-uri PR, sync cu DevOps si dev teams, raport saptamanal stabilitate.

**Provocari tipice:** Teste instabile, schimbari frecvente UI, mediile de test divergente, lipsa de date de test realiste.

**Livrabile cheie:**
- Framework de testare imbunatatit.
- Suite automate noi pentru fluxuri critice.
- Rapoarte de flakiness si actiuni.

**Colaborare:** DevOps, dev teams, QA Lead, Mobile Engineers, SRE.

**Instrumente si tehnologii:** Playwright / Cypress / Selenium, Appium, REST Assured / Postman / Pact, JUnit / TestNG / pytest, GitHub Actions, BrowserStack.

**Indicatori de succes / KPI:**
- Procent flaky tests.
- Acoperire pe fluxuri critice.
- Timp executie suite.
- Reducere regresii in productie.

**Cum arata succesul:** Suita de teste prinde regresii reale, ruleaza rapid si stabil si sustine deploy-uri zilnice.

**Competente necesare:** Solid in cod si testare, intelegere CI/CD, gandire arhitecturala, comunicare clara.

**Parcurs de dezvoltare:** Test Architect, SDET Lead, tranzitie spre platform engineering.

---

## 3.3 QA Automation Engineer

**Antet:** 3 persoane — contributor individual (mid-level).

**Misiunea rolului:** Scrie si mentine teste automate noi pentru functionalitatile livrate de echipe, mentinand suite-urile sanatoase.

**De ce conteaza rolul:** Volumul de feature delivery cere o crestere constanta a acoperirii automate. Mid-level-ul de automatizare livreaza acest volum.

**Rezumat:** Scrie zilnic teste automate pe noile feature-uri si fixeaza pe cele instabile.

**Responsabilitati principale:**
- Implementare teste UI, API, mobile.
- Mentenanta suite existente.
- Fix de teste flaky.
- Lucru cu QA manual pentru scenarii.
- Code review reciproc.

**Activitati zilnice si saptamanale:** Scrierea testelor pentru sprint-ul curent, daily, sync cu QA manual, ticket-uri de flakiness, refinement.

**Provocari tipice:** Schimbari UI/UX dese, dependente externe, gestionarea datelor de test.

**Livrabile cheie:**
- Teste automate noi.
- Reducerea numarului de teste flaky.

**Colaborare:** Senior QA Automation, QA Manual, devs, PO.

**Instrumente si tehnologii:** Acelasi stack ca seniorul.

**Indicatori de succes / KPI:**
- Numar teste noi corecte.
- Stabilitatea testelor scrise.
- Bugs prinse de propria suita.

**Cum arata succesul:** Livreaza teste robuste pentru fiecare feature si scade rata de flakiness.

**Competente necesare:** Cunoastere de un limbaj (JS/TS, Python, Java), intelegere a testarii, atentie la detalii.

**Parcurs de dezvoltare:** Senior QA Automation, SDET, dev backend.

---

## 3.4 Manual QA Tester

**Antet:** 4 persoane — contributor individual.

**Misiunea rolului:** Testeaza manual produsul, in special pe fluxuri complexe, exploratorii si edge case, pentru a prinde probleme care scapa automatizarii.

**De ce conteaza rolul:** Aplicatia mobila are nuante (UX, gesture-uri, device-uri reale) pe care un test automat nu le surprinde. Testerii manuali aduc perspectiva utilizatorului real.

**Rezumat:** Testare manuala disciplinata si exploratorie pe device-uri reale.

**Responsabilitati principale:**
- Executare planuri de test manuale.
- Testare exploratorie pe device-uri reale.
- Reproducerea bug-urilor si descrierea clara.
- Testare regresie manuala pentru zone fara automatizare.
- Validare release candidates.
- Feedback de UX catre Design / Product.

**Activitati zilnice si saptamanale:** Sesiuni de testare, raportare bug-uri, retesting fix-uri, validare release, lucru pe checklists.

**Provocari tipice:** Cerinte schimbatoare, lipsa de timp inainte de release, multitudinea de device-uri.

**Livrabile cheie:**
- Rapoarte de testare pe release.
- Bug-uri detaliate cu pasi de reproducere.

**Colaborare:** QA Automation, dev, PO, Design.

**Instrumente si tehnologii:** TestRail / Xray, Jira, device farm, instrumente capture (Loom), BrowserStack.

**Indicatori de succes / KPI:**
- Bugs gasite pre-release.
- Calitatea rapoartelor de bug.
- Lipsa unor bug-uri majore in productie din zona testata manual.

**Cum arata succesul:** Bug-urile importante sunt prinse inainte de utilizator si calitatea release-ului este predictibila.

**Competente necesare:** Atentie la detalii, gandire critica, comunicare scrisa clara, intelegere a UX.

**Parcurs de dezvoltare:** QA Automation, Senior Manual QA, Quality Engineer Process.

---

## 3.5 Performance Test Engineer

**Antet:** 2 persoane — contributor individual specializat.

**Misiunea rolului:** Evalueaza performanta si scalabilitatea sistemelor sub trafic real si extrem, anticipand probleme inainte sa loveasca productia.

**De ce conteaza rolul:** Aplicatia mobila B2C are picuri (campanii, evenimente) cand poate primi un trafic mult mai mare decat de obicei. Testele de performanta previn caderi vizibile in masa.

**Rezumat:** Specialist in load, stress si soak testing, partener al SRE-ului.

**Responsabilitati principale:**
- Definire scenarii de incarcare realiste.
- Scriere si executare teste (load, stress, soak, spike).
- Analiza rezultatelor si bottleneck-urilor.
- Recomandari concrete catre dev / DevOps.
- Setare baseline-uri si monitorizare regresii performante.

**Activitati zilnice si saptamanale:** Pregatire teste, rulare in medii dedicate, analiza, raport, sync cu SRE si dev, automatizare in CI pe scenarii cheie.

**Provocari tipice:** Medii care nu reflecta productia, costuri ridicate de testare, interpretarea rezultatelor zgomotoase.

**Livrabile cheie:**
- Rapoarte de performanta.
- Plan de capacitate sustinut de date.
- Teste regulate in CI.

**Colaborare:** SRE, DevOps, backend, mobile, Architect, Product (pe evenimente).

**Instrumente si tehnologii:** k6, JMeter, Gatling, Locust, Grafana, Datadog, profiling tools.

**Indicatori de succes / KPI:**
- Capacitate sustinuta (rps, conc users).
- Latente p95/p99.
- Cost pe request.
- Anticiparea problemelor inainte de productie.

**Cum arata succesul:** Sistemul nu cade in picuri si echipa stie clar unde sunt limitele.

**Competente necesare:** Statistica, profiling, intelegere arhitectura backend, scriere scenarii realiste.

**Parcurs de dezvoltare:** Senior Performance Engineer, SRE, Performance Architect.

---

## 3.6 Quality Engineer Process

**Antet:** 1 persoana — contributor individual.

**Misiunea rolului:** Imbunatateste procesele de calitate la nivel de companie, defineste si urmareste metrici de calitate si conduce initiative cross-functionale.

**De ce conteaza rolul:** Calitatea nu apare doar din teste, ci din procese sanatoase (review, definitie de "done", proces de incidente, post-mortem). Quality Engineer Process face ca aceste procese sa fie reale, nu doar pe hartie.

**Rezumat:** Conduce procesele si metricile de calitate.

**Responsabilitati principale:**
- Definirea metricilor de calitate (escape rate, MTTR, defect density).
- Audit pe procese (review-uri, "definition of done", criteria de release).
- Initiative de imbunatatire (shift-left testing, contract testing).
- Suport in adoptia bunelor practici.
- Raportare catre QA Lead si Engineering Leadership.

**Activitati zilnice si saptamanale:** Analiza date de calitate, intalniri cu echipe, scriere de procese si template-uri, training scurt pentru echipe.

**Provocari tipice:** Rezistenta la schimbarea proceselor, lipsa de date curate, masurarea efectului real al schimbarilor.

**Livrabile cheie:**
- Dashboard de calitate.
- Documentatie de procese.
- Rapoarte de imbunatatire.

**Colaborare:** QA Lead, EMs, DevOps Lead, PMO, SRE.

**Instrumente si tehnologii:** Jira, BI tools (Looker / Metabase), Confluence, instrumente de proces.

**Indicatori de succes / KPI:**
- Tendinte pozitive ale defect rate, escape rate.
- Adoptia practicilor in echipe.
- Reducerea timpilor de cycle.

**Cum arata succesul:** Calitatea creste vizibil in timp si procesele sunt urmate pentru ca au sens, nu pentru ca sunt impuse.

**Competente necesare:** Analiza date, comunicare cu echipele, intelegere a procesului software, rabdare in schimbare.

**Parcurs de dezvoltare:** QA Lead, Engineering Process Manager.
