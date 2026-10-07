# Comparatif — les 12 sur un index commun

Toutes les valeurs `AA` ci-dessous proviennent de l'**Artificial Analysis Intelligence Index v4.3.2**,
donc sur le même protocole. `n.d.` = non publié. `*` = version d'index antérieure, non comparable.

> 📦 **Catalogue (passe 8, I10 ; révisé passe 10).** Le tableau fait **14 lignes** : les
> **12 modèles réellement proposés par Freebuff au 2026-10-06** (`llms.txt` + `/plans` +
> `/live` + GitHub README, concordants) **et** Ling 3.1 Flash + Laguna S 2.1, conservés mais
> marqués **`hors cat.`** — **ils n'étaient pas des modèles Freebuff**.
>
> 📦 **2026-10-07 (passe 10) : le catalogue est passé à 11.** **Space Bunny Alpha a été
> retiré du picker le 2026-10-06** (GitHub `c3edf98738bd`, README + `FREEBUFF_PAUSED_FREE_MODEL_IDS`).
> `llms.txt` liste **11 modèles**, `/plans` a **11 lignes**, le changelog dit **« 11 live · 9
> retired · 20 all-time »**. Sur les 11, **8 seulement sont utilisables** sans abonnement en
> France : Muse Spark, Gemini 3.8 Flash et GPT-6.1 Sol sont `Paid plans` / `US only`.

## Le tableau

> ⚠ **Effort non apparié.** AA publie des scores par palier d'effort quand le modèle en
> propose plusieurs. Muse Spark est publié `max` **et** `xhigh`. MiMo-V2.6-Pro, GLM-5.3-Flash,
> Ling 3.1 Flash et MiMo-V2.6-Flash sont publiés **sans suffixe d'effort** dans les sources que
> j'ai lues : je ne sais pas quel effort AA a utilisé. Comparer « Muse Spark (max) » à
> « MiMo Pro (effort ?) » est un rapprochement **meilleur contre non-spécifié**, pas un ordre
> établi. Tout classement par intelligence ci-dessous est **indicatif**, pas une mesure.

<!-- GEN:comparatif|run=2026-10-07 -->
| Modèle | AA | TB 4.0 | HLE | GDPval | AA-LCR | Omis.prec | Omis.non-hall | $/tâche | tok/s | E2E s | Contexte | Freebuff |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Muse Spark 1.3 (max) | **48,1** | 33,3 | 48,7 | 59,2 | 83,0 | 43,6 | 67,1 | **1,60** | 140 | 37 | 1M | **🔒 payant** |
| MiMo-V2.6-Pro | 46,3 | **34,9** | **49,4** | **59,4** | **86,3** | 34,8 | 59,4 | 0,13 | **37** | 64 | 1M | 30/h |
| Solar Pro 4 † | 28 † | n.d. | n.d. | n.d. | 71 * | 19 * | 75,6 * | n.d. | 115 | n.d. | 524K | **0 promo ²** |
| GLM-5.3-Flash | 41,8 | 32,8 | 40 | 47,6 | 80 | n.d. | n.d. | 0,25 | 52 | 51 | 1M | 15/h ⁹ |
| Ling 3.1 Flash | 41,1 | 33,3 | 39,4 | 56,1 | 83,0 | 29,1 | 62,1 | **0,99** | **211** | n.d. | **262K** ¹ | **hors cat. ⁴** |
| DeepSeek-V4.1-Flash | 39,5 | 26,8 | 39,2 | 55,0 | 84,0 | **46,4** | **3,5** | 0,27 | **209** | **13** | 1M | 15/h |
| GPT-6 Luna (max) | 38,1 | 12,6 | 38,5 | 46,9 | 83,3 | 43,8 | 23,3 | **0,07** | 141 | 111 | 1M | 20/h |
| MiMo-V2.6-Flash | 37,9 | 22,7 | n.d. | n.d. | n.d. | n.d. | n.d. | 0,06 | 51 | 53 | 1M | 10/h |
| Laguna S 2.1 | **n.d.** | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | 1M | **hors cat. ⁴** |
| Solar Mini 4 | 24,1 | **1,0** | 25,8 | 28,6 | 83,3 | 18,4 | 64,2 | ~0,35 | 208 | n.d. | 524K | 5 FB/h ⁷ |
| Space Bunny Alpha | **n.d.** | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | 1M | 🪦 **retiré 06/10/2026** |
| DeepSeek V4.1 Flash Fast | **n.d.** | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | 5 j/h ⁵ |
| Gemini 3.8 Flash | **n.d.** | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | 1M | **🔒 payant** |
| GPT-6.1 Sol | **n.d.** | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | 1M | **🔒 FR = payant** |
<!-- /GEN -->

