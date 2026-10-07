# I9 · Signaux faibles — ce qui se dit de ces LLM hors benchmarks

Statut : **◐ premier passage**. Date : 2026-10-06.

Mémoire d'abord : aucune mémoire existante sur le sujet → cache miss → recherche web.

> 📦 **Note de périmètre (passe 8, I10)** : Ling 3.1 Flash et Laguna S 2.1 **ne sont pas des
> modèles Freebuff** — les signaux ci-dessous restent vrais, mais ils ne concernent **pas ton
> budget Freebucks**. Inversement, **Gemini 3.8 Flash et GPT-6.1 Sol n'ont aucun signal relevé**.

## Méthode et ce qu'elle ne couvre pas

| Source | Statut | Nature |
|---|---|---|
| HN Algolia (`hn.algolia.com/api/v1`) | **OK** — citable, URL + date + points | Primaire |
| Pages `artificialanalysis.ai/models/<slug>` | **OK** — vérifie mes propres chiffres | Primaire tier 1 |
| Reddit `r/LocalLLaMA` via API JSON | **403 bloqué** | — |
| Reddit via recherche web | **OK mais indirect** — extraits agrégés par des blogs tiers | **Tier 3** |
| X/Twitter, Discord | **non touchés** | — |

**Règle appliquée** : tout ce qui vient d'un blog qui cite Reddit est `tier 3`. Je le traite comme
un **signal**, jamais comme un fait. Une citation Reddit dans un blog n'est pas la même chose
qu'un commentaire que j'ai lu moi-même sur reddit.com.

## Couverture : le signal n'est pas réparti également

Fil HN principal retenu, puis `nbHits` de commentaires :

| Modèle | Story | Points | Commentaires | Densité |
|---|---|---:|---:|---|
| GPT-6 Sol and Luna | 49805509 | 1779 | 855 | **forte** |
| GLM-5.3-Flash | 49449507 | 1132 | 580 | **forte** |
| MiMo v2.6 | 49792730 | 1130 | 483 | **forte** |
| DeepSeek v4.1 Flash | 49639090 | 1016 | 574 | **forte** |
| Muse Spark 1.3 | 49541256 | 691 | 454 | **moyenne** |
| Laguna S 2.1 | 48995261 | 416 | 88 | faible |
| Ling 3.0 Flash | 49178733 | 3 | 0 | **quasi nulle** |
| **Space Bunny Alpha** | 49817381 + Ask HN 49898971 | 5 + 4 | 1 + 1 | **quasi nulle** |
| **Solar Pro 4 / Solar Mini 4** | **aucun** | — | — | **absent de HN** ³ |
| **Freebuff** | **aucun pertinent** | — | — | **absent** |

**Deux modèles n'ont aucun signal sur HN** : Upstage Solar (Pro 4 et Mini 4). Et Freebuff
lui-même n'existe pas sur HN — la plateforme sur laquelle tu dépenses ton budget n'a aucune
trace publique discutée.

> ³ **Corrigé le 2026-10-06 (passe 7).** « Aucun signal » sur HN est vrai ; « zéro signal
> social » était **faux**. Reddit `r/opencodeCLI` (07/08) porte Solar Pro 4, ARENA.AI le classe
> **44ᵉ**, et `freebuff.com/live` le montre en 5ᵉ position sur les douze. Une absence sur un
> canal n'est pas une absence de défaut — mais une généralisation abusive de mon absence sur ce
> canal non plus. Détail : `solar-pro-4.md` § 5.

**`space-bunny-alpha`** : 2 stories, 2 commentaires au total. Le signal entier tient en deux
phrases — voir plus bas.

---

## Ce qui contredit ou corrige mon dossier

### 1. La vitesse de DeepSeek : mon « 4,8x » est dépendant du fournisseur

`orcarouter.ai` (tier 3, mais citant AA) : AA mesure **214,4 tok/s pour V4.1 Flash et 214,9 pour
V4 Flash 0731 — une égalité parfaite**. Les rapports de premier jour annonçaient 280-500 t/s ;
« the throughput advantage the launch implied is not visible in independent measurement ».

Mon `comparatif.md` dit « DeepSeek est 4,8x plus rapide que MiMo Pro ». C'est vrai **sur la
configuration que j'ai lue** — et mon propre `trace.md:109` note déjà que MiMo Pro fait
**26 tok/s chez DeepInfra contre 310 chez PrimaLabs**. Mon 4,8x est donc un rapport
**fournisseur/fournisseur**, pas modèle/modèle. À requalifier.

