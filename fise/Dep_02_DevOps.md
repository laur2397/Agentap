# Firma IT (aplicatie mobila B2C) — Fise de post
## Departamentul 2. DevOps / Infrastructure / Cloud (13 persoane, 7 roluri)

---

## 2.1 DevOps Lead

**Antet:** 1 persoana — rol de conducere a functiei DevOps.

**Misiunea rolului:** Defineste strategia de CI/CD, infrastructura cloud si fiabilitate operationala, astfel incat echipele sa livreze rapid, in siguranta si la cost controlat.

**De ce conteaza rolul:** Viteza de livrare a unei firme moderne depinde direct de calitatea pipeline-urilor si a infrastructurii. DevOps Lead-ul controleaza costul cloud, timpul de la commit la productie si raspunsul la incidente majore.

**Rezumat:** Conduce echipa DevOps, SRE si infrastructura, fiind punctul de escalare pe incidente.

**Responsabilitati principale:**
- Strategie CI/CD si infrastructura ca cod.
- Bugetare si optimizare cloud (FinOps de baza).
- Politici de release si rollback.
- Coordonarea raspunsului la incidente majore.
- Standarde de observabilitate.
- Plan de capacitate si de continuitate.
- Coaching pentru DevOps Engineers, SRE, Cloud Engineers.

**Activitati zilnice si saptamanale:** Sincronizari cu Head of Engineering, Security si Finance pe cost cloud. Saptamanal review de incidente, schimbari riscante, capacitate. Lunar revizuieste KPI operationali si planuri de hardening.

**Provocari tipice:** Cost cloud in crestere, schimbari frecvente in produs, downtime in cascada, recrutare DevOps senior.

**Livrabile cheie:**
- Strategie DevOps documentata.
- Plan FinOps pentru cloud.
- Politici de release / rollback / oncall.
- Raport trimestrial de fiabilitate si cost.

**Colaborare:** Head of Engineering, SRE, Security Lead, DBA, Architect, Finance, Internal IT.

**Instrumente si tehnologii:** Terraform / Pulumi, Kubernetes, GitHub Actions / GitLab CI / ArgoCD, Datadog / Grafana, AWS / GCP / Azure, PagerDuty / Opsgenie.

**Indicatori de succes / KPI:**
- Lead time for changes.
- Deployment frequency.
- Change failure rate.
- MTTR (timp mediu de recuperare).
- Cost cloud per utilizator activ.

**Cum arata succesul:** Echipele livreaza de zeci de ori pe zi cu risc redus, incidentele se rezolva rapid si costurile cloud cresc subliniar fata de utilizatori.

**Competente necesare:** Experienta solida in operatii cloud, gandire sistemica, leadership, intelegere financiara.

**Parcurs de dezvoltare:** Head of Platform / Head of Infrastructure, CTO al unei firme mai mici.

---

## 2.2 DevOps Engineer

**Antet:** 3 persoane — contributor individual.

**Misiunea rolului:** Construieste si mentine pipeline-uri CI/CD, infrastructura ca cod si automatizari care permit echipelor sa livreze rapid si in siguranta.

**De ce conteaza rolul:** Fara automatizari si pipeline-uri solide, ingineria livreaza incet si cu risc mare. DevOps Engineer-ul este pilonul vitezei si stabilitatii zilnice.

**Rezumat:** Build si mentenanta a sistemului de livrare si a infrastructurii.

**Responsabilitati principale:**
- Pipeline-uri CI/CD per serviciu.
- IaC pentru medii (dev, staging, prod).
- Automatizare deploys (canary, blue-green).
- Monitorizare si alerte de baza.
- Self-service pentru ingineri (template-uri, scripts).
- Suport in incidente.

**Activitati zilnice si saptamanale:** Lucru pe ticket-uri de platforma, debugging pipeline-uri, code review, suport ingineri, participare la incidente.

**Provocari tipice:** Pipeline-uri instabile, diferente intre medii, dependinte de retea, gestiunea secretelor.

**Livrabile cheie:**
- Pipeline-uri CI/CD noi sau imbunatatite.
- Module IaC reutilizabile.
- Documentatie de utilizare pentru echipe.

**Colaborare:** Backend, mobile, SRE, Security, Architect.

**Instrumente si tehnologii:** GitHub Actions / GitLab CI, ArgoCD / Flux, Terraform, Helm, Docker, Kubernetes, Bash / Python.

**Indicatori de succes / KPI:**
- Timp mediu de build.
- Stabilitate pipeline.
- Numar deploy-uri reusite.
- Cereri de suport rezolvate.

**Cum arata succesul:** Echipele deploy-eaza zilnic fara batai de cap, mediile sunt consistente si self-service-ul functioneaza.

**Competente necesare:** Linux, retea, scripting, intelegere container-e, atentie la securitate.

**Parcurs de dezvoltare:** Senior DevOps, Platform Engineer, SRE, DevOps Lead.

---

## 2.3 Site Reliability Engineer (SRE)

**Antet:** 3 persoane — contributor individual, focus pe fiabilitate.

