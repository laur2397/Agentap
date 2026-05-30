"""Brief	ul de proiect pe care firma de agenti il are de rezolvat.

„Memorie colectiva si potriviri pentru un cerc de business” — specificatia
completa (concept validat), stocata ca date + un renderer care o transforma
intr-un brief concis, citibil de catre agenti.

Modul *pur* (fara API): poate fi inspectat fara cheie.
"""

from __future__ import annotations

PROIECT: dict = {
    "meta": {
        "nume_proiect": "Memorie colectiva si potriviri pentru un cerc de business",
        "versiune_document": "1.0",
        "limba": "romana fara diacritice",
        "stadiu": "concept validat prin conversatie, inainte de dezvoltare",
        "scop_document": "Specificatie completa care aduna toate deciziile luate despre aplicatie, ca punct de plecare pentru design si dezvoltare",
    },
    "viziune": {
        "rezumat_o_propozitie": "O aplicatie privata pentru un cerc de oameni de afaceri, care aduna informatia generata in discutii (cine ofera ce, cine cauta ce), o intelege si face proactiv legaturi intre membri, cu tact si cu acordul fiecaruia.",
        "ton_produs": "Un intermediar discret si de incredere, ca un om respectat din grup care face cunostinta intre oameni doar cand amandoi sunt de acord. Nu o baza de date rece, ci relatii facute cu tact.",
        "metafora": "Memoria colectiva a grupului plus un facilitator de conexiuni.",
    },
    "problema": {
        "context": "Un grup de prieteni se intalneste periodic pentru networking, dezbateri de idei de business, schimb de contacte, negocieri si intermedieri.",
        "durere_principala": "Se genereaza permanent informatie valoroasa, dar se pierde. Oamenii sunt ancorati in prea multe lucruri si uita ce s-a discutat.",
        "exemple_concrete": [
            "Cineva spune ca are un furnizor de carbune, dar acum 5 luni altcineva mentiona o cariera de carbune si nu mai stii cine.",
            "Cineva are atat de multe apeluri incat pierde informatii utile si nu le poate retine sau conecta.",
        ],
        "unde_se_pierde_informatia": [
            "In timpul conversatiei (esti in apel sau la o intalnire si nu apuci sa notezi)",
            "Dupa conversatie (ai notat undeva, dar nu mai gasesti sau nu mai stii unde)",
            "In grupurile de chat unde se discuta cateva zile si apoi totul ramane in aer",
        ],
    },
    "utilizatori": {
        "tip": "La granita dintre consumator si profesionist; oameni care fac afaceri si relationare in mod activ",
        "faza_initiala": "Un cerc privat, grupul propriu al fondatorului",
        "evolutie": "Daca functioneaza, se deschide spre mai multe comunitati / o retea de business mai mare",
    },
    "principii_fundamentale": [
        {"nume": "Doua straturi de informatie", "descriere": "Aplicatia stie mult despre fiecare (ca sa fie utila), dar fiecare decide ce se vede despre el."},
        {"nume": "Potrivire in stratul ascuns", "descriere": "Compararea ce-ofera vs ce-cauta se face intern; omul afla de o potrivire doar la momentul potrivit."},
        {"nume": "Consimtamant din ambele parti", "descriere": "Nicio conexiune nu se deschide automat. Aplicatia intreaba intai fiecare parte."},
        {"nume": "Doar membri din interior", "descriere": "Se potrivesc doar oameni care sunt membri si au acceptat. Persoanele pomenite raman nota personala."},
        {"nume": "Sursa mereu vizibila", "descriere": "Cand aplicatia propune ceva, arata de unde stie (ex: din dictarea din 3 martie)."},
        {"nume": "Omul controleaza, AI completeaza", "descriere": "Utilizatorul marcheaza ce e important; ce prinde AI singur sta separat ca sugestii de verificat."},
        {"nume": "Crestere organica prin invitatii", "descriere": "Cand cineva are o resursa buna dar nu e membru, ai un motiv real sa-l inviti."},
    ],
    "functionalitati": {
        "1_aduna_informatia": "Combustibilul aplicatiei: chat/grupuri native, note rapide cu marcaj, dictare scurta dupa apel (NU inregistrare live in v1).",
        "2_intelege_informatia": "Creierul: pentru fiecare intrare, AI extrage CE OFERA si CE CAUTA. Ce marcheaza omul = important; ce prinde AI = sugestii separate.",
        "3_face_legaturile": "Momentul wow: reactiv (intrebi) si proactiv (semnaleaza singura). Flux cu dublu consimtamant si sursa citata, apoi chat cu context.",
        "4_invata_in_timp": "Dupa o conexiune intreaba 'a iesit ceva?' si prioritizeaza tipurile de potriviri care dau roade.",
        "5_secretara_personala": "Asistent AI personal: briefing zilnic, sarcini/follow-up, pe cine sa contactezi, chat care poate crea sarcini.",
    },
    "profil_utilizator": {
        "ce_ofer": "Vizibil celorlalti (control pornit/oprit pe element). Ex: cariera de carbune, spatii comerciale.",
        "ce_caut": "Privat by default, folosit doar pentru potriviri ascunse. Ex: investitor, contabil.",
        "principiu": "Aplicatia stie tot ca sa te ajute. Tu decizi ce vede fiecare despre tine.",
    },
    "ecrane": [
        {"nume": "Potriviri", "rol": "Inima produsului — legaturile propuse cu motiv, sursa si butoane Prezinta-ma/Refuz.", "prioritate": "esential v1"},
        {"nume": "Grupuri", "rol": "Chat si grupuri native unde se discuta.", "prioritate": "esential v1"},
        {"nume": "Dicteaza dupa apel", "rol": "Captarea wow: dictezi, AI extrage ofer/caut + rezumat.", "prioritate": "esential v1"},
        {"nume": "Secretara", "rol": "Asistent personal: tablou de bord + chat care adauga sarcini.", "prioritate": "esential v1"},
    ],
    "plan_de_lansare": {
        "faza_1": {
            "scop": "Validare in grupul propriu",
            "intrebare_de_validat": "Oamenii chiar pun informatie in aplicatie si chiar le plac potrivirile?",
            "include": [
                "Chat / grupuri native",
                "Note scrise cu marcare a ce e important",
                "Profil cu ce ofer / ce caut si control pe vizibilitate",
                "Dictare dupa apel cu extragere AI (forma simpla)",
                "Potrivire de baza plus fluxul 'vrei sa te prezint?'",
                "Secretara personala",
            ],
        },
        "faza_2": {
            "scop": "Crestere, daca faza 1 are succes",
            "include": [
                "Inregistrarea live a intalnirilor fata in fata",
                "Feedback-ul 'a iesit ceva?' si invatarea automata in timp",
                "Deschiderea spre mai multe comunitati",
            ],
        },
    },
    "decizii_amanate": [
        "Inregistrarea audio live a unei mese intregi (amanata pe faza 2)",
        "Gestionarea persoanelor pomenite dar nemembre",
        "Model de monetizare (neabordat)",
        "Platforma tehnica concreta si arhitectura (neabordate)",
    ],
    "riscuri": [
        {"risc": "Captarea informatiei e prea greoaie", "mitigare": "Dictare simpla dupa apel + chat nativ"},
        {"risc": "AI marcheaza prea mult automat", "mitigare": "Sugestiile automate stau separat"},
        {"risc": "Expunere fara acord la conexiuni", "mitigare": "Consimtamant din ambele parti"},
        {"risc": "Informatie despre persoane din afara", "mitigare": "Doar membri din interior intra in potriviri"},
    ],
}


