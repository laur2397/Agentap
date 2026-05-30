"""Demo: echipa de agenti SCRIE codul aplicatiei (prototip real pe disc).

Arhitect -> proiecteaza structura | Programator -> scrie fisierele | Reviewer -> evalueaza.

Rulare (necesita ANTHROPIC_API_KEY — agentii scriu cod efectiv):
    python examples/build_app.py
    python examples/build_app.py --workspace app_v1 --no-review

Fara cheie, scriptul explica ce ar face si verifica mecanic ca uneltele de
scriere a fisierelor functioneaza (scrie un fisier de proba).
"""

from __future__ import annotations

import os
import sys
import tempfile
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

from agentap import build_app, file_tools, list_workspace


def _arg(flag: str, default: str) -> str:
    if flag in sys.argv:
        i = sys.argv.index(flag)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default


def fara_cheie() -> None:
    print("⚠  Lipseste ANTHROPIC_API_KEY — agentii nu pot rula (nu pot scrie codul).")
    print("   Dar verific mecanic ca uneltele de fisiere chiar functioneaza:\n")
    ws = tempfile.mkdtemp(prefix="agentap_proba_")
    scrie, _citeste, listeaza = file_tools(ws)
    print("  ", scrie.run(cale="proba/salut.py", continut="print('agentii pot scrie cod')\n"))
    print("   Fisiere in workspace de proba:", list_workspace(ws))
    print("\n   => Capabilitatea exista. Pune o cheie API in .env si reruleaza ca")
    print("      arhitectul + programatorul sa genereze prototipul real al aplicatiei.")


def main() -> None:
    load_dotenv()
    if not os.environ.get("ANTHROPIC_API_KEY"):
        fara_cheie()
        return

    workspace = _arg("--workspace", "workspace")
    review = "--no-review" not in sys.argv

    def log(event: str, payload: dict[str, Any]) -> None:
        if event == "agent_start":
            print(f"\n▶ [{payload['agent']}] pornește...")
        elif event == "tool_call":
            t = payload["tool"]
            extra = f" {payload['input'].get('cale','')}" if t == "scrie_fisier" else ""
            print(f"   🔧 [{payload['agent']}] {t}{extra}")

    print(f"Echipa de build scrie aplicatia in: {os.path.abspath(workspace)}\n")
    rez = build_app(workspace=workspace, review=review, on_event=log)

    print("\n" + "=" * 70)
    print("FISIERE GENERATE:")
    print("=" * 70)
    for f in rez["fisiere"]:
        print("  ", f)

    print("\n" + "=" * 70)
    print("REZUMAT IMPLEMENTARE (programator):")
    print("=" * 70)
    print(rez["implementare"][:1500])

    if rez["review"]:
        print("\n" + "=" * 70)
        print("REVIEW:")
        print("=" * 70)
        print(rez["review"][:1500])

    print(f"\n✓ Cod scris in {rez['workspace']}")


if __name__ == "__main__":
    main()