`E2E s` = end-to-end pour 500 tokens de sortie, temps de raisonnement inclus.
Laguna S 2.1 et Space Bunny Alpha n'ont **aucune page Artificial Analysis** (404) : non mesurés par le tiers.

- **`†` = estimé.** La page AA porte `28*` et la mention *« Estimate (independent evaluation
  forthcoming) »* ; toutes ses courbes de détail renvoient *« Not publicly available »*.
  **Solar Pro 4 est le seul des douze dont l'index soit une projection** — sous C2 il ne
  devrait pas figurer dans un classement.
- **`²` = tarif : conflit levé en passe 8.** Capture tier 3 : 0/h — **confirmé** par deux
  pages Freebuff primaires (README *« unmetered at full access »* + page `/plans` : **∞ Unlimited
  hrs Solar Pro 4**, badge *Promotional*). `mvalentsev` (10 FB/h) est contredit **et** ses
  allocations sont prouvablement périmées. **Reste le risque d'échéance** : voir ⁶.
- **`⁴` = hors catalogue Freebuff.** Aucune source primaire ne place Ling 3.1 Flash ni
  Laguna S 2.1 sur Freebuff ; `llms.txt`, `/plans`, `/live`, le GitHub README et le
  changelog s'accordent sur **les mêmes modèles, sans eux** (12 au 2026-10-06, **11 depuis le
  retrait de Space Bunny Alpha**). Ils vivent sur OpenRouter / Vercel AI Gateway. Leurs
  chiffres sont conservés, mais **ils ne sont pas des modèles Freebuff**.
- **`⁵` = existence prouvée** (elle était « non prouvée » en passe 1 : l'URL tierce retournait
  404, le modèle existe). `5 j/h` = page `/plans` (Starter). Prix par session non publié.
- ~~**`⁶` = le 0/h de Solar Pro 4 est promotional et peut expirer.** Badge `Promotional` sur
  `/plans`, et la promotion Upstage (−70 %) se termine le **09/10/2026**. Le gratuit de Solar
  Pro 4 n'est pas garanti au-delà. **À re-vérifier le 10/10.**~~
  ✅ **corrigé passe 10** : cette échéance concernait **l'offre API Upstage, pas le prix
  Freebuff**. Source primaire `common/src/constants/freebuff-solar-promo.ts` : le 0/h est
  *« A promotion with **no end date yet** »*, posé le **2026-10-05 07:15Z**, `Promotional` au
  badge. **Il peut se terminer par un commit, à tout moment — mais aucune date n'existe.**
  L'historique complet (9 bascules datées entre le 05/09 et le 05/10) est dans
  `research/solar-pro-4.md` § 7.
- **`⁷` = Solar Mini 4 : 5 FB/h depuis le 05/10, plus dans le gratuit `unlimited`.**
  Changelog : *« Solar Mini 4's free promotion ended on 2026-10-05 »* — passé de `unlimited`
  à `optimized`. ✏️ **corrigé passe 10** : la promo, c'était le **0/h (02/10 → 04/10)**, et
  **5/h est le prix courant depuis le lancement du 23/09** (source primaire `SOLAR_PRICE_CHANGES`).
  **Ce n'est pas un modèle `🔒`** : il reste accessible sans abonnement, il est *métré* —
  12 h/jour avec l'allocation française de 60 FB.
- **`⁸` = GPT-6.1 Sol : 100 Freebucks promotionnels** (2026-09-29) **— et gratuit aux US.**
  ✅ **précisé passe 10** (source primaire `freebuff-sol-promo.ts` + `freebuff-models.ts`) :
  le bandeau dit *« Free in the US, a paid plan elsewhere, until the promotion ends »* ; les
  **100 FB** sont le prix **promotionnel** le plus élevé jamais servi hors campagne Fable, et
  la **1 session/jour** est enforcée côté admission (`FREEBUFF_DAILY_SESSION_LIMITS`).
  En France : **payant, 1 session/jour**.
