# CALL_RECORDER_DESIGN — Reportofon apel + rezumat AI (analiză + decizie)

Cerință: „ascultă apelurile când vreau eu (telefonic normal sau WhatsApp), înregistrează tot ce vorbim
(nu neapărat audio) și fă un rezumat de ambele părți."

## Limită tehnică REALĂ (onest, nenegociabil)
O aplicație web NU poate accesa fluxul unui apel telefonic GSM sau audio-ul altei aplicații (WhatsApp).
iOS și Android interzic asta la nivel de OS — nu există API de browser pentru așa ceva. Singura cale
fezabilă dintr-un browser este **captura prin microfon**, cu apelul pus pe **difuzor** (speaker), ca
microfonul să prindă ambele voci acustic.

## Ce livrăm (realist, util)
Un „Reportofon" în Secretara, pornit MANUAL de user:
1. **Consimțământ + difuzor**: confirmare că ai dreptul/acordul să înregistrezi (multe jurisdicții cer
   consimțământul ambelor părți) + îndemn să pui pe difuzor.
2. **Captură microfon** (getUserMedia + MediaRecorder), pornit/oprit de user.
3. **Transcriere în text** (nu păstrăm audio implicit):
   - LIVE: Web Speech API — merge pe Android/Chrome; pe iPhone Safari e instabil (etichetat onest).
   - ROBUST (cross-platform, incl. iPhone): la stop, trimitem audio-ul la transcriere AI (Whisper,
     endpoint OpenAI-compatibil) prin cheia ta sau prin releu (mod „Standard"). Audio-ul e folosit doar
     pentru transcriere, apoi aruncat (nu se stochează).
4. **Transcript editabil** (poți corecta).
5. **Rezumat AI** structurat (rezumat scurt, ce oferă/cere fiecare parte, decizii, pași următori) cu
   asistentul deja integrat → salvat ca **notiță în Jurnal** (#apel), opțional legat de un contact.

## Confidențialitate & etică
- 100% OPT-IN, pornit manual de fiecare dată. Nimic în fundal, niciodată automat.
- Transcrierea AI / live STT trimite audio/text la furnizor (etichetă clară). Local/offline STT de calitate
  nu e fezabil într-un single-file (modelele Whisper WASM au sute de MB).
- Avertisment legal vizibil despre consimțământul părților. Audio-ul nu se păstrează după transcriere.
- Randare prin textContent (fără innerHTML). CSP: transcrierea folosește originile AI deja permise + releul.

## Limitări declarate
- Calitatea transcrierii depinde de difuzor/zgomot/accent.
- Pe iPhone, transcrierea live nativă e slabă → recomandăm modul „înregistrează apoi transcrie cu AI".
- Nu garantăm captura ambelor părți dacă apelul nu e pe difuzor.

Poartă de audit (etică/confidențialitate/legal): APROBAT obligatoriu înainte de a fi considerat gata.
