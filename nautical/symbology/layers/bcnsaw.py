"""Beacon, safe water (BCNSAW, code 8). Geometry: Point.

``class Bcnsaw : Bcnlat()``.
"""

from .bcnlat import bcnshp
from .prelude import *


class Bcnsaw(Layerable):
    def pre_tile_encode(self, feature, cx):
        bcnshp(feature)

    def layers(self, b):
        return [b.point_layer_from_symbol()]
