# Cercul EIE — aplicație de business networking (prototip)

`eie.html` — o aplicație mobilă **într-un singur fișier**, fără backend, care funcționează 100% în browser.

## Ce face
Un cerc privat de oameni de afaceri în care:
- declari **ce oferi** și **ce cauți**;
- primești **sugestii de conexiuni** pe baza intereselor comune (matching local TF-IDF + cosine);
- te conectezi prin **dublu consimțământ** (ambele părți acceptă);
- ai o **Secretară AI**: notițe + brief de întâlnire, calendar & programare (cu export Google Calendar / .ics / email), task-uri cu remindere, follow-up.

### Ecrane
- **Acasă** — rezumat, statistici, următoarea întâlnire, pulse de rețea, conexiuni recente.
- **Potriviri** — persoane de contactat (filtru pe industrie), card „gist-first”, acțiuni clare.
- **Rețeaua** — lista conexiunilor + hartă force-directed opțională.
- **Secretara** — întâlniri, task-uri, jurnal de notițe (cu #tag-uri), brief de 1 minut.
- **Profil** — ce ofer / ce caut, editare profil, jurnal de audit, confidențialitate, setări.

## Cum o rulezi
1. Deschide `eie.html` în orice browser (telefon sau laptop). Nu necesită server, instalare sau internet (fonturile Google sunt opționale).
2. La prima rulare **alegi o parolă de sesiune** (min. 4 caractere). Din ea se derivează cheia de criptare; nu se salvează pe disc.
3. Apasă **„Doar explorez”** pentru a intra cu 20 de membri demo, sau treci prin onboarding (creezi un cont real).
4. La reschideri, introdu aceeași parolă. ⚠️ Dacă o uiți, datele criptate **nu pot fi recuperate** (există „resetează” cu backup).

## Securitate & confidențialitate (model „Local-Only”)
- **Criptare la repaus**: AES-GCM; cheia derivată din parolă cu PBKDF2 (150k), ținută **doar în RAM**.
- **Integritate**: checksum SHA-256 + Trust Ledger pe lanț HMAC-SHA256 (verificabil).
- **Auto-lock** la inactivitate (3 min) sau manual — cheile sunt eliberate din memorie (best-effort).
- **CSP strict** (`connect-src 'none'` → fără exfiltrare) + **Trusted Types** (zero sink-uri DOM-XSS) + sanitizare la intrare.
- **Privacy-by-design**: „ce caut” și identitatea se dezvăluie celeilalte părți **doar după dublu consimțământ**.
- Scriere tranzacțională cu rollback; import cu validare de schemă.

## Limitări oneste (nu „magie”)
- Fără backend / fără cont real / fără sincronizare automată cu Google (export-urile sunt **inițiate de tine**; aplicația nu trimite nimic singură).
- Matching **euristic** (cuvinte-cheie / TF-IDF), nu embeddings sau LLM real.
- Datele trăiesc doar în browserul tău; ștergerea cache-ului le elimină. Fă-ți **export (JSON)** pentru backup.
- Securitatea finală depinde de **tăria parolei tale** (folosește un manager de parole).

## Testare
Testele sunt scripturi externe (Playwright, în afara fișierului de producție). `eie.html` nu conține cod de test.
Validare rapidă: extrage `<script>` și rulează `node --check`; deschide app-ul și verifică zero erori de consolă.

## Proces
Aplicația a fost dezvoltată printr-un proces auditat: fiecare iterație trece printr-un „board de audit” (vezi `examples/audit.py`, `AUDIT_*.md`) și un jurnal de sprint (`SPRINT_LOG.md`, `BACKLOG.md`).
