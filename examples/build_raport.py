"""Generează un raport VIZUAL (HTML) al proiectului rezolvat de firma de agenți.

Îmbină structura reală a firmei (din `organizatie.py`) cu livrabilul de proiect:
planul executiv + pozițiile departamentelor. Conținutul narativ este generat de
același model pe care îl folosesc agenții (`claude-opus-4-8`), ca substitut al
rulării live a celor 239 de agenți (care necesită o cheie API).

Rulare:
    python examples/build_raport.py            # scrie raport_proiect.html
"""

from __future__ import annotations

import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentap.organizatie import ORGANIZATIE, nume_curat, total_general
from agentap.proiect import PROIECT

# --------------------------------------------------------------------------- #
# Livrabilul „generat” — planul executiv + pozițiile departamentelor.
# (Reprezentativ pentru ce ar produce firma; autor: claude-opus-4-8.)
# --------------------------------------------------------------------------- #
PLAN_EXECUTIV = {
    "rezumat": (
        "Construim un intermediar discret pentru un cerc privat de business: o aplicație "
        "care adună informația din discuții (cine oferă ce, cine caută ce), o înțelege și "
        "propune proactiv conexiuni — mereu cu sursă citată și cu acordul ambelor părți. "
        "Diferențiatorul nu e o bază de date, ci tactul: relații făcute la momentul potrivit."
    ),
    "faze": [
        ("v1 — Validare în grupul propriu", [
            "Chat / grupuri native (informația intră direct în aplicație)",
            "Note rapide cu marcaj „important”",
            "Profil ce ofer / ce caut + control fin pe vizibilitate",
            "Dictare după apel cu extragere AI (ofer/caut + rezumat)",
            "Potrivire de bază + fluxul cu dublu consimțământ „vrei să te prezint?”",
            "Secretară personală (briefing, sarcini, pe cine să contactezi)",
        ]),
        ("v2 — Creștere, dacă v1 prinde", [
            "Înregistrare live a întâlnirilor față în față (sensibil la consimțământ)",
            "Feedback „a ieșit ceva?” + învățare automată în timp",
            "Deschiderea spre mai multe comunități / rețea mai mare",
        ]),
    ],
    "riscuri": [
        ("Captarea informației e prea greoaie", "Dictare simplă după apel + chat nativ; zero formulare lungi.", "critic"),
        ("AI marchează prea mult automat", "Sugestiile automate stau separat de ce marchează omul.", "ridicat"),
        ("Expunere fără acord la conexiuni", "Dublu consimțământ înainte de orice prezentare.", "critic"),
        ("Informație despre persoane din afară", "Doar membrii intră în creierul de potriviri.", "ridicat"),
        ("Mecanici de dependență / dark patterns", "Behavioral Science validează etic fiecare mecanism de engagement.", "mediu"),
    ],
    "primii_pasi": [
        "Prototip al fluxului „dictare după apel → extragere ofer/caut” (efectul wow, cel mai ieftin de validat).",
        "Schema celor două straturi de date (ce știe app-ul vs. ce văd ceilalți) + motorul de potrivire în stratul ascuns.",
        "Fluxul de dublu consimțământ end-to-end pe un grup-pilot de 8-12 membri.",
    ],
}