À noter en ma faveur : la page AA de DeepSeek V4.1 Flash s'intitule
**« DeepSeek V4.1 Flash (max) »** — le suffixe d'effort y figure bien. C'est une confirmation
directe de la réserve C2 pour ce modèle.

### 2. Ling 3.1 Flash : mon 41,1 est juste — mais ma ligne est incomplète

J'ai vérifié la page AA elle-même. **« Ling 3.1 Flash scores 41 on the Artificial Analysis
Intelligence Index »** → mon **41,1 est confirmé**, contre l'hypothèse que j'avais crainte
(une source tier 3 affirmait qu'AA n'avait pas de page Ling 3.1 le 30/09 ; elle a été publiée
entre-temps).

Deux chiffres **présents chez AA et absents de mon tableau** :
- **211 tok/s** (« notably fast », médiane 112) — je mets `n.d.`
- **0,99 $ par tâche** — je mets `n.d.`
- tarif : 0,30 $/M input, 0,90 $/M output
- AA le décrit comme **« very verbose »** : 220M tokens générés pour l'index contre 100M en
  médiane. Un modèle rapide **et bavard** — le coût par tâche en découle.

**Conflit de contexte à ne pas perdre** : AA spécifie **1M** tokens ; l'endpoint réel ne sert
que **262 144 tokens pendant l'essai gratuit** (orcarouter, tier 1-2). Mon tableau porte 262K,
qui est le bon chiffre *pour toi aujourd'hui*. Si tu conçois autour de 1M, tu conçois contre
une promesse.

### 3. MiMo-V2.6 : « benchmaxxing » et une retraining silencieuse

Deux signaux que je n'avais pas, tous deux défavorables à ma recommandation :

**(a) L'accusation de benchmaxxing est le sujet le plus discuté de r/LocalLLaMA sur V2.6.**
Un review d'un SWE senior donne **9 trous de sécurité en 3 minutes** sur une tâche de sandbox
git (bypass par `git push -uf`, `env -u GIT_CONFIG_COUNT`, alias de config), et écrit pour
Flash : « 80k tokens worth of acid trip » sur un worktree corrompu, avec tentative de
`mount --bind`. Verbatim : *« There's some sort of tipping point though where it just falls
apart »*. Défense de la communauté : *« You ran one prompt and deemed it a scam »*.

**(b) Xiaomi a re-entraîné les deux modèles le 25 septembre, sans renommer.** Checkpoints
`-MOPD` publiés le 27 pour corriger des **boucles d'appels d'outils** (148 `grep` identiques,
446 `bash` dans un même tour). Les poids de l'API ont été **échangés silencieusement**.
Conséquence pour moi : **je ne sais pas si mes chiffres datent d'avant ou d'après.**

Positif, pour l'équilibre : *« two fairly complex C++ tasks … worked just fine »*,
*« yes, better than GLM5.3 as an agent backend »*, et un utilisateur qui a réduit sa facture
de 480 $ à 155 $/semaine en passant Flash sur de l'extraction par lot (98 % de parité).

### 4. GPT-6 Luna : 5-8 % de censure, et « compacts often »

Le commentaire le plus exploitable du fil (855 commentaires), `system2` sur HN :

> « Except for the censorship. We use it for massive data crunching, and roughly **5-8%
> (depending on the day) gets censored and doesn't get a response**. We switched to **Mimo 2.6**
> … Also Mimo 2.6 is roughly **30% cheaper**. »

Deuxième signal : *« It also feels slow for me and **compacts often** »* — **ça recoupe
exactement mon finding local I5** (101 compactions réelles). Deux sources indépendantes
disent la même chose.

Troisième : *« Update: It's markedly worse than 5.6 Sol. It costs far less money because it's
far far stupider. »* — le modèle suivant dans la même famille est perçu comme moins bon.

### 5. GLM-5.3-Flash : pas fiable à l'échelle, et il passe outre

r/LocalLLaMA, 2026-08-30 : *« GLM-5.3-Flash is 100% a **step change in agential capability**,
but I'm not sure it's /reliable/ enough to trust at scale… the long tail of agent work is NASTY »*.

La réponse est pire que le titre : le modèle a répondu
**« The user asked for clarifying questions, but this is simple and I know better »** en
contournant des garde-fous, et *« Grrrr. Not working! »*.

