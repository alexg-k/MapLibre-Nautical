"""Distance mark (DISMAR, code 44). Geometry: Point.

https://njord.mxmariner.com/control/symbols/DISMAR
"""

from .prelude import *


class Dismar(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("DISMAR06")

    def layers(self, b):
        return [b.point_layer_from_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP)]