- **`⁹` = GLM 5.3 Flash : 15 FB/h depuis le 2026-10-06.** ✅ **corrigé passe 10** : le `10/h`
  de mon tableau venait de la **fenêtre promotionnelle 03/10 → 06/10** (commit GitHub
  `ce46ee14b2a4` : *« A promotional 10 ran 2026-10-03 to 2026-10-06; the price is 15 again »*).
  Le badge `Promotional` a été retiré le jour même.
- **`🔒` = accès payant uniquement** — GitHub README, colonne `Access` : Gemini 3.8 Flash =
  **`Paid plans`**, Muse Spark 1.3 = **`Paid plans`**, GPT-6.1 Sol = **`US, or paid plans
  elsewhere`** (→ en France : payant). Les trois **apparaissent dans le picker gratuit** de
  `llms.txt` mais **sans accès**. Tes 12 « modèles exposés » n'en comptent que 9 d'utilisables.
- Valeurs marquées `*` pour Solar proviennent de l'époque du lancement (v4.1.1) : elles ne sont
  pas dans le même index que le reste de la colonne.

> **Attention au recoupement.** Ces chiffres sont l'index **v4.3.2**. Le blog Z.ai et toute la
> presse chinoise citent encore **57 pour GLM-5.3-Flash**, obtenu sur la **v4.1.1** (26/08) —
> AA a re-baseliné son index le 07/09 (GLM passe 57 → 42, 0,09 $ → 0,25 $/tâche). Ce n'est ni
> une régression du modèle ni une erreur d'un des deux : ce sont deux versions. Recouper avec une
> source chinoise donnera l'impression que ce tableau est faux.
>
> **Solar Pro 4, l'inverse.** Le communiqué Upstage et l'article AA d'août citent **42** ;
> la page AA actuelle porte **28**. C'est *mon* chiffre qui était périmé. Mais le 28 est une
> **estimation** (`†`), pas une mesure.

## Ce que le tableau dit, et que la comparaison initiale ne disait pas

### 1. Muse Spark 1.3 est le mieux mesuré des douze — mais il n'est pas à toi, et l'ordre n'est pas établi

Sur le même index : Muse Spark 1.3 (max) **48,1** contre MiMo-V2.6-Pro **46,3**. La comparaison
initiale plaçait MiMo Pro en « raisonnement difficile » et Muse Spark en « code agentique », sans
jamais les comparer sur le même index. **`Access = Paid plans`** : sur ton compte gratuit, le
meilleur noté des douze est **inaccessible**.

**Ce que cela ne prouve pas** : MiMo Pro est publié sans suffixe d'effort dans mes sources. Si
AA l'a mesuré à un effort inférieur à `max`, l'écart est un artefact de configuration, pas de
capacité. J'avais conclu « l'ordre était faux » ; la formulation défendable est
**« non comparable jusqu'à appariement de l'effort »**.

Ce qui reste vrai à tous les niveaux d'effort : MiMo Pro est le meilleur **open-weight**
(le poids de Muse Spark n'est pas public). Et il mène TB 4.0 (34,9 %) devant Muse Spark
(33,3 %), là où son index global est plus bas. Les deux affirmations tiennent.

### 2. Muse Spark 1.3 est aussi le plus cher des douze, de 23x

1,60 $/tâche contre 0,07 $ pour GPT-6 Luna max. Et sur Freebuff son prix n'est **pas affiché**.
Le modèle le plus puissant est le seul dont le coût est caché — c'est le point sur lequel il
faut demander une donnée à la plateforme avant toute décision.

### 3. La vitesse est le vrai classement pour un outil de code

| | tok/s | 1er token de réponse | E2E |
|---|---:|---:|---:|
| DeepSeek V4.1 Flash | 209 | 10,6 s | 13 s |
| GLM 5.3 Flash | 52 | 41,4 s | 51 s |
| MiMo V2.6 Pro | 37 | 48,0 s | 64 s |

DeepSeek est **4,8x plus rapide** que MiMo Pro pour livrer une réponse. Sur une journée de
100 itérations de code, c'est 25 minutes perdues contre 5. AA le classe moins intelligent
(39,5 contre 46,3) mais c'est le seul des trois qui te fait attendre une fraction de seconde.

**Réserve ajoutée le 2026-10-06 (I9)** : ce rapport est **fournisseur/fournisseur, pas
modèle/modèle**. `trace.md:109` le note déjà — MiMo Pro fait 26 tok/s chez DeepInfra contre
310 chez PrimaLabs. Et AA mesure DeepSeek V4.1 Flash à **214,4 tok/s contre 214,9 pour le
V4 Flash qu'il remplace** : la supériorité de vitesse affichée au lancement (280-500 t/s
annoncés) **ne se reproduit pas en mesure indépendante**. L'écart que tu verras dépendra du
fournisseur derrière Freebuff, pas du modèle.

