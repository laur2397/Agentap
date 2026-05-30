"""Unelte reale de fisiere — dau agentilor puterea sa SCRIE cod pe disc.

Spre deosebire de uneltele consultative, acestea au efect real: creeaza fisiere
intr-un director „workspace”. Sunt securizate (nu se poate scrie in afara
workspace-ului) ca un agent sa nu atinga restul sistemului.
"""

from __future__ import annotations

import os

from .tools import Tool, tool


def file_tools(workspace: str) -> list[Tool]:
    """Construieste setul de unelte de fisiere legat de un director workspace.

    Returneaza: [scrie_fisier, citeste_fisier, listeaza_fisiere].
    Toate caile sunt relative la workspace si nu pot iesi din el.
    """
    root = os.path.abspath(workspace)
    os.makedirs(root, exist_ok=True)

    def _safe(cale: str) -> str:
        full = os.path.abspath(os.path.join(root, cale))
        if full != root and not full.startswith(root + os.sep):
            raise ValueError(f"Cale interzisa (in afara workspace-ului): {cale}")
        return full

    @tool
    def scrie_fisier(cale: str, continut: str) -> str:
        """Scrie (sau suprascrie) un fisier text in workspace.

        Args:
            cale: Calea relativa a fisierului (ex: backend/app.py).
            continut: Continutul COMPLET al fisierului.
        """
        full = _safe(cale)
        os.makedirs(os.path.dirname(full) or root, exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(continut)
        return f"OK: am scris {cale} ({len(continut)} caractere)."

    @tool
    def citeste_fisier(cale: str) -> str:
        """Citeste un fisier existent din workspace.

        Args:
            cale: Calea relativa a fisierului.
        """
        full = _safe(cale)
        if not os.path.isfile(full):
            return f"Fisierul {cale} nu exista."
        with open(full, encoding="utf-8") as f:
            return f.read()

    @tool
    def listeaza_fisiere() -> str:
        """Listeaza toate fisierele scrise pana acum in workspace."""
        out: list[str] = []
        for dirpath, _, files in os.walk(root):
            for fn in files:
                out.append(os.path.relpath(os.path.join(dirpath, fn), root))
        return "\n".join(sorted(out)) or "(workspace gol)"

    return [scrie_fisier, citeste_fisier, listeaza_fisiere]


def list_workspace(workspace: str) -> list[str]:
    """Listeaza fisierele dintr-un workspace (helper, in afara agentilor)."""
    root = os.path.abspath(workspace)
    if not os.path.isdir(root):
        return []
    out: list[str] = []
    for dirpath, _, files in os.walk(root):
        for fn in files:
            out.append(os.path.relpath(os.path.join(dirpath, fn), root))
    return sorted(out)
