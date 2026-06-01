# AI_CHAT_DESIGN — Asistent AI în Secretara (analiză + decizie)

Cerință: chat cu AI în Secretara — fie un model standard (ex. Ollama local), fie fiecare utilizator își
conectează propriul ChatGPT / Claude / alt model. Analiză din toate unghiurile, apoi integrare. Nimic nu
trece fără poarta de audit.

## Tensiunea centrală
Aplicația e privacy-first (Local-Only implicit, E2EE, CSP `connect-src` restrâns). Un chat AI înseamnă, în
cazul cloud, că textul conversației PLEACĂ la un furnizor (OpenAI/Anthropic/Google). Asta trebuie să fie
**opt-in, transparent, cu etichetă clară per furnizor** — niciodată implicit, niciodată ascuns.

## Opțiuni analizate
1. **Local (Ollama / LM Studio / orice endpoint OpenAI-compatibil pe localhost)** — RECOMANDAT.
   - Datele NU pleacă de pe mașina utilizatorului. 100% pe linia de confidențialitate a produsului.
   - Necesită ca userul să ruleze Ollama (`http://localhost:11434`) cu `OLLAMA_ORIGINS` permisiv pt. browser.
   - CSP: `connect-src` permite deja `http://localhost:*`.
2. **Cloud cu CHEIA TA (BYOK): OpenAI / Anthropic / Gemini / OpenRouter / orice OpenAI-compat.**
   - Userul își pune propria cheie (stocată criptat local, nu pleacă la noi). Conversația pleacă la furnizor.
   - Realități CORS din browser: OpenAI și Gemini permit apeluri din browser; Anthropic cere header
     `anthropic-dangerous-direct-browser-access: true`; OpenRouter e prietenos cu browserul. Endpoint-urile
     locale (Ollama/LM Studio) merg dacă au CORS activat.
   - CSP: adăugăm originile cunoscute (api.openai.com, api.anthropic.com, generativelanguage.googleapis.com,
     openrouter.ai). Self-host: userul își adaugă originea.
3. **Prin releu (proxy央centralizat)** — RESPINS: releul ar vedea prompturile -> rupe modelul zero-knowledge.

## Decizie
**Sistem de furnizor PLUGABIL, opt-in, local-first**, cu 3 adaptoare:
- `openai-compat` (acoperă Ollama, LM Studio, OpenRouter, OpenAI, Groq, Together…): POST `{base}/chat/completions`.
- `anthropic`: POST `api.anthropic.com/v1/messages` (+ header direct-browser).
- `gemini`: POST `generativelanguage.googleapis.com/.../generateContent?key=`.
Implicit: **Local (Ollama)**. Etichetă de confidențialitate per mod (local = privat; cloud = pleacă la furnizor).

## Confidențialitate & securitate (reguli)
- Opt-in explicit; implicit DEZACTIVAT. Cheia stocată DOAR local, în DB-ul criptat (AES-GCM), niciodată trimisă la releu/noi.
- Context: trimitem la model DOAR conversația + un system prompt; includerea datelor locale (task-uri/note) e
  un toggle explicit, nu implicit. Nu trimitem niciodată „ce caut"/contacte fără acțiunea userului.
- Etichetă vizibilă: „Local — rămâne pe dispozitiv" vs „Cloud — conversația pleacă la <furnizor> cu cheia ta".
- CSP: `connect-src` extins STRICT la originile AI cunoscute + localhost; nimic altceva.
- Randare mesaje prin `textContent` (pre-wrap) — fără `innerHTML`/markdown-HTML -> Trusted Types intact.

## Livrare
- Setări AI (mod/furnizor/base/cheie/model) în Secretara.
- Panou de chat în Secretara: listă mesaje + input + trimite + indicator „scrie…". Istoric local (DB.aichat).
- Verificare end-to-end pe localhost cu un mock OpenAI-compatibil (furnizorii cloud nu sunt accesibili din sandbox).
- Poartă de audit: APROBAT obligatoriu înainte de a fi considerat gata.
