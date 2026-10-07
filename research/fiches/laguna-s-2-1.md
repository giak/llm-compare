# Laguna S 2.1 — Poolside
<!-- GEN:prix|run=2026-10-07 -->
**Sur Freebuff :** hors catalogue
<!-- /GEN -->

> ⚠ **HORS CATALOGUE FREEBUFF** (passe 8, investigation I10). Aucune source primaire du
> 2026-10-06 ne place ce modèle sur Freebuff — `llms.txt`, `/plans`, `/live` et le GitHub
> README s'accordent sur 12 modèles, sans lui. Le **0/h Freebuff que je lui attribuais était
> faux** : il est servi par **OpenRouter**, pas par Freebuff.

## Identité
2026-07-21. **118B total / 8B actifs**, MoE. **Open-weight** (OpenMDW-1.1, poids BF16 +
quantifications FP8, INT4, NVFP4, GGUF, MLX). 1M contexte. Texte uniquement.
Raisonnement : **off ou max** — pas de réglage fin de l'effort, la décision est documentée.
Trajectoires d'évaluation complètes publiées sur trajectories.poolside.ai.
Sur Freebuff : **absent du catalogue**.

## Puissance — ⚠ aucune mesure tierce
**Pas de page Artificial Analysis (404 vérifié).** Pas de score sur aucun index indépendant.
Tous les chiffres disponibles sont ceux de Poolside, dans son harnais.

| Benchmark | Laguna S 2.1 | Leader du même tableau |
|---|---:|---|
| Terminal-Bench 2.1 | 70,2 % | Kimi K3 88,3 · Claude Fable 5 88,0 |
| SWE-Bench Multilingual | **78,5 %** | Laguna S 2.1 **devant** Kimi absent, Tencent Hy3 75,8, Qwen 3.7 Max 78,3 |
| SWE-Bench Pro (dataset public) | 59,4 % | Claude Fable 5 80,3 · Muse Spark 1.1 61,5 |
| DeepSWE | 40,4 % | Kimi K3 69,0 · Claude Fable 5 70,0 |
| SWE Atlas (codebase QnA) | 46,2 % | Laguna S 2.1 leader du tableau |
| Toolathlon Verified | 49,7 % | Muse Spark 1.1 75,6 |

**11e sur 13 au Terminal-Bench 2.1** du leaderboard publié dans son propre billet. La
comparaison initiale citait « 70,2 % » sans ce contexte : le nombre est exact, la
conclusion « à tester prioritairement » ne l'impliquait pas.

Ce qu'il **mène réellement** : SWE-Bench Multilingual (78,5 %) et SWE Atlas codebase QnA (46,2 %).
Le premier est le seul benchmark du tableau qui parle de code non-anglais.

## Analyse de problèmes
Raisonnement : **max lève Terminal-Bench 2.1 de 60,4 % à 70,2 %** et DeepSWE de 16,5 % à 40,4 %.
L'effet de l'effort est massif ici, et il n'y a que deux positions : off ou max. Pas de point médian.

Entraîné en **moins de neuf semaines**, du début à la publication. Open-weight.

## Vitesse
**Non mesurée par aucun tiers.** 8B actifs laisse penser à une grande vitesse mais ce n'est
pas une mesure. À 0/h, cette absence est moins coûteuse.

## Coût
**Pas de coût Freebucks : n'est pas un modèle Freebuff** (servi par OpenRouter). Open-weight
donc déployable localement.

## Français
**Aucune donnée.** Mais c'est **le seul modèle du panel dont le meilleur score est sur un
benchmark multilingue** : SWE-Bench Multilingual à 78,5 %, avec une amélioration déclarée de
+5,4 % sur la génération précédente (57,7 % → 63,1 % pour XS.2). Ce n'est pas du français,
mais c'est la seule preuve du panel que le modèle ne restreint pas sa performance à l'anglais.
Poolside est français : c'est le seul des douze laboratoire français, et la publication
mentionne « improving multilingual coding results » comme argument de release.

Statut : **le seul modèle du panel avec un indice de présomption favorable en français. Non mesuré.**

## Avantages
- **0/h et open-weight.** Le seul des douze que tu peux faire tourner chez toi, hors ligne,
  sur du code que tu ne veux pas envoyer.
- 118B-A8B : tourne sur une machine de bureau, pas sur un cluster.
- **SWE-Bench Multilingual 78,5 %, meilleur du tableau.** Sur du code non-anglais.
- **SWE Atlas codebase QnA 46,2 % : le meilleur score sur la compréhension de gros dépôts
  de tous les modèles comparés dans ce tableau.** Directement pertinent pour ton usage.
- 1M contexte, en thinking et en no-thinking.
- **Trajectoires complètes publiées.** Rare. C'est la seule source du panel où tu peux
  auditer les réponses et les trajectories d'évaluation au lieu de croire sur parole.
- Latence en frontal : le benchmark qu'il mène est justement la compréhension d'un dépôt.

## Inconvénients
- **Aucune mesure tierce.** Pas d'AA, pas de classement indépendant. Tu ne sais pas où il
  se place réellement dans le panel.
- 11e au Terminal-Bench 2.1. Ni le meilleur, ni proche.
- DeepSWE à 40,4 % contre 69-70 % pour Kimi K3 et Claude Fable 5 : il fixe moins de tâches
  longues que le front de liste.
- SWE-Bench Pro à 59,4 % contre 80,3 % pour Claude Fable 5.
- Pas de contrôle fin de l'effort (off ou max), donc pas de réglage qualité/coût.
- Texte uniquement.
- Score en baisse apparente sur TB 2.1 vs TB 4.0 pour les autres modèles : 70,2 % sur 2.1
  ne dit rien sur sa position en 4.0. Personne ne l'a mesuré dessus.
- Nécessite une machine capable d'héberger 118B en quantification.

## Verdict pour ton budget

> ⚠ **CONDITIONNEL.** Le verdict ci-dessous dépend de la grille Freebucks/h, qui provient
> d'une capture d'écran et n'est corroborée par aucune source. Le ledger local
> (`state.json.session-refunds.json`, 20 entrées) journalise des *remboursements* à 0 et ne
> peut ni confirmer ni infirmer la grille. Voir `comparatif.md` § Budget.
**Le seul modèle que tu possèdes vraiment.** À 0/h et open-weight, c'est le seul des douze
qui ne peut pas te facturer ni te couper l'accès, et le seul que tu peux faire tourner
localement sur du code confidentiel.

Il n'est pas le meilleur agentique du panel et il le sait : son propre tableau le classe
11e. Son intérêt est ailleurs : SWE Atlas codebase QnA (meilleur du tableau), du multilingue
correct, des poids auditables, et des trajectoires publiées.

Priorité d'usage : comprendre un dépôt, explorer un code que tu ne veux pas envoyer, garder
la maîtrise de l'execution. Pas : la production de code de masse.

C'est aussi le seul modèle du panel dont l'absence de mesure tierce est le moins grave,
puisqu'il est à 0/h et que tu peux l'évaluer toi-même.

## Sources
- https://poolside.ai/blog/introducing-laguna-s-2-1
- https://docs.poolside.ai/release-notes/models
- https://huggingface.co/poolside/Laguna-S-2.1
- https://trajectories.poolside.ai
