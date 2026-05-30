"""Construieste o *firma simulata* de agenti AI din structura organizationala.

Ierarhie pe trei niveluri (simulare educativa):

    CEO (coordonator general)
      └─ deleaga catre 18 manageri de departament
           └─ fiecare deleaga catre rolurile din echipa
                └─ un Agent pentru *fiecare angajat*

Fiecare angajat este un `Agent` cu un system prompt croit pe rolul si
responsabilitatea lui. Fiecare departament si CEO-ul sunt agenti-coordonatori
care deleaga prin unelte `to_*`.

Constructia este ieftina (doar obiecte Python); apelurile catre API au loc abia
cand rulezi `company.run(...)`, `department.run(...)` sau `employee.run(...)`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable

import anthropic

from .base import DEFAULT_MODEL, Agent
from .organizatie import ORGANIZATIE, nume_curat, total_general
from .tools import Tool

# Folosirea diacriticelor romanesti -> ASCII, pentru nume de unelte valide.
_DIACRITICE = str.maketrans(
    {
        "ă": "a", "â": "a", "î": "i", "ș": "s", "ş": "s", "ț": "t", "ţ": "t",
        "Ă": "A", "Â": "A", "Î": "I", "Ș": "S", "Ş": "S", "Ț": "T", "Ţ": "T",
    }
)


def slug(text: str, maxlen: int = 60) -> str:
    """Transforma un text in identificator valid de unealta: [a-z0-9_], <= maxlen."""
    s = text.translate(_DIACRITICE).lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s[:maxlen] or "x"


# --------------------------------------------------------------------------- #
# Prompturi
# --------------------------------------------------------------------------- #
def _prompt_angajat(departament: str, rol: str, descriere: str) -> str:
    dep = nume_curat(departament)
    return (
        f"Ești „{rol}”, angajat în departamentul „{dep}” al unei firme IT care "
        f"dezvoltă o aplicație mobilă. (Mediu SIMULAT, în scop educativ.)\n\n"
        f"Responsabilitatea ta principală: {descriere}\n\n"
        "Cum lucrezi:\n"
        "- Răspunzi din perspectiva și expertiza rolului tău; rămâi în aria ta de competență.\n"
        "- Ești colegial și profesionist; când o sarcină iese din rolul tău, spui clar "
        "ce coleg/departament ar trebui implicat.\n"
        "- Oferi răspunsuri concrete, utile și concise.\n"
        "- Nu iei decizii reale de business și nu inventezi date confidențiale; este o simulare."
    )


def _prompt_manager(departament: str, intro: str, roluri_txt: str) -> str:
    dep = nume_curat(departament)
    return (
        f"Ești managerul departamentului „{dep}” dintr-o firmă IT simulată (educativ).\n\n"
        f"Despre departament: {intro}\n\n"
        f"Echipa ta (roluri disponibile pentru delegare):\n{roluri_txt}\n\n"
        "Cum lucrezi:\n"
        "- Primești o sarcină, o descompui și o delegi rolului potrivit prin uneltele `to_*`.\n"
        "- Trimite fiecărui rol o instrucțiune clară și autonomă (angajatul nu vede "
        "conversația ta, doar textul `task`).\n"
        "- Poți delega de mai multe ori și poți combina rezultatele.\n"
        "- La final, sintetizezi un răspuns coerent din partea departamentului."
    )


_PROMPT_CEO = (
    "Ești directorul general (CEO) al unei firme IT simulate care dezvoltă o "
    "aplicație mobilă. (Mediu educativ.)\n\n"
    "Coordonezi {n} departamente, fiecare cu propriul manager. Primești o cerere, "
    "identifici departamentele relevante și le delegi prin uneltele `to_*`.\n\n"
    "Cum lucrezi:\n"
    "- Gândește scurt ce departamente sunt implicate înainte de a delega.\n"
    "- Trimite fiecărui departament o instrucțiune clară și autonomă.\n"
    "- Pentru cereri cross-funcționale, deleagă mai multor departamente și "
    "integrează rezultatele.\n"
    "- La final, oferi un răspuns executiv, coerent și acționabil."
)


# --------------------------------------------------------------------------- #
# Modele de date
# --------------------------------------------------------------------------- #
@dataclass
class Employee:
    """Un angajat = un agent leaf cu identitate de rol."""

    departament: str
    rol: str
    index: int
    descriere: str
    agent: Agent

    @property
    def eticheta(self) -> str:
        return f"{self.rol} #{self.index}"

    def run(self, task: str) -> str:
        """Întreabă direct acest angajat."""
        return self.agent.run(task)


@dataclass
class Department:
    """Un departament = un manager-agent + angajații lui, grupați pe rol."""

    nume: str
    intro: str
    manager: Agent
    employees: list[Employee] = field(default_factory=list)
    by_role: dict[str, list[Employee]] = field(default_factory=dict)

    def run(self, task: str) -> str:
        """Trimite o sarcină managerului de departament (care deleagă mai departe)."""
        return self.manager.run(task)

    @property
    def headcount(self) -> int:
        return len(self.employees)


# --------------------------------------------------------------------------- #
# Constructie
# --------------------------------------------------------------------------- #
def _delegate_tool(name: str, descriere: str, runner: Callable[[str], str]) -> Tool:
    """Construieste o unealta de delegare cu un singur argument `task`."""
    return Tool(
        name=name,
        description=descriere,
        func=lambda task: runner(task),
        input_schema={
            "type": "object",
            "properties": {
                "task": {"type": "string", "description": "Instrucțiune autonomă pentru țintă."}
            },
            "required": ["task"],
        },
    )


def _build_department(
    nume: str,
    data: dict[str, Any],
    *,
    client: anthropic.Anthropic,
    model: str,
    employee_effort: str,
    manager_effort: str,
    on_event: Callable[[str, dict[str, Any]], None] | None,
) -> Department:
    employees: list[Employee] = []
    by_role: dict[str, list[Employee]] = {}

    # 1. Un agent pentru fiecare angajat.
    for rol, nr, descriere in data["roluri"]:
        for i in range(1, nr + 1):
            agent = Agent(
                name=f"{rol} #{i}" if nr > 1 else rol,
                system=_prompt_angajat(nume, rol, descriere),
                model=model,
                effort=employee_effort,
                client=client,
                on_event=on_event,
            )
            emp = Employee(nume, rol, i, descriere, agent)
            employees.append(emp)
            by_role.setdefault(rol, []).append(emp)

    # 2. Unelte de delegare pe rol (round-robin peste angajații rolului).
    contoare: dict[str, int] = {}
    roluri_txt_linii: list[str] = []
    tools: list[Tool] = []
    nume_folosite: set[str] = set()

    for rol, nr, descriere in data["roluri"]:
        baza = f"to_{slug(rol)}"
        tool_name = baza
        k = 2
        while tool_name in nume_folosite:  # garanteaza unicitatea
            tool_name = f"{baza}_{k}"
            k += 1
        nume_folosite.add(tool_name)

        def runner(task: str, _rol: str = rol) -> str:
            lista = by_role[_rol]
            idx = contoare.get(_rol, 0) % len(lista)
            contoare[_rol] = idx + 1
            return lista[idx].run(task)

        descriere_tool = f"Deleagă către rolul „{rol}” ({nr}x). {descriere}"
        tools.append(_delegate_tool(tool_name, descriere_tool, runner))
        roluri_txt_linii.append(f"- {rol} ({nr}x) → unealta `{tool_name}`")

    manager = Agent(
        name=f"manager:{slug(nume)}",
        system=_prompt_manager(nume, data["intro"], "\n".join(roluri_txt_linii)),
        tools=tools,
        model=model,
        effort=manager_effort,
        client=client,
        on_event=on_event,
    )

    dep = Department(nume=nume, intro=data["intro"], manager=manager, employees=employees, by_role=by_role)
    return dep


class Company:
    """Firma simulata: CEO + departamente + angajati, toti agenti AI."""

    def __init__(
        self,
        departments: dict[str, Department],
        ceo: Agent,
    ) -> None:
        self.departments = departments
        self.ceo = ceo

    # -- interactiune --------------------------------------------------- #
    def run(self, request: str) -> str:
        """Trimite o cerere CEO-ului, care deleagă pe departamente."""
        return self.ceo.run(request)

    def department(self, nume_partial: str) -> Department:
        """Găsește un departament după nume (parțial), preferând potriviri pe cuvânt întreg.

        Ranking: nume curat identic > potrivire pe cuvânt întreg > substring.
        Astfel `department('AI')` găsește departamentul „Artificial Intelligence”,
        nu „Date, AI si Analytics”.
        """
        cheie = nume_partial.lower().strip()
        candidați: list[tuple[int, int, int, Department]] = []
        for nume, dep in self.departments.items():
            curat = nume_curat(nume).lower()
            cuvinte = re.findall(r"[a-z0-9]+", curat)
            if cheie == curat:
                scor = 0  # potrivire exactă pe numele curat
            elif cheie in cuvinte:
                scor = 1  # cuvânt întreg
            elif cheie in nume.lower():
                scor = 2  # substring oriunde
            else:
                continue
            # Departajare: nume mai specific (mai puține cuvinte), apoi mai scurt.
            candidați.append((scor, len(cuvinte), len(nume), dep))

        if not candidați:
            raise KeyError(f"Niciun departament nu se potrivește cu {nume_partial!r}")
        candidați.sort(key=lambda c: c[:3])
        return candidați[0][3]

    def employee(self, departament: str, rol: str, index: int = 1) -> Employee:
        """Găsește un angajat specific (departament parțial + rol parțial)."""
        dep = self.department(departament)
        for emp in dep.employees:
            if rol.lower() in emp.rol.lower() and emp.index == index:
                return emp
        raise KeyError(f"Niciun angajat {rol!r} #{index} în {departament!r}")

    # -- statistici ----------------------------------------------------- #
    @property
    def headcount(self) -> int:
        return sum(d.headcount for d in self.departments.values())

    @property
    def n_agenti(self) -> int:
        """Total agenți instanțiați: angajați + manageri + CEO."""
        return self.headcount + len(self.departments) + 1

    def total_usage(self) -> dict[str, int]:
        """Uzaj de tokeni cumulat pe toți agenții firmei."""
        total = dict(self.ceo.usage)
        for dep in self.departments.values():
            for k, v in dep.manager.usage.items():
                total[k] += v
            for emp in dep.employees:
                for k, v in emp.agent.usage.items():
                    total[k] += v
        return total


def build_company(
    *,
    client: anthropic.Anthropic | None = None,
    model: str = DEFAULT_MODEL,
    employee_effort: str = "medium",
    manager_effort: str = "high",
    on_event: Callable[[str, dict[str, Any]], None] | None = None,
) -> Company:
    """Construiește firma completă din `ORGANIZATIE`.

    Args:
        client: Client Anthropic partajat (creat automat dacă lipsește).
        model: Modelul folosit de toți agenții.
        employee_effort: `effort` pentru agenții-angajați (leaf).
        manager_effort: `effort` pentru manageri și CEO.
        on_event: Callback de observabilitate, propagat la toți agenții.
    """
    client = client or anthropic.Anthropic()

    departments: dict[str, Department] = {}
    ceo_tools: list[Tool] = []
    nume_folosite: set[str] = set()

    for nume, data in ORGANIZATIE.items():
        dep = _build_department(
            nume,
            data,
            client=client,
            model=model,
            employee_effort=employee_effort,
            manager_effort=manager_effort,
            on_event=on_event,
        )
        departments[nume] = dep

        baza = f"to_{slug(nume_curat(nume))}"
        tool_name = baza
        k = 2
        while tool_name in nume_folosite:
            tool_name = f"{baza}_{k}"
            k += 1
        nume_folosite.add(tool_name)

        descriere_tool = f"Deleagă către departamentul „{nume_curat(nume)}”. {data['intro']}"
        ceo_tools.append(_delegate_tool(tool_name, descriere_tool, dep.run))

    ceo = Agent(
        name="CEO",
        system=_PROMPT_CEO.format(n=len(departments)),
        tools=ceo_tools,
        model=model,
        effort=manager_effort,
        client=client,
        on_event=on_event,
    )

    return Company(departments=departments, ceo=ceo)
