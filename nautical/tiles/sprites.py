"""Sprite sheets: njord's per-theme sheets plus the light sector icons of a chart set.

A sector icon is a 200×200 SVG (``nautical.symbology.sector_svg``) rasterized at 1x and 2x. With
one sector sheet the icons are appended to the theme's base sheet; with more, each sheet
``<theme>_sectors<k>`` holds the icons hashed to it (``encode.sector_sheet``) and the style lists
every sheet under MapLibre's multi-sprite form.
"""

import io
import json
import math
from pathlib import Path

from PIL import Image

from ..symbology.colors import ThemeMode
from ..symbology.sector_svg import SectorIcon

ICON_SIZE = 200
COLUMNS = 16


def render_svg(svg, size):
    import cairosvg

    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=size, output_height=size)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def load_sheet(path_stem):
    """``(json, image)`` of a sprite sheet given its path without extension."""
    with open(f"{path_stem}.json") as f:
        index = json.load(f)
    image = Image.open(f"{path_stem}.png").convert("RGBA")
    for name in [n for n, e in index.items() if e["x"] < 0 or e["y"] < 0]:
        # njord's sheets carry one entry outside the image (FSHFAC03), which renderers reject
        print(f"  dropping invalid sprite {name} from {Path(path_stem).name}")
        del index[name]
    return index, image


def save_sheet(path_stem, index, image):
    Path(path_stem).parent.mkdir(parents=True, exist_ok=True)
    with open(f"{path_stem}.json", "w") as f:
        json.dump(index, f, separators=(",", ":"))
    image.save(f"{path_stem}.png", optimize=True)


def pack_icons(icons, ratio, base=None):
    """Lays ``icons`` (``{name: Image}``) out in rows under the optional ``base`` sheet
    ``(index, image)``; answers the combined ``(index, image)``."""
    size = ICON_SIZE * ratio
    names = sorted(icons)
    columns = min(COLUMNS, max(1, len(names)))
    rows = math.ceil(len(names) / columns) if names else 0
    base_index, base_image = base if base else ({}, None)
    base_w = base_image.width if base_image else 0
    base_h = base_image.height if base_image else 0
    width = max(base_w, columns * size)
    height = base_h + rows * size
    image = Image.new("RGBA", (max(width, 1), max(height, 1)), (0, 0, 0, 0))
    index = dict(base_index)
    if base_image:
        image.paste(base_image, (0, 0))
    for i, name in enumerate(names):
        x = (i % columns) * size
        y = base_h + (i // columns) * size
        image.paste(icons[name], (x, y))
        index[name] = {"width": size, "height": size, "x": x, "y": y, "pixelRatio": ratio}
    return index, image


def build_sprites(assets_sprites, output_sprites, sector_sheets, sheets=1, themes=ThemeMode):
    """Writes the sprite sheets of every theme to ``output_sprites``; answers
    ``{theme: [sprite entries]}`` for the style's ``sprite`` property (relative stems).

    ``sector_sheets`` is ``{icon name: sheet index}`` (``sectors.json``); with ``sheets`` 1 the
    icons join the base sheet."""
    assets_sprites = Path(assets_sprites)
    output_sprites = Path(output_sprites)
    output_sprites.mkdir(parents=True, exist_ok=True)
    parsed = [SectorIcon.parse(n) for n in sector_sheets]
    parsed = [p for p in parsed if p is not None]
    result = {}
    for mode in themes:
        base_stem = f"{mode.path_name}_simplified"
        rendered = {ratio: {} for ratio in (1, 2)}
        for icon in parsed:
            svg = icon.svg(mode)
            for ratio in (1, 2):
                rendered[ratio][icon.name] = render_svg(svg, ICON_SIZE * ratio)
        entries = []
        for ratio in (1, 2):
            suffix = "" if ratio == 1 else "@2x"
            base = load_sheet(assets_sprites / f"{base_stem}{suffix}")
            if sheets <= 1:
                index, image = pack_icons(rendered[ratio], ratio, base)
                save_sheet(output_sprites / f"{base_stem}{suffix}", index, image)
            else:
                save_sheet(output_sprites / f"{base_stem}{suffix}", *base)
                for k in range(sheets):
                    icons = {n: im for n, im in rendered[ratio].items() if sector_sheets[n] == k}
                    index, image = pack_icons(icons, ratio)
                    save_sheet(output_sprites / f"{mode.path_name}_sectors{k}{suffix}", index, image)
        if sheets <= 1:
            entries.append({"id": "default", "stem": base_stem})
        else:
            entries.append({"id": "default", "stem": base_stem})
            entries.extend({"id": f"sectors{k}", "stem": f"{mode.path_name}_sectors{k}"} for k in range(sheets))
        result[mode] = entries
        print(f"  {mode.path_name}: {len(parsed)} sector icons in {max(1, sheets)} sheet(s)")
    return result
