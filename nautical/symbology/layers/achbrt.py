"""Anchor berth (ACHBRT, code 3). Geometry: Point, Area."""

from .prelude import *

LINE_COLOR = Color.CHMGF


class Achbrt(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.line_color(LINE_COLOR)
        feature.point_symbol("ACHBRT07")

    def layers(self, b):
        return [
            b.point_layer_from_symbol(),
            b.line_layer_with_color(LINE_COLOR, width=2.0, style=LineStyle.DASH_LINE),
        ]
