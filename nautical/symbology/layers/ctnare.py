"""Caution area (CTNARE, code 27). Geometry: Point, Area."""

from .prelude import *

LINE_COLOR = Color.TRFCD


class Ctnare(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("CHINFO06")

    def layers(self, b):
        return [
            b.point_layer_from_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP),
            b.area_layer_with_point_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP),
            b.line_layer_with_color(LINE_COLOR, style=LineStyle.DASH_LINE),
        ]