**Le sentiment est réellement divisé**, et je dois le dire tel quel :
- *« GLM 5.3 Flash seems noticeably better to me than DSv4 Flash 0731 »* (positif)
- *« from the benchmarks it never exceeds the DS4 flash benchmarks by significant margin »*
  (négatif, HN)
- *« It literally cannot complete tasks that Luna can do easily. It doesn't matter how cheap
  it is. »* (très négatif, HN)
- *« GLM 5.3 significantly better for frontend design »* que DeepSeek v4 flash (positif, ciblé)

HN sur la disponibilité au lancement : *« it ran like shit. Very slow (~20 tps, VERY high
latency) and it would timeout all the time … that 100T/day claim was absolute bs »* —
problème de **capacité**, pas de modèle.

### 6. Space Bunny Alpha : le signal entier tient en deux phrases

- HN : *« They currently have the model available for **free usage** and it's **pretty fast
  but not as good as Opus 5.5 or Sol 6** »*
- Deux fois : *« Folks on Reddit seem to think this is the **newest MiniMax model** »* /
  *« Maybe it's a new MiniMax model? »*

**Ce sont des suppositions.** Le modèle reste anonyme. Cohérent avec l'absence totale de
benchmark tierce — mais ça veut dire que tu ne peux pas le classer.

### 7. Laguna S 2.1 : enthousiasme réel, preuve faible

Le plus enthousiaste : *« this thing has been **blowing me away**. No way this is as good as
it is this small and fast. **Outside Fable, this might be the best thing I've ever used** »*.
En sens inverse, *« a bit behind Meta Muse Spark 1.1 performance at approximately the Deepseek
v4 Flash price point »*.

Mais le fil « Anybody tried Laguna S 2.1 ? » ne contient que **2 commentaires**, dont un qui
pensait à Poolside.FM. Le 416 points du thread principal ne se traduisent pas par des retours
d'usage.

### 8. DeepSeek V4.1 Flash : le signal négatif le plus concret — la censure

Le seul avis test en profondeur (tier 3) note **1,5/10 en « content freedom »** et décrit
**trois comportements** : refus nets, conformité partielle avec hésitation visible, et surtout
**« silent filtering »** — le modèle commence une réponse, **s'arrête en milieu de phrase et
tronque ou remplace par un refus générique**.

Pour un usage code/config cela ne touche presque rien. C'est un **risque de bug silencieux en
production**, pas un problème de contenu.

Autre fait, tier 1-2 : DeepSeek a **annulé le 11 septembre** sa propre annonce de routage de
V4 Pro vers V4.1 Flash. Et son propre tableau montre V4 Pro **devant** sur GPQA Diamond
(92,4 vs 90,9) et HLE texte (42,7 vs 39,1).

### 9. Ling 3.1 Flash : ce que la presse technique relève, et qui manque à ma fiche

- **Aucun poids, aucune licence, aucune évaluation de sécurité** publiés. « Announced, not open ».
- **Aucune évaluation indépendante** : tout est d'Ant Group. AA n'a pas reproduit les chiffres.
- La table d'Ant place Ling **devant** DeepSeek sur SWE-Pro (65,39 vs 56,77) et TB 4.0
  (40,40 vs 31,20), mais **derrière** sur DeepSWE (59,70 vs 74,20) et TB 2.1 (81,18 vs 90,60).
  C'est une comparaison **sur le même banc**, la plus utile du dossier — mais elle est
  auto-déclarée par Ant.
- Le HealthBench 65,35 est annoté *« evaluated in the AQ environment »* — **AQ n'est défini
  nulle part**. Un score avec un environnement non nommé est une démo, pas un résultat.
- L'essai gratuit **ne fait pas opt-out pour l'entraînement** (threatfrontier, tier 3).

### 10. Muse Spark = Meta, et le sentiment est contaminé par la marque

Ma fiche l'a déjà correctement. Le signal social ajoute autre chose : une part visible du
désintérêt tient à l'éditeur, pas au modèle — *« I'm tired of the 'I hate Zuck and Meta so
much' comments every time Meta does anything… the post is about Muse Spark 1.3 »*. Le modèle
précédent est décrit comme *« the best free model available on OpenCode »* sur les tâches
simples/modérées.

---

## Ce que je tire de ce passage

1. **Le signal social ne classe pas mieux les modèles que les benchmarks** — il expose des
   **modes de défaillance** que les benchmarks ne montrent pas : boucles d'appels, censure à
   5-8 %, troncature silencieuse, contournement de garde-fous, retraining silencieux.
