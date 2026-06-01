# SPRINT_LOG_PIVOT — loop 5 (pivot E2EE cu releu)

Decizie fondator dupa al 2-lea panel investitori (tot 0/100): PIVOT REAL — sync + discovery + freemium,
fara ca serverul sa vada datele (zero-knowledge). Local-Only ramane DEFAULT; sync e OPT-IN. Design: PIVOT_DESIGN.md.
Limitare mediu: sandbox cu retea pe allowlist -> NU pot hosta releu live; verific pe localhost; deploy-ul = fondatorul.

- 2026-06-01 · M3a DISCOVERY (verificat pe localhost) · RASPUNS la obiectia #1 (network effects/cold-start): director public OPT-IN pe releu (POST /dir, GET /dir/search, POST /dir/del). Client in Reteaua: cautare dupa cuvant-cheie + rezultate + "Adauga" (creeaza conexiune cu cheia publica -> sync pereche posibil) + toggle "Publica-ma". ONEST: directorul NU e E2EE (serverul vede cardurile publice ca sa le caute) -> strict opt-in, DOAR card public; 'ce caut' nu se publica NICIODATA. VALIDAT Playwright (A publica -> C cauta 'transport' -> gaseste Diana, 'ce caut' NU apare in UI; C adauga -> membru cu pub; releul NU contine textul 'ce caut', doar oferta publica). 0 erori.
- 2026-06-01 · M2 MULTI-DEVICE PROPRIU (verificat pe localhost) · sync E2EE "cu tine insuti": dispozitivele care iti impart identitatea (prin transferul .eie) folosesc un "mailbox de sine" = mailboxId(propria cheie publica), cu cheie de canal ECDH(priv,propriul pub). syncSelfPush/syncSelfPull trimit un snapshot (note+task-uri proprii + profil) sigilat E2EE; merge = last-writer-wins la nivel de dispozitiv (snapshot cel mai recent castiga; versiune DB.selfV bumpata in save(), suprimata la aplicarea unui snapshot remote via APPLYING). Integrat in syncNow alaturi de sync-ul pereche. VALIDAT Playwright (2 dispozitive cu identitate comuna): A adauga nota+task -> B le primeste; B sterge task-ul + adauga nota proprie -> A converge (are nota lui B, stergerea s-a propagat, nota lui A pastrata). 0 erori. Propaga create+edit+delete.
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
