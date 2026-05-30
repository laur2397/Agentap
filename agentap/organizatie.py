"""Structura organizationala - firma IT (aplicatie mobila).

Date: 18 departamente, roluri, numar de angajati si descrieri.
Format: ORGANIZATIE = { departament: { "intro": str, "roluri": [ (rol, nr, descriere), ... ] } }

Acest modul este *pur* (fara dependente de API), deci poate fi folosit pentru
inspectia structurii fara o cheie ANTHROPIC_API_KEY.
"""

from __future__ import annotations

import re

ORGANIZATIE = {
    "1. Engineering / Dezvoltare software": {
        "intro": "Nucleul tehnic si cel mai mare departament al firmei. Organizat pe mai multe echipe (squad-uri) cross-functionale, fiecare responsabila de o zona de produs. Construieste efectiv aplicatiile web, mobile si serviciile backend.",
        "roluri": [
            ("Head of Engineering / VP Eng", 1, "Conduce intreaga organizatie tehnica si standardele de inginerie."),
            ("Engineering Manager", 3, "Coordoneaza cate un squad: prioritizare, livrare si dezvoltarea oamenilor."),
            ("Software Architect", 2, "Defineste arhitectura de ansamblu si deciziile tehnice de fond."),
            ("Tech Lead", 3, "Conduce tehnic fiecare squad si valideaza solutiile de implementare."),
            ("Senior Backend Developer", 5, "Dezvolta logica de server, baze de date, API-uri si servicii critice."),
            ("Backend Developer", 4, "Implementeaza functionalitati pe partea de server."),
            ("Senior Frontend Developer", 4, "Construieste interfetele web si optimizeaza performanta in browser."),
            ("Frontend Developer", 3, "Implementeaza componente UI si integreaza cu backend-ul."),
            ("Senior Mobile Developer", 3, "Conduce dezvoltarea aplicatiilor iOS si Android."),
            ("Mobile Developer", 4, "Implementeaza functionalitati in aplicatiile mobile native."),
        ],
    },
    "2. DevOps / Infrastructure / Cloud": {
        "intro": "Asigura livrarea continua, stabilitatea si scalarea sistemelor. Creste proportional cu Engineering-ul pentru a nu deveni blocaj.",
        "roluri": [
            ("DevOps Lead", 1, "Defineste strategia de infrastructura si standardele de deployment."),
            ("DevOps Engineer", 3, "Construieste si mentine pipeline-urile CI/CD si automatizarile."),
            ("Site Reliability Engineer (SRE)", 3, "Monitorizeaza, asigura uptime-ul si raspunde la incidente."),
            ("Cloud Engineer", 3, "Gestioneaza resursele cloud (AWS/Azure/GCP) si costurile aferente."),
            ("System Administrator", 1, "Administreaza serverele, accesele si configuratiile de sistem."),
            ("Network Engineer", 1, "Proiecteaza si securizeaza reteaua si conectivitatea."),
            ("Database Administrator (DBA)", 1, "Optimizeaza, securizeaza si face backup la bazele de date."),
        ],
    },
    "3. QA / Asigurarea calitatii": {
        "intro": "Garanteaza ca produsul functioneaza corect. Dimensionat la circa un tester la 3-4 developeri, deci creste odata cu Engineering-ul.",
        "roluri": [
            ("QA Lead", 1, "Defineste strategia de testare si standardele de calitate."),
            ("Senior QA Automation Engineer", 3, "Construieste cadrul de testare automata pentru regresie si CI."),
            ("QA Automation Engineer", 3, "Scrie si mentine teste automate pentru functionalitati noi."),
            ("Manual QA Tester", 4, "Testeaza manual scenarii complexe, exploratorii si de edge-case."),
            ("Performance Test Engineer", 2, "Verifica viteza, scalabilitatea si comportamentul sub incarcare."),
            ("Quality Engineer (Process)", 1, "Imbunatateste procesele de calitate de-a lungul ciclului de dezvoltare."),
        ],
    },
    "4. Securitate": {
        "intro": "Protejeaza produsul, datele si infrastructura impotriva amenintarilor.",
        "roluri": [
            ("CISO Deputy / Security Lead", 1, "Conduce strategia de securitate si raspunde la incidente majore."),
            ("Information Security Specialist", 2, "Gestioneaza politicile, accesele si riscurile de securitate."),
            ("Application Security Engineer", 2, "Verifica codul si arhitectura pentru vulnerabilitati de aplicatie."),
            ("Penetration Tester", 2, "Simuleaza atacuri pentru a descoperi puncte slabe inainte ca altii sa o faca."),
            ("Compliance & Audit Specialist", 2, "Asigura conformitatea cu ISO, SOC2, GDPR si pregateste auditurile."),
            ("Security Analyst (SOC)", 1, "Monitorizeaza alertele si investigheaza activitatea suspecta."),
        ],
    },
    "5. Date, AI si Analytics": {
        "intro": "Transforma datele in informatii utile si alimenteaza functionalitatile inteligente. Include analiza specifica de produs mobil (retentie, onboarding, notificari).",
        "roluri": [
            ("Data / AI Lead", 1, "Coordoneaza strategia de date si initiativele de AI."),
            ("Data Engineer", 2, "Construieste pipeline-urile de date si infrastructura de procesare."),
            ("Data Scientist", 2, "Analizeaza datele si construieste modele predictive."),
            ("Machine Learning Engineer", 2, "Pune modelele in productie si le optimizeaza la scara."),
            ("MLOps Engineer", 1, "Automatizeaza ciclul de viata al modelelor de ML."),
            ("Mobile Product Analyst", 1, "Analizeaza retentia, palnia de onboarding si comportamentul in aplicatia mobila."),
            ("Data Analyst", 1, "Produce rapoarte si analize pentru deciziile de business."),
            ("BI Developer", 1, "Construieste dashboard-uri si sisteme de raportare."),
        ],
    },
    "5b. Artificial Intelligence (AI)": {
        "intro": "Departament dedicat construirii si integrarii functionalitatilor inteligente in aplicatie: de la cercetare proprie si modele antrenate intern, pana la AI generativ si integrarea cu modele externe. Lucreaza strans cu Engineering, Produs si Behavioral Science pentru ca functiile AI sa fie utile si responsabile.",
        "roluri": [
            ("Head of AI", 1, "Conduce strategia AI a firmei si prioritizeaza initiativele cu impact in produs."),
            ("AI Research Scientist", 2, "Cerceteaza si antreneaza modele proprii adaptate nevoilor specifice ale produsului."),
            ("Senior ML Engineer", 2, "Construieste si optimizeaza modelele pentru recomandari, personalizare si predictie."),
            ("ML Engineer", 2, "Implementeaza si intretine functionalitatile de invatare automata in aplicatie."),
            ("Generative AI Engineer", 2, "Dezvolta functiile generative (text, imagine, voce) integrate in app."),
            ("LLM / Integration Engineer", 1, "Integreaza si orchestreaza modele externe (ex. furnizori terti) si gestioneaza prompt-urile."),
            ("Conversational AI Designer", 1, "Proiecteaza experienta si fluxurile chatbot-ului si ale asistentului din aplicatie."),
            ("AI Data Specialist", 1, "Pregateste, curata si eticheteaza datele de antrenament."),
            ("Responsible AI / AI Ethics Specialist", 1, "Asigura folosirea corecta, transparenta si fara prejudecati a modelelor AI."),
            ("MLOps Engineer (AI)", 1, "Automatizeaza antrenarea, testarea si punerea in productie a modelelor."),
        ],
    },
    "6. Produs (Product)": {
        "intro": "Defineste ce se construieste, pentru cine si de ce. Cate un Product Manager / Owner pentru fiecare squad de Engineering.",
        "roluri": [
            ("Head of Product / CPO Deputy", 1, "Stabileste viziunea si strategia de produs."),
            ("Senior Product Manager", 3, "Conduce roadmap-ul si prioritizarea pentru linii majore de produs."),
            ("Product Manager", 3, "Gestioneaza functionalitati specifice de la idee la lansare."),
            ("Product Owner", 3, "Traduce cerintele in backlog si lucreaza zilnic cu echipele de dezvoltare."),
            ("Business Analyst", 2, "Analizeaza nevoile si documenteaza cerintele detaliate."),
            ("Product Operations Specialist", 1, "Optimizeaza procesele si instrumentele echipei de produs."),
        ],
    },
    "7. Design / UX": {
        "intro": "Modeleaza experienta si interfata cu care interactioneaza utilizatorul.",
        "roluri": [
            ("Design Lead", 1, "Coordoneaza echipa de design si mentine coerenta vizuala."),
            ("Senior UX Designer", 2, "Proiecteaza fluxuri si experiente complexe centrate pe utilizator."),
            ("UI Designer", 2, "Creeaza interfetele vizuale, componentele si stilul aplicatiei."),
            ("Interaction Designer", 1, "Defineste micro-interactiunile si comportamentul interfetei."),
            ("UX Researcher", 2, "Studiaza utilizatorii prin interviuri, teste si observatie."),
            ("Design System Specialist", 1, "Mentine biblioteca de componente reutilizabile."),
            ("Graphic / Brand Designer", 1, "Realizeaza materialele vizuale si identitatea de brand."),
        ],
    },
    "7b. Behavioral Science & Ethical Product Design": {
        "intro": "Proiecteaza produse pe care oamenii le folosesc cu placere si din proprie vointa, fara mecanisme de dependenta. Maximizeaza valoarea reala pentru utilizator si protejeaza atentia si bunastarea acestuia.",
        "roluri": [
            ("Behavioral Science Lead", 1, "Conduce departamentul si integreaza dovezile stiintifice in deciziile de produs."),
            ("Behavioral Scientist / Psiholog cognitiv", 2, "Intelege motivatia utilizatorului pentru a crea experiente utile, nu compulsive."),
            ("Cercetator neurostiinte / stiinte cognitive", 1, "Fundamenteaza deciziile pe dovezi privind atentia, memoria si starea de bine."),
            ("Ethical / Responsible Design Lead", 1, "Se asigura ca mecanicile de produs nu exploateaza vulnerabilitati psihologice."),
            ("UX Researcher (well-being focus)", 1, "Masoara impactul real al produsului, inclusiv eventualele efecte negative."),
            ("Digital Wellbeing Specialist", 1, "Proiecteaza functii de control: limite de timp, pauze, transparenta."),
            ("Behavioral / Marketing Psychologist", 1, "Aplica principii etice de comunicare si persuasiune, fara dark patterns."),
            ("Data Scientist (engagement quality)", 1, "Distinge intre engagement sanatos si engagement compulsiv in metrici."),
            ("Ethics & Policy Advisor", 1, "Aliniaza produsul la reglementarile privind design-ul addictiv si protectia minorilor."),
        ],
    },
    "8. Project & Program Management": {
        "intro": "Coordoneaza echipele, planurile si livrarile.",
        "roluri": [
            ("Head of PMO", 1, "Conduce biroul de management de proiect si standardele de livrare."),
            ("Program Manager", 2, "Coordoneaza initiative complexe ce cuprind mai multe echipe."),
            ("Project Manager", 3, "Planifica, urmareste si livreaza proiectele in buget si timp."),
            ("Scrum Master", 3, "Faciliteaza procesele agile si elimina blocajele echipelor."),
            ("Delivery Manager", 1, "Asigura livrarea coerenta catre clienti."),
        ],
    },
    "9. Marketing": {
        "intro": "Genereaza vizibilitate, interes si cerere pentru produs. Pentru o aplicatie mobila, include functii specifice de crestere in magazinele de aplicatii.",
        "roluri": [
            ("Marketing Lead", 1, "Defineste strategia si coordoneaza campaniile."),
            ("Digital Marketing Specialist", 2, "Gestioneaza campaniile platite si canalele online."),
            ("Content Marketer", 2, "Produce continut (articole, video, materiale) pentru atragere."),
            ("SEO / SEM Specialist", 1, "Optimizeaza vizibilitatea in motoarele de cautare."),
            ("ASO Specialist (App Store Optimization)", 1, "Optimizeaza prezenta in App Store si Google Play: titlu, cuvinte cheie, capturi de ecran si conversia in magazin."),
            ("Social Media Manager", 1, "Gestioneaza prezenta si comunitatea pe retelele sociale."),
            ("Community Manager", 1, "Gestioneaza comunitatea de utilizatori, recenziile din magazine si feedback-ul public."),
            ("Growth Marketer", 1, "Experimenteaza tactici de crestere si optimizeaza palnia de conversie."),
            ("Brand / PR Specialist", 1, "Gestioneaza imaginea publica si relatiile cu presa."),
            ("Technical Writer", 1, "Scrie documentatia produsului, FAQ-ul, help center-ul si textele de suport in aplicatie."),
            ("Marketing Operations", 1, "Administreaza instrumentele si datele de marketing."),
        ],
    },
    "10. Sales / Vanzari": {
        "intro": "Transforma interesul in venituri si contracte.",
        "roluri": [
            ("Sales Director", 1, "Conduce strategia de vanzari si tintele de venit."),
            ("Account Executive", 3, "Inchide contracte si gestioneaza clientii mari."),
            ("Inside Sales Representative", 2, "Califica si converteste lead-urile la distanta."),
            ("Sales Engineer / Pre-sales", 2, "Ofera suport tehnic in procesul de vanzare si demonstratii."),
            ("Business Development Manager", 1, "Identifica parteneriate si oportunitati noi de piata."),
            ("Sales Operations Specialist", 1, "Optimizeaza procesele, CRM-ul si raportarea de vanzari."),
        ],
    },
    "11. Customer Success & Support": {
        "intro": "Asigura ca utilizatorii obtin valoare si raman fideli. Scaleaza cu baza de clienti, nu cu marimea firmei, deci este unul dintre cele mai mari departamente non-tehnice.",
        "roluri": [
            ("Customer Success Lead", 1, "Coordoneaza echipa si strategia de retentie a clientilor."),
            ("Customer Success Manager", 5, "Gestioneaza relatia continua si succesul clientilor cheie."),
            ("Technical Support Engineer", 6, "Rezolva problemele tehnice raportate de utilizatori."),
            ("Onboarding / Implementation Specialist", 3, "Ghideaza clientii noi in adoptarea produsului."),
            ("Customer Experience Analyst", 2, "Masoara satisfactia si imbunatateste experienta clientului."),
            ("Support Team Lead", 1, "Coordoneaza echipa de suport si nivelul de serviciu (SLA)."),
        ],
    },
    "12. HR / People": {
        "intro": "Atrage, dezvolta si pastreaza oamenii potriviti. Include recrutare tehnica dedicata, esentiala pentru o firma cu pondere mare de roluri inginieresti.",
        "roluri": [
            ("HR Director / Head of People", 1, "Conduce strategia de resurse umane si cultura organizationala."),
            ("Technical Recruiter / Sourcer", 2, "Recruteaza specializat roluri tehnice: developeri, DevOps, data, QA."),
            ("Recruiter / Talent Acquisition", 2, "Recruteaza si selecteaza candidatii pentru rolurile non-tehnice."),
            ("People Operations Specialist", 2, "Gestioneaza administrarea, contractele si procesele HR."),
            ("Learning & Development Specialist", 1, "Organizeaza training-urile si dezvoltarea angajatilor."),
            ("Compensation & Benefits Specialist", 1, "Gestioneaza salarizarea si pachetele de beneficii."),
            ("Employer Branding / Internal Comms", 1, "Construieste imaginea de angajator si comunicarea interna."),
            ("HR Business Partner", 1, "Sprijina managerii pe teme de oameni si echipa."),
        ],
    },
    "13. Finance": {
        "intro": "Gestioneaza banii, bugetele si conformitatea financiara.",
        "roluri": [
            ("Finance Director / CFO Deputy", 1, "Conduce strategia financiara si planificarea."),
            ("Accountant / Contabil", 3, "Tine evidenta contabila si intocmeste situatiile financiare."),
            ("FP&A Analyst", 2, "Realizeaza bugete, previziuni si analize financiare."),
            ("Payroll Specialist", 1, "Proceseaza salariile si contributiile aferente."),
            ("Procurement / Achizitii", 1, "Gestioneaza furnizorii si achizitiile companiei."),
            ("Billing / Revenue Operations", 2, "Administreaza facturarea si incasarile recurente."),
        ],
    },
    "14. Legal & Compliance": {
        "intro": "Acopera aspectele juridice, contractuale si de reglementare. Echipa interna mica, sprijinita de consultanta externa la nevoie.",
        "roluri": [
            ("Head of Legal", 1, "Conduce functia juridica si gestioneaza riscul legal."),
            ("Corporate Lawyer", 1, "Se ocupa de chestiunile corporative si contractuale complexe."),
            ("Contracts Manager", 1, "Negociaza si administreaza contractele."),
            ("Privacy / GDPR Officer (DPO)", 1, "Asigura conformitatea cu protectia datelor."),
            ("Regulatory Compliance Specialist", 1, "Monitorizeaza si aplica reglementarile aplicabile, inclusiv IP."),
        ],
    },
    "15. IT intern / Internal IT": {
        "intro": "Sustine functionarea tehnica a companiei la nivel intern. Dimensionat la baza de angajati, nu la baza de clienti.",
        "roluri": [
            ("Internal IT Manager", 1, "Coordoneaza infrastructura si suportul IT intern."),
            ("Internal Help Desk", 2, "Rezolva problemele tehnice ale angajatilor."),
            ("Endpoint Management Specialist", 1, "Gestioneaza laptopurile, dispozitivele si accesele."),
            ("Internal Tools / Systems Admin", 2, "Administreaza instrumentele interne si integrarile."),
        ],
    },
    "16. Operations / Business Operations": {
        "intro": "Optimizeaza modul in care functioneaza afacerea.",
        "roluri": [
            ("Head of Operations / COO Deputy", 1, "Conduce operatiunile si strategia de eficienta."),
            ("Business Operations Analyst", 2, "Analizeaza si imbunatateste procesele interne."),
            ("Strategy & Planning Specialist", 2, "Sprijina planificarea strategica si deciziile de business."),
            ("Revenue Operations (RevOps)", 2, "Aliniaza procesele dintre vanzari, marketing si customer success."),
            ("Vendor Management", 1, "Gestioneaza relatiile cu furnizorii si partenerii."),
            ("Facilities / Office Manager", 2, "Administreaza spatiile si logistica de birou."),
        ],
    },
}


