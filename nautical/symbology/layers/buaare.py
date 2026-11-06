"""Built-up area (BUAARE, code 13). Geometry: Point, Area."""

from .prelude import *


class Buaare(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("BUAARE02")
        feature.area_color(Color.LANDF)

    def layers(self, b):
        return [
            b.area_layer_with_fill_color(Color.CHBRN),
            b.line_layer_with_color(Color.CSTLN, width=1.0),
            b.point_layer_from_symbol(),
        ]
