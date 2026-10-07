# Solar Pro 4 — investigation de fond

Date : 2026-10-06 (passe 7). Source primaire lue directement :
`artificialanalysis.ai/models/solar-pro4`, `freebuff.com/llms.txt`, GitHub `CodebuffAI/freebuff`.

---

## 1. Mon `42` était périmé — et le `28` actuel n'est pas mesuré

| | Index AA | version | statut | rang |
|---|---:|---|---|---|
| Article AA + communiqué Upstage (12/08) | **42** | v4.1.1 | mesuré | — |
| Page AA aujourd'hui | **28** | v4.3.2 | **estimé** | **#19 / 176** |

La page porte explicitement `28*` avec la mention **« Estimate (independent evaluation
forthcoming) »**. Conséquence directe : les courbes de détail de cette page renvoient toutes
**« Not publicly available »** — Intelligence, Cost per Task, Omniscience, Context Window.

**Solar Pro 4 est le seul des douze dont l'index est une estimation.** Les onze autres sont
mesurés. Sous ma règle C2 (effort non apparié → pas de classement opposable), Solar Pro 4
devrait en plus être **exclu du classement** : on ne compare pas une mesure à une projection.

C'est le même phénomène que GLM (57 → 42) vu à l'envers : ici **mon chiffre était le périmé**,
pas celui du web.

## 2. Le progrès vient de l'abstention, pas du savoir

| | Solar Pro 3 | Solar Pro 4 |
|---|---:|---:|
| Précision (Accuracy) | 19 % | **19 %** |
| Tentatives | 92 % | **41 %** |
| Hallucination | 88 % | **24 %** |
| Index AA-Omniscience | −53 | **−1** |
| Non-hallucination | — | 75,6 % |

**La précision n'a pas bougé d'un point.** Le modèle répond moins souvent et rate autant quand
il répond. En accuracy il reste **derrière** Command A+ (14 %) et MiniMax-M3 (18 %) sur les
échelles où il est classé, malgré un index d'Omniscience supérieur — parce que l'index
récompense l'abstention et pas l'exactitude.

