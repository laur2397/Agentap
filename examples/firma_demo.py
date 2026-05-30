"""Demo: firma simulata de agenti AI (CEO -> departamente -> angajati).

Rulare:
    pip install -r requirements.txt
    cp .env.example .env        # completeaza ANTHROPIC_API_KEY
    python examples/firma_demo.py

    # cu o cerere proprie:
    python examples/firma_demo.py "Vrem sa lansam o functie de notificari. Ce facem?"

    # vorbeste direct cu un angajat:
    python examples/firma_demo.py --angajat "AI" "Head of AI" "Explica-mi strategia AI."
"""

from __future__ import annotations

import os
import sys
from typing import Any

# Permite rularea directa din orice director.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

from agentap import build_company
from agentap.organizatie import total_general


def log_event(event: str, payload: dict[str, Any]) -> None:
    """Afiseaza ierarhia de delegare in timp real."""
    agent = payload.get("agent", "?")
    if event == "tool_call":
        tinta = payload["tool"].replace("to_", "→ ")
        print(f"   [{agent}] deleaga {tinta}")


def main() -> None:
    load_dotenv()
    args = sys.argv[1:]

    company = build_company(on_event=log_event)
    print(
        f"Firma construita: {len(company.departments)} departamente, "
        f"{company.headcount} angajati, {company.n_agenti} agenti AI in total "
        f"(verificare date: {total_general()} angajati).\n"
    )

    # Mod: vorbeste direct cu un angajat.
    if args and args[0] == "--angajat":
        _, departament, rol, *rest = args
        intrebare = " ".join(rest) or "Prezinta-te si spune cu ce te ocupi."
        emp = company.employee(departament, rol)
        print(f"Intrebare catre {emp.eticheta} ({emp.departament}):\n")
        print(emp.run(intrebare))
        return

    # Mod: cerere catre intreaga firma (prin CEO).
    cerere = " ".join(args) or (
        "Vrem sa adaugam in aplicatie un asistent AI conversational, dar etic si "
        "fara mecanisme de dependenta. Cum abordam, ce departamente implicam si "
        "care sunt primii pasi?"
    )

    print("=" * 70)
    print(f"CERERE CATRE CEO: {cerere}")
    print("=" * 70)

    raspuns = company.run(cerere)

    print("\n" + "=" * 70)
    print("RASPUNS:")
    print("=" * 70)
    print(raspuns)

    u = company.total_usage()
    print("\n" + "-" * 70)
    print(
        f"Tokeni — input: {u['input']:,} | output: {u['output']:,} | "
        f"cache citit: {u['cache_read']:,} | cache scris: {u['cache_write']:,}"
    )


if __name__ == "__main__":
    main()