**Misiunea rolului:** Asigura ca platforma respecta obiectivele de fiabilitate (SLI / SLO), conduce raspunsul la incidente si invata sistemul din fiecare cadere.

**De ce conteaza rolul:** Fiabilitatea este un atribut de produs, nu un accident. SRE protejeaza utilizatorul de downtime si afla cauzele reale ale problemelor.

**Rezumat:** Gardian al fiabilitatii, conduce incident response si post-mortems.

**Responsabilitati principale:**
- Definire SLI, SLO, error budget.
- Setare alerte care nu fac zgomot.
- On-call si gestiune incidente.
- Post-mortem fara invinovatire.
- Capacity planning si chaos engineering light.
- Automatizari operationale (toil reduction).

**Activitati zilnice si saptamanale:** On-call rotativ, analiza alerte, lucru pe imbunatatiri de fiabilitate, post-mortems, sync cu DevOps si echipe.

**Provocari tipice:** Alert fatigue, sisteme complexe, lipsa de timp pentru lucru pe termen lung, presiunea de release rapid.

**Livrabile cheie:**
- SLO documentate pe servicii.
- Post-mortems publicate.
- Action items implementati.
- Rapoarte de fiabilitate.

**Colaborare:** DevOps, backend, mobile, Security, Architect, Product (pe cost-uri de fiabilitate).

**Instrumente si tehnologii:** Prometheus / Grafana, Datadog, OpenTelemetry, PagerDuty, Kubernetes, Terraform.

**Indicatori de succes / KPI:**
- Disponibilitate fata de SLO.
- MTTR.
- Numar incidente repetate (regresii).
- Reducere de toil.

**Cum arata succesul:** Serviciile critice isi respecta SLO-urile, incidentele se rezolva rapid si sistemul invata din ele.

**Competente necesare:** Sisteme distribuite, debugging avansat, statistica de baza, scriere clara, calm in incidente.

**Parcurs de dezvoltare:** Senior SRE, SRE Lead, Architect, Head of Platform.

---

## 2.4 Cloud Engineer

**Antet:** 3 persoane — contributor individual, focus pe cloud.

**Misiunea rolului:** Proiecteaza si optimizeaza infrastructura cloud (AWS / Azure / GCP), pe dimensiuni de cost, performanta, securitate si scalabilitate.

**De ce conteaza rolul:** Cloud-ul este coloana vertebrala a aplicatiei mobile. Cloud Engineer-ul tine costurile sub control si infrastructura aliniata cu nevoile reale.

**Rezumat:** Specialist cloud, partener al DevOps si Security.

**Responsabilitati principale:**
- Design retele cloud (VPC, subneturi, peering).
- Optimizare cost (rezervari, savings plans, dimensionare).
- Securitate cloud (IAM, KMS, networking).
- Migrari intre regiuni / conturi.
- Suport pentru echipele de date / AI cu resurse specializate.

**Activitati zilnice si saptamanale:** Lucru pe ticket-uri cloud, audituri de cost si securitate, design de noi medii, sync cu DevOps si Security.

**Provocari tipice:** Cost necontrolat, configuratii istorice, complexitate IAM, schimbari ale furnizorilor cloud.

**Livrabile cheie:**
- Module IaC pentru cloud.
- Rapoarte si plan de reducere cost.
- Audit security cloud.

**Colaborare:** DevOps, SRE, Security, DBA, Data, Finance.

**Instrumente si tehnologii:** AWS / Azure / GCP, Terraform, CloudFormation, IAM, Cost Explorer, KMS, CloudWatch.

**Indicatori de succes / KPI:**
- Cost cloud per utilizator activ.
- Numar findings de securitate cloud.
- Timp de provisioning a unui mediu nou.

**Cum arata succesul:** Cloud-ul este sigur, eficient si predictibil ca pret.

**Competente necesare:** Adanca cunoastere cloud, retea, securitate, IaC, atentie la cost.

**Parcurs de dezvoltare:** Senior Cloud Engineer, Cloud Architect, Head of Cloud / Platform.

---

## 2.5 System Administrator

**Antet:** 1 persoana — contributor individual.

**Misiunea rolului:** Administreaza servere, accese, backup-uri si patch-uri pentru sistemele care nu intra direct in produs (medii interne, instrumente, integrari).

**De ce conteaza rolul:** Multe sisteme suport (CI runners auto-hostate, build farms, instrumente interne) au nevoie de administrare clasica. Fara SysAdmin, ele degradeaza rapid.

**Rezumat:** Owner operational al sistemelor adiacente platformei.

**Responsabilitati principale:**
- Patch management pentru servere.
- Backup-uri si testarea restaurarii.
- Gestiunea acceselor sistem (ssh, sudo).
- Suport pentru DevOps pe sisteme legacy.
- Monitorizare de baza, automatizari de mentenanta.

**Activitati zilnice si saptamanale:** Verificare patch-uri, jurnale, backup-uri, ticket-uri interne, mentenanta planificata in afara orelor de varf.

