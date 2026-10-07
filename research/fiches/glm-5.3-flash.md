# GLM-5.3-Flash — Z.ai
<!-- GEN:prix|run=2026-10-07 -->
**Sur Freebuff :** 15/h
<!-- /GEN -->

## Identité
2026-08-26. **320B total / 18B actifs**. Open-weight. 1M contexte (1 048 576).
45 couches : 34 KDA (attention linéaire) intercalées avec 11 DSA (sparse), ratio 3:1.
288 experts routés top-8, +1 expert partagé. Manifold-Constrained Hyper-Connections.
FP8 natif. **Nativement multimodal** : texte, image, jusqu'à 8 images par requête.
Raisonnement : `low` / `high` / `max`, **défaut max**.
Prix API : 0,15 $ in / 0,50 $ out / 0,026 $ cache. Blended 0,098 $.
Sur Freebuff : **15/h depuis le 2026-10-06** (promo **10/h du 03/10 au 06/10**, badge
`Promotional` retiré). Mon « 10/h » datait de la fenêtre promotionnelle.

## Puissance — AA Intelligence Index v4.3.2
**41,8.** Sous-scores : AA-Briefcase 1454 · GDPval-AA 1647 Elo · AutomationBench 60 % ·
**TB 4.0 32,8 %** · SciCode 52 % · HLE 40 % · GDP.pdf 15 % · CritPt 15 % ·
AA-Omniscience 7 (composite) · AA-LCR 80 %.

À distinguer de son frère **GLM-5.3 (non-Flash)**, index 44,8 et TB 4.0 = 41,9 %.
GLM-5.3 n'est pas exposé par Freebuff. Flash perd ~8,6 points d'index et ~9 points de TB 4.0.

## Analyse de problèmes
TB 4.0 à 32,8 % le place 3e des douze derrière MiMo Pro (34,9 %) et à égalité avec Ling
et Muse Spark (33,3 %). HLE 40 % et CritPt 15 % sont en dessous de MiMo Pro. C'est un bon
exécuteur d'outils et de terminal, pas un raisonneur de fond.

Sécurité offensive : le GLM-5.3 (non-Flash) atteint 84,5 % sur CyberGym et 54,4 % sur
ExploitBench. Rien n'est publié pour Flash sur ces deux benchmarks.

**Réserve de protocole** : Z.ai juge son HLE avec **GPT-5.6 Luna (medium)**, c'est-à-dire un
modèle d'un concurrent direct, comme juge. Déclaré dans la documentation, donc honnête, mais
ça déplace le score.

## Vitesse
**52 tok/s**, TTFT 3,25 s, **1er token de réponse 41,4 s**, E2E 51 s, 982 s par tâche.
69k tokens de sortie par tâche dont 47k de raisonnement.

## Coût
0,25 $/tâche — 4e moins cher. Coût total de l'index 280 $. Prix blended le plus bas des
douze (0,098 $/1M), grâce à la remise cache de 83 %.

## Français
**Drapeau rouge, le plus explicite des douze.** La carte officielle `zai-org/GLM-5.3` déclare
`language: - en - zh`. Aucune autre langue n'est revendiquée, et GLM-5.3 est **explicitement
« non classé »** sur EU MMLU, le seul benchmark récent avec du français traduit par des humains.

Un modèle qui déclare deux langues et qui n'est pas classé sur le benchmark multilingue
européen : sur un projet francophone, c'est le premier risque du panel après MiMo.

## Avantages
- 1M contexte avec la fenêtre de coût long-contexte la plus basse : attention hybride KDA+DSA,
  −3,01x de calcul d'attention et −4,44x de cache KV contre GLM-5.3.
- Le meilleur prix blended des douze (0,098 $/1M) : le moins cher quand le contexte se répète.
- 8 images par requête, entrée vidéo, vision native.
- 18B actifs seulement : déployable sur une machine modeste, contrairement à MiMo Pro (1T).
- TB 4.0 à 32,8 % : réellement utilisable en agent terminal.
- Open-weight.

## Inconvénients
- **Ni le français ni aucune autre langue hors en/zh déclarés.**
- Défaut d'effort à `max` : tu paies le palier le plus cher sans l'avoir choisi. AA mesure
  GLM 5.3 max à 41,9 % sur TB 4.0 contre 34,9 % à `low` : l'écart est réel et facturé d'office.
- Non-hallucination non publiée pour Flash (indice composite Omniscience 7, contre 14 pour
  GLM 5.3 et −5 pour DeepSeek). Zone grise sur la fiabilité.
- 41 s avant le premier mot : agreements avec DeepSeek (10,6 s) sur un modèle moins bon.
- Flash perd 8,6 points d'index contre GLM-5.3 : si le prix Flash n'était pas 4x moindre,
  le choix serait discutable.

## Verdict pour ton budget

> ⚠ **CONDITIONNEL.** Le verdict ci-dessous dépend de la grille Freebucks/h, qui provient
> d'une capture d'écran et n'est corroborée par aucune source. Le ledger local
> (`state.json.session-refunds.json`, 20 entrées) journalise des *remboursements* à 0 et ne
> peut ni confirmer ni infirmer la grille. Voir `comparatif.md` § Budget.
**15/h est correct mais plus « aubaine »** : sur 145 FB, ~9 h 40 de budget pour le 4e
modèle en intelligence (c'était 14 h 30 à 10/h, prix promo). **Mais ne l'adopte pas sans
avoir mesuré son français** : c'est le candidat le plus probable à te décevoir en production
francophone, et il est aussi le seul que la comparaison initiale recommandait en premier
choix.

## Sources
- GitHub `CodebuffAI/freebuff` commit **`ce46ee14b2a4`** — **primaire, 2026-10-06 20:06 UTC** :
  suppression de `freebuff-glm-promo.ts`, commentaire *« A promotional 10 ran 2026-10-03 to
  2026-10-06; the price is 15 again and carries no label »*
- `freebuff.com/llms.txt` + `freebuff.com/plans` — **primaire, relus 2026-10-07**
- https://docs.z.ai/guides/vlm/glm-5.3-flash
- https://docs.z.ai/guides/llm/glm-5.3.md
- https://huggingface.co/zai-org/GLM-5.3-Flash
- https://build.nvidia.com/z-ai/glm-5-3-flash/modelcard
- https://artificialanalysis.ai/models/comparisons/deepseek-v4-1-flash-vs-glm-5-3-flash
- https://translation.ec.europa.eu/news-and-events/news/towards-fair-multilingual-ai-eu-mmlu-new-eu-benchmark-llms-2026-07-22_en
