"""Buoy, cardinal (BOYCAR, code 14). Geometry: Point."""

from .prelude import *

_SYMBOLS = {
    Catcam.NORTH_CARDINAL_MARK: "BOYCAR01",
    Catcam.EAST_CARDINAL_MARK: "BOYCAR02",
    Catcam.SOUTH_CARDINAL_MARK: "BOYCAR03",
    Catcam.WEST_CARDINAL_MARK: "BOYCAR04",
}


class Boycar(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol(_SYMBOLS.get(Catcam.of(feature.props), "BOYDEF03"))

    def layers(self, b):
        return [b.point_layer_from_symbol()]
