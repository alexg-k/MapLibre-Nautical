"""New object (NEWOBJ, code 89). Geometry: Point, Line, Area."""

from .prelude import *

SYMBOL = "NEWOBJ01"


class Newobj(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol(SYMBOL)
        feature.line_color(Color.CHBLK)

    def layers(self, b):
        return [
            b.point_layer_from_symbol(symbol=Symbol.of(SYMBOL), anchor=Anchor.CENTER),
            b.area_layer_with_point_symbol(anchor=Anchor.CENTER),
            b.line_layer_with_color(Color.CHBLK),
        ]