# Poziții detaliate pentru departamentele cheie (autor: claude-opus-4-8).
POZITII = {
    "1. Engineering / Dezvoltare software": (
        "Livrăm v1 ca aplicație mobilă cu backend de chat în timp real. Squad-uri pe: Chat/Grupuri, "
        "Captare (dictare→extragere), Potriviri, Secretară. Primii pași: schema de date pe două straturi, "
        "API de potrivire ofer↔caut, integrarea cu serviciul AI de extragere."
    ),
    "5b. Artificial Intelligence (AI)": (
        "Suntem creierul: extragem „ce oferă / ce caută” din text și dictare, și rulăm motorul de potrivire "
        "în stratul ascuns. Începem cu extragere prin LLM + un scor de potrivire explicabil (cu sursă citată). "
        "Sugestiile AI rămân separate de ce marchează omul, ca să nu devină zgomot."
    ),
    "7b. Behavioral Science & Ethical Product Design": (
        "Garantăm că produsul ajută fără să creeze dependență. Fluxul „vrei să te prezint?” trebuie să fie "
        "respectuos, nu insistent; notificările — utile, nu compulsive. Validăm fiecare mecanism de engagement "
        "și definim metrici de engagement sănătos vs. compulsiv."
    ),
    "6. Produs (Product)": (
        "Prioritizăm strict v1 pe ipoteza centrală: oamenii chiar pun informație și chiar le plac potrivirile. "
        "Definim cele 4 ecrane (Potriviri, Grupuri, Dictează, Secretară) și criteriile de succes măsurabile "
        "pentru pilotul intern."
    ),
    "7. Design / UX": (
        "Ton: intermediar discret și de încredere, nu bază de date rece. Cardul de potrivire arată clar motivul "
        "și sursa, cu acțiuni simple Prezintă-mă / Refuz. Dictarea trebuie să fie o singură apăsare; secretara — "
        "caldă, în limbaj natural."
    ),
    "4. Securitate": (
        "Cerc privat = confidențialitate maximă. Criptare în tranzit și la repaus, control de acces strict pe cele "
        "două straturi de date, și o regulă fermă: persoanele din afară nu intră în motorul de potrivire. Pregătim "
        "un checklist de securitate înainte de pilot."
    ),
    "5. Date, AI si Analytics": (
        "Măsurăm ce contează pentru validare: rata de captare a informației, calitatea potrivirilor, „a ieșit ceva?”. "
        "Construim palnia de onboarding și instrumentăm efectul wow ca să știm dacă pilotul reușește."
    ),
    "14. Legal & Compliance": (
        "GDPR by design: consimțământ explicit, dreptul de a controla vizibilitatea, și clarificarea statutului "
        "persoanelor pomenite dar nemembre. Pregătim termenii pentru un cerc privat și politica de date pentru v2 "
        "(înregistrarea live)."
    ),
}


def _depts_html() -> str:
    cards = []
    for nume, data in ORGANIZATIE.items():
        hc = sum(nr for _, nr, _ in data["roluri"])
        pozitie = POZITII.get(nume)
        extra = (
            f'<p class="poz"><span class="tag">poziție de departament</span>{html.escape(pozitie)}</p>'
            if pozitie else ""
        )
        roluri = "".join(
            f'<li><b>{nr}×</b> {html.escape(rol)}</li>' for rol, nr, _ in data["roluri"]
        )
        cards.append(f"""
        <div class="dept">
          <div class="dept-head">
            <h3>{html.escape(nume_curat(nume))}</h3>
            <span class="hc">{hc} agenți</span>
          </div>
          <p class="intro">{html.escape(data["intro"])}</p>
          {extra}
          <details><summary>Roluri ({len(data["roluri"])})</summary><ul class="roluri">{roluri}</ul></details>
        </div>""")
    return "\n".join(cards)


def _plan_html() -> str:
    faze = ""
    for titlu, items in PLAN_EXECUTIV["faze"]:
        lis = "".join(f"<li>{html.escape(x)}</li>" for x in items)
        faze += f'<div class="faza"><h4>{html.escape(titlu)}</h4><ul>{lis}</ul></div>'

    riscuri = ""
    for risc, mit, nivel in PLAN_EXECUTIV["riscuri"]:
        riscuri += (
            f'<tr><td><span class="lvl lvl-{nivel}">{nivel}</span></td>'
            f"<td>{html.escape(risc)}</td><td>{html.escape(mit)}</td></tr>"
        )

    pasi = "".join(
        f'<li><span class="num">{i}</span>{html.escape(p)}</li>'
        for i, p in enumerate(PLAN_EXECUTIV["primii_pasi"], 1)
    )

    return f"""
    <p class="rezumat">{html.escape(PLAN_EXECUTIV["rezumat"])}</p>
    <div class="faze-grid">{faze}</div>
    <h3>Top riscuri &amp; mitigare</h3>
    <table class="riscuri"><thead><tr><th>Nivel</th><th>Risc</th><th>Mitigare</th></tr></thead>
      <tbody>{riscuri}</tbody></table>
    <h3>Primii 3 pași</h3>
    <ol class="pasi">{pasi}</ol>"""


