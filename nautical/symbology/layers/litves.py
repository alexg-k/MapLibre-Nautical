"""Light vessel (LITVES, code 77). Geometry: Point."""

from .prelude import *

SYMBOL = "LITVES02"


class Litves(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol(SYMBOL)

    def layers(self, b):
        return [b.point_layer_from_symbol(symbol=Symbol.of(SYMBOL))]
