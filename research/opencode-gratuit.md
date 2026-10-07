# OpenCode — qu'est-ce qui est gratuit, quelle source le prouve

> P5 (mini-passe d'exploration) + P7 (recoupement des 25). Vérifié le **2026-10-07**.
> Protocole : MnemoLite d'abord → P5 cache miss → vérification web tier1 ; P7 mem-first
> (hit sur P5) puis 3 vérifications nouvelles (dataset brut, endpoint opérateur, descriptions).
> Les deux pages ont été téléchargées dans le cache du moteur (`moteur/cache/opencode/2026-10-07/`),
> sha1 figés ci-dessous — re-vérifiables par `python3 moteur/engine.py --platform opencode fetch`.

## Verdict

**Oui, OpenCode propose des modèles gratuits, sur deux niveaux de preuve différents :**

1. **Lane « free » documentée** (doc officielle Zen) : **13 modèles à 0 $** (input, output
   et cached-read), mais **« for a limited time »** — c'est une promo/campagne, pas un
   engagement permanent.
2. **Catalogue provider à prix 0.00** : **38 modèles** affichés `$0.00 / $0.00` sur
   `models.opencode.ai` — plus large que la lane documentée. Un prix 0.00 au catalogue
   ≠ lane free documentée : à traiter comme signal, pas comme contrat.

## Source 1 — lane free (tier 1, officielle)

**`https://opencode.ai/docs/zen/`** — HTTP 200, 109 235 o,
sha1 `4d6e261781510c1f7634c2b8091039abfa593f69`, fetch 2026-10-07T09:06:30Z.

- Le tableau de prix Zen (« We support a pay-as-you-go model. Below are the prices per 1M tokens »)
  contient **13 lignes `Free | Free | Free`** :

  | # | Modèle | Particularité |
  |---|--------|---------------|
  | 1 | Big Pickle | stealth model |
  | 2 | Space Bunny Free | stealth, **zero-retention** |
  | 3 | LongCat 2.5 Preview Free | **zero-retention** |
  | 4 | Exo Free | — |
  | 5 | Fledge Alpha Free | — |
  | 6 | MiMo-V2.6-Flash Free | — |
  | 7 | MiMo-V2.5 Free | — |
  | 8 | Ling 3.1 Flash Free | — |
  | 9 | Ling 3.0 Flash Fin Free | — |
  | 10 | Nemotron 3 Ultra Free | **NVIDIA trial-only** |
  | 11 | Nemotron 3.5 Lightning Free | **NVIDIA trial-only** |
  | 12 | Muse Spark 1.3 Contributor Free | prompts utilisés pour améliorer le modèle |
  | 13 | Jev 1.13 Free | input Free, output `-` |

- Hybride : **Jev 1.13** (sans suffixe) = input `$0.042`, output `Free`.
- Citation du bloc conditions : *« … is available on OpenCode for a limited time. The team is
  using this time to collect feedback and improve the model. »* ; pour Space Bunny Free et
  LongCat 2.5 Preview Free : *« Its provider follows a zero-retention policy and does not use
  your data for model training. »* ; pour Nemotron : *« NVIDIA free endpoints: Trial use only —
  do not submit personal or confidential data. »*
- Ancre de santé du moteur : `The free models` (présent dans la page).

## Source 2 — catalogue provider à 0.00 (tier 1, officiel)

**`https://models.opencode.ai/providers/opencode`** — HTTP 200, 939 509 o,
sha1 `a6dc966251e876ed4dc702fd0e8ee626cee82d33`, fetch 2026-10-07T09:06:30Z.

**38 lignes `$0.00 / $0.00`**, dont les 13 de la lane free + 25 supplimites :
`big-pickle`, `deepseek-v4-flash-free`, `exo-free`, `fledge-alpha-free`, `glm-4.7-free`,
`glm-5-free`, `grok-code`, `hy3-free`, `hy3-preview-free`, `jev-1.13-free`,
`kimi-k2.5-free`, `laguna-s-2.1-free`, `ling-2.6-flash-free`, `ling-3.0-flash-fin-free`,
`ling-3.1-flash-free`, `ling-3.0-flash-free`, `ling-3.0-tiny-free`,
`longcat-2.5-preview-free`, `longcat-2.0-free`, `mimo-v2-flash-free`, `mimo-v2-omni-free`,
`mimo-v2-pro-free`, `mimo-v2.5-free`, `mimo-v2.6-flash-free`, `minimax-m2.1-free`,
`minimax-m2.5-free`, `minimax-m3-free`, `muse-spark-1.2-contributor-free`,
`muse-spark-1.3-contributor-free`, `nemotron-3-super-free`, `nemotron-3-ultra-free`,
`nemotron-3.5-lightning-free`, `north-mini-code-free`, `x-preview-f-free` (Ox Alpha Free,
Unlimited), `qwen3.6-plus-free`, `ring-2.6-1t-free`, `space-bunny-free`,
`trinity-large-preview-free`.

> Les 25 en surplus ne figurent **pas** dans le bloc « The free models » de la doc Zen :
> leur gratuité est affichée par le catalogue mais non documentée comme campagne.
> **Recoupement requis** (règle du projet : un chiffre = 2 sources) → fait en P7,
> voir « Recoupement P7 » ci-dessous (résultat : 1 promotion sur 25).

## Recoupements locaux

- `~/.cache/opencode/models.json` (catalogue opencode local, 226 providers) : providers
  `opencode` et `opencode-go` présents ; 698 modèles à `cost 0` **tous providers confondus**
  (groq, zai, poe, alibaba-token-plan…) — ce chiffre n'est **pas** propre à la lane OpenCode.
- Projet llm-compare : `research/verdict.md:144` (space-bunny-free OpenCode) et
  `research/signaux-faibles.md:201` (« best free model available on OpenCode »)
  sont cohérents avec la lane documentée ; freebuff.com expose d'ailleurs les mêmes
  modèles (`space-bunny-alpha` retiré côté freebuff le 06/10, toujours listé free côté Zen le 07/10).

## Recoupement P7 — les 25 surplus (2026-10-07, mem-first puis web)

Mémoire d'abord : `b080a388` (P5) couvrait le constat, pas la preuve → cache miss →
trois vérifications du jour :

1. **Dataset brut `https://models.dev/api.json?type=all`** (5 338 903 o, sha1
   `49006e0b0b`) : provider `opencode` = **38 modèles avec `cost` explicite
   `{input:0, output:0}`, 0 avec `cost` omis** — alors que 446 modèles omis existent
   ailleurs dans le dataset. L'« $0.00 » du catalogue n'est donc **pas** le piège
   « cost omis = $0 » documenté par anomalyco/opencode#29971 (*Model cost shows $0
   when provider omits cost*) : c'est un zéro déclaré.
   *Limite : models.dev et models.opencode.ai partagent l'origine (org anomalyco) —
   deux rendus d'**une** source, pas deux sources.*
