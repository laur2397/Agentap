# Firma IT (aplicatie mobila B2C) — Fise de post
## Departamentul 4. Securitate (10 persoane, 6 roluri)

---

## 4.1 CISO Deputy / Security Lead

**Antet:** 1 persoana — rol de conducere a functiei de securitate.

**Misiunea rolului:** Defineste si conduce strategia de securitate a companiei, gestioneaza riscurile majore si coordoneaza raspunsul la incidente critice.

**De ce conteaza rolul:** Aplicatia mobila B2C lucreaza cu date personale si potential date financiare. Un incident major poate distruge increderea utilizatorilor si poate genera amenzi mari. Security Lead-ul previne si pregateste compania pentru aceste situatii.

**Rezumat:** Conduce echipa de securitate si reprezinta securitatea fata de leadership.

**Responsabilitati principale:**
- Strategie de securitate aliniata cu standarde (ISO 27001, SOC 2).
- Coordonare raspuns la incidente (IR) majore.
- Gestionarea relatiei cu auditori si reglementatori.
- Conducerea echipelor de InfoSec, AppSec, PenTest, Compliance, SOC.
- Raport de risc catre leadership si board.
- Prioritizarea investitiilor in securitate.
- Cultura de securitate in companie.

**Activitati zilnice si saptamanale:** Sync cu Head of Engineering, DPO, Legal, leadership; revizuieste alerte / incidente in derulare, ia decizii pe escalari. Lunar revizuieste registrul de riscuri.

**Provocari tipice:** Echilibrul intre securitate si viteza de livrare, atacuri sofisticate, conformitate cu reglementari multiple, buget limitat.

**Livrabile cheie:**
- Strategie de securitate anuala.
- Registru de riscuri actualizat.
- Plan de raspuns la incidente.
- Rapoarte trimestriale de securitate.

**Colaborare:** Head of Engineering, DevOps Lead, DPO, Legal, Head of Product, HR, IT intern.

**Instrumente si tehnologii:** SIEM, EDR, vulnerability management, GRC tools, dashboards de risc.

**Indicatori de succes / KPI:**
- Numar incidente majore.
- Timp de detectie si raspuns.
- Status audituri si certificari.
- Reducerea findings critice in timp.

**Cum arata succesul:** Compania nu sufera incidente majore, este conforma cu cerintele si securitatea nu blocheaza inutil livrarea.

**Competente necesare:** Experienta solida in securitate cibernetica, leadership, comunicare cu non-tehnic, gandire de risc.

**Parcurs de dezvoltare:** CISO al companiei, CISO la o organizatie mai mare.

---

## 4.2 Information Security Specialist

**Antet:** 2 persoane — contributor individual.

**Misiunea rolului:** Defineste si mentine politicile de securitate ale informatiei, gestioneaza accesele si urmareste riscurile operationale.

**De ce conteaza rolul:** Multe incidente vin din politici slabe sau accese gresite. Acest rol previne aceste probleme zilnice prin politici clare si controale.

**Rezumat:** Owner politici, accese si registre de risc.

**Responsabilitati principale:**
- Definirea si revizuirea politicilor (parole, MFA, BYOD, data handling).
- Gestionarea schemei de accese (IAM, RBAC, ABAC).
- Evaluare riscuri pe sisteme noi.
- Suport pentru echipele de dezvoltare in alegerea solutiilor.
- Educatie de securitate pentru angajati.

**Activitati zilnice si saptamanale:** Revizuiri de cereri de acces, audit accesuri, evaluare riscuri, lucru cu HR si IT pe onboarding / offboarding, sesiuni de educatie.

**Provocari tipice:** Drepturi excesive in timp, politici care raman pe hartie, lipsa de date pentru evaluarea riscurilor.

**Livrabile cheie:**
- Politici de securitate actualizate.
- Registru de acces revizuit.
- Rapoarte de risc pentru sisteme noi.

**Colaborare:** IT intern, HR, DevOps, Compliance, DPO.

**Instrumente si tehnologii:** SSO, IAM, GRC tools, Okta / Azure AD, instrumente de audit acces.

**Indicatori de succes / KPI:**
- Procent accese revizuite la timp.
- Numar conturi orfane / privilegii excesive.
- Aderenta la politici.

