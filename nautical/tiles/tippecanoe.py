"""Newline-delimited GeoJSON per source layer, and the tippecanoe run that tiles it."""

import json
import shutil
import subprocess
from pathlib import Path

import shapely
from shapely.geometry import mapping


class LayerWriter:
    """One ``<layer>.json`` (newline-delimited features) per source layer under ``directory``."""

    def __init__(self, directory):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self._files = {}
        self.counts = {}

    def write(self, layer, geometry, props, minzoom=None, maxzoom=None):
        f = self._files.get(layer)
        if f is None:
            f = self._files[layer] = (self.directory / f"{layer}.json").open("w")
        feature = {"type": "Feature", "properties": props, "geometry": mapping(shapely.force_2d(geometry))}
        zooms = {}
        if minzoom is not None:
            zooms["minzoom"] = int(minzoom)
        if maxzoom is not None:
            zooms["maxzoom"] = int(maxzoom)
        if zooms:
            feature["tippecanoe"] = zooms
        f.write(json.dumps(feature, separators=(",", ":")))
        f.write("\n")
        self.counts[layer] = self.counts.get(layer, 0) + 1

    def close(self):
        for f in self._files.values():
            f.close()
        self._files = {}

    def layer_files(self):
        return {layer: self.directory / f"{layer}.json" for layer in self.counts}


def run_tippecanoe(output, layer_files, max_zoom, min_zoom=0, name=None, description=None, extra_args=()):
    """Tiles ``layer_files`` (``{layer: path}``) into the mbtiles ``output``.

    Every feature is kept (no rate dropping, no feature or tile size limits, no tiny-polygon
    reduction) so soundings and small areas survive at every zoom; shared polygon borders are
    detected so depth areas simplify consistently. ``--no-line-simplification`` is not used; the
    default simplification is at tile resolution and invisible.
    """
    tippecanoe = shutil.which("tippecanoe")
    if tippecanoe is None:
        raise RuntimeError("tippecanoe is not installed")
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        tippecanoe,
        "--force",
        f"--output={output}",
        f"--minimum-zoom={min_zoom}",
        f"--maximum-zoom={max_zoom}",
        "--drop-rate=1",
        "--no-feature-limit",
        "--no-tile-size-limit",
        "--no-tiny-polygon-reduction",
        "--detect-shared-borders",
        "--no-progress-indicator",
    ]
    if name:
        cmd.append(f"--name={name}")
    if description:
        cmd.append(f"--description={description}")
    cmd.extend(extra_args)
    for layer, path in sorted(layer_files.items()):
        cmd.append(f"--named-layer={layer}:{path}")
    print("running:", " ".join(cmd[:12]), f"... ({len(layer_files)} layers)")
    subprocess.run(cmd, check=True)
    return output