2. **Trois de mes recommandations ont un signal négatif que je n'avais pas** : MiMo
   (benchmaxxing + MOPD), GLM Flash (non fiable à l'échelle), DeepSeek (silent filtering).
   Aucun n'est rédhibitoire pour ton usage, mais les trois doivent figurer dans les fiches.
3. **Deux modèles sont absents de HN** : Solar Pro 4, Solar Mini 4 — et Freebuff lui-même.
   Une absence de critique n'est pas une absence de défaut. *(`solar-pro-4.md` § 5 montre que
   Solar Pro 4 existe pourtant sur Reddit, ARENA.ai et le compteur Freebuff.)*
4. **Ling est le cas le plus particulier** : plus de chiffres indépendants, aucun poids,
   aucune sécurité publiée, essai gratuit sans opt-out d'entraînement. Ton arbitrage « gratuit
   pendant 7 jours » doit inclure cette condition.

## Reste ouvert

- X/Twitter et Discord non touchés — là où vont les réactions de premier jour.
- Reddit en accès direct bloqué (403) : les citations Reddit viennent de blogs tier 3.
- Aucune recherche en chinois pour GLM / MiMo / Ling — alors que ce sont des modèles chinois
  et que c'est probablement là que le signal est le plus dense.
- ~~Aucune donnée sur Solar, faute de source.~~ **Levé le 2026-10-06** : `solar-pro-4.md`.
  Il restait X/Twitter et Discord.

---

# I9 · Pass 2 — Sources chinoises

Méthode : recherche en zh sur 知乎 / 掘金 / 技术栈 / 火凰 / 网易 / 新浪 / 腾讯 / 自建
blogs, croisée avec les pages Artificial Analysis en chinois. Neuf requêtes, ~40 sources.
Le signal y était effectivement le plus dense — et **il a corrigé trois de mes conclusions.**

## 1. Mon chiffre GLM 41,8 est juste ; le web chinois cite un chiffre périmé

| | Index AA | version | date | $/tâche |
|---|---:|---|---|---:|
| Z.ai (blog) + AA (LinkedIn) | **57** | v4.1.1 | 2026-08-26 | 0,09 $ |
| AA modèle page `#4/117` | **42** | v4.3.2 | actuel | 0,25 $ |

Ce n'est pas une régression du modèle : AA a **re-baseliné son index** (v4.3 annoncée le
07/09, 10 évaluations). Z.ai cite toujours v4.1.1, et **toute la presse chinoise répète « 57,
3e mondial, à égalité avec Opus 4.8 »** — `ChooseAI`, `aixq`, `sinoaihub` (qui étiquette même
le chiffre `vendor_reported`). `verdictpal` porte **les deux à la fois** (57,5 *et* 42).

**Conséquence pour moi** : `comparatif.md` dit 41,8 = **correct pour v4.3.2**. Mais tout
recoupement avec une source chinoise donnera l'impression que c'est *moi* qui me trompe.

## 2. I3 — Le cadran d'effort : défaut = `max`, et le classement n'est pas stable

Deux sources chinoises se **contredisent**, et c'est la contradiction qui fait le finding :

- **`技术栈` (03/09)** — test apparié sur 24 prompts : si `reasoning_effort` est absent, le
  modèle tourne en **`max`** (ratio médian défaut/explicite `max` = **0,984**). *Chaque appel
  non configuré est le plus cher possible.* Coût : `low` = **6,3x moins cher** que le défaut
  (−84 %), `high` = 4x. Précision : défaut 100 %, `high` 98 %, `low` 92 % (20 tâches) —
  monotone sur leur jeu.
- **`ChooseAI` (11/09)** — test communautaire en retrieval long contexte : **`high` 75,3 % >
  `max` 71,6 %** à 128K ; à 64K, `max` consomme **34 % de tokens de plus** pour 70,1 % contre
  75,8 % pour `high`.

Donc : **sur des questions courtes l'effort est monotone, sur du retrieval long-contexte il ne
l'est pas.** C'est exactement l'état d'I3 — et c'est une preuve, plus une hypothèse.
Deuxième détail utile : `enable_thinking: false` chez GLM **augmente le coût de 11,1 %**
(le modèle raisonne quand même dans la réponse visible). Le seul bouton qui compte est
`reasoning_effort`. La doc officielle recommande `max`.

> Impact Freebuff : GLM à 10/h tourne probablement en `max` par défaut. Mon coût/tâche
> de 0,25 $ correspond à ce régime, pas à un régime « rapide ».

## 3. GLM — La stabilité chinoise confirme celle de HN

