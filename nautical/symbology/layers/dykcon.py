"""Dyke (DYKCON, code 49). Geometry: Line, Area."""

from .prelude import *

LINE_COLOR = Color.LANDF
AREA_COLOR = Color.CHBRN


class Dykcon(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.area_color(AREA_COLOR)
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [
            b.line_layer_with_color(LINE_COLOR),
            b.area_layer_with_fill_color(AREA_COLOR),
        ]
