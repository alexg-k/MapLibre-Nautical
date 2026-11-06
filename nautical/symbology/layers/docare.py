"""Dock area (DOCARE, code 45). Geometry: Area."""

from .prelude import *

AREA_COLOR = Color.DEPVS
LINE_COLOR = Color.CHGRD


class Docare(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.area_color(AREA_COLOR)
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [
            b.area_layer_with_fill_color(AREA_COLOR),
            b.line_layer_with_color(LINE_COLOR, width=0.5),
        ]
