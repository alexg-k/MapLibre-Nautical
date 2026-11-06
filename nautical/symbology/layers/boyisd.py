"""Buoy, isolated danger (BOYISD, code 16). Geometry: Point."""

from .prelude import *


class Boyisd(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("BOYISD12")

    def layers(self, b):
        return [b.point_layer_from_symbol()]
