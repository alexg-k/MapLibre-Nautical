"""Beacon, cardinal (BCNCAR, code 5). Geometry: Point."""

from .prelude import *

_SYMBOLS = {
    Catcam.NORTH_CARDINAL_MARK: "BCNCAR01",
    Catcam.EAST_CARDINAL_MARK: "BCNCAR02",
    Catcam.SOUTH_CARDINAL_MARK: "BCNCAR03",
    Catcam.WEST_CARDINAL_MARK: "BCNCAR04",
}


class Bcncar(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol(_SYMBOLS.get(Catcam.of(feature.props), "BCNDEF13"))

    def layers(self, b):
        return [b.point_layer_from_symbol()]
