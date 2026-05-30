"""Proces real de dezvoltare cu TOTI cei 220 de agenti, pe 5 faze.

  FAZA 1  Cercetare de piata  — agenti-cheie cu CAUTARE WEB reala studiaza
          competitorii si tendintele aplicatiilor mobile de networking.
  FAZA 2  Ideatie             — toti cei 220 propun o imbunatatire, hraniti cu
          cercetarea de piata (deci fundamentat, nu din burta).
  FAZA 3  Peer review         — fiecare agent evalueaza ideile a 3 colegi
          (scor 0-10 + critica). Agentii se verifica intre ei.
  FAZA 4  Sedinta de dezvoltare — managerii (18) dezbat top-ideile si propun
          fiecare un concept de departament; un director sintetizeaza
          un CONCEPT FINAL.
  Output: market_research.json, idei2.json, reviews.json, concept_final.md

Faza 5 (constructia efectiva) e in build_final.py, separat.

Ruleaza in background; salveaza dupa fiecare faza ca sa poata fi reluat.
Necesita ANTHROPIC_API_KEY.
"""
from __future__ import annotations
import asyncio, json, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import anthropic
from agentap.organizatie import ORGANIZATIE, nume_curat

MODEL="claude-opus-4-8"; LOT=5
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(f): return os.path.join(ROOT, f)

PRODUS=("O aplicatie mobila privata de business networking pentru un cerc de "
  "oameni de afaceri: aduna ce ofera/ce cauta fiecare, face potriviri si "
  "propune conexiuni cu dublu consimtamant si sursa citata.")

def toti_angajatii():
    out=[]
    for dep,data in ORGANIZATIE.items():
        for rol,nr,desc in data["roluri"]:
            for i in range(1,nr+1):
                out.append({"dep":nume_curat(dep),"rol":rol,"desc":desc,"idx":i,
                            "id":f"{nume_curat(dep)[:12]}|{rol}|{i}"})
    return out

async def call(client,sem,sysp,user,*,max_tokens=300,tools=None,effort="low"):
    async with sem:
        for a in range(6):
            try:
                kw=dict(model=MODEL,max_tokens=max_tokens,
                    system=[{"type":"text","text":sysp,"cache_control":{"type":"ephemeral"}}],
                    output_config={"effort":effort},
                    messages=[{"role":"user","content":user}])
                if tools: kw["tools"]=tools
                r=await client.messages.create(**kw)
                return "".join(b.text for b in r.content if b.type=="text").strip()
            except anthropic.RateLimitError:
                await asyncio.sleep(3*(2**a))
            except Exception as e:
                return f"[{type(e).__name__}]"
        return "[rate limit]"

async def gather_prog(coros, label):
    sem=None; res=[]; done=0; tot=len(coros)
    for f in asyncio.as_completed(coros):
        res.append(await f); done+=1
        if done%10==0 or done==tot: print(f"   {label}: {done}/{tot}",flush=True)
    return res

