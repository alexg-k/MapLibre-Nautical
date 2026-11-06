"""Lake shore (LAKSHR, code 70). Geometry: Line, Area."""

from .prelude import *

LINE_COLOR = Color.CSTLN


class Lakshr(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [b.line_layer_with_color(LINE_COLOR, style=LineStyle.SOLID, width=1.0)]
