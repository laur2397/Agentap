// Memorie colectiva — frontend (vanilla JS)
let ME = null;          // member_id curent
let CHAT_MATCH = null;  // match_id deschis in chat

const $ = (s) => document.querySelector(s);
const api = async (path, opts = {}) => {
  const r = await fetch(path, {
    ...opts,
    headers: opts.body ? { "Content-Type": "application/json" } : {},
  });
  return r.json();
};
const esc = (s) => (s || "").replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));

// ---- membri ----
async function loadMembers() {
  const { members } = await api("/api/members");
  const sel = $("#member");
  sel.innerHTML = members.map((m) => `<option value="${m.id}">${esc(m.name)}</option>`).join("");
  if (!ME && members.length) ME = members[0].id;
  if (ME) sel.value = ME;
}
$("#member").onchange = (e) => { ME = +e.target.value; refresh(); };
$("#addMember").onclick = async () => {
  const name = prompt("Nume membru nou:");
  if (!name) return;
  const { id } = await api("/api/members", { method: "POST", body: JSON.stringify({ name }) });
  ME = id; await loadMembers(); refresh();
};

// ---- tab-uri ----
document.querySelectorAll(".tab").forEach((t) => {
  t.onclick = () => {
    document.querySelectorAll(".tab").forEach((x) => x.classList.remove("active"));
    document.querySelectorAll(".view").forEach((x) => x.classList.remove("active"));
    t.classList.add("active");
    $("#" + t.dataset.tab).classList.add("active");
    refresh();
  };
};

function activeTab() { return document.querySelector(".tab.active").dataset.tab; }

// ---- POTRIVIRI ----
async function loadMatches() {
  const { matches } = await api("/api/matches?member_id=" + ME);
  const box = $("#matchList");
  if (!matches.length) { box.innerHTML = '<p class="empty">Nicio potrivire inca. Adauga ce oferi / ce cauti in Profil.</p>'; return; }
  box.innerHTML = matches.map((m) => {
    const eu = m.latura === "ofer"
      ? `Tu oferi: <b>${esc(m.offer_text)}</b>`
      : `Tu cauti: <b>${esc(m.seek_text)}</b>`;
    const el = m.latura === "ofer"
      ? `${esc(m.celalalt)} cauta: <b>${esc(m.seek_text)}</b>`
      : `${esc(m.celalalt)} ofera: <b>${esc(m.offer_text)}</b>`;
    let jos = "";
    if (m.status === "conectat") {
      jos = `<div class="statusline"><span class="pill conectat">conectat</span>
             <button class="small" onclick="openChat(${m.id})">Deschide conversatia</button></div>`;
    } else if (m.eu_consimtit) {
      jos = `<div class="statusline"><span class="pill propus">propus</span> Ai acceptat — asteptam confirmarea lui ${esc(m.celalalt)}.</div>`;
    } else {
      jos = `<div class="actions">
               <button class="small" onclick="consent(${m.id},true)">Prezinta-ma</button>
               <button class="small ghost" onclick="consent(${m.id},false)">Refuz</button>
             </div>`;
    }
    return `<div class="card match">
      <div class="top"><span class="who2">↔ ${esc(m.celalalt)}</span><span class="pill score">scor ${m.score}</span></div>
      <div class="pair">${eu}</div>
      <div class="pair">${el}</div>
      <div class="src">📌 sursa: ${esc(m.sursa)}</div>
      ${jos}
    </div>`;
  }).join("");
}
async function consent(id, accept) {
  await api(`/api/matches/${id}/consent`, { method: "POST", body: JSON.stringify({ member_id: ME, accept }) });
  loadMatches();
}
$("#rematch").onclick = async () => { await api("/api/match/run", { method: "POST" }); loadMatches(); };

// ---- PROFIL ----
async function loadProfile() {
  const { items } = await api("/api/items?member_id=" + ME);
  const render = (kind, el) => {
    const list = items.filter((i) => i.kind === kind);
    el.innerHTML = list.length ? list.map((i) => `
      <div class="item"><div><div>${esc(i.text)}</div><div class="meta">sursa: ${esc(i.source)}</div></div>
        <button class="x" onclick="delItem(${i.id})">×</button></div>`).join("")
      : '<p class="empty">Nimic inca.</p>';
  };
  render("ofer", $("#oferList"));
  render("caut", $("#cautList"));
}
async function addItem(kind) {
  const text = $("#" + kind + "Text").value.trim();
  if (!text) return;
  const source = $("#" + kind + "Src").value.trim() || "profil";
  await api("/api/items", { method: "POST", body: JSON.stringify({ member_id: ME, kind, text, source }) });
  $("#" + kind + "Text").value = ""; $("#" + kind + "Src").value = "";
  loadProfile();
}
async function delItem(id) { await api("/api/items/" + id, { method: "DELETE" }); loadProfile(); }

// ---- DICTARE ----
async function dicteaza() {
  const text = $("#dictText").value.trim();
  if (!text) return;
  const { extrase } = await api("/api/dictare", { method: "POST", body: JSON.stringify({ member_id: ME, text }) });
  $("#dictResult").innerHTML = "<h3>Extras (salvat in profil):</h3>" + (extrase.length
    ? extrase.map((e) => `<div class="item"><div>${esc(e.text)}</div><span class="badge ${e.kind === "ofer" ? "vis" : "priv"}">${e.kind}</span></div>`).join("")
    : '<p class="empty">Nu am gasit nimic de extras.</p>');
  $("#dictText").value = "";
}

// ---- SECRETARA ----
async function loadSecretary() {
  const d = await api("/api/secretary?member_id=" + ME);
  $("#briefing").textContent = d.briefing;
  $("#contacte").innerHTML = d.contacte.length ? d.contacte.map((c) => `
    <div class="contact"><span>${esc(c.text)}</span>
      ${c.status === "conectat" ? `<button class="small" onclick="openChat(${c.match_id})">Chat</button>` : ""}</div>`).join("")
    : '<p class="empty">Nimic de urmarit acum.</p>';
  $("#tasks").innerHTML = d.tasks.length ? d.tasks.map((t) => `
    <div class="task ${t.done ? "done" : ""}"><input type="checkbox" ${t.done ? "checked" : ""} onchange="toggleTask(${t.id})">
      <span>${esc(t.text)}</span></div>`).join("")
    : '<p class="empty">Nicio sarcina deschisa.</p>';
}
async function addTask() {
  const text = $("#taskText").value.trim();
  if (!text) return;
  await api("/api/tasks", { method: "POST", body: JSON.stringify({ member_id: ME, text }) });
  $("#taskText").value = ""; loadSecretary();
}
async function toggleTask(id) { await api(`/api/tasks/${id}/toggle`, { method: "POST" }); loadSecretary(); }

// ---- CHAT ----
async function openChat(matchId) {
  CHAT_MATCH = matchId;
  $("#chatOverlay").classList.remove("hidden");
  await loadChat();
}
async function loadChat() {
  const { messages, names } = await api("/api/messages?match_id=" + CHAT_MATCH);
  $("#chatMsgs").innerHTML = messages.map((m) => {
    if (m.sender === null) return `<div class="msg app">${esc(m.text)}</div>`;
    const mine = m.sender === ME;
    const who = mine ? "" : `<b>${esc(names[m.sender] || "?")}: </b>`;
    return `<div class="msg ${mine ? "me" : "them"}">${who}${esc(m.text)}</div>`;
  }).join("");
  const box = $("#chatMsgs"); box.scrollTop = box.scrollHeight;
}
async function sendMsg() {
  const text = $("#chatText").value.trim();
  if (!text) return;
  await api("/api/messages", { method: "POST", body: JSON.stringify({ member_id: ME, match_id: CHAT_MATCH, text }) });
  $("#chatText").value = ""; loadChat();
}
function closeChat() { $("#chatOverlay").classList.add("hidden"); CHAT_MATCH = null; refresh(); }
$("#chatText").addEventListener("keydown", (e) => { if (e.key === "Enter") sendMsg(); });

// ---- refresh per tab ----
function refresh() {
  const t = activeTab();
  if (t === "potriviri") loadMatches();
  else if (t === "profil") loadProfile();
  else if (t === "secretara") loadSecretary();
}

// init
(async () => { await loadMembers(); refresh(); })();
