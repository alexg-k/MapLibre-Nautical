"""Pylon/bridge support (PYLONS, code 98). Geometry: Point, Area."""

from .prelude import *

AREA_COLOR = Color.CHBRN
LINE_COLOR = Color.CSTLN


class Pylons(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.area_color(AREA_COLOR)
        feature.line_color(LINE_COLOR)
        feature.point_symbol("POSGEN03")

    def layers(self, b):
        return [
            b.point_layer_from_symbol(),
            b.area_layer_with_fill_color(AREA_COLOR),
            b.line_layer_with_color(LINE_COLOR, width=2.0),
        ]