**Cum arata succesul:** Politicile sunt clare, acceptate si respectate, iar accesul este "least privilege" cu adevarat.

**Competente necesare:** Cunoastere standarde (ISO, NIST), IAM, comunicare cu non-tehnic, gandire de risc.

**Parcurs de dezvoltare:** Senior InfoSec Specialist, Security Lead, GRC Manager.

---

## 4.3 Application Security Engineer

**Antet:** 2 persoane — contributor individual specializat.

**Misiunea rolului:** Securizeaza aplicatiile prin design securizat, analiza codului, scanari in CI/CD si educatie a echipelor de dezvoltare.

**De ce conteaza rolul:** Cele mai costisitoare bug-uri de securitate sunt cele care ajung in productie. AppSec previne aceste bug-uri inca din design si din pipeline.

**Rezumat:** Partener al ingineriei pentru a livra cod sigur.

**Responsabilitati principale:**
- Threat modeling pentru feature-uri noi.
- Analiza statica si dinamica (SAST, DAST, SCA).
- Securizare CI/CD (scanare, secrete, dependinte).
- Review-uri de cod pe arii sensibile.
- Suport pentru dev teams pe librarii sigure.
- Educatie (training, pair programming, ghiduri).
- Triere si gestionare findings.

**Activitati zilnice si saptamanale:** Threat modeling sessions, review-uri PR, configurare scanere, training scurt, suport pe ticket-uri de securitate.

**Provocari tipice:** Volum mare de findings, fals-pozitive, lipsa de timp a dev-ilor, librarii vulnerabile in continuu.

**Livrabile cheie:**
- Threat models documentate.
- Scanere integrate in CI/CD.
- Reducerea findings critice.

**Colaborare:** Dev teams, Architect, DevOps, Tech Leads, QA.

**Instrumente si tehnologii:** Snyk / Semgrep / SonarQube, OWASP ZAP, GitHub security, Dependabot, secret scanners.

**Indicatori de succes / KPI:**
- Numar findings critice in productie.
- Timp de remediere.
- Acoperire SAST / DAST / SCA.
- Adoptia bunelor practici in echipe.

**Cum arata succesul:** Cod nou apare sigur "by default", echipele inteleg riscurile si stiu sa le evite.

**Competente necesare:** Cunoastere OWASP, criptografie de baza, cod in mai multe limbaje, pedagogie.

**Parcurs de dezvoltare:** Senior AppSec Engineer, AppSec Lead, Security Architect.

---

## 4.4 Penetration Tester

**Antet:** 2 persoane — contributor individual specializat.

**Misiunea rolului:** Identifica activ vulnerabilitati prin teste de penetrare controlate, simuland atacatori reali pentru a anticipa breach-urile.

**De ce conteaza rolul:** Cele mai bune scanere automate nu prind tot. PenTester-ul gandeste ca un atacator si gaseste probleme reale, exploatabile, intr-un mediu controlat.

**Rezumat:** Atacator etic care testeaza limitele apararii.

**Responsabilitati principale:**
- Teste de penetrare web, mobile, API, infrastructura.
- Red team exercises (limitate).
- Verificare social engineering si phishing-like.
- Rapoarte detaliate cu exploituri si remedieri.
- Suport pentru AppSec in prioritizare.
- Re-testare dupa fix-uri.

**Activitati zilnice si saptamanale:** Planificare campanii de testare, executie controlata, scriere rapoarte, sync cu AppSec si DevOps, debrief cu echipele afectate.

**Provocari tipice:** Lipsa de medii safe, presiunea de a nu afecta utilizatorii reali, cerintele cu prioritizare slaba a remedierii.

**Livrabile cheie:**
- Rapoarte de pen-test cu exploit si remediere.
- Verificari post-fix.
- Recomandari arhitecturale derivate din findings.

**Colaborare:** AppSec, DevOps, Architect, Security Lead, dev teams.

**Instrumente si tehnologii:** Burp Suite, Metasploit, Nmap, Frida (mobile), MobSF, Wireshark, instrumente proprii.

**Indicatori de succes / KPI:**
- Numar exploituri reproductibile gasite.
- Timp de remediere.
- Reducerea regresiilor de securitate.

**Cum arata succesul:** Atacurile reale gasesc tot mai putine vulnerabilitati pentru ca PenTesterul le-a gasit primul.