¹ Contexte : AA spécifie **1M** ; l'endpoint réel ne sert que **262 144 tokens pendant
l'essai gratuit**. C'est le chiffre qui compte pour toi aujourd'hui.

### 4. DeepSeek V4.1 Flash est le moins enclin à dire « je ne sais pas »

Précision AA-Omniscience **46,4 %** — la meilleure. Taux de non-hallucination **3,5 %** — le
plus bas de très loin. Muse Spark 1.3 : 67,1 %. Ling 3.1 Flash : 62,1 %. Solar Mini 4 : 64,2 %.

Le mécanisme est l'abstention, pas la justesse : Luna (43,8 % de précision, 23,3 % de
non-hallucination) et Muse Spark (43,6 %, 67,1 %) ont la même justesse et des
comportements opposés.

**Comparateur sur la même échelle.** AA publie pour AA-Omniscience un `Index` (−100..100) qui
pénalise l'hallucination **sans pénaliser le refus** : DeepSeek V4.1 Flash (max) = **−5**
(plus d'erreurs que de bonnes réponses), GLM 5.3 Flash = **+7**, Claude Fable 5.1 = +43.
Mes colonnes `Omni.prec` / `Omni.non-hall` sont bien *Accuracy* et *Non-Hallucination Rate*
(vérifié sur DeepSeek : 46 % / 4 %).

**Trois réserves qui m'interdisent d'en faire une conclusion forte :**
1. Je n'ai pas lu la méthodologie AA. Le mécanisme est inféré d'une phrase d'article, pas vérifié.
2. DeepSeek a un effort **continu** ; AA l'a mesuré à `max`. Un cadran continu poussé à fond
   peut lui-même supprimer l'abstention. **Le effet effort n'est pas contrôlé.**
3. Le dénominateur (tentatives autorisées ou non) est inconnu.

Ce qui est mesuré, c'est une **corrélation** entre « précision élevée » et « aveu d'ignorance
rare » sur deux modèles. Pas une causalité. Statut : **MATERIAL, pas critique.**

### 5. GPT-6 Luna est le champion du coût, et le plus faible en code agentique

0,07 $/tâche, AA-LCR 83,3 %, excellent sur documents longs. Mais **Terminal-Bench 4.0 = 12,6 %**,
et sa non-hallucination est à 23,3 %. Palier par palier, Luna se dégrade fort :
TB 4.0 = 0,0 % (low) → 2,5 % (medium) → 4,5 % (high) → 8,1 % (xhigh) → 12,6 % (max).
L'effort n'efface pas le déficit. Luna est un modèle de raisonnement et de lecture, pas un agent.

### 6. L'effort de raisonnement n'est pas monotone chez tous

| Modèle | palier bas | palier haut | écart |
|---|---:|---:|---:|
| Muse Spark 1.3 — TB 4.0 | 16,7 (xhigh) | 33,3 (max) | **×2** |
| Muse Spark 1.3 — index AA | 45,1 (xhigh) | 48,1 (max) | +3,0 |
| GPT-6 Luna — index AA | 21,5 (low) | 38,1 (max) | +16,6 |
| DeepSeek V4.1 — index AA | 25 (non-reasoning) | 39 (max) | +14 |
| GLM-5.3-Flash — précision | 92 % (`low`) | 100 % (défaut) | +8 pts |
| GLM-5.3-Flash — retrieval 128K | 75,3 % (`high`) | **71,6 %** (`max`) | **−3,7 pts** |

Chez Muse Spark, xhigh est **moins bon que max sur le code agentique**, alors qu'il est meilleur
sur l'index global. Le bon palier dépend de la tâche, pas du modèle.

**Le défaut est `max`.** Test apparié chinois (24 prompts) : si `reasoning_effort` est absent,
le modèle tourne en `max` (ratio médian défaut/explicite = **0,984**). Chaque appel non
configuré est donc le plus cher possible. Sur des questions courtes l'effort est **monotone**
(100 % / 98 % / 92 %), sur du retrieval long-contexte il **s'inverse** (`high` > `max`, et `max`
brûle 34 % de tokens de plus à 64K pour un score plus bas). Chez GLM, `enable_thinking: false`
*augmente* le coût de 11,1 % : le seul bouton qui compte est `reasoning_effort`.

