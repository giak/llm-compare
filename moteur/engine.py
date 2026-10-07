#!/usr/bin/env python3
"""
engine.py — partie DÉTERMINISTE du moteur d'investigation (stdlib, zéro dépendance).

Ici : parse, état, rendu, comparaison, lint. AUCUN jugement — le jugement
(recoupement Tier 1, annotation, journal, mémoire) appartient à l'agent,
selon moteur/ORCHESTRATOR.md.

Sous-commandes :
  import   research/comparatif.md  -> moteur/state/<plateforme>.json   (backfill, refuse d'écraser)
  pair     apparie fiches <-> état : fichier.replace('.', '-') == id
  migrate  insère le bloc GEN:prix après le H1 de chaque fiche (additif)
  check    le rendu depuis l'état == les fichiers ?  (NO REGRESSION ; exit 1 sinon)
  render   réécrit comparatif + blocs GEN:prix, pré-validation avant toute écriture
  show     résumé de l'état
  lint     appariement, structure de fiche (contrat du template), prix (exit 1 si erreur,
           avertissement si section recommandée manquante)
  fetch    santé (llms.txt 200 + ancre) puis téléchargement des sources de l'adapter ->
           moteur/cache/AAAA-MM-DD/ + manifest.json (sha1, fetched_at par source).
           Réutilise le cache du jour ; --revalidate re-télécharge tout (hebdo).
           Échec = rien écrit.
  diff     cache vs état : catalogue, accès, allocations, sections, prix solaires, /plans,
           feed, fraîcheur (≥7 j = revalidation requise). exit 0 = rien ; exit 2 = changement.
           Écrit research/rapport.md (sauf avec --date, qui est un run de test/manuel).
  apply    n'applique QUE le sous-ensemble sûr (accès, allocations, sections, historique
           prix) + sources/sha1 ; le structurel reste décision manuelle.

Migre un tableau : `import` puis `pair` puis `migrate`, puis `check` doit passer.
Boucle quotidienne : `fetch` -> `diff` -> (si exit 2) `apply` -> `render` -> `check` -> `lint`.
"""

from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import fcntl
import hashlib
import json
import math
import os
import re
import stat
import sys
import tempfile
import unicodedata
import urllib.request
from urllib.parse import urlparse
from pathlib import Path

MOTEUR = Path(__file__).resolve().parent
ROOT = MOTEUR.parent
TEMPLATE = MOTEUR / "templates" / "fiche-llm.md"

SCHEMA_VERSION = 1

# Contrat de fiche (moteur/templates/fiche-llm.md) : exigées = ordre imposé,
# recommandées = signalées par `lint` sans faire échouer (NO REGRESSION).
REQUIRED_SECTIONS = ("Identité", "Français", "Avantages", "Inconvénients", "Sources")
RECOMMENDED_SECTIONS = ("Puissance", "Analyse de problèmes", "Vitesse", "Coût", "Verdict")

CACHE_ROOT = MOTEUR / "cache"
MAX_RESPONSE_BYTES = 25 * 1024 * 1024

# §2.5 ORCHESTRATOR : revalidation hebdomadaire des sources de plus de N jours.
REVALIDATE_DAYS = 7

# Colonnes de mesures du tableau : indépendantes de la plateforme (grille du projet),
# clés d'état d'un côté, libellés de l'autre.
MEASURE_KEYS = [
    "aa", "tb4", "hle", "gdpval", "aa_lcr",
    "omis_prec", "omis_nonhall", "usd_task", "tok_s", "e2e_s",
]
MEASURE_HEADERS = [
    "AA", "TB 4.0", "HLE", "GDPval", "AA-LCR",
    "Omis.prec", "Omis.non-hall", "$/tâche", "tok/s", "E2E s",
]

# ---------------------------------------------------------------- plateforme
# Chemins, libellés et colonnes RÉSOLUS par setup_platform() depuis l'adapter
# (moteur/adapters/<platform>.json) — le module ne contient aucune valeur
# freebuff en dur. setup_platform() rebind ces globals avant toute commande.
STATE_PATH: Path | None = None
ADAPTER_PATH: Path | None = None
COMPARATIF: Path | None = None
FICHES_DIR: Path | None = None
FICHES_REL: str | None = None
RAPPORT: Path | None = None
HEADER: list[str] = []
ALIGN: list[str] = []
PLATFORM_LABEL = "Plateforme"     # libellé affiché : colonne, « Sur X : »
FN_KEY = ""                       # clé de marqueur de note (fn) dans l'état
SOLAR_MODEL_MAP: dict[str, str] = {}
ADAPTER: dict = {}

GEN_BEGIN = re.compile(r"^<!-- GEN:comparatif\|run=\d{4}-\d{2}-\d{2} -->$")
GEN_PRIX_BEGIN = re.compile(r"^<!-- GEN:prix\|run=\d{4}-\d{2}-\d{2} -->$")
GEN_END = "<!-- /GEN -->"

SUPER = r"¹²³⁴⁵⁶⁷⁸⁹⁰"
RE_FN = re.compile(f"([{SUPER}]+)$")
RE_MODEL = re.compile(r"^(.*?)(?: \(([^()]+)\))?(?: ([" + SUPER + r"†*]+))?$")
RE_PRICE = re.compile(r"^(\d+)(?:/h| (FB/h|j/h))(?: \(promo\))?$")
RE_RETIRED = re.compile(r"^🪦 \*\*retiré (\d{2})/(\d{2})(?:/(\d{4}))?\*\*$")

VALID_STATUS = ("live", "retired", "absent")
VALID_ACCESS = ("full", "metered", "paid_only", "us_only", "unknown")
VALID_SECTIONS = ("unlimited", "optimized", "powerful")
SOURCE_TYPES = {
    "llms_txt", "readme_md", "picker_ts", "solar_promo_ts", "plans_html",
    "rss", "zen_docs", "zen_catalog", "v1_models", "raw",
}


def path_within(path: Path, base: Path, label: str) -> Path:
    """Résout un chemin et refuse toute sortie de son répertoire autorisé."""
    base_real = base.resolve()
    if base.absolute() != base_real:
        sys.exit(f"{label} : le répertoire de base ne peut pas être un lien symbolique : {base}")
    root_real = ROOT.resolve()
    if base_real != root_real and root_real not in base_real.parents:
        sys.exit(f"{label} : répertoire de base hors du projet : {base}")
    candidate = path.resolve()
    if candidate != base_real and base_real not in candidate.parents:
        sys.exit(f"{label} hors du répertoire autorisé : {path}")
    return candidate


def project_path(raw: str, label: str) -> Path:
    if not isinstance(raw, str) or not raw:
        sys.exit(f"{label} doit être un chemin relatif non vide.")
    rel = Path(raw)
    if rel.is_absolute() or rel == Path(".") or ".." in rel.parts:
        sys.exit(f"{label} doit rester dans le projet : {raw!r}")
    return path_within(ROOT / rel, ROOT, label)


def cache_file(day: Path, name: str, label: str = "fichier de cache") -> Path:
    if (not isinstance(name, str) or not name or name in (".", "..")
            or Path(name).name != name or "/" in name or "\\" in name):
        sys.exit(f"{label} invalide : {name!r}")
    return path_within(day / name, day, label)


def atomic_write_many(items: list[tuple[Path, bytes]]) -> None:
    """Prépare tous les temporaires puis remplace chaque fichier atomiquement."""
    staged: list[tuple[Path, Path]] = []
    destinations = [path.resolve() for path, _ in items]
    if len(destinations) != len(set(destinations)):
        sys.exit("Écriture refusée : un même fichier apparaît plusieurs fois.")
    try:
        for destination, payload in items:
            destination.parent.mkdir(parents=True, exist_ok=True)
            fd, tmp_name = tempfile.mkstemp(
                prefix=f".{destination.name}.", suffix=".tmp",
                dir=destination.parent,
            )
            tmp = Path(tmp_name)
            try:
                with os.fdopen(fd, "wb") as stream:
                    stream.write(payload)
                    stream.flush()
                    os.fsync(stream.fileno())
                mode = (stat.S_IMODE(destination.stat().st_mode)
                        if destination.exists() else 0o644)
                os.chmod(tmp, mode)
            except BaseException:
                try:
                    os.close(fd)
                except OSError:
                    pass
                tmp.unlink(missing_ok=True)
                raise
            staged.append((tmp, destination))
        for tmp, destination in staged:
            os.replace(tmp, destination)
        for parent in {destination.parent for _, destination in staged}:
            dir_fd = os.open(parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
        staged.clear()
    finally:
        for tmp, _ in staged:
            tmp.unlink(missing_ok=True)


def atomic_write_text(path: Path, value: str) -> None:
    atomic_write_many([(path, value.encode("utf-8"))])


def run_locked(func, args) -> None:
    """Sérialise timer et invocations manuelles partageant état/cache."""
    CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    lock_path = path_within(CACHE_ROOT / ".engine.lock", CACHE_ROOT, "verrou moteur")
    with lock_path.open("a", encoding="utf-8") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            func(args)
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def valid_datetime(value: object) -> bool:
    if not isinstance(value, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})",
        value,
    ):
        return False
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def parse_datetime(value: object) -> dt.datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return _aware(parsed)


def valid_http_url(value: object) -> bool:
    if not isinstance(value, str) or not value or any(c.isspace() for c in value):
        return False
    try:
        parsed = urlparse(value)
        return (
            parsed.scheme in ("http", "https")
            and parsed.hostname is not None
            and parsed.username is None
            and parsed.password is None
            and (parsed.port is None or 1 <= parsed.port <= 65535)
        )
    except (ValueError, UnicodeError):
        return False


def setup_platform(platform: str, adapter_path: Path | None = None) -> None:
    """Résout la plateforme : charge l'adapter, rebind les globals du module.

    Le défaut reste freebuff (timers, usages existants) ; --platform change tout.
    Échec franc si l'adapter est absent/incomplet (aucune sortie partielle)."""
    global STATE_PATH, ADAPTER_PATH, COMPARATIF, FICHES_DIR, FICHES_REL, RAPPORT
    global HEADER, ALIGN, PLATFORM_LABEL, FN_KEY, SOLAR_MODEL_MAP, ADAPTER
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", platform):
        sys.exit(f"Identifiant de plateforme invalide : {platform!r}")
    adapters_dir = MOTEUR / "adapters"
    requested = adapter_path or (adapters_dir / f"{platform}.json")
    if not requested.is_absolute():
        requested = ROOT / requested
    if requested.is_symlink():
        sys.exit(f"Un adaptateur ne peut pas être un lien symbolique : {requested}")
    ADAPTER_PATH = path_within(requested, adapters_dir, "adaptateur")
    adapter = load_adapter(ADAPTER_PATH)
    if ADAPTER_PATH.stem != platform:
        sys.exit(f"Adapter {ADAPTER_PATH.name} : le nom de fichier doit être "
                 f"{platform}.json.")
    if adapter["platform"] != platform:
        sys.exit(f"Adapter {ADAPTER_PATH.name} : platform « {adapter['platform']} » "
                 f"!= « {platform} » (nom du fichier = identifiant plateforme).")
    ADAPTER = adapter
    state_candidate = MOTEUR / "state" / f"{platform}.json"
    if state_candidate.is_symlink():
        sys.exit(f"Le fichier d'état ne peut pas être un lien symbolique : {state_candidate}")
    STATE_PATH = path_within(state_candidate, MOTEUR / "state", "fichier d'état")
    PLATFORM_LABEL = adapter.get("label", platform.capitalize())
    FN_KEY = platform
    SOLAR_MODEL_MAP = dict(adapter.get("model_map", {}))
    HEADER = ["Modèle", *MEASURE_HEADERS, "Contexte", PLATFORM_LABEL]
    ALIGN = ["---"] + ["---:"] * (len(HEADER) - 1)
    research = adapter.get("research") or {}
    COMPARATIF = project_path(research["comparatif"], "research.comparatif") \
        if research.get("comparatif") else None
    if research.get("fiches"):
        FICHES_DIR = project_path(research["fiches"], "research.fiches")
        FICHES_REL = research["fiches"]
    else:
        FICHES_DIR = None
        FICHES_REL = None
    RAPPORT = project_path(research["rapport"], "research.rapport") \
        if research.get("rapport") else None


# ---------------------------------------------------------------- état

def cache_day(date_str: str) -> Path:
    """Cache par plateforme (moteur/cache/<platform>/AAAA-MM-DD) : deux
    plateformes ne partagent JAMAIS le même manifest."""
    try:
        parsed = dt.date.fromisoformat(date_str)
    except (TypeError, ValueError):
        sys.exit(f"Date de cache invalide : {date_str!r} (format AAAA-MM-JJ attendu).")
    if parsed.isoformat() != date_str:
        sys.exit(f"Date de cache invalide : {date_str!r} (format AAAA-MM-JJ attendu).")
    platform_dir = path_within(CACHE_ROOT / FN_KEY, CACHE_ROOT, "cache plateforme")
    candidate = platform_dir / parsed.isoformat()
    if candidate.is_symlink():
        sys.exit(f"Un répertoire de cache ne peut pas être un lien symbolique : {candidate}")
    return path_within(candidate, platform_dir, "cache daté")


def load_state() -> dict:
    if not STATE_PATH.exists():
        sys.exit(f"ÉTAT ABSENT : {STATE_PATH} — lancez d'abord `import`.")
    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        sys.exit(f"ÉTAT ILLISIBLE : {STATE_PATH} — {exc}")
    validate(state, expected_platform=FN_KEY)
    return state


def save_state(state: dict) -> None:
    validate(state, expected_platform=FN_KEY)
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(STATE_PATH, json.dumps(state, ensure_ascii=False, indent=2) + "\n")