def brief_text() -> str:
    """Randeaza specificatia intr-un brief concis si citibil pentru agenti."""
    p = PROIECT
    L: list[str] = []
    L.append(f"PROIECT: {p['meta']['nume_proiect']}")
    L.append(f"STADIU: {p['meta']['stadiu']}")
    L.append("")
    L.append(f"VIZIUNE: {p['viziune']['rezumat_o_propozitie']}")
    L.append(f"TON PRODUS: {p['viziune']['ton_produs']}")
    L.append("")
    L.append(f"PROBLEMA: {p['problema']['durere_principala']}")
    L.append("Unde se pierde informatia:")
    L += [f"  - {x}" for x in p["problema"]["unde_se_pierde_informatia"]]
    L.append("")
    L.append(f"UTILIZATORI: {p['utilizatori']['tip']} | start: {p['utilizatori']['faza_initiala']}")
    L.append("")
    L.append("PRINCIPII FUNDAMENTALE:")
    L += [f"  - {pr['nume']}: {pr['descriere']}" for pr in p["principii_fundamentale"]]
    L.append("")
    L.append("FUNCTIONALITATI:")
    L += [f"  - {k}: {v}" for k, v in p["functionalitati"].items()]
    L.append("")
    L.append("PROFIL UTILIZATOR:")
    L.append(f"  - Ce ofer: {p['profil_utilizator']['ce_ofer']}")
    L.append(f"  - Ce caut: {p['profil_utilizator']['ce_caut']}")
    L.append("")
    L.append("ECRANE (v1):")
    L += [f"  - {e['nume']}: {e['rol']}" for e in p["ecrane"]]
    L.append("")
    L.append("PLAN DE LANSARE:")
    L.append(f"  Faza 1 ({p['plan_de_lansare']['faza_1']['scop']}): " + "; ".join(p["plan_de_lansare"]["faza_1"]["include"]))
    L.append(f"  Faza 2 ({p['plan_de_lansare']['faza_2']['scop']}): " + "; ".join(p["plan_de_lansare"]["faza_2"]["include"]))
    L.append("")
    L.append("RISCURI CUNOSCUTE:")
    L += [f"  - {r['risc']} -> mitigare: {r['mitigare']}" for r in p["riscuri"]]
    L.append("")
    L.append("DECIZII AMANATE / DE CLARIFICAT:")
    L += [f"  - {x}" for x in p["decizii_amanate"]]
    return "\n".join(L)


if __name__ == "__main__":
    print(brief_text())
