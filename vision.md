# Vision — llm-compare

**Ce que nous construisons :** une comparaison des offres de LLM **gratuites** qui reste
vraie dans le temps — sur des faits vérifiés et datés, jamais sur des badges.

## Le constat de départ

Une plateforme affiche un prix (Freebucks/h) et un badge « Recommended » : aucun des deux
ne dit quoi que ce soit de la qualité. Le seul signal indépendant disponible est un index
tiers (Artificial Analysis) ; tout le reste est constructeur. Et le terrain bouge vite :
modèles retirés (Space Bunny Alpha, 2026-10-06), modèles dépréciés côté docs ou côté
service, promotions qui vont et viennent — une comparaison figée ment déjà à J+7.

## Ce que le projet est

Trois couches, chacune avec un propriétaire clair :

| Couche | Rôle | Où |
|---|---|---|
| **Recherche** | Les faits établis : comparatif commun, fiches par modèle, verdict, journal append-only | `research/` |
| **Moteur** | Maintenir ces faits vrais : `fetch → diff → apply/verify → render → lint` | `moteur/` (page unique : `ORCHESTRATOR.md`) |
| **Mémoire** | Ce qui a été décidé/constaté, récupérable entre sessions (MnemoLite, write-back obligatoire) | mémoire `project:llm-compare` |

Le moteur observe des sources HTTP par **adaptateur** (aujourd'hui Freebuff et opencode),
maintient un état versionné (`state/*.json`, `schema.json` v1), et ne modifie jamais les
documents sans passer par `diff` (constat) → `apply` (exécution) → `lint` (contrôle).

## La direction

1. **Vérité dans le temps, pas instantanée.** Un chiffre n'a de sens que daté et sourcé.
   L'état du monde (retrait, dépréciation, promotion) est surveillé en continu ; ce qui
   est tiers 2 (annonces, RSS) ou tiers 3 (forums) ne déclenche jamais d'écriture
   automatique — seulement un signal « à vérifier », confié à un humain.
2. **Preuve en couches, sans mélange.** Tier 1 = source primaire de la plateforme ;
   tier 2 = annonce datée ; tier 3 = rumeur. Une source morte (`404`) retire
   l'affirmation, elle ne la rend pas « plausible ». `n.d.` vaut mieux qu'une précision
   inventée.
3. **Combler le trou que personne ne mesure.** La latence n'est enregistrée par aucune
   source du projet : c'est la raison d'être des investigations locales
   (`research/investigations.md`, `i0-francais.md`).
4. **Multi-plateforme par extension, pas par spécial.** Chaque nouvelle plateforme = un
   adaptateur JSON + un état, sans toucher au cœur (`engine.py`). Freebuff et opencode
   aujourd'hui ; d'autres si (et seulement si) une source primaire existe.
5. **Automatiser la surveillance, jamais le jugement.** Le moteur fetch, compare, classe
   (applicable / structurel / à vérifier / problème) et échoue bruyamment (`lint` =
   exit 1). Il ne rédige ni verdict, ni prose : les annotations humaines restent
   humaines (l'NLP sur prose a été écarté après faux positifs prouvés).

## Ce que le projet n'est pas

- **Pas un classement marketing.** Pas de gagnant unique : la conclusion robuste est une
  règle de routage par besoin (`research/verdict.md`).
- **Pas un fan-club ni un jugement de valeur** : constructeur étiqueté `constructeur`,
  jamais mélangé à un tiers.
- **Pas silencieux** : un échec de lint, un diff non nul, un signal debout sont visibles
  dans les rapports — masquer une divergence est la seule vraie régression.
- **Pas spéculatif** : rien n'est câblé sur un artefact inexistant (ex. best-of = N/A
  tant qu'il n'est pas une sortie produite).

## Principes de travail

KISS · DRY · YAGNI · zéro régression · honnêteté absolue (y compris « on ne sait pas ») ·
double-check des faits (mémoire d'abord, web en secours, write-back) · la trace est
append-only · « tout ce qui n'est pas dans l'ORCHESTRATOR n'existe pas ».

## Ancrage (2026-10-07, passe P10)

- Freebuff : **11 modèles live** sur l'état (14 fiches : + Space Bunny Alpha retiré le
  06/10 + 2 `hors cat.`), index commun **AA v4.3.2**.
- opencode : 14 modèles live dans l'état ; divergence tier 1/tier 2 suivie (flag debout
  `mimo-v2-5-free`, jamais auto-appli).
- Boucle quotidienne : `moteur/timer.sh` (systemd `--user`, 06:17±15 min + hebdo dim.
  07:23), rapports `research/rapport.md` et `research/rapport-opencode.md`.

## Ouvert

- **Latence** : aucun terrain de mesure — c'est la prochaine investigation utile.
- **Retraits Freebuff sans source de retrait** : le RSS couvre le cycle de vie (gate
  P10) ; une table explicite si une source primaire apparaît.
- **Flag `mimo-v2-5-free`** : se lever seul si le modèle réapparaît dans le service
  opérateur ; sinon rester debout.
- **Best-of** : à câbler (règle §7-1) seulement le jour où il devient une sortie
  produite.