def validate(state: object, expected_platform: str | None = None) -> None:
    """Valide le contrat de schema.json sans dépendance externe."""
    errs: list[str] = []
    if not isinstance(state, dict):
        sys.exit("ÉTAT INVALIDE : la racine JSON doit être un objet.")

    def error(where: str, message: str) -> None:
        errs.append(f"{where}: {message}")

    def table_cell(value: object) -> bool:
        return isinstance(value, str) and not any(c in value for c in "|\r\n")

    def datetime_field(value: object, where: str, nullable: bool = False) -> None:
        if nullable and value is None:
            return
        if not valid_datetime(value):
            error(where, "date ISO 8601 avec fuseau attendue")

    allowed_top = {
        "platform", "schema_version", "generated_at", "imported_from",
        "sources", "facts", "models",
    }
    for extra in sorted(set(state) - allowed_top):
        error(extra, "champ supplémentaire interdit")
    for key in ("platform", "schema_version", "generated_at", "sources", "facts", "models"):
        if key not in state:
            error(key, "champ manquant")
    platform = state.get("platform")
    if not isinstance(platform, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", platform):
        error("platform", "slug invalide")
    elif expected_platform is not None and platform != expected_platform:
        error("platform", f"{platform!r} ne correspond pas à {expected_platform!r}")
    if type(state.get("schema_version")) is not int or state.get("schema_version") != SCHEMA_VERSION:
        error("schema_version", f"valeur attendue : {SCHEMA_VERSION}")
    datetime_field(state.get("generated_at"), "generated_at")
    if "imported_from" in state and not (
        state["imported_from"] is None or isinstance(state["imported_from"], str)
    ):
        error("imported_from", "chaîne ou null attendu")

    sources = state.get("sources")
    if not isinstance(sources, list):
        error("sources", "liste attendue")
        sources = []
    seen_urls: set[str] = set()
    for i, source in enumerate(sources):
        where = f"sources[{i}]"
        if not isinstance(source, dict):
            error(where, "objet attendu")
            continue
        if set(source) - {"url", "tier", "fetched_at", "sha1"}:
            error(where, "champ supplémentaire interdit")
        for key in ("url", "tier", "fetched_at"):
            if key not in source:
                error(where, f"champ manquant {key}")
        url = source.get("url")
        if not valid_http_url(url):
            error(f"{where}.url", "URL HTTP(S) attendue")
        elif url in seen_urls:
            error(f"{where}.url", "URL source dupliquée")
        else:
            seen_urls.add(url)
        if type(source.get("tier")) is not int or source.get("tier") not in (1, 2, 3):
            error(f"{where}.tier", "niveau 1, 2 ou 3 attendu")
        datetime_field(source.get("fetched_at"), f"{where}.fetched_at")
        if "sha1" in source and (
            not isinstance(source["sha1"], str)
            or not re.fullmatch(r"[0-9a-f]{40}", source["sha1"])
        ):
            error(f"{where}.sha1", "empreinte SHA-1 invalide")

    facts = state.get("facts")
    if not isinstance(facts, dict):
        error("facts", "objet attendu")
    else:
        for name, fact in facts.items():
            where = f"facts.{name}"
            if not isinstance(name, str) or not name:
                error("facts", "clés non vides attendues")
                continue
            if not isinstance(fact, dict):
                error(where, "objet {value, evidence} attendu")
                continue
            if set(fact) - {"value", "evidence"}:
                error(where, "seuls value et evidence sont autorisés")
            if "value" not in fact:
                error(where, "champ value manquant")
            evidence = fact.get("evidence")
            if not isinstance(evidence, dict):
                error(f"{where}.evidence", "objet attendu")
                continue
            if set(evidence) - {"url", "tier", "at", "commit", "quote"}:
                error(f"{where}.evidence", "champ supplémentaire interdit")
            for key in ("url", "tier", "at"):
                if key not in evidence:
                    error(f"{where}.evidence", f"champ manquant {key}")
            if "url" in evidence and not valid_http_url(evidence["url"]):
                error(f"{where}.evidence.url", "URL HTTP(S) attendue")
            if "tier" in evidence and (
                type(evidence["tier"]) is not int or evidence["tier"] not in (1, 2, 3)
            ):
                error(f"{where}.evidence.tier", "niveau 1, 2 ou 3 attendu")
            if "at" in evidence:
                datetime_field(evidence["at"], f"{where}.evidence.at")
            for key in ("commit", "quote"):
                if key in evidence and not isinstance(evidence[key], str):
                    error(f"{where}.evidence.{key}", "chaîne attendue")

    model_fields = {
        "id", "display", "effort", "suffix", "status", "section", "retired_at",
        "access", "emphasis", "fn", "price", "context", "measures", "fiche",
        "history",
    }
    price_fields = {"value", "unit", "promo", "since", "end"}
    history_fields = {"at", "field", "from", "to", "evidence"}
    evidence_fields = {"url", "tier", "commit", "quote"}
    seen: set[str] = set()
    models = state.get("models")
    if not isinstance(models, list):
        error("models", "liste attendue")
        models = []
    for i, m in enumerate(models):
        where = f"models[{i}]"
        if not isinstance(m, dict):
            error(where, "objet attendu")
            continue
        extra = set(m) - model_fields
        if extra:
            error(where, f"champs supplémentaires interdits : {sorted(extra)}")
        for key in ("id", "display", "status", "access", "price", "context", "measures", "history"):
            if key not in m:
                error(where, f"champ manquant {key}")
        mid = m.get("id")
        if not isinstance(mid, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", mid):
            error(f"{where}.id", "slug invalide")
        elif mid in seen:
            error(f"{where}.id", "identifiant dupliqué")
        else:
            seen.add(mid)
        if not table_cell(m.get("display")) or not m.get("display", "").strip():
            error(f"{where}.display", "chaîne non vide sans séparateur Markdown attendue")
        for field in ("effort", "suffix"):
            if field in m and not (m[field] is None or table_cell(m[field])):
                error(f"{where}.{field}", "chaîne sans séparateur Markdown ou null attendue")
        if m.get("status") not in VALID_STATUS:
            error(f"{where}.status", f"valeur invalide {m.get('status')!r}")
        if m.get("access") not in VALID_ACCESS:
            error(f"{where}.access", f"valeur invalide {m.get('access')!r}")
        if "section" in m and m["section"] not in (*VALID_SECTIONS, None):
            error(f"{where}.section", f"valeur invalide {m['section']!r}")
        if "retired_at" in m and m["retired_at"] is not None:
            try:
                if not isinstance(m["retired_at"], str):
                    raise ValueError
                retired_date = dt.date.fromisoformat(m["retired_at"])
                if retired_date.isoformat() != m["retired_at"]:
                    raise ValueError
            except ValueError:
                error(f"{where}.retired_at", "date ISO attendue")
        if m.get("status") == "retired" and not m.get("retired_at"):
            error(f"{where}.retired_at", "obligatoire si status=retired")
        if "emphasis" in m and not isinstance(m["emphasis"], bool):
            error(f"{where}.emphasis", "booléen attendu")
        if "fn" in m:
            if (not isinstance(m["fn"], dict)
                    or any(not isinstance(k, str) or not table_cell(v)
                           for k, v in m["fn"].items())):
                error(f"{where}.fn", "objet de marqueurs sans séparateur Markdown attendu")
        if "fiche" in m and not (m["fiche"] is None or isinstance(m["fiche"], str)):
            error(f"{where}.fiche", "chemin ou null attendu")
        elif isinstance(m.get("fiche"), str):
            try:
                fiche_path(m)
            except SystemExit as exc:
                error(f"{where}.fiche", str(exc))

        price = m.get("price")
        if not isinstance(price, dict):
            error(f"{where}.price", "objet attendu")
        else:
            if set(price) - price_fields:
                error(f"{where}.price", "champ supplémentaire interdit")
            for key in ("value", "unit", "promo"):
                if key not in price:
                    error(f"{where}.price", f"champ manquant {key}")
            value = price.get("value")
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, (int, float))
                or (isinstance(value, float) and not math.isfinite(value))
            ):
                error(f"{where}.price.value", "nombre ou null attendu")
            elif value is not None and value < 0:
                error(f"{where}.price.value", "prix négatif interdit")
            if price.get("unit") is not None and not table_cell(price.get("unit")):
                error(f"{where}.price.unit", "chaîne sans séparateur Markdown ou null attendue")
            if "promo" in price and not isinstance(price["promo"], bool):
                error(f"{where}.price.promo", "booléen attendu")
            if value is None and price.get("unit") is not None:
                error(f"{where}.price", "unité sans valeur")
            if value is not None and price.get("unit") is None:
                error(f"{where}.price", "valeur sans unité")
            for field in ("since", "end"):
                if field in price:
                    datetime_field(price[field], f"{where}.price.{field}", nullable=True)
            if price.get("promo") and value is None:
                error(f"{where}.price.promo", "une promotion exige un prix connu")
            if price.get("since") and price.get("end"):
                starts = parse_datetime(price["since"])
                ends = parse_datetime(price["end"])
                if starts is not None and ends is not None and ends < starts:
                    error(f"{where}.price.end", "fin de promotion antérieure au début")

            access = m.get("access")
            status = m.get("status")
            if status == "live":
                if access == "unknown":
                    if value is not None or price.get("promo"):
                        error(f"{where}.price", "un prix inconnu ne peut pas porter de valeur")
                elif access in ("paid_only", "us_only") and value is not None:
                    error(f"{where}.price", "un accès payant ne porte pas de prix gratuit")
                elif access == "metered" and value is None:
                    error(f"{where}.price", "un accès metered exige un prix")
                elif access == "full" and value != 0:
                    error(f"{where}.price", "un accès full doit être tarifé à zéro")
            elif status in ("retired", "absent"):
                if access != "unknown":
                    error(f"{where}.access", f"status={status} exige access=unknown")
                if value is not None or price.get("promo"):
                    error(f"{where}.price", f"status={status} exige un prix nul et sans promotion")

        context = m.get("context")
        if not isinstance(context, dict):
            error(f"{where}.context", "objet attendu")
        else:
            if set(context) - {"value", "tokens"}:
                error(f"{where}.context", "champ supplémentaire interdit")
            if not table_cell(context.get("value")):
                error(f"{where}.context.value", "chaîne sans séparateur Markdown attendue")
            tokens = context.get("tokens")
            if tokens is not None and (type(tokens) is not int):
                error(f"{where}.context.tokens", "entier ou null attendu")

        measures = m.get("measures")
        if not isinstance(measures, dict):
            error(f"{where}.measures", "objet attendu")
        else:
            for key in MEASURE_KEYS:
                if key not in measures:
                    error(f"{where}.measures", f"champ manquant {key}")
            for key, value in measures.items():
                if not isinstance(key, str) or not table_cell(value):
                    error(f"{where}.measures", "les valeurs doivent être des chaînes sans séparateur Markdown")

        history = m.get("history")
        if not isinstance(history, list):
            error(f"{where}.history", "liste attendue")
            history = []
        for j, entry in enumerate(history):
            hwhere = f"{where}.history[{j}]"
            if not isinstance(entry, dict):
                error(hwhere, "objet attendu")
                continue
            if set(entry) - history_fields:
                error(hwhere, "champ supplémentaire interdit")
            for key in ("at", "field", "from", "to"):
                if key not in entry:
                    error(hwhere, f"champ manquant {key}")
            datetime_field(entry.get("at"), f"{hwhere}.at")
            if "field" in entry and not isinstance(entry["field"], str):
                error(f"{hwhere}.field", "chaîne attendue")
            evidence = entry.get("evidence")
            if "evidence" in entry:
                if not isinstance(evidence, dict):
                    error(f"{hwhere}.evidence", "objet attendu")
                else:
                    if set(evidence) - evidence_fields:
                        error(f"{hwhere}.evidence", "champ supplémentaire interdit")
                    for key in ("url", "tier"):
                        if key not in evidence:
                            error(f"{hwhere}.evidence", f"champ manquant {key}")
                    if "url" in evidence and not isinstance(evidence["url"], str):
                        error(f"{hwhere}.evidence.url", "chaîne attendue")
                    if "tier" in evidence and (
                        type(evidence["tier"]) is not int or evidence["tier"] not in (1, 2, 3)
                    ):
                        error(f"{hwhere}.evidence.tier", "niveau 1, 2 ou 3 attendu")
                    for field in ("commit", "quote"):
                        if field in evidence and not isinstance(evidence[field], str):
                            error(f"{hwhere}.evidence.{field}", "chaîne attendue")
    if errs:
        sys.exit("ÉTAT INVALIDE :\n  - " + "\n  - ".join(errs))


# ---------------------------------------------------------------- tableau

def find_table(lines: list[str]) -> tuple[int, int]:
    try:
        start = next(i for i, l in enumerate(lines) if l.startswith("| Modèle |"))
    except StopIteration:
        sys.exit("Tableau « | Modèle | » introuvable.")
    end = start
    while end + 1 < len(lines) and lines[end + 1].startswith("|"):
        end += 1
    return start, end


def split_row(line: str) -> list[str]:
    parts = line.strip().split("|")
    return [p.strip() for p in parts[1:-1]]


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).lower().strip("-")
    return text or "sans-nom"


def parse_table(text: str) -> list[dict]:
    """Tableau markdown -> modèles (structure d'état)."""
    lines = text.splitlines()
    start, end = find_table(lines)
    if start + 1 >= len(lines):
        sys.exit("LIGNE D'ALIGNEMENT absente après l'entête du tableau.")
    header = split_row(lines[start])
    align = lines[start + 1].strip()
    if header != HEADER:
        sys.exit(f"ENTÊTE DIFFÉRENTE du contrat de rendu :\n  fichier: {header}\n  contrat : {HEADER}")
    if align != "|" + "|".join(ALIGN) + "|":
        sys.exit(f"LIGNE D'ALIGNEMENT DIFFÉRENTE :\n  fichier: {align}\n  contrat : {'|' + '|'.join(ALIGN) + '|'}")

    models = []
    for line in lines[start + 2 : end + 1]:
        cells = split_row(line)
        if len(cells) != len(HEADER):
            sys.exit(f"Ligne à {len(cells)} cellules (attendu {len(HEADER)}):\n  {line}")
        models.append(parse_model_row(cells))
    return models


def parse_model_row(c: list[str]) -> dict:
    name, effort, suffix = RE_MODEL.match(c[0]).groups()

    ctx_i, price_i = len(HEADER) - 2, len(HEADER) - 1
    context_raw = c[ctx_i]
    fn_ctx = ""
    m = RE_FN.search(context_raw)
    if m:
        fn_ctx, context_raw = m.group(1), context_raw[: m.start()].rstrip()

    access, price, status, retired_at, emphasis, fn_price = parse_price_cell(c[price_i])

    slug = slugify(name)
    fn = {}
    if fn_ctx:
        fn["context"] = fn_ctx
    if fn_price:
        fn[FN_KEY] = fn_price
    model = {
        "id": slug,
        "display": name,
        "effort": effort,
        "suffix": suffix,
        "status": status,
        "retired_at": retired_at,
        "access": access,
        "emphasis": emphasis,
        "price": price,
        "context": {"value": context_raw},
        "measures": {k: c[i + 1] for i, k in enumerate(MEASURE_KEYS)},
        "fiche": None,
        "history": [],
    }
    if fn:
        model["fn"] = fn
    return model


