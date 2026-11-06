"""Pile (PILPNT, code 90). Geometry: Point."""

from .prelude import *

SYMBOL = "PILPNT02"


class Pilpnt(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol(SYMBOL)

    def layers(self, b):
        return [b.point_layer_from_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP)]
