"""Traffic control point (TCTLPT, code 144). Geometry: Point."""

from .prelude import *

SYMBOL = "CHKPNT01"


class Tctlpt(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol(SYMBOL)

    def layers(self, b):
        return [b.point_layer_from_symbol(symbol=Symbol.of(SYMBOL), anchor=Anchor.CENTER)]