def parse_price_cell(raw: str) -> tuple[str, dict, str, str | None, bool, str]:
    """Cellule de prix de plateforme -> (access, price, status, retired_at, emphasis, fn).

    Grammaire de la cellule GEN (valeurs fixes : 🔒 payant, hors cat., promo, 🪦…) :
    c'est le contrat de rendu du projet, pas la propriété d'une plateforme."""
    emphasis = raw.startswith("**") and raw.endswith("**") and not raw.startswith("🪦")
    inner = raw[2:-2] if emphasis else raw

    fn = ""
    m = RE_FN.search(inner)
    if m:
        fn, inner = m.group(1), inner[: m.start()].rstrip()

    null_price = {"value": None, "unit": None, "promo": False, "since": None, "end": None}

    if inner.startswith("🪦"):
        mm = RE_RETIRED.match(inner)
        if not mm:
            sys.exit(f"Cellule retrait illisible: {raw!r}")
        day, month, year = mm.groups()
        today_utc = dt.datetime.now(dt.timezone.utc).date()
        retired = None
        if year is not None:
            try:
                candidate = dt.date(int(year), int(month), int(day))
            except ValueError:
                candidate = None
            if candidate is not None and candidate <= today_utc:
                retired = candidate
        else:
            for candidate_year in range(today_utc.year, today_utc.year - 9, -1):
                try:
                    candidate = dt.date(candidate_year, int(month), int(day))
                except ValueError:
                    continue
                if candidate <= today_utc:
                    retired = candidate
                    break
        if retired is None:
            sys.exit(f"Date de retrait invalide : {raw!r}")
        return "unknown", dict(null_price), "retired", retired.isoformat(), emphasis, fn
    if inner == "hors cat.":
        return "unknown", dict(null_price), "absent", None, emphasis, fn
    if inner == "🔒 payant":
        return "paid_only", dict(null_price), "live", None, emphasis, fn
    if inner == "🔒 FR = payant":
        return "us_only", dict(null_price), "live", None, emphasis, fn
    if inner == "0 promo":
        return "metered", {"value": 0, "unit": "h", "promo": True, "since": None, "end": None}, "live", None, emphasis, fn

    pm = RE_PRICE.match(inner)
    if not pm:
        sys.exit(f"Cellule prix illisible: {raw!r}")
    value, sub = pm.groups()
    is_promo = inner.endswith(" (promo)")
    price = {"value": int(value), "unit": sub or "h", "promo": is_promo,
             "since": None, "end": None}
    return "metered", price, "live", None, emphasis, fn


# ---------------------------------------------------------------- rendu

def render_price_cell(m: dict) -> str:
    if m["status"] == "retired":
        d = dt.date.fromisoformat(m["retired_at"])
        inner = f"🪦 **retiré {d.day:02d}/{d.month:02d}/{d.year}**"
    elif m["status"] == "absent":
        inner = "hors cat."
    elif m["access"] == "paid_only":
        inner = "🔒 payant"
    elif m["access"] == "us_only":
        inner = "🔒 FR = payant"
    elif m["access"] == "unknown":
        inner = ""
    elif m["price"]["value"] == 0 and m["price"]["promo"]:
        inner = "0 promo"
    else:
        v, u = m["price"]["value"], m["price"]["unit"]
        inner = f"{v}/{u}" if u == "h" else f"{v} {u}"
        if m["price"].get("promo"):
            inner += " (promo)"

    fn = (m.get("fn") or {}).get(FN_KEY, "")
    cell = inner + (f" {fn}" if fn else "")
    if m.get("emphasis"):
        cell = f"**{cell}**"
    return cell


def render_model_cell(m: dict) -> str:
    cell = m["display"]
    if m.get("effort"):
        cell += f" ({m['effort']})"
    if m.get("suffix"):
        cell += f" {m['suffix']}"
    fn = (m.get("fn") or {}).get("model", "")
    if fn:
        cell += f" {fn}"
    return cell


def render_context_cell(m: dict) -> str:
    cell = m["context"]["value"]
    fn = (m.get("fn") or {}).get("context", "")
    return cell + (f" {fn}" if fn else "")


def render_table(state: dict) -> str:
    out = [
        "| " + " | ".join(HEADER) + " |",
        "|" + "|".join(ALIGN) + "|",
    ]
    for m in state["models"]:
        cells = [render_model_cell(m)]
        cells += [m["measures"][k] for k in MEASURE_KEYS]
        cells += [render_context_cell(m), render_price_cell(m)]
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def render_prix_line(m: dict) -> str:
    """Ligne canonique de prix pour une fiche — même état que la colonne de
    plateforme du comparatif, mais sans les marqueurs de note (⁴… : props du comparatif)."""
    if m["status"] == "retired":
        d = dt.date.fromisoformat(m["retired_at"])
        body = f"🪦 retiré du catalogue le {d.day:02d}/{d.month:02d}/{d.year}"
    elif m["status"] == "absent":
        body = "hors catalogue"
    elif m["access"] == "paid_only":
        body = "🔒 payant (plans payants)"
    elif m["access"] == "us_only":
        body = "🔒 FR = payant (gratuit aux US)"
    elif m["access"] == "unknown":
        body = "prix non publié"
    elif m["price"]["value"] == 0 and m["price"]["promo"]:
        end = m["price"]["end"]
        suffix = f"jusqu'au {end}" if end else "sans échéance connue"
        body = f"0/h (promo {suffix})"
    else:
        v, u = m["price"]["value"], m["price"]["unit"]
        body = f"{v}/{u}" if u == "h" else f"{v} {u}"
        if m["price"].get("promo"):
            body += " (promo)"
    return f"**Sur {PLATFORM_LABEL} :** {body}"


def fiche_path(m: dict) -> Path | None:
    raw = m.get("fiche")
    if not raw:
        return None
    if FICHES_DIR is None:
        sys.exit("chemin de fiche déclaré alors que l'adapter n'a pas de dossier de fiches")
    lexical = ROOT / raw
    if lexical.is_symlink():
        sys.exit(f"Une fiche ne peut pas être un lien symbolique : {raw}")
    path = project_path(raw, "chemin de fiche")
    fiches_root = FICHES_DIR.resolve()
    if path.parent != fiches_root or path.suffix != ".md":
        sys.exit(f"La fiche doit être un fichier .md directement dans {FICHES_REL} : {raw}")
    if path.exists() and not path.is_file():
        sys.exit(f"Le chemin de fiche n'est pas un fichier : {raw}")
    return path


def find_block(lines: list[str], begin_re: re.Pattern) -> tuple[int, int] | None:
    """Un unique bloc GEN complet, ou None si aucun marqueur n'est présent."""
    begins = [i for i, line in enumerate(lines) if begin_re.match(line)]
    ends = [i for i, line in enumerate(lines) if line.strip() == GEN_END]
    if not begins and not ends:
        return None
    if len(begins) != 1 or len(ends) != 1 or begins[0] >= ends[0]:
        sys.exit("Structure GEN invalide : un marqueur de début et un de fin sont requis.")
    return begins[0], ends[0]


# ---------------------------------------------------------------- commandes

def today() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")


def no_comparatif() -> None:
    sys.exit(f"{PLATFORM_LABEL} : pas de comparatif déclaré dans l'adapter "
             f"(research.comparatif) — commande réservée à une plateforme à tableau.")


def no_fiches() -> None:
    sys.exit(f"{PLATFORM_LABEL} : pas de dossier de fiches déclaré dans l'adapter "
             f"(research.fiches) — commande réservée à une plateforme à fiches.")


def cmd_import(args) -> None:
    if COMPARATIF is None:
        no_comparatif()
    if not COMPARATIF.is_file():
        sys.exit(f"Comparatif absent ou illisible : {COMPARATIF}")
    if STATE_PATH.exists() and not args.force:
        sys.exit(f"ÉTAT DÉJÀ PRÉSENT : {STATE_PATH} (utilisez --force pour le refaire).")
    text = COMPARATIF.read_text(encoding="utf-8")
    models = parse_table(text)
    ids = [m["id"] for m in models]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        sys.exit(f"id dupliqués après slugification : {dup}")
    state = {
        "platform": load_adapter(ADAPTER_PATH)["platform"],
        "schema_version": SCHEMA_VERSION,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "imported_from": f"{COMPARATIF.relative_to(ROOT)} (backfill {today()})",
        "sources": [],
        "facts": {},
        "models": models,
    }
    save_state(state)
    print(f"import OK : {len(models)} modèles -> {STATE_PATH.relative_to(ROOT)}")


def cmd_pair(args) -> None:
    """Apparie chaque fiche à son modèle : nom-de-fichier.replace('.', '-') == id."""
    if FICHES_DIR is None or FICHES_REL is None:
        no_fiches()
    state = load_state()
    by_id = {m["id"]: m for m in state["models"]}
    files = sorted(FICHES_DIR.glob("*.md"))
    if not files:
        sys.exit(f"Aucune fiche dans {FICHES_DIR}.")
    pairs: dict[str, Path] = {}
    orphans: list[str] = []
    for f in files:
        key = f.stem.replace(".", "-")
        if key in pairs:
            sys.exit(f"Deux fiches pour l'id « {key} » : {pairs[key].name}, {f.name}")
        if key not in by_id:
            orphans.append(f"{f.name} (clé « {key} » absente de l'état)")
            continue
        pairs[key] = f
    if orphans:
        sys.exit("fiche(s) orpheline(s), non appariée(s) :\n  - " + "\n  - ".join(orphans))
    for key, f in pairs.items():
        by_id[key]["fiche"] = f"{FICHES_REL}/{f.name}"
    save_state(state)
    missing = sorted(set(by_id) - set(pairs))
    tail = f" — sans fiche : {missing}" if missing else ""
    print(f"pair OK : {len(pairs)}/{len(by_id)} modèles appariés{tail}")


def cmd_migrate(args) -> None:
    """Insère le bloc GEN:prix après le H1 de chaque fiche appariée (additif : 3 lignes).

    Valide TOUTES les fiches avant d'écrire la moindre (aucune écriture partielle)."""
    if FICHES_DIR is None:
        no_fiches()
    state = load_state()
    plan: list[tuple[Path, dict, list[str], int]] = []
    errs: list[str] = []
    for m in state["models"]:
        p = fiche_path(m)
        if p is None:
            errs.append(f"{m['id']}: fiche non appariée (lancez `pair`)")
            continue
        if not p.exists():
            errs.append(f"{m['id']}: fichier absent — {m['fiche']}")
            continue
        lines = p.read_text(encoding="utf-8").splitlines()
        existing_block = find_block(lines, GEN_PRIX_BEGIN)
        if existing_block is not None:
            continue
        h1 = next((i for i, l in enumerate(lines) if l.startswith("# ")), None)
        if h1 is None:
            errs.append(f"{p.name}: H1 absent")
            continue
        plan.append((p, m, lines, h1))
    if errs:
        sys.exit("migrate REFUSÉ (aucune écriture) :\n  - " + "\n  - ".join(errs))
    run = today()
    writes: list[tuple[Path, bytes]] = []
    for p, m, lines, h1 in plan:
        out = (
            lines[: h1 + 1]
            + [f"<!-- GEN:prix|run={run} -->", render_prix_line(m), GEN_END]
            + lines[h1 + 1 :]
        )
        writes.append((p, ("\n".join(out) + "\n").encode("utf-8")))
    atomic_write_many(writes)
    print(f"migrate OK : {len(plan)} fiche(s) équipée(s) du bloc GEN:prix "
          f"({len(state['models']) - len(plan)} déjà équipée(s)).")


def cmd_check(args) -> None:
    if COMPARATIF is None:
        no_comparatif()
    if not COMPARATIF.is_file():
        sys.exit(f"Comparatif absent ou illisible : {COMPARATIF}")
    state = load_state()
    errs: list[str] = []

    # 1. comparatif : le tableau rendu depuis l'état == le fichier ?
    rendered = render_table(state)
    lines = COMPARATIF.read_text(encoding="utf-8").splitlines()
    blk = find_block(lines, GEN_BEGIN)
    if blk is not None:
        current = "\n".join(lines[blk[0] + 1 : blk[1]])
        zone = "bloc GEN"
    else:
        start, end = find_table(lines)
        current = "\n".join(lines[start : end + 1])
        zone = "tableau (marqueurs absents)"
    if current != rendered:
        diff = [
            f"  ligne {i + 1}\n    fichier: {c}\n    rendu   : {r}"
            for i, (c, r) in enumerate(zip(current.splitlines(), rendered.splitlines()))
            if c != r
        ]
        if len(current.splitlines()) != len(rendered.splitlines()):
            diff.append(
                f"  nombre de lignes: fichier={len(current.splitlines())} "
                f"rendu={len(rendered.splitlines())}"
            )
        sys.exit(f"check ÉCHEC ({zone}) — NO REGRESSION violée :\n" + "\n".join(diff[:20]))

    # 2. fiches : le bloc GEN:prix == le prix de l'état ?
    n_fiches = 0
    for m in state["models"]:
        p = fiche_path(m)
        if p is None:
            continue  # l'appariement, c'est lint
        if not p.exists():
            errs.append(f"{m['id']}: fichier absent — {m['fiche']}")
            continue
        flines = p.read_text(encoding="utf-8").splitlines()
        fblk = find_block(flines, GEN_PRIX_BEGIN)
        if fblk is None:
            errs.append(f"{p.name}: bloc GEN:prix absent ou ouvert (lancez `migrate`)")
            continue
        got = flines[fblk[0] + 1 : fblk[1]]
        want = [render_prix_line(m)]
        if got != want:
            errs.append(f"{p.name}: prix divergent de l'état\n"
                        f"    fichier: {got}\n    état   : {want}")
        n_fiches += 1
    if errs:
        sys.exit("check ÉCHEC (fiches) :\n  - " + "\n  - ".join(errs))
    print(f"check OK : comparatif ({zone}, {len(state['models'])} lignes) "
          f"+ {n_fiches} fiche(s)")


