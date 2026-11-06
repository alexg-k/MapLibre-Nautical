"""Cargo transshipment area (CTSARE, code 25). Geometry: Point, Area."""

from .prelude import *

LINE_COLOR = Color.CHMGF


class Ctsare(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("CHINFO07")
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [
            b.point_layer_from_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP),
            b.line_layer_with_color(LINE_COLOR, style=LineStyle.DASH_LINE),
        ]
