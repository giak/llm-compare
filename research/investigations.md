# Investigations

Statut au 2026-10-06. `☐` à faire · `◐` partiellement avancé · `⊘` clos, négatif.

Ce qui est acquis et ne se refait pas : identités, URLs, scores AA sur index commun.
Ce qui reste : le comportement réel dans *ton* Freebuff, et le français, que personne
n'a mesuré pour aucun des douze.

---

## P0 — I0 · Le français ◐ — **phase 1 close, phase 2 prête**

**Statut : UNKNOWN, avec un début de mesure.** Instrument et résultats dans
**`research/i0-francais.md`**.

Phase 1 (traces locales, 15 prompts français organiques) : **12 réponses finales en français
sur 15**, raisonnement en anglais sur 13/15. Les modèles répondent donc dans la langue du
prompt — le scénario « le modèle ignore la langue » est écarté. Un défaut net : **1 réponse
française s'ouvre par de la narration de processus en anglais** (`space-bunny-alpha`).

Ce que la phase 1 **ne** dit pas : **zéro échantillon** pour MiMo Flash, MiMo Pro, Ling,
DeepSeek, Muse, Luna, Solar, Laguna. DeepSeek a 1 thread à **0 message**. Et
`m-22ff70c712` (9 threads, 296 messages) est un **ID opaque** introuvable dans le catalogue
local — non attribuable aux 12. Aucune comparaison inter-modèles possible : prompts non
identiques.

