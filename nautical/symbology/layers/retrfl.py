"""Retro-reflector (RETRFL, code 112). Geometry: Point."""

from .prelude import *

SYMBOL = "RETRFL02"


class Retrfl(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol(SYMBOL)

    def layers(self, b):
        return [b.point_layer_from_symbol(symbol=Symbol.of(SYMBOL), anchor=Anchor.CENTER)]
