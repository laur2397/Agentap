# Iteratia 5 — redesign social/luminos (sedinta de urgenta, 220 agenti)

Aceasta este **Specificația Tehnică și de Design (Iterația 5)**. Ca CPO, ordinea de zi este clară: eliminăm „fricțiunea cognitivă” și transformăm platforma dintr-un audit financiar într-un motor de networking high-end.

---

# Redesign Spec v.5: "Human-Centric Ecosystem"

## 1. Direcția Vizuală: The Bloom/Clay Aesthetic
*   **Palette:**
    *   `Background`: `#FAFAFA` (Off-white)
    *   `Card-Surface`: `#FFFFFF`
    *   `Primary-Accent`: `#6366F1` (Indigo-Vivid)
    *   `Status-Pill-BG`: `rgba(99, 102, 241, 0.08)`
    *   `Text-Main`: `#1E293B` (Slate-800)
    *   `Text-Muted`: `#64748B` (Slate-500)
*   **Tipografie:** `Inter`, font-face 400 (regular) & 600 (bold). Fără serif.
*   **Shadows:** `0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03)`.
*   **Micro-interactions:** Efect de "lift" (ridicare) la hover pe carduri; butoane cu tranziție lină de stare (scale-down 0.98 la click).

## 2. Limbaj: Din Jargon în Context (Tabel Conversie)

| Jargon (Vechi) | Uman (Nou) |
| :--- | :--- |
| `TF-IDF / Cosine Similarity` | "Aveți interese comune în Energie" |
| `Trust Ledger Verified` | "Profil verificat și activ" |
| `Deal Flow Score: 88` | "Potrivire excelentă pentru profilul tău" |
| `SHA-256 / Hash Match` | "Conexiune securizată" |
| `1 semnale (trigger)` | "Bogdan caută parteneri în piață" |
| `ROI (Projected)` | "Valoare potențială ridicată" |
| `Double Opt-in Status` | "Acord reciproc confirmat" |
| `Compliance Check: Passed` | "Sigur de contactat" |

## 3. Cardul de Potrivire (Regândit - "Gist-First")
*   **Header (2 secunde):** Avatar (rotunjit 12px), Nume (Bold 16px), Titlu (14px).
*   **Body (Context):** O singură frază narativă: *"Bogdan caută furnizor. Aveți 3 interese comune și o conexiune mutuală (Maria)."*
*   **Action-Dock:**
    *   `Primary`: Buton Indigo ("Cere introducere")
    *   `Secondary`: Buton Ghost ("Vezi profil")
    *   `Menu-Dots`: ("Salvează", "Ignoră")
*   **Status vs. Acțiune:** Statusul ("Prospect") stă în colțul dreapta-sus ca o pastilă discretă; nu se atinge de zona de acțiune.

## 4. Transformarea Ecranelor
*   **Acasa (Timeline):** Bandă orizontală de zile (ex: "Joi, 12 Oct") cu carduri tip Timeline. Eliminăm tabelele.
*   **Potriviri:** Grid de carduri „Airy”. Spațiu între carduri: 24px.
*   **Rețea:** Listă cu avataruri și status „Live” (bulină verde mică pe avatar).
*   **Profil:** Structură de tip tab (Bio, Interese, Conexiuni). Acțiuni clare la top-level.

## 5. Ce ascundem, dar păstrăm (The "Under-the-Hood" layer)
*   **Criptarea (SHA-256):** Rămâne în header-ul de securitate al sesiunii, dar devine un simplu "Shield Icon" mic în footer-ul fiecărui card, indicând "Conexiune protejată" la hover.
*   **Audit/Compliance:** Aceste date rămân disponibile pentru echipa de Customer Success într-un "Admin Toggle" (pentru a satisface nevoile lor de suport) fără a fi vizibile utilizatorului final.

---

### Implementare (Single-File Snippet Demo)
```html
<style>
  body { font-family: 'Inter', sans-serif; background: #FAFAFA; color: #1E293B; }
  .card { background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
  .btn-indigo { background: #6366F1; color: white; border: none; padding: 8px 16px; border-radius: 8px; cursor: pointer; }
  .pill { background: #EEF2FF; color: #4F46E5; padding: 4px 12px; border-radius: 99px; font-size: 12px; font-weight: 600; }
</style>

<div class="card" style="width: 350px;">
  <div style="display: flex; justify-content: space-between; align-items: start;">
    <div style="font-weight: bold;">Bogdan Ionescu</div>
    <span class="pill">Prospect</span>
  </div>
  <p style="font-size: 14px; color: #64748B; margin: 12px 0;">Bogdan caută furnizor. Aveți 3 interese comune în Energie.</p>
  <div style="display: flex; gap: 8px;">
    <button class="btn-indigo">Cere introducere</button>
    <button style="border: 1px solid #E2E8F0; background: none; padding: 8px 16px; border-radius: 8px; cursor: pointer;">Profil</button>
  </div>
</div>
```

**Concluzie:** Această iterație elimină complexitatea inutilă. Ne concentrăm pe **Relație**, nu pe **Algoritm**. Aștept versiunea finală de UI pentru QA.