#!/usr/bin/env python3
"""Converts a directory of S-57 cells into one symbolized vector tile set.

    python3 -m nautical.convert_maps [--input DIR] [--output DIR] [--max-zoom 14]

For every cell: the chart's scale, display zoom and coverage are read, then every feature is
symbolized njord-style (``SY``, ``AC``, ``LC``, ... props), cut into the zoom bands in which
finer charts do not cover it (see ``nautical.tiles.priority``) and written to one newline-
delimited GeoJSON file per S-57 object class, which tippecanoe tiles into ``charts.mbtiles``.
Beside it, ``charts.json`` lists the charts and ``sectors.json`` the light sector icons the
sprite sheets need.
"""

import argparse
import json
import shutil
import sys
import tempfile
import time
from multiprocessing import Pool
from pathlib import Path

from shapely.geometry import LineString, MultiLineString

from .symbology.factory import LayerFactory
from .symbology.layerable import SymbologyConfig
from .tiles.encode import Symbolizer, assign_sector_sheets, sector_image_name, topmar_associations
from .tiles.priority import pieces, plan
from .tiles.s57 import Cell, chart_summary, find_cells
from .tiles.tippecanoe import LayerWriter, run_tippecanoe

DEFAULT_INPUT = "sample_data/ENC_ROOT"
DEFAULT_OUTPUT = "output"
DEFAULT_MAX_ZOOM = 14
#: 150 icons of 200×200 px keep a sheet under 6 Mpx (24 Mpx at 2x), far below browser limits.
DEFAULT_SECTORS_PER_SHEET = 150
PLY_LAYER = "PLY"

_worker_state = {}


def read_metadata(path):
    try:
        return Cell(path).read_metadata(), None
    except Exception as e:  # noqa: BLE001
        return None, f"{path}: {e}"


def _init_worker(config, max_zoom, work_dir):
    _worker_state["factory"] = LayerFactory(config=config)
    _worker_state["max_zoom"] = max_zoom
    _worker_state["work_dir"] = Path(work_dir)


def convert_chart(chart_plan):
    """Symbolizes, clips and writes one chart's features into ``<work_dir>/<chart>/``."""
    factory = _worker_state["factory"]
    max_zoom = _worker_state["max_zoom"]
    chart = chart_plan.chart
    symbolizer = Symbolizer(factory)
    started = time.time()
    try:
        Cell(chart.path).read_features(chart)
    except Exception as e:  # noqa: BLE001
        return {"chart": chart.name, "error": str(e)}
    assoc = topmar_associations(chart.features)
    writer = LayerWriter(_worker_state["work_dir"] / chart.name)
    for layer, features in chart.features.items():
        if layer == "M_COVR":
            continue
        for f in features:
            if f.geometry is None or f.geometry.is_empty:
                continue
            props = symbolizer.symbolize(
                layer, f.props, chart.name, assoc.get(f.props.get("LNAM"), ()) if layer == "TOPMAR" else ()
            )
            for piece in pieces(chart_plan, f.geometry, props, max_zoom):
                writer.write(layer, piece.geometry, props, piece.minzoom, piece.maxzoom)
    # every chart contributes its coverage outline, whatever its zoom
    boundary = chart.coverage.boundary
    if not boundary.is_empty:
        writer.write(PLY_LAYER, boundary, {"NAME": chart.name})
    writer.close()
    chart.features = {}
    return {
        "chart": chart.name,
        "counts": writer.counts,
        "sectors": sorted(symbolizer.sector_icons),
        "seconds": round(time.time() - started, 1),
    }


def prefix_sector_names(lights_file, sheets, sheet_count):
    """Rewrites the ``SI`` of every light to its multi-sprite name (``sectors<k>:<name>``)."""
    lights_file = Path(lights_file)
    tmp = lights_file.with_suffix(".tmp")
    with lights_file.open() as src, tmp.open("w") as out:
        for line in src:
            feature = json.loads(line)
            si = feature["properties"].get("SI")
            if si in sheets:
                feature["properties"]["SI"] = sector_image_name(si, sheets[si], sheet_count)
            out.write(json.dumps(feature, separators=(",", ":")))
            out.write("\n")
    tmp.replace(lights_file)


