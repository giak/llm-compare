# Journal des vérifications

Format : quoi → source → verdict. `CONFIRMÉ` = la source primaire dit exactement ça.
`CONFIRMÉ PARTIEL` = la source dit autre chose / en plus. `RETRABILLÉ` = source morte ou fausse.

## 2026-10-05 — Passe 1

### Identité des 12 modèles
| Modèle | Source primaire | Verdict |
|---|---|---|
| MiMo-V2.6-Pro/Flash | mimo.mi.com/docs/en-US/news/latest/v2-6 | CONFIRMÉ — 2026-09-22, open-weight |
| GLM-5.3-Flash | docs.z.ai/guides/vlm/glm-5.3-flash + HF zai-org | CONFIRMÉ — 2026-08-26 |
| DeepSeek-V4.1-Flash | huggingface.co/deepseek-ai + arxiv 2609.19969 | CONFIRMÉ — 2026-09-09 |
| GPT-6 Luna | artificialanalysis.ai/models/releases/gpt-6-luna | CONFIRMÉ — 2026-09-22 |
| Solar Pro 4 | artificialanalysis.ai/articles/upstage-solar-pro-4 | CONFIRMÉ — 2026-08-11 |
| Solar Mini 4 | artificialanalysis.ai/articles/korean-ai-lab-upstage-releases-solar-mini-4 | CONFIRMÉ — 2026-09-23 |
| Ling 3.1 Flash | openrouter.ai/inclusionai/ling-3.1-flash | CONFIRMÉ — 2026-10-02 |
| Laguna S 2.1 | poolside.ai/blog/introducing-laguna-s-2-1 + HF | CONFIRMÉ — 2026-07-21 |
| Muse Spark 1.3 | research.meta.ai/blog/introducing-muse-spark-1-3 | CONFIRMÉ — 2026-09-02 |
| Space Bunny Alpha | spacebunny.app/docs | CONFIRMÉ — preview anonyme sept. 2026 |

### Contrôle des 10 URLs citées par la comparaison initiale
| URL citée | HTTP | Verdict |
|---|---|---|
| mimo.xiaomi.com/mimo-v2-6/article | 200 | CONFIRMÉ |
| docs.z.ai/guides/vlm/glm-5.3-flash | 200 | CONFIRMÉ |
| build.nvidia.com/deepseek-ai/deepseek-v4.1-flash/modelcard | 200 | CONFIRMÉ |
| **pi.dev/models/basaten/deepseek-ai-deepseek-v4-1-flash-fast** | **404** | **RETRABILLÉ** |
| research.meta.ai/static/muse-spark-1-3-…methodology | 200 | CONFIRMÉ |
| developers.openai.com/api/docs/models | 200 | CONFIRMÉ |
| artificialanalysis.ai/models/gpt-6-luna | 200 | CONFIRMÉ |
| artificialanalysis.ai/articles/upstage-solar-pro-4 | 200 | CONFIRMÉ |
| upstage.ai/blog/en/solar-mini-4 | 200 | CONFIRMÉ |
| openrouter.ai/inclusionai/ling-3.1-flash | 200 | CONFIRMÉ |
| poolside.ai/blog/introducing-laguna-s-2-1 | 200 | CONFIRMÉ |
| blog.buildfastwithai.com/space-bunny-review | 200 | CONFIRMÉ |

1 source morte sur 12. Elle portait l'affirmation « DeepSeek V4.1 Flash Fast est un endpoint
distinct », donc l'existence même du modèle « Flash Fast » n'est pas sourcée.

### Écarts trouvés entre la comparaison initiale et les sources
- GPT-6 Luna : 6 paliers d'effort dont `none`, pas 5. AA 18 → 38, pas 22 → 38.
- MiMo : 3 variantes, pas 2. `mimo-v2.6-pro-ultraspeed` (20x) n'était pas mentionnée.
- Solar Pro 4 : AA 42 exact, mais la précision Omniscience ne bouge pas (19 %) —
  le gain vient de l'abstention.
- Solar Mini 4 : « ~3B actifs » confirmé (35B/3B). TB 4.0 = 1 %, invisible dans la comparaison.
- Ling 3.1 Flash : 262K = le plus petit contexte des 12. Non signalé.
- Laguna S 2.1 : 70,2 % = 11e place sur le leaderboard cité dans le même billet.
- DeepSeek V4.1 Flash : effort **continu**, pas à paliers. 552B backbone + 196B Engram.

### Contrôle de la base locale Freebuff (lecture seule)
8 bases, 1478 messages. `messages.metrics_json` = `usage` (input/cached/output/total),
`costUsd`, `context` (usedTokens, windowTokens, compactionThresholdTokens), `compactions`.
`costUsd` est à 0 partout : la facturation se fait en Freebucks, pas en USD.
Modèles réellement utilisés dans `threads.model` : `z-ai/glm-5.3-flash`,
`deepseek/deepseek-v4-flash`, `stealth/space-bunny-alpha`, `m-22ff70c712`.
`reasoning_effort` est à `max` sur 1338 messages, `None` sur 140.
Aucun champ de latence nulle part.

Découverte rattachée à la §2.1 de `verdict.md` : le thread configuré sur
`deepseek/deepseek-v4-flash` sert en réalité V4.1-Flash (routage documenté par DeepSeek
le 14/09/2026). Le libellé affiché ment.

## 2026-10-05 — Passe 2 : alignement sur un index commun

