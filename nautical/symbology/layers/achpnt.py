"""Anchor (ACHPNT, code 1003). Geometry: Point.

S-52 display: SY(ACHPNT01), rendered using ACHARE02 (identical symbol).
"""

from .prelude import *


class Achpnt(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("ACHARE02")

    def layers(self, b):
        return [b.point_layer_from_symbol(symbol=Symbol.of("ACHARE02"), anchor=Anchor.CENTER)]
