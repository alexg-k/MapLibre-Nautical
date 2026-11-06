"""Shoreline construction (SLCONS, code 122). Geometry: Point, Line, Area.

``class Slcons : Lndare()``.
"""

from .lndare import Lndare
from .prelude import *


class Slcons(Layerable):
    def pre_tile_encode(self, feature, cx):
        Lndare().pre_tile_encode(feature, cx)

    def layers(self, b):
        return Lndare().layers(b)
