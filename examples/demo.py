"""Demo: sistemul multi-agent Agentap în acțiune.

Rulează:
    pip install -r requirements.txt
    cp .env.example .env   # și completează ANTHROPIC_API_KEY
    python examples/demo.py

Coordonatorul primește o cerere, o descompune și deleagă către agenții
specializați (cercetare / cod / redactare), apoi sintetizează răspunsul.
"""

from __future__ import annotations

import os
import sys
from typing import Any

# Permite rularea directa din orice director.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

from agentap import build_team


def log_event(event: str, payload: dict[str, Any]) -> None:
    """Afișează frumos ce se întâmplă în culise (cine deleagă, cine apelează unelte)."""
    agent = payload.get("agent", "?")
    if event == "agent_start":
        print(f"  ▶ [{agent}] pornește: {payload['task'][:80]}")
    elif event == "tool_call":
        print(f"    🔧 [{agent}] apelează {payload['tool']}")
    elif event == "agent_done":
        print(f"  ✓ [{agent}] gata")


def main() -> None:
    load_dotenv()

    # Cererea poate veni din linia de comandă, altfel folosim un exemplu implicit.
    request = " ".join(sys.argv[1:]) or (
        "Calculează al 20-lea număr Fibonacci rulând cod, apoi scrie un paragraf "
        "scurt și prietenos care explică ce este șirul lui Fibonacci."
    )

    print("=" * 70)
    print(f"CERERE: {request}")
    print("=" * 70)

    team = build_team(on_event=log_event)
    answer = team.run(request)

    print("\n" + "=" * 70)
    print("RĂSPUNS FINAL:")
    print("=" * 70)
    print(answer)

    usage = team.total_usage()
    print("\n" + "-" * 70)
    print(
        f"Tokeni — input: {usage['input']:,} | output: {usage['output']:,} | "
        f"cache citit: {usage['cache_read']:,} | cache scris: {usage['cache_write']:,}"
    )


if __name__ == "__main__":
    main()
