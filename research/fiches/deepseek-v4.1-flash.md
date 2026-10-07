# DeepSeek-V4.1-Flash — DeepSeek
<!-- GEN:prix|run=2026-10-07 -->
**Sur Freebuff :** 15/h
<!-- /GEN -->

## Identité
2026-09-09. **552B backbone + 196B Engram**, open-weight. 8B actifs en prefill, 16B en décode.
Architecture Causal Encoder-Decoder, 40 couches (20 encodeur + 20 décodeur).
CSA2 (Compressed Sparse Attention 2) en 3 modes statiques : Full / Reindex / Reuse.
KV cache global 890 octets/token en FP4 (~1/4 de V4-Flash), persistant ~1/8 (SWA Bounded Replay).
Pré-entraînement 45T tokens, contexte étendu à 1M à 34T tokens.
Multimodal natif texte + image. Effort de raisonnement **continu**, pas à paliers.
Prix API : 0,30 $ in / 1,20 $ out / 0,006 $ cache. Blended 0,184 $.
Sur Freebuff : **15/h**.

## ⚠ Avertissement de routage
DeepSeek a **retiré** `deepseek-v4-flash` et `deepseek-v4-pro` : depuis le 14/09/2026 04:00 UTC,
ils routent vers V4.1-Flash. La base Freebuff locale contient un thread configuré sur
`deepseek/deepseek-v4-flash`, qui sert donc V4.1-Flash sous un libellé obsolète.
Si l'interface affiche « V4 Flash », c'est V4.1-Flash. Ne raisonne pas sur le libellé.

## Puissance — AA Intelligence Index v4.3.2
**39,5.** Sous-scores : AA-Briefcase 1421 · GDPval-AA 1600 Elo · **AutomationBench 69 %** (le
meilleur des douze) · TB 4.0 26,8 % · SciCode 52 % · HLE 39,2 % · GDP.pdf 13 % · CritPt 14,3 % ·
AA-Omniscience **−5** (le plus bas) · AA-LCR 84,0 %.

Tableur Ant : DeepSWE 74,20 (meilleur du panel), TB 2.1 90,60 (meilleur du panel),
MultiChallenge 72,12 (meilleur du panel).

## Analyse de problèmes
AutomationBench 69 % et DeepSWE 74,2 % disent qu'il exécute bien et termine le travail.
HLE 39,2 % et CritPt 14,3 % disent qu'il raisonne moyen. TB 4.0 à 26,8 % est le point faible :
il est 6e du panel alors qu'il est 6e en index. Si tu fais du code long-horizon difficile,
c'est un défaut mesuré, pas une impression.

## Vitesse
**209 tok/s — le plus rapide des douze, de loin.** TTFT **1,02 s**, 1er token de réponse
**10,6 s**, E2E **13 s**, 304 s par tâche.
Sans raisonnement : 215 tok/s, TTFT 0,95 s, E2E 3,3 s, index 25,0.
AA note la variante Azure à 209 tok/s contre 141 chez OpenAI pour le même Luna :
**le débit dépend autant du fournisseur que du modèle.**

## Coût
0,27 $/tâche en raisonnement max, 0,15 $ sans raisonnement (index 25,0).
89k tokens de sortie par tâche dont 63k de raisonnement : le plus bavard des trois
modèles comparables : DeepSeek 89k, contre MiMo Pro à 64k et GLM Flash à 69k.

## Français
**Aucune donnée publiée.** DeepSeek est réputé multilingue et GiLM est utilisé en français
dans la communauté, mais aucune évaluation officielle pour V4.1-Flash. Statut : **inconnu**.

## Avantages
- **Le plus rapide des douze**, et de loin : 13 s E2E contre 64 s pour MiMo Pro.
- **Meilleure précision AA-Omniscience des douze : 46,4 %.** Quand il répond juste, il
  répond vraiment juste.
- AutomationBench 69 % et MultiChallenge 72,1 % : les meilleurs du panel sur l'exécution
  d'outils et la conversation multi-tour.
- 1M contexte, effort continu donc réglable finement — le seul des douze dans ce cas.
- Cache hit à 98 % de remise, et 0,006 $/1M : le moins cher en entrée répétée.
- Open-weight, et l'architecture CED est explicitement conçue pour les charges agentiques
  à forte entrée, ce qui correspond à ton usage.
- Sans raisonnement : index 25,0 à 0,15 $/tâche et 3,3 s. Un mode « traitement de masse ».

## Inconvénients
- **Non-hallucination 3,5 %. Le plus bas des douze, de très loin.** Il ne dit presque jamais
  « je ne sais pas ». Sur du code, il va inventer une API, une signature, une option de
  configuration, avec un ton affirmatif. Muse Spark 1.3 est à 67,1 %, Ling à 62,1 %.
  **C'est le seulygrave de ce dossier** et il conditionne tout le reste.
- Omniscience composite à **−5**, le plus bas. Précision bonne, mais l'aveu d'ignorance
  quasi inexistant.
- TB 4.0 à 26,8 % : mauvais sur le code long-horizon difficile, précisément sa cible revendiquée.
- 63k tokens de raisonnement par tâche : le coût réel est fonction du raisonnement, pas du prix affiché.
- 0,27 $/tâche : 4x Luna pour 1,4 point d'index de moins.
- Attention : la comparaison initiale comparait V4.1 Flash (39,5) à V4 Flash 0731 (34,3),
  deux modèles différents confondus par le routage. Vérifie quel libellé est réellement servi.

## Verdict pour ton budget

> ⚠ **CONDITIONNEL.** Le verdict ci-dessous dépend de la grille Freebucks/h, qui provient
> d'une capture d'écran et n'est corroborée par aucune source. Le ledger local
> (`state.json.session-refunds.json`, 20 entrées) journalise des *remboursements* à 0 et ne
> peut ni confirmer ni infirmer la grille. Voir `comparatif.md` § Budget.
**Le meilleur pour itérer vite, à condition de relire systématiquement.** À 15/h c'est
9 h 40 de budget pour le seul modèle qui te livre une réponse en 13 s. Utilise-le pour
explorer, chercher, itérer sur du code que tu vas relire de toute façon.

Ne l'utilise pas pour écrire de la configuration, de la migration ou du SQL où une invention
passe en production. Pour ça : Ling 3.1 Flash (62,1 % de non-hallucination, gratuit) ou
Muse Spark 1.3 (67,1 %) si le budget suit.

## Sources
- https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash
- https://arxiv.org/html/2609.19969
- https://www.deepseek.com/en/news/deepseek-v4-1-flash/
- https://build.nvidia.com/deepseek-ai/deepseek-v4.1-flash/modelcard
- https://artificialanalysis.ai/models/comparisons/deepseek-v4-1-flash-vs-glm-5-3-flash
- https://openrouter.ai/deepseek/deepseek-v4.1-flash