def cmd_render(args) -> None:
    """Réécrit comparatif + blocs GEN:prix. Pré-valide tout avant la première écriture."""
    if COMPARATIF is None:
        no_comparatif()
    if not COMPARATIF.is_file():
        sys.exit(f"Comparatif absent ou illisible : {COMPARATIF}")
    state = load_state()
    rendered = render_table(state)
    lines = COMPARATIF.read_text(encoding="utf-8").splitlines()
    cblk = find_block(lines, GEN_BEGIN)
    if cblk is None:
        sys.exit("comparatif: marqueurs GEN absents (migration faite ?).")

    plan: list[tuple[Path, list[str], tuple[int, int], str]] = []
    errs: list[str] = []
    for m in state["models"]:
        p = fiche_path(m)
        if p is None:
            continue
        if not p.exists():
            errs.append(f"{m['id']}: fichier absent — {m['fiche']}")
            continue
        flines = p.read_text(encoding="utf-8").splitlines()
        fblk = find_block(flines, GEN_PRIX_BEGIN)
        if fblk is None:
            errs.append(f"{p.name}: bloc GEN:prix absent ou ouvert (lancez `migrate`)")
            continue
        prix = render_prix_line(m)
        if flines[fblk[0] + 1 : fblk[1]] != [prix]:
            plan.append((p, flines, fblk, prix))
    if errs:
        sys.exit("render REFUSÉ (aucune écriture) :\n  - " + "\n  - ".join(errs))

    old_inner = lines[cblk[0] + 1 : cblk[1]]
    new_inner = rendered.splitlines()
    out_lines = lines[: cblk[0] + 1] + new_inner + [GEN_END] + lines[cblk[1] + 1 :]
    changed_c = sum(1 for a, b in zip(old_inner, new_inner) if a != b)
    changed_c += abs(len(old_inner) - len(new_inner))

    writes: list[tuple[Path, bytes]] = [
        (COMPARATIF, ("\n".join(out_lines) + "\n").encode("utf-8"))
    ]
    for p, flines, fblk, prix in plan:
        f_out = flines[: fblk[0] + 1] + [prix] + flines[fblk[1] :]
        writes.append((p, ("\n".join(f_out) + "\n").encode("utf-8")))
    atomic_write_many(writes)

    n_paired = sum(1 for m in state["models"] if m.get("fiche"))
    print(f"render OK : comparatif {changed_c} ligne(s) modifiée(s), "
          f"{len(plan)}/{n_paired} fiche(s) réécrite(s).")


def cmd_show(args) -> None:
    state = load_state()
    print(f"platform={state['platform']} schema={state['schema_version']} "
          f"généré={state['generated_at']} sources={len(state['sources'])}")
    for m in state["models"]:
        cell = render_price_cell(m) or "—"
        print(f"  {m['id']:<32} {m['status']:<7} {m['access']:<10} "
              f"{m['measures']['aa']:>10}  {cell}")


def cmd_lint(args) -> None:
    """Cohérence inter-doc. Erreur = exit 1 ; manques « recommandés » = avertissements."""
    state = load_state()
    errs: list[str] = []
    warns: list[str] = []

    # 1. état interne (prix/accès cohérents)
    for m in state["models"]:
        p = m["price"]
        if p["value"] is None and p["unit"] is not None:
            errs.append(f"{m['id']}: unité sans valeur")
        if p["value"] is not None and p["unit"] is None:
            errs.append(f"{m['id']}: valeur sans unité")
        if m["status"] == "live" and m["access"] == "unknown":
            errs.append(f"{m['id']}: live + access inconnu")

    # 1b. marqueurs GEN : un seul bloc bien formé par document machine-owned.
    if COMPARATIF is not None:
        if not COMPARATIF.exists():
            errs.append(f"comparatif absent : {COMPARATIF.relative_to(ROOT)}")
        else:
            try:
                if find_block(COMPARATIF.read_text(encoding="utf-8").splitlines(),
                              GEN_BEGIN) is None:
                    errs.append("comparatif : bloc GEN:comparatif absent")
            except SystemExit as exc:
                errs.append(f"comparatif : {exc}")

    # 2. appariement bijectionnel état <-> fiches (si la plateforme a des fiches)
    paired_rels: set[str] = set()
    if FICHES_DIR is not None:
        for m in state["models"]:
            if not m.get("fiche"):
                errs.append(f"{m['id']}: fiche non appariée (lancez `pair`)")
                continue
            paired_rels.add(m["fiche"])
            if not (ROOT / m["fiche"]).exists():
                errs.append(f"{m['id']}: fichier absent — {m['fiche']}")
        for f in sorted(FICHES_DIR.glob("*.md")):
            rel = f"{FICHES_REL}/{f.name}"
            if rel not in paired_rels:
                errs.append(f"fiche orpheline (absente de l'état) : {rel}")

    # 3. structure de chaque fiche appariée (H1 == id, sections exigées dans l'ordre)
    for m in state["models"]:
        p = fiche_path(m)
        if p is None or not p.exists():
            continue
        flines = p.read_text(encoding="utf-8").splitlines()
        try:
            if find_block(flines, GEN_PRIX_BEGIN) is None:
                errs.append(f"{p.name}: bloc GEN:prix absent")
        except SystemExit as exc:
            errs.append(f"{p.name}: {exc}")
        h1 = next((l for l in flines if l.startswith("# ")), None)
        if h1 is None:
            errs.append(f"{p.name}: H1 absent")
            continue
        head = h1[1:].split(" — ")[0]
        if slugify(head) != m["id"]:
            errs.append(f"{p.name}: H1 « {head} » ne slugsifie pas en « {m['id']} »")
        h2s = [l[3:].strip() for l in flines if l.startswith("## ")]
        idx = -1
        for s in REQUIRED_SECTIONS:
            pos = next(
                (i for i, h in enumerate(h2s) if h == s or h.startswith(s + " ")), None
            )
            if pos is None:
                errs.append(f"{p.name}: section exigée manquante « ## {s} »")
            elif pos < idx:
                errs.append(f"{p.name}: section « {s} » hors ordre")
            else:
                idx = pos
        missing_rec = [
            s for s in RECOMMENDED_SECTIONS
            if not any(h == s or h.startswith(s + " ") for h in h2s)
        ]
        if missing_rec:
            warns.append(f"{p.name}: sections recommandées manquantes — "
                         + ", ".join(missing_rec))

    # 4. le template contient toutes les sections exigées (dérive du contrat)
    if not TEMPLATE.exists():
        errs.append(f"template absent : {TEMPLATE.relative_to(ROOT)}")
    else:
        tpl_h2 = [
            l[3:].strip()
            for l in TEMPLATE.read_text(encoding="utf-8").splitlines()
            if l.startswith("## ")
        ]
        for s in REQUIRED_SECTIONS:
            if s not in tpl_h2:
                errs.append(f"template: section exigée manquante « ## {s} »")

    # 7. §7 : dépréciation (docs Zen du jour) + version d'index AA
    ad = load_adapter(None)
    if any(s.get("type") == "zen_docs" for s in ad.get("sources", [])):
        try:
            day = cache_day(today())
            mf = cache_file(day, "manifest.json", "manifeste de cache")
            man = None
            bodies = None
            if mf.exists():
                _, man = load_cache(today())
                bodies = validate_manifest(day, man, ad)
        except SystemExit as exc:
            errs.append(f"cache du jour invalide : {exc}")
            man = bodies = None
        if man is not None and bodies is not None:
            idx7 = state_index(state)
            for sid, e in man["entries"].items():
                if e.get("type") != "zen_docs":
                    continue
                dep = ex_zen(
                    bodies[sid].decode("utf-8", errors="replace")
                ).get("zen_deprecated") or []
                dep_ids = {mid for mid in (
                    match_model(r["name"], idx7, ad.get("aliases", {}))
                    for r in dep) if mid}
                for mid in sorted(dep_ids & {m["id"] for m in state["models"]}):
                    warns.append(f"{mid}: déprécié (docs Zen du jour) — "
                                 "relecture du claim gratuit requise")
    if FICHES_DIR is not None:
        aa = any("rtificial Analysis" in f.read_text(encoding="utf-8", errors="replace")
                 for f in FICHES_DIR.glob("*.md"))
        if aa:
            iv = state["facts"].get("index_version")
            ev = iv.get("evidence") if isinstance(iv, dict) else None
            if iv is None:
                warns.append("facts.index_version absent alors que les fiches citent "
                             "l'index AA — saisir avec URL+date+preuve")
            elif not (isinstance(ev, dict) and ev.get("url")):
                errs.append("facts.index_version : evidence.url manquant")
            elif ev.get("tier") not in (1, 2, 3):
                errs.append("facts.index_version : evidence.tier manquant")

    # §7-3 : status=retired ⇒ aucune ligne machine (bloc GEN) ne revendique
    # le gratuit/disponible. Prose annotée hors GEN exclue (faux positifs
    # prouvés : encadrés « verdict caduc », claims barrés ~~).
    claim_re = re.compile(r"gratuit|disponible|\bfree\b|0 promo|\b0/h\b", re.I)
    for m in state["models"]:
        if m["status"] != "retired":
            continue
        p = fiche_path(m)
        if p is not None and p.exists():
            gm = re.search(r"<!-- GEN:prix[^>]*-->(.*?)<!-- /GEN -->",
                           p.read_text(encoding="utf-8", errors="replace"), re.S)
            if gm and claim_re.search(gm.group(1)):
                errs.append(f"{p.name}: ligne GEN revendique le gratuit "
                            "alors que status=retired")
        if COMPARATIF is not None and COMPARATIF.exists():
            gc = re.search(r"<!-- GEN:comparatif[^>]*-->(.*?)<!-- /GEN -->",
                           COMPARATIF.read_text(encoding="utf-8", errors="replace"),
                           re.S)
            if gc:
                for line in gc.group(1).splitlines():
                    if line.startswith(f"| {m['display']} |") \
                            and claim_re.search(line):
                        errs.append(f"comparatif: ligne GEN « {m['display']} » "
                                    "revendique le gratuit alors que status=retired")

    if errs:
        sys.exit("lint ÉCHEC:\n  - " + "\n  - ".join(errs))
    n = len(state["models"])
    if warns:
        print(f"lint OK ({n} modèles, appariement + structure + prix) "
              f"avec {len(warns)} avertissement(s) :")
        for w in warns:
            print(f"  ⚠ {w}")
    else:
        print(f"lint OK : {n} modèles, appariement + structure + prix.")


# ============================================== adapters, réseau, diff, apply

def http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "llm-compare-moteur/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        if resp.status != 200:
            raise OSError(f"HTTP {resp.status}")
        body = resp.read(MAX_RESPONSE_BYTES + 1)
        if len(body) > MAX_RESPONSE_BYTES:
            raise OSError(f"réponse trop volumineuse (limite {MAX_RESPONSE_BYTES} octets)")
        return body


def load_adapter(path: Path | None = None) -> dict:
    candidate = path if path is not None else ADAPTER_PATH
    if candidate is None:
        sys.exit("Adaptateur non résolu : appelez setup_platform() d'abord.")
    p = path_within(candidate, MOTEUR / "adapters", "adaptateur")
    if not p.exists():
        sys.exit(f"Adapter absent : {p}")
    try:
        a = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        sys.exit(f"Adapter illisible : {p} — {exc}")
    if not isinstance(a, dict):
        sys.exit(f"Adapter {p.name} : objet JSON attendu.")
    allowed = {"platform", "label", "model_map", "research", "health", "aliases", "sources"}
    extra = set(a) - allowed
    if extra:
        sys.exit(f"Adapter {p.name} : clés inconnues {sorted(extra)}")
    for key in ("platform", "health", "sources"):
        if key not in a:
            sys.exit(f"Adapter {p.name} : clé manquante « {key} »")
    if not isinstance(a["platform"], str) or not re.fullmatch(
        r"[a-z0-9][a-z0-9-]*", a["platform"]
    ):
        sys.exit(f"Adapter {p.name} : identifiant platform invalide.")
    if (not isinstance(a["health"], dict)
            or not isinstance(a["health"].get("url"), str)
            or not isinstance(a["health"].get("must_contain"), str)
            or not a["health"]["must_contain"]):
        sys.exit(f"Adapter {p.name} : health.url et health.must_contain requis.")
    if set(a["health"]) - {"url", "must_contain"}:
        sys.exit(f"Adapter {p.name} : clés health inconnues.")
    if not valid_http_url(a["health"]["url"]):
        sys.exit(f"Adapter {p.name} : health.url HTTP(S) invalide.")
    if not isinstance(a["sources"], list) or not a["sources"]:
        sys.exit(f"Adapter {p.name} : sources doit être une liste non vide.")
    seen: set[str] = set()
    seen_urls: set[str] = set()
    seen_types: set[str] = set()
    for s in a["sources"]:
        if not isinstance(s, dict):
            sys.exit(f"Adapter {p.name} : chaque source doit être un objet.")
        if set(s) - {"id", "url", "tier", "type"}:
            sys.exit(f"Adapter {p.name} : clés inconnues dans la source {s!r}.")
        for k in ("id", "url", "tier", "type"):
            if k not in s:
                sys.exit(f"Adapter {p.name} : source incomplète {s!r}")
        if not isinstance(s["id"], str) or not re.fullmatch(
            r"[A-Za-z0-9][A-Za-z0-9._-]*", s["id"]
        ) or s["id"] in (".", "..", "manifest.json"):
            sys.exit(f"Adapter {p.name} : id de source invalide {s['id']!r}")
        if s["id"] in seen:
            sys.exit(f"Adapter {p.name} : id dupliqué {s['id']}")
        seen.add(s["id"])
        if not valid_http_url(s["url"]):
            sys.exit(f"Adapter {p.name} : URL invalide pour {s['id']!r}")
        if s["url"] in seen_urls:
            sys.exit(f"Adapter {p.name} : URL source dupliquée {s['url']}")
        seen_urls.add(s["url"])
        if type(s["tier"]) is not int or s["tier"] not in (1, 2, 3):
            sys.exit(f"Adapter {p.name} : tier invalide pour {s['id']!r}")
        if not isinstance(s["type"], str) or s["type"] not in SOURCE_TYPES:
            sys.exit(f"Adapter {p.name} : type de source inconnu {s['type']!r}")
        if s["type"] != "raw" and s["type"] in seen_types:
            sys.exit(f"Adapter {p.name} : type de source dupliqué {s['type']!r}")
        seen_types.add(s["type"])
    for key in ("aliases", "model_map"):
        mapping = a.get(key, {})
        if not isinstance(mapping, dict) or any(
            not isinstance(k, str) or not k.strip()
            or not isinstance(v, str)
            or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", v)
            for k, v in mapping.items()
        ):
            sys.exit(f"Adapter {p.name} : {key} doit associer des clés non vides "
                     "à des identifiants d'état valides.")
    research = a.get("research", {})
    if research is None:
        research = {}
    if not isinstance(research, dict):
        sys.exit(f"Adapter {p.name} : research doit être un objet.")
    if set(research) - {"comparatif", "fiches", "rapport"}:
        sys.exit(f"Adapter {p.name} : clés research inconnues.")
    for key in ("comparatif", "fiches", "rapport"):
        if key in research and research[key] is not None:
            target = project_path(research[key], f"research.{key}")
            if target.exists() and (target.is_dir() if key != "fiches" else target.is_file()):
                expected = "un dossier" if key == "fiches" else "un fichier"
                sys.exit(f"Adapter {p.name} : research.{key} doit désigner {expected}.")
    if "label" in a and (
        not isinstance(a["label"], str) or not a["label"].strip()
        or a["label"] != a["label"].strip()
        or any(c in a["label"] for c in "|\r\n")
    ):
        sys.exit(f"Adapter {p.name} : label invalide pour le rendu Markdown.")
    return a


