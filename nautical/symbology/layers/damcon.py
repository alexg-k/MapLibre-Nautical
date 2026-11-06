"""Dam (DAMCON, code 38). Geometry: Point, Line, Area."""

from .prelude import *


class Damcon(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("CHINFO06")

    def layers(self, b):
        return [
            b.point_layer_from_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP),
            b.line_layer_with_color(Color.CSTLN),
            b.area_layer_with_fill_color(Color.LANDF),
        ]
