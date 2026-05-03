#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="$ROOT_DIR/custom_components/dynamic_label_dashboard/"
TARGET_HOST="k0nsti@192.168.178.173"
TARGET_DIR="/config/custom_components/dynamic_label_dashboard"

if [[ ! -d "$SRC_DIR" ]]; then
  echo "Source dir not found: $SRC_DIR" >&2
  exit 1
fi

ssh "$TARGET_HOST" "sudo -n mkdir -p '$TARGET_DIR' && sudo -n chown -R k0nsti:k0nsti '$TARGET_DIR'"
rsync -av --delete \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  "$SRC_DIR" "$TARGET_HOST:$TARGET_DIR/"

echo "Deployed to $TARGET_HOST:$TARGET_DIR"
