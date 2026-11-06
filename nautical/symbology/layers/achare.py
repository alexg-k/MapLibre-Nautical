"""Anchorage area (ACHARE, code 4). Geometry: Point, Area."""

from .prelude import *

LINE_COLOR = Color.CHMGF


class Achare(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("ACHARE02")
        feature.line_pattern("ACHARE02")

    def layers(self, b):
        return [
            b.point_layer_from_symbol(),
            b.line_layer_with_color(LINE_COLOR, width=2.0, style=LineStyle.custom_dash(3.0, 4.0)),
            b.line_layer_with_pattern(),
            b.line_layer_with_label(Label(prop="OBJNAM")),
        ]
