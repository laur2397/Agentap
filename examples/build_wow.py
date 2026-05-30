"""Pasul 2-3: agentii construiesc aplicatia WOW din ideile lor reale.

  - ARHITECT (Opus, effort high): din ideile celor 220 agenti -> selecteaza top
    features 'wow' implementabile client-side + note de design.
  - PROGRAMATOR (Opus, streaming): scrie EFECTIV aplicatia intr-un singur HTML
    standalone, salvat in app/wow.html.

Necesita idei_agenti.json (ruleaza intai agenti_wow.py --all) si ANTHROPIC_API_KEY.
"""

from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import anthropic

MODEL = "claude-opus-4-8"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PALETA = (
    "Stil obligatoriu — light editorial, lux discret pentru business: fundal fildes (#faf8f3), "
    "titluri serif Playfair Display, accent bleumarin profund (#1a2f4b) + auriu discret (#b8924a), "
    "carduri albe cu umbra fina, colturi rotunjite, eleganta sobra. Romana fara diacritice in cod."
)


def grupeaza_idei() -> str:
    d = json.load(open(os.path.join(ROOT, "idei_agenti.json"), encoding="utf-8"))
    pe_dep: dict[str, list[str]] = {}
    for x in d:
        if x["ok"]:
            pe_dep.setdefault(x["dep"], []).append(f"[{x['rol']}] {x['idee']}")
    bloc = []
    for dep, idei in pe_dep.items():
        bloc.append(f"### {dep} ({len(idei)} idei)")
        bloc.extend(idei)
    return "\n".join(bloc)


def arhitect(client, idei_txt: str) -> str:
    print("ARHITECT: sintetizez ideile echipei...", flush=True)
    r = client.messages.create(
        model=MODEL, max_tokens=4000,
        system=[{"type": "text",
                 "text": "Esti arhitect de produs. Selectezi si prioritizezi features 'wow' care chiar pot fi construite intr-un singur fisier HTML standalone (fara backend, date in localStorage). Mediu educativ.",
                 "cache_control": {"type": "ephemeral"}}],
        output_config={"effort": "high"},
        messages=[{"role": "user", "content":
            f"Iata ideile de la echipa, grupate pe departament:\n\n{idei_txt}\n\n"
            "Selecteaza cele mai bune 7-9 features 'wow' care se pot implementa client-side "
            "(HTML+JS+localStorage), peste aplicatia existenta (Potriviri, Grupuri, Profil, "
            "Dicteaza, Secretara). Pentru fiecare: nume scurt + 1 rand cum se vede in UI. "
            "Adauga 3 randuri de directie de design. Fii concret si implementabil."}],
    )
    return "".join(b.text for b in r.content if b.type == "text").strip()


def programator(client, spec: str) -> str:
    print("PROGRAMATOR: scriu aplicatia (streaming)...", flush=True)
    user = (
        f"{PALETA}\n\nSPEC de la arhitect (features wow alese din ideile echipei):\n{spec}\n\n"
        "Scrie o aplicatie web COMPLETA si FUNCTIONALA intr-un SINGUR fisier HTML standalone "
        "(fara dependinte externe in afara de Google Fonts; date in localStorage). "
        "Cerinte:\n"
        "- Ecrane: Potriviri, Grupuri (chat), Profil (ce ofer vizibil / ce caut privat), "
        "Dicteaza dupa apel (extragere euristica), Secretara (briefing+sarcini), cu bara de navigatie jos.\n"
        "- Motor de potrivire client-side (suprapunere de cuvinte cheie intre 'caut' si 'ofer'), "
        "flux cu DUBLU CONSIMTAMANT, sursa mereu citata.\n"
        "- Implementeaza cat de multe din features-le wow din spec poti, real functionale.\n"
        "- Date demo la prima rulare (3 membri: Ana Popescu, Bogdan Marin, Cristina Ilie; o potrivire de carbune).\n"
        "Raspunde DOAR cu codul HTML complet, de la <!DOCTYPE html> la </html>, nimic altceva."
    )
    with client.messages.stream(
        model=MODEL, max_tokens=32000,
        output_config={"effort": "high"},
        messages=[{"role": "user", "content": user}],
    ) as stream:
        for _ in stream.text_stream:
            pass
        msg = stream.get_final_message()
    return "".join(b.text for b in msg.content if b.type == "text")


def extrage_html(txt: str) -> str:
    m = re.search(r"<!DOCTYPE html>.*</html>", txt, re.S | re.I)
    if m:
        return m.group(0)
    m = re.search(r"```(?:html)?\s*(.*?)```", txt, re.S)
    return m.group(1).strip() if m else txt.strip()


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Lipseste ANTHROPIC_API_KEY"); sys.exit(1)
    if not os.path.exists(os.path.join(ROOT, "idei_agenti.json")):
        print("Lipseste idei_agenti.json — ruleaza intai agenti_wow.py --all"); sys.exit(1)

    client = anthropic.Anthropic()
    idei_txt = grupeaza_idei()
    spec = arhitect(client, idei_txt)
    print("\n--- SPEC ARHITECT ---\n" + spec[:1000] + "\n---\n", flush=True)

    html = extrage_html(programator(client, spec))
    out = os.path.join(ROOT, "app", "wow.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\nGATA: aplicatia scrisa de agenti -> {out} ({len(html)} caractere)")

    with open(os.path.join(ROOT, "app", "wow_spec.md"), "w", encoding="utf-8") as f:
        f.write("# Spec WOW (sintetizat de agentul arhitect din ideile celor 220)\n\n" + spec)


if __name__ == "__main__":
    main()
