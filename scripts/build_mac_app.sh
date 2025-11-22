#!/usr/bin/env bash
set -euo pipefail

APP_NAME="WordMemorizer"
PORTABLE_DATA_DIR="$HOME/Library/Application Support/WordMemorizer"

python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller

mkdir -p "${PORTABLE_DATA_DIR}"

pyinstaller \
  --noconfirm \
  --windowed \
  --name "${APP_NAME}" \
  --add-data "app/templates:app/templates" \
  --add-data "app/static:app/static" \
  desktop_app.py

echo "Built app at dist/${APP_NAME}.app. Zip and upload to Releases for a double-clickable macOS build."
