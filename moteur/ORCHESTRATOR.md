# ORCHESTRATOR — moteur d'investigation (Freebuff, opencode, …)

Une page. Tout ce qui n'est pas ici n'existe pas.

## État (2026-10-07, P1+P2+P3+P4+P5+P6+P7+P8+P9+P10)

| Élément | État |
|---|---|
| `schema.json` | ✅ v1 |
| `engine.py` : `import` / `pair` / `migrate` / `check` / `render` / `show` / `lint` | ✅ — `check` prouvé sur comparatif **et** 14 fiches ; test négatif : prix corrompu dans une fiche → échec localisé, `render` répare ; section exigée retirée → `lint` échoue |
| `state/freebuff.json` | ✅ backfill + **appariement 14/14** (`fiche` renseigné) |
| Bloc `GEN:comparatif` | ✅ migré (2 lignes ajoutées, 0 ligne modifiée) |
| Bloc `GEN:prix` dans les 14 fiches | ✅ migré (**42 ajouts, 0 suppression**) |
| `templates/fiche-llm.md` | ✅ contrat de fiche (H1 == id slugifié, 5 sections exigées, 5 recommandées) ; `lint` vérifie que le template contient bien les exigées |
| `lint` actif | ✅ appariement bijectionnel, structure de fiche, prix fiche↔état, état interne. ⚠ **4 avertissements réels** (sections recommandées manquantes dans 4 fiches — relevé, pas bloqué) |
| `lint` §7 | ✅ P9+P10 : « déprécié ⇒ relecture claim gratuit » = **warn** (docs Zen ∩ état, pas d'NLP) ; `facts.index_version` **exigé** (`evidence.url`+`tier`) si fiches citent l'AA (saisi P9 : `v4.3.2` tier 1) ; §7-3 **err** : status=retired ⇒ aucune ligne **machine (GEN)** ne revendique gratuit (prose annotée exclue — faux positifs prouvés) ; best-of = **N/A** (pas une sortie §6) ; version = globale (`facts.index_version`), une seule version active |
| `adapters/freebuff.json` | ✅ 6 sources (5×tier 1 + RSS tier 2), health (llms.txt 200 + ancre), aliases, `label`/`model_map`/`research` ; **gate RSS P10** : dernier événement « withdrawn/replaced » du feed (tier 2) encore `live` dans l'état → « à vérifier » (jamais d'apply) — ping-pong géré (retrait→retour = aligné) |
| `adapters/opencode.json` + `state/opencode.json` | ✅ P5+P6+P7 : health = doc Zen (200 + ancre `The free models`), 3 sources (`zen_docs`, `zen_catalog`, `zen_served`), **14 modèles** = 13 lane (tier 1, `0 promo`) + muse-spark-1.2 (P7, règle 3 observations : catalogue 0.00 + dataset cost explicite + servi `/zen/v1/models`, tier 2, `0` non-promo) ; gates : retrait lane/prix/catalogue structurels, conflit → à vérifier, PROMOTION → problème manuel, **déprécié → à vérifier** (P9, table « Deprecated models » extraite des docs) ; dérive `mimo-v2.5-free` recoupée P8 (docs périmés, absent du v1, retraite non prouvée). Note : `research/opencode-gratuit.md` (recoupement P7 des 25 + dérive P8) ; mémoires `b080a388` + P6 + P7 `8de07a59` + P8 `c416a02a` |
| `fetch` / `diff` / `apply` | ✅ boucle quotidienne prouvée sur cache réel : fetch → diff exit 2 (24 auto, 0 structurel) → apply → diff exit 0 ; tests négatifs : retrait simulé = structurel **non appliqué** (status intact), format de source mangé = signalé. `fetch` réutilise le cache du jour, `--revalidate` force tout, `diff` refuse un cache ≥7 j et écrit `research/rapport.md` (sauf `--date`). Détection de dérive de sha1 = auto-op `sources` |
| Timer quotidien / hebdo | ✅ `moteur/timers/` (unités systemd --user) + `install.sh` installés : quotidien 06:17±15 min, hebdo dim. 07:23 — `timer.sh quotidien\|hebdo` (exit 2 du diff = normal pour une unité, vécu via `rapport.md`) |
| Engine paramétré par plateforme | ✅ P5 : `--platform <nom>` (défaut `freebuff`) rebind `STATE_PATH`/`COMPARATIF`/`FICHES_*`/`RAPPORT`/`HEADER`/`ALIGN`/libellé/`FN_KEY`/`model_map` depuis `adapters/<nom>.json` ; échec franc si l'adapter est absent ou si `platform` ≠ nom de fichier. Cache par plateforme : `moteur/cache/<plateforme>/AAAA-MM-DD/`. État vide géré (comptes, pas de faux problèmes ; `render`/`check` refusés sans comparatif) |

