"""Cable, overhead (CBLOHD). Geometry: Line."""

from .prelude import *


class Cblohd(Layerable):
    def layers(self, b):
        return [b.line_layer_with_color(Color.CHBLK, width=0.5, style=LineStyle.custom_dash(10.0, 5.0))]
