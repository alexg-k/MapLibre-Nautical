#!/usr/bin/env python3
"""Writes the MapLibre styles, sprite sheets, fonts and the tileserver-gl config into ``output/``.

    python3 -m nautical.generate_mapstyle [--assets assets] [--output output]

One style per depth unit and theme: ``light`` (metres, day), ``dusk``, ``dark`` (night), and
``light-feet``, ``light-fathoms``, ... The sprite sheets are njord's per-theme sheets with the
light sector icons of the converted charts (``output/sectors.json``) added.
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

from .symbology.colors import ColorLibrary, Depth, Theme, ThemeMode
from .symbology.factory import LayerFactory
from .symbology.layerable import SymbologyConfig
from .symbology.style import style
from .tiles.sprites import build_sprites

CHARTS_SOURCE = "charts"
BASE_SOURCE = "base"
STYLE_NAMES = {ThemeMode.DAY: "light", ThemeMode.DUSK: "dusk", ThemeMode.NIGHT: "dark"}


def style_id(depth, theme):
    name = STYLE_NAMES[theme.mode]
    if theme.custom:
        name += f"-{theme.custom}"
    if depth != Depth.METERS:
        name += f"-{depth.value}"
    return name


def sprite_property(entries):
    """Paths relative to tileserver-gl's ``paths.sprites``."""
    if len(entries) == 1:
        return entries[0]["stem"]
    return [{"id": e["id"], "url": e["stem"]} for e in entries]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--assets", default="assets", help="directory with njord's sprites/ and fonts/ (scripts/fetch_assets.sh)")
    ap.add_argument("--output", default="output", help="output directory (charts.mbtiles from convert_maps lives here)")
    ap.add_argument("--depths", default="meters,feet,fathoms", help="comma separated depth units to emit")
    ap.add_argument("--themes", default="day,dusk,night", help="comma separated themes to emit")
    ap.add_argument("--custom", default="", help="comma separated custom colour sets from colors.json (e.g. shom,sweden)")
    ap.add_argument("--shallow-depth", type=float, default=3.0)
    ap.add_argument("--safety-depth", type=float, default=6.0)
    ap.add_argument("--deep-depth", type=float, default=9.0)
    ap.add_argument("--skip-sprites", action="store_true", help="do not rebuild the sprite sheets")
    args = ap.parse_args(argv)

    assets = Path(args.assets)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    if not (assets / "sprites").is_dir() or not (assets / "fonts").is_dir():
        print(f"{assets} has no sprites/ and fonts/; run scripts/fetch_assets.sh first", file=sys.stderr)
        return 1

    depths = [Depth(d.strip()) for d in args.depths.split(",") if d.strip()]
    modes = [ThemeMode(t.strip().upper()) for t in args.themes.split(",") if t.strip()]
    customs = [None] + [c.strip() for c in args.custom.split(",") if c.strip()]

    sectors_file = output / "sectors.json"
    sectors = {"sheets": 1, "icons": {}}
    if sectors_file.exists():
        with sectors_file.open() as f:
            sectors = json.load(f)
    else:
        print(f"{sectors_file} not found (run convert_maps first); styles get no light sector icons")

    if args.skip_sprites and (output / "sprites").is_dir():
        sprites = {mode: [{"id": "default", "stem": f"{mode.path_name}_simplified"}] for mode in modes}
        if sectors["sheets"] > 1:
            for mode in modes:
                sprites[mode].extend(
                    {"id": f"sectors{k}", "stem": f"{mode.path_name}_sectors{k}"} for k in range(sectors["sheets"])
                )
    else:
        print("building sprite sheets")
        sprites = build_sprites(assets / "sprites", output / "sprites", sectors["icons"], sectors["sheets"], modes)

    fonts = output / "fonts"
    if fonts.exists():
        shutil.rmtree(fonts)
    shutil.copytree(assets / "fonts", fonts)

    colors = ColorLibrary.load()
    config = SymbologyConfig(args.shallow_depth, args.safety_depth, args.deep_depth)
    factory = LayerFactory(config=config, colors=colors, source=CHARTS_SOURCE, base_source=BASE_SOURCE)

    sources = {CHARTS_SOURCE: {"type": "vector", "url": "mbtiles://charts.mbtiles", "promoteId": "LNAM"}}
    if (output / "base.mbtiles").exists():
        sources[BASE_SOURCE] = {"type": "vector", "url": "mbtiles://base.mbtiles"}
    else:
        print("no base.mbtiles; the Natural Earth base layers stay empty (run convert_basemap to add it)")
        sources[BASE_SOURCE] = {"type": "vector", "url": "mbtiles://charts.mbtiles"}

    styles = {}
    for custom in customs:
        if custom and not colors.has_custom(custom):
            print(f"unknown custom colour set {custom!r}; available: {colors.custom_names()}", file=sys.stderr)
            return 1
        for mode in modes:
            theme = Theme(mode, custom)
            for depth in depths:
                id_ = style_id(depth, theme)
                doc = style(
                    factory,
                    depth,
                    theme,
                    sources=sources,
                    sprite=sprite_property(sprites[mode]),
                    glyphs="{fontstack}/{range}.pbf",
                    name=id_,
                )
                path = output / f"{id_}.json"
                with path.open("w") as f:
                    json.dump(doc, f, indent=2)
                    f.write("\n")
                # raster rendering (static images, png tiles) only for the main style: every
                # rendered style costs tileserver-gl a renderer pool with all sprite sheets decoded
                styles[id_] = {"style": path.name, "serve_rendered": id_ == "light"}
                print(f"  {path} ({len(doc['layers'])} layers)")

    config_json = {
        "options": {
            "paths": {"root": "", "styles": "", "sprites": "sprites", "fonts": "fonts", "mbtiles": ""},
            # every raster renderer decodes all sprite sheets (hundreds of MB with light sectors)
            "minRendererPoolSizes": [1, 1, 1],
            "maxRendererPoolSizes": [2, 2, 2],
        },
        "styles": styles,
        "data": {name: {"mbtiles": f"{name}.mbtiles"} for name in ("charts", "base") if (output / f"{name}.mbtiles").exists()},
    }
    with (output / "config.json").open("w") as f:
        json.dump(config_json, f, indent=2)
        f.write("\n")
    print(f"tileserver-gl config: {output / 'config.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
