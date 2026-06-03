#!/usr/bin/env python3
"""
Generează desktop.html (si index.html) din app/eie.html — sursa unica de adevar.

Cum functioneaza:
  - NU modifica deloc aplicatia (app/eie.html ramane intacta).
  - index.html = copie 1:1 a aplicatiei (varianta de telefon servita din radacina).
  - desktop.html = aplicatia + UN SINGUR bloc <style> ("desktop skin") injectat inainte
    de </head>. Skin-ul se aplica doar pe ecrane late CU MOUSE (min-width:760px si
    pointer:fine) si re-aranjeaza acelasi DOM intr-un layout de desktop: bara laterala
    (din tab bar) + bara de sus + continut centrat. Pe telefon/tableta-touch sau ecran
    ingust, desktop.html arata exact ca aplicatia de telefon.
  - Aceleasi date: ambele ruleaza acelasi JS, deci folosesc acelasi localStorage.

Reruleaza dupa orice schimbare in aplicatie:  python3 tools/build-desktop.py
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "app" / "eie.html"
OUT_DESKTOP = ROOT / "desktop.html"
OUT_INDEX = ROOT / "index.html"

# ─────────────────────────────────────────────────────────────────────────────
# Desktop skin: re-aranjeaza acelasi DOM (header / main / nav) prin CSS Grid.
# Gated pe (min-width:760px) and (pointer:fine) — adica doar pe desktop cu mouse.
# Acelasi prag ca "rama de telefon" din app => fara banda intermediara confuza.
# ─────────────────────────────────────────────────────────────────────────────
DESKTOP_SKIN = """
<style id="eie-desktop-skin">
/* ===== VARIANTA DE DESKTOP — strat generat, peste stilurile aplicatiei ===== */
.eie-toapp{display:none}  /* implicit ascuns; aratat doar in layout-ul de desktop */
@media (min-width:760px) and (pointer:fine){
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

  /* ----- CONTINUT centrat (nu intins) ----- */
  main{grid-area:main!important;overflow-y:auto;
    padding:30px 34px 64px!important}
  main>.view{max-width:860px;margin:0 auto;width:100%}
  /* schimbarea de ecran ramane instant pe desktop */
  .view.on>*{animation-duration:.28s!important;animation-delay:0s!important}
  /* randurile de chip-uri se aseaza pe mai multe linii (nu scroll orizontal pe desktop) */
  .filters,.an-strip{flex-wrap:wrap!important;overflow:visible!important}

  /* ----- OVERLAY-uri: centrate pe ecran, nu lipite jos (bottom-sheet pe telefon) ----- */
  .overlay,.quickov{align-items:center!important;justify-content:center!important}
  .modal{width:min(92vw,560px)!important;max-width:560px!important;
    border-radius:20px!important;max-height:85vh}
  .quicksheet{max-width:520px;width:min(92vw,520px);margin:0 auto;border-radius:20px!important}
  .searchov{max-width:720px}

  /* link discret de intoarcere la varianta de telefon */
  .eie-toapp{display:block;position:fixed;right:16px;bottom:14px;z-index:60;
    font-size:12px;font-weight:700;color:var(--ink2);text-decoration:none;
    padding:8px 14px;border:1px solid var(--line2);border-radius:999px;
    background:var(--card);box-shadow:var(--shadow-lg)}
  .eie-toapp:hover{color:var(--ink);border-color:var(--primary-dim)}
}
</style>
"""

# Un link discret "Versiunea de telefon" -> index.html, vizibil doar pe desktop.
TOAPP_LINK = '\n<a class="eie-toapp" href="index.html" title="Deschide varianta de telefon">📱 Versiunea de telefon</a>\n'


def _replace_once(text, old, new, what):
    """Inlocuieste exact o data; daca nu gaseste, opreste build-ul (fail-loud)."""
    if text.count(old) < 1:
        sys.exit(f"build-desktop: nu gasesc ancora pentru {what}: {old!r}")
    return text.replace(old, new, 1)


def main():
    if not SRC.exists():
        sys.exit(f"Nu gasesc sursa: {SRC}")
    html = SRC.read_text(encoding="utf-8")

    # index.html = copie 1:1 (varianta de telefon din radacina, mereu sincronizata cu sursa)
    OUT_INDEX.write_text(html, encoding="utf-8")

    # desktop.html = sursa + skin
    out = _replace_once(html, "</head>", DESKTOP_SKIN + "</head>", "</head>")
    out = re.sub(r"<title>(.*?)</title>",
                 lambda m: f"<title>{m.group(1)} — Desktop</title>",
                 out, count=1, flags=re.S)
    out = _replace_once(out, '<div class="shell">', '<div class="shell">' + TOAPP_LINK, '<div class="shell">')
    OUT_DESKTOP.write_text(out, encoding="utf-8")

    print(f"OK -> {OUT_INDEX.relative_to(ROOT)} ({len(html):,} bytes)")
    print(f"OK -> {OUT_DESKTOP.relative_to(ROOT)} ({len(out):,} bytes)")


if __name__ == "__main__":
    main()
