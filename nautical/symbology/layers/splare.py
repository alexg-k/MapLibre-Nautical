"""Spoil area (SPLARE, code 131). Geometry: Area."""

from .prelude import *

LINE_COLOR = Color.CHMGD


class Splare(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("CHINFO07")
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [
            b.area_layer_with_point_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP),
            b.line_layer_with_color(LINE_COLOR, style=LineStyle.DASH_LINE),
        ]
