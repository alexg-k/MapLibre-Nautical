"""Radar station (RADSTA, code 104). Geometry: Point.

S-52 lookups: ``SY(POSGEN01)``, or for a radar surveillance station (CATRAS 2)
``SY(RDOSTA02);TE('ch %s','COMCHA',3,1,2,'15110',0,0,CHBLK,11)``.
"""

from .prelude import *

SURVEILLANCE = "_SURV"


class Radsta(Layerable):
    def pre_tile_encode(self, feature, cx):
        if int_value(feature.props, "CATRAS") == 2:
            feature.point_symbol("RDOSTA02")
            feature.props[SURVEILLANCE] = True
        else:
            feature.point_symbol("POSGEN01")

    def layers(self, b):
        return [
            b.point_layer_from_symbol(),
            b.text_layer(
                ["concat", "ch ", ["to-string", ["get", "COMCHA"]]],
                text_anchor=Anchor.BOTTOM_LEFT,
                text_justify=TextJustify.LEFT,
                filter=[filters.ALL, ["has", SURVEILLANCE], ["has", "COMCHA"]],
            ),
        ]