C'est exactement l'objet de **I4** : sur tes tâches, se taire est-ce un gain (moins
d'hallucinations à relire) ou un blocage (une réponse refusée) ? Le protocole I4 n'a pas été
exécuté ; ce dossier n'y répond pas.

## 3. Le détail des benchmarks est daté — je ne le mets plus dans le tableau

Chiffres publiés au lancement, donc sur **v4.1.1** :

| Benchmark | valeur | réserve |
|---|---:|---|
| Terminal-Bench **4.0** | 0,5 % | source OpenRouter, pas AA |
| Terminal-Bench 2.1 | 57,3 % | autre version — non comparable au 4,0 |
| Humanity's Last Exam | 29,2 % | époque lancement |
| GPQA Diamond | 89,1 % | époque lancement |
| SWE-bench Verified | 70,6 % | **vendeur**, pas tiers |
| CritPt | 5,4 % | — |
| GDPval-AA v2 | Elo 1276 | conflictuel : 38,8 / 30,5 ailleurs |
| AA-LCR | 71 | — |

Le passage **57,3 % (TB 2.1) → 0,5 % (TB 4.0)** est le plus brutal du dossier, mais c'est un
changement de benchmark, pas une chute du modèle. **Aucun de ces chiffres ne doit figurer
dans un tableau dont l'en-tête dit v4.3.2.**

## 4. Vitesse et contexte : trois sources, trois chiffres — et une correction

- **Vitesse** : la page AA dit aujourd'hui **115,1 tok/s** (`#61/176`, médiane 112,
  *above average*), TTFT **1,91 s**. Ma note de travail portait **99 tok/s** : **c'est faux,
  corriger**. (Mesuré sur l'API Upstage.)
- **Contexte** : AA **512k** en tête de page, **510k** dans sa propre FAQ — le même site se
  contredit de 2k. Upstage 512K. **Freebuff README : 524K.** L'article AA de lancement parlait
  de **384k effectifs**. À retenir pour le projet : **524K**, c'est ce que sert Freebuff.
- **Modality** : **text only**, pas d'images. Confirmé AA + Freebuff.
- **Langues** : EN / KR / JA. **Ni chinois, ni français.**
- Poids et nombre de paramètres : **non divulgués**. Propriétaire.
- Une variante **non-reasoning** existerait peut-être (AA : « A non-reasoning variant may
  also exist ») — non vérifiée.
- Prix : **0,30 $/M in, 1,20 $/M out**, cache −80 %, blendé 0,22 $/M (7:2:1).
- Promotion : −90 % jusqu'au 10/09, **−70 % (0,09 $/0,36 $) jusqu'au 09/10/2026**, plein le
  10/10. **La promotion expire dans 3 jours.**

## 5. Signal social : « zéro signal » était faux — correction d'I9

Mon `signaux-faibles.md` affirme : *« Solar Pro 4 et Solar Mini 4 : zéro signal social »*.

- **HN : confirmé vide.** C'est la seule partie juste.
- **Reddit existe** : `r/opencodeCLI`, 2026-08-07 — *« Solar Pro 4 by Upstage.ai is now on
  OpenCode »*, *« not even featured on their official website »*, *« on par with popular
  chinese open source models »*.
- **ARENA.AI** (ex-LMArena) : rang **44**, à égalité avec MiniMax M2.7 et Nemotron 3 ; première
  entreprise coréenne dans le haut de tableau ; **point faible : la récupération d'erreur**.
- **Critique coréenne** du set de comparaison d'Upstage : graphiques bornés aux « open models
  sous 320B » et au « fast-tier », top commercial exclu (légende honnête, comparaison
  flatteuse).
- **`freebuff.com/live`** : Solar Pro 4 = **253 utilisateurs simultanés**, 5ᵉ des douze —
  devant GPT-6 Luna (142), Solar Mini 4 (115), MiMo 2.6 Pro (72), Muse Spark 1.3 (23),
  Gemini 3.8 Flash (6). Compteur en direct, non archivé : à re-vérifier avant citation.

**Ce que ça change** : Solar Pro 4 n'est pas invisible, il est **absent de HN** et présent
sur Reddit et dans l'arène coréenne. Une absence de critique sur un canal n'est pas une
absence de défaut — mais ma formulation « zéro signal » était une généralisation abusive.

## 6. Test indépendant : CrucibleMark signale un défaut disqualifiant

`cruciblemark.com/reports/solar-pro4/review/` (tier 2, test indépendant) :

- 75,42 % global, rang **#33**
- **« Tool use hallucination » — qualifié de *disqualifying signal***
- **P95 95,33 s — qualifié de *Problematic*** ; 36,59 tok/s
- timeout 2/49 — *Sporadic*
- *« no switchable mode exists in this test »* — pas de mode « non-reasoning » à activer
- sovereignty risk : **MEDIUM**

Le P95 est cohérent avec les 8,6 min/tâche d'AA contre 6,0 pour Pro 3 : **Solar Pro 4 est plus
lent que son prédécesseur avec moins de tokens de sortie** (43k vs 52k).

## 7. Sur Freebuff : statut confirmé, tarif confirmé — mais promotionnel

**Confirmé par source primaire :**

- `freebuff.com/llms.txt` : *« Solar Pro 4: Upstage flagship »*, dans le picker **full mode**,
  **et** en **limited mode** avec **6 sessions d'une heure par jour**.
- GitHub README : *« Solar Pro 4 — Upstage's larger, stronger model; **524K context, text
  only** »*, accès *Full and limited access*.
- GitHub README : Solar Pro 4 fait partie des cinq modèles **« unmetered at full access and
  cost no session at all »** (avec GLM 5.3 Flash, DeepSeek V4.1 Flash, MiMo 2.6 Flash,
  Solar Mini 4).
- `freebuff.com/plans` (**ajouté en passe 8**) : **`∞ Unlimited hrs — Solar Pro 4`**, badge
  **`Promotional`**. Corroboration de ma capture à 0/h.

| source | statut | tarif Solar Pro 4 |
|---|---|---:|
| ma capture d'écran (tier 3) | — | **0/h** ✓ |
| `freebuff.com/plans` (**primaire**) | Starter | **`∞ Unlimited`** ✓ |
| GitHub README (primaire) | full access | « cost no session at all » ✓ |
| **GitHub `common/src/constants/freebuff-solar-promo.ts` (primaire, lu 2026-10-07)** | — | **historique complet des prix, voir ci-dessous** |
| Changelog `freebuff-changelog.nordicnode…` (tier 2) | — | **entrée en gratuit le 05/10/2026** |
| `mvalentsev.github.io` (tier 3, lu 2026-10-01) | — | **10/h** ✗ contredit |

**Le conflit est levé : 0/h est confirmé par deux sources primaires indépendantes.** La source
qui donnait 10 FB/h était de toute façon périmée (elle annonce « 100/70/40 », alors que
`llms.txt` dit **150/105/60**) — ses prix avec.

**Historique officiel des prix (passe 10, source primaire `SOLAR_PRICE_CHANGES`)** — le fichier
du dépôt public *liste* chaque bascule, avec horodatage :

| à partir de | prix | note |
|---|---:|---|
| 2026-09-05 | **0** | *Labor Day weekend (through Sep 7 PT)* |
| 2026-09-08 | 5 | retour en payant |
| 2026-09-09 15:49Z | **0** | *0 Freebucks* |
| 2026-09-13 05:00Z | 5 | « Metered again » |
| 2026-09-14 03:46Z | 10 | tagline *Limited-time trial* |
| 2026-09-25 19:00Z | 10 | retour en picker, *Upstage flagship* |
| **2026-10-05 07:15Z** | **0** | **promotion, « no end date yet »** |

Le code dit textuellement : *« A promotion with no end date yet. End it by appending a
transition back to `SOLAR_PRO_4_OFFER` and dropping the catalog row's `promotional` »*.

**Date d'entrée, ajoutée en passe 9 :** Solar Pro 4 n'a *toujours* pas été gratuit. Ajouté le
2026-08-28 en *limited-time trial*, retiré le 09-23, ré-ajouté le 09-25, puis **passé de la
section `optimized` à la section `unlimited` le 05/10/2026** (*« free as a promotion »*).
Le 0/h a donc **quelques jours**, pas des mois.

> ✅ **CORRECTION (passe 10, 2026-10-07)** — l'affirmation suivante, publiée en passes 7 à 9,
> **était fausse** : *« la promotion Upstage (−70 %) se termine le 09/10/2026 ; à re-vérifier
> le 10/10 »*. Cette échéance concernait **l'offre API Upstage**, pas le prix Freebuff. Le prix
> Freebuff est un choix produit **sans aucune date de fin** (cf. `SOLAR_PRICE_CHANGES`).
> Le badge `Promotional` reste posé, mais il ne présage **pas** d'une échéance datée.
> **Ce qui reste vrai :** c'est une promotion, elle peut se terminer par un commit, à tout
> moment — simplement on ne sait pas quand.

**Note de cohérence :** `llms.txt` dit *« Freebucks buy one-hour model sessions »*, alors que
le README appelle cinq modèles *« unmetered »*. Les deux se concilient : *unmetered* = **ne
consomme pas la session allouée** ; la page `/plans` montre elle que GLM, DeepSeek, MiMo Flash
et Solar Mini ont des **heures finies**. C'est **deux compteurs différents** (sessions vs
Freebucks) — ce que ma grille §6 confondait.