Sections 4 à 7 ci-dessous = **contrat** (ce que P3-P5 doivent livrer), pas l'état courant.

## 1. Split code / jugement

| | Qui | Ce que ça fait |
|---|---|---|
| **Déterministe** | `engine.py` (stdlib, zéro dépendance) | `fetch` des sources déclarées, parse, **`diff`** vs `state/*.json`, **`render`** des blocs `GEN`, **`lint`** de cohérence, `check` (comparaison du rendu au fichier existant) |
| **Jugement** | agent (skill + `source-verifier`) | recouper chaque diff sur Tier 1, décider `CONFIRME`/`REJETE`, écrire l'**annotation** humaine hors bloc, journal `trace.md`, write-back MnemoLite |

Jamais l'inverse. Un LLM ne rend pas un tableau ; du code ne conclut pas sur une preuve.

## 2. Règles inviolables

1. **Source de vérité = `state/<plateforme>.json`** (versionné dans git). Les markdown ne font que le rendre.
2. **Écriture machine uniquement dans les blocs balisés** :
   `<!-- GEN:id|run=AAAA-MM-JJ -->` … `<!-- /GEN -->`.
   Toute prose hors bloc est **humaine et interdite au moteur** (« annoter, jamais effacer »).
3. **Preuve** : Tier 1 requis pour publier un fait ; Tier 2 = déclencheur de vérification, jamais preuve ; Tier 3 = hypothèse étiquetée. Tout fait affiché porte `source + tier + date`.
4. **NO REGRESSION** : avant toute migration, `python3 moteur/engine.py check` doit rendre **à l'identique** les blocs existants. Écart = on ne migre pas, on corrige d'abord.
5. **Diff, pas ré-écriture** : un run ne re-valide que ce qui a changé, plus la revalidation hebdomadaire (`--revalidate`) des sources vieilles de >7 jours.

## 3. Pipeline

```
quotidien : timer --user → timer.sh quotidien = fetch → diff           [installé, 06:17±15 min]
apply     : diff non vide → recoupement Tier 1 (agent) → apply → render → check
            → lint → trace.md (append) → write-back mémoire            [après un diff non vide]
hebdo     : timer --user → timer.sh hebdo = fetch --revalidate → diff   [installé, dim. 07:23]
```

`engine.py [--platform <nom>] fetch|diff|apply|render|check|lint` — une entrée par phase.
`--platform` (défaut `freebuff`) sélectionne l'adapter, l'état et le cache ; les timers
parcourent toutes les plateformes déclarées et une plateforme peut aussi s'appeler à la main
(ex. `python3 moteur/engine.py --platform opencode diff`).
`diff` écrit `research/rapport.md` (diff du dernier run, si l'adapter déclare
`research.rapport`) sauf avec `--date` (runs de test/manuels) ; un cache de ≥7 jours
est refusé (problème → `fetch --revalidate`).
Pour une unité systemd, l'exit 2 du diff est un état normal : `timer.sh` le traduit en 0,
le détail vit dans `rapport.md`.
L'agent n'est appelé que si `diff` sort non vide **ou** en `--revalidate`.
`apply` n'applique que le sous-ensemble sûr (accès, allocations, sections, historique
prix, provenance sources/sha1) ; le retrait/d'une divergence = décision manuelle, listée, jamais appliqué.
`apply` refuse toute écriture si une source, une ligne ou une date d'observation est
invalide/incomplète ou si le cache est périmé. Les différences structurelles et les
signaux à vérifier restent affichés pour décision humaine.

## 4. Contrat adapter — ajouter un outil = ajouter un fichier

`moteur/adapters/<plateforme>.json` (JSON, pas YAML : l'engine est stdlib, zéro
dépendance, donc zéro parseur YAML) :

```json
{
  "platform": "freebuff",
  "label": "Freebuff",
  "model_map": { "FREEBUFF_SOLAR_PRO_4_MODEL_ID": "solar-pro-4" },
  "research": {
    "comparatif": "research/comparatif.md",
    "fiches": "research/fiches",
    "rapport": "research/rapport.md"
  },
  "health": {
    "url": "https://freebuff.com/llms.txt",
    "must_contain": "Freebuff"
  },
  "aliases": { "meta/muse-spark-1.3-contributor": "muse-spark-1-3" },
  "sources": [
    { "id": "llms",           "url": "https://freebuff.com/llms.txt", "tier": 1, "type": "llms_txt" },
    { "id": "picker_sections","url": "https://raw.githubusercontent.com/…/freebuff-picker-sections.ts", "tier": 1, "type": "picker_ts" },
    { "id": "feed_models",    "url": "https://…/feed-models.xml", "tier": 2, "type": "rss" }
  ]
}
```