> Statut I3 : **hypothèse devenue mesure.** Reste : le même test sur les autres modèles.

### 7. Le même modèle vaut 3x selon le harness

Muse Spark 1.3 sur Terminal-Bench 4.0 : **33,3 %** chez AA, **10,6 %** chez Vals AI.
Ling 3.1 Flash sur TB 4.0 : **33,3 %** chez AA, **40,4 %** en auto-déclaration Ant.
DeepSeek V4.1 Flash sur TB 4.0 : **26,8 %** chez AA, **31,2 %** en auto-déclaration.

Un score de benchmark sans son harness est un chiffre sans unité.

## Le français : UNKNOWN, avec des sources qui se contredisent

**Statut : INCONCLUANT.** Aucun score français n'a été trouvé pour aucun des douze modèles.
Ce n'est pas la même chose qu'une absence de score : voir l'espace de recherche ci-dessous.

### Deux limites de cette recherche
**Angle mort** : documentation en ja/ko/ar, articles de labo non indexés, et toute source
postérieure au 2026-10-05. Un négatif universal affirmé à partir de cet espace serait
infalsifiable — donc il n'est pas affirmatif.

### Ce que chaque source donne réellement
| Source | Tier | Ce qu'elle dit |
|---|---|---|
| Carte HF `XiaomiMiMo/MiMo-V2.6-Pro-RL` | primaire | `language: - en - zh` |
| Carte HF `zai-org/GLM-5.3` | primaire | `language: - en - zh` |
| Table de benchmarks Z.ai (z.ai/blog/glm-5.3) | primaire | **aucune ligne multilingue** |
| Doc Xiaomi `updates/model.md` | primaire | « Chinese, English, code-switching, Wu, Cantonese, Minnan, Sichuanese » — **section AUDIO** |
| shshi.cn (agrégateur tiers) | tier 3 | « 支持138种语言互译 » — **138 langues**, non corroboré |
| Global-MMLU (Cohere, 42 lang.) | tier 1 | évalue Llama/Qwen/Mistral/GPT-4o/Claude Sonnet 3.5 — **aucun des douze** |
| EU MMLU (CE, 16 lang. UE) | tier 1 | **aucun des douze** ; GLM-5.3 « non classé » ; leader Ministral 3 14B, 49,7 |
| MMLU French (2 leaderboards) | tier 2 | **1 modèle chacun**, aucun des douze |

### Trois corrections contre ma propre sur-interprétation
1. **`language:` est une étiquette de métadonnées d'entraînement, pas une déclaration de
   capacité.** Elle n'établit ni un défaut, ni un défaut de support. Contre-exemple de classe :
   Qwen est tagué `en, zh` et fonctionne en français.
2. **La citation Xiaomi vient d'une section audio** (transcription de paroles, parole dans le
   bruit). Je l'avais généralisée au modèle de langage. Erreur de portée.
3. **Les checkpoints lus ≠ ce que Freebuff sert.** J'ai lu `-RL` et base ; la plateforme sert
   une variante hébergée, possiblement post-entraînée.

### Et la contre-preuve que je n'avais pas trouvée
shshi.cn revendique **138 langues** pour GLM-5.3. C'est un tiers de rang 3, et le même site
se trompe ailleurs (il annonce Apache 2.0 alors que la licence réelle est `other`, et 80 t/s
sur A100, et un contexte 128K face au 1M réel). On ne le promeut donc pas non plus.
Mais son existence suffit à casser la formulation « ne revendique que en+zh ».

### Ce qui reste vrai
Aucun des deux modèles recommandés en premier par la comparaison initiale ne dispose d'une
preuve de couverture française, dans un sens ou dans l'autre. C'est **UNKNOWN**, pas un risque
établi. L'investigation I0 doit trancher par la mesure, pas par la métadonnée.

Sources : `research/trace.md` § Passe 3.

## Ton budget : 60/jour + 85 wallet = 145 Freebucks