def norm_id(s: str) -> str:
    """slug + suppression du « v » de version : mimo-v2-6 <-> MiMo 2.6."""
    return re.sub(r"(?<=[a-z-])v(?=\d)", "", slugify(s))


def digit_insert(s: str) -> str:
    return re.sub(r"(?<=[a-z])(?=\d)", "-", s)


def state_index(state: dict) -> dict[str, str]:
    """Variantes normalisées d'un id -> id canonique, sans collisions."""
    idx: dict[str, str] = {}
    for m in state["models"]:
        for variant in {m["id"], slugify(m["id"]), norm_id(m["id"])}:
            previous = idx.get(variant)
            if previous is not None and previous != m["id"]:
                sys.exit(f"ÉTAT INVALIDE : normalisation ambiguë « {variant} » "
                         f"pour {previous!r} et {m['id']!r}.")
            idx[variant] = m["id"]
    return idx


def match_model(raw: str, index: dict[str, str], aliases: dict[str, str],
                comment: str | None = None) -> str | None:
    """Nom rencontré dans une source -> id d'état, ou None (non apparié = signalé).

    Candidats, dans l'ordre : alias déclaré ; commentaire humain de la ligne
    (seul, puis préfixé vendor : « V4.1 Flash » + deepseek/... -> deepseek-v4-1-flash) ;
    id brut et id de base (sans vendor) ; formes normalisées (v de version, jointure
    chiffre/alphabet : solar-pro4 -> solar-pro-4)."""
    if raw in aliases:
        return aliases[raw]
    vendor = raw.split("/")[0] if "/" in raw else ""
    base = raw.split("/")[-1]
    cands: list[str] = []
    if comment:
        cands += [slugify(comment), norm_id(comment)]
        if vendor:
            cands.append(f"{slugify(vendor)}-{slugify(comment)}")
    cands += [slugify(raw), norm_id(raw), slugify(base), digit_insert(slugify(base))]
    if vendor:
        cands += [
            f"{slugify(vendor)}-{norm_id(base)}",
            f"{slugify(vendor)}-{slugify(base)}",
        ]
    matches = list(dict.fromkeys(index[c] for c in cands if c in index))
    if len(matches) > 1:
        sys.exit(f"Appariement ambigu pour {raw!r} : {matches}. "
                 "Ajoutez un alias explicite dans l'adaptateur.")
    return matches[0] if matches else None


def comment_display(c: str | None) -> str | None:
    """« Solar Pro 4 (2026-10-05): free as a promotion » -> « Solar Pro 4 »."""
    if not c:
        return None
    return re.split(r"\s\(|:|'s |,", c)[0].strip()


# ------------------------------------------------------------ extracteurs

def ex_llms(text: str) -> dict:
    catalog: list[str] = []
    allocations: list[dict] = []
    seen_alloc: dict[str, int] = {}
    seen_catalog: set[str] = set()
    mode: str | None = None
    catalog_done = False
    catalog_unparsed = 0
    allocation_unparsed = 0
    for line in text.splitlines():
        if line.startswith("### "):
            if mode == "models":
                catalog_done = True
            h = line[4:].lower()
            mode = None
            if not catalog_done and "model" in h:
                mode = "models"
            elif "countries" in h or "freebucks" in h:
                mode = "alloc"
            continue
        if line.startswith("## "):
            mode = None
            continue
        if mode == "models":
            m = re.match(r"^- ([^:]+):\s+\S", line)
            if m:
                name = m.group(1).strip()
                if name in seen_catalog:
                    catalog_unparsed += 1
                else:
                    seen_catalog.add(name)
                    catalog.append(name)
            elif line.startswith("- "):
                catalog_unparsed += 1
        elif mode == "alloc":
            m = re.match(r"^- (.+?):\s*(\d+)\b", line)
            if m:
                entry = (m.group(1).strip(), int(m.group(2)))
                if entry[0] in seen_alloc:
                    allocation_unparsed += 1
                else:
                    seen_alloc[entry[0]] = entry[1]
                    allocations.append({"scope": entry[0], "freebucks": entry[1]})
            elif line.startswith("- "):
                allocation_unparsed += 1
    if not allocations:
        # Format en prose (depuis 2026-10) : phrases stables de la FAQ.
        # Les deux formats échouant ensemble => 0 extrait => signal « format changé ».
        def add(scope: str, n: int) -> None:
            nonlocal allocation_unparsed
            if scope in seen_alloc:
                if seen_alloc[scope] != n:
                    allocation_unparsed += 1
                return
            seen_alloc[scope] = n
            allocations.append({"scope": scope, "freebucks": n})

        for pat, scope in (
            (r"free limited-access allowance is (\d+) Freebucks a day", "limited"),
            (r"or (\d+) on a VPN or proxy", "vpn"),
        ):
            m = re.search(pat, text)
            if m:
                add(scope, int(m.group(1)))
        m = re.search(r"include (\d+) a day on Starter, (\d+) on Plus, or (\d+) on Pro", text)
        if m:
            for scope, g in (("starter", 1), ("plus", 2), ("pro", 3)):
                add(scope, int(m.group(g)))
    return {
        "catalog": catalog,
        "allocations": allocations,
        "catalog_unparsed": catalog_unparsed,
        "allocation_unparsed": allocation_unparsed,
    }


def classify_access(raw: str) -> str | None:
    if raw.startswith("US"):
        return "us_only"
    if raw == "Paid plans":
        return "paid_only"
    if raw.startswith("Full"):
        return "free"
    return None


def ex_readme(text: str) -> dict:
    access: dict[str, str] = {}
    in_access_table = False
    unparsed = 0
    for line in text.splitlines():
        if line.startswith("|") and "model" in line.lower() and "access" in line.lower():
            in_access_table = True
            continue
        if not in_access_table:
            continue
        if not line.strip():
            in_access_table = False
            continue
        if not line.startswith("|"):
            unparsed += 1
            continue
        if re.match(r"^\|\s*:?-{2,}", line):
            continue
        m = re.match(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*([^|]+?)\s*\|", line)
        if not m:
            unparsed += 1
            continue
        name, value = m.group(1).strip(), m.group(2).strip()
        if name in access:
            unparsed += 1
            continue
        access[name] = value
    return {"access": access, "unparsed": unparsed}


def ex_picker(text: str) -> dict:
    placements: list[dict] = []
    seen: set[str] = set()
    unparsed = 0
    comment: str | None = None
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines)
                  if re.search(r"\bconst\s+PLACEMENTS\b", line)), None)
    end = next((i for i in range((start + 1) if start is not None else len(lines),
                                 len(lines))
                if lines[i].strip() == "})"), None)
    if start is None or end is None:
        return {"placements": [], "unparsed": 1}
    block = "\n".join(lines[start + 1:end])
    expected = len(re.findall(r"^\s*['\"][^'\"]+['\"]\s*:\s*\{", block, re.M))
    i = start + 1
    while i < end:
        line = lines[i].strip()
        i += 1
        if line.startswith("//"):
            comment = line.lstrip("/ ").strip()
            continue
        m = re.match(r"^'([^']+)':\s*\{(.*)$", line)
        if not m:
            continue
        raw_id, rest = m.group(1), m.group(2)
        if raw_id in seen:
            unparsed += 1
            continue
        seen.add(raw_id)
        trailing = re.search(r"//\s*(.+)$", rest)
        tail = trailing.group(1).strip() if trailing else None
        sm = re.search(r"section:\s*'(\w+)'", rest)
        section = sm.group(1) if sm else None
        if section is None:
            while i < end:
                sub = lines[i].strip()
                i += 1
                sm2 = re.search(r"section:\s*'(\w+)'", sub)
                if sm2:
                    section = sm2.group(1)
                    break
                if sub.startswith("}"):
                    break
        placements.append({"raw": raw_id, "section": section, "comment": tail or comment})
        comment = None
    unparsed += max(0, expected - len(placements) - unparsed)
    return {"placements": placements, "unparsed": unparsed}


def ex_solar(text: str) -> dict:
    offers = {
        m.group(1): int(m.group(2))
        for m in re.finditer(r"(\w*OFFER)\s*=\s*\{\s*price:\s*(\d+)", text)
    }
    changes: list[dict] = []
    seen: set[tuple[str, str]] = set()
    unparsed = 0
    body = re.search(r"SOLAR_PRICE_CHANGES\s*=\s*\[(.*?)\n\s*\]", text, re.S)
    if body:
        expected = len(re.findall(r"^\s*\{", body.group(1), re.M))
        for block in re.finditer(r"\{(.*?)\}", body.group(1), re.S):
            b = block.group(1)
            at = re.search(r"at:\s*'([^']+)'", b)
            model = re.search(r"modelId:\s*(\w+)", b)
            if not (at and model):
                unparsed += 1
                continue
            key = (model.group(1), at.group(1))
            if key in seen:
                unparsed += 1
                continue
            seen.add(key)
            pm = re.search(r"price:\s*(\d+)", b)
            spread = re.search(r"\.\.\.(\w+)", b)
            if pm:
                price: int | None = int(pm.group(1))
            elif spread and spread.group(1) in offers:
                price = offers[spread.group(1)]
            else:
                price = None
            tag = re.search(r"tagline:\s*'((?:[^'\\]|\\.)*)'", b)
            changes.append({
                "at": at.group(1),
                "raw_model": model.group(1),
                "model": SOLAR_MODEL_MAP.get(model.group(1)),
                "price": price,
                "tagline": tag.group(1) if tag else None,
            })
        unparsed += max(0, expected - len(changes) - unparsed)
    return {
        "solar_changes": changes,
        "solar_promo_active": "SOLAR_PRO_4_PROMOTIONAL" in text,
        "solar_unparsed": unparsed,
    }


def ex_plans(text: str) -> dict:
    rows: list[dict] = []
    tr_rows = re.findall(r"<tr\b[^>]*>.*?</tr>", text, re.S | re.I)
    candidates = [
        row for row in tr_rows
        if re.search(r"<th\b(?=[^>]*\bscope\s*=\s*['\"]row['\"])", row, re.I)
    ]
    for row_html in candidates:
        m = re.search(
            r"<th\b(?=[^>]*\bscope\s*=\s*['\"]row['\"])[^>]*>(.*?)</th>"
            r"((?:\s*<td\b[^>]*>.*?</td>)+)",
            row_html, re.S | re.I,
        )
        if not m:
            continue
        raw_th = m.group(1)
        badges = re.findall(r"pricing-model-promo\">([^<]+)<", raw_th)
        display = re.sub(r"<span[^>]*>.*?</span>", "", raw_th)
        display = re.sub(r"<[^>]+>", "", display).strip()
        hours = [
            re.sub(r"<[^>]+>", "", td).strip()
            for td in re.findall(r"<td\b[^>]*>(.*?)</td>", m.group(2), re.S | re.I)
        ]
        rows.append({"display": display, "badges": badges, "hours": hours})
    return {"rows": rows, "unparsed_rows": len(candidates) - len(rows)}


def ex_rss(text: str) -> dict:
    items: list[dict] = []
    unparsed = 0
    for m in re.finditer(r"<item>(.*?)</item>", text, re.S):
        blk = m.group(1)
        t = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", blk, re.S)
        d = re.search(r"<pubDate>(.*?)</pubDate>", blk, re.S)
        when = None
        if d:
            try:
                when = email.utils.parsedate_to_datetime(d.group(1).strip()).isoformat()
            except (TypeError, ValueError):
                when = d.group(1).strip()
        title = t.group(1).strip() if t else "?"
        if title == "?" or parse_datetime(when) is None:
            unparsed += 1
        items.append({"title": title, "pubDate": when})
    return {"items": items, "unparsed": unparsed}


def _row_cells(row_html: str) -> list[str]:
    """Texte de chaque cellule d'un <tr>/<thead> (boutons/svg scripts écartés)."""
    out: list[str] = []
    for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row_html, re.S):
        c = re.sub(r"<button.*?</button>", "", c, flags=re.S)
        c = re.sub(r"<svg.*?</svg>", "", c, flags=re.S)
        c = re.sub(r"<[^>]+>", " ", c)
        out.append(" ".join(c.split()))
    return out


def ex_zen(text: str) -> dict:
    """Docs Zen (opencode.ai/docs/zen) : lane free + table « Deprecated models ».

    Lignes Input=Free => lane free documentée (la doc dit elle-même
    « for a limited time »). La table de config est écartée via son en-tête
    (Input/Output). La section « Deprecated models » (h3 id=deprecated-models,
    colonnes Model | Deprecation date) est extraite en noms d'affichage —
    appariement à l'état côté build_observation."""
    free: list[str] = []
    unparsed = 0
    for tb in re.findall(r"<table[^>]*>.*?</table>", text, re.S):
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", tb, re.S)
        if not rows:
            continue
        hdr = _row_cells(rows[0])
        if "Input" not in hdr or "Output" not in hdr:
            continue
        for r in rows[1:]:
            cells = _row_cells(r)
            if len(cells) < 4:
                unparsed += 1
            elif cells[1] == "Free":
                free.append(cells[0])
    dep: list[dict] = []
    i = text.find('id="deprecated-models"')
    if i != -1:
        seg = text[i:]
        end = re.search(r'<h[234][^>]*id="(?!deprecated-models)', seg)
        if end:
            seg = seg[:end.start()]
        for r in re.findall(r"<tr[^>]*>(.*?)</tr>", seg, re.S):
            cells = _row_cells(r)
            if len(cells) >= 2 and cells[0] != "Model":
                dep.append({"name": cells[0], "date": cells[1]})
    return {"zen_lane": free, "zen_deprecated": dep, "zen_unparsed_rows": unparsed}


