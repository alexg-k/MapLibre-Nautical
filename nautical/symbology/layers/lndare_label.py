"""Land area (LNDARE, code 71). Geometry: Point, Line, Area.

The land area names, split out of ``Lndare`` so they are registered with the low-priority
labels, late in the draw order.
"""

from .prelude import *


class LndareLabel(Layerable):
    source_layer = "LNDARE"

    def layers(self, b):
        return [b.area_layer_with_text(Label(prop="OBJNAM"), halo_color=Color.LANDA, text_optional=True)]