def nume_curat(departament: str) -> str:
    """Elimina prefixul numeric din numele departamentului ('5b. Foo' -> 'Foo')."""
    return re.sub(r"^\d+[a-z]?\.\s*", "", departament).strip()


def total_pe_departament() -> dict[str, int]:
    """Returneaza un dict {departament: numar_angajati}."""
    return {dep: sum(nr for _, nr, _ in d["roluri"]) for dep, d in ORGANIZATIE.items()}


def total_general() -> int:
    """Numarul total de angajati din toate departamentele."""
    return sum(nr for d in ORGANIZATIE.values() for _, nr, _ in d["roluri"])


def listeaza_angajati() -> list[tuple[str, str, str]]:
    """Returneaza o lista plata cu toti angajatii: (departament, rol, descriere)."""
    out: list[tuple[str, str, str]] = []
    for dep, d in ORGANIZATIE.items():
        for rol, nr, descriere in d["roluri"]:
            for i in range(1, nr + 1):
                eticheta = f"{rol} #{i}" if nr > 1 else rol
                out.append((dep, eticheta, descriere))
    return out


def afiseaza() -> None:
    """Afiseaza structura completa in consola."""
    for dep, d in ORGANIZATIE.items():
        subtotal = sum(nr for _, nr, _ in d["roluri"])
        print(f"\n{'=' * 70}\n{dep}  ({subtotal} angajati)\n{'-' * 70}")
        print(f"{d['intro']}\n")
        for rol, nr, descriere in d["roluri"]:
            print(f"  [{nr}x] {rol}")
            print(f"        {descriere}")
    print(f"\n{'=' * 70}")
    print(f"TOTAL DEPARTAMENTE: {len(ORGANIZATIE)}")
    print(f"TOTAL ANGAJATI: {total_general()}")


def export_csv(cale: str = "organizatie.csv") -> None:
    """Exporta toti angajatii intr-un fisier CSV."""
    import csv

    with open(cale, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Departament", "Rol", "Numar", "Descriere"])
        for dep, d in ORGANIZATIE.items():
            for rol, nr, descriere in d["roluri"]:
                w.writerow([dep, rol, nr, descriere])
    print(f"Export realizat: {cale}")


if __name__ == "__main__":
    afiseaza()
