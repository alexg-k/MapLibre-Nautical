"""Fence/wall (FNCLNE, code 52). Geometry: Line."""

from .prelude import *

LINE_COLORS = [Color.CHBLK, Color.LANDF]


class Fnclne(Layerable):
    def pre_tile_encode(self, feature, cx):
        if Convis.of(feature.props) == Convis.VISUAL_CONSPICUOUS:
            feature.line_color(Color.CHBLK)
        else:
            # NOT_VISUAL_CONSPICUOUS, None
            feature.line_color(Color.LANDF)

    def layers(self, b):
        return [b.line_layer_with_colors(LINE_COLORS, width=1.0)]
