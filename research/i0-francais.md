# I0 · Le français — mesure locale + instrument contrôlé

Statut : **◐ partiel**. Phase 1 close (mesure sur les traces locales). Phase 2 (instrument) prête,
à exécuter sur Freebuff — je ne peux pas appeler la plateforme.

Date : 2026-10-06. Sources : 8 bases `desktop-v2.db`, lecture seule, 1506 messages.

---

## Phase 1 — Ce que les traces locales mesurent

### Méthode (et le piège que j'ai évité au deuxième essai)

Les `parts_json` assistant contiennent **plusieurs kinds** : `reasoning` (9960), `tool` (17838),
`text` (9841), `ad` (2144), `changes` (394), `notice` (19), `compaction` (80).

Mon premier calcul a lu le premier champ `text` trouvé — qui est celui du **reasoning**. Résultat
affiché : « 3 réponses françaises sur 15 ». C'était faux : je mesurais la langue du raisonnement
interne, pas celle de la réponse à l'utilisateur.

Reprise sur `kind='text'` uniquement. Le raisonnement et la réponse finale ont des langues
**différentes** — c'est la mesure, pas un bug.

### Résultat — réponse finale (`kind='text'`) à un prompt français

| Modèle | threads | prompts FR | réponse **fr** | réponse **en** |
|---|---:|---:|---:|---:|
| `m-22ff70c712` — **ID non résolu** | 9 | 8 | **6** | 2 |
| `stealth/space-bunny-alpha` | 5 | 5 | **4** | 1 |
| `z-ai/glm-5.3-flash` | 2 | 2 | **2** | 0 |
| `deepseek/deepseek-v4-flash` | 1 | 0 | 0 | 0 |
| **Total** | 17 | **15** | **12** | **3** |

**12 réponses françaises sur 15 (80 %).**

| Signal | Valeur |
|---|---|
| Réponse finale **entièrement en anglais** à un prompt FR | **3 / 15** |
| Réponse finale française **s'ouvrant en anglais** | **1 / 15** |
| Réponses **mixtes** (fr et en tous deux substantiels) | **5 / 15** |
| Raisonnement (`kind='reasoning'`) en anglais | **13 / 15** |

### Les trois constats

**1. Les modèles raisonnent en anglais et répondent en français.** 13 raisonnements anglais,
12 réponses françaises. C'est le comportement attendu et souhaitable — le raisonnement n'est pas
affiché à l'utilisateur. **Ce n'est pas un défaut.**

**2. Les deux réponses anglaires de `space-bunny-alpha` et de `m-22ff70c712` portent sur des
tâches où l'anglais technique domine** — correction d'une contradiction entre fichiers de
compétences nommés en anglais, et diagramme Mermaid du pipeline CI. Attribuable à la tâche,
pas à la langue du modèle. **Non concluant.**

**3. Une fuite réelle : narration de processus en anglais dans la réponse finale.**
`space-bunny-alpha`, à une demande française :

> « I'll start by loading the memory protocol and gathering context in parallel. Mnemolite is up.
> Loading the mem-first protocol and exploring your project in parallel. Memory first, then local
> project context. »

La réponse *est* classée française — le français arrive plus loin — mais l'utilisateur a une
phrase d'ouverture anglaise. C'est un défaut de langue visible, et c'est le seul défaut net que
la phase 1 produise.

### Ce que la phase 1 ne dit pas — quatre limites

1. **n = 15, prompts non identiques.** Ce sont des prompts organiques de mes propres sessions,
   pas les 10 prompts contrôlés du protocole. **Aucune comparaison inter-modèles n'est possible**
   : chaque modèle a reçu des tâches différentes.
2. **Zéro échantillon pour les modèles décisifs.** MiMo-V2.6-Flash, MiMo-V2.6-Pro, Ling 3.1 Flash,
   DeepSeek V4.1 Flash, Muse Spark, Luna, Solar, Laguna : **aucun message français local.**
   DeepSeek a 1 thread configuré et **0 message**. Le modèle que je recommandais comme défaut
   sur le français n'a jamais parlé dans cette base.
3. **`m-22ff70c712` est un ID opaque de catalogue**, absent du catalogue local
   (`~/.cache/opencode/models.json`, 8615 entrées) comme de tout fichier de configuration.
   9 threads et 296 messages **ne sont attribuables à aucun des 12**.
   > **CORRIGÉ en passe 8 (I10)** : j'avais écrit que `m-00032eaeec` « n'existe dans aucune
   > base, artefact ». **Faux — il existe** : 266 messages sur 4 mondes, et `world_snapshot.model`
   > le résout en **`mimo/mimo-v2.5`**, retiré du catalogue le 2026-09-22. Le seul artefact
   > confirmé reste `m-916b95b337`.
   > Conséquence : **mi-mimo-v2.5 dans mes données locales**, et I0 doit le compter séparément
   > de MiMo 2.6.
4. **Le score de langue est un classifieur heuristique** (stop-words + diacritiques), pas une
   grammaire. Il sépare fr/en, il ne juge pas la qualité.

**Conséquence : la phase 1 ne peut pas trancher I0.** Elle établit que les modèles déjà utilisés
*répondent* en français, ce qui élimine le scénario « le modèle ignore la langue du prompt ».
Elle ne dit rien sur la qualité, ni sur MiMo et Ling.

---

## Phase 2 — Instrument contrôlé (à exécuter sur Freebuff)

### Ordre

