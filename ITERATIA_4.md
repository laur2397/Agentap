# Iteratia 4 — spec din sedinta de imbunatatire (220 agenti)

În calitate de CPO, am sintetizat viziunea celor 16 departamente într-o **Iterație 4 (nume de cod: "The Intelligent Core")**. Aceasta transformă `eie.html` dintr-un document static într-un organism algoritmic autonom, păstrând puritatea *Local-Only* și arhitectura *Single-File*.

Iată specificația pentru **Iterația 4**:

---

### 1. TOP 10 ÎMBUNĂTĂȚIRI PRIORITIZATE

1.  **Motor de Matching Semantic (Vector-Lite):** Înlocuim TF-IDF cu embeddings `Xenova/all-MiniLM-L6-v2` (ONNX Web). *Impact:* Potriviri bazate pe sens, nu pe cuvinte cheie. *UI:* Scorul de proximitate (0-100%) sub fiecare card.
2.  **Persistență IndexedDB Criptată:** Migrare de la RAM la `IndexedDB` cu AES-GCM. *Impact:* Datele supraviețuiesc refresh-ului. *UI:* "Vault Status Badge" în header (Sync/OK/Error).
3.  **Secretara AI "Context-Aware":** Implementare RAG local (VectorStore în IndexedDB). *Impact:* AI-ul reține istoricul conversației. *UI:* Chat-bubble cu efect `typewriter` și butoane "Quick-Action".
4.  **Vizualizare Force-Directed (Canvas/D3):** Motor de fizică pentru rețea. *Impact:* Scalabilitate vizuală. *UI:* Noduri care se atrag/resping natural; particule animate pe conexiuni.
5.  **Dashboard "Why Matched?" (Radar Chart):** Vizualizarea logică a algoritmului. *Impact:* Transparență radicală. *UI:* Radar chart SVG în tooltip-ul fiecărui profil (Trust/Competențe/Interese).
6.  **Pipeline Kanban Vizual:** Tab de "Potriviri" transformat în funnel. *Impact:* Gestionarea proactivă a lead-urilor. *UI:* Coloane drag-and-drop cu statusuri (Prospectare/Calificare/Închis).
7.  **Sistem de "Panic Wipe":** Securitate extremă. *Impact:* Protecție la acces fizic. *UI:* Buton "slide-to-wipe" în setări și "Privacy Shield" (blur UI la inactivitate).
8.  **Onboarding Interactiv (Driver.js):** Ghidaj pas-cu-pas. *Impact:* Elimină churn-ul. *UI:* Spotlight pe funcții cheie cu progress stepper.
9.  **Audit Ledger Imuabil:** Hash-chain vizibil. *Impact:* Integritate dovedită. *UI:* Tab "Audit" în profil cu semnături SHA-256 exportabile.
10. **Design Tokens & Glassmorphism:** Sistem de variabile CSS. *Impact:* Consistență premium. *UI:* Blur-uri, transparențe și ierarhii de elevație (Depth System).

---

### 2. ÎMBUNĂTĂȚIRI VIZUALE (Rafinament Premium)
*   **Fluid Morphing:** Tranziții de stare între ecrane folosind `View Transitions API`. Aplicația nu se mai încarcă, se "transformă".
*   **Skeleton Shimmer:** Toate elementele (profile, grafuri) folosesc skeleton-uri animate în timpul calculului.
*   **Glassmorphism Depth:** Cardurile de profil folosesc `backdrop-filter: blur(10px)` pentru a crea ierarhie vizuală.
*   **Zen Mode:** După 20 minute de activitate, UI-ul trece subtil în grayscale pentru a reduce oboseala cognitivă (Wellbeing Pulse).

---

### 3. ÎMBUNĂTĂȚIRI FUNCȚIONALE
*   **Matching:** Motorul `Vector-Lite` calculează distanța cosinus în browser; orice editare de profil recalibrează *instantaneu* ordinea în ecranul "Potriviri".
*   **Secretara:** Acum parșează intenția (ex: "găsește pe cineva în București") și returnează un card de acțiune interactiv, nu doar text.
*   **Rețeaua:** Zoom & Pan nativ pe Canvas; nodurile afișează "Pulse" (activitate recentă) prin pulsații ușoare de lumină.
*   **Filtrare:** Smart Filter Bar (sidebar) cu slider-e pentru "Trust Score" și "Relevanță".

---

### 4. CRITERIU DE SUCCES: Cum știm că am reușit?
O îmbunătățire este **NOTABILĂ** și **SUCCESUL** este atins dacă:
1.  **Testul de 5 secunde:** Un utilizator nou înțelege *de ce* i-a fost recomandat un membru în mai puțin de 5 secunde (datorită Radar Chart-ului).
2.  **Testul de Persistență:** După un `hard refresh` (F5), aplicația revine exact în starea anterioară (chat-ul și filtrele rămân active).
3.  **Testul de "Agentic Feel":** Secretara AI propune activ o acțiune (ex: "Ai o potrivire de 90% cu X, dorești să inițiezi un mesaj?") fără ca utilizatorul să o fi întrebat explicit.
4.  **Testul de Audit:** Exportul fișierului JSON conține hash-ul lanțului de integritate, validat de "Integrity Guard" la import, confirmând că datele nu au fost compromise.

**Acesta este standardul Iteratiei 4. Implementarea începe imediat.**