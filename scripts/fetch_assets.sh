#!/usr/bin/env bash
# Fetches the sprite sheets and fonts the style needs from njord into assets/.
#
#   scripts/fetch_assets.sh [ASSETS_DIR]
#
# NJORD_REF pins the njord commit (default: the one the symbology was ported from).

set -euo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_DIR=$( cd -- "$SCRIPT_DIR/.." &> /dev/null && pwd )
ASSETS_DIR=${1:-"$PROJECT_DIR/assets"}
NJORD_REF=${NJORD_REF:-997bf21cfd9300c679bcb1fa3362edf44956d8a0}
NJORD_ARCHIVE_URL="https://github.com/manimaul/njord/archive/${NJORD_REF}.tar.gz"

mkdir -p "$ASSETS_DIR"

TMP_DIR=$(mktemp -d)
cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

ARCHIVE="$TMP_DIR/njord.tar.gz"

if command -v curl >/dev/null 2>&1; then
    curl -L --fail "$NJORD_ARCHIVE_URL" -o "$ARCHIVE"
elif command -v wget >/dev/null 2>&1; then
    wget -O "$ARCHIVE" "$NJORD_ARCHIVE_URL"
else
    echo "curl or wget is required to download njord assets" >&2
    exit 1
fi

tar -xzf "$ARCHIVE" -C "$TMP_DIR" --wildcards "*/crates/njord-server/resources/www/*"
WWW=$(find "$TMP_DIR" -type d -path "*/crates/njord-server/resources/www" | head -n 1)

if [ -z "$WWW" ] || [ ! -d "$WWW/fonts" ] || [ ! -d "$WWW/sprites" ]; then
    echo "njord archive did not contain resources/www/fonts and resources/www/sprites" >&2
    exit 1
fi

rm -rf "$ASSETS_DIR/fonts" "$ASSETS_DIR/sprites"
cp -R "$WWW/fonts" "$ASSETS_DIR/fonts"
cp -R "$WWW/sprites" "$ASSETS_DIR/sprites"
echo "$NJORD_REF" > "$ASSETS_DIR/NJORD_REF"

echo "Fetched njord fonts and sprites (${NJORD_REF}) into $ASSETS_DIR"
