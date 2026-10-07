# Verdict

Base : **11 modèles** exposés par Freebuff depuis le retrait de Space Bunny Alpha (2026-10-06 ;
12 au 2026-10-05). Fiches dans `fiches/`, tableau commun dans `comparatif.md`,
journal et auto-revue dans `trace.md`.

## 1. La conclusion robuste : il n'y a pas de gagnant unique

Ce qui est établi, c'est une **règle de routage**, pas un classement. Les scores ci-dessous
sont tous sur l'AA Intelligence Index v4.3.2, donc directement comparables.

| Besoin | Premier choix | Pourquoi (fait vérifié) |
|---|---|---|
| Intelligence mesurée | **Muse Spark 1.3** | AA 48,1, le plus élevé publié — *effort non apparié, voir 1b* |
| Intelligence open-weight | **MiMo-V2.6-Pro** | AA 46,3, champion HLE / CritPt / **TB 4.0 34,9 %** / AA-LCR |
| Coût par tâche réel | **MiMo-V2.6-Flash** | 0,06 $/tâche, cache hit à 99 % de remise |
| Long contexte, pas de code | **Ling 3.1 Flash** | AA 41,1, AA-LCR 83,0 %, non-hallucination 62,1 % — ⏰ gratuit sous condition, fenêtre fermée le 2026-10-13 |
| Code agentique | **MiMo-V2.6-Pro** (34,9 %) puis Muse Spark / Ling (33,3 %) | TB 4.0, même version |
| **Vitesse** | **DeepSeek-V4.1-Flash** | 209 tok/s, 13 s E2E — 5x plus rapide que MiMo Pro |
| Lecture de documents | **Ling 3.1 Flash** | 83,0 % AA-LCR |
| Possession / local | **Laguna S 2.1** | 0/h, open-weight, seul modèle hébergeable chez toi |
| Banc d'essai gratuit | ~~**Space Bunny Alpha**~~ | 🪦 **retiré du catalogue le 06/10/2026** — remplacé par **Solar Pro 4** (0/h, promotional open-ended), sinon MiMo 2.6 Flash à 10 FB/h pour la mesure répétée |

Le reste est un arbitrage, pas une hiérarchie.

## 1b. Les corrections majors de la deuxième passe

Sur index commun, trois affirmations de la §1 initiale tombent — sous réserve d'appariement
d'effort (voir l'avertissement en tête de `comparatif.md`) :

1. **Muse Spark 1.3 (48,1) est mieux mesuré que MiMo-V2.6-Pro (46,3)** sur le même index.
   Le classement initial plaçait MiMo Pro en « raisonnement difficile » sans le comparer à
   Muse Spark. **Mais MiMo Pro est publié sans suffixe d'effort** : si AA l'a mesuré sous
   `max`, l'écart est un artefact de configuration. Formulation défendable :
   *non comparable jusqu'à appariement*, pas *ordre établi*.
   Ce qui tient à tous les efforts : MiMo Pro est le meilleur open-weight, et il mène
   TB 4.0 (34,9 %) devant Muse Spark (33,3 %).
2. **Muse Spark 1.3 est aussi le plus cher : 1,60 $/tâche, 23x Luna max.** Et sur Freebuff
   son prix **n'est pas affiché**. Le modèle le mieux mesuré est le seul dont le coût est caché.
3. **GPT-6 Luna n'est pas le champion du coût sur Freebuff.** 20/h pour le moins cher des
   douze en coût réel (0,07 $/tâche), pendant que DeepSeek est à 15/h, 1,6x plus
   intelligent et 8x plus rapide. Le débit plateforme ne reflète pas l'efficience.

Et un fait mesuré, avec sa limite :

4. **DeepSeek-V4.1-Flash a un taux de non-hallucination de 3,5 %** — le plus bas des douze.
   Meilleure précision AA-Omniscience (46,4 %), et il n'a presque jamais l'air d'hésiter.
   **Réserve** : je n'ai pas lu la méthodologie AA, et l'effort `max` sur son cadran continu
   n'est pas contrôlé. Corrélation mesurée, causalité non établie. Statut MATERIAL.

