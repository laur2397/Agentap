"""Smoke test — verifică viu că agenții firmei chiar răspund prin API.

Spre deosebire de verificarea structurală (care nu apelează API-ul), acest script
chiar pune câțiva agenți reprezentativi să lucreze și confirmă lanțul de delegare:

    1. un ANGAJAT răspunde direct (cel mai ieftin test)
    2. un DEPARTAMENT deleagă către un rol
    3. CEO-ul deleagă către un departament

Necesită `ANTHROPIC_API_KEY`. Rulează:
    python examples/smoke_test.py

Cod de ieșire: 0 = totul OK, 1 = ceva a eșuat. Bun de pus în CI.
"""

from __future__ import annotations

import os
import sys
from typing import Any

# Permite rularea directa din orice director.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

from agentap import build_company


def _nonempty(text: str) -> bool:
    return bool(text) and not text.startswith("[")


def main() -> int:
    load_dotenv()
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("⚠  Lipsește ANTHROPIC_API_KEY — nu pot rula testul viu.")
        print("   Pune cheia în .env (vezi .env.example) și reîncearcă.")
        return 1

    # Logăm fiecare delegare ca să se vadă lanțul.
    def log(event: str, payload: dict[str, Any]) -> None:
        if event == "tool_call":
            print(f"      [{payload['agent']}] → {payload['tool']}")

    co = build_company(on_event=log, employee_effort="low", manager_effort="medium")
    print(f"Firmă: {co.headcount} angajați, {co.n_agenti} agenți.\n")

    rezultate: list[tuple[str, bool]] = []

    # 1. Un angajat răspunde direct.
    print("1) Angajat direct — Head of AI:")
    emp = co.employee("AI", "Head of AI")
    r1 = emp.run("În maximum 2 propoziții, cu ce te ocupi?")
    print(f"   ↳ {r1[:160]}")
    rezultate.append(("angajat", _nonempty(r1)))

    # 2. Un departament deleagă către un rol.
    print("\n2) Departament — Securitate deleagă unui rol:")
    r2 = co.department("Securitate").run(
        "Cere unui specialist să dea 3 verificări rapide de securitate înainte de lansare."
    )
    print(f"   ↳ {r2[:160]}")
    rezultate.append(("departament", _nonempty(r2)))

    # 3. CEO-ul deleagă către un departament.
    print("\n3) CEO — deleagă către departamentul potrivit:")
    r3 = co.run("Pe scurt: ce departament se ocupă de optimizarea în App Store și ce ar face primul?")
    print(f"   ↳ {r3[:160]}")
    rezultate.append(("ceo", _nonempty(r3)))

    # Raport.
    print("\n" + "=" * 60)
    toate_ok = all(ok for _, ok in rezultate)
    for nume, ok in rezultate:
        print(f"  {'✓' if ok else '✗'} {nume}")
    u = co.total_usage()
    print(
        f"\nTokeni — input: {u['input']:,} | output: {u['output']:,} | "
        f"cache citit: {u['cache_read']:,}"
    )
    print("REZULTAT:", "TOTUL FUNCȚIONEAZĂ ✓" if toate_ok else "AU EȘUAT TESTE ✗")
    return 0 if toate_ok else 1


if __name__ == "__main__":
    sys.exit(main())
