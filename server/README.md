# Releu Cercul EIE — zero-knowledge (loop5 / pivot E2EE)

Server-releu de referință pentru sincronizarea E2EE. **Nu vede conținutul** — transportă doar
text criptat end-to-end pe „mailbox"-uri opace. Nu deține chei, nu poate decripta.

## Rulare locală
```bash
node server/relay.js
# implicit pe http://127.0.0.1:8787
```
Variabile de mediu opționale:
- `PORT` (implicit 8787)
- `RELAY_FILE` — cale către un fișier JSON pentru persistență (implicit: doar în memorie)
- `RELAY_MAXBYTES` (implicit 65536) — dimensiunea maximă per mesaj
- `RELAY_MAXITEMS` (implicit 500) — inel per mailbox
- `CORS_ORIGIN` (implicit `*`)

## API
- `POST /m/:mailbox` — body = ciphertext (text/plain) → `{seq}`
- `GET /m/:mailbox?since=N` → `{items:[{seq,ct}], last}`
- `GET /health` → `{ok:true}`

`:mailbox` = 16–128 caractere hex (derivat client-side din cheile publice ale perechii).

## Conectarea aplicației
În app: **Profil → Sincronizare** → pune adresa releului → **Salvează** → **Activează sync**.
Sync e **opt-in**; implicit aplicația rămâne Local-Only.

## Producție (go-live)
1. Deployează `relay.js` pe un host cu Node (Render / Fly.io / Railway / un VPS). Pune-l pe HTTPS.
2. **Important — CSP:** în `app/eie.html`, în meta `Content-Security-Policy`, adaugă originea releului tău
   la `connect-src` (înlocuiește/extinde `http://127.0.0.1:* http://localhost:*` cu `https://relay.domeniul-tau`).
   Asta păstrează protecția anti-exfiltrare: aplicația poate vorbi DOAR cu releul tău, nimic altceva.
3. Pentru scară reală: înlocuiește stocarea in-memory cu Redis/Postgres și adaugă rate-limiting/uthentificare
   de transport. Modelul E2EE nu se schimbă — serverul rămâne zero-knowledge.

## Model de amenințare (onest)
Releul e „honest-but-curious": vede **metadata** (id de mailbox, dimensiuni, momentul mesajelor),
NU și conținutul. Nu stochează niciodată chei private. Conținutul e criptat AES-GCM cu o cheie de canal
derivată prin ECDH P-256 + HKDF între cele două chei publice ale perechii.