**Competente necesare:** Mentalitate ofensiva, cunoastere protocoale, cod si retea, etica profesionala, scriere clara.

**Parcurs de dezvoltare:** Senior PenTester, Red Team Lead, Security Architect.

---

## 4.5 Compliance & Audit Specialist

**Antet:** 2 persoane — contributor individual.

**Misiunea rolului:** Asigura conformitatea cu standarde si reglementari (ISO 27001, SOC 2, GDPR) si conduce auditurile externe si interne.

**De ce conteaza rolul:** Pentru o aplicatie B2C, conformitatea este un prerequisite pentru a opera pe piete reglementate. Specialistul mentine compania pregatita continuu, nu doar inainte de audit.

**Rezumat:** Owner de conformitate si pregatire pentru audituri.

**Responsabilitati principale:**
- Mapare cerinte ISO / SOC 2 / GDPR pe controale.
- Audituri interne periodice.
- Pregatirea si insotirea auditurilor externe.
- Gestionarea evidentelor (evidence collection).
- Plan de actiuni de remediere.
- Lucru cu DPO pe GDPR (DPIA, ROPA).

**Activitati zilnice si saptamanale:** Lucru pe controale, colectare dovezi, sync cu echipele care detin controale, intalniri cu auditori, raportare.

**Provocari tipice:** Volumul mare de dovezi, schimbari de reglementari, dependenta de alte echipe, evitarea muncii ultime-zile inainte de audit.

**Livrabile cheie:**
- Matrice de controale actualizata.
- Rapoarte audit intern.
- Pachete de evidence pentru auditori.

**Colaborare:** Security Lead, DPO, Legal, IT intern, DevOps, HR, Finance.

**Instrumente si tehnologii:** GRC platforms (Vanta / Drata / Tugboat / OneTrust), Jira, Confluence.

**Indicatori de succes / KPI:**
- Rezultat audituri (numar findings).
- Procent controale automatizate.
- Timp de pregatire pentru audit.

**Cum arata succesul:** Auditul devine o formalitate, nu o criza. Conformitatea este continua.

**Competente necesare:** Atentie la detalii, intelegere de standarde, rabdare in colectarea evidentelor, comunicare diplomatica.

**Parcurs de dezvoltare:** Senior Compliance, GRC Manager, Head of Compliance.

---

## 4.6 Security Analyst (SOC)

**Antet:** 1 persoana — contributor individual.

**Misiunea rolului:** Monitorizeaza alertele de securitate, investigheaza activitati suspecte si declanseaza raspunsul la incidente cand este nevoie.

**De ce conteaza rolul:** Multe incidente sunt observabile in loguri si telemetrie. SOC-ul transforma aceste semnale in actiuni rapide, oprind atacatori inainte sa faca daune.

**Rezumat:** Ochi si urechi ale securitatii in operatii zilnice.

**Responsabilitati principale:**
- Monitorizare alerte SIEM, EDR, cloud security.
- Triere alerte (false pozitive / adevarate).
- Investigatii initiale si escaladari.
- Documentare incidente.
- Tuning alerte cu echipele de InfoSec si AppSec.
- Suport in IR.

**Activitati zilnice si saptamanale:** Monitorizare continua (in regim de zi sau ture), lucru pe ticket-uri, raport zilnic / saptamanal, sync cu Security Lead.

**Provocari tipice:** Alert fatigue, lipsa de context pe alerte, presiunea de a rezolva rapid.

**Livrabile cheie:**
- Raport zilnic de alerte tratate.
- Incidente documentate.
- Sugestii de tuning.

**Colaborare:** Security Lead, AppSec, InfoSec, DevOps, SRE.

**Instrumente si tehnologii:** SIEM (Splunk / ELK / Wazuh), EDR (CrowdStrike / SentinelOne), cloud security tools, ticketing.

**Indicatori de succes / KPI:**
- Timp mediu de triere.
- Rata fals-pozitive.
- Numar incidente confirmate inainte de impact.

**Cum arata succesul:** Alertele sunt tratate la timp, atacatorii sunt opriti devreme si echipele de dev primesc semnale utile.

**Competente necesare:** Cunoastere de retea, sisteme, atacuri comune, atentie, rabdare, scriere precisa.

**Parcurs de dezvoltare:** Senior SOC Analyst, Incident Response Specialist, Threat Hunter.