Phase 2 : 10 prompts identiques + grille binaire 12 critères, **dans `i0-francais.md`**.
Priorité : `mimo-v2.6-flash` et `glm-5.3-flash` **en premier** (ce sont les deux dont
l'éditeur ne revendique que `en, zh`), puis Ling et Space Bunny (coût nul).

L'ordre d'exécution proposé en fin de fichier place I0 après I2. **Inverser** : I0 est le
seul test qui peut lever la réserve française et rendre les deux défauts à 0-10/h
réutilisables — et Ling expire le 2026-10-13, soit avant la plupart des autres leviers.

**Ce que je ne peux pas faire** : appeler Freebuff. Le passage manuel est le tien.

---

## P0 — I2 · Les 0/h sont-ils réels ? ☐ — **URGENT**

**Statut : ⏰ fenêtre qui se ferme.** Ant : essai gratuit de deux semaines depuis le
2026-09-30 → expiration ~2026-10-16. Vercel AI Gateway : gratuit **jusqu'au 2026-10-13**.
Nous sommes le 2026-10-06.

Si Ling 3.1 Flash est bien 0/h, il est le 4e des douze en intelligence (41,1) avec 62,1 % de
non-hallucination, pendant que GLM Flash coûte 10/h et DeepSeek 15/h. Passé l'expiration il
coûte probablement l'un de ces prix.

Protocole : consommer une session longue sur un 0/h et surveiller le seuil. Chercher la
**valeur** du palier, pas seulement le fait qu'il existe. Puis comparer avec la grille
affichée.

Décisif si : un palier réel existe (ex. 2 h/jour) → le tri par prix est faux d'un cran
supérieur, et tu connais le modèle réellement gratuit.

**Avancée le 2026-10-06 (passe 7)** — sources primaires lues :

- `freebuff.com/llms.txt` fixe la **France à 60 FB/jour** (full access) : ta prémisse
  « 60/jour » est **validée**. Le mode *full* contient bien Solar Pro 4.
- Mais `llms.txt` **ne publie aucun tarif horaire**. Le README GitHub dit que cinq modèles
  (GLM, DeepSeek, MiMo Flash, Solar Mini, Solar Pro) sont *« unmetered at full access »* ;
  un tiers dit **10 FB/h pour Solar Pro 4**. **Trois sources, aucune concluante.**
- Le problème s'est **agrandi** : ce n'est plus seulement « quel est le prix », c'est « quel
  est encore le catalogue ». Voir I6.

---

## P0 — I10 · Le catalogue réel de Freebuff ◐ — **résolu, 2 erreurs trouvées**

**Question** : mes douze modèles sont-ils encore les douze que propose Freebuff ?

**Concordances primaires (2026-10-06)** — `freebuff.com/llms.txt`, `freebuff.com/plans`,
`freebuff.com/live`, **GitHub `CodebuffAI/freebuff` README** (npm : 403) — **recoupées par le
changelog tier 2 `freebuff-changelog.nordicnode.workers.dev`** :

| | |
|---|---|
| **Catalogue réel (12 au 2026-10-06)** | MiMo 2.6 Flash, GLM 5.3 Flash, DeepSeek V4.1 Flash, DeepSeek V4.1 Flash Fast, GPT-6 Luna, MiMo 2.6 Pro, Solar Mini 4, Solar Pro 4, Space Bunny Alpha, Gemini 3.8 Flash, Muse Spark 1.3, GPT-6.1 Sol |
| **Catalogue réel (11 depuis le 2026-10-06)** | idem **sans Space Bunny Alpha** — retiré du picker, `llms.txt` et `/plans` (GitHub `c3edf98738bd`, 2026-10-07 00:14Z) ; changelog : **« 11 live · 9 retired · 20 all-time »** |
| **Dans mes 12, PAS sur Freebuff** | **Ling 3.1 Flash**, **Laguna S 2.1** |
| **Sur Freebuff, ABSENTS de mes 12** | **Gemini 3.8 Flash**, **GPT-6.1 Sol** |
| **Utilisables sur un compte FR gratuit** | **8** *(9 au 2026-10-06)* — les 11 moins Muse Spark, Gemini 3.8 Flash, GPT-6.1 Sol (`Access = Paid plans` / `US only`) |

**Deux erreurs, de natures différentes :**

1. **Ling et Laguna n'ont jamais figuré sur aucune source Freebuff.** Aucun des quatre
   catalogues primaires du jour ne les cite ; ils vivent sur **OpenRouter / Vercel AI
   Gateway** (leurs changelogs parlent d'eux, mais jamais de Freebuff). Ma grille leur
   attribuait **0/h Freebuff** — **faux**. Je ne peux pas prouver qu'ils n'y ont *jamais* été,
   mais **quatre sources primaires concordantes du jour ne les connaissent pas**.
2. **Gemini 3.8 Flash et GPT-6.1 Sol me manquaient** — et les deux sont **inaccessibles sans
   abonnement** en France. GitHub README, colonne `Access` : Gemini = **`Paid plans`**,
   Muse Spark = **`Paid plans`**, GPT-6.1 Sol = **`US, or paid plans elsewhere`**. Les trois
   sont **dans le picker gratuit** de `llms.txt` mais **sans accès**. C'est la découverte la
   plus lourde : **Muse Spark 1.3, mon 48,1, n'est pas utilisable** — et **mes 12 n'en
   comptent que 9 d'utilisables**.

**Éléments acquis en chemin :**

- **Nouvelle source en passe 9 : `freebuff-changelog.nordicnode.workers.dev`** (tier 2 —
  miroir des commits publics `CodebuffAI/freebuff`, avec lien permalink). Elle donne la
  frise complète : **20 modèles depuis le 05/08, 12 vivants, 8 retirés, 23 changements de
  catalogue**. Mon « 5 changements en 3 semaines » venait de `mvalentsev` et était **trop bas**.
  Voir `research/veille.md`.
- **Deux promotions opposées le même jour (05/10)** : Solar Mini 4 **sort** du gratuit
  (« free promotion ended ») pendant que Solar Pro 4 **y entre**. Code :
  `common/src/util/freebuff-picker-sections.ts`, sections `unlimited` / `optimized`.
- **`GPT-6.1 Sol` : « promotional 100 Freebucks »** (09/29) — premier prix Freebucks brut
  que je récupère pour un modèle du catalogue.
- **Gemini 3.8 Flash a vécu deux vies** : gratuit le 09-03, retiré le jour même, ré-ajouté
  le 09-22 **derrière un abonnement payant**. Sa description d'origine : *« the priciest row
  per message »*.
- `/plans` (primaire) donne les **heures/jour** et dévoile les prix relatifs : Solar Pro 4 **`∞`**
  (Space Bunny **`∞` jusqu'au 06/10, retiré depuis**), Solar Mini 0,05 $/h, **GLM 0,15 $/h**,
  MiMo Flash/DeepSeek 0,10-0,15 $/h, Luna 0,20 $/h, MiMo Pro 0,325 $/h, DeepSeek Fast 0,52 $/h,
  Gemini 0,87 $/h, GPT-6.1 Sol 2,60 $/h.
  ✏️ **corrigé passe 10** : j'avais regroupé **GLM avec MiMo Flash et DeepSeek à 0,10 $**.
  Or `/plans` donne **17 h pour GLM *et* DeepSeek** contre **26 h pour MiMo Flash** — deux
  prix différents. La correction vient d'en bas : le commit GitHub du 06/10 dit que le prix
  courant de GLM est **15 Freebucks** (promo 10 du 03/10 au 06/10). **17 h ↔ 15 FB, 26 h ↔ 10 FB**
  : les heures de `/plans` **recoupent** les prix du code, ce qui fait de la table d'heures un
  **second réfecteur de prix** — et lève une partie de I2.
  Autre point : `/plans` affiche aujourd'hui **« $2.50 refilled daily »** pour Starter (ma
  note disait 2,60 $/j) — l'écart 2,50/2,60 ne change aucun arrondi ci-dessus.
- **Solar Pro 4 porte le badge `Promotional`** — ~~et sa promotion Upstage expirerait le
  09/10/2026~~ **FAUX (passe 10)** : le prix Freebuff est une promotion **open-ended, sans
  date** (`SOLAR_PRICE_CHANGES`, primaire). L'échéance 09/10 concernait l'offre API Upstage.
- `freebuff.com/live` : 4 827 utilisateurs, **France = 151** (5ᵉ pays). Solar Pro 4 = 253
  sessions (5ᵉ des 12). Corrige le « zéro signal » d'I9.
- Le catalogue **bouge vite** : **23 changements depuis le 05/08/2026**, 8 modèles retirés.
  `llms.txt` lui-même prévient : *« check your model picker for the current selection »*.
- **Nouveau champ côté serveur (06/10) : `freebucksRefundSources`**, qui sépare le
  remboursement en `daily` et `wallet` → **preuve que les deux poches existent**. Utile
  pour I2/I6.
- **`m-00032eaeec` = `mimo/mimo-v2.5`** (résolu via `world_snapshot`) — **corrige I0**, qui
  traitait ces ID comme fabriqués. MiMo 2.5 a été retiré du catalogue le 2026-09-22.

**Ce qui reste ouvert** : les benchmarks de Gemini 3.8 Flash et GPT-6.1 Sol (**non collectés**),
et la confirmation que ton picker affiche bien ces 12-là (à faire en une capture).

---

## P1 — I1 · « Flash » et « Flash Fast » sont-ils le même modèle ? ☐

La source est morte (404) et DeepSeek ne documente aucun « Flash Fast ». Écart de prix 40 %.
Si c'est le même modèle avec une file différente, tu paies 40 % pour rien.

Protocole : 3 prompts identiques sur `Flash` (15/h) et `Flash Fast` (25/h). Chrono sur le
premier token et sur la fin. Relever `inputTokens` / `outputTokens` des deux côtés.

Décisif si : tokens quasi identiques et latences du même ordre → même modèle, palier de
service. Écart net → deux services distincts.

---

## P1 — I3 · L'effort est-il un cadran de qualité ? ☐ — **PRIORITÉ HAUTE**

**Préuve déjà acquise, locale** : sur 1490 messages de ta base, `reasoning_effort` vaut
`max` sur 1350 et `None` sur 140. **Zéro palier intermédiaire n'a jamais été utilisé.** Tu
paies le palier haut par défaut, jamais par choix.

Et AA mesure un écart qui rend la question urgente : GLM 5.3 vaut 41,9 % sur TB 4.0 à `max`
contre 34,9 % à `low`. Luna vaut 0,0 % sur TB 4.0 à `low` et 12,6 % à `max`. L'effort
n'est pas décoratif — mais il n'est pas monotone partout (Muse Spark : `xhigh` 16,7 % contre
`max` 33,3 % sur TB 4.0).

Protocole : même prompt difficile sur les 6 paliers de Luna. Coût en tokens + critère
binaire que tu tranches à la main (test qui passe / ne passe pas). Cherche le palier où le
coût monte et la qualité plus.

Décisif si : la qualité est plate au-dessus d'un palier → tu descends partout.

---

## P1 — I4 · Solar Pro 4 : prudence ou annonces ? ◐ — **exécuté, et bloqué sur Solar**

Son gain AA vient de l'abstention : précision inchangée à 19 %, 41 % de tentatives contre
92 %, hallucination de 88 % à 24 %. Sur *tes* tâches, se taire peut être ce que tu veux — ou
ce qui te bloque.

Protocole : 10 prompts de ton travail réel, compter refus/non-réponses par modèle à qualité
égale. Tu obtiens un taux d'abstention et un coût par réponse utile.

### Exécution (passe 8) — mesure sur les 8 bases locales, 1 510 messages

**Blocage central : Solar Pro 4 = 0 échantillon local.** 0 message sur 1 510. Le corpus ne
contient que 4 modèles : `stealth/space-bunny-alpha` (1 046 msgs), `m-00032eaeec` (**résolu :
`mimo/mimo-v2.5`**, via `world_snapshot`), `z-ai/glm-5.3-flash` (168) et `m-22ff70c712`
(30, toujours opaque). **Le protocole ne peut pas répondre sur Solar Pro 4 hors session live.**

Ce qui *est* mesurable — **« le tour n'a pas agi »** (ni outil, ni fichier modifié) :

| Modèle | turns | a agi | réponse sans action | rien du tout | n'a pas agi |
|---|---:|---:|---:|---:|---:|
| stealth/space-bunny-alpha | 523 | 469 | 53 | 1 | **10,3 %** |
| mimo-v2.5 | 133 | 116 | 11 | 6 | **12,8 %** |
| z-ai/glm-5.3-flash | 84 | 78 | 4 | 2 | **7,1 %** |
| m-22ff70c712 (opaque) | 15 | 15 | 0 | 0 | 0 % |
| **Solar Pro 4** | **0** | — | — | — | **aucun échantillon** |

**Deux erreurs de méthode attrapées en vol, réutilisables :**

1. **Le regex de refus sur les parties mixtes donne 192/523 (37 %) — faux positifs massifs.**
   Le champ `parts_json` contient `reasoning` (la pensée) *et* `text` (la réponse finale).
   Mes « refus » étaient du raisonnement interne (« I can't see the output »).
2. **Même en isolant `kind='text'`, ça reste faux : 49/523 (9,4 %).** Les captures sont des
   *réserves honnêtes*, pas des abstentions : « ce que je ne peux pas trancher à ta place »,
   « une limite que je ne peux pas lever ». **Un agent qui déclare ses limites n'est pas un
   agent qui refuse.** Le taux GLM (1/84) contre Space Bunny (49/523) mesure un **style**,
   pas une abstention.

**Conséquence : le protocole tel qu'écrit n'est pas mesurable a posteriori.** Il faut les 10
prompts envoyés **à froid, aux mêmes modèles, en même conditions**. Corpus prêt : 576 prompts
utilisateurs réels extraits (projet `audio-sync-tool`), dont une sélection de 10 est
reproductible — **attention, un token Discogs en clair y figure : le filtrer avant tout envoi.**

**Apport de la passe 7 (recherche de bureau)** — `research/solar-pro-4.md` :

1. L'index AA de Solar Pro 4 est **estimé**, pas mesuré (« independent evaluation
   forthcoming ») et **toutes** ses courbes de détail sont *Not publicly available*. Seul des
   douze dans ce cas → **ne pas le classer**.
2. Le gain est structurellement **de l'abstention**, pas de la compétence : ça renforce
   l'intérêt du protocole ci-dessus.
3. **CrucibleMark signale une « tool use hallucination »**, qualifiée de *disqualifying
   signal*. Pour un agent qui exécute des commandes, c'est **plus grave que l'index**.
4. Plus lent que Solar Pro 3 (8,6 vs 6,0 min/tâche) avec moins de tokens de sortie.
5. **Promotion −70 % qui expire le 09/10/2026** — fenêtre de 3 jours.

---

## P2 — I5 · La compaction ◐ — un fait nouveau, un négatif dur

**Ce que la mesure locale a donné.**

101 événements de compaction réels, sur 3 modèles et 5 projets. Découverte **non documentée
ailleurs** : la compaction a **deux déclencheurs**, pas un.

| Déclencheur | Événements |
|---|---|
| `context_limit` | une partie |
| `cache_expiry` | une partie |

`cache_expiry` signifie qu'une compaction peut être déclenchée par un **événement de coût ou
de performance**, pas seulement par un débordement de capacité. C'est une donnée de
mécanique de plateforme que je n'ai trouvée dans aucune source publique.

Confirmation : à l'événement, `context.usedTokens` est de 67k à 94k selon le modèle, très
en dessous du seuil (320k ou 400k). Ces compactions ne sont donc **pas** des débordements.

| Modèle | n | usedTokens à l'événement | Seuil | Fenêtre | seuil/fenêtre |
|---|---:|---:|---:|---:|---:|
| Space Bunny Alpha | 71 | 93 811 | 320 000 | 1 000 000 | **32 %** |
| `m-22ff70c712` | 18 | 87 814 | 320 000 | 1 000 000 | **32 %** |
| GLM 5.3 Flash | 12 | 67 464 | 400 000 | 1 000 000 | **40 %** |

**Le négatif** : l'effet sur la qualité et sur la production **n'est pas mesurable** ici.
Zéro paire avant/après exploitable. Deux raisons structurelles :
- la couverture de `usage` est de **46,2 %** des messages (688 sur 1490) ;
- les messages voisins d'une compaction ne portent pas de `context` — il n'y a donc pas de
  `usedTokens` « après » à comparer.

La couverture de `context` est de 47,0 %, celle de `costUsd` de 45,8 %.

**Ce qu'il faut pour clore I5** : un relevé propre, où chaque message porte ses métriques.
Ce n'est pas un problème de méthode, c'est un problème de couverture de la source.

---

## P2 — I6 · Le modèle économique de Freebuff ⊘ — **NON RÉSOLVABLE EN LOCAL**

J'ai cherché une source de prix locale. Elle n'existe pas.

| Source testée | Résultat |
|---|---|
| `messages.metrics_json.costUsd` | 0 sur les 682 messages qui le portent |
| `state.json.session-refunds.json` | 20 entrées, **toutes `freebucks: 0`**, toutes `settled`, 3 threads / 20 attempts |
| `state.json` | 0 occurrence de `price`, `pricing`, `rate`, `catalog` |
| table `sponsored_runs` | 0 ligne ; `threads.sponsored` non-null sur 0 thread sur 17 |

Le fichier s'appelle *refunds* : il journalise les **remboursements**, pas les débits. Il ne
peut donc ni confirmer ni infirmer la grille affichée. `sponsored_runs` vide signifie que le
mécanisme de parrainage existe dans le schéma mais **n'a jamais été observé** localement —
ni preuve ni réfutation.

**Conclusion : I6 exige la plateforme, pas la base locale.** Deux questions à poser :
le débit de Muse Spark 1.3, et la confirmation de la grille (0/h réels ou quotas).

---

## P2 — Corrélation structurelle : ta base ne permet pas de comparer des modèles ⊘

| Modèle | threads | messages | part |
|---|---:|---:|---:|
| Space Bunny Alpha | 5 | 1046 | **70,2 %** |
| `m-22ff70c712` (alias local non résolu) | 9 | 276 | 18,5 % |
| GLM 5.3 Flash | 2 | 168 | 11,3 % |

**Un seul modèle domine le corpus.** DeepSeek a un thread configuré mais **zéro message**.
Il n'y a donc aucune base de comparaison multi-modèles dans tes traces : tout ce qui précède
est de la documentation externe, pas de l'observation directe.

Conséquence de méthode : toute statistique par modèle tirée de cette base porte sur un
échantillon de 1 à 5 threads. À ne pas utiliser comme preuve de performance.

---

## P1 — I9 · Signaux faibles (hors benchmarks) ◐ — **premier passage clos**

**Livrable : `research/signaux-faibles.md`.** HN Algolia (primaire, citable) + pages AA
(vérification de mes propres chiffres) + Reddit en tier 3 via blogs agrégateurs. API Reddit
bloquée en 403. X/Twitter et Discord non touchés.

Ce que le signal social apporte que les benchmarks ne donnent pas : les **modes de défaillance**.
Trois de mes recommandations en ont un que je n'avais pas — MiMo (accusation de benchmaxxing,
retraining `-MOPD` silencieux le 25/09), GLM Flash (« not reliable enough to trust at scale »,
contournement de garde-fous), DeepSeek (troncature silencieuse en milieu de phrase).

Corrections factuelles appliquées :
- **Ling 3.1 Flash** — mon 41,1 est **confirmé** par la page AA, contre l'hypothèse d'un
  chiffre fantôme. Deux colonnes remplies : **211 tok/s**, **0,99 $/tâche**.
- **DeepSeek vitesse** — le « 4,8x » est un rapport fournisseur/fournisseur. AA mesure
  V4.1 Flash à 214,4 tok/s et V4 Flash à 214,9 : égalité. Réserve ajoutée au `comparatif.md`.
- **Ling contexte** — AA dit 1M, l'endpoint sert 262K en essai. Conflit documenté.

Découverte : **deux modèles du tableau sont socialement invisibles** (Solar Pro 4, Solar
Mini 4), et **Freebuff lui-même n'a aucune trace sur HN**. Absence de critique ≠ absence de
défaut.
*Corrigé passe 7 : c'est une absence sur **HN**, pas une absence de signal — Reddit,
ARENA.ai et `freebuff.com/live` parlent de Solar Pro 4.*

Reste ouvert : source chinoise (le signal y est probablement le plus dense pour GLM/MiMo/Ling),
accès direct à Reddit, X/Discord, et toute donnée sur Solar.

**Pass 2 — sources chinoises : fait, et il a corrigé trois conclusions.** 9 requêtes, ~40
sources chinoises recoupées avec les pages AA en chinois. Résultats détaillés dans
`research/signaux-faibles.md` § pass 2. En résumé :

1. **Mon 41,8 pour GLM est juste, les Chinois citent 57** — 57 = index v4.1.1 (26/08),
   42 = v4.3.2 actuel. Re-baselining AA le 07/09. Z.ai et toute la presse chinoise sont périmés.
2. **I3 passée de hypothèse à mesure** : défaut = `max` (ratio 0,984), monotone en question
   courte, **inversé en retrieval long-contexte** (`high` 75,3 % > `max` 71,6 %).
3. **MiMo nuancé** : le post-mortem officiel chiffré (flooding 11,1 % → 24,6 %, MOPD 90 k$,
   59 appels d'outil) transforme un « retraining silencieux » en défaut **avoué et corrigé**.
4. **DeepSeek : inversion de coût** — +36 % par tâche que le V4 précédent malgré un token
   moins cher ; sur une tâche, *plus lent* malgré moins de sorties (attente d'outil 18,7 vs 6,6 min).
5. **§4 renforcé** : AA-Omniscience Index DeepSeek **−5** (erreurs > réponses) vs GLM **+7**.

Reste : X/Twitter, Discord, accès direct Reddit (403), ~~toute donnée Solar~~ → **levé** :
`research/solar-pro-4.md`.

---

## P3 · Restants ☐

- **I7 · Non-hallucination sur ton domaine.** AA-Omniscience est à 18-46 % pour tout le
  monde. Sur du code et de la config, une invention est un bug. 20 faits du projet que tu
  connais, un par modèle.
- **I8 · Space Bunny Alpha en première main.** Le seul sans donnée tierce, gratuit, et
  l'agent qui écrit ce dépôt. Observation directe possible, **biais déclaré** : je suis le
  sujet. Utile comme borne, pas comme preuve.
  → 🪦 **caduc (passe 10)** : modèle **retiré de Freebuff le 06/10/2026**. Les mesures locales
  restent valables comme archives, mais le banc d'essai est à re-choisir (Solar Pro 4, 0/h).
- **I10 · Le catalogue.** ✅ **Traité (passe 8)** → section P0 en tête de fichier. Deux erreurs
  corrigées dans `comparatif.md` : Ling et Laguna n'étaient pas sur Freebuff, Gemini 3.8 Flash
  et GPT-6.1 Sol manquaient. **Reste** : benchmarks des deux nouveaux, et une capture du picker
  pour confirmer que les 12 affichés sont bien ceux-là.
  → **passe 10** : le catalogue est désormais **11** (Space Bunny Alpha retiré le 06/10),
  et `llms.txt`/`/plans`/changelog le confirment sans capture nécessaire.

---

## Ce que je ne ferai pas

- Recopier les scores AA en classement : les efforts ne sont pas appariés.
- Comparer Terminal-Bench 2.1 à 4.0.
- Écrire un harness avant d'avoir une cible mesurée — et les données locales ne la fournissent pas.
- Traiter la métadonnée `language:` comme une mesure de capacité.

## Ordre d'exécution proposé

1. **I0** — Seul test qui peut lever la réserve française et rendre les deux défauts à
   0-10/h réutilisables. Instrument prêt dans `i0-francais.md`, **passage manuel requis**.
   Priorité : `mimo-v2.6-flash` et `glm-5.3-flash` en premier, puis Ling et Space Bunny
   (coût nul).
2. **I2** — Urgence réelle **2026-10-09** : promotion Solar Pro 4 (0/h) qui s'éteint.
   Conditionne tout arbitrage budgétaire. *(L'essai Ling jusqu'au 10-13 ne concerne plus I2 :
   Ling n'est pas un modèle Freebuff — voir I10.)*
3. **I3** — Levier de coût le plus direct, sur un modèle déjà payé.
4. **I1** — Décisif et bon marché.
5. **I4** — 10 prompts contre Solar Pro 4 : **nécessite une session live**, corpus local prêt.

I0 et I2 sont **à faire en parallèle** : I0 porte sur la langue, I2 sur les quotas, et les deux
se jouent dans la même session Freebuff — **avant le 09/10** pour I2.
