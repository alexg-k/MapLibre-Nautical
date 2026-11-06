"""Incineration area (ICNARE, code 67). Geometry: Point, Area."""

from .prelude import *

LINE_COLOR = Color.CHMGF
SYMBOL = "CHINFO07"


class Icnare(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.line_color(LINE_COLOR)
        feature.area_pattern(SYMBOL)

    def layers(self, b):
        return [
            b.line_layer_with_color(LINE_COLOR, style=LineStyle.DASH_LINE, width=1.0),
            b.point_layer_from_symbol(
                symbol=Symbol.of(SYMBOL),
                anchor=Anchor.CENTER,
                icon_rotation_alignment=IconRotationAlignment.MAP,
            ),
            b.area_layer_with_single_symbol(symbol=SYMBOL),
        ]