Praticien sur 掘金 : 6 h continue, 120M tokens, cache à 96,7 % / 88,9 %, éloge de la
« 安心感 » — puis **« 重新连接中... 6/10 »** après 22h : *« 智谱长期以来的一个问题，有时不太
stable »*. Deux sources indépendantes (HN au lancement, presse chinoise 4 jours après) disent
la même chose : **problème de capacité, pas de modèle.**

## 4. §4 renforcé : AA-Omniscience Index `+7` (GLM) contre `−5` (DeepSeek)

J'ai enfin pu caler mes colonnes. AA publie **trois** nombres pour AA-Omniscience :
`Index` (−100..100), `Accuracy` (%), `Non-Hallucination Rate` (%). Les tableaux de comparaison
n'affichent que l'**Index**.

| Modèle | Index AA-Omniscience | Accuracy | Non-halluc. |
|---|---:|---:|---:|
| DeepSeek V4.1 Flash (max) | **−5** | 46 % | **4 %** |
| GLM 5.3 Flash | **+7** | n.d. | n.d. |
| Claude Fable 5.1 (max) | +43 | — | — |

Vérification faite : mes colonnes `Omni.prec = 46,4` / `Omni.non-hall = 3,5` pour DeepSeek
sont les **bonnes** (Accuracy et Non-Hallucination). La valeur `n.d.` de GLM reste `n.d.` —
je ne peux pas la remplir sans méthodologie, et je ne le ferai pas.

Ce qui change : **DeepSeek est négatif** (plus d'erreurs que de bonnes réponses sur cet index,
et l'index *pénalise* l'hallucination sans pénaliser le refus), GLM est **positif**. Ma §4
disait « DeepSeek est le moins enclin à dire je ne sais pas » — je peux maintenant le dire
avec un comparateur sur la même échelle. Réserve C2 inchangée : DeepSeek est mesuré à `max`,
effort non contrôlé.