**Ce qui est confirmé et utile au budget :** `llms.txt` fixe la **France à 60 Freebucks/jour**
(full access, pays éligible). Ta prémisse « 60/jour » est donc **validée par la source
primaire** — et la France est en mode **full**, pas limited.

## 8. Finding collatéral : mon catalogue de douze a dérivé — **traité en I10**

Le picker `llms.txt` actuel contient **Gemini 3.8 Flash** et **GPT-6.1 Sol**, et ne contient
**ni Ling 3.1 Flash, ni Laguna S 2.1**. Le changelog de `mvalentsev` enregistre **cinq
changements de catalogue en trois semaines** (09-16, 09-22, 09-23, 09-25, 09-29).

`llms.txt` prévient lui-même : *« Available models depend on your app and access level; check
your model picker for the current selection. »*

→ **Résolu en passe 8 (investigation I10)** : `comparatif.md` a corrigé les deux lignes fausses
et ajouté les deux manquantes. **Reste** : les benchmarks de Gemini 3.8 Flash et GPT-6.1 Sol.

## 9. Verdict provisoire

1. **Ne pas classer Solar Pro 4.** Index **estimé** (28), effort non documenté, détails non
   publics : c'est le modèle le moins bien établi des douze, et pourtant l'un des mieux notés.