- `platform` **doit** égaler le nom du fichier (`opencode.json` → `"platform": "opencode"`),
  sinon refus franc — le nom de fichier est l'identifiant plateforme.
- `label` = libellé affiché (colonne du comparatif, « Sur X : ») ; défaut = nom capitalisé.
- `model_map` = correspondances d'identifiants de source vers id d'état (ex. modelId solar).
- `research` = chemins relatifs à la racine projet ; clé absente ou `null` = la plateforme
  n'a ni comparatif, ni fiches, ni rapport → `import`/`render`/`check`/`pair`/`migrate`
  refusent proprement avec un message explicite.
- `health` : 200 + ancre `must_contain` obligatoires, sinon RUN ABORT (pas de diff partiel).
- `type` = fonction extractrice dans `engine.py` (`llms_txt`, `readme_md`, `picker_ts`,
  `solar_promo_ts`, `plans_html`, `rss`, `zen_docs` = lane free des docs Zen (Input=Free)
  + section « Deprecated models » (noms+dates, appariés à l'état),
  `zen_catalog` = prix du catalogue (ids normalisés, split 0.00/payant),
  `v1_models` = ids servis par `/zen/v1/models`) ;
  `raw` = collecte horodatée (sha1, fraîcheur) sans extraction ; type inconnu au
  chargement = refus franc (pas de sortie partielle).
  Chaque type d'extraction n'est déclaré qu'une fois par adaptateur.
- `id` source = identifiant de fichier sûr ; tier, URL HTTP(S), type, clés inconnues et
  doublons sont validés au chargement. Les chemins `research` restent relatifs à la racine
  du projet ; les liens symboliques qui sortent du projet sont refusés.
- `aliases` : noms de source non réductibles par normalisation -> id d'état.
- Cache : `moteur/cache/<plateforme>/AAAA-MM-DD/` — deux plateformes ne partagent jamais
  le même manifest. Chaque corps est nommé avec son SHA-1 ; le manifeste est remplacé
  atomiquement après les corps. `diff` et `apply` recalculent le SHA-1 avant parsing.

Rien d'autre à toucher pour un nouvel outil (IDE, CLI, …) : ni `engine.py`, ni templates.

## 5. Cadence (choix actés)

- **Quotidien** : `llm-compare-quotidien.timer` (systemd --user, 06:17±15 min) →
  `moteur/timer.sh quotidien` = **pour chaque plateforme déclarée dans
  `moteur/adapters/`** : `fetch` (réutilise le cache du jour) → `diff` (échec d'une
  plateforme n'empêche pas les suivantes, l'unité échoue au total).
  Exit 0 → rien ne se passe ; exit 2 → détails dans le rapport de la plateforme
  (`research.rapport`).
- **Hebdo** : `llm-compare-hebdo.timer` (dim. 07:23) → `timer.sh hebdo` = idem avec
  `fetch --revalidate` (re-télécharge tout, fraîcheur ≥7 j garantie).
- **Installation** : `sh moteur/timers/install.sh` (copie dans `~/.config/systemd/user/`,
  `enable --now`). Les unités du dépôt restent la source de vérité.
- **À la demande** : boucle `apply → render → check → lint` manuelle après un diff non vide.

## 6. Sorties produites

| Fichier | Propriétaire |
|---|---|
| `state/<plateforme>.json` | machine (bloc unique, tout le fichier) |
| `research/comparatif.md` § tableau | machine (bloc `GEN:comparatif`) |
| `research/fiches/*.md` § lignes `Sur <plateforme> :` | machine (bloc `GEN:prix`), annotations autour |
| `research/trace.md` | agent (append-only, format § Passe N) |
| `research/rapport*.md` | machine (diff du dernier run, par plateforme via `research.rapport`) |
| mémoire MnemoLite | agent (`status:CONFIRME`, `project:llm-compare`) |

Les fichiers écrits par le moteur passent par un fichier temporaire puis un remplacement
atomique. Un rendu multi-fichiers est préparé en entier avant le premier remplacement ;
`check` détecte une interruption entre deux remplacements.

## 7. Lint (échec = rapport, jamais de silencieux)

- prix d'une fiche == prix du comparatif == prix du `best-of` — **N/A** : le best-of
  n'est pas une sortie §6 (clos P10 ; se recâbler si un jour produit)
- tout modèle du comparatif a une fiche, et inversement (ou `hors cat.`)
- `status: retired` ⇒ aucune ligne machine (bloc `GEN`) ne dit « gratuit / disponible »
  — prose annotée hors GEN volontairement exclue (faux positifs prouvés : encadrés
  « verdict caduc », claims barrés `~~`)
- toute mesure porte `index_version` : version **globale** `facts.index_version` (P9) —
  une seule version active ⇒ « deux mesures sans même version » ne peut pas arriver
- tout fait affiché a `source + tier + date` ; dates ISO partout
