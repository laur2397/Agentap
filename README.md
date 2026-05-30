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
