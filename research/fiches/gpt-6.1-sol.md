# GPT-6.1 Sol — OpenAI
<!-- GEN:prix|run=2026-10-07 -->
**Sur Freebuff :** 🔒 FR = payant (gratuit aux US)
<!-- /GEN -->

> Ajoutée en **passe 8 (I10)** : ce modèle était **dans le catalogue Freebuff, absent de mes
> douze**. `Access = US, or paid plans elsewhere` → **en France, il est payant.**

## Identité
Ouverture de release : **2026-09-29** — il a **remplacé GPT-6 Sol après 7 jours** de service
(artificialanalysis.ai, *« GPT-6.1 Sol replaces GPT-6 Sol after just 7 days, with near-Astra
intelligence »*). **1M de contexte, images** (GitHub README). Texte + image.

**Accès (GitHub README) : `US, or paid plans elsewhere`** — *« OpenAI's flagship at a
**temporary promotional price**, **one session a day for every account** »*.
`freebuff.com/plans` : **1 h/jour sur Starter** (2,60 $/j) → **2,60 $/h**, le plus cher du
catalogue. Badge **`Promotional`**.

**Ce que le code ajoute (passe 10, source primaire `common/src/constants/freebuff-sol-promo.ts`,
lu 2026-10-07)** — le bandeau exact que voit l'utilisateur :

> *« Free in the US, a paid plan elsewhere, until the promotion ends. One session a day on
> every plan. »*

et dans `freebuff-models.ts` : *« **FREE TO US VIEWERS and paywalled for everyone else** … at a
**PROMOTIONAL 100 Freebucks** — the most expensive row we have offered outside the Fable
campaign »*. La limite d'**1 session/jour** n'est pas une clause commerciale : elle est
**enforcée côté admission** (`FREEBUFF_DAILY_SESSION_LIMITS`, débit journalier non
remboursable), donc elle tient **sur toutes les surfaces et contre les démarrages parallèles**.

## Puissance — **relation connue, valeur non collectée**
AA : *« il score **1 point sous GPT-6 Astra** sur l'Intelligence Index, à **moins du quart de
son coût par tâche** »*. Je **n'ai pas relevé les valeurs absolues** — donc aucune ligne
exploitable dans `comparatif.md`.

## Coût
2,60 $/h sur Starter ; badge `Promotional` → **prix temporaire**. Freebucks : **100 FB
promotionnels** pour qui y a accès (le plus cher jamais servi hors campagne Fable), **0 pour
les spectateurs US** — et **en France : payant, 1 session/jour**.
Côté upstream, OpenRouter flex : **1,00 $ in / 0,05 $ cache / 5,00 $ out** par 1M — 20x
GPT-6 Luna sur input frais. L'effort est **plafonné à `high`** par décision produit
(2026-09-29) parce que le raisonnement se facture en output à 5 $/M.

## Français
**Aucune donnée collectée.**

## Avantages
- Flagship OpenAI dans le catalogue, 1M de contexte + images.
- Rapport intelligence/cost-per-task déclaré excellent par AA (vs GPT-6 Astra).

## Inconvénients
- **Inaccessible en France sans abonnement.**
- **Prix promotionnel temporaire** — peut bouger, comme Solar Pro 4.
- **Zéro valeur d'index relevée** : non comparable aujourd'hui.

## À faire
1. Récupérer l'index AA et le coût par tâche exacts (l'article existe, je n'ai pas les
   chiffres) — **échéance : avant tout arbitrage**.
2. ~~Vérifier si l'offre gratuite US s'étend~~ — **résolu passe 10** : le périmètre est écrit
   dans le code, *« Free in the US, a paid plan elsewhere »* ; il ne s'étend pas.

## Sources
- GitHub `CodebuffAI/freebuff` **`common/src/constants/freebuff-sol-promo.ts`** — **primaire,
  lu 2026-10-07** : tooltip *Free in the US, a paid plan elsewhere*, `FREEBUFF_DAILY_SESSION_LIMITS = 1`
- GitHub `CodebuffAI/freebuff` **`common/src/constants/freebuff-models.ts`** — **primaire,
  lu 2026-10-07** : *FREE TO US VIEWERS*, prix promotionnel **100 Freebucks**, prix upstream
  OpenRouter flex, effort plafonné à `high`
- `artificialanalysis.ai/articles/gpt-6-1-sol-replaces-gpt-6-sol-after-just-7-days-...` —
  **tier 1, 2026-09-29** (relation vs Astra, 7 jours de service)
- GitHub `CodebuffAI/freebuff` README — **primaire, relu 2026-10-07** : `US, or paid plans
  elsewhere`, *temporary promotional price*, *one session a day*, 1M context, images
- `freebuff.com/llms.txt` — **primaire, relu 2026-10-07** : « GPT-6.1 Sol: OpenAI flagship. »
- `freebuff.com/plans` — **primaire, relu 2026-10-07** : 1 hr, badge `Promotional`

Journal : `research/trace.md` § Passe 8. Catalogue : `research/investigations.md` § I10.
