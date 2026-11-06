"""Weed / kelp (WEDKLP, code 158). Geometry: Point, Area."""

from .prelude import *

LINE_COLOR = Color.CHGRF


class Wedklp(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("WEDKLP03")
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [
            b.point_layer_from_symbol(),
            b.area_layer_with_single_symbol(),
            b.line_layer_with_color(LINE_COLOR, style=LineStyle.DASH_LINE, width=1.0),
        ]
