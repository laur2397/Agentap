"""Echipa de build — agenti care chiar SCRIU codul aplicatiei.

Pipeline:
    Arhitect  -> proiecteaza structura de fisiere si deciziile tehnice (text)
    Programator -> implementeaza fiecare fisier folosind unealta scrie_fisier
    Reviewer  -> citeste codul scris si raporteaza ce ar imbunatati

Spre deosebire de firma consultativa (care produce un plan), aceasta echipa
produce un PROTOTIP REAL pe disc, intr-un workspace.

ATENTIE: rularea face apeluri la API (necesita ANTHROPIC_API_KEY) si poate dura
si consuma tokeni — agentii scriu cod efectiv.
"""

from __future__ import annotations

import os
from typing import Any, Callable

import anthropic

from .base import DEFAULT_MODEL, Agent
from .proiect import brief_text
from .tools_fs import file_tools, list_workspace

_ARHITECT = (
    "Ești arhitect software. Proiectezi prototipuri minimale dar funcționale.\n"
    "Pentru brief-ul primit, propui o structură de fișiere pentru un prototip v1 "
    "RULABIL și SIMPLU (preferă un singur backend + o interfață web statică, fără "
    "framework-uri grele). Pentru fiecare fișier dai: calea, rolul și ce conține pe scurt. "
    "Alegi un stack ușor de rulat local (ex: Python stdlib/Flask + HTML/CSS/JS simplu). "
    "Nu scrii cod aici — doar planul de fișiere."
)

_PROGRAMATOR = (
    "Ești programator full-stack. Implementezi un prototip v1 RULABIL scriind fișiere reale "
    "cu unealta `scrie_fisier`.\n\n"
    "Reguli:\n"
    "- Scrie fiecare fișier complet (cod care chiar rulează), prin `scrie_fisier`.\n"
    "- Preferă simplitatea: cât mai puține dependențe, ușor de pornit local.\n"
    "- Include un README scurt cu pașii de rulare.\n"
    "- Acoperă funcționalitățile cheie din brief, la nivel de prototip (nu producție).\n"
    "- După ce ai scris tot, folosește `listeaza_fisiere` și confirmă pe scurt ce ai construit.\n"
    "Nu cere voie — construiește direct."
)

_REVIEWER = (
    "Ești code reviewer. Primești lista de fișiere și poți citi oricare cu `citeste_fisier`.\n"
    "Verifici dacă prototipul e coerent și rulabil. Raportezi concis: ce e bine, ce lipsește, "
    "ce ai schimba (max 8 puncte). Nu rescrii codul, doar evaluezi."
)


def build_app(
    *,
    workspace: str = "workspace",
    brief: str | None = None,
    client: anthropic.Anthropic | None = None,
    model: str = DEFAULT_MODEL,
    review: bool = True,
    on_event: Callable[[str, dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Pune o echipă de agenți să scrie un prototip real al aplicației pe disc.

    Args:
        workspace: Directorul unde se scrie codul.
        brief: Brief-ul de produs (implicit: cel din `proiect.py`).
        client: Client Anthropic partajat (creat automat dacă lipsește).
        model: Modelul agenților.
        review: Dacă rulează și pasul de review.
        on_event: Callback de observabilitate (tool_call etc.).

    Returnează: {"plan", "implementare", "review", "fisiere": [...], "workspace"}.
    """
    client = client or anthropic.Anthropic()
    brief = brief or brief_text()
    fs = file_tools(workspace)

    arhitect = Agent("architect", _ARHITECT, model=model, effort="high", client=client, on_event=on_event)
    programator = Agent(
        "programator", _PROGRAMATOR, tools=fs, model=model, effort="high",
        max_tokens=16000, client=client, on_event=on_event,
    )

    plan = arhitect.run(
        f"{brief}\n\nProiectează structura de fișiere pentru un prototip v1 rulabil al acestei aplicații."
    )
    implementare = programator.run(
        f"{brief}\n\nPlan arhitectural propus:\n{plan}\n\n"
        f"Implementează prototipul v1 în workspace, scriind fiecare fișier cu `scrie_fisier`."
    )

    review_txt = ""
    if review:
        reviewer = Agent("reviewer", _REVIEWER, tools=fs, model=model, effort="medium", client=client, on_event=on_event)
        fisiere = list_workspace(workspace)
        review_txt = reviewer.run(
            "Fișiere scrise:\n" + "\n".join(fisiere) + "\n\nEvaluează prototipul (citește ce ai nevoie)."
        )

    return {
        "plan": plan,
        "implementare": implementare,
        "review": review_txt,
        "fisiere": list_workspace(workspace),
        "workspace": os.path.abspath(workspace),
    }