def ex_zcatalog(text: str) -> dict:
    """Catalogue models.opencode.ai (dataset Models.dev) : prix par modèle.

    « $0.00 / $0.00 » = cost0 **explicite** dans models.dev/api.json — distinct
    de « cost omis » (anomalyco/opencode#29971 : l'omis s'affiche aussi $0 chez
    le client). ids normalisés via slugify (alignés sur l'état, vérifié 13/13)."""
    zero: list[str] = []
    paid: list[str] = []
    unparsed = 0
    seen: set[str] = set()
    for m in re.finditer(
        r"<tr\b(?=[^>]*\bdata-search\s*=)[^>]*>(.*?)</tr>", text, re.S | re.I
    ):
        cells = _row_cells(m.group(1))
        if len(cells) != 9 or not re.fullmatch(r"\$[\d.]+ / \$[\d.]+", cells[4]):
            unparsed += 1
            continue
        mid = slugify(cells[1])
        if mid in seen:
            unparsed += 1
            continue
        seen.add(mid)
        (zero if cells[4] == "$0.00 / $0.00" else paid).append(mid)
    return {"cat_zero": zero, "cat_paid": paid, "cat_unparsed_rows": unparsed}


def ex_vserved(text: str) -> dict:
    """GET /zen/v1/models (opérateur, sans auth) : ids réellement servis.

    Observation datée : exclut les entrées legacy du catalogue (vérifié sur
    8/9 payants legacy absents) — l'absence = « non servi ce jour », pas une
    preuve de retrait définitif."""
    try:
        data = json.loads(text)
    except ValueError:
        return {"served": []}
    rows = data.get("data") if isinstance(data, dict) else None
    if not isinstance(rows, list):
        return {"served": []}
    served: list[str] = []
    seen: set[str] = set()
    invalid = 0
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
            invalid += 1
            continue
        mid = slugify(row["id"])
        if mid in seen:
            invalid += 1
            continue
        seen.add(mid)
        served.append(mid)
    return {"served": served, "invalid_rows": invalid}


# ------------------------------------------------------------ fetch / cache

def cmd_fetch(args) -> None:
    adapter = load_adapter()
    health = adapter["health"]
    try:
        probe = http_get(health["url"]).decode("utf-8", errors="replace")
    except Exception as exc:
        sys.exit(f"fetch ABORT (santé) : {health['url']} -> {exc}")
    if health.get("must_contain") and health["must_contain"] not in probe:
        sys.exit(f"fetch ABORT (santé) : {health['url']} ne contient pas "
                 f"{health['must_contain']!r}")

    day = cache_day(today())
    mf = cache_file(day, "manifest.json", "manifeste de cache")
    prev: dict = {}
    if not args.revalidate and mf.exists():
        try:
            previous_manifest = json.loads(mf.read_text(encoding="utf-8"))
            if (isinstance(previous_manifest, dict)
                    and previous_manifest.get("platform", FN_KEY) == FN_KEY
                    and isinstance(previous_manifest.get("entries"), dict)):
                prev = previous_manifest["entries"]
        except (OSError, json.JSONDecodeError):
            print(f"  manifeste de cache illisible, téléchargement complet : {mf}",
                  file=sys.stderr)

    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    entries: dict[str, dict] = {}
    blobs: list[tuple[Path, bytes]] = []
    errs: list[str] = []
    reused = 0
    for s in adapter["sources"]:
        old = prev.get(s["id"])
        if (isinstance(old, dict) and old.get("url") == s["url"]
                and old.get("tier") == s["tier"] and old.get("type") == s["type"]
                and valid_datetime(old.get("fetched_at"))):
            try:
                old_file = cache_file(day, old.get("file"), f"cache {s['id']}")
                old_body = old_file.read_bytes()
                old_hash = old.get("sha1")
                old_size = old.get("bytes")
                if (isinstance(old_hash, str)
                        and hashlib.sha1(old_body).hexdigest() == old_hash
                        and len(old_body) <= MAX_RESPONSE_BYTES
                        and ("bytes" not in old or
                             (type(old_size) is int and old_size == len(old_body)))):
                    filename = f"{s['id']}-{old_hash}"
                    entries[s["id"]] = {
                        "url": s["url"],
                        "tier": s["tier"],
                        "type": s["type"],
                        "sha1": old_hash,
                        "file": filename,
                        "bytes": len(old_body),
                        "fetched_at": old["fetched_at"],
                    }
                    if old_file.name != filename:
                        blobs.append((cache_file(day, filename), old_body))
                    reused += 1
                    print(f"  {s['id']:<16} réutilisé (cache du jour, sha1:{old_hash[:12]})")
                    continue
            except (OSError, SystemExit):
                pass
            print(f"  {s['id']:<16} cache invalide, nouveau téléchargement")
        try:
            body = http_get(s["url"])
        except Exception as exc:
            errs.append(f"{s['id']} ({s['url']}) : {exc}")
            continue
        digest = hashlib.sha1(body).hexdigest()
        filename = f"{s['id']}-{digest}"
        entries[s["id"]] = {
            "url": s["url"],
            "tier": s["tier"],
            "type": s["type"],
            "sha1": digest,
            "file": filename,
            "bytes": len(body),
            "fetched_at": now,
        }
        blobs.append((cache_file(day, filename), body))
        print(f"  {s['id']:<16} tier {s['tier']} {len(body):>8} o  "
              f"sha1:{entries[s['id']]['sha1'][:12]}")
    if errs:
        sys.exit("fetch ABORT (aucun cache écrit) :\n  - " + "\n  - ".join(errs))

    manifest = {"platform": FN_KEY, "fetched_at": now, "entries": entries}
    manifest_text = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    atomic_write_many(blobs + [(mf, manifest_text.encode("utf-8"))])
    mode = "revalidé (--revalidate)" if args.revalidate else "cache du jour"
    print(f"fetch OK : {len(entries) - reused} téléchargée(s), {reused} réutilisée(s) "
          f"[{mode}] -> {day.relative_to(ROOT)}")


