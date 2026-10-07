#!/bin/sh
# Entrée des timers systemd --user (moteur/timers/) : une seule porte d'entrée,
# journalisée dans le journal utilisateur, pour CHAQUE plateforme déclarée dans
# moteur/adapters/. exit 2 du diff (changements) = état normal pour un timer :
# rapporté dans le rapport de la plateforme (research.rapport), pas en échec unité.
set -eu
cd "$(dirname "$0")/.."

case "${1:-}" in
  quotidien) mode="" ;;
  hebdo)     mode="--revalidate" ;;
  *)
    echo "usage: $0 quotidien|hebdo" >&2
    exit 64
    ;;
esac

rc=0
found=0
for a in moteur/adapters/*.json; do
  [ -f "$a" ] || continue
  found=1
  p=${a##*/}
  p=${p%.json}
  f=0
  python3 moteur/engine.py --platform "$p" fetch $mode || f=$?
  if [ "$f" -ne 0 ]; then
    rc=$f
    continue
  fi
  d=0
  python3 moteur/engine.py --platform "$p" diff || d=$?
  case "$d" in
    0|2) ;;
    *)   rc=$d ;;
  esac
done

[ "$found" -eq 1 ] || {
  echo "aucun adaptateur JSON dans moteur/adapters/" >&2
  exit 1
}

exit "$rc"
