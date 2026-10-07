# Ling 3.1 Flash — inclusionAI (Ant Group)
<!-- GEN:prix|run=2026-10-07 -->
**Sur Freebuff :** hors catalogue
<!-- /GEN -->

> ⚠ **HORS CATALOGUE FREEBUFF** (passe 8, investigation I10). Aucune source primaire du
> 2026-10-06 ne place ce modèle sur Freebuff — `llms.txt`, `/plans`, `/live` et le GitHub
> README s'accordent sur 12 modèles, sans lui. Le **0/h Freebuff que je lui attribuais était
> faux** : il vient d'OpenRouter / Vercel AI Gateway. Gratuit **jusqu'au 2026-10-13 sur
> Vercel**, pas via tes Freebucks.

## Identité
2026-09-30 sur OpenRouter, 2026-10-02 comme date de release AA.
**560B total / 25B actifs**. Hybrid reasoning MoE. AA classe le modèle en « proprietary »
malgré l'annonce d Ant d'une mise open source après l'essai gratuit.
Contexte : **262 144 tokens** — le plus petit des douze. 32 768 tokens de sortie max.
Thinking activé par défaut, désactivable. Outils, MCP, cache implicite.
Sur Freebuff : **absent du catalogue**.

> ⏰ **FENÊTRE FERMÉE.** Ant annonce un essai gratuit de deux semaines à partir du
> 2026-09-30 (→ ~2026-10-16). Vercel AI Gateway : gratuit **jusqu'au 2026-10-13**. Nous sommes
> le 2026-10-06. Le statut gratuit est une fenêtre de 7 à 10 jours, pas un état permanent.

## Puissance — AA Intelligence Index v4.3.2
**41,1** — 4e des douze, et **le meilleur rapport qualité/gratuit du panel**.

Sous-scores : HLE 39,4 % · **AA-LCR 83,0 %** · GDPval-AA 56,1 % · CritPt 18,0 % ·
SciCode 54,1 % · **TB 4.0 33,3 %** · Omniscience précision 29,1 %, non-hallucination **62,1 %**.

Comparaison directe AA (DeepSeek V4.1 Flash max 39,5 · GLM 5.3 Flash 41,8) : Ling est
**plus intelligent que DeepSeek** et à égalité d'index avec GLM Flash, pour 0 Freebucks.

Tableur Ant (non reproduit indépendamment au jour de la publication) :
TB 4.0 40,40 (DeepSeek 31,20 · GLM Flash 32,80) · SWE-Pro 65,39 (56,77 · 63,06) ·
BrowseComp 91,67, meilleur de la table · MCP-Atlas 83,00 · CyberGym 87,90.
Mais DeepSeek garde la tête sur DeepSWE 74,20 contre 59,70, et sur MultiChallenge 72,12 contre 69,78.

## Analyse de problèmes
Deux temps sur long horizon : Ling gagne TB 4.0 (le plus dur) et perd TB 2.1 face à DeepSeek
(81,18 contre 90,60). Lecture : il est plus **robuste sur les tâches récentes et dures** que
sur les tâches longues déjà normalisées. Pour un agent qui travaille sur du frais, c'est
le bon profil. Aucun chiffre HLE/CritPt cares comparable à DeepSeek ou GLM au-delà de AA.

## Vitesse
**Non mesurée par AA** (page sans chiffres de vitesse). AA classe Ling 3.0 Flash à 353 tok/s,
ce qui fait de la famille la plus rapide du marché, mais **ce n'est pas le 3.1**.
À mesurer. Le 0/h rend l'absence de mesure coûteuse.

## Coût
0 $/tâche côté AA (non mesuré). **Pas de coût Freebucks : n'est pas un modèle Freebuff.**
Gratuit sur **Vercel AI Gateway jusqu'au 2026-10-13**, et sur Ant ~2026-10-16 (essai de deux
semaines, limité à 256 000 tokens, 1M contexte annoncé ensuite) — **un autre canal que tes
Freebucks**.

## Français
**Aucune donnée publiée.** Aucun classement sur un benchmark multilingue. inclusionAI
(Ant Group) publie en chinois et en anglais. Rien ne déclare le français, rien ne l'exclut.
Ant revendique des gains en médical, finance et science des matériaux, ce qui implique une
base large, mais ce n'est pas une preuve.

## Avantages
- **Gratuit, 4e du panel en intelligence** — mais via Vercel/Ant, **pas Freebuff** (voir
  l'encadré en tête). Fenêtre fermée le 2026-10-13.
- Meilleure non-hallucination que DeepSeek (62,1 % contre 3,5 %) et que Luna (23,3 %).
- TB 4.0 = 33,3 % : agent terminal réel, égal au meilleur du panel.
- BrowseComp 91,67 et MCP-Atlas 83,00 : conçu pour la recherche et les outils.
- Open source annoncé.
- 25B actifs : déployable en local, contrairement à MiMo Pro.

## Inconvénients
- **262 144 de contexte, soit 4x moins que les 11 autres.** Sur un gros dépôt ou un
  document long, c'est un mur. AA-LCR 83,0 % se mesure dans les limites de cette fenêtre.
  C'est le seul critère où il est nettement moins bien que tout le monde.
- **0/h signifie probablement quota, pas illimité.** Investigation I2 : mesure le seuil.
- **Aucun chiffre de vitesse ni de coût par tâche.** AA n'a pas mesuré. On ne peut pas le
  placer sur le rapport latence/coût, et c'est précisément ce qu'il faudrait pour l'utiliser
  en boucle.
- Précision AA-Omniscience 29,1 % : la plus basse des six modèles où elle est publiée.
  Il se trompe, mais il le dit (62,1 % de non-hallucination).
- Poids non encore publiés à la date des sources.
- **Aucune carte de sécurité.** Ant n'a publié ni red-team, ni évaluation de jailbreak,
  ni system card. Le seul test externe disponible porte sur Ling 3.0 Flash, pas 3.1,
  et rapporte 26 % de bugs sur tâches multi-tours.

## Verdict pour ton budget

> ⚠ **CONDITIONNEL.** Le verdict ci-dessous dépend de la grille Freebucks/h, qui provient
> d'une capture d'écran et n'est corroborée par aucune source. Le ledger local
> (`state.json.session-refunds.json`, 20 entrées) journalise des *remboursements* à 0 et ne
> peut ni confirmer ni infirmer la grille. Voir `comparatif.md` § Budget.
**Le meilleur choix par défaut si le 0/h est réel.** AA 41,1 avec 62,1 % de non-hallucination
et TB 4.0 à 33,3 %, gratuit. Il remplace GLM Flash (10/h) et DeepSeek (15/h) sur tout le
travail non critique et multi-tour, là où DeepSeek hallucine.

Deux réserves qui se combinent mal : **le contexte de 262K** interdit les sessions vraiment
longues, et **l'absence de toute mesure de vitesse** empêche de savoir s'il est utilisable en
boucle. Sur les deux, c'est le modèle que je testerais en premier.

## Sources
- https://openrouter.ai/inclusionai/ling-3.1-flash
- https://artificialanalysis.ai/models/ling-3-1-flash
- https://technode.com/2026/09/30/ant-group-launches-ling-3-1-flash-with-560-billion-parameters/
- https://threatfrontier.com/articles/ling-3-1-flash-ant-group-best-flash-model-yet-cybergym
- https://vercel.com/changelog/ling-3.1-flash-is-now-available-on-ai-gateway
