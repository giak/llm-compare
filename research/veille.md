# Veille — LLM & Freebuff

Statut : **◐ amorcée**. Date : 2026-10-06.
Périmètre : **surveiller** ce qui bouge, **expliquer** les mécanismes, **transmettre** des
pratiques. À distinguer du comparatif : ici on documente un *système*, pas un *classement*.

---

## 1. Sources

> ✅ **Premier relevé complet effectué le 2026-10-07 (passe 10)** — `feed.xml` + `feed-models.xml`
> + `llms.txt` + `/plans` + **commits GitHub recoupés un par un** (règle § 4 respectée).
> Ce que ça a donné : 1 retrait de modèle, 2 fin/promos de prix, 1 retrait de badge, 12 releases.
> Détail : `research/trace.md` § Passe 10.

### Freebuff — priorité 1

| Source | Type | Ce qu'elle donne | Fréquence |
|---|---|---|---|
| `freebuff-changelog.nordicnode.workers.dev` | **Tier 2 — miroir de commits** | Tout : diffs GitHub `CodebuffAI/freebuff`, traduits en « plain English », avec lien commit | **quotidienne** |
| ↳ `/models/` | idem | **Frise du catalogue : 20 modèles depuis le 05/08, 12 vivants, 8 retirés**, dates d'entrée/sortie par modèle | idem |
| ↳ `/feed-models.xml` | idem | **RSS des changements de catalogue** — le seul flux à s'abonner si on ne veut qu'une chose | — |
| ↳ `/feed.xml` | idem | RSS de tous les changements (bruyant) | — |
| ↳ `/day/YYYY-MM-DD/` | idem | Le jour, avec diff et permalink | idem |
| `github.com/CodebuffAI/freebuff` | **Tier 1** — source que le miroir reflète | La vérité : lues derrière chaque entrée du changelog | à la main |
| `freebuff.com/llms.txt` | **Tier 1** | Catalogue courant, allocations par pays, règles Freebucks | hebdo |
| `freebuff.com/plans` | **Tier 1** | Heures/jour par modèle, prix relatifs, badges `Promotional` | hebdo |
| `freebuff.com/live` | **Tier 1** | Compteur d'utilisateurs, répartition par pays | hebdo |

**Pourquoi ce changelog en priorité.** Il n'est pas tier 3 : il ne raconte pas, il **diffuse un
commit public** et renvoie au permalink GitHub. Sa force est d'avoir *déjà* rendu lisibles des
choses que je reliserais à la main. Sa limite : c'est un projet tiers, **verrouillé par les
relectures**, corrigeable via issue → `data/overrides.json`. **Recouper avant d'affirmer.**

### LLM — priorité 2 (à construire)

| Source | Ce qu'on en tire |
|---|---|
| `artificialanalysis.ai` | Index, vitesse, coût — **toujours noter la version de l'index** (v4.1.1 vs v4.3.2) |
| `hn.algolia.com/api/v1` | Sentiment développeur, primaire et citable (URL + date + points) |
| Changelogs constructeurs | Release dates, fenêtres promotionnelles |
| Reddit | **API directe en 403** — tier 3 uniquement |
| X / Discord | **non atteints** — trou connu |

---

## 2. Explications à écrire

Les mécanismes que le comparatif *utilise* sans les expliquer. Dans l'ordre d'utilité :

1. **Trois poches d'argent au lieu d'une** — allocation journalière (`daily`), *wallet*
   (Freebucks gagnés), et *sessions*. Le champ `freebucksRefundSources` ajouté le 06/10
   les sépare explicitement `daily` / `wallet`. Conséquence : « il me reste des Freebucks »
   peut vouloir dire trois choses différentes.
2. **Section `unlimited` vs `optimized`** — c'est *ça* qui dit si un modèle est gratuit,
   pas son prix affiché. Code : `common/src/util/freebuff-picker-sections.ts`.
3. **Pourquoi les prix bougent** — *« A model's Freebucks cost can vary »* : ils suivent le
   coût d'exécution du modèle. Un prix gratuit n'est pas une spécification.
4. **Index AA et ses versions** — un même modèle peut valoir 57 ou 42 selon la version de
   l'index. Ce n'est ni une régression ni une erreur de source.
5. **L'effort n'est pas apparié** — comparer `max` à un effort non spécifié n'établit pas
   d'ordre. C'est la réserve C2 du projet.
6. **Abstention ≠ refus** — un modèle qui déclare ses limites n'est pas un modèle qui se
   tait. Voir I4 : mes deux détecteurs ont échoué.

---

## 3. Tips & tricks — ce qui est déjà *prouvé* par le dossier

