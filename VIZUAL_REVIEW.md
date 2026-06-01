# VIZUAL_REVIEW — 12 experti au vazut aplicatia (scor mediu 6.0/10, GATA 0/12)

# VIZUAL_REVIEW.md

## SCOR VIZUAL AGREGAT: 6.0/10
Produsul are o fundație cromatică corectă și o arhitectură logică, dar suferă de o supraîncărcare vizuală care îi anulează poziționarea premium. Este perceput în prezent ca un "dashboard tehnic" aglomerat, nu ca un instrument de networking rafinat; necesită o curățenie radicală pentru a inspira încredere și eleganță.

## CE MERGE VIZUAL
1. **Paleta cromatică:** Utilizarea fundalului închis cu accente indigo este corectă și sustenabilă pentru un produs privacy-first.
2. **Ierarhia logică:** Structura informațională pe ecrane este bine gândită și intuitivă.
3. **Tipografia:** Alegerea fontului Inter este excelentă pentru lizibilitate și sobrietate.
4. **Consecvența de bază:** Există o încercare de sistem (carduri, butoane) care oferă o structură de plecare.
5. **Dark Mode:** Implementarea modului întunecat transmite corect caracterul "securizat" al produsului.

## CE STRICA VIZUAL
1. **Densitatea informațională:** Excesul de text explicativ (micro-copy) sufocă interfața și transformă aplicația într-un document tehnic.
2. **Zgomotul vizual:** Prea multe borduri (strokes), umbre și elemente grafice care concurează între ele.
3. **Inconsistențe de sistem:** Padding-uri inegale, raze de colțuri variabile și dimensiuni haotice ale elementelor.
4. **Lipsa spațiului negativ (whitespace):** Interfața este înghesuită; elementele nu au loc să "respire", ceea ce obosește ochiul.
5. **Contrastul deficitar:** Textele secundare și iconografia nu respectă standardele de accesibilitate, fiind greu de scanat.

## TOP 15 IMBUNATATIRI VIZUALE
1. **Standardizare:** Definește și aplică un sistem de 4-8px pentru toate padding-urile și marginile.
2. **Eliminare borduri:** Elimină bordurile (strokes) exterioare ale cardurilor; folosește doar diferențe subtile de nuanță (surface layers).
3. **Radical copy-cut:** Redu textele explicative la 50% din volum; folosește iconografie pentru a descrie funcționalitățile.
4. **Radius Token:** Setează o rază de colț unică (ex: 12px sau 16px) pentru absolut toate elementele (carduri, inputuri, butoane).
5. **Contrast WCAG:** Crește luminozitatea textelor secundare/gri pentru a atinge un raport de contrast de minim 7:1.
6. **Aerisire:** Mărește spațiul dintre elementele ierarhice (ex: între titluri și paragrafe) cu cel puțin 24px.
7. **Simplitate Header:** Simplifică header-ul; păstrează doar acțiunile critice și ascunde restul în meniul de setări.
8. **Ierarhie Tipografică:** Diferențiază clar titlurile (bold/large) de corpul textului (regular/medium) pentru a ghida scanarea.
9. **Butoane:** Uniformizează stilul butoanelor (doar 2 tipuri: Primar/Solid și Secundar/Ghost).
10. **Eliminare Umbre:** Elimină toate umbrele (drop shadows) "murdare"; folosește doar iluminare subtilă dacă e necesar.
11. **Tooltips:** Mută explicațiile tehnice lungi în iconițe de tip "i" (info) cu tooltip-uri native.
12. **Grid Sistem:** Aliniază toate elementele pe un grid strict, evitând decalajele vizuale.
13. **Iconografie:** Folosește o singură familie de iconițe (ex: Phosphor sau Heroicons) cu grosime (stroke) constantă.
14. **Focus:** Folosește spațiul negativ pentru a evidenția butonul de acțiune principal (Call to Action).
15. **Contrast vizual:** Folosește nuanțe de gri mai deschise pentru fundalul cardurilor pentru a le separa vizual de background-ul general, fără a folosi linii.

## VERDICT
**MAI E DE LUCRU.** Produsul nu este gata de lansare în stadiul actual deoarece nu comunică „premium” la prima vedere. Blocajul principal este **densitatea vizuală**. Odată ce se implementează „curățenia” (reducerea textului + utilizarea spațiului negativ), produsul va trece automat la standardul necesar.