2. **Endpoint opérateur `https://opencode.ai/zen/v1/models`** (HTTP 200, 7 232 o,
   sha1 `147abc76c5ba`) : **86 ids servis** sans auth.
   - 12/13 lane servis — **`mimo-v2.5-free` absent** : dérive doc/API signalée.
   - **1 seul surplus y figure : `muse-spark-1.2-contributor-free`.**
   - Sémantique : 8/9 payants absents sont des « Legacy model retained for
     compatibility » → l'endpoint exclut l'hérité ; absence = « non servi ce jour »,
     pas retrait définitif (contre-exemple : claude-opus-4-1, non legacy, absent).
3. **Descriptions du dataset** : 15 des 25 = legacy ; 10 en description « live ».
   Parmi les 10, seul muse-spark-1.2 est servi ; deepseek-v4-flash-free, hy3-free,
   laguna-s-2.1-free, ling-3.0-flash-free, ling-3.0-tiny-free, longcat-2.0-free,
   nemotron-3-super-free, north-mini-code-free, x-preview-f-free affichent 0.00 mais
   ne sont **pas servis ce jour**.

Corroboration tier 3 (pas une preuve) : codeagentswarm.com (2026-08) traite DeepSeek
V4 Flash Free / MiMo-V2.5 Free comme gratuits ; zen.mdx historique (anomalyco/opencode)
et frank.dev.opencode.ai montrent des lanes passées incluant Kimi K2.5 Free /
MiniMax M2.5 Free / Nemotron 3 Super Free → **les campagnes free tournent**.

### Décision P7 (règle à 3 observations du jour)

Promotion ssi **les trois** concordent : (a) catalogue `$0.00 / $0.00`, (b) dataset
`cost` explicite 0/0, (c) servi par `/zen/v1/models`. Preuve = **tier 2** (aucun
contrat docs), `promo: false` (aucune campagne documentée) — rendu « 0 » à côté des
« 0 promo » de la lane.

| Groupe | N | Décision |
|---|---|---|
| Lane documentée | 13 | déjà en état (P6, tier 1, promo true) |
| `muse-spark-1.2-contributor-free` | 1 | **promu** (tier 2, promo false) |
| Legacy « retained for compatibility » | 15 | reste signal catalogue, pas d'état (non servis) |
| Live mais non servis ce jour | 9 | reste signal, pas d'état (disponibilité échoue) |
| `mimo-v2.5-free` (lane) | 1 | en état (docs) + **à vérifier** : non servi API |

État final : **14 modèles**. Vigie quotidienne : gate `zen_catalog` (RETRAIT prix /
RETRAIT catalogue structurels ; CONFLIT de sources → « à vérifier ») + gate `v1_models`
(non servi → « à vérifier » ; modèle 0.00 **et** servi hors état → problème **PROMOTION**,
jamais appliqué automatiquement).

### Dérive mimo-v2.5 (recoupée en P8, 2026-10-07)

`mimo-v2.5-free` documenté dans la lane Zen du jour **et** absent de `GET /zen/v1/models`
du jour (seul `mimo-v2.6-flash-free`, sorti 2026-09-22, y figure) → **dérive côté
opérateur confirmée** : docs périmés au moins depuis fin août (issues ouvertes
#45132 — 403/429 **sélectifs par clé depuis ~mi-juillet** — et #45291 du 26/08 « unavailable
for several days »), routeur Go amputé de MiMo (blog flabs.tech 17/09, « trust the router »).
Décision inchangée : reste en état (contrat docs), verify permanent, **retraite définitive
non prouvable** de l'extérieur (indisponibilité historiquement sélective, pas d'auth pour
sonder `chat/completions`) — le flag se lève seulement si l'opérateur bouge.

## État du pipeline (P5 + P6 + P7)

- `moteur/adapters/opencode.json` : health = zen docs (ancre `The free models`),
  3 sources : `zen_docs` (lane), `zen_catalog` (prix), `zen_served` (`/zen/v1/models`).
- `moteur/state/opencode.json` : **14 modèles** — 13 lane (P6, tier 1, `0 promo`) +
  muse-spark-1.2 (P7, tier 2, `0`, promo false).
- Boucle quotidienne prouvée : `fetch --revalidate` → `diff` → `apply` ; état stable =
  1 seul « à vérifier » debout (`mimo-v2.5-free` non servi) ; retrait / format mangé /
  promotion candidat signalés, jamais appliqués.
- Cache dédié : `moteur/cache/opencode/` (jamais partagé avec freebuff).