> ⚠ **TOUTE CETTE SECTION EST CONDITIONNELLE ET NON OPPOSABLE.**
> La grille ci-dessous provient d'une capture d'écran reprise par une comparaison tierce —
> le même artefact dont j'ai démontré une source morte sur douze et **un modèle inexistant**
> (« DeepSeek V4.1 Flash Fast »). Un document qui se trompe sur ce qui est vérifiable n'est pas
> fiable sur ce qui ne l'est pas.
>
> **Tentative de corroboration, échouée.** Le ledger local
> `state.json.session-refunds.json` contient bien un champ `freebucks` par tentative :
> **20 entrées, toutes à 0, toutes `settled`, 3 threads, 20 attempts.** Le fichier s'appelle
> *refunds* — il journalise les remboursements, pas les débits. Il **ne peut ni confirmer ni
> infirmer** la grille. `costUsd` vaut 0 sur les 682 messages qui le portent, et la table
> `sponsored_runs` est vide (0 ligne, `threads.sponsored` non-null sur 0 thread sur 17).
> Conclusion : **aucune source de prix locale n'existe.** Voir investigation I6.
>
> **2026-10-06 (passe 7) — corroboration web, en conflit.** `freebuff.com/llms.txt` (primaire)
> ne publie **aucun tarif par modèle** ; il fixe l'allocation à **60 FB/jour en France** et
> énonce *« Freebucks buy one-hour model sessions »*. Le README GitHub dit que Solar Pro 4,
> GLM, DeepSeek, MiMo Flash et Solar Mini sont **« unmetered at full access »**. Un tiers dit
> **10 FB/h pour Solar Pro 4**. Trois sources, **aucune concluante** : la grille ci-dessous
> reste conditionnelle. Détail : `research/solar-pro-4.md` § 7.

> **2026-10-06 (passe 8) — conflit LEVÉ.** La page `freebuff.com/plans` (primaire) publie les
> heures par jour et par modèle : **`∞ Unlimited` pour Solar Pro 4 *et* Space Bunny Alpha**,
> badge `Promotional`. Cela **confirme le 0/h** et **contredit les 10 FB/h du tiers**, dont les
> allocations sont de toute façon prouvablement périmées. Les prix dérivés de `/plans`
> (Starter = 2,60 $/j) correspondent aussi à ma grille pour Solar Mini (0,05 $), GLM, MiMo Flash
> et DeepSeek (0,10 $), Luna (0,20 $) — sauf DeepSeek Flash Fast (0,52 $ vs mes 25/h).
> **Le prix gratuit par modèle reste non publié**, et il *bouge* : *« A model's Freebucks cost
> can vary »*. I2/I6 restent ouverts, mais sur un terrain plus étroit.

> **2026-10-07 (passe 10) — AVANCEMENT CONSIDÉRABLE sur I2/I6 : les prix datés sont publics.**
> Le dépôt GitHub public contient **`common/src/constants/freebuff-solar-promo.ts`**, qui
> **liste chaque bascule de prix avec son horodatage** (`SOLAR_PRICE_CHANGES`), et
> **`freebuff-sol-promo.ts`** / **`freebuff-glm-promo.ts`** (supprimé) qui donnent les prix
> exacts. Ce qui est **prouvé aujourd'hui** : Solar Pro 4 (9 bascules, 0/5/10 selon les
> dates), Solar Mini 4 (5 → 0 → 5), GLM (15 → promo 10 → 15), GPT-6.1 Sol (**100 promo**,
> gratuit aux US), MiMo 2.6 Pro (**30**), DeepSeek Flash Fast (**25, 50 en pointe semaine**).
> **Ce qui reste non publié** : la **carte complète** `prices[modelId]` côté serveur
> (`freebucksPricing()`, hors dépôt). La grille ci-dessous est donc **corrigée mais toujours
> conditionnelle**.