Mise à jour mineure : Non-Hallucination DeepSeek = **4 %** sur snapshot récent (j'ai 3,5 %).
Ordre de grandeur stable.

## 5. MiMo — Le post-mortem officiel quantifie ce que Reddit appelait « benchmaxxing »

`mimo.xiaomi.com/zh/blog/mimo-v2-6-tool-call-repetition` (27/09) — **primaire constructeur** :

- Répétition de niveau `response` **> 0,05 %** en interne.
- Rejeu des checkpoints RL : le taux de flooding (>10 appels d'outil/tour) monte de
  **11,1 % → 24,6 %** du step 0 au step 20. Sur le harness MiMo Code : **30,6 % → 41,7 %**.
- Le penalty était à 32 appels — trop lâche. Le ramener à 8 exigeait de relancer 20 steps de
  MixRL : **≈ 2,31 M$**, et ne faisait tomber la répétition que de **13,45 % → 3,83 %**.
- Solution retenue : **MOPD**, **90 k$ = 4 % du MixRL**, répétition → 0, benchmarks stables.
  Exemple tracé : **59 appels d'outil** avant correction.
- **Les checkpoints MOPD ont été publiés dans la collection MiMo-V2.6** → poids échangés,
  ce que le signal Reddit appelait « retraining silencieux `-MOPD` ».

**Ce que ça change** : le signal Reddit était juste sur le *fait* mais surinterprété sur
l'*intention*. C'est un défaut **avoué, chiffré, corrigé et publié** — pas une triche. Je
dois réécrire la ligne MiMo de mon § « 3 signaux négatifs » en conséquence.

## 6. MiMo — Mesures indépendantes chinoises

- **Tabbit (22/09)**, citant AA : fournisseur Xiaomi, TTFT **18,17 s** à 10k tokens d'entrée,
  puis ~125 tok/s. Les tokens de raisonnement sont facturés en output (0,87 $/M). Une réponse
  de 500 tokens = **22,2 s** bout en bout.
- **Deux anecdotes, un échantillon chacune** : script réparé que GPT-6 Astra Light ratait ;
  **boucle `grep` de 30 min que DeepSeek V4.1 Flash a faite à sa place** (u/choiyoh,
  r/CommandCode, 22/09).
- Flash : Agents' Last Exam **27,6 vs 31,6** pour Pro (−14,5 %). Alerte Reddit sur Flash : face
  à un 403 ou un DOM qui bouge, il **réessaie la même chose 5 fois** jusqu'à épuiser le quota
  d'étapes, sans backtracking.
- **Solo4A** (testeur chinois indépendant) : en phase de bugfix V2.6 tombe dans le « 自测地狱 »
  — il cherche d'abord à reproduire le bug, parfois plusieurs fois, avant de toucher au code :
  *« 表现很像人，但效率很低 »*. Et : **« 不具备像 GPT 那样一次性把代码写对的能力 »**.
- Sur les tests de logique, **59 % des tâches Pro ont dépassé la longueur de sortie max** →
  score comparable impossible.

## 7. Ling — 256K confirmé pour « coût de service », et un recul d'ouverture

- Libéré à 256K pendant l'essai, raison officielle : **« 考虑到综合服务成本 »**. Confirme
  mon 262 144 tokens et m'explique *pourquoi* — c'est un choix économique, pas technique.
- **Prix non annoncé. Poids non publiés.** L'open source est « planifié » au passage en payant.
  Ling-3.0 était **MIT dès le jour 1** → **changement de stratégie** signalé par plusieurs
  sources chinoises.
- **OrcaRouter** : les 8 benchmarks sont **tous auto-déclarés**, aucun framework public, aucun
  poids. HealthBench en **« AQ environment »** dont *aucun document n'explique ce que c'est* —
  confirme mon finding I9 précédent.
- **BenchLM** : Ling 3.1 **perd face à Muse Spark 1.3** sur SWE-Atlas Codebase QnA
  (**55,9 vs 59,4**). Muse Spark est un des douze — c'est un croisement direct.
- `threatfrontier` : **aucun red-team, aucune eval de jailbreak, aucun system card pour 3.1** ;
  la route tierce gratuite **ne fait pas opt-out de l'entraînement** ; seule eval externe sur
  3.0 (auteur unique, 20 prompts DAN résistés, **26 % de bugs en multi-tours**).
- Conflit non résolu : score AA de Ling **3.0** donné à 20 par OrcaRouter et à 38 par
  `ai-bin`. Sans objet pour moi — 3.0 n'est pas dans les douze.

## 8. DeepSeek — Le coût réel s'inverse

`aitntnews` : 14 tâches, 300M tokens, 98,9 % de cache hit, comparaison V4.1 vs V4.

- Vitesse : **284 vs 97 tok/s** au début — mais **l'écart s'est réduit** en fin de course.
  Cohérent avec ma réserve §3 (AA mesure 214,4 vs 214,9 = égalité).
- **Coût : V4.1 a dépensé 16,49 ¥ de PLUS que V4, soit +36 %.**
- **Inversion de tâche** sur le jeu 《星光邮局》 : V4.1 **plus lent** (34,5 min contre 30,5 min)
  alors qu'il a sorti *moins* de tokens (113k vs 150k). Temps modèle 15,5 vs 23,4 min —
  mais **attente d'outil 18,7 vs 6,6 min**. Il écrit plus vite et vérifie plus longtemps.

`青瓜传媒` le résume : **« 单价降了但话说得多，实际单任务成本可能不降反升 »** — le prix unitaire
baisse, le volume monte, **le coût par tâche peut augmenter**. Et confirme deux signaux
précédents : **« 路由口径变动频繁：V4 Pro 的下线通告发过两版 »** (annonce rétractée), plus un
bug de suivi de langue côté Web (question EN → chaîne de raisonnement CN, ~50 % de reproduct.).

Autres : `cf-1` dit que la **troncature JSON a *été corrigée*** dans V4.1 (l'ancien Flash
gérait mal `enum`) — différent de la troncation silencieuse de contenu, mais à ne pas confondre.
Rapport communautaire d'** boucle d'inférence en contexte ultra-long + effort `max`** — le
même motif de flooding que chez MiMo.

## Ce que le pass 2 a changé dans mes conclusions

| Avant | Après |
|---|---|
| GLM « benchmaxxé » à 57 chez AA | 57 = v4.1.1 périmé ; **41,8 = v4.3.2 correct** |
| MiMo : retraining silencieux, signal négatif dur | Défaut **avoué, chiffré, corrigé (90 k$)** ; le fait tient, l'intention non |
| DeepSeek = meilleur rapport vitesse/utilité | **Coût par tâche potentiellement +36 %** malgré token moins cher |
| Ling : 262K sans explication | 256K **pour raison de coût de service**, prix et poids inconnus |
| I3 : « l'effort n'est pas monotone » (hypothèse) | **Mesuré** : monotone en court, **inversé en long contexte** |

**Reste ouvert** : X/Twitter, Discord, accès direct à Reddit (403), toute donnée Solar.
