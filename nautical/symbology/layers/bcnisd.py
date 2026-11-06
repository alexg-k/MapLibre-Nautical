"""Beacon, isolated danger (BCNISD, code 6). Geometry: Point."""

from .prelude import *


class Bcnisd(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("BCNISD21")

    def layers(self, b):
        return [b.point_layer_from_symbol()]
