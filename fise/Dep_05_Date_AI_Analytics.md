# Firma IT (aplicatie mobila B2C) — Fise de post
## Departamentul 5. Date, AI si Analytics (11 persoane, 8 roluri)

---

## 5.1 Data / AI Lead

**Antet:** 1 persoana — rol de conducere a functiei de date / analytics.

**Misiunea rolului:** Defineste strategia de date si analytics a companiei si conduce echipa care transforma datele in decizii si in valoare pentru produs.

**De ce conteaza rolul:** Aplicatia mobila genereaza un volum mare de date comportamentale si tranzactionale. Fara strategie, ele devin gunoi scump. Cu strategie, devin avantaj competitiv si baza pentru AI.

**Rezumat:** Conduce Data Engineering, Data Science, Analytics si guvernanta datelor.

**Responsabilitati principale:**
- Strategia de date (ingestie, modelare, calitate, acces).
- Guvernanta datelor (lineage, calitate, privacy).
- Plan de analiza si BI.
- Coordonarea cu Head of AI pe ML / GenAI.
- Buget si plan de capacitate.
- Coaching Data Engineers, Scientists, Analysts.

**Activitati zilnice si saptamanale:** Sync cu Head of Engineering, CPO si Head of AI, review de proiecte, decizii pe arhitectura date, 1:1, alocare oameni.

**Provocari tipice:** Calitatea datelor, costurile de storage si compute, alinierea cu produs, conformitate (GDPR).

**Livrabile cheie:**
- Strategie de date documentata.
- Politica de guvernanta.
- Roadmap analytics.
- Raport trimestrial.

**Colaborare:** Head of Engineering, Head of AI, CPO, DPO, DevOps Lead, Security Lead.

**Instrumente si tehnologii:** Data warehouse (Snowflake / BigQuery / Redshift), dbt, Airflow, Looker / Tableau.

**Indicatori de succes / KPI:**
- Calitatea datelor (completitudine, prospetime).
- Adoptia dashboardurilor de catre echipe.
- Reducerea timpilor de obtinere a raspunsurilor.
- Initiative AI sustinute prin date.

**Cum arata succesul:** Deciziile in companie se iau pe date, echipele au incredere in cifre si AI-ul are date de calitate cu care lucreaza.

**Competente necesare:** Experienta in date la scara, leadership, gandire strategica, intelegere business.

**Parcurs de dezvoltare:** Head of Data, Chief Data Officer.

---

## 5.2 Data Engineer

**Antet:** 2 persoane — contributor individual.

**Misiunea rolului:** Construieste si mentine pipeline-urile de date (ETL / ELT) si infrastructura de date care alimenteaza analytics, BI si ML.

**De ce conteaza rolul:** Tot lantul de decizii si AI depinde de date care vin la timp si curate. Data Engineer-ul este coloana vertebrala a acestui lant.

**Rezumat:** Construieste pipeline-uri robuste de date.

**Responsabilitati principale:**
- Pipeline-uri ETL / ELT.
- Modelare date in warehouse (dimensionala, OBT).
- Calitatea datelor (testare, monitorizare).
- Performanta query / cost in warehouse.
- Suport pentru echipele de data si AI.

**Activitati zilnice si saptamanale:** Cod pipeline, debugging, code review, sync cu echipele care produc date, monitorizare freshness.

**Provocari tipice:** Date inconsistente la sursa, schimbari de schema, costuri de compute, latenta.

**Livrabile cheie:**
- Pipeline-uri noi sau imbunatatite.
- Modele in warehouse.
- Teste de calitate a datelor.

**Colaborare:** Data Scientists, ML Engineers, Analysts, Backend, DevOps, DBA.

**Instrumente si tehnologii:** Airflow / Dagster, dbt, Spark, Snowflake / BigQuery, Python, SQL.

**Indicatori de succes / KPI:**
- Freshness datelor.
- Numar incidente data quality.
- Cost compute pe pipeline.

**Cum arata succesul:** Datele sunt la timp, corecte si echipele au incredere in ele.

**Competente necesare:** SQL avansat, Python, modelare date, intelegere sisteme distribuite.

**Parcurs de dezvoltare:** Senior Data Engineer, Data Platform Lead, Architect Data.

---

## 5.3 Data Scientist

**Antet:** 2 persoane — contributor individual.

**Misiunea rolului:** Analizeaza date complexe si construieste modele predictive si analize care sprijina deciziile de produs si de business.

**De ce conteaza rolul:** Multe decizii importante au nevoie de evidence cantitativ. Data Scientist-ul aduce rigoarea statistica si modelele care explica si prezic comportamentul utilizatorilor.

**Rezumat:** Analize si modele care raspund la intrebari de business si de produs.

**Responsabilitati principale:**
- Analize ad-hoc pentru intrebari strategice.
- Modele predictive (retentie, churn, conversie).
- Experimente A/B (design, analiza, interpretare).
- Comunicare rezultate catre stakeholders.
- Documentare metodologie.

