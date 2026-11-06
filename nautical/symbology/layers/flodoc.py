"""Floating dock (FLODOC, code 57). Geometry: Line, Area."""

from .prelude import *

AREA_COLOR = Color.CHBRN
LINE_COLOR = Color.CSTLN


class Flodoc(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.area_color(AREA_COLOR)
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [
            b.area_layer_with_fill_color(AREA_COLOR),
            b.line_layer_with_color(LINE_COLOR),
        ]
