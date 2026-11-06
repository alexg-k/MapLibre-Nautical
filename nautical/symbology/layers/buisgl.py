"""Building, single (BUISGL, code 12). Geometry: Point, Area.

``class Buisgl : Lndare()`` with ``areaColor = LANDF``.
"""

from .lndare import Lndare
from .prelude import *

LNDARE = Lndare(area_color=Color.LANDF)


class Buisgl(Layerable):
    def pre_tile_encode(self, feature, cx):
        LNDARE.pre_tile_encode(feature, cx)

    def layers(self, b):
        return LNDARE.layers(b)
