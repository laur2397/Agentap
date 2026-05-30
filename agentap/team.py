"""Echipa implicită de agenți specializați.

Trei workeri care acoperă cazuri comune:
    - researcher: caută informații pe web (unealtă server-side `web_search`).
    - coder:      scrie și *rulează* cod (unealtă server-side `code_execution`).
    - writer:     redactează și structurează text (fără unelte — pură limbă).

Toți rulează la `effort` mai mic decât coordonatorul, fiind subagenți focalizați.
"""

from __future__ import annotations

from typing import Any, Callable

import anthropic

from .base import Agent
from .orchestrator import Orchestrator

# Unelte server-side Anthropic (rulează pe infrastructura Anthropic).
_WEB_SEARCH = {"type": "web_search_20260209", "name": "web_search"}
_CODE_EXEC = {"type": "code_execution_20260120", "name": "code_execution"}


def build_team(
    *,
    client: anthropic.Anthropic | None = None,
    on_event: Callable[[str, dict[str, Any]], None] | None = None,
) -> Orchestrator:
    """Construiește orchestratorul cu echipa implicită (cercetare/cod/redactare)."""
    client = client or anthropic.Anthropic()

    researcher = Agent(
        name="researcher",
        system=(
            "Ești un cercetător. Găsești informații actuale și de încredere pe web.\n"
            "Folosește căutarea web pentru fapte recente sau verificabile. Citează "
            "sursele și distinge clar între fapt confirmat și speculație."
        ),
        server_tools=[_WEB_SEARCH],
        effort="medium",
        client=client,
    )

    coder = Agent(
        name="coder",
        system=(
            "Ești un inginer software. Scrii cod corect și îl *rulezi* pentru a-l "
            "verifica.\n"
            "Folosește execuția de cod pentru a testa ipoteze, a calcula rezultate "
            "și a valida soluții. Întoarce cod curat, cu explicații scurte."
        ),
        server_tools=[_CODE_EXEC],
        effort="high",
        client=client,
    )

    writer = Agent(
        name="writer",
        system=(
            "Ești un redactor. Transformi materialul brut într-un text clar, "
            "bine structurat și plăcut de citit.\n"
            "Adaptează tonul la cerință. Fii concis, folosește structură (titluri, "
            "liste) când ajută, și nu inventa fapte care nu ți-au fost date."
        ),
        effort="medium",
        client=client,
    )

    return Orchestrator(
        workers=[researcher, coder, writer],
        client=client,
        on_event=on_event,
    )
