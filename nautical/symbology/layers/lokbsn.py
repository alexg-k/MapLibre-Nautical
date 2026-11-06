"""Lock basin (LOKBSN, code 79). Geometry: Area.

Registered twice: as ``LOKBSN`` (standard) and ``lokbsn`` (inland).
"""

from .prelude import *

AREA_COLOR = Color.DEPVS
LINE_COLOR = Color.CHBLK


class Lokbsn(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.area_color(AREA_COLOR)
        feature.line_color(LINE_COLOR)

    def layers(self, b):
        return [
            b.area_layer_with_fill_color(AREA_COLOR, None),
            b.line_layer_with_color(LINE_COLOR, width=1.0),
        ]
