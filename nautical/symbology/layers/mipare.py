"""Military practice area (MIPARE, code 83). Geometry: Point, Area."""

from .prelude import *

LINE_COLOR = Color.CHMGD


class Mipare(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("CHINFO06")
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [
            b.point_layer_from_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP),
            b.area_layer_with_point_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP),
            b.line_layer_with_color(LINE_COLOR, style=LineStyle.DASH_LINE),
        ]
