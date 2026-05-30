# 🤖 Agentap

Un mic framework **multi-agent** educativ, construit peste [Claude API](https://docs.claude.com/),
care demonstrează pattern-ul **orchestrator → workers**: un agent coordonator
descompune o cerere și o deleagă unor agenți specializați, apoi sintetizează
rezultatele.

> Proiect în scop **educativ** — pentru cercetare pe tema AI și a agenților AI.

## Arhitectură

```
        ┌──────────────┐
        │ Orchestrator │  ← planifică & deleagă
        └──────┬───────┘
               │  unelte „delegate_to_*”
   ┌───────────┼────────────┐
   ▼           ▼            ▼
┌────────┐ ┌────────┐ ┌────────┐
│research│ │ coder  │ │ writer │   ← agenți specializați (workers)
│web срч.│ │cod exec│ │  text  │
└────────┘ └────────┘ └────────┘
```

- **`Agent`** (`agentap/base.py`) — buclă agentică peste Messages API, cu
  *prompt caching*, *adaptive thinking* și *tool use* (manual loop).
- **`Tool` / `@tool`** (`agentap/tools.py`) — definește unelte din funcții Python;
  schema se deduce din type hints.
- **`Orchestrator`** (`agentap/orchestrator.py`) — împachetează fiecare worker
  ca unealtă de delegare pentru coordonator.
- **`build_team`** (`agentap/team.py`) — echipa implicită: cercetare / cod / redactare.

## Concepte Claude API folosite

| Concept | Unde | De ce |
|---|---|---|
| Tool use (manual loop) | `base.py` | Control fin: logging, uzaj, limită de iterații |
| Prompt caching | `base.py` (`cache_control` pe system) | System prompt înghețat → reducere de cost |
| Adaptive thinking + `effort` | `base.py` | Raționament reglat pe complexitate |
| Unelte server-side (`web_search`, `code_execution`) | `team.py` | Rulează pe infra Anthropic, fără cod de tool |
| Model `claude-opus-4-8` | `base.py` | Cel mai capabil model |

## Instalare & rulare

```bash
pip install -r requirements.txt
cp .env.example .env          # completează ANTHROPIC_API_KEY
python examples/demo.py
```

Sau cu cererea ta:

```bash
python examples/demo.py "Caută cele mai noi modele Claude și fă-mi un rezumat."
```

## Exemplu de cod

```python
from agentap import build_team

team = build_team()
raspuns = team.run("Calculează 20! rulând cod și explică ce e factorialul.")
print(raspuns)
```

## 🏢 Firmă simulată de agenți (CEO → departamente → angajați)

Pe lângă echipa de bază, Agentap conține o **organizație IT completă simulată**:
**18 departamente, 220 de angajați**, fiecare cu propriul agent AI, organizați
într-o ierarhie pe trei niveluri (**239 de agenți** în total). Mediu pur
**educativ**, pentru cercetare pe sisteme multi-agent.

```python
from agentap import build_company

firma = build_company()
print(firma.headcount, "angajați,", firma.n_agenti, "agenți")

# Cerere către întreaga firmă (CEO-ul deleagă pe departamente, care deleagă pe roluri)
print(firma.run("Vrem să lansăm o funcție de notificări. Cum procedăm?"))

# Vorbește direct cu un angajat
hai = firma.employee("AI", "Head of AI")
print(hai.run("Care e strategia noastră AI?"))

# Trimite o sarcină unui departament întreg
print(firma.department("Securitate").run("Faceți un checklist de securitate pentru lansare."))
```

Datele organizației trăiesc în `agentap/organizatie.py` (modul **pur**, fără API —
poți inspecta structura fără cheie):

```bash
python -m agentap.organizatie   # afișează toate departamentele și rolurile
python examples/firma_demo.py    # rulează firma vie (necesită ANTHROPIC_API_KEY)
```

| Componentă | Unde | Rol |
|---|---|---|
| `ORGANIZATIE` | `organizatie.py` | Datele: 18 departamente, roluri, descrieri |
| `Employee` | `company.py` | Un agent per angajat, cu prompt de rol |
| `Department` | `company.py` | Manager-agent + delegare pe roluri |
| `Company` / `build_company` | `company.py` | CEO + toate departamentele |

## Extindere

Adaugă un worker nou:

```python
from agentap import Agent, Orchestrator

analyst = Agent(
    name="analyst",
    system="Ești un analist de date. Interpretezi cifre și tendințe.",
    effort="high",
)
team = Orchestrator(workers=[analyst, ...])
```

Sau o unealtă proprie:

```python
from agentap import tool

@tool
def get_weather(city: str) -> str:
    "Întoarce vremea curentă pentru un oraș."
    return f"Senin în {city}."
```
