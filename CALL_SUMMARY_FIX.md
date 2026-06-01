# Rezolvare „rezumatul apelului nu merge" — diagnostic + fix (ședință agenți + audit)

## De ce NU mergea (diagnostic real, din cod + capturi)
1. **Cache / versiune veche** — userul rula o build veche (scria „Transcriu live", buton „Stop"), nu fix-ul nou.
2. **Bug de logică (cauza principală):** pe iPhone, Web Speech live produce text-gunoi parțial (ex. „Păi în
   fiecare an când a rpd"). Codul păstra transcrierea live dacă avea >20 caractere -> **bloca transcrierea
   bună prin AI**. Gunoiul „câștiga".
3. **Lipsă backend AI pentru transcriere:** pe iPhone transcrierea se face DOAR prin AI (Web Speech e inutil).
   Dacă userul n-a configurat un furnizor care acceptă audio (OpenAI/Gemini/Standard-prin-releu), nu avea cum
   să transcrie. „Standard" cere releu deployat cu AI_KEY; „Local" nu merge pe telefon.
4. **Anularea ecoului** (reparată anterior, v3.1) ștergea vocea celuilalt din difuzor.

## Fix-uri aplicate (v3.2) — verificate e2e pe localhost
- **AI = sursa de adevăr:** la Stop, dacă există audio + asistent AI care acceptă audio, transcriem prin AI și
  **înlocuim** transcrierea live (gunoiul iOS). Gate-ul „>20 caractere" eliminat. (Verificat: gunoiul e înlocuit.)
- **Transcriere prin GEMINI** adăugată (audio inline → generateContent). Gemini are **tier gratuit** -> cea mai
  accesibilă cale pe iPhone. (OpenAI Whisper rămâne cel mai tolerant la format; Standard-prin-releu pt. cei ce deployează.)
- **Pre-check vizibil:** dacă nu e configurat AI, reportofonul arată un avertisment clar („ai nevoie de
  OpenAI/Gemini/Standard, configurează la ⚙ Setări") — nu mai înregistrezi „în gol".
- **Audio aruncat garantat** (finally) + timeout de rețea (nu atârnă) + indicator de versiune **v3.2**.

## Ce trebuie să facă userul ca să MEARGĂ (onest)
Transcrierea pe iPhone cere un AI care acceptă audio. Cea mai simplă cale GRATUITĂ:
1. Ia o cheie gratuită Google AI Studio (aistudio.google.com).
2. Secretara → Asistent AI → ⚙ Setări → Furnizor = **Google Gemini** → pune cheia → Salvează → Testează.
3. Apel pe **difuzor**, Cercul deschis (v3.2), **● Înregistrează** → **Stop și rezumă**.
(Notă: Gemini poate refuza unele formate audio de pe iPhone; dacă dă eroare de format, folosește OpenAI sau Standard.)

## Limită de OS (nenegociabilă)
Pe un singur telefon, în timpul apelului real, iOS poate suspenda microfonul browserului când treci în
aplicația de apel. Cel mai sigur: difuzor + Cercul deschis pe ecran, sau un al 2-lea dispozitiv.
