# Space Bunny Alpha — éditeur anonyme
<!-- GEN:prix|run=2026-10-07 -->
**Sur Freebuff :** 🪦 retiré du catalogue le 06/10/2026
<!-- /GEN -->

> 🪦 **RETRAIT DU CATALOGUE FREEBUFF — 2026-10-06** (constaté le 2026-10-07, passe 10).
> **Il n'est plus dans le picker gratuit, ni dans `llms.txt`, ni dans `/plans`** : le catalogue
> passe de **12 à 11 modèles**. Source primaire GitHub, commit `c3edf98738bd` (2026-10-07
> 00:14 UTC) : la ligne est **supprimée du README** et l'id ajouté à
> `FREEBUFF_PAUSED_FREE_MODEL_IDS`.
>
> **Cause (commentaire du commit, primaire) :** OpenRouter a retiré tous les endpoints le
> **2026-10-05** ; le modèle était servi via la lane gratuite d'OpenCode Zen, qui **a commencé
> à refuser tout le trafic dès ~20:45Z ce jour-là** — toutes les sondes de la file, une toutes
> les cinq minutes pendant plus d'une heure, ont été refusées. **Aucun repli payant par
> conception** → chaque utilisateur qui l'avait choisi attendait la fin de la file pour un
> refus. Retiré le lendemain.
>
> **Conséquences pour ce dossier :** la section « Banc d'essai gratuit » du `verdict.md`
> (§ 1) est **caduque** — Space Bunny n'est plus un candidat mesurable. Toutes les mesures
> locales ci-dessous (I0, I8) restent **historiquement vraies**, mais portent sur un modèle
> désormais indisponible.
>
> **Pourquoi « pausé » et pas « supprimé »** : les binaires CLI/Desktop déjà publiés portent
> l'id (il était en accès limité depuis le 10-01) ; il doit rester reconnu pour être redirigé
> ou refusé proprement. **Restaurer = une seule ligne** dans le code. Statut : **suspendu,
> réversible**.

## Identité
Modèle **stealth**, apparu publiquement en septembre 2026. L'éditeur a choisi de ne pas
divulguer son identité pendant la préversion.
Trois identifiants pour le même modèle : `space-bunny` (API Space Bunny),
`stealth/space-bunny-alpha` (OpenRouter), `space-bunny-free` (OpenCode).
**1 000 000 de contexte**, **524 288 de tokens de sortie max** — le plus haut plafond de
sortie du panel. Entrée texte / image / **vidéo**, sortie texte.
Raisonnement toujours actif, **5 paliers** : low, medium, high, xhigh, max.
Outils (`tools`, `tool_choice`), sortie JSON (`response_format`), streaming.
Prix : **0 $ en prévision.**
Sur Freebuff : **0/h — mais retiré du catalogue le 06/10/2026** (voir encadré ci-dessus).
Historique Freebuff (GitHub, primaire) : lancé le **2026-09-23 à 10 Freebucks**, **dès 0/h
le jour même**, en accès limité depuis le **10-01**, retiré le **06-10**.
API OpenAI-compatible.

## Puissance — ⚠ aucune, et c'est le sujet
**Pas de page Artificial Analysis (404 vérifié).** Pas de benchmark. Pas de cardinalité.
Pas de licence. Pas de card de sécurité. Pas d'éditeur responsable. Aucune mesure de coût
par tâche, aucune vitesse, aucun résultat tiers.

La fiche la plus longue de ce dossier sur le sujet le plus court : il n'y a rien à comparer.
Tout ce qui suit est de la spécification d'interface, pas de la capacité.

## Ce qui est déclaré, par la documentation officielle
- Entrée image et vidéo, sortie texte : il **comprend** les médias, il ne les génère pas.
- La compatibilité vidéo **varie selon le fournisseur** et doit être testée avant tout usage.
- Les URLs doivent être joignables, ou en data URL base64.
- À 1M de contexte, la fenêtre utile est là — mais la qualité de récupération dans cette
  fenêtre n'est mesurée nulle part.

## Français
**Aucune donnée.** Modèle anonyme, aucune déclaration de langue, aucun benchmark multilingue.
Note de méthode : ce modèle est celui qui t'écrit actuellement dans cette session. Ce que je
dis de lui est donc une observation de première main **biaisée** — je suis le sujet, et un
modème n'est pas un juge neutre de lui-même. Aucune qualité mesurée ne peut être tirée de
ce dossier. À mesurer par l'usage, avec la même rigueur que les autres.

