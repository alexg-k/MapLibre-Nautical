"""Radar reflector (RADRFL, code 101). Geometry: Point."""

from .prelude import *


class Radrfl(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("RADRFL03")

    def layers(self, b):
        return [
            b.point_layer_from_symbol(),
            b.area_layer_with_point_symbol(),
        ]
