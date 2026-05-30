"""Pune firma de agenti REALA in actiune: brainstorm -> sinteza -> build.

Flux:
  1. Fiecare ANGAJAT (paralel, in loturi) da o idee „wow” pentru aplicatie,
     din perspectiva rolului lui. -> idei reale, de la cei ~220 de agenti.
  2. Un agent ARHITECT (opus, effort high) sintetizeaza ideile intr-o spec.
  3. Un agent PROGRAMATOR scrie EFECTIV aplicatia (HTML standalone) pe disc.

Rulare:
    python examples/agenti_wow.py --limit 8     # test rapid pe 8 agenti
    python examples/agenti_wow.py --all         # toti angajatii (~220)

Necesita ANTHROPIC_API_KEY in mediu.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import anthropic
from agentap.organizatie import ORGANIZATIE, nume_curat, total_general

MODEL = "claude-opus-4-8"
LOT = 4  # cati agenti rulam in paralel simultan (mic, ca sa evitam rate limit)

BRIEF = (
    "Aplicatie privata pentru un cerc de business: aduna ce ofera / ce cauta fiecare, "
    "face potriviri in stratul ascuns si propune conexiuni cu dublu consimtamant si sursa "
    "citata. Are ecrane: Potriviri, Grupuri (chat), Profil, Dicteaza dupa apel, Secretara."
)


def angajati(limit: int | None) -> list[tuple[str, str, str, int]]:
    """Lista (departament, rol, descriere, index) pentru fiecare angajat."""
    out = []
    for dep, data in ORGANIZATIE.items():
        for rol, nr, descriere in data["roluri"]:
            for i in range(1, nr + 1):
                out.append((dep, rol, descriere, i))
    return out[:limit] if limit else out


async def idee_angajat(client, sem, dep, rol, descriere) -> dict:
    """Un angajat da o idee scurta de feature wow din rolul lui."""
    sys_prompt = (
        f"Esti „{rol}” in departamentul „{nume_curat(dep)}” al unei firme IT. "
        f"Responsabilitate: {descriere}. Mediu educativ simulat."
    )
    user = (
        f"{BRIEF}\n\nDin expertiza ta de „{rol}”, propune O SINGURA idee concreta care ar "
        "face aplicatia 'wow'. Format: o propozitie de feature (max 25 cuvinte), la obiect. "
        "Fara introducere, doar ideea."
    )
    async with sem:
        for attempt in range(6):  # reincercari cu backoff la rate limit
            try:
                r = await client.messages.create(
                    model=MODEL, max_tokens=120,
                    system=[{"type": "text", "text": sys_prompt, "cache_control": {"type": "ephemeral"}}],
                    output_config={"effort": "low"},
                    messages=[{"role": "user", "content": user}],
                )
                txt = "".join(b.text for b in r.content if b.type == "text").strip()
                return {"dep": nume_curat(dep), "rol": rol, "idee": txt, "ok": True}
            except anthropic.RateLimitError:
                await asyncio.sleep(2 * (2 ** attempt))  # 2,4,8,16,32,64s
            except Exception as e:  # noqa: BLE001
                return {"dep": nume_curat(dep), "rol": rol, "idee": f"[eroare: {type(e).__name__}]", "ok": False}
        return {"dep": nume_curat(dep), "rol": rol, "idee": "[rate limit persistent]", "ok": False}


async def brainstorm(client, lista) -> list[dict]:
    sem = asyncio.Semaphore(LOT)
    tasks = [idee_angajat(client, sem, d, r, desc) for (d, r, desc, _i) in lista]
    rez = []
    done = 0
    for fut in asyncio.as_completed(tasks):
        rez.append(await fut)
        done += 1
        if done % LOT == 0 or done == len(tasks):
            print(f"   ...{done}/{len(tasks)} agenti au raspuns")
    return rez


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Lipseste ANTHROPIC_API_KEY"); sys.exit(1)

    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    elif "--all" not in sys.argv:
        limit = 8  # implicit, test mic

    lista = angajati(limit)
    print(f"Pun {len(lista)} agenti la treaba (din {total_general()} angajati), in loturi de {LOT}...\n")

    client = anthropic.AsyncAnthropic()
    t0 = time.time()
    idei = asyncio.run(brainstorm(client, lista))
    dt = time.time() - t0
    ok = sum(1 for i in idei if i["ok"])
    print(f"\n✓ {ok}/{len(idei)} idei colectate in {dt:.0f}s")

    with open(os.path.join(os.path.dirname(__file__), "..", "idei_agenti.json"), "w", encoding="utf-8") as f:
        json.dump(idei, f, ensure_ascii=False, indent=2)

    print("\nMostre de idei reale de la agenti:")
    for i in idei[:10]:
        if i["ok"]:
            print(f"  · [{i['rol']}] {i['idee'][:90]}")


if __name__ == "__main__":
    main()