**Activitati zilnice si saptamanale:** Analize in notebooks, sync cu Product si Marketing, dezvoltare modele, prezentari, code review.

**Provocari tipice:** Date murdare, intrebari ambigue, presiune pentru raspunsuri rapide, interpretare statistica corecta.

**Livrabile cheie:**
- Analize si rapoarte clare.
- Modele predictive validate.
- Recomandari concrete catre business.

**Colaborare:** Product, Marketing, ML Engineers, Data Engineers, Analysts.

**Instrumente si tehnologii:** Python (pandas, scikit-learn, statsmodels), SQL, Jupyter, Looker.

**Indicatori de succes / KPI:**
- Impactul analizelor in decizii.
- Calitatea modelelor (validare).
- Adoptia recomandarilor.

**Cum arata succesul:** Echipele iau decizii mai bune pe baza muncii Data Scientist-ului, iar modelele sunt utile in productie.

**Competente necesare:** Statistica, ML clasic, comunicare, intelegere business.

**Parcurs de dezvoltare:** Senior Data Scientist, ML Engineer, Analytics Lead.

---

## 5.4 Machine Learning Engineer

**Antet:** 2 persoane — contributor individual.

**Misiunea rolului:** Duce modelele de ML in productie si construieste pipeline-urile care le antreneaza, le evalueaza si le servesc la scala.

**De ce conteaza rolul:** Un model in notebook nu ajuta utilizatorul. ML Engineer-ul transforma un experiment in serviciu fiabil si scalabil.

**Rezumat:** Productizeaza modelele de ML pentru aplicatia mobila.

**Responsabilitati principale:**
- Pipeline-uri de antrenare si evaluare.
- Servicii de inferenta (latenta scazuta, scalabile).
- Feature store si gestiune feature-uri.
- Monitorizare modele (drift, performanta).
- Coordonare cu Data Engineers si Data Scientists.
- Lucru cu MLOps pentru deploy.

**Activitati zilnice si saptamanale:** Cod, training jobs, debugging, sync cu DS, deploy modele, monitorizare metrici.

**Provocari tipice:** Drift de date, latenta in inferenta, cost de training, reproducibilitate.

**Livrabile cheie:**
- Modele in productie, monitorizate.
- Feature store curat.
- Documentatie pipeline.

**Colaborare:** Data Scientists, Data Engineers, MLOps, Backend, AI team.

**Instrumente si tehnologii:** Python, PyTorch / TensorFlow / scikit-learn, MLflow, Feast, Kubernetes, Triton / SageMaker.

**Indicatori de succes / KPI:**
- Latenta si throughput inferenta.
- Drift detection si reactie.
- Frecventa retraining.

**Cum arata succesul:** Modelele in productie merg stabil, sunt monitorizate si aduc valoare utilizatorului.

**Competente necesare:** ML, ingineria software, sisteme distribuite, observabilitate.

**Parcurs de dezvoltare:** Senior MLE, ML Architect, Head of AI Engineering.

---

## 5.5 MLOps Engineer

**Antet:** 1 persoana — contributor individual.

**Misiunea rolului:** Automatizeaza si standardizeaza ciclul de viata al modelelor (training, validare, deploy, monitorizare) pentru a face livrarea ML-ului sigura si repetabila.

**De ce conteaza rolul:** Fara MLOps, modelele se livreaza ad-hoc si esueaza tacit in productie. MLOps este DevOps-ul pentru ML.

**Rezumat:** DevOps specializat pe pipeline-uri ML.

**Responsabilitati principale:**
- Pipeline-uri standardizate training / eval / deploy.
- Versionare modele si date.
- Monitorizare model in productie.
- Suport pentru ML Engineers si Data Scientists.
- Optimizare cost de compute.

**Activitati zilnice si saptamanale:** Cod pe platforma ML, debugging job-uri, sync cu DevOps, suport pe deploy.

**Provocari tipice:** Cost GPU, reproducibilitate, fragmentare instrumente.

**Livrabile cheie:**
- Platforma ML / template-uri.
- Monitorizare model.
- Reducere cost training.

**Colaborare:** ML Engineers, Data Scientists, DevOps, Cloud Engineers, AI team.

**Instrumente si tehnologii:** Kubeflow / SageMaker / Vertex AI, MLflow, Airflow, Docker, Kubernetes, Terraform.

**Indicatori de succes / KPI:**
- Timp de la model la productie.
- Cost de compute pe model.
- Acoperire monitorizare modele.

**Cum arata succesul:** Livrarea ML-ului este sigura, rapida si previzibila.

**Competente necesare:** DevOps, ML basics, cloud, scripting, atentie la cost.

**Parcurs de dezvoltare:** Senior MLOps, ML Platform Lead, MLOps for AI.

---

## 5.6 Mobile Product Analyst

**Antet:** 1 persoana — contributor individual.

**Misiunea rolului:** Analizeaza retentia, onboardingul si conversia in aplicatia mobila si recomanda imbunatatiri concrete pentru echipele de produs si design.

