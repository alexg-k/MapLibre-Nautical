"""Offshore production area (OSPARE, code 88). Geometry: Area."""

from .prelude import *

SYMBOL = "CTYARE51"
COLOR = Color.CHMGD


class Ospare(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol(SYMBOL)

    def layers(self, b):
        return [
            b.line_layer_with_color(COLOR, style=LineStyle.DASH_LINE, width=2.0),
            b.point_layer_from_symbol(symbol=Symbol.of(SYMBOL)),
        ]
