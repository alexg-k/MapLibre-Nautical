"""Canal (CANALS, code 23). Geometry: Line, Area.

Canals, with a configurable fill colour; ``Rivers`` and the Natural Earth
``RiversLakeCenterlines`` delegate to it.
"""

from .prelude import *


class Canals(Layerable):
    def __init__(self, fill_color=Color.DEPVS):
        self.fill_color = fill_color

    def pre_tile_encode(self, feature, cx):
        feature.area_color(self.fill_color)

    def layers(self, b):
        return [
            b.line_layer_with_color(Color.CHBLK, width=0.5),
            b.area_layer_with_fill_color(self.fill_color),
        ]
