"""Buoy, installation (BOYINB, code 15). Geometry: Point."""

from .prelude import *


class Boyinb(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("BOYMOR11")

    def layers(self, b):
        return [b.point_layer_from_symbol()]
