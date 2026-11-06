"""Ice area (ICEARE, code 66). Geometry: Area."""

from .prelude import *


class Iceare(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("ICEARE04P")
        feature.area_pattern("ICEARE04P")

    def layers(self, b):
        return [
            b.point_layer_from_symbol(),
            b.area_layer_with_fill_pattern("ICEARE04P"),
        ]
