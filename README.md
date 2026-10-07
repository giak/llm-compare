# llm-compare

Comparer les **11** modèles LLM exposés par Freebuff (12 jusqu'au retrait de Space Bunny
Alpha le 2026-10-06) — et l'offre gratuite d'**opencode** — sur des faits vérifiés plutôt
que sur des badges.

- **Vision** : [`vision.md`](vision.md)
- **Moteur (page unique)** : [`moteur/ORCHESTRATOR.md`](moteur/ORCHESTRATOR.md)

## Le problème

La plateforme affiche un prix en Freebucks/h et un badge « Recommended ». Aucun des deux ne
dit quoi que ce soit de la qualité. Le seul signal indépendant disponible est Artificial
Analysis (coût par tâche, tokens par tâche, latence par tâche). Le reste est constructeur.
Et le terrain bouge : retraits, dépréciations, promotions — une comparaison figée ment.

## Recherche — `research/`

| Fichier | Contenu |
|---|---|
| `research/comparatif.md` | **Le tableau des 14** (11 live Freebuff, Space Bunny Alpha retiré le 06/10, Ling + Laguna `hors cat.`) sur l'index AA commun + budget |
| `research/fiches/` | 14 fiches, bijection vérifiée avec l'état (H1 + sections exigées) |
| `research/verdict.md` | La comparaison, les corrections, ce qui est prouvé / non prouvé |
| `research/trace.md` | Journal append-only des vérifications (22 sections, auto-revue adversariale) |
| `research/investigations.md` | Hypothèses testables localement dans Freebuff |
| `research/i0-francais.md` | **I0 : mesure locale du français + les 10 prompts contrôlés** |
| `research/signaux-faibles.md` | **I9 : ce qui se dit de ces LLM sur HN/Reddit, hors benchmarks** |
| `research/solar-pro-4.md` | **Investigation de fond Solar Pro 4 : index estimé, 0/h confirmé mais promotionnel** |
| `research/veille.md` | **Veille : sources à surveiller, explications à écrire, tips prouvés** |
| `research/opencode-gratuit.md` | **Offre gratuite opencode : docs vs service opérateur, divergences suivies** |
| `research/rapport.md`, `research/rapport-opencode.md` | Rapports de la boucle quotidienne (constats + signaux à vérifier) |

## Moteur — `moteur/`

Un moteur d'observation maintient la recherche vraie dans le temps (P1→P10) :

| Élément | Rôle |
|---|---|
| `moteur/ORCHESTRATOR.md` | Page unique : règles, état, lint §7 — « tout ce qui n'est pas ici n'existe pas » |
| `moteur/engine.py` | `import / pair / migrate / fetch / diff / apply / check / render / show / lint` |
| `moteur/schema.json` | Contrat de l'état (v1) |
| `moteur/adapters/` | `freebuff.json` (6 sources : 5×tier 1 + RSS tier 2) et `opencode.json` (3 sources Zen) |
| `moteur/state/` | États versionnés + faits datés (`facts.index_version = v4.3.2`…) |
| `moteur/templates/` | Contrat de fiche (sections exigées / recommandées) |
| `moteur/timer.sh` + `moteur/timers/` | Boucle systemd `--user` : quotidien 06:17±15 min, hebdo dim. 07:23 |

**Boucle :** `fetch` (cache du jour) → `diff` (exit **0** = rien / **2** = à vérifier /
**1** = lint) → `apply` (écriture datée) → `render` → `lint §7`.

**Signaux debout** (« à vérifier », jamais auto-applis) : `mimo-v2-5-free` côté opencode
(divergence docs/service), « retrait RSS non répercuté » côté freebuff (gate P10).

## Règles de preuve

1. Un chiffre constructeur est étiqueté `constructeur`, jamais mélangé à un chiffre tiers.
2. Un score n'est comparable qu'à **version de benchmark identique**. Terminal-Bench 2.1 ≠ 4.0.
3. Une source morte est une source morte : `404` = affirmation retirée, pas « plausible ».
4. Le prix Freebuff est un prix de plateforme. Il ne prédit pas le coût par tâche.
5. Un signal tier 2 (RSS, documentation datée) déclenche un recoupement humain,
   jamais une écriture automatique.
6. Un échec `lint` est un rapport, jamais un silencieux.

## Données Freebuff (local, read-only)

```
~/.config/freebuff-desktop/projects/<projet>-<uuid>/desktop-v2.db
```

`messages.metrics_json` contient `usage` (input/cached/output/total), `costUsd`,
`context` (usedTokens, windowTokens, compactionThresholdTokens) et `compactions`.
`threads.model` + `threads.reasoning_effort` donnent le modèle et l'effort.

**`messages.parts_json` est une liste de parts, chacune avec un champ `kind`.** Mesures
observées : `tool` 17838, `reasoning` 9960, `text` 9841, `ad` 2144, `changes` 394,
`notice` 19, `compaction` 80. **Toute mesure sur « la réponse de l'assistant » doit filtrer
`kind='text'`** — sinon elle mesure le raisonnement interne (anglais sur 13/15 prompts
français), pas ce que l'utilisateur voit.

`threads.model` porte 3 slugs lisibles et **un ID opaque** `m-22ff70c712` (9 threads,
296 messages), introuvable dans le catalogue local. Non attribuable aux 12.
Un autre ID, `m-00032eaeec`, **a été résolu** en passe 8 : `world_snapshot.model` →
`mimo/mimo-v2.5` (retiré du catalogue le 2026-09-22).

**Ce qui manque et qu'aucune source ne rattrape : la latence.** Freebuff ne l'enregistre pas.
C'est la raison pour laquelle les investigations existent.
