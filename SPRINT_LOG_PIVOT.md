# SPRINT_LOG_PIVOT — loop 5 (pivot E2EE cu releu)

Decizie fondator dupa al 2-lea panel investitori (tot 0/100): PIVOT REAL — sync + discovery + freemium,
fara ca serverul sa vada datele (zero-knowledge). Local-Only ramane DEFAULT; sync e OPT-IN. Design: PIVOT_DESIGN.md.
Limitare mediu: sandbox cu retea pe allowlist -> NU pot hosta releu live; verific pe localhost; deploy-ul = fondatorul.

- 2026-06-01 · M1 FUNDATIE E2EE (verificat pe localhost) ·
  (1) identitate ECDH P-256 (ensureIdentity): cheie privata stocata criptat in DB (la repaus AES-GCM), cheie publica partajabila;
  (2) format cod/QR EIE2 cu cheie publica (k), back-compat EIE1; addByCode stocheaza member.pub+cursor;
  (3) releu de referinta ZERO-KNOWLEDGE in server/relay.js (Node built-in, append-only, fara dependinte) + server/README.md cu deploy;
  (4) transport opt-in (DB.relay {url,on}) + CSP connect-src restrans STRICT la origin-ul releului (implicit doar localhost);
  (5) cheie de canal pereche = ECDH(privA,pubB)->HKDF->AES-GCM; envelope sealFor/openFrom; mailboxId = SHA-256(sort(pubA,pubB));
  (6) sync pereche: syncPushTo/syncPullFrom/syncNow — cardul public se propaga automat la contacte.
  VALIDAT end-to-end Playwright (2 contexte, Ana<->Bogdan): schimb EIE2 -> Ana isi schimba oferta+rolul -> push -> Bogdan pull ->
  primeste 'Director General' + 'OFERTA_NOUA_SYNC_42'; RELEUL a stocat DOAR ciphertext (fara scurgere de nume/rol/oferta in clar). 0 erori consola.
  Onestitatea claim-urilor actualizata: trustchip arata 'Sync E2EE' cand e activ, 'Local' implicit; textul de transparenta + 'Despre' nuantate.
  RAMAS: M2 multi-device propriu + UI stare sync/merge; M3 discovery opt-in + freemium tiers + entitlements.
