"""Buoy, safe water (BOYSAW, code 18). Geometry: Point."""

from .prelude import *


class Boysaw(Layerable):
    def pre_tile_encode(self, feature, cx):
        first = Colour.first(feature.props)
        feature.point_symbol("BOYSAW12" if first == Colour.RED else "BOYSPP11")

    def layers(self, b):
        return [b.point_layer_from_symbol()]
