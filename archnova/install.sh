#!/usr/bin/env bash
# archnova kurulum: ./install.sh [--system]
set -euo pipefail
cd "$(dirname "$0")"
if [[ "${1:-}" == "--system" ]]; then
  sudo pip install --break-system-packages .
else
  pip install --user --break-system-packages .
  echo "PATH'inde ~/.local/bin olsun, sonra: archnova"
fi
