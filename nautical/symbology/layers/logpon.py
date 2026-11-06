"""Log pond (LOGPON, code 80). Geometry: Point, Area."""

from .prelude import *

LINE_COLOR = Color.CHBLK


class Logpon(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("FLTHAZ02")
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [
            b.point_layer_from_symbol(),
            b.line_layer_with_color(LINE_COLOR, width=1.0, style=LineStyle.custom_dash(3.0, 4.0)),
        ]
