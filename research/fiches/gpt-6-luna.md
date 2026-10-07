# GPT-6 Luna — OpenAI
<!-- GEN:prix|run=2026-10-07 -->
**Sur Freebuff :** 20/h
<!-- /GEN -->

## Identité
2026-09-22. 1M contexte. Paramètres non publiés.
`reasoning.effort` ∈ `none`, `low`, `medium`, `high`, `xhigh`, `max` — défaut `medium`.
**Chat Completions ne supporte les appels de fonction qu'à `effort: none`.**
Avec les outils intégrés, il faut passer par l'API Responses.
Prix API : 0,10 $ in / 0,50 $ out / 0,01 $ cache read / 0,125 $ cache write.
Sur Freebuff : **20/h**.

## Puissance — AA Intelligence Index v4.3.2, par palier
| Palier | Index | HLE | GDPval | AA-LCR | CritPt | SciCode | TB 4.0 | Omis.prec | non-hallu |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| max | **38,1** | 38,5 | 46,9 | 83,3 | 19,4 | 54,6 | **12,6** | 43,8 | 23,3 |
| xhigh | 34,6 | 34,3 | 43,2 | 80,0 | 17,4 | 51,7 | 8,1 | 44,2 | 17,6 |
| high | 32,9 | 32,9 | 42,2 | 79,3 | 15,4 | 50,3 | 4,5 | 42,8 | 15,6 |
| medium | 29,9 | 28,3 | 38,1 | 78,3 | 10,6 | 50,9 | 2,5 | 43,1 | 15,3 |
| low | 21,5 | 20,3 | 26,8 | 74,0 | 2,6 | 46,9 | 0,0 | 40,8 | 15,7 |
| none | 18,5 | 8,6 | 27,5 | 39,7 | 1,1 | 43,1 | 1,5 | 31,9 | 21,1 |

La comparaison initiale annonçait « de 22 à 38 ». La fourchette réelle est **18,5 à 38,1**,
et il y a six paliers, pas deux.

## Analyse de problèmes
C'est le profil le plus ** Specialist du panel : long contexte et coût, pas code agentique.
AA-LCR 83,3 % : il lit et retrouve l'information dans un gros document, aussi bien que
Solar Mini 4 et Ling. HLE 38,5 % : moyen. CritPt 19,4 % : moyen.

**TB 4.0 = 12,6 %**, 10e des douze. Et la progression est d'interaction faible :
0,0 % (low) → 2,5 → 4,5 → 8,1 → 12,6 (max). Même à fond, il est à la moitié de DeepSeek
(26,8 %) et au tiers de MiMo Pro (34,9 %). L'effort ne rachète pas le déficit structurel.

## Vitesse
141 tok/s chez OpenAI, **209 tok/s chez Azure** — même modèle, 1,5x d'écart.
1er token de réponse 107 s chez OpenAI, 55 s chez Azure. E2E 111 s chez OpenAI, 57 s chez Azure.
140M tokens générés sur l'index : **le plus bavard** des modèles analysés (médiane 100M).

## Coût
**0,07 $/tâche — le moins cher des douze.** Prix 0,10/0,50 $ = le moins cher aussi, avec
Grok 4.6. Cache write à 0,125 $, soit 2,5x le prix d'entrée : un contexte réécrit
constamment est facturé plus cher qu'un contexte lu. 152 tok/s de sortie en moyenne.

## Français
**Aucune donnée publiée.** OpenAI publie des évaluations multilingues sur ses autres modèles,
pas sur Luna dans les sources disponibles. Mais Luna inherits GPT-6 family, la plus large
couverture linguistique d'OpenAI, et l'index AA mesure de l'anglais de bout en bout.
Statut : **probablement le meilleur des douze en français, mais non prouvé.**

## Avantages
- **0,07 $/tâche, le moins cher des douze** — et l'index complet coûte 0,50 $ à lui seul.
- AA-LCR 83,3 % : excellent sur documents longs et questions denses.
- AA-Omniscience précision 43,8 %, 2e du panel derrière DeepSeek.
- Six paliers d'effort, le plus fin réglage disponible sur la plateforme.
- Cache preservation : « ajuster l'effort et les outils sans casser le cache ». Changer
  d'effort en cours de session ne détruit pas la réutilisation du contexte. C'est un
  avantage concret en session longue.
- 1M contexte, 51k tokens de sortie par tâche à max (fort, mais ce n'est pas le plus bavard
  en effort relatif).

## Inconvénients
- **TB 4.0 = 12,6 %.** Le pire profil agentique du panel avec Solar Mini 4. Si tu fais du
  code avec outils, Luna n'est pas le bon outil, quel que soit le palier.
- **Non-hallucination 23,3 %.** Deuxième pire du panel, à 4x Solar Mini 4 et 17x DeepSeek.
  Il affirme quand il ne sait pas. Précision 43,8 % correcte, mais la confiance est mal calibrée.
- **107 s avant le premier mot chez OpenAI.** Le plus lent du panel. Azure à 55 s est
  nettement meilleur : le fournisseur compte autant que le modèle.
- 20/h sur Freebuff pour le moins cher des douze en coût réel : le débit plateforme ne
  reflète pas l'efficience.
- Chat Completions cassé avec les outils au-dessus de `none` : piège d'intégration.
- Le mode `none` (index 18,5, AA-LCR 39,7 %) est inutilisable : le long contexte s'effondre.
  Le « mode rapide » de Luna ne sait pas lire un document long.
- Paliers bas inutilisables sur le raisonnement : CritPt tombe à 2,6 % (low) et 1,1 % (none).

## Verdict pour ton budget

> ⚠ **CONDITIONNEL.** Le verdict ci-dessous dépend de la grille Freebucks/h, qui provient
> d'une capture d'écran et n'est corroborée par aucune source. Le ledger local
> (`state.json.session-refunds.json`, 20 entrées) journalise des *remboursements* à 0 et ne
> peut ni confirmer ni infirmer la grille. Voir `comparatif.md` § Budget.
**Le champion du coût, mais pas du travail.** À 20/h c'est paradoxalement plus cher sur
Freebuff que DeepSeek (15/h) qui est 1,6x plus intelligent et 8x plus rapide.

Use-le pour : lire et questionner des documents longs, résumer, extraire, chercher dans un
contexte large. Ne l'utilise pas pour : écrire du code agentique, produire de la configuration,
ou toute tâche où une invention coûte cher.

Le seul vrai avantage budgétaire à 20/h est le mode **non-raisonné** (3,3 s, 0,15 $/tâche) pour
le traitement de masse, mais il faut vérifier que Freebuff l'expose.

## Sources
- https://artificialanalysis.ai/models/gpt-6-luna
- https://artificialanalysis.ai/models/releases/gpt-6-luna
- https://artificialanalysis.ai/models/gpt-6-luna/providers
- https://developers.openai.com/api/docs/models/gpt-6-luna
- https://openai.com/index/introducing-gpt-6-sol-and-luna/
- https://openrouter.ai/openai/gpt-6-luna