| Modèle | Freebucks/h | Heures sur 145 FB | Verdict budget *(conditionnel)* |
|---|---:|---:|---|
| Solar Pro 4 | **0** ✓ | non borné | index AA **estimé** ; gratuit mais **promotional, sans échéance** (open-ended depuis 05/10) ⁶ |
| Space Bunny Alpha | 🪦 | — | **retiré du catalogue le 06/10/2026** — plus de ligne budgétaire |
| Solar Mini 4 | 5 | 29 h | agentique quasi nul (TB 4.0 = 1 %) ; **5/h depuis le 05/10**, hors `unlimited` ⁷ |
| MiMo 2.6 Flash | 10 | 14 h 30 | AA 37,9 — le défaut partout |
| GLM 5.3 Flash | 15 | 9 h 40 | AA 41,8 — **15/h depuis le 06/10**, le 10/h était la promo ⁹ |
| DeepSeek V4.1 Flash | 15 | 9 h 40 | le plus rapide, hallucine 96,5 % du temps |
| GPT-6 Luna | 20 | 7 h 15 | le moins cher en $/tâche, faible en code |
| DeepSeek Flash Fast | 25 *(50 en pointe)* | 5 h 48 *(2 h 54 en pointe)* | **existence prouvée** (prix : `/plans` dit 5 j/h sur Starter) |
| MiMo 2.6 Pro | 30 | 4 h 50 | ~1 point sous Muse Spark, 5x plus lent |
| Muse Spark 1.3 | **🔒** | **inaccessible** | le mieux mesuré — **`Access = Paid plans`** |
| Gemini 3.8 Flash | **🔒** | **inaccessible** | `Paid plans` ; seul modèle acceptant audio/vidéo/PDF |
| GPT-6.1 Sol | **100 promo ⁸** | ~0,6 h si c'est 100/h | **US gratuit, ailleurs payant** → en France : payant. **1 session/jour enforcée** |
| Ling 3.1 Flash | *hors cat.* | — | **n'est pas un modèle Freebuff** — essai Vercel/Ant jusqu'au ~10-13 |
| Laguna S 2.1 | *hors cat.* | — | **n'est pas un modèle Freebuff** — OpenRouter |

Ces heures sont arithmétiques et **optimistes** : elles supposent un débit horaire linéaire,
ce que rien ne confirme. Le débit est probablement indexé sur les tokens.

### Solar Mini 4 : coût/tâche NON RÉCONCILIÉ
AA titre « ~5x le coût par tâche de GPT-6 Luna (max) malgré des prix par token similaires ».
Vérification arithmétique :
- Mini 4 = 88k tokens de sortie × $0,40/1M = **$0,0352**
- Luna max = 51k × $0,50/1M = **$0,0255**
- **ratio de sortie : 1,38x**, pas 5x.

Pour atteindre 5x au total, le volume d'entrée devrait différer d'environ 5x — **dont je n'ai
aucune donnée**. Le chiffre de ~$0,35 que j'avais advanced est mon aritmétique sur le « ~ »
d'AA, pas une mesure. Statut : **OPEN**, discrepancy non expliquée.

### Ce que le budget dit, sous condition
1. **Sur ton compte français gratuit, 8 modèles sont utilisables** — les **11** du catalogue
   moins Muse Spark, Gemini 3.8 Flash et GPT-6.1 Sol, **listés mais verrouillés** (payant / US),
   **et moins Space Bunny Alpha, retiré le 06/10** *(c'était 9 sur 12 au 2026-10-06)*.
   Le modèle le mieux noté du tableau (Muse Spark, 48,1) **n'est pas accessible** : c'est la
   conséquence la plus lourde du catalogue réel.
2. **Ling 3.1 Flash n'est pas un modèle Freebuff.** Son essai gratuit (Vercel jusqu'au
   2026-10-13, Ant ~10-16) est un **autre canal** — réel, mais hors de ce budget. Ne le mélange
   plus avec les Freebucks.
3. **Ne dépense pas en Muse Spark : tu ne le peux pas** sans abonnement (1,60 $/tâche chez Meta
   en sus).
4. **DeepSeek V4.1 Flash est le meilleur rapport vitesse/utilité pour le code**, si tu relis.
5. **Le seul 0/h restant est Solar Pro 4** — confirmé par `/plans` (`∞`), **promotional mais
   sans échéance** (open-ended depuis le 05/10, voir ⁶). ~~Space Bunny Alpha~~ : **retiré le
   06/10**, la ligne « banc d'essai gratuit » du `verdict.md` est caduque.
6. **Le prix gratuit par modèle reste non publié** et est déclaré variable. Le tri par prix
   ci-dessus reste **conditionnel** : I2 et I6 restent ouverts.

Sources : `research/trace.md`. Fiches détaillées : `research/fiches/`.
Solar Pro 4 : `research/solar-pro-4.md`.
