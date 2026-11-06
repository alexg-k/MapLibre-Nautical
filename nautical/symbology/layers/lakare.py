"""Lake (LAKARE, code 69). Geometry: Area."""

from .prelude import *


class Lakare(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.line_color(Color.CSTLN)
        feature.area_color(Color.DEPDW)
        feature.line_color(Color.CSTLN)

    def layers(self, b):
        return [
            b.area_layer_with_fill_color(Color.DEPDW),
            b.line_layer_with_color(Color.CSTLN, style=LineStyle.SOLID, width=1.0),
        ]
