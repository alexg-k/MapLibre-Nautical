"""Traffic separation zone (TSEZNE, code 150). Geometry: Area."""

from .prelude import *

AC = Color.TRFCF


class Tsezne(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.area_color(AC)

    def layers(self, b):
        return [b.area_layer_with_fill_color(AC, 0.25)]