**Provocari tipice:** Sisteme mostenite, ferestre limitate de mentenanta, presiunea de a evita downtime.

**Livrabile cheie:**
- Plan de patching documentat.
- Backup-uri verificate.
- Runbook-uri operationale.

**Colaborare:** DevOps, Cloud Engineer, Security, Internal IT.

**Instrumente si tehnologii:** Linux, Bash / Ansible, monitorizare clasica (Nagios / Zabbix), instrumente backup, MFA / SSO.

**Indicatori de succes / KPI:**
- Compliance patching.
- Reusita restaurarilor de test.
- Numar incidente cauzate de mentenanta.

**Cum arata succesul:** Sistemele suport nu cad, backup-urile functioneaza si vulnerabilitatile sunt inchise la timp.

**Competente necesare:** Solid Linux, retea de baza, scripting, disciplina operationala.

**Parcurs de dezvoltare:** DevOps Engineer, Cloud Engineer, Internal IT Manager.

---

## 2.6 Network Engineer

**Antet:** 1 persoana — contributor individual.

**Misiunea rolului:** Proiecteaza si mentine topologia de retea (cloud si birou), VPN-uri si politici de securitate de retea care sustin atat produsul, cat si activitatea interna.

**De ce conteaza rolul:** Reteaua este invizibila cand merge si critica atunci cand cade. Network Engineer asigura conectivitate sigura, stabila si conforma.

**Rezumat:** Specialist retea pentru cloud si birou.

**Responsabilitati principale:**
- Design retea cloud (VPC, segmentare, peering).
- VPN-uri pentru angajati si parteneri.
- Firewall-uri, ACL-uri, politici de securitate retea.
- Debugging probleme de retea.
- Lucru cu furnizori ISP / DDoS protection / CDN.

**Activitati zilnice si saptamanale:** Schimbari de retea cu schimburi controlate, monitorizare, lucru cu DevOps si Security, suport pentru Internal IT pe partea de birou.

**Provocari tipice:** Topologii complexe, atacuri DDoS, instabilitate ISP, schimbari care implica downtime.

**Livrabile cheie:**
- Documentatie topologie retea.
- Politici de retea actualizate.
- Plan de raspuns la incidente de retea.

**Colaborare:** DevOps, Cloud, Security, Internal IT, Architect.

**Instrumente si tehnologii:** AWS VPC / Transit Gateway, Cloudflare / Akamai, IPSec / Wireguard VPN, instrumente de captura trafic.

**Indicatori de succes / KPI:**
- Disponibilitate retea.
- Numar incidente DDoS / mitigate.
- Latenta intre regiuni.

**Cum arata succesul:** Reteaua este stabila, sigura si bine documentata.

**Competente necesare:** Cunoastere temeinica TCP/IP, BGP, DNS, securitate retea, gandire detasata in incidente.

**Parcurs de dezvoltare:** Senior Network Engineer, Network Architect, Cloud Architect.

---

## 2.7 Database Administrator (DBA)

**Antet:** 1 persoana — contributor individual.

**Misiunea rolului:** Asigura performanta, disponibilitatea si securitatea bazelor de date critice pentru aplicatia mobila si pentru raportari.

**De ce conteaza rolul:** Bazele de date sunt centrul de gravitatie al datelor utilizatorilor. Performanta interogarilor, backup-urile si replicarea hotarasc cat de rapida si rezistenta este aplicatia.

**Rezumat:** Expert pe baze de date, ghideaza echipele in modelare si optimizare.

**Responsabilitati principale:**
- Setarea si tuning-ul bazelor de date.
- Backup-uri, restaurari, replicare.
- Optimizare interogari si indecsi.
- Suport pentru ingineri pe modelare si performanta.
- Monitorizare baze de date si planificare capacitate.
- Politici de retentie si securitate a datelor.

**Activitati zilnice si saptamanale:** Analiza query-uri lente, suport pentru echipe, planificare migrari, verificari backup, sync cu Security pe acces.

**Provocari tipice:** Cresterea volumului de date, migrari fara downtime, queries scrise neoptim, presiune pe cost storage.

**Livrabile cheie:**
- Plan de backup si recovery testat.
- Plan de capacitate.
- Recomandari de modelare si indexare.

**Colaborare:** Backend, Data, DevOps, Security.

**Instrumente si tehnologii:** PostgreSQL / MySQL / MongoDB, Redis, instrumente cloud manageriate (RDS / Cloud SQL), pgbench, EXPLAIN, observabilitate dedicata.

**Indicatori de succes / KPI:**
- Latenta query-uri critice.
- RPO / RTO realizate.
- Numar incidente legate de BD.
- Cost storage per utilizator activ.

**Cum arata succesul:** Bazele de date sunt rapide, sigure si scalabile, iar incidentele se rezolva rapid.

**Competente necesare:** Expertiza in unul sau mai multe RDBMS, intelegere a sistemelor de fisiere si I/O, tuning, securitate.

**Parcurs de dezvoltare:** Senior DBA, Data Platform Engineer, Database Architect.