def load_cache(date_str: str) -> tuple[Path, dict]:
    day = cache_day(date_str)
    mf = cache_file(day, "manifest.json", "manifeste de cache")
    if not mf.exists():
        sys.exit(f"Cache absent : {mf} — lancez `fetch`.")
    try:
        manifest = json.loads(mf.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        sys.exit(f"Manifeste de cache illisible : {mf} — {exc}")
    if not isinstance(manifest, dict):
        sys.exit(f"Manifeste de cache invalide : objet JSON attendu ({mf}).")
    return day, manifest


def validate_manifest(day: Path, manifest: dict, adapter: dict) -> dict[str, bytes]:
    """Vérifie l'identité, la complétude et l'intégrité de chaque source."""
    if manifest.get("platform", FN_KEY) != FN_KEY:
        sys.exit(f"Cache d'une autre plateforme : {manifest.get('platform')!r}.")
    if not valid_datetime(manifest.get("fetched_at")):
        sys.exit("Manifeste invalide : fetched_at global absent ou illisible.")
    entries = manifest.get("entries")
    if not isinstance(entries, dict):
        sys.exit("Manifeste invalide : entries doit être un objet.")
    expected = {source["id"]: source for source in adapter["sources"]}
    if set(entries) != set(expected):
        missing = sorted(set(expected) - set(entries))
        extra = sorted(set(entries) - set(expected))
        sys.exit(f"Manifeste incomplet/inattendu : manquantes={missing}, extras={extra}.")
    bodies: dict[str, bytes] = {}
    for sid, source in expected.items():
        entry = entries[sid]
        if not isinstance(entry, dict):
            sys.exit(f"Manifeste invalide : entrée {sid!r} doit être un objet.")
        for key in ("url", "tier", "type", "sha1", "file"):
            if key not in entry:
                sys.exit(f"Manifeste invalide : {sid!r} sans {key}.")
        if (not isinstance(entry["url"], str) or entry["url"] != source["url"]
                or type(entry["tier"]) is not int or entry["tier"] != source["tier"]
                or not isinstance(entry["type"], str) or entry["type"] != source["type"]):
            sys.exit(f"Manifeste périmé : configuration de source différente pour {sid!r}.")
        fetched_at = entry.get("fetched_at", manifest["fetched_at"])
        if not valid_datetime(fetched_at):
            sys.exit(f"Manifeste invalide : fetched_at illisible pour {sid!r}.")
        if not isinstance(entry["sha1"], str) or not re.fullmatch(
            r"[0-9a-f]{40}", entry["sha1"]
        ):
            sys.exit(f"Manifeste invalide : SHA-1 illisible pour {sid!r}.")
        body_path = cache_file(day, entry["file"], f"cache {sid}")
        try:
            body = body_path.read_bytes()
        except OSError as exc:
            sys.exit(f"Fichier de cache absent/illisible pour {sid!r} : {exc}")
        if hashlib.sha1(body).hexdigest() != entry["sha1"]:
            sys.exit(f"Intégrité du cache violée pour {sid!r} : SHA-1 différent.")
        if "bytes" in entry and (
            type(entry["bytes"]) is not int or entry["bytes"] != len(body)
        ):
            sys.exit(f"Intégrité du cache violée pour {sid!r} : taille différente.")
        if len(body) > MAX_RESPONSE_BYTES:
            sys.exit(f"Cache invalide pour {sid!r} : corps trop volumineux.")
        bodies[sid] = body
    return bodies


def build_observation(day: Path, manifest: dict, state: dict, adapter: dict) -> tuple[dict, list[str]]:
    source_bodies = validate_manifest(day, manifest, adapter)
    obs: dict = {}
    problems: list[str] = []
    idx = state_index(state)
    state_empty = not idx  # état vide : on ne crie pas « non apparié » N fois
    state_ids = {m["id"] for m in state["models"]}
    aliases = adapter.get("aliases", {})
    invalid_aliases = {
        name: target for name, target in aliases.items() if target not in state_ids
    }
    if invalid_aliases and not state_empty:
        for name, target in sorted(invalid_aliases.items()):
            problems.append(f"alias adaptateur invalide : {name!r} -> {target!r} "
                            "(cible absente de l'état)")
    aliases = {name: target for name, target in aliases.items()
               if target in state_ids}
    for sid, meta in manifest["entries"].items():
        t = meta["type"]
        if t == "raw":
            continue
        try:
            text = source_bodies[sid].decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            problems.append(f"source {sid!r} : texte UTF-8 invalide ({exc}) "
                            "— apply bloqué")
            continue
        if t == "llms_txt":
            obs.update(ex_llms(text))
        elif t == "readme_md":
            extracted = ex_readme(text)
            obs["access_raw"] = extracted["access"]
            if extracted["unparsed"]:
                problems.append(f"README : {extracted['unparsed']} ligne(s) "
                                "d'accès illisible(s) — apply bloqué")
        elif t == "picker_ts":
            extracted = ex_picker(text)
            obs["placements"] = extracted["placements"]
            if extracted["unparsed"]:
                problems.append(f"picker : {extracted['unparsed']} entrée(s) "
                                "illisible(s) — apply bloqué")
        elif t == "solar_promo_ts":
            obs.update(ex_solar(text))
            if obs.get("solar_unparsed"):
                problems.append(f"solar-promo : {obs['solar_unparsed']} "
                                "transition(s) illisible(s) — apply bloqué")
        elif t == "plans_html":
            extracted = ex_plans(text)
            obs["plans_rows"] = extracted["rows"]
            if extracted["unparsed_rows"]:
                problems.append(f"/plans : {extracted['unparsed_rows']} ligne(s) "
                                "de modèle illisible(s) — apply bloqué")
        elif t == "rss":
            extracted = ex_rss(text)
            obs["feed_items"] = extracted["items"]
            if extracted["unparsed"]:
                problems.append(f"feed : {extracted['unparsed']} élément(s) "
                                "sans titre/date exploitable — apply bloqué")
        elif t == "zen_docs":
            extracted = ex_zen(text)
            obs.update(extracted)
            if extracted["zen_unparsed_rows"]:
                problems.append(f"zen docs : {extracted['zen_unparsed_rows']} "
                                "ligne(s) de modèle illisible(s) — apply bloqué")
        elif t == "zen_catalog":
            extracted = ex_zcatalog(text)
            obs.update(extracted)
            if extracted["cat_unparsed_rows"]:
                problems.append(f"zen_catalog : {extracted['cat_unparsed_rows']} "
                                "ligne(s) illisible(s) — apply bloqué")
        elif t == "v1_models":
            extracted = ex_vserved(text)
            obs.update(extracted)
            if extracted.get("invalid_rows"):
                problems.append(f"v1/models : {extracted['invalid_rows']} "
                                "entrée(s) invalide(s) — apply bloqué")
        else:
            problems.append(f"type de source inconnu : {t} ({sid})")

    if obs.get("catalog_unparsed"):
        problems.append(f"catalogue : {obs['catalog_unparsed']} ligne(s) illisible(s) "
                        "— apply bloqué")
    if obs.get("allocation_unparsed"):
        problems.append(f"allocations : {obs['allocation_unparsed']} ligne(s) illisible(s) "
                        "— apply bloqué")
    if "catalog" in obs:
        resolved = []
        for name in obs["catalog"]:
            mid = match_model(name, idx, aliases)
            if mid:
                if mid in resolved:
                    problems.append(f"catalogue : entrée dupliquée pour {mid!r}")
                    continue
                resolved.append(mid)
            elif not state_empty:
                problems.append(f"catalogue : modèle non apparié {name!r}")
        obs["catalog_ids"] = resolved
    if "zen_lane" in obs:
        resolved = []
        for name in obs["zen_lane"]:
            mid = match_model(name, idx, aliases)
            if mid:
                if mid in resolved:
                    problems.append(f"zen docs : entrée lane dupliquée pour {mid!r}")
                    continue
                resolved.append(mid)
            elif not state_empty:
                problems.append(f"zen docs : modèle lane non apparié {name!r}")
        obs["zen_lane_ids"] = resolved
    if "zen_deprecated" in obs:
        # non apparié = normal (les dépréciés sont hors état) : pas de problème
        obs["zen_deprecated_ids"] = [
            mid for mid in (match_model(row["name"], idx, aliases)
                            for row in obs["zen_deprecated"]) if mid
        ]
    if "access_raw" in obs:
        acc: dict[str, str] = {}
        for name, raw in obs["access_raw"].items():
            mid = match_model(name, idx, aliases)
            if mid:
                if mid in acc:
                    problems.append(f"README : plusieurs lignes d'accès pour {mid!r}")
                    continue
                acc[mid] = raw
            elif not state_empty:
                problems.append(f"README : ligne non appariée {name!r} ({raw!r})")
        obs["access"] = acc
    valid_placements = []
    seen_placements: set[str] = set()
    for pl in obs.get("placements", []):
        if pl.get("section") not in VALID_SECTIONS:
            problems.append(f"picker : section absente/invalide pour {pl['raw']!r} "
                            f"({pl.get('section')!r}) — apply bloqué")
            continue
        mid = match_model(pl["raw"], idx, aliases,
                          comment=comment_display(pl.get("comment")))
        if mid:
            if mid in seen_placements:
                problems.append(f"picker : plusieurs placements pour {mid!r}")
                continue
            pl["id"] = mid
            valid_placements.append(pl)
            seen_placements.add(mid)
        elif not state_empty:
            problems.append(f"picker : modèle non apparié {pl['raw']!r}")
    if "placements" in obs:
        obs["placements"] = valid_placements
    if "solar_changes" in obs:
        valid_changes = []
        for change in obs["solar_changes"]:
            if change.get("price") is None:
                problems.append(f"solar-promo : prix illisible pour "
                                f"{change.get('raw_model')!r} à {change.get('at')!r} "
                                "— apply bloqué")
                continue
            if not valid_datetime(change.get("at")):
                problems.append(f"solar-promo : date invalide pour "
                                f"{change.get('raw_model')!r} — apply bloqué")
                continue
            valid_changes.append(change)
        obs["solar_changes"] = valid_changes
    # Provenance : sha1 du cache vs sha1 de l'état (par url).
    obs["sources_meta"] = [
        {"id": sid, "type": e["type"], "url": e["url"], "tier": e["tier"],
         "sha1": e["sha1"],
         "fetched_at": e.get("fetched_at") or manifest["fetched_at"]}
        for sid, e in manifest["entries"].items()
    ]
    if "plans_rows" in obs:
        ids = []
        for row in obs["plans_rows"]:
            mid = match_model(row["display"], idx, aliases)
            row["id"] = mid
            if mid:
                if mid in ids:
                    problems.append(f"/plans : plusieurs lignes pour {mid!r}")
                    continue
                ids.append(mid)
            elif not state_empty:
                problems.append(f"/plans : ligne non appariée {row['display']!r}")
        obs["plans_ids"] = ids
    if "feed_items" in obs:
        # Événements du feed (tier 2) : dernier événement connu par modèle.
        # « X withdrawn/replaced by » = out ; « X returns/joins/added » ou
        # « X replaces Y in » = in (X) / out (Y). Non apparié = modèle jamais
        # suivi, normal — pas de problème.
        feed_ev: dict[str, tuple[dt.datetime, dict]] = {}
        for it in obs["feed_items"]:
            raw = (it.get("title") or "").strip()
            t = re.sub(r"^\[[^\]]+\]\s*", "", raw)
            when = it.get("pubDate") or ""
            instant = parse_datetime(when)
            if instant is None:
                continue
            evs: list[tuple[str, str]] = []
            mo = re.match(r"(.+?)\s+withdrawn\b", t, re.I)
            if mo:
                evs.append((mo.group(1), "out"))
            mo = re.match(r"(.+?)\s+replaced\b", t, re.I)
            if mo:
                evs.append((mo.group(1), "out"))
            mo = re.match(r"(.+?)\s+replaces\s+(.+?)\s+in\b", t, re.I)
            if mo:
                evs.append((mo.group(2), "out"))
                evs.append((mo.group(1), "in"))
            mo = re.match(r"(.+?)\s+returns?\s+to\b", t, re.I)
            if mo:
                evs.append((mo.group(1), "in"))
            mo = re.match(r"(.+?)\s+joins?\b", t, re.I)
            if mo:
                evs.append((mo.group(1), "in"))
            mo = re.match(r"(.+?)\s+added\s+to\b", t, re.I)
            if mo:
                evs.append((mo.group(1), "in"))
            for name, act in evs:
                mid = match_model(name.strip(), idx, aliases)
                if not mid:
                    continue
                prev = feed_ev.get(mid)
                if prev is None or instant >= prev[0]:
                    feed_ev[mid] = (
                        instant, {"act": act, "when": when, "title": raw}
                    )
        obs["feed_events"] = {mid: entry for mid, (_, entry) in feed_ev.items()}
    return obs, problems


def _aware(x: dt.datetime) -> dt.datetime:
    return x if x.tzinfo else x.replace(tzinfo=dt.timezone.utc)


def previous_recorded_price(model: dict, at: str) -> object:
    """Dernier prix enregistré avant l'événement, ou None si l'historique ne le sait pas."""
    instant = parse_datetime(at)
    if instant is None:
        return None
    previous = [
        (when, event.get("to"))
        for event in model.get("history", [])
        if event.get("field") == "price"
        and (when := parse_datetime(event.get("at"))) is not None
        and when < instant
    ]
    return max(previous, key=lambda item: item[0])[1] if previous else None


def compute_changes(state: dict, obs: dict, adapter: dict) -> dict:
    """Le cœur : observé vs état. Auto = appliqué par `apply` ; structurel/à
    vérifier/problèmes = jugement humain. Extrait vide => problème (jamais de
    masse-retrait silencieux si un format de source change).

    Chaque logique ne tourne QUE si l'adapter déclare la source correspondante
    (2e plateforme sans llms.txt/picker/plans => pas de fausses alarmes), et un
    état vide compte sans comparer (backfill d'abord)."""
    report: list[str] = []
    auto: list[dict] = []
    structural: list[str] = []
    verify: list[str] = []
    problems: list[str] = []
    by_id = {m["id"]: m for m in state["models"]}
    stypes = {s["type"] for s in adapter["sources"]}
    has_models = bool(state["models"])
    catalog_ids = obs.get("catalog_ids")

    if not has_models:
        n_obs = len(obs.get("catalog") or []) + len(obs.get("zen_lane") or [])
        report.append(f"état vide : {n_obs} observation(s), 0 modèle dans l'état")
        if n_obs:
            structural.append("ÉTAT VIDE — backfill requis (import ou saisie) "
                              "avant tout diff de contenu")

    if "llms_txt" in stypes:
        if not catalog_ids:
            if has_models:
                problems.append("llms.txt : 0 modèle extrait (format changé ?) "
                                "— logique catalogue suspendue")
            live_ids: set[str] = set()
        else:
            live_ids = {m["id"] for m in state["models"] if m["status"] == "live"}
            observed = set(catalog_ids)
            for mid in sorted(live_ids - observed):
                structural.append(f"RETRAIT probable : {mid} (live dans l'état, absent de llms.txt)")
            for mid in sorted(observed - live_ids):
                structural.append(f"RÉAPPARITION/NOUVEAU : {mid} (dans llms.txt, status={by_id[mid]['status']})")
            report.append(f"catalogue : {len(observed)} observés / {len(live_ids)} live dans l'état")

    if "zen_docs" in stypes:
        lane = obs.get("zen_lane_ids")
        if lane is None:
            problems.append("zen docs : source absente du cache")
        elif not lane:
            if has_models:
                problems.append("zen docs : 0 modèle free extrait (format changé ?) "
                                "— logique lane suspendue")
        else:
            live = {m["id"] for m in state["models"] if m["status"] == "live"}
            observed = set(lane)
            # gratuité toujours affichée par le catalogue (0.00 ou payant)
            # = la gate catalogue porte le retrait ; catalogue cassé = silence.
            covered = set(obs.get("cat_zero") or []) | set(obs.get("cat_paid") or [])
            cat_broken = "zen_catalog" in stypes and not covered
            if not cat_broken:
                for mid in sorted((live - observed) - covered):
                    structural.append(f"RETRAIT lane : {mid} (live dans l'état, "
                                      f"plus free dans la lane Zen)")
            for mid in sorted(observed - live):
                structural.append(f"RÉAPPARITION lane : {mid} (free dans la lane Zen, "
                                  f"status={by_id[mid]['status']})")
            report.append(f"lane free Zen : {len(observed)} observés / "
                          f"{len(live)} live dans l'état")
        # « Deprecated models » (même page) : un modèle déprécié encore présent
        # dans l'état = claim gratuit à recouper — jamais de retrait auto.
        dep_rows = obs.get("zen_deprecated")
        if lane is not None:
            if not dep_rows:
                problems.append("zen docs : section « Deprecated models » introuvable "
                                "— logique dépréciation suspendue")
            else:
                known = {m["id"] for m in state["models"]}
                dep_ids = set(obs.get("zen_deprecated_ids") or [])
                for mid in sorted(dep_ids & known):
                    verify.append(f"modèle déprécié : {mid} — listé « Deprecated "
                                  f"models » (docs Zen), présent dans l'état — à recouper")
                report.append(f"dépréciés docs : {len(dep_rows)} dont "
                              f"{len(dep_ids & known)} présent(s) dans l'état")

    if "zen_catalog" in stypes:
        if "cat_zero" not in obs:
            problems.append("zen_catalog : source absente du cache")
        else:
            zero = set(obs["cat_zero"])
            paid = set(obs.get("cat_paid") or [])
            if not zero and not paid:
                problems.append("zen_catalog : 0 ligne extraite (format changé ?) "
                                "— logique catalogue suspendue")
            elif has_models:
                lane_obs = set(obs.get("zen_lane_ids") or [])
                live = {m["id"] for m in state["models"] if m["status"] == "live"}
                in_cat = zero | paid
                for mid in sorted((live & paid) - lane_obs):
                    structural.append(f"RETRAIT prix : {mid} (payant au catalogue, "
                                      f"free dans l'état)")
                for mid in sorted((live & paid) & lane_obs):
                    verify.append(f"CONFLIT prix : {mid} free dans la lane Zen, "
                                  f"payant au catalogue — à recouper")
                for mid in sorted((live - in_cat) - lane_obs):
                    structural.append(f"RETRAIT catalogue : {mid} (live dans l'état, "
                                      f"absent du catalogue)")
                for mid in sorted((live - in_cat) & lane_obs):
                    verify.append(f"hors catalogue mais documenté lane : {mid} — "
                                  f"à recouper")
                report.append(f"catalogue free : {len(live & zero)} free / "
                              f"{len(live)} live dans l'état")

    if "v1_models" in stypes:
        if "served" not in obs:
            problems.append("v1/models : source absente du cache")
        elif not obs["served"]:
            problems.append("v1/models : 0 modèle servi extrait (format changé ?) "
                            "— logique service suspendue")
        else:
            served = set(obs["served"])
            if has_models:
                live = {m["id"] for m in state["models"] if m["status"] == "live"}
                for mid in sorted(live - served):
                    verify.append(f"non servi (v1/models) : {mid} — observation "
                                  f"datée, à recouper avant tout retrait")
                report.append(f"servi opérateur : {len(live & served)} / "
                              f"{len(live)} live dans l'état")
            zero = set(obs.get("cat_zero") or [])
            if zero and has_models:
                known = {m["id"] for m in state["models"]}
                for mid in sorted((zero & served) - known):
                    problems.append(f"PROMOTION : {mid} (catalogue 0.00 + servi "
                                    f"v1) — décision manuelle")

    if "readme_md" in stypes and has_models:
        access = obs.get("access")
        if access and catalog_ids:
            for mid in sorted(set(catalog_ids) - set(access)):
                structural.append(f"DIVERGENCE README/llms : {mid} dans llms.txt, pas dans le tableau README")
            for mid in sorted(set(access) - set(catalog_ids)):
                structural.append(f"DIVERGENCE README/llms : {mid} dans README, pas dans llms.txt")
        if not access:
            problems.append("README : 0 ligne d'accès extraite (format changé ?) — logique accès suspendue")
        else:
            for mid, raw in sorted(access.items()):
                m = by_id[mid]
                if m["status"] != "live":
                    continue
                want = classify_access(raw)
                if want is None:
                    problems.append(f"README : valeur d'accès inconnue pour {mid} : {raw!r}")
                    continue
                if want in ("paid_only", "us_only"):
                    new = want
                elif m["access"] in ("paid_only", "us_only"):
                    new = "metered" if (m["price"]["value"] or 0) > 0 else "full"
                elif m["access"] == "unknown":
                    new = "metered" if (m["price"]["value"] or 0) > 0 else "full"
                else:
                    new = m["access"]
                if new != m["access"]:
                    auto.append({"op": "access", "id": mid, "from": m["access"], "to": new,
                                 "why": f"README : {raw!r}"})
                    report.append(f"accès : {mid} {m['access']} -> {new} (README : {raw})")

    if "llms_txt" in stypes:
        alloc = obs.get("allocations")
        if alloc is None:
            problems.append("llms.txt : source absente du cache")
        elif not alloc:
            problems.append("llms.txt : 0 allocation extraite (format changé ?)")
        else:
            cur = state["facts"].get("freebucks")
            cur_val = cur.get("value") if isinstance(cur, dict) else cur
            if cur_val != alloc:
                auto.append({"op": "facts_freebucks", "from": cur_val, "to": alloc})
                report.append(f"allocations : {len(alloc)} lignes "
                              f"(état : {'vide' if not cur_val else len(cur_val)})")

    if "picker_ts" in stypes and has_models:
        placements = obs.get("placements") or []
        if not placements:
            problems.append("picker-sections : 0 placement extrait (format changé ?)")
        else:
            for pl in placements:
                mid = pl.get("id")
                if not mid:
                    problems.append(f"picker : placement non apparié {pl['raw']!r}")
                    continue
                m = by_id[mid]
                if m.get("section") != pl["section"]:
                    auto.append({"op": "section", "id": mid, "from": m.get("section"),
                                 "to": pl["section"]})
                    report.append(f"section : {mid} {m.get('section')} -> {pl['section']}")

    # Provenance (§6) : l'état doit dire le dernier fetch RÉEL. Dérive de sha1 =
    # contenu changé depuis le dernier apply -> auto (apply réécrit sources).
    state_src = {s["url"]: s for s in state.get("sources", [])}
    drifted = [m for m in obs.get("sources_meta", [])
               if state_src.get(m["url"], {}).get("sha1") != m["sha1"]]
    refetched_same = [m for m in obs.get("sources_meta", [])
                      if m["url"] in state_src and m["sha1"] == state_src[m["url"]]["sha1"]
                      and state_src[m["url"]].get("fetched_at") != m["fetched_at"]]
    if drifted:
        auto.append({"op": "sources"})
        report.append(f"provenance : {len(drifted)} source(s) ressassée(s) avec sha1 "
                      f"nouveau : {', '.join(sorted(m['id'] for m in drifted))}")
    if refetched_same:
        report.append(f"resassé sans changement de contenu (sha1 identique) : "
                      f"{len(refetched_same)} source(s)")

    if "solar_promo_ts" in stypes and has_models:
        changes = obs.get("solar_changes") or []
        solar_url = next((s["url"] for s in adapter["sources"] if s["type"] == "solar_promo_ts"), "?")
        if not changes:
            problems.append("solar-promo : 0 transition de prix extraite (format changé ?)")
        else:
            have = {(m["id"], h["at"]) for m in state["models"]
                    for h in m["history"] if h.get("field") == "price"}
            latest: dict[str, tuple[dt.datetime, dict]] = {}
            for ch in changes:
                mid = ch["model"]
                if not mid or mid not in by_id:
                    problems.append(f"solar-promo : modelId non résolu {ch['raw_model']!r}")
                    continue
                if (mid, ch["at"]) not in have:
                    auto.append({"op": "history", "id": mid,
                                 "entry": {"at": ch["at"], "field": "price",
                                           "from": previous_recorded_price(by_id[mid], ch["at"]),
                                           "to": ch["price"],
                                           "evidence": {"url": solar_url, "tier": 1,
                                                        "quote": ch["tagline"] or ""}}})
                    report.append(f"historique prix : + {mid} {ch['at']} -> {ch['price']}")
                instant = parse_datetime(ch["at"])
                if ch["price"] is not None and instant is not None and (
                    mid not in latest or instant > latest[mid][0]
                ):
                    latest[mid] = (instant, ch)
            for mid, (_, ch) in sorted(latest.items()):
                sp = by_id[mid]["price"]
                if sp["value"] != ch["price"]:
                    verify.append(f"PRIX solar : {mid} état={sp['value']} / dépôt={ch['price']} "
                                  f"(dernier changement {ch['at']}) — décision manuelle")
            report.append(f"prix solaires : {len(changes)} transitions, promo "
                          f"{'active' if obs.get('solar_promo_active') else 'inactive'}")

    if "plans_html" in stypes:
        rows = obs.get("plans_rows") or []
        plans_ids = obs.get("plans_ids") or []
        if not rows:
            problems.append("/plans : 0 ligne extraite (format changé ?)")
        else:
            badges = [f"{r['display']} ({'/'.join(r['badges'])})" for r in rows if r["badges"]]
            report.append(f"/plans : {len(rows)} lignes, badges : "
                          f"{', '.join(badges) if badges else 'aucun'}")
            if catalog_ids:
                for mid in sorted(set(catalog_ids) - set(plans_ids)):
                    structural.append(f"DIVERGENCE /plans : {mid} dans llms.txt, absent de /plans")
                for mid in sorted(set(plans_ids) - set(catalog_ids)):
                    structural.append(f"DIVERGENCE /plans : {mid} dans /plans, absent de llms.txt")

    feed_src = next((s for s in adapter["sources"] if s["type"] == "rss"), None)
    if feed_src:
        items = obs.get("feed_items") or []
        if not items:
            problems.append("feed : 0 item extrait (format changé ?)")
        else:
            prev = next((s["fetched_at"] for s in state["sources"]
                         if s["url"] == feed_src["url"]), None)
            prev_dt = (parse_datetime(prev) if prev
                       else dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=7))
            if prev_dt is None:
                prev_dt = dt.datetime.now(dt.timezone.utc) - dt.timedelta(
                    days=REVALIDATE_DAYS
                )
            fresh = []
            for it in items:
                when = parse_datetime(it["pubDate"])
                if when is None:
                    continue
                if when > prev_dt:
                    fresh.append(it)
            for it in fresh:
                verify.append(f"feed tier 2 : « {it['title']} » ({it['pubDate']}) — à recouper tier 1")
            report.append(f"feed : {len(items)} items, {len(fresh)} depuis le dernier fetch")
            # Dernier événement « out » du feed encore non répercuté par l'état :
            # dérive tier 2 ↔ état — recoupement humain, jamais d'apply auto.
            feed_ev = obs.get("feed_events") or {}
            live = {m["id"] for m in state["models"] if m["status"] == "live"}
            outs = {mid: ev for mid, ev in feed_ev.items() if ev["act"] == "out"}
            non_rec = sorted(mid for mid in outs if mid in live)
            for mid in non_rec:
                ev = outs[mid]
                verify.append(f"retrait RSS non répercuté : {mid} "
                              f"(« {ev['title']} » {ev['when']}) — tier 2, "
                              f"à recouper tier 1")
            report.append(f"retraits RSS : {len(outs)} dernier-événement out, "
                          f"{len(non_rec)} encore live dans l'état")

    return {"report": report, "auto": auto, "structural": structural,
            "verify": verify, "problems": problems}


