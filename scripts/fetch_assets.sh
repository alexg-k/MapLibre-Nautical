#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_DIR=$( cd -- "$SCRIPT_DIR/.." &> /dev/null && pwd )
OUTPUT_DIR=${1:-"$PROJECT_DIR/output"}
S57TILER_REF=${S57TILER_REF:-master}
S57TILER_ARCHIVE_URL="https://github.com/manimaul/s57tiler/archive/${S57TILER_REF}.tar.gz"

mkdir -p "$OUTPUT_DIR"

TMP_DIR=$(mktemp -d)
cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

ARCHIVE="$TMP_DIR/s57tiler.tar.gz"

if command -v curl >/dev/null 2>&1; then
    curl -L "$S57TILER_ARCHIVE_URL" -o "$ARCHIVE"
elif command -v wget >/dev/null 2>&1; then
    wget -O "$ARCHIVE" "$S57TILER_ARCHIVE_URL"
else
    echo "curl or wget is required to download s57tiler assets" >&2
    exit 1
fi

tar -xzf "$ARCHIVE" -C "$TMP_DIR"
ASSET_ROOT="$TMP_DIR/s57tiler-${S57TILER_REF}/data"

if [ ! -d "$ASSET_ROOT/fonts" ] || [ ! -d "$ASSET_ROOT/sprites" ]; then
    echo "s57tiler archive did not contain data/fonts and data/sprites" >&2
    exit 1
fi

rm -rf "$OUTPUT_DIR/fonts" "$OUTPUT_DIR/sprites"
cp -R "$ASSET_ROOT/fonts" "$OUTPUT_DIR/fonts"
cp -R "$ASSET_ROOT/sprites" "$OUTPUT_DIR/sprites"

echo "Fetched fonts and sprites into $OUTPUT_DIR"
