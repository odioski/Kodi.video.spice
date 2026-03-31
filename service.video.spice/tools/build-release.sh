#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ROOT_DIR=$(cd "$SCRIPT_DIR/.." && pwd)
DIST_DIR="$ROOT_DIR/dist"
TMP_DIR=$(mktemp -d)

cleanup() {
    rm -rf "$TMP_DIR"
}

trap cleanup EXIT

cd "$ROOT_DIR"

mapfile -t addon_info < <(
    python3 - <<'PY'
import xml.etree.ElementTree as ET

root = ET.parse("addon.xml").getroot()
print(root.attrib["id"])
print(root.attrib["version"])
PY
)

ADDON_ID=${addon_info[0]}
ADDON_VERSION=${addon_info[1]}
STAGE_DIR="$TMP_DIR/$ADDON_ID"
ZIP_PATH="$DIST_DIR/$ADDON_ID-$ADDON_VERSION.zip"
CHANGELOG_FILE="changelog-$ADDON_VERSION.txt"

mkdir -p "$DIST_DIR" "$STAGE_DIR/resources/lib"

cp addon.xml service.py video.spice.gif LICENSE.txt "$STAGE_DIR/"
cp resources/__init__.py "$STAGE_DIR/resources/"
cp resources/lib/__init__.py resources/lib/overlay.py "$STAGE_DIR/resources/lib/"

if [[ -f "$CHANGELOG_FILE" ]]; then
    cp "$CHANGELOG_FILE" "$STAGE_DIR/"
fi

for asset in icon.png fanart.jpg; do
    if [[ -f "$asset" ]]; then
        cp "$asset" "$STAGE_DIR/"
    fi
done

rm -f "$ZIP_PATH"

(
    cd "$TMP_DIR"
    zip -qr "$ZIP_PATH" "$ADDON_ID"
)

printf 'Built %s\n' "$ZIP_PATH"

missing_assets=()
for asset in icon.png fanart.jpg; do
    if [[ ! -f "$ROOT_DIR/$asset" ]]; then
        missing_assets+=("$asset")
    fi
done

if (( ${#missing_assets[@]} > 0 )); then
    printf 'Warning: missing recommended Kodi repository assets: %s\n' "${missing_assets[*]}"
fi

if [[ $(basename "$ROOT_DIR") != "$ADDON_ID" ]]; then
    printf 'Note: source folder name does not match add-on id; the zip uses the correct %s/ root.\n' "$ADDON_ID"
fi