D'abord **Ling 3.1 Flash** (gratuit jusqu'au 2026-10-13) et ~~**Space Bunny Alpha** (0/h)~~ :
coût nul, et ce sont les deux que la phase 1 n'a pas couverts ensemble. Puis les candidats
sérieux.
→ 🪦 **mise à jour passe 10 (2026-10-07)** : **Space Bunny Alpha a été retiré de Freebuff le
06/10** — il n'est plus mesurable. Le remplaçant à coût nul est **Solar Pro 4** (0/h,
promotional open-ended). Ling reste en place (fenêtre fermée le 2026-10-13).

**Ordre de priorité** — les deux modèles dont l'éditeur ne revendique que `en, zh` passent
**en premier**, pas en dernier :

1. `mimo-v2.6-flash` — défaut recommandé par `comparatif.md`
2. `glm-5.3-flash` — défaut code/outil recommandé
3. `ling-3.1-flash` — gratuit, fenêtre fermée le 13
4. `space-bunny-alpha` — 0/h, déjà partiellement couvert
5. `deepseek-v4.1-flash` — 15/h, défaut vitesse
6. `mimo-v2.6-pro` — escalade
7. Le reste si le budget le permet

### Les 10 prompts — identiques pour chaque modèle

À coller **en français, tel quel**, sans reformulation, dans un fil neuf.

**P1 — subjonctif et accord**
> Explique en trois phrases, sans faute, pourquoi « il faut que nous partions » est correct
> et « il faut que nous partons » ne l'est pas. Puis donne deux autres verbes qui exigent
> le subjonctif après « il faut que ».

**P2 — anglicisme**
> Corrige cette phrase et explique chaque correction : « On va backer le flush de la cache
> avant de shipper le fix, et on va le push sur main une fois le green du CI. »

**P3 — négation et particule**
> Compare « je ne mange pas de pain » et « je ne mange pas un pain ». Explique la différence
> de sens, puis fais la même distinction avec « boire ».

**P4 — registre**
> Écris deux versions d'un même message à un collègue dont le code a cassé la CI :
> (a) sur Slack, en deux phrases ; (b) par email à un client externe, en cinq phrases.
> Garde le même contenu factuel dans les deux.

**P5 — correction, 8 fautes**
> Corrige ce texte, puis liste chaque correction en une ligne :
> « Malgrés quelque chose, il ce demande au jour d'hui si quelque soit l'heure, il faut que je vais
> voir cette personne dont je lui fais confiance. Je ne vois aucune raison de refuser, et d'ailleurs
> c'est un livre que je l'ai lu deux fois. »

**P6 — piège de prémisses**
> Dans quel pays se trouve la tour Eiffel ? Et quelle est la deuxième plus haute ville de France
> après Tourcoing ? Réponds aux deux questions en une phrase chacune.

**P7 — résumé technique**
> Résume en français, en quatre lignes maximum, ce que fait un index B-tree et pourquoi il
> accélère une recherche. Interdiction d'employer un mot anglais, y compris pour « index ».

**P8 — contrôle bilingue** *(même tâche que P7, en anglais)*
> Summarize in four lines what a B-tree index does and why it speeds up a search. The summary
> must be self-contained.

**P9 — enchaînement long**
> À partir de maintenant, réponds **uniquement** en français, et termine chaque réponse par la
> phrase « C'était écrit en français. » Je commence : liste cinq pièges du français écrit.

**P10 — mémoire de la consigne**
> Quelle langue ai-je utilisé dans mon tout premier message de cette conversation ? Cite-la,
> puis redis le premier mot de ce message.

P9 et P10 mesurent la **rétention de la contrainte linguistique** sur un fil long — c'est là que
compaction et effort risquent de faire perdre la consigne.

### Grille de notation — binaire, à la main

Un point par ligne, **0 ou 1**, noté à la main par toi (je ne note pas mon propre sujet).

| # | Critère | Question |
|---|---|---|
| G1 | Aucune faute d'accord | — |
| G2 | Aucune faute de conjugaison ou de mode | — |
| G3 | Aucune faute d'orthographe | — |
| G4 | Aucune tournure calquée de l'anglais | — |
| G5 | Registre conforme à la demande | — |
| L1 | **Toute** la réponse est en français (y compris l'ouverture) | — |
| L2 | Aucune narration de processus en anglais | — |
| L3 | Aucun mot anglais injustifié hors jargon technique | — |
| C1 | Contrainte P9 tenue (fin de réponse) | — |
| C2 | Contrainte P10 tenue (bonne langue citée) | — |
| V1 | P6 : la fausse prémisses est refusée, pas avalée | — |
| V2 | P5 : les 8 corrections sont les 8 bonnes | — |

**Décompte : /12.** Seuil de passage : **10/12**, avec **L1, L2 et V1 obligatoires** — un
modèle qui répond en anglais à l'ouverture ou qui avale la fausse prémisses ne passe pas,
quelle que soit la note.

### Ce qui rend le test non opposable tant que ce n'est pas fait

- Sans P8, aucun écart fr/en n'est imputable à la langue plutôt qu'à la tâche.
- Sans les 10 prompts identiques, aucun classement.
- Sans le passage manuel, **la question UNKNOWN de `comparatif.md` reste UNKNOWN.**

## Résultat attendu de la phase 2

Deux issues possibles, et l'arbitrage change selon l'issue :

- **MiMo Flash et GLM Flash passent ≥10/12** → la réserve française est levée, les deux défauts
  à 0-10/h redeviennent les meilleurs choix du tableau.
- **L'un échoue sur L1/L2** → il sort du périmètre par défaut, et Ling 3.1 Flash (gratuit
  jusqu'au 13) devient le défaut français tant que la fenêtre est ouverte.
