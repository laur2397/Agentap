"""Memorie colectiva si potriviri — prototip v1 (backend).

Aplicatie web pentru un cerc privat de business. ZERO dependinte externe:
doar biblioteca standard Python (http.server, sqlite3, json).

Functii v1:
  - Membri (cerc privat; fara autentificare reala, e prototip)
  - Profil: ce ofer (vizibil) / ce caut (privat, doar pentru potriviri)
  - Motor de potrivire in stratul ascuns (ce caut A <-> ce ofera B)
  - Flux cu DUBLU CONSIMTAMANT inainte de orice conexiune
  - Sursa mereu citata (de unde stie aplicatia)
  - Dictare/nota cu extragere automata (euristica simpla, fara LLM)
  - Secretara: sarcini + pe cine sa contactezi
  - Conexiuni cu chat si context generat

Rulare:
    python app/server.py
    deschide http://localhost:8000
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "data.db")
STATIC = os.path.join(BASE, "static")

# Cuvinte prea comune ca sa conteze la potrivire.
STOP = {
    "si", "sau", "de", "la", "in", "un", "o", "cu", "pe", "pentru", "din", "ca",
    "care", "este", "are", "am", "ai", "vreau", "caut", "ofer", "cineva", "zona",
    "bun", "buna", "nou", "noua", "the", "a", "al", "ale", "lui", "mea", "meu",
}


# --------------------------------------------------------------------------- #
# Baza de date
# --------------------------------------------------------------------------- #
def conn() -> sqlite3.Connection:
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys = ON")
    return c


def init_db() -> None:
    c = conn()
    c.executescript(
        """
        CREATE TABLE IF NOT EXISTS members(
            id INTEGER PRIMARY KEY, name TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS items(
            id INTEGER PRIMARY KEY,
            member_id INTEGER NOT NULL,
            kind TEXT NOT NULL,            -- 'ofer' | 'caut'
            text TEXT NOT NULL,
            visible INTEGER NOT NULL DEFAULT 1,
            source TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS matches(
            id INTEGER PRIMARY KEY,
            offer_item INTEGER NOT NULL,
            seek_item INTEGER NOT NULL,
            offer_member INTEGER NOT NULL,
            seek_member INTEGER NOT NULL,
            score INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'propus',   -- propus|conectat|respins
            offer_consent INTEGER DEFAULT 0,
            seek_consent INTEGER DEFAULT 0,
            UNIQUE(offer_item, seek_item));
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY,
            match_id INTEGER NOT NULL,
            sender INTEGER,                -- NULL = mesaj de la aplicatie
            text TEXT NOT NULL,
            created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY,
            member_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL);
        """
    )
    c.commit()
    if not c.execute("SELECT 1 FROM members LIMIT 1").fetchone():
        _seed(c)
    c.close()


def _seed(c: sqlite3.Connection) -> None:
    """Date demo ca aplicatia sa arate imediat o potrivire wow."""
    today = date.today().isoformat()
    membri = ["Ana", "Bogdan", "Cristina"]
    ids = {}
    for n in membri:
        cur = c.execute("INSERT INTO members(name) VALUES(?)", (n,))
        ids[n] = cur.lastrowid

    def item(m, kind, text, vis, src):
        c.execute(
            "INSERT INTO items(member_id,kind,text,visible,source,created_at) VALUES(?,?,?,?,?,?)",
            (ids[m], kind, text, vis, src, today),
        )

    item("Bogdan", "ofer", "Cariera de carbune in zona Gorj", 1, "nota din 3 martie")
    item("Bogdan", "caut", "Investitor pentru proiect imobiliar", 0, "discutie telefonica")
    item("Ana", "caut", "Furnizor de carbune pentru fabrica", 0, "dictare dupa apel")
    item("Ana", "ofer", "Spatii comerciale de inchiriat in centru", 1, "profil")
    item("Cristina", "ofer", "Prieten cu firma de excavari, utilaje in zona Brasov", 1, "audio din 12 ianuarie")
    item("Cristina", "caut", "Contabil bun pentru firma noua", 0, "nota rapida")
    c.execute(
        "INSERT INTO tasks(member_id,text,done,created_at) VALUES(?,?,0,?)",
        (ids["Ana"], "De sunat furnizorul recomandat de grup", today),
    )
    c.commit()
    run_matching(c)


# --------------------------------------------------------------------------- #
# Motor de potrivire (in stratul ascuns)
# --------------------------------------------------------------------------- #
def _tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) >= 3 and w not in STOP}


def run_matching(c: sqlite3.Connection) -> int:
    """Compara fiecare 'caut' cu fiecare 'ofer' vizibil al altui membru."""
    cauta = c.execute("SELECT * FROM items WHERE kind='caut'").fetchall()
    ofera = c.execute("SELECT * FROM items WHERE kind='ofer' AND visible=1").fetchall()
    noi = 0
    for s in cauta:
        st = _tokens(s["text"])
        for o in ofera:
            if o["member_id"] == s["member_id"]:
                continue
            comun = st & _tokens(o["text"])
            score = len(comun)
            if score < 1:
                continue
            try:
                c.execute(
                    "INSERT INTO matches(offer_item,seek_item,offer_member,seek_member,score) "
                    "VALUES(?,?,?,?,?)",
                    (o["id"], s["id"], o["member_id"], s["member_id"], score),
                )
                noi += 1
            except sqlite3.IntegrityError:
                pass  # potrivire deja existenta
    c.commit()
    return noi


def _naive_extract(text: str) -> list[tuple[str, str]]:
    """Extragere euristica simpla din dictare/nota: (kind, propozitie)."""
    out: list[tuple[str, str]] = []
    for parte in re.split(r"[.\n;]+", text):
        p = parte.strip()
        if len(p) < 4:
            continue
        low = p.lower()
        if any(k in low for k in ("caut", "am nevoie", "vreau", "imi trebuie")):
            out.append(("caut", p))
        elif any(k in low for k in ("ofer", "am un", "am o", "vand", "detin", "furnizor", "cunosc", "prieten")):
            out.append(("ofer", p))
        else:
            out.append(("ofer", p))  # implicit, ramane sugestie de verificat
    return out


# --------------------------------------------------------------------------- #
# Logica de consimtamant
# --------------------------------------------------------------------------- #
def apply_consent(c: sqlite3.Connection, match_id: int, member_id: int, accept: bool) -> dict:
    m = c.execute("SELECT * FROM matches WHERE id=?", (match_id,)).fetchone()
    if not m:
        return {"error": "potrivire inexistenta"}
    if not accept:
        c.execute("UPDATE matches SET status='respins' WHERE id=?", (match_id,))
        c.commit()
        return {"status": "respins"}

    if member_id == m["offer_member"]:
        c.execute("UPDATE matches SET offer_consent=1 WHERE id=?", (match_id,))
    elif member_id == m["seek_member"]:
        c.execute("UPDATE matches SET seek_consent=1 WHERE id=?", (match_id,))
    c.commit()

    m = c.execute("SELECT * FROM matches WHERE id=?", (match_id,)).fetchone()
    if m["offer_consent"] and m["seek_consent"] and m["status"] != "conectat":
        c.execute("UPDATE matches SET status='conectat' WHERE id=?", (match_id,))
        o = c.execute("SELECT * FROM items WHERE id=?", (m["offer_item"],)).fetchone()
        s = c.execute("SELECT * FROM items WHERE id=?", (m["seek_item"],)).fetchone()
        on = _name(c, m["offer_member"])
        sn = _name(c, m["seek_member"])
        ctx = (
            f"Aplicatia v-a pus in legatura. {sn} cauta: „{s['text']}”, iar {on} ofera: "
            f"„{o['text']}”. Sursa: {o['source']}. Va las sa continuati de aici."
        )
        c.execute(
            "INSERT INTO messages(match_id,sender,text,created_at) VALUES(?,NULL,?,?)",
            (match_id, ctx, date.today().isoformat()),
        )
        c.commit()
        return {"status": "conectat"}
    return {"status": "asteptare confirmarea celeilalte parti"}


def _name(c: sqlite3.Connection, mid: int) -> str:
    r = c.execute("SELECT name FROM members WHERE id=?", (mid,)).fetchone()
    return r["name"] if r else "?"


# --------------------------------------------------------------------------- #
# API
# --------------------------------------------------------------------------- #
def api(method: str, path: str, q: dict, body: dict) -> tuple[int, dict]:
    c = conn()
    try:
        # --- membri ---
        if path == "/api/members" and method == "GET":
            rows = c.execute("SELECT * FROM members ORDER BY name").fetchall()
            return 200, {"members": [dict(r) for r in rows]}
        if path == "/api/members" and method == "POST":
            cur = c.execute("INSERT INTO members(name) VALUES(?)", (body["name"].strip(),))
            c.commit()
            return 200, {"id": cur.lastrowid}

        mid = int(q.get("member_id", [0])[0] or body.get("member_id", 0) or 0)

        # --- profil / items ---
        if path == "/api/items" and method == "GET":
            rows = c.execute(
                "SELECT * FROM items WHERE member_id=? ORDER BY kind,created_at DESC", (mid,)
            ).fetchall()
            return 200, {"items": [dict(r) for r in rows]}
        if path == "/api/items" and method == "POST":
            c.execute(
                "INSERT INTO items(member_id,kind,text,visible,source,created_at) VALUES(?,?,?,?,?,?)",
                (mid, body["kind"], body["text"].strip(),
                 int(body.get("visible", body["kind"] == "ofer")),
                 body.get("source", "profil"), date.today().isoformat()),
            )
            c.commit()
            run_matching(c)
            return 200, {"ok": True}
        if path.startswith("/api/items/") and method == "DELETE":
            c.execute("DELETE FROM items WHERE id=?", (int(path.rsplit("/", 1)[1]),))
            c.commit()
            return 200, {"ok": True}

        # --- dictare cu extragere ---
        if path == "/api/dictare" and method == "POST":
            extrase = _naive_extract(body["text"])
            src = f"dictare {date.today().isoformat()}"
            for kind, txt in extrase:
                c.execute(
                    "INSERT INTO items(member_id,kind,text,visible,source,created_at) VALUES(?,?,?,?,?,?)",
                    (mid, kind, txt, int(kind == "ofer"), src, date.today().isoformat()),
                )
            c.commit()
            run_matching(c)
            return 200, {"extrase": [{"kind": k, "text": t} for k, t in extrase]}

        # --- potriviri ---
        if path == "/api/match/run" and method == "POST":
            return 200, {"noi": run_matching(c)}
        if path == "/api/matches" and method == "GET":
            rows = c.execute(
                """SELECT m.*, oi.text offer_text, oi.source offer_source,
                          si.text seek_text
                   FROM matches m
                   JOIN items oi ON oi.id=m.offer_item
                   JOIN items si ON si.id=m.seek_item
                   WHERE (m.offer_member=? OR m.seek_member=?) AND m.status!='respins'
                   ORDER BY m.score DESC, m.id DESC""",
                (mid, mid),
            ).fetchall()
            out = []
            for r in rows:
                latura = "ofer" if r["offer_member"] == mid else "caut"
                eu_consimtit = r["offer_consent"] if latura == "ofer" else r["seek_consent"]
                celalalt = _name(c, r["seek_member"] if latura == "ofer" else r["offer_member"])
                out.append({
                    "id": r["id"], "status": r["status"], "score": r["score"],
                    "latura": latura, "celalalt": celalalt,
                    "offer_text": r["offer_text"], "seek_text": r["seek_text"],
                    "sursa": r["offer_source"], "eu_consimtit": bool(eu_consimtit),
                })
            return 200, {"matches": out}
        if path.startswith("/api/matches/") and path.endswith("/consent") and method == "POST":
            match_id = int(path.split("/")[3])
            return 200, apply_consent(c, match_id, mid, bool(body.get("accept")))

        # --- conexiuni / mesaje ---
        if path == "/api/messages" and method == "GET":
            match_id = int(q.get("match_id", [0])[0])
            rows = c.execute(
                "SELECT * FROM messages WHERE match_id=? ORDER BY id", (match_id,)
            ).fetchall()
            return 200, {"messages": [dict(r) for r in rows], "names": _names_map(c)}
        if path == "/api/messages" and method == "POST":
            c.execute(
                "INSERT INTO messages(match_id,sender,text,created_at) VALUES(?,?,?,?)",
                (int(body["match_id"]), mid, body["text"].strip(), date.today().isoformat()),
            )
            c.commit()
            return 200, {"ok": True}

        # --- sarcini ---
        if path == "/api/tasks" and method == "GET":
            rows = c.execute(
                "SELECT * FROM tasks WHERE member_id=? ORDER BY done,id DESC", (mid,)
            ).fetchall()
            return 200, {"tasks": [dict(r) for r in rows]}
        if path == "/api/tasks" and method == "POST":
            c.execute(
                "INSERT INTO tasks(member_id,text,created_at) VALUES(?,?,?)",
                (mid, body["text"].strip(), date.today().isoformat()),
            )
            c.commit()
            return 200, {"ok": True}
        if path.startswith("/api/tasks/") and path.endswith("/toggle") and method == "POST":
            tid = int(path.split("/")[3])
            c.execute("UPDATE tasks SET done=1-done WHERE id=?", (tid,))
            c.commit()
            return 200, {"ok": True}

        # --- secretara (briefing) ---
        if path == "/api/secretary" and method == "GET":
            tasks = c.execute(
                "SELECT * FROM tasks WHERE member_id=? AND done=0 ORDER BY id DESC", (mid,)
            ).fetchall()
            de_contactat = c.execute(
                """SELECT m.id, m.status,
                          oi.text offer_text, si.text seek_text,
                          m.offer_member, m.seek_member
                   FROM matches m
                   JOIN items oi ON oi.id=m.offer_item
                   JOIN items si ON si.id=m.seek_item
                   WHERE (m.offer_member=? OR m.seek_member=?) AND m.status IN ('propus','conectat')
                   ORDER BY m.status DESC, m.score DESC""",
                (mid, mid),
            ).fetchall()
            contacte = []
            for r in de_contactat:
                latura = "ofer" if r["offer_member"] == mid else "caut"
                celalalt = _name(c, r["seek_member"] if latura == "ofer" else r["offer_member"])
                motiv = (
                    f"{celalalt}: potrivire {'confirmata' if r['status']=='conectat' else 'propusa'} "
                    f"({'tu oferi' if latura=='ofer' else 'tu cauti'})"
                )
                contacte.append({"match_id": r["id"], "text": motiv, "status": r["status"]})
            briefing = _briefing(_name(c, mid), len(tasks), len(contacte))
            return 200, {
                "briefing": briefing,
                "tasks": [dict(t) for t in tasks],
                "contacte": contacte,
            }

        return 404, {"error": "ruta inexistenta"}
    finally:
        c.close()


def _names_map(c: sqlite3.Connection) -> dict:
    return {str(r["id"]): r["name"] for r in c.execute("SELECT id,name FROM members")}


def _briefing(nume: str, n_tasks: int, n_contacte: int) -> str:
    parti = [f"Buna, {nume}!"]
    if n_contacte:
        parti.append(f"Ai {n_contacte} legatura/legaturi de urmarit.")
    if n_tasks:
        parti.append(f"Ai {n_tasks} sarcina/sarcini deschise.")
    if n_tasks == 0 and n_contacte == 0:
        parti.append("Esti la zi. Adauga ce oferi sau ce cauti ca sa gasesc potriviri.")
    else:
        parti.append("Verifica mai jos cu cine merita sa vorbesti azi.")
    return " ".join(parti)


# --------------------------------------------------------------------------- #
# Server HTTP
# --------------------------------------------------------------------------- #
class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, data: dict) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _static(self, path: str) -> None:
        rel = "index.html" if path in ("/", "") else path.lstrip("/")
        full = os.path.abspath(os.path.join(STATIC, rel))
        if not full.startswith(STATIC) or not os.path.isfile(full):
            self.send_error(404)
            return
        ctype = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
        }.get(os.path.splitext(full)[1], "application/octet-stream")
        with open(full, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        u = urlparse(self.path)
        if u.path.startswith("/api/"):
            code, data = api("GET", u.path, parse_qs(u.query), {})
            self._send(code, data)
        else:
            self._static(u.path)

    def _read_body(self) -> dict:
        ln = int(self.headers.get("Content-Length", 0) or 0)
        if not ln:
            return {}
        try:
            return json.loads(self.rfile.read(ln).decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    def do_POST(self) -> None:
        u = urlparse(self.path)
        code, data = api("POST", u.path, parse_qs(u.query), self._read_body())
        self._send(code, data)

    def do_DELETE(self) -> None:
        u = urlparse(self.path)
        code, data = api("DELETE", u.path, parse_qs(u.query), self._read_body())
        self._send(code, data)

    def log_message(self, *args) -> None:  # liniste in consola
        pass


def main() -> None:
    init_db()
    port = int(os.environ.get("PORT", "8000"))
    srv = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"Memorie colectiva — ruleaza pe http://localhost:{port}  (Ctrl+C pentru stop)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nOprit.")


if __name__ == "__main__":
    main()
