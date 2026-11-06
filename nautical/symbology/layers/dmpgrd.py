"""Dumping ground (DMPGRD, code 48). Geometry: Point, Area."""

from .prelude import *

LINE_COLOR = Color.CHMGD


class Dmpgrd(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("CHINFO07")

    def layers(self, b):
        return [
            b.point_layer_from_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP),
            b.line_layer_with_color(LINE_COLOR, width=1.0, style=LineStyle.DASH_LINE),
        ]
