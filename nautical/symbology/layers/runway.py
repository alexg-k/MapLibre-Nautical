"""Runway (RUNWAY, code 117). Geometry: Point, Line, Area."""

from .prelude import *

AREA_COLOR = Color.CHBRN
LINE_COLOR = Color.CHBLK
SYMBOL = "AIRARE02"


class Runway(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.line_color(LINE_COLOR)
        feature.area_color(AREA_COLOR)
        feature.point_symbol(SYMBOL)

    def layers(self, b):
        return [
            b.line_layer_with_color(LINE_COLOR),
            b.area_layer_with_fill_color(AREA_COLOR),
            b.point_layer_from_symbol(symbol=Symbol.of(SYMBOL)),
        ]
