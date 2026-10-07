# MiMo-V2.6-Pro — Xiaomi
<!-- GEN:prix|run=2026-10-07 -->
**Sur Freebuff :** 30/h
<!-- /GEN -->

## Identité
2026-09-22. **Plus de 1T paramètres**, open-weight (MIT), rapport technique publié.
1M contexte. Entrée texte / image / vidéo / **audio**, sortie texte.
Trois variantes : `mimo-v2.6-pro`, `mimo-v2.6-flash`, `mimo-v2.6-pro-ultraspeed` (20x).
Prix API : 0,435 $ in / 0,87 $ out / 0,0036 $ cache. Blended 0,18 $.
Sur Freebuff : **30/h** — le plus cher de la plateforme.

## Puissance — AA Intelligence Index v4.3.2
**46,3** — le **meilleur open-weight** des douze (les poids de Muse Spark 1.3 ne sont pas publics).

Sous-scores : **HLE 49,4 %** (le plus élevé des douze) · **AA-LCR 86,3 %** (le plus élevé) ·
GDPval-AA 59,4 % (le plus élevé) · SciCode 60,9 % · CritPt 26,6 % (le plus élevé) ·
**TB 4.0 34,9 %** (le plus élevé des douze) · AA-Briefcase 1517 (le plus élevé) ·
Omniscience précision 34,8 %, non-hallucination 59,4 %.

Position : 11e sur l'index AA global, derrière Claude Opus 5.5 (58), Claude Sonnet 5.5 (56),
GPT-6 Astra (52,7), Gemini 4 Argon (52,6), GPT-6.1 Sol (51,8), Claude Opus 5 (50,8).

## Analyse de problèmes
C'est le modèle de raisonnement le plus solide des douze sur les trois axes qui comptent :
HLE (49,4 %), CritPt (26,6 %), TB 4.0 (34,9 %). DeepSWE v1.1 pendant le RL :
58,4 → 72,6 en six jours, ~750k trajectoires, ~2,62 M$ de coût d'entraînement.

## Vitesse
**37,4 tok/s — le plus lent des douze.** TTFT 3,78 s, temps de raisonnement 47,9 s,
1er token de réponse 47,9 s, E2E 64 s, 1 420 s par tâche (23,7 min).

Écart fournisseur énorme sur le même poids : Xiaomi 42 tok/s, DeepInfra 26, Novita 43,
**PrimaLabs 310**. Soit 11,4x entre le plus lent et le plus rapide. AA note 64k tokens de
sortie par tâche dont 38k de raisonnement — bavard.

## Coût
0,13 $/tâche — le 3e moins cher des douze. Coût total de l'index : 207 $ (le moins cher
aussi, devant Luna). Cache hit à 99 % de remise : sur une session longue avec contexte
répété, l'écart réel se resserre encore.

## Français
**Drapeau rouge.** La carte officielle `XiaomiMiMo/MiMo-V2.6-Pro-RL` déclare
`language: - en - zh`. La documentation Xiaomi est explicite : « Bilingual & Dialects:
Chinese, English, code-switching, Wu, Cantonese, Minnan, Sichuanese ».

Le français n'est pas revendiqué. Ce n'est pas la preuve qu'il écrit mal en français, mais
c'est l'absence de toute garantie constructeur, sur le modèle qui est le meilleur du panel.
À vérifier avant d'en faire ton modèle par défaut.

## Avantages
- Meilleur open-weight des douze, et le seul avec un rapport technique public.
- Champion sur HLE, CritPt, TB 4.0, AA-LCR, GDPval, Briefcase : six premières places.
- 1M contexte, entrée **audio** en plus de l'image et de la vidéo.
- Cache hit à 99 % de remise : le moins cher à l'usage répété.
- Open-weight : déployable localement, auditable, pas de dépendance plateforme.

## Inconvénients
- **Le plus lent des douze** : 64 s E2E contre 13 s pour DeepSeek. Sur 100 itérations, ~1 h 45 perdues.
- **30/h sur Freebuff** : 4 h 50 pour tout ton budget. À ce prix, tu ne peux pas l'utiliser
  en boucle, seulement en escalade.
- **Ni le français ni aucune autre langue hors en/zh déclarés.**
- Non-hallucination 59,4 %, correct mais loin de Muse Spark (67,1 %).
- Précision AA-Omniscience 34,8 % : nettement derrière DeepSeek (46,4 %) et Luna (43,8 %).
  Il se trompe plus souvent que ces deux-là, mais le dit un peu plus souvent.
- Pas de contrôle fin de l'effort documenté comme Luna ou GLM.

## Verdict pour ton budget

> ⚠ **CONDITIONNEL.** Le verdict ci-dessous dépend de la grille Freebucks/h, qui provient
> d'une capture d'écran et n'est corroborée par aucune source. Le ledger local
> (`state.json.session-refunds.json`, 20 entrées) journalise des *remboursements* à 0 et ne
> peut ni confirmer ni infirmer la grille. Voir `comparatif.md` § Budget.
**Excellente qualité, mauvaise ergonomie.** À 30/h c'est un modèle d'escalade : tu l'utilises
quand DeepSeek ou Ling ont échoué, pas en première intention. Si le français se révèle correct,
c'est le meilleur candidat pour les tâches longues et difficiles à 4 h 50 de budget.

## Sources
- https://mimo.mi.com/docs/en-US/news/latest/v2-6
- https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Pro-RL
- https://artificialanalysis.ai/models/mimo-v2-6-pro
- https://artificialanalysis.ai/models/mimo-v2-6-pro/providers
- https://openrouter.ai/xiaomi/mimo-v2.6-pro
