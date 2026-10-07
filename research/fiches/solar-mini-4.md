# Solar Mini 4 — Upstage
<!-- GEN:prix|run=2026-10-07 -->
**Sur Freebuff :** 5 FB/h
<!-- /GEN -->

> ⚠ **PLUS GRATUIT DEPUIS LE 05/10/2026** (passe 9, changelog Freebuff) : *« Solar Mini 4's
> free promotion ended on 2026-10-05 »* — passé de la section `unlimited` à `optimized`.
> **Tout le raisonnement « 5/h = l'aubaine du panel » ci-dessous est périmé** : le prix de 5/h
> était celui d'une promo, et la promo est finie. Le constat *coût par tâche* reste valable,
> mais l'arbitrage « cheap en Freebucks » n'existe plus.
>
> ✏️ **CORRECTION (passe 10, 2026-10-07, source primaire `freebuff-solar-promo.ts`)** —
> **l'encadré ci-dessus avait la chronologie inversée.** L'histoire réelle datée :
> **5/h à son lancement (2026-09-23)** → **0/h du 2026-10-02 18:00Z au 2026-10-05** (promo
> *« Free through Sunday, Oct 4 PT »*) → **retour à 5/h le 2026-10-05 00:00 PT**.
> La promo, c'était le **0/h** ; **5/h est le prix courant**, pas l'inverse. Mon chiffre de
> 5/h du tableau initial était donc **juste**, et c'est l'encadré de passe 9 qui était faux.
> Conséquence pratique inchangée : **depuis le 05/10, 5 FB/h et section `optimized`** (plus
> dans le Unlimited gratuit).

## Identité
2026-09-23. **35B total / 3B actifs** (déclaré par Upstage, non vérifiable : modèle propriétaire).
524 288 de contexte. Texte uniquement. Raisonnement natif.
Prix API : 0,10 $ in / 0,40 $ out.
Sur Freebuff : **5 FB/h depuis le 05/10** (section `optimized`, plus dans le `unlimited`
gratuit ; gratuit 0/h du 02/10 au 04/10).

## Puissance — AA Intelligence Index v4.3.2
**24,1** — le dernier des douze avec une mesure. Sous-scores : HLE 25,8 % · **AA-LCR 83,3 %**
(égale Luna max, au-dessus de GPT-6 Astra max à 81 %) · GDPval-AA 1072 Elo / 28,6 % ·
SciCode 47,6 % · CritPt **1,4 %** · **Terminal-Bench 4.0 = 1 %** · AutomationBench-AA 22 % ·
AA-Omniscience **−11**, précision 18,4 %, **non-hallucination 64,2 %**.

## Analyse de problèmes
Le plus mauvais profil de raisonnement du panel : CritPt 1,4 %, TB 4.0 1 %. Il ne résout pas.
Sa valeur est ailleurs et elle est réelle : **AA-LCR 83,3 %** sur la compréhension en
contexte long. Il lit et retrouve l'information dans un gros document aussi bien que
Luna max, Muse Spark 1.3 et Ling 3.1 Flash, avec 3 milliards de paramètres actifs.

Scientifique : SciCode 47,6 %, devant MiniMax-M3 et Inkling (xhigh) à 47 %.
Économique : GDPval-AA Elo 1072, proche d'Inkling.

## Vitesse
**208 tok/s — le plus rapide du panel, avec DeepSeek.** Mais 88k tokens de sortie par tâche
dont 72k de raisonnement : **7,1 min par tâche**, plus lent que Luna max (5,8 min à 152 tok/s)
et 2,5x Inkling (2,8 min). Le débit est rapide, la tâche est lente.

## Coût — la découverte qui compte
AA titre : « coûte ~5x plus cher par tâche que GPT-6 Luna (max) malgré des prix par token
similaires ». Luna max = 0,07 $/tâche, donc **Solar Mini 4 ≈ 0,35 $/tâche**.

C'est l'inversion centrale du dossier : **le modèle le moins cher de la plateforme en
Freebucks/h (5/h) est l'un des plus chers en coût réel par tâche**, précisément parce qu'il
brûle 88k tokens de sortie. Le tri par prix de la plateforme produit l'ordre inverse de
l'ordre réel sur ce modèle.

## Français
**Aucune donnée.** Même origine coréenne que Solar Pro 4 : coréen, japonais, anglais.
Statut : **probablement le plus faible des douze**, non mesuré.

## Avantages
- **5/h : 29 h de budget pour le prix de 2 h de MiMo Pro.**
- **AA-LCR 83,3 %** : la lecture en long contexte est son vrai talent, à égalité avec les
  meilleurs du panel.
- Non-hallucination 64,2 % : 2e du panel. Quand il dit ne pas savoir, il dit vrai.
  Bien meilleur que DeepSeek (3,5 %) et Luna (23,3 %).
- 208 tok/s : très réactif en lecture.
- 3B actifs seulement : le moins cher à héberger, en local ou non.
- 524K contexte : le 3e plus grand du panel.
- Prix API le plus bas : 0,10/0,40 $.
- AA note qu'il définit un nouveau point de Pareto intelligence / paramètres actifs sous 3B.

## Inconvénients
- **TB 4.0 = 1 % et CritPt 1,4 %.** Il n'est pas un modèle de raisonnement. Ne lui confie
  aucune tâche d'analyse.
- **88k tokens de sortie par tâche, 72k en raisonnement.** Coût réel ~0,35 $/tâche pour un
  index de 24. C'est le mauvais rapport coût/qualité du panel, et le prix affiché de 5/h
  le masque complètement.
- 7,1 min par tâche : lent malgré 208 tok/s.
- Précision AA-Omniscience 18,4 %, la plus basse des sept modèles où elle est publiée.
  Il se trompe plus souvent que tout le monde — et comme son non-hallucination est bon,
  il se trompe en le disant clairement.
- GDPval-AA 28,6 % : très faible sur le travail de connaissance.
- Texte uniquement. Pas d'image, pas d'audio.
- Taille non vérifiable : 35B/3B est une déclaration constructeur sur un modèle fermé.

## Verdict pour ton budget

> ⚠ **CONDITIONNEL.** Le verdict ci-dessous dépend de la grille Freebucks/h, qui provient
> d'une capture d'écran et n'est corroborée par aucune source. Le ledger local
> (`state.json.session-refunds.json`, 20 entrées) journalise des *remboursements* à 0 et ne
> peut ni confirmer ni infirmer la grille. Voir `comparatif.md` § Budget.
**Pas un modèle de travail. Un modèle de lecture, et uniquement là où c'est gratuit.**
Le piège est total : 5/h semble être l'aubaine du panel, et le coût par tâche réel est
5x celui du modèle le moins cher. Ne l'utilise pas pour « économiser ».

Utilise-le pour : parcourir un gros document, en extraire des faits, un lot de résumés.
Ignoré pour : tout ce qui doit réfléchir. Si tu veux lire un document long, Ling 3.1 Flash
le fait gratuitement (0/h) avec 83,0 % d'AA-LCR et 62,1 % de non-hallucination, donc un
meilleur choix à prix nul.

## Sources
- https://artificialanalysis.ai/articles/korean-ai-lab-upstage-releases-solar-mini-4
- https://openrouter.ai/upstage/solar-mini4