def build() -> str:
    n_dep = len(ORGANIZATIE)
    n_ang = total_general()
    n_agenti = n_ang + n_dep + 1
    nume_proiect = PROIECT["meta"]["nume_proiect"]
    viziune = PROIECT["viziune"]["rezumat_o_propozitie"]

    return f"""<!DOCTYPE html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agentap — Raport de proiect</title>
<style>
  :root {{
    --bg:#0e1220; --panel:#161c2e; --panel2:#1d2438; --ink:#e8ecf6; --muted:#9aa6c4;
    --accent:#6ea8fe; --accent2:#9b8cff; --good:#46d39a; --line:#283150;
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink);
    font:15px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif; }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:0 20px 80px; }}
  header.hero {{ background:linear-gradient(135deg,#1c2748,#241c52); padding:54px 20px 40px;
    text-align:center; border-bottom:1px solid var(--line); }}
  .hero h1 {{ margin:0 0 6px; font-size:30px; letter-spacing:.3px; }}
  .hero .sub {{ color:var(--muted); max-width:760px; margin:0 auto 22px; }}
  .stats {{ display:flex; gap:14px; justify-content:center; flex-wrap:wrap; }}
  .stat {{ background:rgba(255,255,255,.05); border:1px solid var(--line); border-radius:14px;
    padding:14px 22px; min-width:120px; }}
  .stat b {{ display:block; font-size:28px; background:linear-gradient(90deg,var(--accent),var(--accent2));
    -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; }}
  .stat span {{ color:var(--muted); font-size:12.5px; text-transform:uppercase; letter-spacing:.5px; }}
  section {{ margin-top:38px; }}
  h2 {{ font-size:20px; margin:0 0 4px; }}
  h2 .em {{ color:var(--accent); }}
  .lead {{ color:var(--muted); margin:0 0 18px; }}
  .flow {{ display:flex; align-items:stretch; gap:0; flex-wrap:wrap; }}
  .step {{ flex:1; min-width:150px; background:var(--panel); border:1px solid var(--line);
    border-radius:12px; padding:14px 16px; position:relative; }}
  .step h4 {{ margin:0 0 4px; font-size:14px; }}
  .step p {{ margin:0; color:var(--muted); font-size:13px; }}
  .arrow {{ display:flex; align-items:center; color:var(--accent); font-size:22px; padding:0 8px; }}
  .panel {{ background:var(--panel); border:1px solid var(--line); border-radius:16px; padding:22px 24px; }}
  .rezumat {{ font-size:16px; border-left:3px solid var(--accent); padding-left:14px; color:#dde4f5; }}
  .faze-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin:18px 0; }}
  .faza {{ background:var(--panel2); border:1px solid var(--line); border-radius:12px; padding:14px 18px; }}
  .faza h4 {{ margin:0 0 8px; color:var(--accent2); }}
  .faza ul {{ margin:0; padding-left:18px; }} .faza li {{ margin:4px 0; }}
  table.riscuri {{ width:100%; border-collapse:collapse; margin:10px 0 4px; font-size:14px; }}
  .riscuri th, .riscuri td {{ text-align:left; padding:9px 10px; border-bottom:1px solid var(--line); vertical-align:top; }}
  .riscuri th {{ color:var(--muted); font-weight:600; font-size:12px; text-transform:uppercase; }}
  .lvl {{ font-size:11px; padding:2px 9px; border-radius:20px; text-transform:uppercase; font-weight:700; }}
  .lvl-critic {{ background:#3a1b22; color:#ff8a9c; }} .lvl-ridicat {{ background:#3a2f17; color:#ffce6e; }}
  .lvl-mediu {{ background:#1f3326; color:#7fe0ad; }}
  ol.pasi {{ list-style:none; padding:0; margin:8px 0 0; }}
  ol.pasi li {{ display:flex; gap:12px; align-items:flex-start; margin:10px 0; }}
  .num {{ flex:none; width:26px; height:26px; border-radius:50%; background:var(--accent); color:#0b1020;
    font-weight:700; display:grid; place-items:center; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); gap:16px; }}
  .dept {{ background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:16px 18px; }}
  .dept-head {{ display:flex; justify-content:space-between; align-items:baseline; gap:10px; }}
  .dept h3 {{ margin:0; font-size:16px; }}
  .hc {{ flex:none; background:rgba(110,168,254,.15); color:var(--accent); border-radius:20px;
    padding:2px 10px; font-size:12px; font-weight:600; }}
  .intro {{ color:var(--muted); font-size:13px; margin:8px 0; }}
  .poz {{ font-size:13.5px; background:var(--panel2); border-radius:10px; padding:10px 12px; margin:8px 0; }}
  .tag {{ display:inline-block; font-size:10px; text-transform:uppercase; letter-spacing:.6px;
    color:var(--good); border:1px solid var(--good); border-radius:6px; padding:1px 7px; margin-right:8px; }}
  details summary {{ cursor:pointer; color:var(--accent); font-size:13px; margin-top:6px; }}
  ul.roluri {{ columns:2; font-size:13px; color:var(--muted); margin:8px 0 0; padding-left:18px; }}
  .note {{ background:#23202e; border:1px solid #4a3d6b; border-radius:12px; padding:12px 16px;
    color:#d8cdf0; font-size:13px; margin-top:14px; }}
  footer {{ text-align:center; color:var(--muted); font-size:12.5px; margin-top:40px; }}
  @media (max-width:680px) {{ .faze-grid {{ grid-template-columns:1fr; }} ul.roluri {{ columns:1; }} }}
</style>
</head>
<body>
<header class="hero">
  <h1>🏢 {html.escape(nume_proiect)}</h1>
  <p class="sub">{html.escape(viziune)}</p>
  <div class="stats">
    <div class="stat"><b>{n_agenti}</b><span>agenți AI</span></div>
    <div class="stat"><b>{n_dep}</b><span>departamente</span></div>
    <div class="stat"><b>{n_ang}</b><span>angajați</span></div>
    <div class="stat"><b>3</b><span>niveluri</span></div>
  </div>
</header>

<div class="wrap">

  <section>
    <h2>Cum lucrează firma <span class="em">— fan-out → fan-in</span></h2>
    <p class="lead">Brief-ul intră o dată; ies un plan executiv și pozițiile fiecărui departament.</p>
    <div class="flow">
      <div class="step"><h4>1 · Brief</h4><p>Specificația proiectului intră în firmă.</p></div>
      <div class="arrow">→</div>
      <div class="step"><h4>2 · {n_ang} angajați</h4><p>Fiecare contribuie din rolul lui.</p></div>
      <div class="arrow">→</div>
      <div class="step"><h4>3 · {n_dep} manageri</h4><p>Sintetizează poziția echipei.</p></div>
      <div class="arrow">→</div>
      <div class="step"><h4>4 · CEO</h4><p>Consolidează planul executiv.</p></div>
    </div>
  </section>

  <section>
    <h2>📋 Plan executiv consolidat <span class="em">(CEO)</span></h2>
    <p class="lead">Livrabilul final al firmei pentru acest proiect.</p>
    <div class="panel">{_plan_html()}</div>
  </section>

  <section>
    <h2>🗂️ Pozițiile departamentelor</h2>
    <p class="lead">Toate cele {n_dep} departamente, cu headcount-ul real. Cele cheie au și poziția pe proiect.</p>
    <div class="grid">{_depts_html()}</div>
  </section>

  <p class="note">ℹ️ Conținutul narativ (plan + poziții) este generat de <b>claude-opus-4-8</b> —
  exact modelul folosit de agenți — ca substitut al rulării live a celor {n_agenti} de agenți,
  care necesită o cheie API. Structura, departamentele și headcount-urile sunt datele reale din proiect.
  Mediu simulat, în scop educativ.</p>

  <footer>Generat de Agentap · raport de proiect · {html.escape(nume_proiect)}</footer>
</div>
</body>
</html>"""


if __name__ == "__main__":
    cale = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "raport_proiect.html")
    with open(cale, "w", encoding="utf-8") as f:
        f.write(build())
    print(f"Raport scris: {cale}")
