"""Fishing ground (FSHGRD, code 56). Geometry: Area."""

from .prelude import *

LINE_COLOR = Color.CHMGD


class Fshgrd(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("FSHGRD01")
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [
            b.line_layer_with_color(LINE_COLOR),
            b.area_layer_with_single_symbol(),
        ]
