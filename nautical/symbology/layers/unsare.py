"""Unsurveyed area (UNSARE, code 154). Geometry: Area."""

from .prelude import *


class Unsare(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.area_color(Color.NODTA)
        feature.area_pattern("NODATA03P")
        feature.line_color(Color.CHGRD)

    def layers(self, b):
        return [
            b.area_layer_with_fill_color(Color.NODTA),
            b.line_layer_with_color(Color.CHGRD),
            b.area_layer_with_fill_pattern("NODATA03P"),
        ]
