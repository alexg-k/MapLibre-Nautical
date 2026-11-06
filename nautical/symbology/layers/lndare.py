"""Land area (LNDARE, code 71). Geometry: Point, Line, Area.

Land areas, with a configurable area colour; ``Buisgl``, ``Slcons`` and the Natural Earth
``Land`` / ``MinorIslands`` delegate to it.
"""

from .prelude import *


class Lndare(Layerable):
    def __init__(self, area_color=Color.LANDA):
        self.area_color = area_color

    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("LNDARE01")
        feature.area_color(self.area_color)

    def layers(self, b):
        return [
            b.area_layer_with_fill_color(self.area_color),
            b.line_layer_with_color(Color.CSTLN, width=2.0),
            b.point_layer_from_symbol(
                anchor=Anchor.CENTER,
                icon_allow_overlap=True,
                icon_rotation_alignment=IconRotationAlignment.MAP,
            ),
        ]