def concatenate(work_dir, chart_names, out_dir):
    """Joins the per-chart layer files into one file per layer."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    layer_files = {}
    for name in chart_names:
        chart_dir = Path(work_dir) / name
        if not chart_dir.is_dir():
            continue
        for path in sorted(chart_dir.glob("*.json")):
            layer = path.stem
            target = layer_files.get(layer)
            if target is None:
                target = layer_files[layer] = out_dir / f"{layer}.json"
                target.write_bytes(b"")
            with target.open("ab") as out, path.open("rb") as src:
                shutil.copyfileobj(src, out)
    return layer_files


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", default=DEFAULT_INPUT, help="directory searched recursively for .000 cells")
    ap.add_argument("--output", default=DEFAULT_OUTPUT, help="output directory (charts.mbtiles, charts.json, sectors.json)")
    ap.add_argument("--max-zoom", type=int, default=DEFAULT_MAX_ZOOM, help="tile pyramid depth; MapLibre overzooms beyond it")
    ap.add_argument("--shallow-depth", type=float, default=3.0, help="metres; DEPVS up to this DRVAL1")
    ap.add_argument("--safety-depth", type=float, default=6.0, help="metres; DEPMS up to this DRVAL1")
    ap.add_argument("--deep-depth", type=float, default=9.0, help="metres; DEPMD up to this DRVAL1, DEPDW beyond")
    ap.add_argument("--workers", type=int, default=None, help="parallel chart conversions (default: CPU count)")
    ap.add_argument(
        "--sectors-per-sheet",
        type=int,
        default=DEFAULT_SECTORS_PER_SHEET,
        help="light sector icons per sprite sheet; up to this many are merged into the base sheet, more are "
        "spread over extra sheets (MapLibre multi-sprite) so no sheet grows beyond what browsers decode",
    )
    ap.add_argument("--keep-geojson", action="store_true", help="keep the per-layer GeoJSON under <output>/geojson")
    ap.add_argument("--skip-tippecanoe", action="store_true", help="only write the GeoJSON")
    args = ap.parse_args(argv)

    cells = find_cells(args.input)
    if not cells:
        print(f"no .000 cells under {args.input}", file=sys.stderr)
        return 1
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    config = SymbologyConfig(args.shallow_depth, args.safety_depth, args.deep_depth)

    print(f"reading metadata of {len(cells)} cells")
    charts = []
    with Pool(args.workers) as pool:
        for chart, error in pool.imap_unordered(read_metadata, cells):
            if error:
                print("skipping", error, file=sys.stderr)
            else:
                charts.append(chart)
    plans = plan(charts, args.max_zoom)
    ordered = [p.chart for p in plans]
    with (output / "charts.json").open("w") as f:
        json.dump([chart_summary(c) for c in ordered], f, indent=2)

    work_dir = Path(tempfile.mkdtemp(prefix="nautical-", dir=output))
    sectors = set()
    counts = {}
    try:
        print(f"converting {len(plans)} charts (max zoom {args.max_zoom})")
        with Pool(args.workers, initializer=_init_worker, initargs=(config, args.max_zoom, work_dir)) as pool:
            for result in pool.imap_unordered(convert_chart, plans):
                if "error" in result:
                    print("failed", result["chart"], result["error"], file=sys.stderr)
                    continue
                sectors.update(result["sectors"])
                for layer, n in result["counts"].items():
                    counts[layer] = counts.get(layer, 0) + n
                print(f"  {result['chart']}: {sum(result['counts'].values())} features in {result['seconds']}s")
        geojson_dir = output / "geojson"
        if geojson_dir.exists():
            shutil.rmtree(geojson_dir)
        layer_files = concatenate(work_dir, [c.name for c in ordered], geojson_dir)

        sheets = assign_sector_sheets(sectors, args.sectors_per_sheet)
        sheet_count = max(sheets.values(), default=0) + 1
        with (output / "sectors.json").open("w") as f:
            json.dump({"sheets": sheet_count, "icons": sheets}, f, indent=2)
        if sheet_count > 1 and "LIGHTS" in layer_files:
            prefix_sector_names(layer_files["LIGHTS"], sheets, sheet_count)
        print(f"{sum(counts.values())} features in {len(layer_files)} layers; {len(sectors)} light sector icons")
        if not args.skip_tippecanoe:
            run_tippecanoe(
                output / "charts.mbtiles",
                layer_files,
                args.max_zoom,
                name="charts",
                description="S-57 ENC charts symbolized for MapLibre",
            )
        if not args.keep_geojson and not args.skip_tippecanoe:
            shutil.rmtree(geojson_dir)
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