## 1c. Le français : UNKNOWN, pas un risque établi

**Aucun score français trouvé pour aucun des douze modèles** — dans un espace de recherche
borné (EN + ZH, sources tier 1 à 3, jusqu'au 2026-10-05). Ce n'est pas un négatif universal.

Deux cartes de modèle officielles déclarent `language: - en - zh` :

| Modèle | Déclaration officielle |
|---|---|
| MiMo-V2.6-Pro-RL | `en`, `zh` |
| GLM-5.3 | `en`, `zh` |

**Trois corrections contre ma propre sur-interprétation :**
- `language:` est une étiquette de métadonnées d'entraînement, **pas une déclaration de
  capacité**. Contre-exemple de classe : Qwen est tagué `en, zh` et fonctionne en français.
- La citation Xiaomi « Bilingual & Dialects » vient d'une **section audio** du même document.
  Je l'avais généralisée au modèle de langage. Erreur de portée.
- J'ai lu les checkpoints publiés (`-RL`, base), pas la variante hébergée que Freebuff sert.

**Et la contre-preuve que je n'avais pas trouvée** : un agrégateur tiers (shshi.cn) revendique
« 138 langues » pour GLM-5.3. Tier 3, et le même site se trompe ailleurs (licence annoncée
Apache 2.0 au lieu de `other`, 80 t/s sur A100, contexte 128K au lieu de 1M). On ne le promeut
pas non plus — mais son existence casse la formulation « ne revendique que en+zh ».

**Résultat net : UNKNOWN.** Les deux modèles recommandés en premier par la comparaison
initiale sont ceux pour lesquels le doute est le plus fort, mais un doute n'est pas un risque
démontré. I0 tranche par la mesure.


L'instrument existe et personne ne l'a passé sur eux. C'est l'investigation la plus rentable
du dossier (`investigations.md`, I0).

## 2. Les quatre corrections qui changent des décisions

### 2.1 « DeepSeek V4.1 Flash Fast » n'a aucune source

L'URL citée par la comparaison Perplexity (`pi.dev/models/basaten/deepseek-ai-deepseek-v4-1-flash-fast`)
répond **404**. Aucun document DeepSeek ne mentionne un endpoint « Flash Fast ».

Ce qui existe, et qui est plus important : DeepSeek a **retiré** `deepseek-v4-flash`,
qui route désormais silencieusement vers V4.1-Flash. Confirmé sur la base locale :
le thread `deepseek/deepseek-v4-flash` utilise donc V4.1-Flash sans le dire.

Conséquence : si Freebuff facture « Flash » 15/h et « Flash Fast » 25/h, l'écart de prix
ne correspond à aucun produit DeepSeek documenté. C'est une étiquette de plateforme.
**À mesurer, pas à supposer.**

### 2.2 Le prix Freebucks/h est anti-corrélé au coût réel sur un cas

| Modèle | Freebuff | Coût/tâche (AA) |
|---|---|---|
| Solar Mini 4 | 5/h — le moins cher | **~0,35 $ (~5x Luna max)** |
| GPT-6 Luna (max) | 20/h | 0,07 $ |

Solar Mini 4 est le modèle le moins cher de la plateforme et l'un des plus chers
par tâche, parce qu'il brûle 88k tokens de sortie par tâche. Le tri par Freebucks/h
inverse l'ordre réel sur ce couple. **Le bon curseur est le coût par tâche.**

### 2.3 Les scores ne sont pas sur la même version de benchmark

Terminal-Bench **2.1** (Poolside, juillet) et Terminal-Bench **4.0** (index AA courant v4.3.2)
sont deux benchmarks différents. Le 70,2 % de Laguna S 2.1 est sur 2.1. Le 57 % de Solar Pro 4
est sur 2.1. Le 1 % de Solar Mini 4 est sur 4.0.

Mélanger ces chiffres dans un tableau produit un classement qui n'a pas de sens.
AA publie aussi plusieurs versions de son index (les 42 de Solar Pro 4 sont d'août,
les 46 de MiMo et les 38 de Luna sont de septembre) : **seuls les scores portant la même
version d'index sont comparables.**

### 2.4 Solar Pro 4 : le progrès vient Mostly de l'abstention

AA : AA-Omniscience passe de -53 à -1, mais la **précision reste à 19 %**. Le modèle
n'essaie que 41 % des questions contre 92 % avant. Le taux d'hallucination tombe de 88 % à 24 %
parce qu'il se tait. Il est aussi plus lent : 8,6 min/tâche contre 6,0.

« Choix spécialisé pour documents et outils » est donc à double tranchant :
il va mieux sur les tâches agentiques (GDPval-AA Elo 1277, au-dessus de la base humaine de 1000)
et il échoue davantage en s'abstenant.

## 3. Le tableau de la comparaison initiale, corrigé

| Modèle | Affirmation initiale | Verdict |
|---|---|---|
| MiMo 2.6 Pro | meilleur pour le raisonnement difficile | Vrai mais relatif : AA 46 = meilleur **open-source**, pas leader absolu. Il existe une 3e variante non citée, `mimo-v2.6-pro-ultraspeed` (20x). |
| GLM 5.3 Flash | multimodal, 320B/18B, ~1M | Confirmé. Précision manquante : 1er GLM-5 natif multimodal, `reasoning_effort` low/high/max **défaut max**. Z.ai a jugé son HLE avec GPT-5.6 Luna (medium) — biais fournisseur à noter. |
| DeepSeek V4.1 Flash | multimodal, 1M, raisonnement | Confirmé + 552B backbone / 196B Engram, 8B prefill / 16B decode, effort **continu** (pas 6 paliers). |
| DeepSeek Flash Fast | endpoint distinct | **404, sans source.** Retiré. |
| Muse Spark 1.3 | code/agents, résultats forts | Confirmé (Meta, 2026-09-02). La méthodo de Meta dit eux-mêmes prendre « la valeur comparable la plus haute » entre leur eval, le leaderboard et l'auto-déclaration du fournisseur — sélection optimiste assumée. |
| GPT-6 Luna | « plusieurs niveaux d'effort », AA 22-38 | Confirmé mais **sous-compté** : 6 paliers dont `none` = 18. Fourchette réelle **18 → 38**. |
| Solar Pro 4 | docs/outils, AA 42 | Confirmé + le progrès vient de l'abstention (§2.4). |
| Solar Mini 4 | ~3B actifs, AA 24 | Confirmé (35B total / 3B actifs, AA 24,1). Mais **pire** en agentique : TB 4.0 = 1 %. |
| Ling 3.1 Flash | 560B/25B, 262K contexte | Confirmé. Conséquence non tirée : c'est le **plus petit contexte des 12** (262K contre 1M partout ailleurs). |
| Laguna S 2.1 | 70,2 % TB 2.1, à tester | Confirmé, mais 70,2 % = **11e place** sur le leaderboard du même billet (Kimi K3 88,3 / Claude Fable 5 88,0). Intéressant par la taille, pas par le score. Pas de contrôle d'effort (off/max). |
| Space Bunny Alpha | anonyme, résultats contradictoires | Confirmé : preview anonyme, `stealth/space-bunny-alpha` (OpenRouter), `space-bunny-free` (OpenCode). 1M contexte, 524K sortie, texte/image/vidéo → texte. Aucun benchmark indépendant. **→ Retiré de Freebuff le 06/10/2026** (voir encadré de la fiche). |

## 4. Ce qu'aucune recherche web ne peut trancher

Le classement defended des 12 sur *ton* usage. Les variables que personne ne publie :

- le routage réel de Freebuff (quel's modèle sert vraiment une requête, à quel effort)
- la latence vue par toi, qui n'est pas celle d'AA
- les quotas journaliers, donc « 0/h » n'est pas « illimité »
- le comportement en session longue avec compaction : personne ne bench ça

Ces quatre points sont l'objet de `investigations.md`.
