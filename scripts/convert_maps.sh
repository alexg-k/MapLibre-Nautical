#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
S57_INPUT_DIR=${1:-"$SCRIPT_DIR"'/../sample_data/ENC_ROOT'}

cd $SCRIPT_DIR/..

mkdir -p output_geojson
mkdir -p output
find $S57_INPUT_DIR -name "*.000" -type f -exec sh -c 'python3 enc-mapbox-converter/cli.py --input {} --output ../output/$(basename {} .000)' \;
