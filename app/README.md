# 🤝 Memorie colectiva si potriviri — prototip v1

Aplicatie web pentru un cerc privat de business: aduna ce ofera / ce cauta
fiecare, face potriviri **in stratul ascuns** si propune conexiuni doar cu
**acordul ambelor parti**, cu **sursa mereu citata**.

> Prototip educativ. **Zero dependinte** — doar Python standard (3.10+).

## Rulare

```bash
python app/server.py
# deschide http://localhost:8000
```

La prima pornire se creeaza `app/data.db` cu cativa membri demo (Ana, Bogdan,
Cristina) si o potrivire „wow” (carbune) deja pregatita. Sterge `app/data.db`
ca sa reincepi de la zero.

## Ce poti incerca

1. **Potriviri** — alege „Esti: Ana”. Vei vedea o potrivire propusa (Bogdan
   ofera carbune, tu cauti carbune), cu sursa citata. Apasa **Prezinta-ma**.
2. Schimba pe **Bogdan** → vede aceeasi potrivire → **Prezinta-ma**. Acum
   ambii au acceptat → se deschide **conexiunea** cu un mesaj de context.
3. **Profil** — adauga ce oferi (vizibil) / ce cauti (privat). Potrivirile se
   recalculeaza automat.
4. **Dicteaza** — scrie cateva fraze; aplicatia extrage ofer/caut (euristica
   simpla, ca demonstratie a fluxului).
5. **Secretara** — briefing, pe cine sa contactezi, sarcini.

## Cum respecta principiile din specificatie

| Principiu | Unde |
|---|---|
| Doua straturi (stie mult / arati cat vrei) | `ce ofer` vizibil vs `ce caut` privat |
| Potrivire in stratul ascuns | `run_matching()` compara intern |
| Consimtamant din ambele parti | fluxul `Prezinta-ma` → confirmare → `conectat` |
| Sursa mereu vizibila | fiecare item are `source`, afisat pe card |
| Om controleaza, AI completeaza | dictarea extrage „sugestii”, omul le tine in profil |

## Limitari (constient prototip)

- Fara autentificare reala (alegi cine esti dintr-un select) — e un cerc privat.
- Extragerea din dictare e pe baza de reguli, nu LLM (vezi `_naive_extract`).
- Potrivirea e pe suprapunere de cuvinte-cheie, nu semantica.
- Stocare in SQLite local, fara migrari.

Acestea sunt exact zonele unde, in v2, intra echipele de **AI** (extragere si
potrivire semantica), **Securitate** (auth, criptare) si **Behavioral Science**
(fluxuri etice de notificare).
