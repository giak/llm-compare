#!/bin/sh
# Installe les timers systemd --user depuis le dépôt (source de vérité = moteur/timers/).
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd -P)
PROJECT_ROOT=$(CDPATH= cd "$SCRIPT_DIR/../.." && pwd -P)
UNIT_DIR=${XDG_CONFIG_HOME:-"$HOME/.config"}/systemd/user
mkdir -p "$UNIT_DIR"

escaped_root=$(printf '%s\n' "$PROJECT_ROOT" | sed 's/%/%%/g; s/[\\&|]/\\&/g')
for unit in \
  llm-compare-quotidien.service llm-compare-quotidien.timer \
  llm-compare-hebdo.service llm-compare-hebdo.timer; do
  sed "s|@PROJECT_ROOT@|$escaped_root|g" "$SCRIPT_DIR/$unit" > "$UNIT_DIR/$unit"
done

systemctl --user daemon-reload
systemctl --user enable --now llm-compare-quotidien.timer llm-compare-hebdo.timer
systemctl --user list-timers 'llm-compare-*'
