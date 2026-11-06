"""Sloping ground (SLOGRD, code 127). Geometry: Area."""

from .prelude import *


class Slogrd(Layerable):
    def layers(self, b):
        return [
            b.area_layer_with_fill_color(Color.LANDF),
            b.line_layer_with_color(Color.CSTLN),
        ]
