"""Pontoon (PONTON)."""

from .prelude import *


class Ponton(Layerable):
    def layers(self, b):
        return [
            b.area_layer_with_fill_color(Color.CHBRN),
            b.line_layer_with_color(Color.CSTLN, width=2.0),
        ]
