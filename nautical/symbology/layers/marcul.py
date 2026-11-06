"""Marine farm/culture (MARCUL, code 82). Geometry: Point, Line, Area."""

from .prelude import *

LINE_COLOR = Color.CHGRD
SYMBOL = "MARCUL02"


class Marcul(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.line_color(LINE_COLOR)
        feature.area_pattern(SYMBOL)

    def layers(self, b):
        return [
            b.line_layer_with_color(LINE_COLOR, style=LineStyle.DASH_LINE, width=2.0),
            b.point_layer_from_symbol(symbol=Symbol.of(SYMBOL)),
            b.area_layer_with_single_symbol(symbol=SYMBOL),
        ]
