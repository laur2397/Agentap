# Iteratia 2 — spec din sedinta de review (220 agenti)

Aceasta este **Specificația Tehnică pentru Iterația 2**, consolidată din input-ul tuturor departamentelor pentru a transforma prototipul `eie.html` într-un instrument de business viabil, păstrând constrângerea de "single-file" (pentru viteză și portabilitate).

---

### 1. CE PĂSTRĂM (Fundația)
*   **Arhitectura Single-File:** HTML/JS/CSS într-un singur fișier pentru portabilitate maximă.
*   **Stocare:** `localStorage` ca motor de persistență rapidă.
*   **Focus:** Interfața "Premium Dark+Gold" și filozofia de "Secretara AI" pentru input.
*   **Core-ul:** Cele 5 ecrane fundamentale (Acasă, Potriviri, Rețea, Secretara, Profil).

---

### 2. TOP 10 ÎMBUNĂTĂȚIRI (Prioritizate)
1.  **Schema Registry (Validator):** Validare JSON cu `AJV` sau simplu regex înainte de scriere în `localStorage` (previne coruperea).
2.  **Sistem de Criptare (Web Crypto API):** Datele (Trust Score, profil) sunt criptate cu AES-GCM (parolă = cheie).
3.  **Onboarding „Wizard”:** 3 întrebări la prima rulare (Ofer/Caut/Industrie) pentru a popula profilul.
4.  **Motor de Matching (Cosine Similarity):** Vectorizare simplificată (TF-IDF local) pentru a trece de la cuvinte cheie la context.
5.  **Audit Log:** Un jurnal ascuns (read-only pentru user) care înregistrează timestamp-ul fiecărei acțiuni (pentru conformitate).
6.  **Trust Ledger:** Modul pe ecranul „Acasă” ce afișează istoricul tranzacțiilor (match-uri confirmate).
7.  **Status Vizual "Procesare":** Indicatori (spinners) pentru Secretara AI (elimină "cutia neagră").
8.  **Dual Consent Flow:** Butoane de "Accept/Refuz" cu confirmare obligatorie înainte de a dezvălui datele de contact.
9.  **Pipeline Tracker:** Adăugarea stadiilor (Prospectare -> Contract) în profilul de match.
10. **Export/Import JSON:** Funcționalitate de backup manual pentru a simula portabilitatea datelor între dispozitive.

---

### 3. SCHIMBĂRI DE EXPERIENȚĂ & DESIGN
*   **Design Tokens:** Trecerea la CSS Variables (`--gold-primary: #D4AF37`) pentru consistență vizuală.
*   **Progressive Disclosure:** Carduri KPI „acordeon” care se extind doar la tap pentru a păstra ecranul curat.
*   **Skeleton Screens:** Înlocuirea ecranelor albe/goale cu animații de încărcare (skeleton) în timp ce algoritmul procesează.
*   **Accesibilitate:** Contrast crescut (4.5:1) și dimensiuni minime pentru touch-target (44px).

---

### 4. ÎNCREDERE & DATE (Credibilitate fără backend)
*   **Transparență Algoritmică:** Lângă fiecare match, un icon „i” (Explainability) care explică: *"Am propus acest match pentru că ambele profiluri au menționat [Termen X]"*.
*   **Consent Manager:** Modal obligatoriu la start cu link-uri către termeni și politică de date.
*   **Simularea ROI:** Un card "Network Capital" care cumulează valorile estimate ale tranzacțiilor închise (ex: 2 match-uri finalizate = 10.000 EUR ROI).
*   **Securitate:** Timeout de sesiune de 5 minute (șterge cheia de criptare din RAM la inactivitate).

---

### 5. CE AMÂNĂM PENTRU ITERAȚIA 3
*   **Migrarea la Firebase/Supabase:** Amânăm până la validarea "Product-Market Fit" pe un număr minim de 50 de utilizatori.
*   **Integrare OpenAI API (Cloud):** Amânăm pentru a menține aplicația 100% offline-first și fără costuri de infrastructură momentan.
*   **Graf SVG Dinamic (D3.js):** Amânăm complexitatea vizuală pentru a prioritiza precizia algoritmului de matching.
*   **SSO (Azure AD/Okta):** Amânăm integrarea enterprise până la faza de pilot B2B.

---

**NOTĂ FINALĂ CPO:** Iterația 2 nu este despre „mai multe funcții”, ci despre **„mai multă rigoare”**. Vrem ca utilizatorul să simtă că aplicația „gândește” (prin matching semantic) și că datele sale sunt în siguranță (prin criptare locală). **Termen de execuție: 14 zile.** Aștept commit-urile pe branch-ul `iteration-2`.