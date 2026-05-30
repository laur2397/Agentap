# Spec WOW (sintetizat de agentul arhitect din ideile celor 220)

# Cele 7-9 features 'wow' selectate (client-side, fezabile)

Am eliminat tot ce cere backend real (blockchain, MDM, VPN WireGuard, ANAF, semnături criptografice reale, A/B testing, status pages live). Am păstrat ce dă efect 'wow' cu localStorage + JS pur.

### 1. **Why-Match Card** (Match Explainer)
La fiecare potrivire, un card expandabil arată cele 2-3 fraze exacte citate din ambele profiluri (ofer↔caut) care au generat match-ul, cu scor explicabil — nu un procent opac.

### 2. **Confidence Trail / Sursă citată**
Sub fiecare potrivire, un mic timeline „cine a spus ce, când” (ex: „din Dictare 12 mai”) care arată lanțul-sursă, expandabil la tap.

### 3. **Dublu consimțământ animat (gest de glisare/handshake)**
Slider „strânge mâna” care deblochează contactul doar când ambele părți confirmă; starea se salvează în localStorage și animă firul vizual dintre profiluri.

### 4. **Warm Intro Path (Trust Graph)**
Pentru fiecare potrivire calculează din datele locale lanțul cel mai scurt A→B→tu și afișează „te poate prezenta [X]”, cu buton „Cere introducere”.

### 5. **Voice-to-Match după Dictează**
După dictare, un parser simplu (regex/keywords pe „ofer/caut/are nevoie”) extrage oferte/nevoi, creează un card de intenție editabil și propune instant 1-3 potriviri.

### 6. **Auto-generated Intro Brief**
La dublu consimțământ, generează automat un brief de 3 rânduri (ce oferă fiecare + sursa citată + o frază de deschidere) gata de copiat/trimis.

### 7. **Reciprocity Receipt (scor echilibru sănătos)**
Indicator vizual per conexiune care arată dacă schimbul e echilibrat (ambii dau/primesc) sau extractiv, cu avertizare discretă — calculat din istoricul de favoruri din localStorage.

### 8. **Match Decay + „de ce acum”**
Fiecare potrivire neacționată pierde scor vizibil cu un countdown subtil, creând urgență, cu explicația citată din sursă.

### 9. **Pașaport de consimțământ (export GDPR)**
Buton care exportează ca JSON/text descărcabil dovada conexiunii: dublul accept, sursa citată, timestamp — „probă auditabilă” fără criptografie reală.

---

## Direcție de design (3 rânduri)

**Vizual:** Un singur accent cromatic pentru „încredere” (verde-teal) gradat după scor; firul/lanțul ca metaforă unificatoare (linie SVG animată ce conectează profiluri și surse). Carduri cu colțuri rotunde, ierarhie clară: scor → de ce → sursă → acțiune.

**Interacțiune:** Totul progressive disclosure — vezi scorul, tap pentru „de ce”, tap pentru sursă; o singură acțiune primară per card (slider de consimțământ). Micro-animații CSS la deblocare (handshake, fir desenat) pentru momentul 'wow', sub 300ms.

**Date & încredere:** Fiecare element vizibil are o sursă citată cu timestamp din localStorage (nimic „magic”); folosește seed data realist la prima rulare ca demo-ul să arate plin și credibil instant.