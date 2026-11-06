"""Precautionary area (PRCARE, code 96). Geometry: Point, Area."""

from .prelude import *

LINE_COLOR = Color.TRFCF
SYMBOL = "PRCARE12"


class Prcare(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol(SYMBOL)
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [
            b.point_layer_from_symbol(symbol=Symbol.of(SYMBOL)),
            b.line_layer_with_color(LINE_COLOR, width=2.0, style=LineStyle.custom_dash(3.0, 2.0)),
            # Room for lights / buoys.
            b.area_layer_with_point_symbol(symbol=SYMBOL, icon_offset=[30.0, 30.0]),
        ]
