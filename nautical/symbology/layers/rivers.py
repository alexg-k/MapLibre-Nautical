"""River (RIVERS, code 114). Geometry: Line, Area.

``class Rivers : Canals()``.
"""

from .canals import Canals
from .prelude import *


class Rivers(Layerable):
    def pre_tile_encode(self, feature, cx):
        Canals().pre_tile_encode(feature, cx)

    def layers(self, b):
        return Canals().layers(b)
