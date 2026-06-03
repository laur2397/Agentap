#!/usr/bin/env python3
"""
Generează desktop.html din app/eie.html (sursa unica de adevar pentru logica + date).

Cum functioneaza:
  - NU modifica deloc aplicatia (app/eie.html ramane intacta).
  - Ia continutul aplicatiei si injecteaza UN SINGUR bloc <style> ("desktop skin")
    inainte de </head>. Skin-ul se aplica doar pe ecrane late (min-width:980px) si
    re-aranjeaza acelasi DOM intr-un layout de desktop: bara laterala (din tab bar) +
    bara de sus + continut lat, centrat. Pe ecran ingust, desktop.html arata exact ca
    aplicatia de telefon (skin-ul nu se aplica).
  - Aceleasi date: desktop.html ruleaza acelasi JS, deci foloseste acelasi localStorage
    (acelasi cont/retea) cand e servit de pe acelasi domeniu.

Reruleaza dupa orice schimbare in aplicatie:  python3 tools/build-desktop.py
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "app" / "eie.html"
OUT = ROOT / "desktop.html"

# ─────────────────────────────────────────────────────────────────────────────
# Desktop skin: re-aranjeaza acelasi DOM (header / main / nav) prin CSS Grid.
# Totul gated pe @media (min-width:980px) ca sub el sa ramana aplicatia de telefon.
# ─────────────────────────────────────────────────────────────────────────────
DESKTOP_SKIN = """
<style id="eie-desktop-skin">
/* ===== VARIANTA DE DESKTOP — strat generat, peste stilurile aplicatiei ===== */
/* Sub 980px ramane aplicatia de telefon, neatinsa. */
@media (min-width:980px){
  /* anuleaza "rama de telefon" si revine la tot ecranul */
  body{display:block!important;place-items:initial!important;animation:none!important;
    background:radial-gradient(130% 90% at 50% -10%,#11161f,#0a0c12 60%)!important}
  .shell::before{display:none!important}   /* fara notch */

  /* shell = grila: bara de sus (lat) + bara laterala (stanga) + continut */
  .shell{display:grid!important;width:100%!important;max-width:none!important;
    height:100vh!important;height:100dvh!important;margin:0!important;
    border-radius:0!important;box-shadow:none!important;overflow:hidden!important;
    background:var(--bg)!important;
    grid-template-columns:268px minmax(0,1fr);
    grid-template-rows:auto minmax(0,1fr);
    grid-template-areas:"head head" "side main"}

  /* ----- BARA DE SUS ----- */
  header{grid-area:head!important;position:relative!important;top:auto!important;
    padding:14px 30px!important;border-bottom:1px solid var(--line)!important;
    background:color-mix(in srgb,var(--bg) 92%,transparent)!important}
  header .htop{max-width:none}

  /* ----- BARA LATERALA (din tab bar) ----- */
  nav{grid-area:side!important;position:relative!important;bottom:auto!important;
    border-top:0!important;border-right:1px solid var(--line)!important;
    background:var(--nav-bg)!important;padding:16px 12px!important;
    overflow-y:auto;scrollbar-width:none}
  nav::after{display:none!important}
  nav::-webkit-scrollbar{width:0;height:0}
  .navin{flex-direction:column!important;align-items:stretch!important;
    padding:0!important;gap:3px}
  .tab{flex:none!important;flex-direction:row!important;justify-content:flex-start!important;
    align-items:center!important;min-height:0!important;padding:11px 14px!important;
    gap:14px!important;font-size:14.5px!important;font-weight:600!important;
    border-radius:14px!important;text-align:left}
  .tab .ic{width:42px!important;height:42px!important;border-radius:13px!important;flex:none}
  .tab .ic svg{width:24px!important;height:24px!important}
  .tab::before{display:none!important}     /* fara indicatorul de sus al tab-ului */
  .tab:hover{background:color-mix(in srgb,var(--primary-soft) 70%,transparent)}
  .tab.on{background:var(--primary-soft)!important;color:var(--primary-dim)!important}
  .tab.on .ic{background:transparent!important}
  /* badge-ul de notificare trece la capatul din dreapta al randului */
  .navbadge{position:static!important;margin-left:auto!important;top:auto!important;left:auto!important}

  /* ----- CONTINUT lat, centrat ----- */
  main{grid-area:main!important;overflow-y:auto;
    padding:30px 34px 64px!important}
  main>.view{max-width:1100px;margin:0 auto;width:100%}
  /* schimbarea de ecran ramane instant pe desktop */
  .view.on>*{animation-duration:.28s!important;animation-delay:0s!important}

  /* overlay-uri (cautare/quick-add) centrate, nu pe toata latimea */
  .searchov{max-width:700px}
  .quicksheet{max-width:520px;margin-left:auto;margin-right:auto}

  /* link discret de intoarcere la varianta de telefon (vezi marcaj jos) */
  .eie-toapp{position:fixed;right:16px;bottom:14px;z-index:60;
    font-size:12px;font-weight:600;color:var(--muted);text-decoration:none;
    padding:7px 13px;border:1px solid var(--line);border-radius:999px;
    background:color-mix(in srgb,var(--bg) 80%,transparent);backdrop-filter:blur(8px)}
  .eie-toapp:hover{color:var(--ink);border-color:var(--line2)}
}
/* sub 980px (telefon) ascundem complet marcajul de desktop */
@media (max-width:979.98px){.eie-toapp{display:none!important}}
</style>
"""

# Un link discret "Versiunea de telefon" -> index.html, vizibil doar pe desktop.
TOAPP_LINK = '\n<a class="eie-toapp" href="index.html" title="Deschide varianta de telefon">📱 Versiunea de telefon</a>\n'


def main():
    if not SRC.exists():
        sys.exit(f"Nu gasesc sursa: {SRC}")
    html = SRC.read_text(encoding="utf-8")

    if "</head>" not in html:
        sys.exit("Sursa nu are </head> — nu pot injecta skin-ul.")

    # 1) injecteaza skin-ul inainte de </head>
    out = html.replace("</head>", DESKTOP_SKIN + "</head>", 1)

    # 2) titlu distinct (nu influenteaza nimic functional)
    out = re.sub(r"<title>(.*?)</title>",
                 lambda m: f"<title>{m.group(1)} — Desktop</title>",
                 out, count=1, flags=re.S)

    # 3) link de intoarcere la telefon, chiar dupa <div class="shell">
    out = out.replace('<div class="shell">', '<div class="shell">' + TOAPP_LINK, 1)

    OUT.write_text(out, encoding="utf-8")
    print(f"OK -> {OUT.relative_to(ROOT)} ({len(out):,} bytes)")


if __name__ == "__main__":
    main()