**De ce conteaza rolul:** Aplicatia mobila B2C castiga sau pierde utilizatori la fiecare ecran. Mobile Product Analyst este vocea cantitativa care explica unde si de ce pierdem oameni.

**Rezumat:** Specialist analytics pe produs mobil.

**Responsabilitati principale:**
- Analize de palnie (instalare, activare, retentie).
- Analize de cohorte si retentie pe termen lung.
- Analiza experimente A/B pe ecrane mobile.
- Dashboards pentru PM-ii produsului mobil.
- Recomandari concrete catre Product si Design.

**Activitati zilnice si saptamanale:** Analize ad-hoc, dashboards, sync cu PM, prezentari pentru leadership, lucru cu Behavioral Science pe interpretari etice.

**Provocari tipice:** Date mobile incomplete (ITP, ATT), interpretarea diferentei intre engagement sanatos si compulsiv, multitudinea de fluxuri.

**Livrabile cheie:**
- Rapoarte de retentie / palnie.
- Analize de experimente.
- Dashboards pentru produs mobil.

**Colaborare:** Product Managers, Design, Mobile Devs, Data Scientists, Behavioral Science.

**Instrumente si tehnologii:** Amplitude / Mixpanel / GA4, SQL, Looker, Python, Firebase.

**Indicatori de succes / KPI:**
- Acuratetea analizelor (verificare).
- Numar decizii bazate pe analize.
- Impactul interventiilor in produs.

**Cum arata succesul:** Produsul mobil are decizii bazate pe date solide si valori de retentie cresc.

**Competente necesare:** Analytics mobile, SQL, statistica, comunicare cu PM, intelegere produs.

**Parcurs de dezvoltare:** Senior Product Analyst, Product Analytics Lead, Data Science.

---

## 5.7 Data Analyst

**Antet:** 1 persoana — contributor individual.

**Misiunea rolului:** Produce analize si rapoarte pentru decizii de business in marketing, sales, finance si operations.

**De ce conteaza rolul:** Echipele de business au nevoie de raspunsuri rapide si corecte. Data Analyst-ul transforma cerinte in cifre si insights.

**Rezumat:** Generalist analytics pentru zona non-produs.

**Responsabilitati principale:**
- Rapoarte si analize ad-hoc pentru business.
- Dashboards in Looker / Tableau.
- Documentare metrici.
- Suport pentru self-service.
- Lucru cu Data Engineers pe nevoi de date noi.

**Activitati zilnice si saptamanale:** Cereri de la business, sync cu stakeholders, scriere SQL, prezentari.

**Provocari tipice:** Cereri ambigue, metrici incoerente, time pressure.

**Livrabile cheie:**
- Rapoarte clare.
- Dashboards bine intretinute.
- Definitii standardizate.

**Colaborare:** Marketing, Sales, Finance, Operations, Data Engineers.

**Instrumente si tehnologii:** SQL, Looker / Tableau, Excel, Python (light), dbt.

**Indicatori de succes / KPI:**
- Adoptia dashboard-urilor.
- Timp de raspuns la cereri.
- Acuratete rapoartelor.

**Cum arata succesul:** Echipele de business iau decizii pe baza unor rapoarte clare si predictibile.

**Competente necesare:** SQL, intelegere business, comunicare clara, atentie la detalii.

**Parcurs de dezvoltare:** Senior Data Analyst, Analytics Lead, Data Scientist.

---

## 5.8 BI Developer

**Antet:** 1 persoana — contributor individual.

**Misiunea rolului:** Construieste sistemele de raportare si dashboard-urile care fac datele accesibile si utile in companie.

**De ce conteaza rolul:** Un raport bun economiseste ore de discutii. BI Developer-ul produce platforma comuna de raportare a companiei.

**Rezumat:** Specialist BI pe raportare si dashboards.

**Responsabilitati principale:**
- Dezvoltare dashboards complexe.
- Modelare semantica (LookML / metric layer).
- Optimizare performanta query.
- Standardizare metrici.
- Training echipe pe self-service.

**Activitati zilnice si saptamanale:** Cod LookML / SQL, modelare semantica, sync cu analysts si stakeholders, optimizare.

**Provocari tipice:** Metrici inconsistente, performanta dashboards, schimbari de cerinte.

**Livrabile cheie:**
- Dashboards in productie.
- Strat semantic mentenabil.
- Documentatie metrici.

**Colaborare:** Data Engineers, Analysts, business teams.

**Instrumente si tehnologii:** Looker / Tableau / Power BI, SQL, dbt, warehouse.

**Indicatori de succes / KPI:**
- Adoptia dashboards.
- Coerenta metrici.
- Performanta query.

**Cum arata succesul:** Compania are o limba comuna a cifrelor, sustinuta de dashboards rapide si corecte.

**Competente necesare:** Modelare semantica, SQL, BI tools, intelegere business.

**Parcurs de dezvoltare:** Senior BI Developer, Analytics Engineering Lead, Data Platform.
