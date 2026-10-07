# Solar Pro 4 — Upstage
<!-- GEN:prix|run=2026-10-07 -->
**Sur Freebuff :** 0/h (promo sans échéance connue)
<!-- /GEN -->

## Identité
2026-08-11. Propriétaire, paramètres non publiés. Contexte non publié.
Texte uniquement. Raisonnement natif. Prix API : 0,30 $ in / 1,20 $ out / 0,06 $ cache.
Sur Freebuff : **0/h — confirmé** par `/plans` (`∞ Unlimited`) et le README (*unmetered*),
**mais badge `Promotional`** : entré en gratuit le **2026-10-05**, promotion **« open-ended »,
sans date de fin** (GitHub, primaire). `mvalentsev` (10 FB/h) est contredit et ses allocations
sont périmées.
**Correction (passe 10, 2026-10-07) :** mon « échéance 2026-10-09 » **n'était pas celle de ce
prix** — c'était la fin d'une promo −70 % *Upstage* sur l'API. Le prix Freebuff 0/h est un
choix produit **sans échéance publiée**.

## Puissance
**AA Intelligence Index 42 — mais mesuré le 12/08/2026, sur une version antérieure de l'index.**
Pas de mesure sur v4.3.2. Seul modèle du panel où le score n'est pas aligné sur l'index commun :
**les 42 ne sont pas directement comparables aux 41,8 de GLM Flash ni aux 46,3 de MiMo Pro.**

Sous-scores publiés (août 2026) : **Terminal-Bench 2.1 = 57 %** (Solar Pro 3 : 12 %) ·
**AA-LCR = 71 %** (Solar Pro 3 : 31 %) · **τ³-Banking = 23 %** (9 %) ·
**GDPval-AA v2 Elo 1277**, au-dessus de la base humaine de 1000, devant Qwen3.7 Max (1272)
et MiMo-V2.5-Pro (1266) · AA-Omniscience composite −1 (Solar Pro 3 : −53).

## Analyse de problèmes — la nuance qui compte
Le bond d'AA-Omniscience de −53 à **−1** **ne vient pas de plus de connaissances** :
la précision reste à **19 %**, exactement celle de Solar Pro 3. Ce qui change :
il n'essaie que **41 %** des questions au lieu de 92 %, et son taux d'hallucination tombe
de 88 % à 24 %. **Il a appris à se taire.**

En contrepartie il est plus lent : 8,6 min par tâche contre 6,0 pour la génération précédente,
alors qu'il utilise moins de tokens. 43k tokens de sortie par tâche.

## Vitesse
Non publiée dans les sources consultées. Latence en hausse par rapport à Solar Pro 3.

## Coût
0,30/1,20 $ par 1M, cache à 0,06 $ (80 % de remise). **0/h sur Freebuff — confirmé en passe 8
par `/plans` (`∞ Unlimited`)**, badge `Promotional` : promotion **open-ended depuis le
05/10/2026** (pas d'échéance ; voir encadré en § Identité).

## Français
**Aucune donnée.** Upstage est un labo coréen : le modèle est positionné sur le coréen,
le japonais et l'anglais. Solut de français non mesurable a priori. Statut : **probablement
le plus faible des douze en français**, mais non mesuré.

## Avantages
- **0/h** : gratuit, ou le second meilleur rapport du panel avec Ling.
- GDPval-AA Elo 1277, au-dessus de la base humaine : réel sur le travail de connaissance.
- AA-LCR 71 % et τ³-Banking 23 % : le point fort revendiqué, documents et outils, tient.
- Terminal-Bench 2.1 à 57 % : agent terminal correct.
- Hallucination de 88 % à 24 % : le gain le plus net du panel sur ce critère.
- Moins bavard que la génération précédente (43k contre 52k tokens de sortie).

## Inconvénients
- **Score non aligné sur l'index commun.** On ne peut pas le classer contre les onze autres.
- **Précision knowledge stagnante à 19 %.** Sur les faits, il ne sait pas plus que la 3.
- Progression par l'abstention : si tu as besoin d'une réponse, il peut ne pas en donner.
  Sur 41 % de tentative seulement, c'est un problème opérationnel réel.
- **Plus lent** que la génération précédente malgré moins de tokens.
- Texte uniquement : pas d'image, pas de vidéo, pas d'audio.
- Contexte non publié : impossible de savoir s'il tient un gros dépôt.
- Upstage publie un communiqué de presse (PRNewswire) qui cite ses propres chiffres sur
  l'index AA comme si c'était une validation indépendante. AA a bien mesuré 42, mais le
  cadrage du communiqué est promotionnel.

## Verdict pour ton budget

> ⚠ **CONDITIONNEL.** Le verdict ci-dessous dépend de la grille Freebucks/h, qui provient
> d'une capture d'écran et n'est corroborée par aucune source. Le ledger local
> (`state.json.session-refunds.json`, 20 entrées) journalise des *remboursements* à 0 et ne
> peut ni confirmer ni infirmer la grille. Voir `comparatif.md` § Budget.
**À tester en premier parmi les 0/h, mais pour un usage précis : lire des documents, poser
des questions, chercher une info. Ne pas l'utiliser comme cerveau du projet.** Ses 41 % de
tentatives signifient que sur deux questions tu n'auras rien, et sa précision de 19 % signifie
que la réponse obtenue peut être fausse.

C'est le meilleur candidat du panel pour une revue de documentation, et le pire pour tout ce
qui exige une réponse fiable à chaque question.

## Sources
- https://artificialanalysis.ai/articles/upstage-solar-pro-4
- https://www.prnewswire.com/news-releases/upstage-ai-unveils-solar-pro-4-scoring-42-on-artificial-analysis-index-to-rank-among-global-frontier-models-302856434.html
