"""Checkpoint (CHKPNT, code 28). Geometry: Point, Area."""

from .prelude import *


class Chkpnt(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("POSGEN04")
        feature.line_color(Color.CHBLK)

    def layers(self, b):
        return [
            b.line_layer_with_color(Color.CHBLK),
            b.point_layer_from_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP),
        ]
