# Review Secretara AI — board

Iată raportul consolidat în urma review-ului executiv. Direcția este clară: transformăm acest prototip într-un instrument robust de productivitate, păstrând filozofia *privacy-first*.

***

# SECRETARA_REVIEW.md

## CE MERGE
1. **Arhitectura Local-Only:** Zero dependențe externe, conformitate GDPR nativă și latență zero.
2. **"Brief de 1 minut":** Reducerea efortului cognitiv prin centralizarea contextului (notite, task-uri, istoric).
3. **Sistemul HMAC:** Validarea integrității întâlnirilor oferă trasabilitate fără nevoie de server.
4. **Logica de "Notează după apel":** Extragerea intentiilor prin cuvinte-cheie aduce valoare imediată fără LLM-uri scumpe.
5. **Privacy by Design:** Stocarea locală elimină vectorii de atac cloud și exfiltrarea datelor.
6. **Fluxul de lucru:** Traseul notițe -> task-uri -> întâlniri este intuitiv și fluid pentru utilizator.

## CE NU MERGE / LIPSESTE
1. **Volatilitatea datelor:** Lipsa persistenței la refresh (starea actuală este doar în RAM).
2. **Backup-ul securizat:** Riscul critic de pierdere a întregii baze de date prin ștergerea cache-ului.
3. **Vizibilitatea "Pipeline-ului":** Lipsa prioritizării relațiilor (nu știm cine necesită follow-up urgent).
4. **Notificări/Alertare:** Task-urile și întâlnirile sunt "invizibile" dacă utilizatorul nu accesează activ aplicația.
5. **Căutare Globală:** Incapacitatea de a scana rapid prin întreg istoric (notite + task-uri + persoane).
6. **Managementul sesiunii:** Lipsa unui mecanism de import/export care să permită portabilitatea între browsere/dispozitive.

## TOP 20 IMBUNATATIRI
1. Implementare `localStorage` pentru persistență automată la fiecare modificare.
2. Buton de "Export JSON" (backup) și "Import JSON" (restaurare) în setări.
3. Command Palette (Ctrl+K) pentru crearea rapidă de notite/task-uri oriunde.
4. Motor de căutare "Fuzzy" (search-as-you-type) pentru toate datele stocate.
5. Sistem de scoring/prioritizare (1-5 stele) pentru contacte.
6. Vizualizare "Timeline" pentru istoricul interacțiunilor cu fiecare persoană.
7. CSS Grid pentru organizarea modulară a tab-urilor și dashboard-ului.
8. Status relație (Rece/Activ/Prioritar) cu filtrare pe ecranul principal.
9. Notificări native (Browser Notification API) pentru task-uri scadente.
10. Funcție "Emergency Wipe" pentru ștergerea completă a `localStorage`.
11. Filtrare avansată pe dashboard după tag-uri și dată.
12. Badge-uri vizuale pe tab-uri pentru task-uri "în întârziere".
13. Export criptat (AES-GCM via Web Crypto API) pentru backup-ul JSON.
14. Vizualizator săptămânal de întâlniri (Calendar view simplificat).
15. Validare de ștergere (Data Portability - "Export înainte de ștergere").
16. Input de tip "Quick Add" pentru task-uri cu detecție de dată (ex: "mâine").
17. Service Worker simplu pentru caching local (PWA-ready pentru offline).
18. Sortare automată a task-urilor în funcție de termenul limită (scadență).
19. Audit log pentru acțiunile critice (creare/ștergere intâlnire).
20. Mod "Focus" (ascunde tot, lasă doar notița activă și input-ul de comandă).