def _print_result(res: dict, problems: list[str], state: dict) -> int:
    print(f"=== diff — état {state['generated_at']} ===")
    for line in res["report"]:
        print(f"  {line}")
    for line in res["structural"]:
        print(f"  ! STRUCTUREL  {line}")
    for line in res["verify"]:
        print(f"  ? À VÉRIFIER  {line}")
    for line in problems + res["problems"]:
        print(f"  ✗ PROBLÈME   {line}")
    n = len(res["auto"]) + len(res["structural"]) + len(res["verify"]) + len(problems) + len(res["problems"])
    if n:
        print(f"= {n} élément(s) : {len(res['auto'])} applicable(s), "
              f"{len(res['structural'])} structurel, {len(res['verify'])} à vérifier, "
              f"{len(problems) + len(res['problems'])} problème(s)")
        return 2
    print("= aucun changement")
    return 0


def stale_cache_entries(manifest: dict) -> list[str]:
    now = dt.datetime.now(dt.timezone.utc)
    stale: list[str] = []
    for sid, entry in sorted(manifest["entries"].items()):
        at = entry.get("fetched_at") or manifest["fetched_at"]
        fetched = parse_datetime(at)
        if fetched is None:
            stale.append(f"{sid} (date invalide)")
        elif fetched > now:
            stale.append(f"{sid} (date future)")
        elif now - fetched >= dt.timedelta(days=REVALIDATE_DAYS):
            age = now - fetched
            stale.append(f"{sid} ({age.days} j)")
    return stale


def write_rapport(res: dict, problems: list[str], state: dict, day: Path,
                  manifest: dict, code: int) -> Path:
    """§6 ORCHESTRATOR : research/rapport.md = diff du dernier run (machine-owned)."""
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    all_problems = problems + res["problems"]
    if code:
        verdict = (f"exit {code} — {len(res['auto'])} applicable(s), "
                   f"{len(res['structural'])} structurel, {len(res['verify'])} à vérifier, "
                   f"{len(all_problems)} problème(s)")
        next_step = "`apply` → `render` → `check` → `lint` (agent : recoupe le tier 2 d'abord)"
    else:
        verdict = "exit 0 — aucun changement"
        next_step = "rien"
    out = [
        "# Rapport — diff du dernier run", "",
        f"- généré : {now}",
        f"- cache : {day.name} ({len(manifest['entries'])} sources)",
        f"- état : {state['generated_at']}",
        f"- verdict : {verdict}", "",
        "## Constat",
    ]
    out += [f"- {line}" for line in res["report"]] or ["- (rien)"]
    out.append("")
    for title, items, mark in (
        ("Décision manuelle (structurel)", res["structural"], "!"),
        ("À vérifier (tier 2, jamais preuve)", res["verify"], "?"),
        ("Problèmes", all_problems, "✗"),
    ):
        if items:
            out.append(f"## {title}")
            out += [f"- {mark} {item}" for item in items]
            out.append("")
    out += ["## Prochaine étape", next_step, ""]
    atomic_write_text(RAPPORT, "\n".join(out))
    return RAPPORT


def cmd_diff(args) -> None:
    adapter = load_adapter()
    state = load_state()
    day, manifest = load_cache(args.date or today())
    obs, problems = build_observation(day, manifest, state, adapter)
    # Fraîcheur : une source de >= REVALIDATE_DAYS jours exige la revalidation hebdo.
    stale = stale_cache_entries(manifest)
    if stale:
        problems.append(f"non revalidé depuis ≥{REVALIDATE_DAYS} j : {', '.join(stale)} "
                        f"— `fetch --revalidate`")
    res = compute_changes(state, obs, adapter)
    print(f"[cache {day.name}, {len(manifest['entries'])} sources]")
    code = _print_result(res, problems, state)
    if args.date is None and RAPPORT is not None:
        path = write_rapport(res, problems, state, day, manifest, code)
        print(f"rapport : {path.relative_to(ROOT)}")
    if code:
        sys.exit(code)


def url_of(adapter: dict, type_: str) -> str:
    return next((s["url"] for s in adapter["sources"] if s["type"] == type_), "?")


def observed_at_for(obs: dict, type_: str) -> str:
    source = next((s for s in obs.get("sources_meta", [])
                   if s.get("type") == type_), None)
    if source is None:
        sys.exit(f"apply : provenance absente pour la source {type_!r}.")
    return source["fetched_at"]


def cmd_apply(args) -> None:
    adapter = load_adapter()
    state = load_state()
    day, manifest = load_cache(args.date or today())
    obs, problems = build_observation(day, manifest, state, adapter)
    res = compute_changes(state, obs, adapter)
    blocking_problems = problems + res["problems"]
    stale = stale_cache_entries(manifest)
    if stale:
        blocking_problems.append(
            f"cache non revalidé depuis ≥{REVALIDATE_DAYS} j : "
            f"{', '.join(stale)} — relancer fetch --revalidate"
        )
    if blocking_problems:
        print("apply REFUSÉ : observation incomplète ou invalide ; l'état reste inchangé.")
        for line in blocking_problems:
            print(f"  - {line}")
        sys.exit(1)
    by_id = {m["id"]: m for m in state["models"]}
    applied = 0
    for op in res["auto"]:
        if op["op"] == "access":
            m = by_id[op["id"]]
            observed_at = observed_at_for(obs, "readme_md")
            m["history"].append({"at": observed_at, "field": "access", "from": op["from"],
                                 "to": op["to"],
                                 "evidence": {"url": url_of(adapter, "readme_md"), "tier": 1,
                                              "quote": op["why"]}})
            m["access"] = op["to"]
        elif op["op"] == "section":
            m = by_id[op["id"]]
            observed_at = observed_at_for(obs, "picker_ts")
            m["history"].append({"at": observed_at, "field": "section", "from": op["from"],
                                 "to": op["to"],
                                 "evidence": {"url": url_of(adapter, "picker_ts"), "tier": 1,
                                              "quote": ""}})
            m["section"] = op["to"]
        elif op["op"] == "facts_freebucks":
            observed_at = observed_at_for(obs, "llms_txt")
            state["facts"]["freebucks"] = {
                "value": op["to"],
                "evidence": {"url": url_of(adapter, "llms_txt"), "tier": 1,
                             "at": observed_at},
            }
        elif op["op"] == "sources":
            # simple marqueur : le rafraîchissement complet de state["sources"]
            # est fait en fin d'apply, depuis le manifest du cache courant.
            pass
        elif op["op"] == "history":
            by_id[op["id"]]["history"].append(op["entry"])
        else:
            sys.exit(f"apply : op inconnu {op!r}")
        applied += 1

    def _hkey(h: dict) -> dt.datetime:
        # Tri chronologique réel : « ...T05:00:00Z » > « ...T00:00:00-07:00 »
        # serait faux en comparaison lexicographique (fuseaux différents).
        return parse_datetime(h.get("at")) or dt.datetime.max.replace(
            tzinfo=dt.timezone.utc
        )

    for m in state["models"]:
        m["history"].sort(key=_hkey)
    state["sources"] = [
        {"url": e["url"], "tier": e["tier"],
         "fetched_at": e.get("fetched_at") or manifest["fetched_at"],
         "sha1": e["sha1"]}
        for e in manifest["entries"].values()
    ]
    state["generated_at"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    save_state(state)
    print(f"apply OK : {applied} opération(s), {len(state['sources'])} sources enregistrées")
    if res["structural"]:
        print("  décision manuelle restante :")
        for line in res["structural"]:
            print(f"    - {line}")
    if res["verify"]:
        print("  à vérifier (tier 2 / jugement) :")
        for line in res["verify"]:
            print(f"    - {line}")
    if problems + res["problems"]:
        print("  problèmes :")
        for line in problems + res["problems"]:
            print(f"    - {line}")
    print("Ensuite : render, check, lint, trace, write-back mémoire.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--platform", default="freebuff",
                    help="plateforme = nom d'adapter (adapters/<nom>.json) ; défaut: freebuff")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("import", help="backfill: tableau comparatif -> état")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_import)
    sub.add_parser("pair", help="apparie fiches <-> état (fichier.replace('.','-') == id)").set_defaults(func=cmd_pair)
    sub.add_parser("migrate", help="insère le bloc GEN:prix dans chaque fiche").set_defaults(func=cmd_migrate)
    sub.add_parser("check", help="rendu depuis l'état == fichiers ?").set_defaults(func=cmd_check)
    sub.add_parser("render", help="réécrit comparatif + blocs GEN:prix").set_defaults(func=cmd_render)
    sub.add_parser("show", help="résumé de l'état").set_defaults(func=cmd_show)
    sub.add_parser("lint", help="cohérence inter-doc").set_defaults(func=cmd_lint)
    p = sub.add_parser("fetch", help="santé puis téléchargement des sources -> cache daté")
    p.add_argument("--adapter", default=None)
    p.add_argument("--revalidate", action="store_true",
                   help="re-télécharge tout, ignore le cache du jour (cadence hebdo)")
    p.set_defaults(func=cmd_fetch)
    for name, fn, hlp in (
        ("diff", cmd_diff, "cache vs état (exit 2 s'il y a du changement)"),
        ("apply", cmd_apply, "applique le sous-ensemble sûr du diff + sources"),
    ):
        p = sub.add_parser(name, help=hlp)
        p.add_argument("--adapter", default=None)
        p.add_argument("--date", default=None, help="cache du jour AAAA-MM-JJ (défaut: aujourd'hui)")
        p.set_defaults(func=fn)
    args = ap.parse_args()
    adapter_arg = getattr(args, "adapter", None)
    setup_platform(args.platform, Path(adapter_arg) if adapter_arg else None)
    run_locked(args.func, args)


if __name__ == "__main__":
    main()