2. **Son gain est de l'abstention**, pas de la compétence. À transformer en question mesurable
   (I4) avant toute recommandation.
3. **Le test indépendant signale une hallucination d'outil** — le défaut le plus coûteux pour
   un agent qui exécute des commandes. C'est plus grave que l'index.
4. **Statut Freebuff confirmé, prix confirmé en passe 8.** 60 FB/jour en France confirmé, et
   **0/h corroboré par deux sources primaires** (`/plans` = `∞ Unlimited` + README).
5. **Mais le 0/h est `Promotional` — sans échéance.** ✅ corrigé en passe 10 : la promo
   Upstage (−70 %) finissant le 09/10 **ne concerne pas ce prix**. Le 0/h Freebuff est une
   promotion **open-ended depuis le 05/10** (`SOLAR_PRICE_CHANGES`, primaire). Elle peut
   se terminer par un commit, **mais personne ne sait quand** — et l'historique montre que
   ce prix a déjà basculé **6 fois en un mois**.

---

## Sources

- `artificialanalysis.ai/models/solar-pro4` — **primaire, lue le 2026-10-06** (28 estimé,
  #19/176, 115,1 tok/s, TTFT 1,91 s, 512k/510k, 0,30 $/1,20 $, text only, 2026-08-06)
- `freebuff.com/llms.txt` — **primaire, lu le 2026-10-06** (picker, limited mode 6 sessions,
  allocations 150/105/60/25/20)
- `freebuff.com/plans` — **primaire, relu le 2026-10-07** (`∞ Unlimited hrs Solar Pro 4`,
  badge `Promotional`, heures/jour des **11** modèles)
- GitHub `CodebuffAI/freebuff` — **primaire, lu 2026-10-07** : README (524K text only,
  *unmetered at full access*, *DeepSeek V4 Pro retired*) et
  **`common/src/constants/freebuff-solar-promo.ts`** (`SOLAR_PRICE_CHANGES`, historique des
  prix daté, promo *open-ended* depuis 2026-10-05)
- `artificialanalysis.ai/articles/upstage-solar-pro-4` — 12/08, v4.1.1 (42, Omniscience,
  latence)
- `upstage.ai/blog/ko/solar-pro-4`, `console.upstage.ai/docs/models/solar-pro4`
- `cruciblemark.com/reports/solar-pro4/review/` — tier 2, test indépendant
- `mvalentsev.github.io/awesome-free-ai-coding/providers/freebuff/` — tier 3, lu 2026-10-01,
  **allégations d'allocation périmées**
- Reddit `r/opencodeCLI` (2026-08-07) via tier 3 — API directe en 403
- `freebuff.com/live` — compteur en direct, non archivé

Journal : `research/trace.md` § Passe 7 et 8. Tableau : `research/comparatif.md`.
Catalogue : `research/investigations.md` § I10.
