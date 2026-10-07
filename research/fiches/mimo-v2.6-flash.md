# MiMo-V2.6-Flash — Xiaomi
<!-- GEN:prix|run=2026-10-07 -->
**Sur Freebuff :** 10/h
<!-- /GEN -->

## Identité
2026-09-22. Variante basse de MiMo. Open-weight. 1M contexte.
Entrée texte / image / vidéo / audio, sortie texte. Omnimodal natif.
Raisonnement activable (`thinking: {type: "disabled"}` pour le désactiver).
Prix API identique à Pro : 0,435 $ in / 0,87 $ out / 0,0036 $ cache.
Sur Freebuff : **10/h**.

## Puissance — AA Intelligence Index v4.3.2
**37,9** — 7e des douze mesurés. Sous-scores mesurés : **Terminal-Bench 4.0 = 22,7 %**.
Vitesse 51 tok/s, TTFT 3,91 s, E2E 52,8 s.
Index AA global : 32e sur 118 pour les modèles open-weight de taille comparable.

Le reste des sous-scores n'a pas été récupéré dans les sources consultées : **n.d.**

Position : 1,6 point sous DeepSeek V4.1 Flash (39,5), 3,9 sous GLM Flash (41,8),
8,4 sous MiMo Pro (46,3).

## Analyse de problèmes
TB 4.0 à 22,7 % : le deuxième pire des modèles raisonnaurs du panel, devant Luna (12,6)
et Solar Mini 4 (1). C'est son plafond mesuré. Pour du raisonnement, DeepSeek fait mieux
en étant 5x plus rapide, et GLM Flash fait mieux pour le même prix.

Côté RL : Xiaomi annonce que **Flash dépasse complètement MiMo-V2.5-Pro** après entraînement,
et DeepSWE v1.1 progresse de 48,8 à 65,7 en six jours (~750k trajectoires, ~850 k$).
C'est une vraie montée en puissance, mais le niveau absolu reste sous ses concurrents directs.

## Vitesse
51 tok/s. **Presque 4x plus rapide que MiMo Pro** (37 tok/s) pour 8,4 points d'index de moins.
C'est le compromis interne à la famille Xiaomi et il est bien fait.

## Coût
**0,06 $/tâche — le moins cher des douze mesurés.** Blended 0,18 $/1M, cache hit à 99 % de remise.

## Français
**Même drapeau rouge que Pro.** La documentation Xiaomi déclare explicitement chinois et
anglais (+ dialectes chinois : Wu, Cantonese, Minnan, Sichuanese). Le français n'est pas
revendiqué. Aucun score français publié.

## Avantages
- **0,06 $/tâche, le moins cher du panel** (avec Luna max à 0,07 $).
- Cache hit à 99 % de remise : sur une session avec contexte répété, c'est le moins cher
  en usage réel, pas seulement en théorie.
- **Omnimodal** : texte, image, vidéo **et audio**. Le seul du panel avec de l'audio en entrée
  avec MiMo Pro. Aucun autre des douze ne prend de l'audio.
- 51 tok/s : 1,4x plus rapide que Pro.
- 1M contexte.
- Open-weight, rapport technique public, RL documenté.
- 10/h sur Freebuff : 14 h 30 de budget.

## Inconvénients
- **Ni le français ni aucune autre langue hors en/zh déclarés.** Même drapeau que Pro.
- **TB 4.0 à 22,7 %** : mauvais en code agentique, et c'est son usage principal.
- 37,9 d'index : 7e du panel. Ce n'est pas le modèle pour les tâches difficiles.
- 52,8 s E2E : lent, même si 5x moins que les pioneers.
- **Même prix API que Pro** (0,435/0,87 $) alors qu'il est 8,4 points moins bon. À prix
  identique, le choix Flash se justifie uniquement par le débit de la plateforme, qui
  différencie 10/h contre 30/h.
- Les sous-scores détaillés ne sont pas publiés dans mes sources : l'analyse de problèmes
  repose sur TB 4.0 seul.

## Verdict pour ton budget

> ⚠ **CONDITIONNEL.** Le verdict ci-dessous dépend de la grille Freebucks/h, qui provient
> d'une capture d'écran et n'est corroborée par aucune source. Le ledger local
> (`state.json.session-refunds.json`, 20 entrées) journalise des *remboursements* à 0 et ne
> peut ni confirmer ni infirmer la grille. Voir `comparatif.md` § Budget.
**Bonne valeur si le français passe, mais GLM Flash l domine à prix égal.**

À 10/h, GLM 5.3 Flash donne AA 41,8 contre 37,9, TB 4.0 32,8 % contre 22,7 %, et un blended
de 0,098 $ contre 0,18 $. Les deux sont open-weight et tous deux ne déclarent que en+zh.
Si tu choisis entre les deux à prix Freebuff égal, GLM Flash gagne sur tous les axes mesurés.

Ce que MiMo Flash apporte en plus : **l'entrée audio**. Si tu travailles sur de la
transcription ou de l'analyse sonore, c'est le seul du panel qui le fait, et il n'a pas
d'équivalent.

## Sources
- https://mimo.mi.com/docs/en-US/news/latest/v2-6
- https://mimo.mi.com/static/docs/updates/model.md
- https://mimo.mi.com/models/en-US/mimo-v2.6-flash
- https://artificialanalysis.ai/leaderboards/models
