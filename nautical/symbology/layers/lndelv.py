"""Land elevation (LNDELV, code 75). Geometry: Point, Line.

S-52 lookups: a point is ``SY(POSGEN04);TE('%3.0lf m','ELEVAT',3,2,2,'15110',1,0,CHBLK,28)``, a
line (a land contour) is ``LS(SOLD,1,LANDF)`` with no text.
"""

from .prelude import *

FEET_PER_METER = 3.28084


class Lndelv(Layerable):
    def pre_tile_encode(self, feature, cx):
        feature.point_symbol("POSGEN04")

    def layers(self, b):
        return [
            b.line_layer_with_color(Color.LANDF, width=1.0, filter=filters.eq_type_line_string()),
            b.point_layer_from_symbol(anchor=Anchor.CENTER),
            b.text_layer(
                elevation(b.depth),
                text_anchor=Anchor.LEFT,
                text_justify=TextJustify.LEFT,
                text_offset=Offset.coord(1.2, 0.0),
                filter=[filters.ALL, filters.eq_type_point(), ["has", "ELEVAT"]],
            ),
        ]


def elevation(depth):
    """Whole units, per ``%3.0lf``. Like ``ClearanceLabel`` the tile stays unit-agnostic and the
    style picks metres or feet from the depth preference."""
    if depth == Depth.METERS:
        return ["concat", ["to-string", ["round", ["get", "ELEVAT"]]], "m"]
    return ["concat", ["to-string", ["round", ["*", ["get", "ELEVAT"], FEET_PER_METER]]], "ft"]