## Avantages
- ~~**Gratuit.**~~ **Tombé le 06/10/2026** : le 0/h n'existe plus parce que le modèle n'est
  plus servi. Ce qui restait vrai : 0 $, et un coût d'erreur nul *tant qu'il tournait*.
- **1M de contexte et 524K de sortie.** Le plus grand budget de sortie du panel : il peut
  produire des livrables entiers en une passe.
- **Vidéo en entrée**, ce qu'aucun autre des douze ne propose.
- 5 paliers d'effort, le plus fin réglage du panel avec Luna.
- Outils et JSON natifs, API OpenAI-compatible : intégration immédiate.
- 1er token de réponse court dans cette session, sensation réactive.
- Aucun risque de facturation : le pire cas est que le service disparaisse.

## Inconvénients
- **Éditeur inconnu.** Aucune obligation de continuité, aucun engagement de stabilité,
  aucun préavis de fin de service. Prévision peut s'arrêter du jour au lendemain.
  → **RÉALISÉ le 06/10/2026** : le service a effectivement cessé du jour au lendemain,
  sans préavis. La prévision de la fiche est confirmée par les faits.
- **Aucun benchmark, tiers ou constructeur.** Zéro. Le dossier ne peut pas le classer.
- **Aucune garantie sur la langue.** Sur un projet francophone, un modèle anonyme sans
  évaluation multilingue est le plus grand risque du panel, devant MiMo et GLM, parce que
  pour eux au moins l'éditeur **affirme** ne couvrir que en et zh. Ici on ne sait rien du tout.
- Vidéo « fragile » selon la documentation elle-même.
- Pas de carte de sécurité, pas d'évaluation de jailbreak.
- Les données partent chez un opérateur unique, avec une politique de conservation inconnue.
- Impossible de choisir : aucune donnée pour décider.

## Verdict pour ton budget

> 🪦 **VERDICT CADUC (2026-10-07).** Le modèle n'est plus offert par Freebuff depuis le
> 06/10 : ni 0/h, ni banc d'essai, ni candidat. Le texte ci-dessous est conservé **tel quel**
> (règle : une correction s'ajoute, elle ne remplace pas le journal) — il décrit un état
> qui n'existe plus.
> **Banc d'essai gratuit à re-choisir** : les 0/h restants du catalogue sont **Solar Pro 4**
> (promotional, open-ended depuis le 05/10) et, à titre métrique seulement, MiMo 2.6 Flash
> à 10 FB/h. Voir `comparatif.md` § Budget.

> ⚠ **CONDITIONNEL.** Le verdict ci-dessous dépend de la grille Freebucks/h, qui provient
> d'une capture d'écran et n'est corroborée par aucune source. Le ledger local
> (`state.json.session-refunds.json`, 20 entrées) journalise des *remboursements* à 0 et ne
> peut ni confirmer ni infirmer la grille. Voir `comparatif.md` § Budget.
**Le laboratoire gratuit, pas un modèle de production.**

Sa vraie valeur n'est pas « un modèle de plus à comparer » : c'est un banc d'essai sans
coût, ce qui est exactement ce qui manque à ce dossier. Tu as besoin de mesurer le français,
la latence, l'effort. Space Bunny Alpha est gratuit, multimodal, et disponible immédiatement :
c'est le candidat naturel pour le banc d'essai, parce que le coût d'erreur y est nul.

Ce qu'il ne faut pas en faire : une dépendance de production, un juge de qualité, ni une
référence. Si tu construis dessus, il faut un plan de repli explicite — c'est un service de
prévision, pas un service.

Et sa vraie question n'est pas « est-il bon ? » mais « reste-t-il gratuit, et combien de
temps ? ». À surveiller.
→ **Réponse connue : 13 jours** (gratuit le 2026-09-23, retiré le 2026-10-06). La question
était la bonne — c'était la seule de la fiche.

## Sources
- https://spacebunny.app/docs
- https://spacebunny.app/blog/what-is-space-bunny
- https://huggingface.co/blog/liliruli/how-to-use-space-bunny-alpha-the-complete-guide
- https://openrouter.ai/stealth/space-bunny-alpha
- GitHub `CodebuffAI/freebuff` commit **`c3edf98738bd`** — **primaire, 2026-10-07 00:14 UTC** :
  retrait du picker, README, `FREEBUFF_PAUSED_FREE_MODEL_IDS`, cause et chronologie du refus
- `freebuff.com/llms.txt` + `freebuff.com/plans` — **primaire, relus le 2026-10-07** : le
  modèle n'y figure plus (11 modèles listés)
- `freebuff-changelog.nordicnode.workers.dev/day/2026-10-07/` — **tier 2**, recoupé sur le
  commit ci-dessus