Rien ici n'est du conseil générique : chaque point est sourcé.

- **Vérifie la date de l'index avant de recouper.** Deux versions en circulation, mêmes
  modèles, chiffres différents. Leçon Passe 6/7.
- **Ne lis pas un champ `parts_json` entier pour mesurer un comportement.** Il mélange
  `reasoning` et `text` : tout détecteur doit filtrer sur `kind='text'`. Sinon on mesure la
  pensée interne, pas la réponse (erreur I4 : 37 % → 9,4 % de faux positifs).
- **Une source qui annonce des allocations périmées a probablement aussi des prix périmés.**
  `mvalentsev` disait 100/70/40, `llms.txt` dit 150/105/60 — et ses tarifs horaires tombent.
- **Un badge `Promotional` veut dire « ça va changer ».** Solar Mini 4 est passé de gratuit à
  payant le **05/10** ; Solar Pro 4 est entré en gratuit le même jour. Deux modèles, deux
  directions, 24 h d'écart.
- **Un modèle peut être *listé* sans être *accessible*** : Gemini 3.8 Flash apparaît dans le
  picker gratuit mais porte `Access = Paid plans`.
- **Un modèle peut changer de valeur sans changer de nom** : MiMo 2.5 → 2.6, GPT-5.6 → 6,
  Muse Spark 1.2 → 1.3. Toute mesure prise avant la bascule ne s'applique plus.
- **Cherche l'existence dans les pages de la plateforme, pas dans la doc upstream** : DeepSeek
  V4.1 Flash Fast n'est documenté nulle part chez DeepSeek, mais listé sur 5 pages Freebuff.
- **Un badge `Promotional` peut ne pas avoir d'échéance.** Solar Pro 4 porte le badge depuis le
  05/10, et le code dit *« A promotion with no end date yet »*. Mon inference « badge = date »
  m'a fait publier une **échéance fausse (09/10)** pendant 3 jours. Le badge dit *« ça peut
  changer »*, **pas « quand »**. *(preuve : `freebuff-solar-promo.ts`, passe 10)*
- **Les prix datés sont dans le dépôt, pas dans `llms.txt`.** `freebuff-solar-promo.ts`
  (`SOLAR_PRICE_CHANGES`) liste chaque bascule de prix avec horodatage, et les fichiers
  `*-promo.ts` donnent le prix courant. C'est la source qui a levé I2/I6 partiellement.
  *(preuve : passe 10)*
- **Les heures de `/plans` recoupent les prix du code.** GLM et DeepSeek affichent **17 h**
  quand MiMo Flash affiche **26 h** — ratio 1,53, soit **15 FB vs 10 FB**. Une table
  d'heures est un second réfecteur de prix, utilisable même quand le prix n'est pas écrit.
  *(preuve : `/plans` + commit `ce46ee14b2a4`, passe 10)*
- **Une promo gratuite a une date, une promo payante n'en a pas toujours.** Solar Mini 4
  (*« Free through Sunday, Oct 4 PT »*) était bornée ; Solar Pro 4 ne l'est pas. Même
  mécanisme, deux promesses différentes. *(preuve : `SOLAR_PRICE_CHANGES`, passe 10)*
- **Un modèle peut disparaître entre deux relevés hebdomadaires.** Space Bunny Alpha a vécu
  **13 jours** (23/09 → 06/10) et est parti **sans préavis**, à cause d'un fournisseur en
  amont (OpenRouter → OpenCode Zen) : le catalogue n'est pas une donnée, c'est un **état**.
  *(preuve : commit `c3edf98738bd`, passe 10)*

---

## 4. Règles de cette veille

- **Mémoire d'abord** avant toute recherche ; **write-back obligatoire** après.
- **Recouper une entrée du changelog sur le commit GitHub** avant de l'affirmer dans le
  comparatif — c'est un miroir, pas une source.
- **Ne pas mélanger deux canaux** : le gratuit Vercel/Ant de Ling n'est pas un Freebudget.
- **Ne pas republier un classement** tant que l'effort AA n'est pas apparié (C2).
- Annoter, **jamais effacer** : une correction s'ajoute, elle ne remplace pas le journal.

---

## Ce qui reste à faire

- [ ] Abonnement RSS `feed-models.xml` — le seul qui vaille le coup.
- [ ] Écrire l'explication 1 et 2 (les trois poches, unlimited/optimized) : elles conditionnent
      tout le budget.
- [ ] Recenser les 8 modèles retirés et leurs dates — base d'une vraie ligne du temps.
- [ ] Lier chaque tip à sa preuve dans le journal (trace.md).
- [ ] Étendre la partie LLM (priorité 2) : sources encore à choisir.
