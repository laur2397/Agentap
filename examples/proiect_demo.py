"""Demo: toata firma de agenti lucreaza la PROIECTUL real.

Proiect: „Memorie colectiva si potriviri pentru un cerc de business”.

Implicit ruleaza un DRY-RUN (fara API): arata exact ce agenti ar fi implicati
si cati. Cu `--live` (si o cheie ANTHROPIC_API_KEY) pune firma sa lucreze efectiv:
fiecare angajat contribuie -> managerii sintetizeaza -> CEO-ul livreaza planul.

Rulare:
    python examples/proiect_demo.py                 # dry-run (gratis), mode=everyone
    python examples/proiect_demo.py --mode departments
    python examples/proiect_demo.py --live          # rulare reala (costa tokeni!)
    python examples/proiect_demo.py --live --mode departments
"""

from __future__ import annotations

import os
import sys
from typing import Any

# Permite rularea directa (python examples/proiect_demo.py) din orice director.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

from agentap import brief_text, build_company


def _arg(flag: str, default: str) -> str:
    if flag in sys.argv:
        i = sys.argv.index(flag)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default


def dry_run(mode: str) -> None:
    """Construieste firma si arata planul de implicare, fara apeluri API."""
    co = build_company()
    plan = co.project_plan(mode=mode)

    print("=" * 70)
    print("DRY-RUN — cine ar lucra la proiect (fara apeluri API)")
    print(f"Mod: {mode}")
    print("=" * 70)
    for nume, info in plan["departamente"].items():
        membri = info["membri"]
        eticheta = "angajati" if mode == "everyone" else "roluri"
        print(f"\n{nume}")
        print(f"   manager: {info['manager']}  |  {len(membri)} {eticheta}")
        print("   " + ", ".join(membri[:6]) + (" ..." if len(membri) > 6 else ""))

    print("\n" + "=" * 70)
    print(f"CEO: {plan['ceo']}")
    print(f"AGENTI IMPLICATI: {plan['agenti_implicati']}")
    print("=" * 70)
    if mode == "everyone":
        print("(mode=everyone => toti agentii firmei contribuie)")
    print("\nPentru rulare reala: adauga --live (necesita ANTHROPIC_API_KEY).")


def live_run(mode: str) -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("⚠  Lipseste ANTHROPIC_API_KEY — nu pot rula --live. Vezi .env.example.")
        sys.exit(1)

    def progres(event: str, payload: dict[str, Any]) -> None:
        if event == "dept_start":
            print(f"\n▶ [{payload['i']}/{payload['din']}] {payload['departament']}")
        elif event == "angajat":
            print(f"   · {payload['eticheta']} ({payload['j']}/{payload['din']})")
        elif event == "dept_done":
            print(f"   ✓ poziție de departament gata")
        elif event == "ceo_start":
            print("\n👔 CEO consolidează planul final...")

    co = build_company(on_progress=progres, employee_effort="low", manager_effort="medium")
    print(f"Firma: {co.headcount} angajati, {co.n_agenti} agenti. Mod: {mode}\n")
    print("ATENTIE: mode=everyone face ~239 apeluri API. Foloseste --mode departments pentru un test mai ieftin.\n")

    rezultat = co.run_project(brief_text(), mode=mode, on_progress=progres)

    print("\n" + "=" * 70)
    print("PLAN EXECUTIV CONSOLIDAT (CEO):")
    print("=" * 70)
    print(rezultat["plan"])

    u = rezultat["usage"]
    print("\n" + "-" * 70)
    print(
        f"Tokeni — input: {u['input']:,} | output: {u['output']:,} | "
        f"cache citit: {u['cache_read']:,} | cache scris: {u['cache_write']:,}"
    )


def main() -> None:
    load_dotenv()
    mode = _arg("--mode", "everyone")
    if mode not in ("everyone", "departments"):
        print("Mod invalid. Foloseste: everyone | departments")
        sys.exit(1)

    if "--live" in sys.argv:
        live_run(mode)
    else:
        dry_run(mode)


if __name__ == "__main__":
    main()
