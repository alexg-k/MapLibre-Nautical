"""Coastguard station (CGUSTA, code 29). Geometry: Point."""

from .prelude import *


class Cgusta(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("CGUSTA02")

    def layers(self, b):
        return [b.point_layer_from_symbol(anchor=Anchor.BOTTOM_LEFT)]
