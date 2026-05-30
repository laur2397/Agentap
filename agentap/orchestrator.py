"""Orchestrator — coordonatorul sistemului multi-agent.

Pattern: *orchestrator → workers*. Coordonatorul nu rezolvă singur sarcina; el
o descompune și deleagă fiecare bucată unui agent specializat. Fiecare subagent
este expus coordonatorului ca o *unealtă* `delegate_to_<nume>`: când coordonatorul
o apelează, rulăm subagentul respectiv și îi întoarcem rezultatul.

Astfel, întreaga inteligență de planificare/delegare trăiește în system prompt-ul
coordonatorului, iar fiecare worker rămâne focalizat pe domeniul lui.
"""

from __future__ import annotations

from typing import Any, Callable

import anthropic

from .base import DEFAULT_MODEL, Agent
from .tools import Tool

_COORDINATOR_SYSTEM = """\
Ești coordonatorul unei echipe de agenți AI specializați. Nu rezolvi sarcinile
singur — le descompui și delegi fiecare parte agentului potrivit, folosind
uneltele `delegate_to_*`.

Principii:
- Analizează cererea și fă un plan scurt înainte de a delega.
- Deleagă o instrucțiune clară și autonomă fiecărui agent (el nu vede
  conversația ta, doar textul pe care i-l trimiți).
- Poți delega de mai multe ori și poți combina rezultatele.
- La final, sintetizează rezultatele într-un răspuns coerent pentru utilizator.
- Folosește un agent doar când chiar aduce valoare; pentru lucruri triviale,
  răspunde direct.
"""


def _make_delegation_tool(agent: Agent) -> Tool:
    """Împachetează un subagent ca unealtă `delegate_to_<nume>`."""

    def _delegate(task: str) -> str:
        return agent.run(task)

    description = (
        f"Deleagă o sarcină agentului '{agent.name}'. "
        f"Trimite o instrucțiune completă și autonomă în câmpul `task`. "
        f"Specializare: {agent.system.strip().splitlines()[0]}"
    )

    return Tool(
        name=f"delegate_to_{agent.name}",
        description=description,
        func=_delegate,
        input_schema={
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "Instrucțiunea autonomă pentru agent.",
                }
            },
            "required": ["task"],
        },
    )


class Orchestrator:
    """Coordonează o echipă de agenți specializați.

    Args:
        workers: Lista de agenți specializați.
        model: Modelul pentru coordonator (default: cel mai capabil).
        client: Client Anthropic partajat (creat automat dacă lipsește).
        on_event: Callback de observabilitate, propagat la toți agenții.
    """

    def __init__(
        self,
        workers: list[Agent],
        *,
        model: str = DEFAULT_MODEL,
        client: anthropic.Anthropic | None = None,
        on_event: Callable[[str, dict[str, Any]], None] | None = None,
    ) -> None:
        self.client = client or anthropic.Anthropic()
        self.workers = workers

        # Asigură-te că workerii partajează clientul și callback-ul de evenimente.
        for w in workers:
            w.client = self.client
            if on_event and w.on_event is None:
                w.on_event = on_event

        self.coordinator = Agent(
            name="coordinator",
            system=_COORDINATOR_SYSTEM,
            tools=[_make_delegation_tool(w) for w in workers],
            model=model,
            effort="high",
            client=self.client,
            on_event=on_event,
        )

    def run(self, request: str) -> str:
        """Rulează o cerere de la cap la coadă și întoarce răspunsul final."""
        return self.coordinator.run(request)

    def total_usage(self) -> dict[str, int]:
        """Uzajul de tokeni cumulat: coordonator + toți workerii."""
        total = dict(self.coordinator.usage)
        for w in self.workers:
            for k, v in w.usage.items():
                total[k] += v
        return total
