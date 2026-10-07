# DeepSeek V4.1 Flash Fast — endpoint Freebuff réel, origine upstream inconnue
<!-- GEN:prix|run=2026-10-07 -->
**Sur Freebuff :** 5 j/h
<!-- /GEN -->

> ✅ **EXISTENCE PRUVÉE (passe 8, I10)** — j'avais écrit « aucune source ne mentionne ce
> produit ». **Faux** : `freebuff.com/llms.txt`, `/plans` (« 5hrs DeepSeek V4.1 Flash Fast »),
> `/live` et le GitHub README le listent tous (npm : 403). Ce que je cherchais — un document
> **DeepSeek/upstream** — n'existe toujours pas : c'est **un endpoint exposé par Freebuff
> dont la provenance reste non documentée**.

## Identité
Ce que la plateforme affiche : un endpoint distinct « DeepSeek V4.1 Flash Fast ».
Tarif : **mon 25/h était sur palier** ; la page `/plans` (Starter) donne **5 h/jour**, soit
0,52 $/h — le prix le plus élevé des modèles non verrouillés après GPT-6.1 Sol.

> **Passe 10 — le tarif exact, source primaire** (`freebuff-models.ts`, lu 2026-10-07) :
> *« Priced on DeepSeek's own clock: **50 Freebucks in the weekday window where DeepSeek
> direct doubles, 25 the rest of the time** »*. Le 25/h que je tenais de la capture est donc
> **le hors-palier** ; il existe un **palier semaine à 50/h**, soit **2× plus cher**. Mon
> « 5 h 48 sur 145 FB » n'est valable **qu'en dehors de la fenêtre de pointe**.

## Ce que les sources disent
**Rien côté amont.** Aucune source primaire, aucune documentation, aucun communiqué, aucune
page de fournisseur ne mentionne un produit nommé « V4.1 Flash Fast » **chez DeepSeek**, chez
un fournisseur d'hébergement, ou ailleurs. C'est Freebuff qui l'expose — sans documenter d'où
il vient.

L'URL sur laquelle la comparaison initiale s'appuyait pour cette affirmation,
`pi.dev/models/basaten/deepseek-ai-deepseek-v4-1-flash-fast`, répond **404**. Une source
morte est une affirmation retirée, pas une affirmation plausible.

Ce qui existe, documenté :
- `deepseek-v4-flash` → **retiré**, route vers V4.1-Flash
- `deepseek-v4-pro` → route vers V4.1-Flash depuis le 14/09/2026 04:00 UTC, en attendant V4.1-Pro
- `deepseek-flash` → le nom d'API courant pour V4.1-Flash

Aucun « Fast », aucun palier de latence, aucun endpoint dédié dans la documentation DeepSeek.

## Analyse de problèmes
Sans documentation ni benchmark, il n'y a rien à analyser. L'écart de prix de 10/h
(40 % de plus) ne correspond à aucun produit identifié.

Trois hypothèses, aucune vérifiable depuis l'extérieur :
1. **Alias de la même API** avec une file d'attente ou une priorité différente. Le surcoût
   n'achète alors que de la latence, ce qui est legitimate à payer.
2. **Routeur de plateforme** : Freebuff sert V4.1-Flash via un fournisseur différent, plus
   cher et plus rapide, sous son propre label.
3. **Erreur d'affichage** : une entrée du catalogue qui n'a rien à voir avec DeepSeek.

La base locale ne permet pas de trancher : un seul thread utilise DeepSeek, configuré sur
`deepseek/deepseek-v4-flash`, et `metrics_json` ne contient aucune latence.

## Français
Sans objet : aucune information sur un modèle dont l'existence n'est pas établie.

## Avantages
Inconnu. Si l'hypothèse 1 est bonne, une latence garantie — mais c'est une hypothèse.

## Inconvénients
- **40 % de surcoût sur un produit non documenté.** C'est la seule chose qu'on sait.
- Acheter une qualité supérieure qui n'existe pas, ou une latence qui n'est pas mesurée.
- Le risque le plus probable, par principe : payer deux fois le même appel.

## Verdict pour ton budget

> ⚠ **CONDITIONNEL.** Le verdict ci-dessous dépend de la grille Freebucks/h, qui provient
> d'une capture d'écran et n'est corroborée par aucune source. Le ledger local
> (`state.json.session-refunds.json`, 20 entrées) journalise des *remboursements* à 0 et ne
> peut ni confirmer ni infirmer la grille. Voir `comparatif.md` § Budget.
**Ne l'achète pas tant que la question n'est pas tranchée.** 25/h contre 15/h, c'est 5 h 48 de
budget au lieu de 9 h 40 pour un modèle dont l'identité n'est pas établie.

Investigation I1, à faire tôt parce qu'elle est bon marché et décisive : trois prompts
identiques, un sur chaque endpoint, chrono sur le premier token et sur la fin. Relever
`inputTokens` et `outputTokens` des deux côtés depuis `metrics_json`.

Décisif si : tokens quasi identiques et latences du même ordre → même modèle, palier de
service, et le surcoût est inutile. Écart net de qualité → il y a deux services distincts et
il faut savoir lequel.

En attendant, **DeepSeek V4.1 Flash à 15/h est le bon choix** : mesuré, documenté,
209 tok/s, et la seule limite qu'on puisse lui reprocher est la non-hallucination à 3,5 %.

## Sources
- `pi.dev/.../deepseek-v4-1-flash-fast` → **HTTP 404**, contrôlé le 2026-10-05
- https://www.deepseek.com/en/news/deepseek-v4-1-flash/ (liste des endpoints, aucun « Fast »)
- https://api-docs.deepseek.com/news/news260910
- Base locale : `~/.config/freebuff-desktop/projects/*/desktop-v2.db`