Objectif : obtenir des scores **comparables entre modèles**, ce que la passe 1 n'avait pas
(version d'index hétérogène, pas de coût par tâche, pas de vitesse).

### Source de la mise en commun
Les pages `artificialanalysis.ai/models/<slug>` rendent leurs tableaux en JavaScript : le
contenu utile est absent du HTML. Deux contournements qui marchent :
- `openrouter.ai/<vendor>/<model>` réaffiche les tableaux AA **en statique** (indice global,
  8 sous-scores, par palier d'effort). C'est la source la plus dense.
- `artificialanalysis.ai/models/comparisons/<a>-vs-<b>` sort les tableaux de comparaison en
  statique, avec coût par tâche, tokens par tâche, vitesse, latence et temps par tâche.

### Index AA Intelligence v4.3.2 — les 12 alignés
| Modèle | Index | TB 4.0 | HLE | GDPval-AA | AA-LCR | non-hallu | $/tâche | tok/s | E2E |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Muse Spark 1.3 (max) | 48,1 | 33,3 | 48,7 | 59,2 | 83,0 | 67,1 | 1,60 | 140 | 37 s |
| Muse Spark 1.3 (xhigh) | 45,1 | **16,7** | 47,5 | 56,5 | 83,0 | 68,5 | 1,37 | 148 | n.d. |
| MiMo-V2.6-Pro | 46,3 | **34,9** | 49,4 | 59,4 | 86,3 | 59,4 | 0,13 | 37 | 64 s |
| Solar Pro 4 | 42 * | n.d. | n.d. | n.d. | 71 * | n.d. | n.d. | n.d. | n.d. |
| GLM-5.3-Flash | 41,8 | 32,8 | 40 | 47,6 | 80 | n.d. | 0,25 | 52 | 51 s |
| Ling 3.1 Flash | 41,1 | 33,3 | 39,4 | 56,1 | 83,0 | 62,1 | n.d. | n.d. | n.d. |
| DeepSeek-V4.1-Flash (max) | 39,5 | 26,8 | 39,2 | 55,0 | 84,0 | **3,5** | 0,27 | **209** | **13 s** |
| DeepSeek-V4.1-Flash (no rais.) | 25,0 | n.d. | n.d. | n.d. | n.d. | n.d. | 0,15 | 215 | 3,3 s |
| GPT-6 Luna (max) | 38,1 | 12,6 | 38,5 | 46,9 | 83,3 | 23,3 | **0,07** | 141 | 111 s |
| GPT-6 Luna (none) | 18,5 | 1,5 | 8,6 | 27,5 | 39,7 | 21,1 | n.d. | 130 | n.d. |
| MiMo-V2.6-Flash | 37,9 | 22,7 | n.d. | n.d. | n.d. | n.d. | 0,06 | 51 | 53 s |
| Laguna S 2.1 | **n.d.** | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. |
| Solar Mini 4 | 24,1 | 1,0 | 25,8 | 28,6 | 83,3 | 64,2 | ~0,35 | 208 | n.d. |
| Space Bunny Alpha | **n.d.** | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. |

`*` = index antérieur (mesure du 12/08/2026), non comparable.

### Constats de la passe 2
1. **Muse Spark 1.3 (48,1) bat MiMo-V2.6-Pro (46,3)** sur le même index. Inversion de l'ordre
   de la comparaison initiale.
2. **Muse Spark 1.3 coûte 1,60 $/tâche**, le plus cher des douze, 23x Luna max. Prix non
   affiché sur Freebuff.
3. **L'effort n'est pas monotone** : Muse Spark TB 4.0 = 16,7 % à xhigh contre 33,3 % à max.
   Le palier bas a un meilleur index global (45,1) mais deux fois moins de code agentique.
4. **DeepSeek-V4.1-Flash : non-hallucination 3,5 %**, le pire du panel, avec la meilleure
   précision Omniscience (46,4 %).
5. **Le harness fait varier le score de 3x** : Muse Spark TB 4.0 = 33,3 % (AA) contre
   10,6 % (Vals AI). Ling 3.1 Flash = 33,3 % (AA) contre 40,4 % (Ant, auto-déclaré).
6. **Le fournisseur compte autant que le modèle** : GPT-6 Luna 141 tok/s chez OpenAI contre
   209 chez Azure. MiMo Pro : 26 tok/s chez DeepInfra contre 310 chez PrimaLabs.
7. **Terminal-Bench 2.1 → 4.0 effondre tout** : Muse Spark 84,3 % → 33,3 %. La passe 1
   comparait des scores 2.1 à des scores 4.0. Corrigé.

### Français — le trou
Recherche ciblée sur Global-MMLU, MMLU-ProX, EU MMLU, MMLU French, benchmarks multilingues :
**aucun score français publié pour aucun des douze modèles.** Les leaderboards français
recensés contiennent un seul modèle chacun, et EU MMLU ne classe aucun des douze.

Deux déclarations officielles trouvées sur les cartes de modèle HuggingFace :
- `XiaomiMiMo/MiMo-V2.6-Pro-RL` : `language: - en - zh`
- `zai-org/GLM-5.3` : `language: - en - zh`
Et la documentation Xiaomi confirme en texte : « Bilingual & Dialects: Chinese, English,
code-switching, Wu, Cantonese, Minnan, Sichuanese ».

Indication positive : Laguna S 2.1 (Poolside, laboratoire français) mène son propre tableau sur
**SWE-Bench Multilingual** à 78,5 %, et Ling 3.1 Flash revendique des gains large domaine.
Ce sont des indices, pas des mesures de français.

### Contrôle supplémentaire : pages AA absentes
`artificialanalysis.ai/models/laguna-s-2-1` → **404**
`artificialanalysis.ai/models/space-bunny-alpha` → **404**

Ces deux modèles n'ont donc aucune mesure tierne. Ce n'est pas anodin : ce sont deux des
quatre modèles gratuits sur Freebuff.

## Limites connues de cette passe

- Les scores AA ne sont pas tous sur la même version d'index (v4.3.2 courant ; les 42 de
  Solar Pro 4 datent d'août). Comparables seulement à version identique.
- Terminal-Bench 2.1 et 4.0 cohabitent dans les sources : aucun score croisé valide.
- Space Bunny Alpha n'a aucun benchmark tiers. Je tourne dessus : c'est une observation
  de première main, pas une preuve, et c'est biaisé par le fait que je suis le sujet.
- Aucune mesure de latence n'a été prise côté utilisateur : les chiffres AA sont ceux d'AA,
  pas les tiens. Le routage de Freebuff peut être très différent.
- Les chiffres de la plateforme (Freebucks/h) viennent de la comparaison initiale, non
  revérifiés par une source : c'est une capture d'écran, pas une API.

---

## 2026-10-06 — Passe 3 : auto-revue adversariale

Auto-revue du livrable des deux passes précédentes. **10 défauts trouvés, dont 3 qui
invalidaient une conclusion publiée.** Patches appliqués, journalisés ici.

### Défauts CRITICAL
| # | Défaut | Correction |
|---|---|---|
| C1 | Inférence sur le tag HF `language:` — étiquette de métadonnées d'entraînement traitée comme déclaration de capacité. Aggravant : la citation Xiaomi vient d'une section **audio**, généralisée au LM. Aggravant : checkpoints lus ≠ variante hébergée. | `verdict.md` §1c, `comparatif.md` § Français : requalifié en **UNKNOWN**, les trois reserves inscrites |
| C2 | Défaut d'appariement d'effort : Muse Spark **(max) 48,1** comparé à MiMo Pro **46,3 publié sans suffixe d'effort**. Formulation « l'ordre était faux » = certitude non justifiée. | Bandeau d'avertissement en tête de `comparatif.md` ; §1 et §1b de `verdict.md` |
| C3 | Négatif universal (« aucun score français publié ») formulé depuis une recherche bornée et anglophone. | « non trouvé dans l'espace couvert », l'espace étant nommé |

### Défauts MATERIAL
| # | Défaut | Correction |
|---|---|---|
| C4 | Coût/tâche de Solar Mini 4 non réconcilié : AA dit ~5x Luna « malgré des prix similaires », mais 88k×$0,40 = $0,035 contre 51k×$0,50 = $0,026 → **1,38x**. Mon $0,35 était mon arithmétique sur un « ~ ». | Section dédiée dans `comparatif.md`, statut **OPEN** |
| C5 | Méthodologie AA-Omniscience non-hallucination jamais lue. Mécanisme inféré d'une phrase d'article. Effort `max` sur cadran **continu** non contrôlé. | « le plus grave du dossier » → **MATERIAL**, avec les trois réserves |
| C6 | Couche budget dépendant de la grille issue de la capture d'écran — l'artefact dont une source morte sur douze a démontré la fiabilité. Signalé en chat, jamais conditionné dans les fichiers. | Bandeau ⚠ CONDITIONNEL sur `comparatif.md` **et les 12 fiches** ; ledger local documenté comme non concluant |
| C7 | Fait temporel manqué : Ling gratuit sous condition d'essai deux semaines (→ ~2026-10-16, Vercel 2026-10-13). Les deux dates étaient dans mes sources, enterrées en note. | Bandeau ⏰ en tête de `ling-3.1-flash.md` et dans la section budget |

### Défauts MINOR
- **C8** : le schéma `sponsored_runs` / `threads.sponsored` existe mais n'a **jamais été
  observé** (0 ligne, 0 thread non-null sur 17). Classé *non testé*, plus *alternatif actif*.
- **C9** : `models.md` dupliquait `fiches/` → **supprimé**.
- **C10** : l'écart harness 3x (Muse Spark 33,3 % AA / 10,6 % Vals AI) n'a pas été vérifié
  comme apparié en effort. Mentionné, non corrigé faute de source.

### Contre-preuve trouvée contre ma propre conclusion (C3)
La recherche en chinois a produit une affirmation que je n'avais pas trouvée :
shshi.cn revendique « **138 种语言** » pour GLM-5.3. Tier 3, et le même site se trompe
ailleurs (licence Apache 2.0 au lieu de `other`, 80 t/s sur A100, contexte 128K au lieu de 1M).
**Non promu** — mais sa présence suffit à casser « ne revendique que en+zh ».
Z.ai en revanche ne publie **aucune ligne multilingue** dans sa propre table de benchmarks.

### Mesures locales de la passe 3
| Mesure | Valeur |
|---|---|
| messages, 8 bases | 1490 |
| couverture `usage.outputTokens` | **46,2 %** (688) |
| couverture `context.usedTokens` | 47,0 % (701) |
| couverture `costUsd` | 45,8 % (682) |
| événements de compaction réels | **101**, sur 3 modèles / 5 projets |
| déclencheurs de compaction | **`context_limit`** et **`cache_expiry`** |
| seuil de compaction | **32 %** de la fenêtre (320k/1M) ; **40 %** pour GLM Flash |
| `reasoning_effort` | `max` 1350 · `None` 140 · **aucun palier intermédiaire** |
| concentration du corpus | Space Bunny Alpha **70,2 %** des messages |
| ledger de prix | `session-refunds.json`, 20 entrées, **toutes à 0**, `settled` |

**Découverte** : la compaction se déclenche sur `cache_expiry`, pas seulement sur
`context_limit`. À l'événement, `usedTokens` est de 67k-94k, très en dessous du seuil de
320k/400k. Ces événements sont donc déclenchés par la **performance/coût**, pas par la
capacité. Non documenté dans les sources publiques consultées.

**Négatif dur (I5)** : effet sur la qualité et la production **non mesurable**. Zéro paire
avant/après. Cause structurelle double : couverture usage 46 %, et les messages voisins d'une
compaction ne portent pas `context`.

**Négatif dur (I6)** : aucune source de prix locale n'existe. `costUsd` à 0 partout, le
ledger journalise des *remboursements* à 0, `state.json` ne contient aucune clé de prix,
`sponsored_runs` vide. La question du modèle économique est **non résolvable en local**.

**Négatif dur (comparaison multi-modèles)** : un seul modèle couvre 70,2 % du corpus, DeepSeek
a un thread à zéro message. La base ne permet **aucune** comparaison de performance entre
modèles. Tout ce qui précède est documentaire, pas observationnel.

### État après patches
Les 10 défauts sont corrigés dans les fichiers. Ce qui reste ouvert et non corrigeable
localement : grille de prix, configuration d'effort de chaque mesure AA, méthodologie AA
Omniscience, date exacte d'expiration du gratuit Ling, correspondance checkpoints ↔ service
hébergé, volume d'entrée par tâche de Solar Mini 4.

---

## 2026-10-06 — Passe 4 : I0 phase 1 (français, mesure locale)

Livrable : `research/i0-francais.md`. Mesure sur les 8 bases `desktop-v2.db`, lecture seule.

### Erreur de mesure attrapée en vol
Mon premier calcul a affiché **« 3 réponses françaises sur 15 »**. Chiffre faux. Le champ `text`
lu était celui de la part `kind='reasoning'`, pas `kind='text'`.

Décompte réel des parts assistant :

| kind | occurrences |
|---|---:|
| `tool` | 17 838 |
| `reasoning` | 9 960 |
| `text` | 9 841 |
| `ad` | 2 144 |
| `changes` | 394 |
| `notice` | 19 |
| `compaction` | 80 |

Reprise sur `kind='text'` : **12 réponses françaises sur 15**. Raisonnement anglais sur
13/15. Les deux langues diffèrent, et c'est la mesure — le raisonnement interne n'est pas
affiché à l'utilisateur.

**Leçon** : dans cette base, « réponse d'un assistant » n'est pas un champ, c'est un
filtre sur `kind`. Toute mesure de langue, de ton ou de longueur qui ne pose pas ce filtre
mesure le raisonnement.

### Erreur d'attribution attrapée en vol
Deux IDs de modèle sont apparus dans mes premiers décomptes : `m-00032eaeec` et
`m-916b95b337`. Vérification par recherche directe dans les 3 tables : **absents de toute
base**. Artefacts de scripts, écartés. Les threads concernés portent en réalité
`m-22ff70c712`.

### Résultat

| Modèle | threads | prompts FR | final FR | final EN |
|---|---:|---:|---:|---:|
| `m-22ff70c712` — ID non résolu | 9 | 8 | 6 | 2 |
| `stealth/space-bunny-alpha` | 5 | 5 | 4 | 1 |
| `z-ai/glm-5.3-flash` | 2 | 2 | 2 | 0 |
| `deepseek/deepseek-v4-flash` | 1 | **0** | 0 | 0 |
| **Total** | 17 | **15** | **12** | **3** |

Signaux : réponse finale entièrement anglaise **3/15** · réponse française s'ouvrant en
anglais **1/15** · réponses mixtes **5/15** · raisonnement anglais **13/15**.

Défaut net : une fuite de narration de processus en anglais en tête d'une réponse française
(`space-bunny-alpha`) : *« I'll start by loading the memory protocol… »*.

### Contre-preuves trouvées contre la mesure elle-même
1. **Zéro échantillon pour les modèles décisifs.** MiMo Flash, MiMo Pro, Ling, Muse, Luna,
   Solar, Laguna : aucun message français local. DeepSeek : 1 thread, **0 message**.
   Les deux défauts que je recommandais sous réserve de français n'ont **jamais parlé** ici.
2. **`m-22ff70c712` non attribuable.** ID opaque, absent du catalogue local
   (`~/.cache/opencode/models.json`, 8615 entrées) et de tout fichier de configuration.
   9 threads / 296 messages sans nom. Ne pas deviner à quoi il correspond.
3. **Prompts non identiques entre modèles.** n=15 organiques : aucune comparaison
   inter-modèles n'est licite. La phase 1 tranche le scénario « le modèle ignore la langue »,
   pas la qualité.

### Décision
La phase 1 **ne clôt pas I0**. Elle écarte une hypothèse (ignorance de la langue du prompt) et
produit un instrument : 10 prompts identiques + grille binaire 12 critères dans
`i0-francais.md`. Priorité inversée par rapport à l'ordre initial : **I0 avant I2**, parce que
c'est le seul test qui peut rendre les deux défauts à 0-10/h réutilisables, et parce que la
fenêtre Ling ferme le 2026-10-13.

Blocage : le passage manuel sur Freebuff n'est pas automatisable depuis ici.

---

## 2026-10-06 — Passe 5 : I9, signaux faibles

Livrable : `research/signaux-faibles.md`. Investigation nouvelle, proposée par l'utilisateur :
« ce qui se dit sur ces LLM, par les réseaux sociaux ».

### Protocole
Mémoire d'abord (`search_memory`, requête signaux faibles/réseaux) → **cache miss** →
recherche web autorisée → write-back obligatoire.

Sources et statut :

| Source | Statut |
|---|---|
| HN Algolia API | **primaire, citable** — story ID, points, date, URL |
| `artificialanalysis.ai/models/<slug>` | **tier 1** — sert à vérifier mes propres chiffres |
| Reddit `r/LocalLLaMA` API JSON | **403 bloqué** |
| Reddit via blogs agrégateurs | **tier 3** — signal, jamais fait |
| X/Twitter, Discord | non touchés |

### Deux vérifications qui ont échoué puis réussi
1. **Hypothèse : mon 41,1 pour Ling 3.1 est un chiffre fantôme.** Une source tier 3
   affirmait qu'AA n'avait pas de page Ling-3.1 au 30/09. Résolution : fetch direct de la
   page → **« Ling 3.1 Flash scores 41 on the Artificial Analysis Intelligence Index »**.
   **Confirmé.** Mais deux colonnes de mon tableau étaient vides alors qu'AA les publie :
   **211 tok/s** et **0,99 $/tâche**. Remplies.
2. **Mon « DeepSeek est 4,8x plus rapide que MiMo Pro » est un rapport de fournisseurs.**
   AA mesure V4.1 Flash à 214,4 tok/s et le V4 Flash qu'il remplace à **214,9** — égalité.
   Les 280-500 t/s du premier jour ne se reproduisent pas. Mon propre `trace.md:109`
   avait déjà la donnée : MiMo Pro = 26 tok/s chez DeepInfra, 310 chez PrimaLabs.
   **Réserve ajoutée au `comparatif.md` §3.**

### Confirmation utile
La page AA de DeepSeek s'intitule **« DeepSeek V4.1 Flash (max) »** — le suffixe d'effort y
figure. Preuve directe à l'appui de la réserve C2 pour ce modèle précis.

### Trois signaux négatifs sur mes propres recommandations
| Recommandation | Signal trouvé |
|---|---|
| MiMo-V2.6 (escalade) | « benchmaxxed scam » : 9 trous de sécurité en 3 min ; **retraining `-MOPD` silencieux le 25/09**, poids API échangés sans renommer |
| GLM-5.3-Flash (défaut code) | « not reliable enough to trust at scale » ; a répondu *« this is simple and I know better »* en contournant des garde-fous |
| DeepSeek V4.1 Flash (défaut vitesse) | **troncature silencieuse** en milieu de phrase, noté 1,5/10 « content freedom » |

Aucun n'est rédhibitoire pour l'usage code/config. Tous doivent entrer dans les fiches.

### Un croisement fort
GPT-6 Luna : *« roughly 5-8% gets censored and doesn't get a response »* **et**
*« it feels slow for me and **compacts often** »*. La compaction est le **seul** finding de mon
dossier local (I5, 101 événements) qui soit corroboré par une source externe indépendante.
Deux sources, une observation : c'est la corroboration la plus solide du dossier.

### Deux absences
- **Solar Pro 4 et Solar Mini 4 : zéro signal social.** Requêtes HN vides, aucun fil.
  *(→ **corrigé en passe 7** : c'est une absence **HN**, pas une absence de signal.)*
- **Freebuff : aucune trace pertinente sur HN.** La plateforme qui porte le budget n'est
  discutée nulle part.

Leçon : absence de critique ≠ absence de défaut. Dans ce dossier, deux modèles recommandés
à 0/h et 5/h sont **non évaluables socialement**.

### Erreur d'édition en vol
En ajoutant I9 à `investigations.md` j'ai remplacé l'en-tête `## P3 · Restants ☐` au lieu de
l'insérer avant, épiant I7 et I8 orphelins. Repéré par `grep "^## "` et corrigé. **Leçon** :
un `edit` sur un en-tête de section doit inclure l'en-tête dans `newString`.

### État
`comparatif.md` : 1 ligne complétée (Ling), 1 réserve ajoutée (vitesse DeepSeek).
`investigations.md` : I9 ajouté, ordre d'exécution inchangé pour l'instant.
Reste : I9bis sources chinoises, X/Discord, accès direct Reddit.

---

## 2026-10-06 — Passe 6 : I9 pass 2, sources chinoises

Instruction : « oui, pousse les investigations ». Reprise de I9 sur le terrain annoncé
comme le plus dense — les sources chinoises.

### Protocole
`search_memory` (sources chinoises / 评测 / 知乎 / 微博) → **cache miss** → 9 requêtes web en
zh → write-back obligatoire. Livrable : `research/signaux-faibles.md` § pass 2.

Le seul fait mémoire qui ressortait : *Mistral sert GLM 5.2 (Z.ai) depuis le 11/08*. Sans
portée sur les douze — mais c'est le premier résultat utile de la session sur ce périmètre.

### Ce que la langue a changé
La couverture anglaise (HN) donnait des **opinions**. La couverture chinoise donne des
**chiffres**, et trois fois elle a contredit ma lecture :

1. **GLM : mon chiffre tenait, le leur était périmé.** Z.ai et les médias chinois citent
   « 57, 3e mondial » — obtenu sur l'index **v4.1.1** du 26/08. AA a re-baseliné en **v4.3.2**
   le 07/09 : **42**, et le coût par tâche passe de 0,09 $ à 0,25 $. Mon `comparatif.md` dit
   41,8. **J'aurais pu « corriger » mon chiffre à 57 sur la foi d'une source tierce — j'aurais
   cassé une donnée juste.** Leçon : vérifier la *version* avant de céder à un recoupement.

2. **MiMo : le signal Reddit était juste sur le fait, faux sur l'intention.** Le blog officiel
   `mimo.xiaomi.com` publie le post-mortem complet — flooding 11,1 % → 24,6 % sur 20 steps,
   threshold à 32 trop lâche, alternative MixRL à **2,31 M$** rejetée, **MOPD à 90 k$**
   (4 %) retenue, exemple tracé à **59 appels d'outil**. Les checkpoints MOPD sont *dans* la
   collection publique. Ce que j'ai écrit comme « retraining silencieux » est un correctif
   annoncé avec ses coûts. **Un adversaire qui publie son propre échec chiffré n'est pas en
   train de cacher quelque chose.** Je réécris.

3. **DeepSeek : le gain de vitesse ne se paie pas en euros.** Test 14 tâches / 300M tokens :
   V4.1 a coûté **36 % de plus** que V4. Et sur une tâche il est sorti *plus lentement* avec
   *moins* de tokens — parce que le temps d'outil est passé de 6,6 à 18,7 minutes. Écrire vite
   et vérifier longtemps, c'est plus lent.

### Un finding qui sort de mon propre dossier
I3 (« l'effort est-il un cadran de qualité ? ») était une **hypothèse** dans
`investigations.md`. Deux sources chinoises s'y sont contredit, et c'est la contradiction qui
fait la preuve : en question courte l'effort est monotone (100/98/92), en retrieval 128K il
**s'inverse** (`high` 75,3 % > `max` 71,6 %). Plus le défaut : si `reasoning_effort` est
absent, GLM tourne en **`max`** — ratio mesuré 0,984. Gratuit à 10/h sur Freebuff, probablement
au régime le plus cher.

J'ai promis dans le tableau de routage du `verdict.md` que I3 donnerait « un résultat en une
heure ». Il l'a donné — en passant par le chinois.

### Une confirmation méthodologique utile
Les tableaux de comparaison AA n'affichent qu'un seul nombre « AA-Omniscience », alors qu'AA
en publie **trois** (`Index`, `Accuracy`, `Non-Hallucination Rate`). J'ai cru une fois de plus
ne pas pouvoir caler mes colonnes. Vérification sur DeepSeek : `Index = −5`,
`Accuracy = 46 %`, `Non-Hallucination = 4 %` — et mon tableau dit 46,4 / 3,5.
**Mes colonnes étaient bonnes.** Le `n.d.` de GLM reste `n.d.` : sans méthodologie, je ne
remplis pas.

Effet collatéral : l'`Index` **−5** de DeepSeek contre **+7** de GLM est un comparateur de
même échelle que je n'avais pas. §4 renforcée, réserve C2 inchangée (DeepSeek mesuré à `max`).

### Erreur évitée
Un `edit` raté aurait pu réécrire « DeepSeek est 4,8x plus rapide » alors que deux sources
chinoises confirment ce que mon propre §3 disait déjà : l'écart est un rapport fournisseurs.
La donnée AA (214,4 vs 214,9) est restée la bonne. **Ne pas corriger ce qui est déjà corrigé.**

### État
- `signaux-faibles.md` : 216 → 379 lignes (§ pass 2 ajouté).
- `comparatif.md` : note de version v4.3.2 vs v4.1.1 ; §4 enrichi (Index −5/+7) ;
  §6 enrichi (défaut `max`, inversion long-contexte, DeepSeek +14).
- `investigations.md` : I9 pass 2 décrit sous le « Reste ouvert ».
- Reste : X/Twitter, Discord, accès direct Reddit (403), toute donnée Solar.

---

## 2026-10-06 — Passe 7 : investigation Solar Pro 4

Instruction : « faire une investigation poussée, creuser tout ce qui tourne autour du LLM
Solar Pro 4 ». Puis « continue if you have next steps ».

### Protocole
`search_memory` (Solar Pro 4 / Upstage / tarif) → **cache miss** sur le fond (le seul hit
utile confirmait que mon `42` était déjà étiqueté « index antérieur, non comparable ») →
recherche web → **lecture directe des pages sources**, pas des résumés :
`artificialanalysis.ai/models/solar-pro4`, `freebuff.com/llms.txt`, GitHub `CodebuffAI/freebuff`.
Livrable : `research/solar-pro-4.md`.

### La leçon méthodologique de la passe
**Ouvrir la page modèle AA valait plus que dix recherches web.** La page répond en une lecture
à trois questions que mes tableaux ne posent pas :

1. le chiffre porte-t-il un `*` avec *« Estimate (independent evaluation forthcoming) »* ?
2. les courbes de détail disent-elles *« Not publicly available »* ?
3. le rang est-il `#N / 176` ou `#N / 117` (index différent) ?

Ici : **oui, oui, et #19/176**. Un tableau dont toutes les courbes de détail sont
*Not publicly available* **ne peut pas être rempli** — et Solar Pro 4 est le seul des douze
dans ce cas. Sous C2, il ne devrait pas être classé du tout.

### Les cinq corrections

1. **`42` → `28`, et le `28` est une estimation.** Mon chiffre venait de l'article AA du
   12/08 (v4.1.1) ; la page actuelle est en v4.3.2. **Exactement l'inverse du cas GLM**
   (57 → 42, où c'était *leur* chiffre qui était périmé). Même mécanisme, direction opposée :
   la leçon est **vérifier la version avant de céder à un recoupement**, pas « le web a tort ».
2. **`99 tok/s` → `115,1 tok/s`**, TTFT `2,13 s` → `1,91 s`, `#61/176`. Ma note de travail
   était fausse ; corrigée.
3. **« Zéro signal social » était faux.** HN est bien vide, mais Reddit `r/opencodeCLI`,
   ARENA.ai (44ᵉ) et `freebuff.com/live` (253 utilisateurs, 5ᵉ/12) existent. Formulation
   corrigée dans `signaux-faibles.md`, `investigations.md` et en note dans Passe 5 —
   **sans réécrire le journal** : on annote, on n'efface.
4. **`0/h` non corroboré — conflit à trois sources.** Capture tier 3 : 0/h. `mvalentsev` :
   10 FB/h. README GitHub : *« unmetered at full access »*. Et `llms.txt` dit *« Freebucks buy
   one-hour model sessions »*, ce qui **équilibre les deux** et impliquerait que GLM, DeepSeek,
   MiMo Flash et Solar Mini sont **aussi** à 0 — contredisant ma propre grille. Aucune source
   concluante.
5. **Le catalogue a dérivé.** Le picker actuel contient Gemini 3.8 Flash et GPT-6.1 Sol, et
   **ne contient ni Ling ni Laguna**. Cinq changements en trois semaines. Ouvert en **I10**.

### Un fait utile acquis
`freebuff.com/llms.txt` fixe la **France à 60 Freebucks/jour** en *full access*. La prémisse
budgétaire « 60/jour » du projet est donc **validée par la source primaire** — et la France
est bien en mode *full*, pas *limited*. `mvalentsev`, lui, annonce « 100 aux USA, 70 ou 40
ailleurs » : **prouvablement périmé**, ce qui jette le doute sur ses prix horaires aussi.

### Le finding le plus grave n'est pas un chiffre d'index
**CrucibleMark** (test indépendant) signale une **« tool use hallucination »** qualifiée de
*disqualifying signal*, plus un P95 de **95,33 s** qualifié de *Problematic*. Pour un agent
qui exécute des commandes, une hallucination d'outil coûte plus cher qu'un index bas.
C'est entré en I4, avec la mention que **le protocole I4 n'est pas exécuté**.

### État
- `solar-pro-4.md` : **créé** (livrable de la passe).
- `comparatif.md` : ligne Solar corrigée (28†, 115 tok/s, 524K, ⚠0/10) + footnotes `†` et `²`
  + note de version Solar + banner §6 enrichi + points 4 et 5 de § « Ce que le budget dit ».
- `signaux-faibles.md` : « zéro signal » → « absent de HN », note³, ligne « Reste ouvert » levée.
- `investigations.md` : I2 avancée (60 FB confirmé, tarif non), I4 enrichie, I9 corrigée,
  **I10 ouverte** (dérive du catalogue).
- `README.md` : ligne `solar-pro-4.md` ajoutée.
- Reste : X/Twitter, Discord, Reddit direct (403), **protocole I4 non exécuté**,
  **I10 à traiter avant tout arbitrage**.

---

## 2026-10-06 — Passe 8 : I10 (catalogue) + I4 exécuté

Deux investigations demandées ensemble. **I10 a restructuré le tableau ; I4 a livré une
mesure et s'est heurtée à un mur.**

### Ce qui a été fait

**I10 — le catalogue réel.** Quatre sources primaires du jour relues et recoupées :
`freebuff.com/llms.txt`, `/plans`, `/live`, GitHub README (npm : 403, écarté). **Les quatre
s'accordent sur les mêmes 12 modèles.** Diff avec mes douze : **Ling et Laguna sortent,
Gemini 3.8 Flash et GPT-6.1 Sol entrent.**

**I4 — exécuté sur les 8 bases locales** (1 510 messages, 4 modèles). Deux prototypes de
détection testés et **tous les deux réfutés**, voir ci-dessous.

### Corrections

1. **Ling 3.1 Flash et Laguna S 2.1 ne sont pas des modèles Freebuff.** Quatre catalogues
   primaires ne les connaissent pas. **Ma grille leur attribuait 0/h — faux.** Leurs fiches
   portent désormais un encadré « hors catalogue », et leurs lignes du tableau aussi. Leur
   gratuité réelle vient d'OpenRouter/Vercel, **pas de tes Freebucks**.
2. **Gemini 3.8 Flash et GPT-6.1 Sol manquaient** — et sont **payants en France**
   (`Access = Paid plans` / `US, or paid plans elsewhere`), tout comme **Muse Spark 1.3**,
   mon meilleur noté. **Conséquence : 12 modèles au catalogue, 9 utilisables** sur ton compte
   gratuit. Le tableau passe à 14 lignes (12 + 2 hors catalogue).
3. **Le conflit tarifaire Solar Pro 4 est levé.** `/plans` publie **`∞ Unlimited hrs Solar Pro
   4`** + badge `Promotional` → **0/h confirmé** par deux sources primaires, `mvalentsev`
   (10 FB/h) contredit. **Mais** le 0/h est promotionnel : échéance **09/10/2026**.
4. **DeepSeek V4.1 Flash Fast existe bien.** J'avais écrit « aucune source ne mentionne ce
   produit » — les cinq pages Freebuff le listent. Ce qui manque, c'est l'**origine upstream**,
   pas l'existence.
5. **`m-00032eaeec` n'était pas un artefact.** `world_snapshot.model` le résout en
   **`mimo/mimo-v2.5`** (266 messages), retiré du catalogue le 2026-09-22. **I0 était faux**
   sur ce point — corrigé dans `i0-francais.md` et `README.md`.
6. **Détection de refus : les deux méthodes échouent.** Regex sur `parts` mixtes → 37 % de
   « refus » ; isolé sur `kind='text'` → 9,4 %, **mais ce sont des réserves honnêtes**
   (« ce que je ne peux pas trancher »), pas des abstentions. Un agent qui déclare ses limites
   n'est pas un agent qui refuse. **Le taux mesure un style, pas l'abstention.**

### Ce qui bloque

**Solar Pro 4 = 0 échantillon local** (0 message sur 1 510). Le protocole I4 **ne peut pas
répondre** sur le modèle qui motivait l'investigation. Il reste **exécutable en session live** :
les 10 prompts sont extraits (576 prompts utilisateurs réels), **à filtrer — un token Discogs
en clair s'y trouve**.

### Ce qui reste vrai, conditionnel

- **Gratuit.** Solar Pro 4 et Space Bunny Alpha à 0/h confirmés ; Solar Mini 4 à 5/h,
  GLM/MiMo Flash/DeepSeek à 10/h dérivés de `/plans`.
- **Instable.** *« A model's Freebucks cost can vary »* — Freebuff dit lui-même que les prix
  bougent. Le tri par prix est une photographie, pas une spécification.

### État
- `comparatif.md` : 14 lignes (12 catalogue + 2 hors), footnotes `²`/`⁴`/`⁵`/`⁶` réécrites,
  grille §6 refaite, « Ce que le budget dit » remplacé (9 utilisables sur 12).
- `investigations.md` : **I10 en section complète (P0)**, **I4 marquée exécutée + bloquée**,
  I2 et l'ordre d'exécution ré-ancrés sur le **09/10** (et non le 10-13, qui concernait Ling).
- `fiches/` : **14 fiches** — `gemini-3.8-flash.md` et `gpt-6.1-sol.md` créées ; Ling, Laguna
  (hors catalogue), Muse Spark (payant), DeepSeek Fast (existe), Solar Pro 4 (0/h confirmé)
  corrigés.
- `solar-pro-4.md` : § 7 conflit levé, § 8 traité, sources complétées.
- `i0-francais.md`, `README.md` : ID `m-00032eaeec` résolu.
- Reste : benchmarks de **Gemini 3.8 Flash** et **GPT-6.1 Sol** non collectés ; capture du
  picker pour confirmer les 12 affichés ; **I4 en session live avant le 09/10**.

---

## 2026-10-06 — Passe 9 : nouvelle source + extension du périmètre

Ressource ajoutée : **`freebuff-changelog.nordicnode.workers.dev`**. Périmètre élargi :
**veille, explications, tips & tricks** sur les LLM et l'usage de Freebuff →
`research/veille.md` (créé).

### Ce que la source donne

**Tier 2, pas tier 3.** Elle ne raconte pas : elle **diffuse les commits publics**
`CodebuffAI/freebuff` et renvoie au permalink GitHub, avec un résumé « plain English » et le
diff. Chaque entrée est donc recoupable. Limites : projet tiers, corrections via issue →
`data/overrides.json`. **À recouper avant d'affirmer.**

Elle fournit ce que je n'avais pas :
- **Frise du catalogue** : **20 modèles depuis le 05/08, 12 vivants, 8 retirés,
  23 changements** — mon « 5 changements en 3 semaines » venait de `mvalentsev` et était
  **trop bas**.
- **RSS** : `/feed-models.xml` (catalogue) et `/feed.xml` (tout) — le seul abonnement à
  prendre au sérieux.
- **Sections `unlimited` / `optimized`** : c'est *ça* qui dit si un modèle est gratuit, pas
  son prix. Fichier source : `common/src/util/freebuff-picker-sections.ts`.

### Corrections immédiates

1. **Solar Mini 4 n'est plus gratuit depuis le 05/10/2026** — *« free promotion ended »*.
   **Mon `5/h` est périmé d'un jour**, et tout l'argument « l'aubaine du panel » tombe.
   Fiche corrigée avec encadré, ligne du tableau en `🔒 payant ⁷`, grille §6 idem.
2. **Solar Pro 4 est entré en gratuit le même 05/10**, en passant d'`optimized` à
   `unlimited`. Sa date d'entrée réelle est le **05/10**, pas depuis toujours : le 0/h a
   quelques jours. Historique : trial le 08-28, retrait 09-23, retour 09-25, gratuit 10-05.
3. **Deux promotions opposées le même jour** — c'est la preuve que « gratuit » est un
   **état promu, pas un prix**.
4. **`GPT-6.1 Sol` : « promotional 100 Freebucks »** (09-29) — premier prix Freebucks brut
   récupéré pour un modèle du catalogue. Unité non précisée → **non converti en heures**
   (footnote `⁸`).
5. **Gemini 3.8 Flash a vécu deux vies** : gratuit le 09-03 (« the priciest row per message »),
   retiré le jour même, ré-ajouté le 09-22 **derrière abonnement**.

### Nouveau fait utile au modèle économique (I2/I6)

Champ `freebucksRefundSources` ajouté le **06/10** : le remboursement se sépare en
**`daily`** et **`wallet`**. **Les deux poches existent côté protocole** — ce que je ne
pouvais pas prouver en local.

### État
- `research/veille.md` : **créé** — 4 sources Freebuff classées, 6 explications à écrire,
  7 tips prouvés, règles, todo.
- `comparatif.md` : Solar Mini 4 → `🔒 payant ⁷`, GPT-6.1 Sol → `100 promo ⁸`, footnotes
  `⁶`/`⁷`/`⁸`, `⁴` corrigée (npm 403).
- `investigations.md` : I10 enrichie (23 changements, deux promotions, `freebucksRefundSources`).
- `fiches/solar-mini-4.md` : encadré d'obsolescence.
- `solar-pro-4.md` : date d'entrée 05/10 + ligne changelog dans le tableau des tarifs.
- `README.md` : ligne `veille.md`.
- Reste : **abonner `feed-models.xml`** ; écrire les explications 1 et 2 ; recenser les
  8 modèles retirés ; étendre la partie LLM de la veille.

---

## 2026-10-07 — Passe 10 : relevé des 36 dernières heures — le catalogue passe à 11

**Déclencheur** : « des mises à jour de Freebuff ont été faites ces dernières heures ».
**Méthode** : mémoire d'abord (mémoires `status:CONFIRME` du 06/10 → warm route), puis
re-fetch des sources, puis **recoupement commit par commit sur GitHub Tier 1** conformément à
la règle § 4 de `veille.md` (« recouper une entrée du changelog sur le commit »). Clone
sparse du dépôt public pour lire les fichiers sources eux-mêmes, pas les résumés.

### Sources relues (2026-10-07 06:01–06:10 UTC)

| source | tier | état |
|---|---|---|
| `freebuff-changelog.nordicnode.workers.dev/feed.xml` | 2 | 60 entrées, **36 depuis le 06/10 14:00** |
| ↳ `/feed-models.xml` | 2 | 24 entrées, catalogue : **« 11 live · 9 retired · 20 all-time »** |
| `freebuff.com/llms.txt` | 1 | **11 modèles** au picker |
| `freebuff.com/plans` | 1 | **11 lignes**, Solar Pro 4 et GPT-6.1 Sol en `Promotional` |
| GitHub `CodebuffAI/freebuff` | 1 | commits `c3edf98738bd`, `ce46ee14b2a4`, `03cf8e76c4d8`, `3cdc0facd415` **lus en diff** |
| GitHub fichiers sources | 1 | `freebuff-solar-promo.ts`, `freebuff-sol-promo.ts`, `freebuff-models.ts`, README **lus en entier** |

### Les 6 faits des dernières heures

1. **🪦 Space Bunny Alpha retiré** — suppression du picker le **2026-10-06**, commit
   `c3edf98738bd` le **07/10 00:14Z**. Cause (commentaire du commit, primaire) : OpenRouter a
   retiré tous les endpoints le **05/10** ; la lane gratuite d'OpenCode Zen a refusé **tout**
   le trafic à partir de ~20:45Z, et **chaque sonde de la file, une toutes les 5 minutes pendant
   plus d'une heure, a été refusée**. Aucun repli payant par conception → l'utilisateur
   attendait la fin de la file pour un refus. *Paused, not deleted* : les binaires publiés
   portent l'id. **13 jours de service gratuit.**
2. **GLM 5.3 Flash : fin de promo, 10 → 15 FB/h** — commit `ce46ee14b2a4` (06/10 20:06Z),
   `freebuff-glm-promo.ts` **supprimé**, commentaire : *« A promotional 10 ran 2026-10-03 to
   2026-10-06; the price is 15 again and carries no label »*.
3. **Solar Mini 4 : `unlimited` → `optimized`** — commit `03cf8e76c4d8` (06/10 08:46Z),
   *« free promotion ended on 2026-10-05 »*.
4. **GPT-6.1 Sol : gratuit aux US, 1 session/jour partout** — `freebuff-sol-promo.ts` :
   *« Free in the US, a paid plan elsewhere, until the promotion ends »* + prix promotionnel
   **100 Freebucks**, limite **enforcée côté admission** (`FREEBUFF_DAILY_SESSION_LIMITS`).
5. **Solar Pro 4 : 0/h « open-ended »** — `freebuff-solar-promo.ts` : *« A promotion with no
   end date yet »*, posé le **05/10 07:15Z**. Historique complet de **9 bascules datées**.
6. **DeepSeek V4 Pro retiré** (hors des 12 : `3cdc0facd415`) + Claude Sonnet 4 aliasé sur
   Sonnet 4.6 + releases CLI 0.2.20 / 0.2.21 / 0.2.22 + tooltips raccourcis.

### Trois erreurs corrigées, dont une de raisonnement

1. **`verdict.md` § 1 « banc d'essai gratuit = Space Bunny Alpha » → CADUC.** Modèle parti.
   Remplaçant : **Solar Pro 4 (0/h)**.
2. **L'échéance « 09/10/2026 » du 0/h de Solar Pro 4 était FAUSSE.** Elle venait de l'offre
   **API Upstage −70 %**, pas du prix Freebuff, qui est **sans date**. Publié en passes 7, 8
   et 9, corrigé en passe 10 dans `comparatif.md` (⁶), `solar-pro-4.md` (§ 7 et § 9) et la
   fiche. **Leçon : un badge `Promotional` dit « ça peut changer », pas « quand ».**
3. **La chronologie Solar Mini 4 était inversée dans la fiche (passe 9)** : j'avais écrit
   « le 5/h était le prix d'une promo ». **C'est l'inverse** : 5/h depuis le lancement
   (23/09), **0/h du 02/10 au 04/10** puis retour à 5/h. Mon chiffre de tableau était bon,
   mon encadré de correction était faux.
4. *(mineur)* **GLM à 10/h était le prix promotionnel**, pas le prix courant — mon tableau
   datait de la fenêtre 03/10→06/10. Corrigé en **15/h** (fiche + `comparatif.md` ⁹).
5. *(mineur)* **Solar Mini 4 était marqué `🔒 payant`** : il n'est **pas verrouillé par
   abonnement**, il est *métré* (5 FB/h, 12 h/jour avec 60 FB français). Corrigé.

### Avancement sur I2/I6 (prix par modèle)

**Le tiers de la question est levé.** Les prix **datés** sont publics dans le dépôt :
`SOLAR_PRICE_CHANGES` (9 bascules horodatées), `freebuff-sol-promo.ts` (100 FB),
`freebuff-glm-promo.ts` (15 → 10 → 15), commentaires de `freebuff-models.ts`
(MiMo Pro **30**, DeepSeek Fast **25/50 en pointe**).
**Second réfecteur** : les heures de `/plans` — **17 h pour GLM et DeepSeek, 26 h pour MiMo
Flash** → ratio 1,53 = **15 FB vs 10 FB**. Les deux sources convergent.
**Reste bloqué** : la carte complète `prices[modelId]` est côté serveur (`freebucksPricing()`),
hors dépôt. **I2 et I6 passent de « ouverts » à « partiellement résolus ».**

### État des fichiers modifiés

- `fiches/space-bunny-alpha.md` — encadré 🪦 complet, avantages/verdict/commentaires caducs,
  réponse à sa propre question (« combien de temps ? » → **13 jours**).
- `fiches/glm-5.3-flash.md` — 10 → **15/h**, verdict recalé (9 h 40 au lieu de 14 h 30).
- `fiches/solar-pro-4.md` + `research/solar-pro-4.md` — échéance fausse corrigée,
  **historique de prix daté ajouté**, verdict § 9.5 réécrit.
- `fiches/solar-mini-4.md` — chronologie inversée corrigée, **5 FB/h** confirmé.
- `fiches/gpt-6.1-sol.md` — bandeau du code, 100 FB, 1 session/jour enforcée, effort `high`.
- `fiches/deepseek-v4.1-flash-fast.md` — **25/50 FB** selon l'horloge DeepSeek.
- `comparatif.md` — catalogue 11, 8 utilisables, lignes Space Bunny/Solar Mini/GLM/Sol,
  footnotes ⁶/⁷/⁸ corrigées + **⁹ ajoutée**, § budget réécrit, **nouveau bloc passe 10**.
- `verdict.md`, `investigations.md` (I8/I10), `i0-francais.md`, `README.md` — 11 modèles,
  candidats de remplacement.
- `veille.md` — premier relevé daté + **5 nouvelles leçons sourcées**.

### Ce qui reste

- [ ] Abonner `feed-models.xml` (le RSS existe, l'abonnement non).
- [ ] Retrouver **la carte complète des prix Freebucks** (endpoint serveur ?) → I2/I6 fermés.
- [ ] Re-vérifier Solar Pro 4 **à chaque relevé** : la promo est sans date mais pas sans fin.
- [ ] Recenser les **9 modèles retirés** (le changelog les date tous).
- [ ] I8 à refaire **sur Solar Pro 4** (le banc d'essai gratuit a changé de modèle).

---

## 2026-10-07 — Moteur d'investigation, P1 (contrat + schéma + engine)

**Objectif** : industrialiser ce que les passes 1-10 font à la main (collecte → recoupe →
édition → journal → mémoire), avec un adapter par plateforme (Freebuff, opencode, et plus
tard IDE/CLI) et des sorties cohérentes entre elles (fiches, comparatif, best-of).

**Décisions actées** : autonomie « proposer + appliquer les blocs GEN » (jamais la prose
humaine) ; cadence quotidien `check` + hebdo `--revalidate` ; moteur **dans ce dépôt** ;
2 adapters (Freebuff, opencode).

**Construit :**
- `moteur/ORCHESTRATOR.md` — une page : split code/jugement, 5 règles inviolables, pipeline,
  contrat adapter (« ajouter un outil = ajouter un fichier »), cadence, sorties, lint.
- `moteur/schema.json` — JSON Schema v1 : état plateforme = `facts` + `models` ; mesures AA
  **saisies** et conservées verbatim (marqueurs `**` / `*` / `†` intacts), prix structurés
  (value/unit/promo/end), historique daté avec preuve (url + tier + commit), sources avec
  `sha1`.
- `moteur/engine.py` — stdlib, zéro dépendance, 5 sous-commandes : `import` (backfill),
  `check` (rendu depuis l'état == fichier ?), `render` (bloc GEN), `show`, `lint`.
- `moteur/state/freebuff.json` — backfill des **14 lignes** du tableau de `comparatif.md`.

**Preuves (double vérification) :**
1. `import` → `check` = **OK sur 14/14 lignes** (round-trip parse ↔ rendu).
2. Migration : marqueurs `<!-- GEN:comparatif|run=2026-10-07 -->` / `<!-- /GEN -->` insérés ;
   `diff` pré/post-migration = **exactement 2 lignes ajoutées, 0 ligne de tableau modifiée**.
3. Test négatif : prix injecté `99/h` dans l'état → `check` **échoue** (exit 1, ligne citée),
   état restauré, `check` OK. Une garde qui n'échoue jamais ne prouve rien.
4. Le `check` a attrapé **3 défauts réels de mon propre code** pendant le développement :
   alignement du tableau (12 colonnes à droite, pas 2 — vérifié par programme, pas à l'œil),
   unité `15/h` (slash collé) vs `5 FB/h` (espace), gras des cellules `hors cat.`.
   Le contrat de rendu est donc calé sur le fichier, pas sur ma mémoire.

**Reste :**
- [ ] **P2** : titre de fiche imposé (`templates/fiche-llm.md`), appariement fiche↔état
  (champ `fiche` encore `null`), lint prix fiche↔comparatif, règles §7 non encore activées.
- [ ] **P3** : adapter Freebuff (`llms.txt`, `/plans`, feeds, GitHub, DB locale) + fetch/diff.
- [ ] **P4** : timer quotidien `check`, hebdo `apply --revalidate`.
- [ ] **P5** : mini-passe d'exploration **opencode** (qu'est-ce qui est gratuit, quelle
  source le prouve), puis `adapters/opencode.yaml`.

## 2026-10-07 — Moteur d'investigation, P2 (contrat de fiche + appariement + lint)

**Construit :**
- `moteur/templates/fiche-llm.md` — contrat : H1 `# Nom — Éditeur` (le segment avant ` — `
  doit slugsifier en l'`id` de l'état), **5 sections exigées** (Identité, Français,
  Avantages, Inconvénients, Sources — issues de l'intersection réelle des 14 fiches),
  **5 recommandées** (Puissance, Analyse de problèmes, Vitesse, Coût, Verdict).
- `engine.py` : `pair` (appariement mécanique `fichier.replace('.', '-') == id`),
  `migrate` (bloc `GEN:prix` après le H1, **pré-validation de toutes les fiches avant la
  moindre écriture**), `check` étendu (comparatif **+** chaque fiche), `render` atomique,
  `lint` (appariement bijectionnel, structure, H1↔id, prix fiche↔état, dérive du template).
- Prix canonique rendu **depuis l'état** dans les 2 surfaces (colonne Freebuff du comparatif,
  ligne `**Sur Freebuff :** …` de la fiche) : le prix n'est écrit qu'une fois.

**Preuves :**
1. `pair` = **14/14** appariés (règle mécanique vérifiée sur les 14 noms de fichiers).
2. Migration fiches : **42 ajouts, 0 suppression, 0 ligne modifiée** (diff strict).
3. Test négatif prix : ligne de fiche corrompue `15/h → 99/h` → `check` **échoue en citant
   les deux valeurs** → `render` répare **1/14** → `check` OK.
4. Test négatif structure : `## Français` renommé → `lint` **échoue** (exit 1) → restauré.
5. `lint` remonte **4 manques réels** (sections recommandées absentes de space-bunny,
   fast, gemini, gpt-6.1-sol) — signalés, pas bloqués : ce sont des lacunes connues, pas des
   régressions.

**Honnêteté — §7 non implémenté (et pourquoi) :**
- « retired ⇒ aucune prose ne dit “gratuit” » : analyse de prose = faux positifs garantis
  (les fiches parlent d'historique). Reporté, pas faussement déclaré.
- `index_version` / date de mesure dans `facts` : à saisir avec URL+date+preuve (P3).
- Règle « promo non-nulle = erreur » **supprimée** : elle aurait rejeté un état valable
  (la promo GLM à 10/h était légitime). Erratum de conception de P1.
- freebuff est **en dur** dans engine (`STATE_PATH`, `COMPARATIF`, `HEADER`, libellé
  « Sur Freebuff ») → à paramétrer en P5, avec un 2e vrai plateforme pour tester.

**Reste :** P3 (adapter Freebuff : fetch/parse/diff des sources + revalidation) — P4 (timer)
— P5 (exploration opencode, puis son adapter + paramétrage plateforme).

## 2026-10-07 — Moteur d'investigation, P3 (adapter + fetch/diff/apply)

**Construit :**
- `moteur/adapters/freebuff.json` — **JSON** (l'engine est stdlib : ni YAML ni parseur YAML ;
  §4 de l'ORCHESTRATOR mis à jour en conséquence). Health : llms.txt 200 + ancre `Freebuff`,
  sinon RUN ABORT. 6 sources : llms, plans, readme, picker_sections, solar_promo (tier 1) +
  feed RSS (tier 2). Alias déclaré : `meta/muse-spark-1.3-contributor`.
- `engine.py fetch` : santé d'abord, puis téléchargement de **toutes** les sources —
  tout-ou-rien (aucun écrit partiel), cache daté `moteur/cache/AAAA-MM-DD/` +
  `manifest.json` (sha1 par source, horodaté).
- `engine.py diff` : cache vs état sur 6 fronts — catalogue (RETRAIT/RÉAPPARITION = toujours
  **structurel**), accès README, allocations Freebucks, sections du picker, historique de prix
  solaire, lignes `/plans`, items du feed (tier 2 = « à vérifier », jamais preuve).
  Chaque extracteur vide = **problème explicite** (« format changé ? »), jamais de
  masse-retrait silencieuse. exit 0 = rien, exit 2 = changement.
- `engine.py apply` : **sous-ensemble sûr uniquement** (accès, allocations, sections,
  historique de prix, sources+sha1) ; structurel listé en « décision manuelle », non appliqué.
  `facts.freebucks` stocké `{value, evidence{url,tier,at}}` — la règle « tout fait porte
  source+tier+date » du schéma.
- Appariement de noms étendu : alias → commentaire×vendor (« V4.1 Flash » + `deepseek/…`
  → `deepseek-v4-1-flash`) → brut/base → formes normalisées (suppression du `v` de version,
  jointure chiffre : `solar-pro4` → `solar-pro-4`).
- Tri de l'historique sur l'instant **parsé** (ISO à fuseaux mixtes `-07:00`/`Z` : la
  comparaison lexicographique aurait pu mal ordonner). `.gitignore` : `moteur/cache/`.

**Preuves :**
1. Premier run réel : `fetch` 6 sources → `diff` **exit 2** (24 applicable, **0 structurel**,
   2 à vérifier, **0 problème**) → `apply` **24 ops** (13 sections None→valeur,
   10 transitions de prix, 5 allocations) → `diff` **exit 0 « aucun changement »**
   → `render` 0 ligne → `check` OK → `lint` OK. Idempotence de la boucle prouvée.
2. Test négatif A (GLM supprimé du cache) : diff signale **RETRAIT + divergences
   README et /plans** en structurel ; `apply` → **0 opération**, `status` de
   `glm-5-3-flash` **inchangé (live)**. Le retrait reste une décision humaine.
3. Test négatif B (phrases d'allocations mangées) : diff → **« 0 allocation extraite
   (format changé ?) »** exit 2.
4. Recoupement tier 1 des 2 items du feed tier 2 (protocole) : « Space Bunny Alpha
   withdrawn » → **CONFIRME** (absent de llms.txt et du picker ; état déjà `retired`
   2026-10-06) ; « DeepSeek V4.1 Flash Fast enabled » → **CONFIRME** (présent au
   catalogue llms.txt, section `powerful` du picker).
5. Restauration après tests négatifs : `sources[].sha1` == manifest réel (6/6).

**Honnêteté :**
- Contrat §4 disait `adapters/*.yaml` → **livré en JSON** (stdlib, zéro dépendance) ; §4 réécrit.
- Le format `llms.txt` des allocations **a changé le jour même** (bullets `- US: 150` →
  prose) : parser bullets + repli sur des phrases stables de la FAQ ; les deux vides =
  signal franc. Constaté et corrigé sur le run réel, pas simulé.
- `--revalidate` (hebdo) et `research/rapport.md` (§6) **non produits** : P4, avec le timer.
  `diff` imprime en stdout pour l'instant.
- Les items « à vérifier » du feed sortent du diff suivant (fenêtre = date du dernier
  fetch) : le recoupement se fait pendant la passe — il a été fait (preuve 4), pas repoussé.

**Reste :** P4 (timer quotidien + `--revalidate` hebdo + `rapport.md` persistant) —
P5 (opencode + paramétrage plateforme, freebuff encore en dur dans engine).

## 2026-10-07 — Moteur d'investigation, P4 (revalidation, rapport, timers)

**Construit :**
- `engine.py fetch` : réutilise les sources déjà en cache **le jour même** (répétitions du
  jour gratuites), `--revalidate` re-télécharge tout (hebdo). `fetched_at` par source dans
  le manifest (provenance honnête : une source réutilisée garde sa date de téléchargement).
- `engine.py diff` : (a) **fraîcheur** — une source de ≥7 jours = problème explicite
  (« `fetch --revalidate` ») ; (b) **`research/rapport.md`** = diff du dernier run
  (machine-owned, §6), écrit à chaque diff sauf `--date` (runs de test/manuels) ;
  (c) **dérive de provenance** — sha1 du cache ≠ sha1 de l'état = auto-op `sources`
  (l'état doit dire le dernier fetch réel ; un ressassage à sha1 identique est constaté
  sans forcer de cycle).
- `moteur/timer.sh quotidien|hebdo` + unités systemd --user (`moteur/timers/`) +
  `install.sh` : le timer traduit l'exit 2 du diff en 0 (un changement n'est pas un
  échec d'unité ; le détail vit dans `rapport.md`).

**Preuves :**
1. Réutilisation : `fetch` → « 0 téléchargée(s), 6 réutilisée(s) » (santé toujours probee).
   `fetch --revalidate` → 6 téléchargées ; le corps du feed a un sha1 **nouveau**
   (0f1c80bea194 → 1494321a824c) alors que l'extraction ne montre **aucun** changement
   de fait (24 items, 0 nouveau) → diff **exit 2** sur l'auto-op `provenance` → `apply`
   (1 op) → diff **exit 0**.
2. Rapport : contenu vérifié en exit 2 (verdict, constat, « Prochaine étape : apply… »)
   et en exit 0 (« aucun changement ») ; `diff --date` sur un cache de test laisse le
   rapport **intact** (md5 identique).
3. Fraîcheur : copie de cache datée de 9 jours → diff signale les 6 sources
   (« non revalidé depuis ≥7 j ») exit 2, rapport non touché.
4. Timers installés : `install.sh` → `list-timers` = quotidien jeudi 06:27 CEST,
   hebdo dimanche 07:31 CEST. Déclenchement manuel du service : `Result=success`,
   `ExecMainStatus=0`, manifest + rapport réécrits à l'horodatage du run (preuve d'exécution
   bout-en-bout dans systemd).
5. `timer.sh` : diff exit 2 → script exit 0 (contrat unité), fetch/diff OK en dry-run.

**Honnêteté :**
- La sortie du timer n'est **pas relisible** ici via `journalctl --user` (« No journal
  files were found ») : la preuve durable du run = `research/rapport.md` (+ mtimes).
  À ne pas confondre avec un timer silencieusement cassé.
- Le timer ne déclenche **jamais** `apply` : recoupement tier 1 + décision restent
  manuels (§1). Un diff non vide peut attendre la prochaine session.
- Corps feed ancien remplacé par le revalidate : le delta exact de sha1 n'est pas
  reconstituable (ancien octets non conservés) — seul l'extraction (inchangee) est traçable.
- `rapport.md` est écrasé à chaque run : l'historique reste `trace.md` (append-only, agent).

**Reste :** P5 (opencode : deuxième plateforme + paramétrage de engine, encore freebuff en
dur dans `STATE_PATH`/`COMPARATIF`/`HEADER`).

## 2026-10-07 — Moteur d'investigation, P5 (paramétrage plateforme + exploration opencode)

**Construit :**
- `engine.py --platform <nom>` (défaut `freebuff`) : `setup_platform()` charge
  `adapters/<nom>.json` et rebind les globals (`STATE_PATH`, `ADAPTER_PATH`,
  `COMPARATIF`, `FICHES_DIR/REL`, `RAPPORT`, `HEADER`, `ALIGN`, `PLATFORM_LABEL`,
  `FN_KEY`, `SOLAR_MODEL_MAP`) ; `HEADER`/`ALIGN` dérivent de `MEASURE_HEADERS` +
  libellé ; colonne prix indexée sur la **dernière** colonne (`c[-2]` contexte,
  `c[-1]` prix) ; échec franc si l'adapter est absent ou `platform` ≠ nom de fichier.
- Clés d'adapter : `label`, `model_map`, `research.{comparatif,fiches,rapport}`
  (absentes = plateforme sans tableau/fiches/rapport → `import`/`render`/`check`/
  `pair`/`migrate` refusés avec message explicite ; `lint` saute l'appariement).
- `compute_changes` porte désormais par **type de source déclaré** dans l'adapter
  (une plateforme sans `llms.txt`/`picker`/`plans` ne déclenche aucune fausse
  alarme « format changé ») + branche **état vide** : comptes et signal
  « ÉTAT VIDE — backfill requis », jamais de comparaison ; `build_observation`
  ne crie pas « non apparié » N fois si l'état est vide.
- Cache **par plateforme** : `moteur/cache/<plateforme>/AAAA-MM-DD/` (deux
  plateformes ne partagent jamais le même manifest ; cache freebuff migré) ;
  nouveau type de source `raw` = collecte horodatée (sha1, fraîcheur) sans extraction.
- `schema.json` : `fn` accepte n'importe quelle clé de plateforme (`string`),
  plus de `freebuff` en dur.
- `adapters/opencode.json` : health = `https://opencode.ai/docs/zen/` (200 + ancre
  `The free models`), 2 sources tier 1 `raw` (zen docs + catalogue provider) ;
  `state/opencode.json` = **état vide** (`models: []`).
- Note d'exploration **`research/opencode-gratuit.md`** (spec P5 — « qu'est-ce qui
  est gratuit, quelle source le prouve »). Format d'adapter : **JSON, pas YAML**
  (arbitrage acté en P3 : stdlib = zéro parseur YAML ; la spec P5 disait `.yaml`,
  corrigée par le fait).

**Exploration (mem-first, puis web) :**
- MnemoLite : santé 8001 OK, recherche hybride → **cache miss** (aucune mémoire
  opencode) → web tier1 autorisée.
- **Fait 1** : la doc officielle Zen liste **13 modèles 100 % Free** (input/output/
  cached-read), tous « for a limited time » ; zero-retention pour Space Bunny Free et
  LongCat 2.5 Preview Free ; NVIDIA trial-only pour Nemotron ; Jev 1.13 hybride
  (input $0.042, output Free).
- **Fait 2** : le catalogue `models.opencode.ai/providers/opencode` affiche **38
  lignes `$0.00 / $0.00`** — 25 de plus que la lane documentée : gratuité affichée,
  non documentée comme campagne → recoupement obligatoire avant publication.
- Write-back : mémoire `b080a388-5dc5-475c-89fc-ab613e032310`
  (`status:CONFIRME`, `project:llm-compare`, `source:b1cd19203d` + `source:661b5325f5`,
  `verifie-2026-10-07`).

**Preuves :**
1. NO REGRESSION freebuff (après paramétrage) : `show` ✓, `fetch` (cache migré,
   6 réutilisées), `diff` exit 0 avec les mêmes lignes de rapport (11/11, 10
   transitions, 11 lignes /plans, 24 items), `render` 0 ligne modifiée, `check` OK
   (bloc + 14 fiches), `lint` OK (4 avertissements réels préexistants).
2. Rejets francs : `--platform coucou` → « Adapter absent » exit 1 ; `import` sans
   `--force` sur un état présent → refus ; `platform` ≠ nom de fichier → refus.
3. opencode de bout en bout (état vide) : `show` 0 modèle → `fetch` (santé 200 +
   ancre, 2 sources, `moteur/cache/opencode/`) → `diff` exit 2 (1 auto-provenance,
   « état vide : 0 observation(s), 0 modèle dans l'état », **0 faux problème**) →
   `apply` (1 op, 2 sources) → `diff` exit 0 ; `render`/`check` refusés avec message
   explicite ; `lint` OK (0 modèle, sans fiche).
4. Sources vérifiées live : les 2 URLs répondent 200 ; ancre `The free models`
   présente ; extractions 13 lignes Free / 38 lignes 0.00 recomptées par programme,
   sha1 des corps figés dans la note et dans le manifest du cache.

**Honnêteté :**
- opencode n'a **aucun** pipeline de contenu pour l'instant : `raw` ne prouve que la
  fraîcheur (sha1/date), pas un fait. La preuve du « gratuit » vit dans la note +
  la mémoire, pas encore dans l'état — c'est le contrat P6.
- Les 38 lignes 0.00 ≠ contrat public : seul le bloc « The free models » de la doc
  Zen est une affirmation documentée ; le reste est un signal de catalogue.
- Les timers restent sur le défaut freebuff ; opencode s'appelle à la main
  (`--platform opencode`).
- Mémoire : warning non bloquant `namespace de tag inconnu 'platform:'` (registre
  EPIC-60) — le tag est volontaire pour le filtrage, il n'est pas dans le registre.
- Ancien doublon supprimé : la docstring de `import` mentionnait le chemin freebuff
  (reste en dur, illustratif — le chemin réel vient de l'adapter).

**Reste :** P6 (backfill opencode : extraire la lane free des zen docs dans
`state/opencode.json` — décider le périmètre : 13 lane documentée, ou 38 catalogue
avec statut de preuve distinct ; puis extraction type `zen_docs` et boucle quotidienne).

## 2026-10-07 — Moteur d'investigation, P6 (backfill opencode + boucle quotidienne)

**Décision de périmètre (actée) :**
- L'état porte **les 13 modèles de la lane free documentée** (doc Zen, bloc « The free
  models », prix `Free|Free|Free`), pas les 38 lignes `$0.00/$0.00` du catalogue.
- Raison : le contrat « gratuit » opposable est celui que la doc officielle documente
  (avec ses conditions : « limited time », zero-retention, NVIDIA trial-only). Les 25
  lignes restantes du catalogue sont un **signal** (prix affiché 0.00, non documenté en
  campagne) — promotion en modèles = décision manuelle ultérieure, avec recoupement
  (voir `research/opencode-gratuit.md`).
- Mémorisé : MnemoLite, type `decision`, `status:CONFIRME`.

**Construit :**
- Extracteur **`ex_zen`** (type `zen_docs`) : parse les `<table>` des docs Zen, retient
  la table d'en-tête `Input`/`Output` (écarte config et deprecation), liste les lignes
  `Input=Free` → `obs["zen_lane"]` ; résolution en `obs["zen_lane_ids"]` via
  `match_model` (mêmes règles d'appariement que freebuff : alias, slug, forme normalisée).
- `compute_changes` : logique **lane** gate sur `zen_docs` — retrait de la lane =
  structurel (décision manuelle, jamais appliqué), modèle non apparié = problème,
  extraction vide = problème (« format changé ? ») **sans** masse-retrait,
  état vide = comptes seulement. La provenance (sha1/fetched_at) reste universelle.
- **Backfill** `moteur/state/opencode.json` : 13 modèles générés depuis le cache du jour
  par `ex_zen` + `slugify` (recette triviale, reproductible) ; chaque modèle :
  `status: live`, `access: full`, `price {value: 0, unit: "Mtok", promo: true}` (la doc
  dit « limited time » → promo), `context: n.d.`, `measures: 10× n.d.` (colonnes AA
  freebuff hors périmètre opencode), `history[0]` = entrée prix avec evidence
  (url Zen, tier 1, quote de la ligne) ; `sources: []` jusqu'au premier apply.
- `fetch --revalidate` régénère le manifest avec le type `zen_docs` (le type de source
  vit dans le manifest, pas dans le corps caché).

**Preuves :**
1. Backfill ↔ source : `ex_zen` sur le cache donne **exactement** la liste des 13 noms
   extraits indépendamment en P5 (assert sur les deux ensembles, zéro écart) ; 13 ids
   uniques.
2. Boucle complète : `show` (13) → `lint` OK → `fetch --revalidate` (2× tier 1) →
   `diff` exit 2 (**lane 13/13**, seul auto = provenance) → `apply` → `diff` exit 0.
3. Test négatif A — retrait simulé (ligne `Exo Free` supprimée de la table de prix du
   cache) : diff = **structurel `RETRAIT lane : exo-free`**, 0 applicable ;
   `apply` n'applique rien (status **toujours `live`**) et liste la décision manuelle ;
   restauration octet-à-octet → diff exit 0.
4. Test négatif B — format mangé (cellules `Free` renommées) : diff = **problème**
   « 0 modèle free extrait (format changé ?) », **aucun** faux retrait des 13 ;
   restauration → diff exit 0.
5. Test négatif C — modèle ajouté à la lane (`Zozo 9 Ultra Free`) : diff = problème
   « modèle lane non apparié » (ajout d'état = décision manuelle) ; restauration → 0.
6. NO REGRESSION freebuff après P6 : diff / check / lint tous exit 0 (mêmes lignes de
   rapport, 4 avertissements réels inchangés).

**Honnêteté :**
- Le sha1 de provenance vient du **manifest** (« ce que le fetch a reçu »), pas d'un
  re-hachage du fichier : une édition manuelle du cache change l'extraction mais pas
  la provenance — c'est le contrat (le cache est machine-owned, on ne l'édite pas ;
  les tests le font puis restaurent octet-à-octet).
- `zen_catalog` (38 lignes 0.00) reste `raw` : collecté, fraîcheur prouvée, **jamais**
  découpé en faits — le catalogue n'entre dans l'état qu'après décision + recoupement.
- `unit: "Mtok"` et `promo: true` rendent « 0 promo » : honnête (campagne à durée
  limitée), mais le coût/ratio exact (quota ?) n'est **pas** documenté — `access: full`
  dit « pas de quota connu », pas « illimité garanti ».
- `generated_at` bouge à chaque `apply` même sans op (réécriture des sources) :
  c'est la date de dernière écriture machine, pas celle d'un changement de fait.

**Reste :** P7 (pistes) : extraction `zen_catalog` (promotion des 25 lignes 0.00 avec
statut de preuve distinct), table de dépréciation des docs Zen (19 lignes — signaux de
retrait), décisions `lint` §7 restantes (index_version, prose « gratuit »), éventuel
comparatif/fiches opencode (nécessiterait `research.comparatif` dans l'adapter).

## 2026-10-07 — P6 (suite) : cadence multi-plateformes

**Constat :** deux écarts au contrat §5/§6 découverts en relisant la cadence après P6 —
(a) `moteur/timer.sh` ne lançait que la plateforme par défaut : le timer quotidien
n'exécutait **jamais** opencode (la boucle « prouvée » P6 ne l'était qu'à la main) ;
(b) l'adapter opencode ne déclarait pas `research.rapport` : un diff opencode à
changements aurait écrit **le rapport de freebuff** (chemin unique, collision) — en
l'état : aucun rapport du tout pour opencode, donc « exit 2 → détails dans le rapport »
faux pour cette plateforme.

**Construit :**
- `timer.sh` : boucle sur `moteur/adapters/*.json` (aucune liste en dur — une plateforme
  ajoutée dans P7 est prise d'office ; garde fichier manquant) ; `fetch` échoué sur une
  plateforme = rc non nul mais les suivantes tournent quand même, l'unité échoue au
  total ; `diff` 0/2 reste « normal timer », autre rc = échec.
- opencode : `"research": {"rapport": "research/rapport-opencode.md"}` — chemin
  distinct, freebuff garde `research/rapport.md` (zéro churn sur sortie déjà publiée).

**Preuves :** `sh moteur/timer.sh quotidien` de bout en bout : freebuff (6 en cache
réutilisés, diff 0, `rapport.md`) **puis** opencode (2 réutilisés, diff 0,
`rapport-opencode.md` écrit, verdict/constat corrects), exit 0. Unités systemd
`enabled` (quotidien prochain 06:26, hebdo dimanche) — elles appellent `timer.sh`,
aucune réinstallation nécessaire. Régression : fb check/lint + oc lint exit 0.

**Honnêteté :** les timers n'ont encore **jamais** fired (LAST « - ») : la cadence est
installée et correcte au code près, mais pas encore observée en conditions réelles ;
le premier run réel est celui de demain 06:26. `install.sh` non touché (interface
`timer.sh quotidien|hebdo` inchangée).

**Reste inchangé :** pistes P7 (lanes catalogue, dépréciations, lint §7, comparatif).

## 2026-10-07 — Moteur d'investigation, P7 (recoupement catalogue + promotion)

**Contexte :** P6 a acté « 13 lane documentée dans l'état, 38 lignes 0.00 au catalogue =
signal, recoupement avant affirmation ». P7 = ce recoupement (choix utilisateur), puis
industrialisation de la veille sur ces signaux.

**Construit :**
- **Recoupement des 25 surplus** (mem-first : hit mémoire P5 `b080a388` = constat sans
  preuve → cache miss → 3 vérifications) :
  1. dataset brut `models.dev/api.json` (sha1 `49006e0b0b`) : les 38 ont `cost` **explicite**
     0/0 (446 `cost` omis existent ailleurs → le zéro affiché n'est pas le piège
     anomalyco/opencode#29971) ; mais même origine que le catalogue = **une** source, deux rendus ;
  2. endpoint opérateur `/zen/v1/models` (sha1 `147abc76c5ba`) : 86 servis = 12/13 lane
     (**`mimo-v2.5-free` absent** → dérive doc/API) + **1 seul surplus : muse-spark-1.2** ;
     8/9 payants absents = legacy → absence = « non servi ce jour », pas retrait ;
  3. descriptions dataset : 15/25 legacy, 10 live dont 9 non servis.
  - Corroboration tier 3 (non probante) : codeagentswarm (2026-08), zen.mdx historique +
    frank.dev = lanes passées tournantes (Kimi K2.5, MiniMax M2.5, Nemotron 3 Super…).
- **Décision (règle 3 observations)** : promotion ssi catalogue 0.00 **et** dataset cost
  explicite **et** servi v1 → **muse-spark-1.2-contributor-free promu** (14e modèle,
  evidence tier **2**, `promo: false` → rendu « 0 » vs « 0 promo » lane). 15 legacy +
  9 non servis restent **signaux hors état** ; mimo-v2.5 reste en état (contrat docs)
  avec flag « à vérifier ».
- **Moteur** : extracteurs `ex_zcatalog` (table prix, ids `slugify` — alignement vérifié
  13/13 sur l'état) et `ex_vserved` (JSON `/zen/v1/models`) ; helper `_row_cells` partagé
  avec `ex_zen` (DRY) ; adapter : `zen_catalog` passe `raw` → dédié + source
  `zen_served` ajoutée (tier 1) ; **3 gates coordonnées** :
  - lane : retrait seulement si le catalogue ne couvre plus le modèle (et silencieux si
    le catalogue est cassé) ;
  - catalogue : `RETRAIT prix` / `RETRAIT catalogue` structurels **sauf** si la lane
    documente encore le modèle → alors `CONFLIT`/`hors catalogue documenté` en « à vérifier »
    (deux sources qui se contredisent = recoupement, pas décision) ;
  - v1 : non servi → « à vérifier » (observation datée) ; `0.00 + servi` hors état →
    problème `PROMOTION` (manuel).

**Preuves :**
1. Extraction : 38 zero / 82 payants / 86 servis / 13 lane — identiques aux comptes P5.
2. `show` 14 modèles (« 0 » muse vs « 0 promo » lane) ; `lint` OK ; `apply` → provenance
   3 sources ; stable = **1 seul « à vérifier » debout** (mimo-v2.5 non servi), 0 structurel.
3. Négatifs : (N1) muse payant → `RETRAIT prix` **seul** (pas de double feu lane) ;
   (N2) deepseek devient servi + jev retiré → `PROMOTION` + 2 non-servis en à-vérifier ;
   (N3) format catalogue mangé → problème « 0 ligne », **aucune** masse-retrait
   (silence lane activé par `cat_broken`). Restauration octet-à-octet → état stable.
4. NO REGRESSION freebuff : diff/check/lint exit 0 (bug intercepté en route : deux bras
   `elif has_models` ajoutés « source absente » chez les adaptateurs **sans** ces sources —
   `stypes` vient de l'adapter, pas du manifeste ; corrigé en miroir du pattern
   `obs.get(...) is None` de P6, fb-diff repassé à 0).

**Honnêteté :**
- models.dev et models.opencode.ai = **une** source (org anomalyco), deux rendus ; le
  2e chiffre indépendant vient de l'endpoint opérateur — encore opérateur. La vérification
  100 % tier extérieure d'un tarif quelqu'un d'autre n'existe pas : la note le dit.
- « non servi ce jour » = observation datée d'un endpoint sans auth (peut filtrer) —
  d'où « à vérifier », jamais retrait automatique.
- Le catalogue legacy contient des lignes 0.00 de modèles hérités non servis : les
  compter comme « gratuits » aurait gonflé l'état de 15 fausses disponibilités.
- état stable en exit 2 (verify debout sur mimo-v2.5) : c'est le signal voulu, pas une
  régression ; les timers mappent 0|2 → exit 0.

**Reste :** P8 (pistes) : recouper mimo-v2.5 (dispo réelle ?) ; si l'endpoint filtre,
documenter sa sémantique exacte ; table dépréciation Zen ; lint §7 ; promotion future
d'un modèle sortant de legacy (la gate PROMOTION le signalera).

## 2026-10-07 — Moteur d'investigation, P8 (recoupement de la dérive mimo-v2.5-free)

**Contexte :** P7 a laissé un seul « à vérifier » permanent : `mimo-v2.5-free` documenté
par la doc Zen mais absent de `GET /zen/v1/models`. P8 = trancher quel côté dérive.

**Mémoire d'abord :** `search_memory` hybride (« mimo-v2.5-free non servi endpoint ») →
**cache miss** (seules des notes « test » au score ≤0.01) → web autorisé.

**Preuves (2026-10-07) :**
1. **Local** : endpoint servi (sha1 `147abc76c5ba`) = 86 ids, famille MiMo =
   `mimo-v2.6-flash-free` **seul** (aucun v2.5) ; dataset models.dev = entrée
   `mimo-v2.5-free` toujours présente (release 2026-04-24) ; snapshot docs du jour
   = 1 occurrence, ligne de lane « MiMo-V2.5 Free | mimo-v2.5-free ».
2. **Docs live** (`opencode.ai/docs/zen` + `opencode.ai/v2/docs/console/models`,
   fetch le jour même) : modèle **toujours documenté** dans la lane, avec la phrase de
   campagne « available on OpenCode for a limited time ».
3. **Issues** (tier 1 = dépôt opérateur) :
   - #45132 (ouverte) : 403 `{"model":" "}` sur `mimo-v2.5-free` **depuis ~mi-juillet**,
     puis d'autres free ; certains comptes reçoivent 429 FreeUsageLimitError →
     indisponibilité **sélective par clé** (dupes #43054, #38028, #40343) ;
   - #45291 (ouverte, 2026-08-26) : « MiMo 2.5 Free unavailable for several days »,
     `Forbidden {"model":"mimo-v2.5-free"}` ;
   - #45996/#45990 (2026-08-28) : mimo-v2.5 cassé côté routeur **Console Go**
     (`provider.only: tencent`) — endpoint distinct de zen/v1.
4. **Tier 3** : blog flabs.tech (2026-09-17) : `mimo-v2.5` retiré de la liste du routeur
   Go (« no MiMo at all ») alors que la doc Go l'annonce toujours (« trust the router ») ;
   dataset = release de `mimo-v2.6-flash-free` au **2026-09-22** (successeur servi).
5. Commit 5a5d981 (#29610) : ajout du modèle aux docs Zen (mai 2026) — point de départ.

**Verdict :** la dérive est **réelle et côté opérateur** — docs Zen périmés (au moins
depuis fin août) et liste `zen/v1` amputée de `mimo-v2.5-free` aujourd'hui ; le successeur
v2.6 est servi. **Reste dans l'état** (contrat docs tier 1) ; le verify permanent du diff
est la bonne représentation, aucun retrait automatique.

**Honnêteté :** retraite **définitive non prouvable** de l'extérieur — indisponibilité
historiquement sélective par clé (403/429), pas d'auth pour sonder `chat/completions` ;
la liste anonyme rend 12/13 lane donc n'est pas globalement filtrée, mais « absent de la
liste » ≠ « mort définitivement ». Le flag ne se lève que si l'opérateur bouge
(réapparition dans `/v1/models` ou retrait des docs).

**Aucun changement moteur/état** (KISS : le message « observation datée, à recouper
avant tout retrait » couvre déjà le cas). Mémoire `status:CONFIRME` écrite (write-back).

**Reste :** P9 (pistes) : table dépréciation Zen (gate « retired ⇒ plus de claim ») ;
lint §7 (`index_version`, prose) ; si réapparition de v2.5 dans `/v1/models`, lever le flag.

## 2026-10-07 — Moteur d'investigation, P9 (dépréciation Zen + lint §7)

**Contexte :** « Reste » P8 = table dépréciation Zen + lint §7 (`index_version`, prose
« retired »). Le flag mimo-v2.5 se lève tout seul si l'opérateur bouge — hors périmètre.

**Reconnaissance :** la page Zen du jour contient **déjà** une section
`<h3 id="deprecated-models">` : 18 lignes `Model | Deprecation date` (GPT 5.x Codex,
Claude Opus 4.1, Kimi K2.5, GLM 5/4.7/4.6, MiniMax M2.5/M2.1, Gemini 3 Pro, Qwen3
Coder 480B…). Croisements avec les états : **VIDE** (opencode 14 et freebuff 14) —
les nouvelles règles sont dormantes, zéro régression.

**Construit :**
- **`ex_zen` enrichie** (même page, même fetch, zéro source supplémentaire) : extraction
  de la section dépréciation en noms d'affichage → `zen_deprecated` ; résolution vers ids
  d'état dans `build_observation` (`zen_deprecated_ids`, non-apparié = normal, les
  dépréciés sont censés être hors état) ; helper `_row_cells` réutilisé (DRY).
- **Gate diff** (bloc `zen_docs`) : section vide/absente → **problème** « logique
  dépréciation suspendue » (extraction vide ⇒ problème, règle maison) ; déprécié ∩ état →
  **à vérifier** « relecture claim gratuit » (jamais de retrait auto) ; report
  `dépréciés docs : N dont M présent(s) dans l'état`.
- **Lint §7a** : déprécié (docs Zen du jour, cache du jour si présent) ∩ état → **warn**
  (exit 0). Pas d'analyse NLP de prose (l'ORCHESTRATOR notait le risque de faux
  positifs) : le signal est « état/fiche porte encore le claim d'un modèle que les docs
  déclarent déprécié » — exact, vérifiable, sans regex sur la prose.
- **Lint §7b** : si les fiches citent l'index AA (`rtificial Analysis`), `facts.index_version`
  est exigé — absent → **warn** ; présent sans `evidence.url`/`tier` → **erreur** (exit 1).
  Fait saisi dans `state/freebuff.json` : `v4.3.2` + evidence (URL page index, tier 1,
  `at` 2026-10-07T11:22:57Z) — **mem-first** (cache miss) puis web : page AA du jour =
  v4.3.2, re-baselining v4.3 du 2026-09-07, 10 évaluations (même version que les valeurs
  de `comparatif.md`/fiches).

**Preuves :**
1. Baseline : fb diff/check/lint = 0 (4 avertissements historiques inchangés), oc lint OK,
   oc diff = report `dépréciés docs : 18 dont 0` + seul verify mimo (exit 2).
2. **T1** (ligne « Big Pickle » injectée dans la table) : verify diff
   `modèle déprécié : big-pickle` + report `19 dont 1` + **warn lint** — les deux
   règles tirent ; restauration octet-à-octet.
3. **T2** (id de section masqué) : lane intacte (13) + **problème unique**
   « section « Deprecated models » introuvable » ; restauration OK.
   *(1er essai avorté : le script Python ouvrait `w` avant de lire → fichier tronqué ;
   restauration immédiate depuis orig, script réécrit en 2 temps — le test vide a d'abord
   prouvé la robustesse : lane 0 = problème, pas de crash.)*
4. **T3** (`facts.index_version` retiré) : warn lint apparaît (5 → exit 0), fait ré-ajouté
   avec la même evidence → retour à 4 avertissements.
5. Bug de route intercepté en route : la gate lisait `r["id"]` (jamais posé) au lieu de
   `obs["zen_deprecated_ids"]` — T1 diff ne tirait pas alors que le lint tirait ;
   corrigé, T1bis vert.

**Honnêteté :** croisement dépréciés∩état vide aujourd'hui → ces règles sont de la
vigilance, pas un signal actif (elles ne prouvent rien tant qu'elles ne tirent pas) ;
la table de dépréciation est une source **opencode** (docs Zen) — freebuff n'a pas
d'équivalent, la règle est donc déclarée par l'adapter, jamais globale ; l'analyse de
prose « gratuit » telle qu'envisagée §7 a été **remplacée** par un signal exact
(déprécié ∩ état) — l'NLP sur prose reste non implémenté (trop de faux positifs).

**Documents :** ORCHESTRATOR (état P1…P9, ligne lint §7, type `zen_docs`).
**Mémoire :** write-back décision P9 (mem-first fait pour `index_version`).

**Reste :** table dépréciation **freebuff** (source équivalente si elle existe) ;
analyse NLP prose si un jour utile ; fiche↔best-of (best-of toujours inexistant) ;
lever le flag mimo-v2.5 si réapparition dans `/v1/models`.

## 2026-10-07 — Moteur d'investigation, P10 (retrait RSS freebuff + lint §7 clos)

**Contexte :** « Reste » P9 = table dépréciation freebuff, NLP prose, fiche↔best-of.
Reconnaissance : freebuff n'a pas de table « dépréciés » mais son **RSS** (24 items,
tier 2) publie les cycles retrait/retour (« X withdrawn », « X replaces Y », « X returns ») ;
l'état modélise déjà `status: retired` + `retired_at` (space-bunny-alpha, 06/10) ;
le best-of n'existe pas et **n'est pas une sortie §6** ; la §7 « prose » est en réalité
« aucune ligne machine ne dit gratuit pour un retired ».

**Construit :**
- **Gate RSS** (freebuff, source déclarée `rss`) : `build_observation` transforme les
  titres du feed en événements `in`/`out` par modèle (withdrawn/replaced/replaces/returns/
  joins/added — nom avant le motif, apparié via `match_model` non-apparié=silencieux),
  garde le **dernier événement par date** ; gate : dernier événement `out` ∩ modèles
  `live` → **à vérifier** « retrait RSS non répercuté — tier 2, à recouper tier 1 »
  (jamais d'apply) + report `retraits RSS : N out, M encore live`.
- **Lint §7-3** (erreur, exit 1) : `status=retired` ⇒ le bloc `GEN:prix` de la fiche et
  la ligne `GEN:comparatif` du modèle ne doivent contenir aucun claim
  (`gratuit|disponible|\bfree\b|0 promo|\b0/h\b`). **Prose annotée hors GEN exclue** :
  la fiche space-bunny-alpha prouve les faux positifs sur données réelles (l.109
  « Space Bunny Alpha est gratuit… » sous bannière « VERDICT CADUC », l.67 claim barré
  `~~Gratuit.~~`) — l'NLP de prose reste non implémenté, documenté comme tel.
- **§7-1 best-of** : clos **N/A** (pas une sortie §6, aucun fichier) — pas de règle
  spéculative sur un artefact inexistant (YAGNI) ; **§7-4** = version globale unique
  `facts.index_version` (P9) ⇒ « deux mesures sans même version » structurellement
  impossible, documenté.

**Preuves :**
1. Baseline : feed tout-puissant sur l'historique réel — le ping-pong est géré :
   gemini-3-8-flash (retrait 03/09 **puis** « returns » 22/09 → dernier `in` → aligné),
   muse-1-3 (alternances 07→13→28/09 → dernier `in`), space-bunny (`out` 07/10 mais
   `retired` en état → pas de faux signal) ; **fb diff = 0** (zéro régression),
   report `1 out, 0 encore live`.
2. **T1** (retrait frais injecté « Solar Pro 4 withdrawn » 08/10) : 2 verifies
   (feed frais + `retrait RSS non répercuté : solar-pro-4`), report `2 out, 1 live` ;
   restauration octet-à-octet → retour 0.
3. **T2** (« gratuit » injecté dans le GEN:prix de la fiche retirée) : lint ÉCHEC exit 1,
   message localisé ; restauration OK.
4. **T3** (idem dans la ligne GEN:comparatif) : lint ÉCHEC exit 1 ; restauration OK.
5. Suite complète : fb diff/check/lint = 0 (4 avertissements historiques), oc diff = 2
   (verify mimo seul, inchangé), oc lint OK. `py_compile` + `sh -n timer.sh` OK.

**Honnêteté :** le gate tire sur le **tier 2 daté** face à l'état tier 1 courant — un
retour sans item « returns » resterait un verify debout (comme le flag mimo) ; les titres
RSS ne sont pas un format stable (parsing par motifs, non-apparié silencieux = modèles
jamais suivis sortent du périmètre, ex. Ox Alpha, MiniMax M3) ; la règle §7-3 ne couvre
que les lignes machine — les annotations humaines restent de la relecture humaine.

**Documents :** ORCHESTRATOR (état P10, §7 réécrit, ligne adapter freebuff).
**Mémoire :** write-back décision P10 (`97bf38f6-86a4-43c7-bc2a-165882f7bd99`).

**Reste :** si un jour le best-of devient une sortie §6, câbler la règle §7-1 (prix
fiche == comparatif == best-of) ; table dépréciation explicite freebuff si une source
apparaît (le RSS couvre le cycle de vie) ; lever le flag mimo-v2.5 si réapparition.
