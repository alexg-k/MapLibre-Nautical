"""Crane (CRANES, code 35). Geometry: Point, Area."""

from .prelude import *

LINE_COLOR = Color.CHBLK
AREA_COLOR = Color.CHBRN


class Cranes(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("CRANES01")
        feature.line_color(LINE_COLOR)
        feature.area_color(AREA_COLOR)

    def layers(self, b):
        return [
            b.point_layer_from_symbol(),
            b.area_layer_with_fill_color(AREA_COLOR),
            b.area_layer_with_point_symbol(),
            b.line_layer_with_color(LINE_COLOR),
        ]
