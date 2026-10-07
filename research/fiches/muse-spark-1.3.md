# Muse Spark 1.3 — Meta
<!-- GEN:prix|run=2026-10-07 -->
**Sur Freebuff :** 🔒 payant (plans payants)
<!-- /GEN -->

## Identité
Meta Superintelligence Labs, 2026-09-02. Poids **non publics**. 1M contexte.
Compatible protocole Anthropic et OpenAI. Raisonnement : `max` / `xhigh`.
Prix API : 1,25 $ in / 4,25 $ out / 0,15 $ cache par 1M. Blended 0,78 $.
Sur Freebuff : **🔒 `Access = Paid plans`** (GitHub README). Il **apparaît dans le picker
gratuit de `llms.txt` mais sans accès** — inaccessible sur ton compte français sans
abonnement. Fallback : *« When it is busy or unavailable, it answers on DeepSeek V4.1 Flash
rather than making you wait »* — **tu peux croire parler à Muse Spark sans en parler à Muse
Spark.**

## Puissance — AA Intelligence Index v4.3.2
| Palier | Index | Codage | Agentique |
|---|---:|---:|---:|
| max | **48,1** | 75,8 | 55,5 |
| xhigh | 45,1 | 76,5 | 51,5 |

Sous-scores (max) : GPQA Diamond 93,5 % · HLE 48,7 % · GDPval-AA 59,2 % · AA-LCR 83,0 % ·
SciCode 58,8 % · CritPt 24,9 % · τ-Bench Banking 50,5 % · **TB 4.0 33,3 %** ·
Omniscience précision 43,6 %, non-hallucination 67,1 %.

**C'est le score le plus élevé des douze.** Meilleure non-hallucination des douze avec
Solar Mini 4.

## Analyse de problèmes
Meilleur que MiMo Pro sur 6 des 10 composantes de l'index AA (Briefcase 1517, GDPval 1688,
AutomationBench 59 %, SciCode 61 %, Omniscience 14, LCR 80 pour GLM — voir la comparaison
MiMo Pro vs GLM 5.3 max dans `verdict.md`). Sur le raisonnement pur (HLE 48,7 %) il est
proche de MiMo Pro (49,4 %).

Contrepartie assumée par Meta : entre la 1.2 et la 1.3, ~20 % d'appels d'outils en moins et
~25 % de tokens en moins. Moins bavard = moins de contexte perdu sur les sessions longues.
C'est un avantage réel pour un outil de code, et un signal de conception assumé.

## Vitesse
140 tok/s (148 pour xhigh), E2E 37 s, 1er token de réponse 34,9 s. Raisonnement 9,9 s.

## Coût
**1,60 $/tâche** sur l'index AA. Le plus cher des douze, de 23x Luna max (0,07 $).
Coût total de l'index : 1 600 $.

## Français
**Aucune donnée publiée.** Meta ne publie aucune évaluation multilingue pour ce modèle.
Rien ne déclare le français, rien ne l'exclut non plus. Statut : **inconnu**, à mesurer.

## Avantages
- Le plus intelligent des douze sur index commun.
- Meilleure non-hallucination (67,1 %) → le plus fiable pour du code et de la config.
- 25 % de tokens en moins que la génération précédente : sessions longues moins coûteuses.
- Protocole Anthropic compatible : migration d'outillage facile.
- GDPval-AA 59,2 % : bon sur le travail de connaissance, pas seulement sur le code.

## Inconvénients
- **Prix non affiché sur Freebuff.** Impossible de budgéter tant que la plateforme ne répond pas.
- 23x le coût par tâche de Luna. À tarif Meta, ~10 tâches absorbent 145 Freebucks d'équivalent.
- Le palier `xhigh` est **moins bon que `max` en code agentique** : 16,7 % contre 33,3 % sur
  TB 4.0, soit une division par deux, alors que son index global est meilleur. Comportement
  contre-intuitif, non expliqué par l'éditeur.
- Résultat très sensible au harness : TB 4.0 = 33,3 % chez AA, 10,6 % chez Vals AI. Même
  modèle, même palier, 3x d'écart.
- La méthodologie de Meta annonce retenir « la valeur comparable la plus haute » entre leur
  propre eval, le leaderboard officiel et l'auto-déclaration du fournisseur. Sélection
  optimiste explicite.
- TB 2.1 = 84,3 % mais TB 4.0 = 33,3 %. L'écart mesure à quel point le benchmark 4.0 est plus dur,
  pas une régression du modèle.

## Verdict pour ton budget

> ⚠ **CONDITIONNEL.** Le verdict ci-dessous dépend de la grille Freebucks/h, qui provient
> d'une capture d'écran et n'est corroborée par aucune source. Le ledger local
> (`state.json.session-refunds.json`, 20 entrées) journalise des *remboursements* à 0 et ne
> peut ni confirmer ni infirmer la grille. Voir `comparatif.md` § Budget.
**Le meilleur des douze, à condition de connaître son prix.** C'est la seule donnée manquante
qui bloque une décision. Demande à Freebuff le débit de Muse Spark 1.3. Si c'est proche de
0,78 $/1M blended, il est hors budget pour un usage quotidien. Si la plateforme le subventionne,
c'est le choix par défaut pour le code difficile.

## Sources
- https://research.meta.ai/blog/introducing-muse-spark-1-3
- https://research.meta.ai/static/muse-spark-1-3-multimodal-evaluation-methodology
- https://developer.meta.com/ai/models/muse-spark/
- https://artificialanalysis.ai/models/releases/muse-spark-1-3
- https://openrouter.ai/meta/muse-spark-1.3