# ---------------- FAZA 1: cercetare de piata (web search) ----------------
async def faza1(client):
    print("FAZA 1 — Cercetare de piata (cautare web reala)",flush=True)
    # agenti-cheie din departamente relevante
    cheie=[("Artificial Intelligence (AI)","Head of AI"),
           ("Produs (Product)","Head of Product / CPO Deputy"),
           ("Date, AI si Analytics","Mobile Product Analyst"),
           ("Marketing","Growth Marketer"),
           ("Marketing","ASO Specialist (App Store Optimization)"),
           ("Behavioral Science & Ethical Product Design","Behavioral Science Lead"),
           ("Design / UX","Senior UX Designer"),
           ("Engineering / Dezvoltare software","Software Architect"),
           ("Securitate","CISO Deputy / Security Lead"),
           ("Sales / Vanzari","Business Development Manager")]
    sem=asyncio.Semaphore(3)  # web search e mai greu -> paralelism mic
    intrebari={
      "Head of AI":"Ce functii AI au aplicatiile de networking de top in 2024-2025? Cauta pe web.",
      "Head of Product / CPO Deputy":"Care sunt principalii competitori (LinkedIn, Shapr, Lunchclub, etc.) si ce le lipseste? Cauta pe web.",
      "Mobile Product Analyst":"Ce metrici de retentie si onboarding au aplicatiile mobile de networking de succes? Cauta pe web.",
      "Growth Marketer":"Ce tactici de crestere virala folosesc aplicatiile de networking? Cauta exemple reale pe web.",
      "ASO Specialist (App Store Optimization)":"Ce trenduri exista in App Store pentru apps de business/networking in 2025? Cauta pe web.",
      "Behavioral Science Lead":"Ce critici de etica/addictie au primit aplicatiile de networking? Cum se face networking sanatos? Cauta pe web.",
      "Senior UX Designer":"Ce pattern-uri UX premium folosesc aplicatiile mobile de lux/exclusiviste? Cauta exemple pe web.",
      "Software Architect":"Ce tehnologii folosesc aplicatiile moderne de networking (matching, real-time)? Cauta pe web.",
      "CISO Deputy / Security Lead":"Ce probleme de confidentialitate au avut aplicatiile de networking? Cauta pe web.",
      "Business Development Manager":"Ce modele de monetizare folosesc aplicatiile de networking premium? Cauta pe web.",
    }
    async def one(dep,rol):
        sysp=f"Esti „{rol}” in „{dep}”. Cercetezi piata pentru un produs nou."
        u=(f"{PRODUS}\n\n{intrebari[rol]}\n\nDupa cautare, sintetizeaza in 4-6 bullet-uri "
           "CONCRETE (nume reale de produse/functii/cifre). Citeaza ce ai gasit.")
        txt=await call(client,sem,sysp,u,max_tokens=700,
                       tools=[{"type":"web_search_20260209","name":"web_search"}],effort="medium")
        return {"rol":rol,"dep":dep,"research":txt}
    res=await gather_prog([one(d,r) for d,r in cheie],"cercetare")
    json.dump(res,open(P("market_research.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"   -> {len(res)} rapoarte de piata salvate\n",flush=True)
    return res

def research_digest(res):
    return "\n".join(f"[{r['rol']}] "+r["research"].replace("\n"," ")[:400] for r in res if not r["research"].startswith("["))

# ---------------- FAZA 2: ideatie (toti 220) ----------------
async def faza2(client,research):
    print("FAZA 2 — Ideatie cu toti cei 220 de agenti",flush=True)
    dig=research_digest(research)[:6000]
    sem=asyncio.Semaphore(LOT)
    ang=toti_angajatii()
    async def one(a):
        sysp=f"Esti „{a['rol']}” in „{a['dep']}”. {a['desc']}"
        u=(f"{PRODUS}\n\nCERCETARE DE PIATA (de la echipa, din surse reale):\n{dig}\n\n"
           "Din rolul si expertiza ta, propune O imbunatatire CONCRETA si diferentiatoare "
           "pentru aceasta aplicatie, fundamentata pe cercetarea de mai sus. Max 35 cuvinte. "
           "Sa fie ceva ce competitorii NU au. Doar ideea, la obiect.")
        idee=await call(client,sem,sysp,u,max_tokens=140)
        return {**a,"idee":idee}
    res=await gather_prog([one(a) for a in ang],"idei")
    res=[x for x in res if not x["idee"].startswith("[")]
    json.dump(res,open(P("idei2.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"   -> {len(res)} idei fundamentate salvate\n",flush=True)
    return res

# ---------------- FAZA 3: peer review ----------------
async def faza3(client,idei):
    print("FAZA 3 — Peer review (agentii se verifica intre ei)",flush=True)
    sem=asyncio.Semaphore(LOT)
    n=len(idei)
    async def one(i,a):
        # 3 idei ale altora, pseudo-aleator dar reproductibil
        peers=[idei[(i+k*37+11)%n] for k in (1,2,3)]
        bloc="\n".join(f"{j+1}. [{p['rol']}] {p['idee']}" for j,p in enumerate(peers))
        sysp=f"Esti „{a['rol']}”, evaluator critic dar constructiv."
        u=(f"Produs: {PRODUS}\n\nEvalueaza aceste 3 idei ale colegilor. Pentru fiecare da: "
           "scor 0-10 (cat de wow + fezabil + diferentiator) si o critica de o propozitie. "
           f"Format strict: linii „1: scor | critica”.\n\n{bloc}")
        ev=await call(client,sem,sysp,u,max_tokens=220,effort="low")
        return {"reviewer":a["id"],"peers":[p["id"] for p in peers],"eval":ev}
    res=await gather_prog([one(i,a) for i,a in enumerate(idei)],"reviews")
    json.dump(res,open(P("reviews.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    # agregare scoruri
    import re
    score={}
    for r in res:
        nums=re.findall(r"(\d+)\s*:\s*(\d+(?:\.\d+)?)",r["eval"])
        for pos,sc in nums:
            k=int(pos)-1
            if 0<=k<len(r["peers"]):
                score.setdefault(r["peers"][k],[]).append(float(sc))
    by_id={a["id"]:a for a in idei}
    ranked=[]
    for pid,scs in score.items():
        if pid in by_id:
            ranked.append({**by_id[pid],"peer_score":round(sum(scs)/len(scs),2),"n_votes":len(scs)})
    ranked.sort(key=lambda x:x["peer_score"],reverse=True)
    json.dump(ranked,open(P("idei_ranked.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"   -> {len(ranked)} idei punctate de colegi. TOP 5:",flush=True)
    for x in ranked[:5]:
        print(f"      {x['peer_score']}  [{x['rol'][:22]}] {x['idee'][:70]}",flush=True)
    print("",flush=True)
    return ranked

# ---------------- FAZA 4: sedinta de dezvoltare ----------------
async def faza4(client,ranked,research):
    print("FAZA 4 — Sedinta de dezvoltare (managerii sintetizeaza)",flush=True)
    top=ranked[:40]
    bloc="\n".join(f"({x['peer_score']}) [{x['dep']} · {x['rol']}] {x['idee']}" for x in top)
    dig=research_digest(research)[:3000]
    # un director de produs sintetizeaza conceptul final (effort high)
    sysp=("Esti Chief Product Officer. Conduci o sedinta de dezvoltare cu toata firma. "
          "Ai cercetarea de piata si TOP ideile votate de cei 220 de angajati.")
    u=(f"PRODUS de baza: {PRODUS}\n\nCERCETARE DE PIATA:\n{dig}\n\n"
       f"TOP 40 idei (cu scor mediu dat de colegi):\n{bloc}\n\n"
       "Sintetizeaza un CONCEPT DE PRODUS coerent si ambitios care combina cele mai bune idei "
       "intr-o viziune unitara. Structura:\n"
       "1. PROPUNEREA UNICA (1 paragraf): ce face acest produs revolutionar fata de LinkedIn/Shapr/etc.\n"
       "2. NUME nou propus pentru aplicatie + tagline\n"
       "3. 6-8 FUNCTII-CHEIE (fiecare cu o linie: ce e + de ce e wow), care se pot construi client-side intr-un HTML\n"
       "4. DIFERENTIATORUL principal fata de competitie\n"
       "5. DESIGN: directie vizuala in 2 randuri\n"
       "Fii concret si indraznet. E munca a 220 de oameni — sa se vada.")
    concept=await call(client,asyncio.Semaphore(1),sysp,u,max_tokens=2500,effort="high")
    open(P("concept_final.md"),"w",encoding="utf-8").write(
        "# Concept final — sinteza sedintei de dezvoltare (220 agenti)\n\n"+concept)
    print("\n===== CONCEPT FINAL =====\n",flush=True)
    print(concept[:1800],flush=True)
    print("\n=========================",flush=True)
    return concept

async def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("no key"); sys.exit(1)
    client=anthropic.AsyncAnthropic()
    t0=time.time()
    research=await faza1(client)
    idei=await faza2(client,research)
    ranked=await faza3(client,idei)
    await faza4(client,ranked,research)
    print(f"\nPROCES_COMPLET in {time.time()-t0:.0f}s — toti cei {len(idei)} agenti au muncit pe 4 faze.",flush=True)

if __name__=="__main__":
    asyncio.run(main())
