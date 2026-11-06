"""Natural Earth base layers, drawn under the charts."""

from .canals import Canals
from .lakare import Lakare
from .lndare import Lndare
from .prelude import *


class AntarcticIceShelves(Layerable):
    def layers(self, b):
        return [
            b.area_layer_with_fill_color(Color.CHWHT),
            b.line_layer_with_color(Color.CSTLN, width=0.5),
        ]


class Bathymetry(Layerable):
    def layers(self, b):
        return [b.area_layer_with_fill_color(Color.DEPMD)]


class Coastline(Layerable):
    def layers(self, b):
        return [b.line_layer_with_color(Color.CSTLN, width=1.0)]


class GlaciatedAreas(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("ICEARE04P")
        feature.area_pattern("ICEARE04P")

    def layers(self, b):
        return [
            b.point_layer_from_symbol(symbol=Symbol.of("ICEARE04P")),
            b.area_layer_with_fill_pattern("ICEARE04P"),
            b.line_layer_with_color(Color.CSTLN, width=0.5),
        ]


class Lakes(Layerable):
    source_layer = "lakes"

    def pre_tile_encode(self, feature, cx):
        Lakare().pre_tile_encode(feature, cx)

    def layers(self, b):
        return Lakare().layers(b)


class Land(Layerable):
    source_layer = "land"

    def pre_tile_encode(self, feature, cx):
        Lndare().pre_tile_encode(feature, cx)

    def layers(self, b):
        return Lndare().layers(b)


class MinorIslands(Layerable):
    source_layer = "minor_islands"

    def pre_tile_encode(self, feature, cx):
        Lndare().pre_tile_encode(feature, cx)

    def layers(self, b):
        return Lndare().layers(b)


class Ocean(Layerable):
    def layers(self, b):
        return [b.area_layer_with_fill_color(Color.DEPDW)]


class Playas(Layerable):
    def layers(self, b):
        return [
            b.area_layer_with_fill_color(Color.LANDA),
            b.line_layer_with_color(Color.CSTLN, width=0.5),
        ]


class Reefs(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.area_pattern("FOULAR01P")

    def layers(self, b):
        return [
            b.point_layer_from_symbol(symbol=Symbol.of("FOULAR01P")),
            b.area_layer_with_fill_pattern("FOULAR01P"),
            b.line_layer_with_color(Color.CSTLN, width=0.5),
        ]


class RiversLakeCenterlines(Layerable):
    source_layer = "rivers_lake_centerlines"

    def pre_tile_encode(self, feature, cx):
        Canals().pre_tile_encode(feature, cx)

    def layers(self, b):
        return Canals().layers(b)
