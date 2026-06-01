# PIVOT_DESIGN — de la Local-Only la hibrid E2EE cu releu (loop 5)

Decizie fondator (dupa al 2-lea panel de investitori, tot 0/100): PIVOT REAL catre scara de tip venture.
Adaugam sincronizare automata + discovery + freemium, FARA ca serverul sa vada datele in clar (zero-knowledge).

## Principiu director
Serverul-releu este un "postas prost": stocheaza si transporta DOAR ciphertext. Nu poate citi continutul,
nu detine cheile. Confidentialitatea ramane (E2EE), dar castigam efecte de retea, multi-device si monetizare.
Local-Only ramane MODUL IMPLICIT; releul/sync e OPT-IN (nu rupem produsul auditat pentru cei care vor pur-local).

## Identitate & chei (WebCrypto, fara biblioteci)
- La prima rulare: se genereaza o pereche de chei ECDH P-256 (cheie de identitate, pe termen lung).
- Cheia PRIVATA se stocheaza criptata in DB-ul local (cu cheia de sesiune AES-GCM existenta). NU pleaca niciodata.
- Cheia PUBLICA e partajabila — intra in "codul de conexiune" si in QR (extindem formatul: EIE2:).
- Canal pereche (A<->B): secret comun = ECDH(privA, pubB) == ECDH(privB, pubA) -> HKDF -> cheie AES-GCM de canal.
- Mailbox id = SHA-256(sort(pubA_raw, pubB_raw)) in hex -> identificator opac, deterministic, fara PII.

## Releu (zero-knowledge) — REST minimal
- POST /m/:mailbox        body=ciphertext (append-only)        -> {seq}
- GET  /m/:mailbox?since=N                                     -> [{seq, ct}]   (ct = base64 ciphertext)
- Fara conturi pt. transport (mailbox-ul e capabilitatea). Rate-limit + cap de dimensiune.
- Stocare: in-memory / fisier (referinta). Productie: Redis/Postgres. Serverul NU are cheile -> nu poate decripta.
- (Freemium se aplica la nivel de ENTITLEMENT separat, nu blocheaza transportul de baza in referinta.)

## Sincronizare (faza 1 — pereche, contacte deja cunoscute)
- Model: fiecare schimbare relevanta pt. un contact pereche se serializeaza, se cripteaza cu cheia de canal,
  se trimite in mailbox-ul perechii. Celalalt client polleste (GET ?since=cursor), decripteaza, aplica (merge).
- Merge: append-only event log per mailbox + last-writer-wins pe id de inregistrare (simplu, determinist).
- Multi-device propriu: un "mailbox de sine" criptat cu o cheie derivata din parola -> sync intre device-urile tale.

## Discovery (faza 2 — mai tarziu, partea grea filozofic)
- Optional, opt-in. Directory unde publici un card public minimal + cheia publica.
- Tensiune reala: discovery de straini cere ca serverul sa vada ceva cautabil -> NU e E2EE pe acea parte.
  De aceea e separat, opt-in, si publica DOAR cardul public (nu 'ce caut'). Decizie amanata pana validam faza 1.

## Freemium (faza 3)
- Free: local + sync pereche cu pana la N contacte + 1 device.
- Paid: sync nelimitat + multi-device + (ulterior) discovery + backup gestionat.
- Enforcement real cere entitlements server-side (token semnat). Referinta: definim tier-urile + gating client (stub).

## Modificari de securitate (constiente, auditabile)
- CSP: connect-src trece din 'none' in origin-ul releului (ws/https), DOAR cand sync e activat. Local-Only ramane default.
- Threat model nou: serverul e "honest-but-curious" -> vede metadata (mailbox id, dimensiuni, timing), NU continut.
  Documentam ce scurge metadata. connect-src restrans strict la origin-ul releului (anti-exfiltrare catre alte domenii).

## Faze livrabile (fiecare: validat + audit la fiecare al 3-lea)
M1 (fundatie, verificabila pe localhost):
  1. Identitate ECDH P-256 (generare, stocare criptata, expunere cheie publica).
  2. Format EIE2: cod/QR cu cheie publica + compat. inapoi cu EIE1.
  3. Releu de referinta (Node, in /server) + teste.
  4. Strat client de transport (fetch catre releu, opt-in, CSP comutabila).
  5. Cheie de canal pereche via ECDH+HKDF; envelope E2EE (encrypt/decrypt).
  6. Sync pereche end-to-end: A -> releu -> B, aplicat la B. Test pe localhost cu 2 contexte; releul vede doar ciphertext.
M2: multi-device propriu (mailbox de sine) + UI de stare sync + reziliența/merge.
M3: discovery opt-in (card public) + freemium tiers + entitlements.

## Ce NU facem
- Nu trimitem niciodata 'ce caut' sau continut in clar la server. Nu stocam chei private pe server.
- Nu pretindem ca e live: in acest mediu verificam pe localhost; deploy-ul de productie il face fondatorul.
