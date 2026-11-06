#!/usr/bin/env python3
"""Builds the Natural Earth base map njord draws under the charts.

    python3 -m nautical.convert_basemap [--assets assets] [--output output] [--max-zoom 8]

Downloads the Natural Earth physical vector files njord uses (into ``assets/ne/``) and tiles them
into ``base.mbtiles``: the 1:110m files for zooms 0-2, 1:50m for 3-4 and 1:10m from 5 up, as
njord picks the scale per zoom. The layer names are njord's (``land``, ``ocean``, ``lakes``, ...),
which the base style layers read.
"""

import argparse
import shutil
import sys
import tempfile
import urllib.request
from pathlib import Path

from osgeo import ogr
from shapely import wkb

from .symbology.factory import LayerFactory
from .tiles.encode import Symbolizer
from .tiles.s57 import _repair
from .tiles.tippecanoe import LayerWriter, run_tippecanoe

BASE_URL = "https://naciscdn.org/naturalearth/{scale}/physical/{name}.zip"

FILES = {
    "10m": [
        "ne_10m_coastline",
        "ne_10m_land",
        "ne_10m_minor_islands",
        "ne_10m_ocean",
        "ne_10m_lakes",
        "ne_10m_rivers_lake_centerlines",
        "ne_10m_glaciated_areas",
        "ne_10m_reefs",
        "ne_10m_playas",
        "ne_10m_antarctic_ice_shelves_polys",
    ],
    "50m": [
        "ne_50m_coastline",
        "ne_50m_land",
        "ne_50m_ocean",
        "ne_50m_lakes",
        "ne_50m_rivers_lake_centerlines",
        "ne_50m_glaciated_areas",
        "ne_50m_antarctic_ice_shelves_polys",
    ],
    "110m": [
        "ne_110m_coastline",
        "ne_110m_land",
        "ne_110m_ocean",
        "ne_110m_lakes",
        "ne_110m_rivers_lake_centerlines",
        "ne_110m_glaciated_areas",
    ],
}

#: The zoom band of each scale (njord's ``find_base_map_scale``: 110m below z3, 50m below z5).
ZOOM_BANDS = {"110m": (0, 2), "50m": (3, 4), "10m": (5, None)}


def normalize_layer_name(filename):
    base = filename.rsplit(".", 1)[0]
    for prefix in ("ne_10m_", "ne_50m_", "ne_110m_"):
        if base.startswith(prefix):
            base = base[len(prefix) :]
            break
    if base.startswith("bathymetry"):
        return "bathymetry"
    if base.startswith("lakes"):
        return "lakes"
    return base


def download(assets, scales):
    for scale in scales:
        out = Path(assets) / "ne" / scale
        out.mkdir(parents=True, exist_ok=True)
        for name in FILES[scale]:
            target = out / f"{name}.zip"
            if target.exists() and target.stat().st_size > 0:
                continue
            url = BASE_URL.format(scale=scale, name=name)
            print(f"  downloading {url}")
            with urllib.request.urlopen(url) as resp, target.open("wb") as f:
                shutil.copyfileobj(resp, f)


def read_shapefile(zip_path):
    """``(props, geometry)`` of every feature of the zipped shapefile."""
    ds = ogr.Open(f"/vsizip/{zip_path}")
    if ds is None:
        raise RuntimeError(f"cannot open {zip_path}")
    layer = ds.GetLayerByIndex(0)
    defn = layer.GetLayerDefn()
    keep = {"name", "scalerank", "featurecla", "min_zoom"}
    for f in layer:
        g = f.GetGeometryRef()
        if g is None:
            continue
        geometry = _repair(wkb.loads(bytes(g.ExportToIsoWkb())))
        if geometry is None or geometry.is_empty:
            continue
        props = {}
        for i in range(defn.GetFieldCount()):
            key = defn.GetFieldDefn(i).GetName()
            if key in keep and f.IsFieldSetAndNotNull(i):
                props[key] = f.GetField(i)
        yield props, geometry


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--assets", default="assets", help="where the Natural Earth zips are kept (assets/ne/<scale>/)")
    ap.add_argument("--output", default="output")
    ap.add_argument("--max-zoom", type=int, default=8, help="tile pyramid depth of the base map (overzoomed beyond)")
    ap.add_argument("--scales", default="10m,50m,110m")
    args = ap.parse_args(argv)

    scales = [s.strip() for s in args.scales.split(",") if s.strip()]
    print("fetching Natural Earth files")
    download(args.assets, scales)

    factory = LayerFactory()
    by_source_layer = {e.source_layer: e for e in factory.entries if e.base}
    symbolizer = Symbolizer(factory, drop=())
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    work_dir = Path(tempfile.mkdtemp(prefix="nautical-base-", dir=output))
    try:
        writer = LayerWriter(work_dir)
        for scale in scales:
            minzoom, maxzoom = ZOOM_BANDS[scale]
            if maxzoom is not None and minzoom > args.max_zoom:
                continue
            for name in FILES[scale]:
                layer = normalize_layer_name(name)
                entry = by_source_layer.get(layer)
                n = 0
                for props, geometry in read_shapefile(Path(args.assets) / "ne" / scale / f"{name}.zip"):
                    if entry is not None:
                        props = symbolizer.symbolize(entry.key, props, "natural_earth")
                    props["SCALE"] = scale
                    writer.write(layer, geometry, props, minzoom, maxzoom)
                    n += 1
                print(f"  {name}: {n} features -> {layer} z{minzoom}-{maxzoom if maxzoom is not None else args.max_zoom}")
        writer.close()
        run_tippecanoe(
            output / "base.mbtiles",
            writer.layer_files(),
            args.max_zoom,
            name="base",
            description="Natural Earth base map",
            extra_args=["--simplify-only-low-zooms"],
        )
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
