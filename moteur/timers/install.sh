#!/bin/sh
# Installe les timers systemd --user depuis le dépôt (source de vérité = moteur/timers/).
set -eu
cd "$(dirname "$0")"

mkdir -p ~/.config/systemd/user
cp llm-compare-quotidien.service llm-compare-quotidien.timer \
   llm-compare-hebdo.service llm-compare-hebdo.timer ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now llm-compare-quotidien.timer llm-compare-hebdo.timer
systemctl --user list-timers 'llm-compare-*'
