# AI 100% OFFLINE (fără cloud, fără cheie) — transcriere apel + rezumat

Aplicația poate face transcrierea apelului și rezumatul **complet local**, fără să trimită nimic în cloud.
Adevărul tehnic, pe scurt:
- **Ollama** rulează LLM-uri text → face **REZUMATUL** offline. **NU transcrie audio** (n-are speech-to-text).
- Pentru **TRANSCRIERE offline** ai nevoie de un **Whisper local** care expune un endpoint OpenAI-compatibil
  (`/v1/audio/transcriptions`): **LocalAI**, **whisper.cpp (server)** sau **faster-whisper-server**.

## ⚠ Unde merge offline
- **DA, pe un CALCULATOR** (laptop/desktop) unde rulezi serverul local. Verificat end-to-end.
- **NU pe telefon** direct din pagina HTTPS: browserul blochează apelurile către un server local prin HTTP
  (mixed content), iar pe telefon oricum nu rulează Ollama/LocalAI. (Offline pe telefon ar cere Whisper în
  browser — transformers.js/WASM — un pas viitor, mai greu; rupe modelul single-file/CSP strict.)

## Varianta cea mai simplă: LocalAI (face și transcriere, și rezumat)
LocalAI e un singur server, OpenAI-compatibil, care oferă atât Whisper cât și LLM-uri locale.

1. Instalează LocalAI (Docker, pe calculatorul tău):
   ```
   docker run -p 8080:8080 --name local-ai localai/localai:latest
   ```
   (sau vezi localai.io — alege un model Whisper + un model de chat, ex. `whisper-1` și un LLM mic)
2. Deschide aplicația **pe acel calculator**: `app/eie.html` (sau localhost) — ca să fie pe HTTP, fără mixed content.
3. În app: Secretara → Asistent AI → ⚙ Setări → Furnizor = **Endpoint OpenAI-compatibil (custom)** (sau **Local**)
   → Base URL = `http://localhost:8080/v1` → Model = numele modelului tău → **Salvează** → **Testează**.
4. Reportofon: ● Înregistrează → Stop și rezumă → transcriere + rezumat, **totul local**.

## Varianta Ollama (rezumat) + whisper.cpp (transcriere)
- **Ollama** pentru rezumat: instalează ollama, `ollama run llama3.1`, pornește cu `OLLAMA_ORIGINS='*'`.
  Base URL = `http://localhost:11434/v1`.
- **whisper.cpp** pentru transcriere: rulează server-ul whisper.cpp (expune `/v1/audio/transcriptions`).
- În app pui Base URL la serverul care are AMBELE (de aceea LocalAI e mai simplu — le are pe amândouă).

## De ce nu merge pe telefon (onest)
Pagina e servită pe **HTTPS** (github.io). Un browser refuză să cheme un server **HTTP** local (mixed content),
iar telefonul nu rulează Ollama/LocalAI. Soluții:
- Folosește aplicația **pe calculatorul** unde rulează serverul local (cel mai simplu).
- SAU servește și aplicația local pe HTTP, în aceeași rețea (avansat).
- Pe viitor: Whisper în browser (offline pe telefon) — îl putem aborda separat.
