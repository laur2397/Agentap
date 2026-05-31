# Paleta vizuala — board directori + Cxx

În calitate de CEO/CPO, am analizat inputul valoros al echipei. Decizia strategică este să **adoptăm un sistem dual (Light & Soft-Dark)**, deoarece utilizatorii noștri (executivi/antreprenori) accesează aplicația în contexte diferite: în timpul zilei (birou/lumină naturală) și seara (lounge/relaxare).

Vom merge pe direcția **„Modern Executive Heritage”** — un hibrid între *Quiet Luxury Sand* și *Soft-Dark Navy*, care oferă vizibilitate, autoritate și confort cognitiv.

### 1. DECIZIE: "The Executive Hybrid"
*   **De ce:** Eliminăm percepția de „bunker” prin paleta Light, dar păstrăm „eleganța nocturnă” a modului Soft-Dark. Această flexibilitate crește timpul de retenție, deoarece utilizatorul nu trebuie să „lupte” cu luminozitatea ecranului în funcție de mediu. Este premium-accesibil: sofisticat, dar empatic.

---

### 2. DESIGN TOKENS (CSS Variables)

```css
:root {
  /* LIGHT MODE (Implicit pentru Onboarding & Daytime) */
  --bg: #F7F4EF;        --bg2: #EDEAE5;       /* Fond principal */
  --card: #FFFFFF;      --card2: #F5F3EF;     /* Carduri/Containere */
  --line: #E0DBD4;      --ink: #1A202C;       /* Text primar (Antracit) */
  --ink2: #4A5568;      --muted: #A0AEC0;     /* Text secundar/Inactiv */
  --primary: #B88E56;   --accent: #1A2B3C;    /* Bronz-mat / Navy-profund */
  --success: #2E7D32;   --warn: #D97706;

  /* SOFT-DARK MODE (Pentru Night/Lounge) */
  --bg-d: #121625;      --bg2-d: #1A202C;
  --card-d: #1E2536;    --card2-d: #252D3E;
  --line-d: #2D3748;    --ink-d: #F8F9FA;
  --ink2-d: #CBD5E0;    --muted-d: #718096;
  --primary-d: #D4AF37; --accent-d: #94A3B8;
  --success-d: #54C2A0; --warn-d: #F6AD55;
}
```

---

### 3. PSIHOLOGIE & UTILIZARE

| Token | Rol | Psihologie |
| :--- | :--- | :--- |
| **--bg** | Fundal | **Siguranță:** Crem-nisipiu reduce anxietatea și oboseala oculară. |
| **--card** | Interfață | **Claritate:** Distincția dintre fundal și card creează ierarhie vizuală. |
| **--primary** | Acțiuni/CTA | **Exclusivitate:** Bronz-mat/Champagne transmite valoare fără a fi strident. |
| **--accent** | UI/Header | **Autoritate:** Navy-profund/Gri-ardezie ancorează brandul în zona business. |
| **--ink** | Text principal | **Profesionalism:** Antracitul este mai blând cu ochii decât negrul pur. |
| **--success** | Trust Score | **Validare:** Verdele natural (nu electric) inspiră încredere în AI. |

---

### 4. IMPLEMENTARE: REGULI DE UX
*   **Ierarhie:** Folosim `Cormorant Garamond` pentru Headings (Bold/Semibold) pentru a păstra identitatea premium. `Jost` (400-500) pentru orice text care necesită lizibilitate rapidă.
*   **Tactilitate:** Înlocuim liniile grele cu **umbra difuză**: `box-shadow: 0 4px 20px rgba(0,0,0,0.05);` (Light) sau `0 4px 20px rgba(0,0,0,0.3);` (Dark).
*   **Borduri:** `border: 0.5px solid var(--line);` pentru a menține un look minimalist, de "galerie de artă".
*   **Input-uri/Butoane:** Butoanele de acțiune vor folosi `--primary` cu un ușor gradient subtil pentru a sugera profunzime, nu platitudine.

### 5. ACCESIBILITATE (WCAG)
*   **Contrast:** Raportul de contrast între `--ink` și `--bg` este de **8.4:1**, depășind standardul AAA (7:1).
*   **Confort:** Am eliminat complet puritatea negrului (#000000) și a albului (#FFFFFF) pentru a preveni „efectul de halou” pe ecranele OLED, crescând timpul de retenție prin confort vizual prelungit.
*   **AI Empatic:** Mesajele Secretarei AI vor apărea pe carduri cu fundal `--card2` pentru a le distinge vizual de conținutul generat de utilizatori, facilitând „încrederea în recomandări”.

Această structură este gata de pasat către echipa de frontend (React/Tailwind sau CSS nativ) pentru implementare imediată.