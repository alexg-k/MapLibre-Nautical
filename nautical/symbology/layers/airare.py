"""Airport / airfield (AIRARE, code 2). Geometry: Point, Area."""

from .prelude import *

AREA_COLOR = Color.LANDA
LINE_COLOR = Color.LANDF
SYMBOL = "AIRARE02"


class Airare(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.area_color(AREA_COLOR)
        feature.line_color(LINE_COLOR)
        feature.point_symbol(SYMBOL)

    def layers(self, b):
        return [
            b.point_layer_from_symbol(),
            b.area_layer_with_fill_color(AREA_COLOR),
            b.area_layer_with_point_symbol(symbol=SYMBOL),
            b.line_layer_with_color(LINE_COLOR, width=1.0),
        ]
