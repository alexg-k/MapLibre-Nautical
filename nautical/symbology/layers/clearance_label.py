"""Vertical and horizontal clearance labels: CHBLK on a CHWHT halo, per the S-52 presentation
library's ``TE('clr %4.1lf','VERCLR',3,1,2,'15110',1,1,CHBLK,11)``.

Registered separately, late in the draw order (clearance is text group 11 and display-base),
under the key ``<CLASS>_CLEARANCE``. The text is composed by style expressions off the raw
attributes, so the same tile serves feet and metres.
"""

from .prelude import *

#: Marks a BRIDGE whose CATBRG is an opening type, so the style reads VERCCL/VERCOP.
OPENING_BRIDGE = "_OPBR"

FEET_PER_METER = 3.28084


def opening_bridge(feature):
    feature.props[OPENING_BRIDGE] = True


class ClearanceLabel(Layerable):
    def __init__(self, object_class):
        self.object_class = object_class

    @property
    def key(self):
        return f"{self.object_class}_CLEARANCE"

    @property
    def source_layer(self):
        return self.object_class

    def layers(self, b):
        """Unfiltered by geometry type and placed as a point, so a bridge encoded as a polygon,
        a line or a point all get one upright label at the geometry's centre. The two labels
        anchor away from each other vertically so an opening bridge's two-line label grows upward
        without running into ``hor clr`` below it."""
        return [
            _label(b, f"{b.key}_vertical", vertical_text(b.depth), Anchor.BOTTOM_LEFT, Offset.coord(1.2, -0.3)),
            _label(b, f"{b.key}_horizontal", horizontal_text(b.depth), Anchor.TOP_LEFT, Offset.coord(1.2, 0.3)),
        ]


def _label(b, id_, text, text_anchor, offset):
    return b.layer(
        id_,
        LayerType.SYMBOL,
        layout=layout(
            text_font=[Font.ROBOTO_BOLD],
            text_anchor=text_anchor,
            text_justify=TextJustify.LEFT,
            text_field=text,
            text_offset=offset.property(),
            text_size=14.0,
            # Zeroed so the default collision buffer doesn't bridge the gap between the pair.
            text_padding=0.0,
            symbol_placement=Placement.POINT,
        ),
        paint=b.label_paint(Color.SNDG2, Color.DEPDW),
    )


def vertical_text(depth):
    opening = ["has", OPENING_BRIDGE]
    return [
        "case",
        ["all", opening, present("VERCCL"), present("VERCOP")],
        ["concat", "clr cl ", clearance("VERCCL", depth), "\n", "clr op ", clearance("VERCOP", depth)],
        ["all", opening, present("VERCCL")],
        ["concat", "clr cl ", clearance("VERCCL", depth)],
        ["all", opening, present("VERCOP")],
        ["concat", "clr op ", clearance("VERCOP", depth)],
        ["all", present("VERCLR"), present("VERCSA")],
        ["concat", "clr ", clearance("VERCLR", depth), "\n", "sf clr ", clearance("VERCSA", depth)],
        present("VERCLR"),
        ["concat", "clr ", clearance("VERCLR", depth)],
        present("VERCSA"),
        ["concat", "sf clr ", clearance("VERCSA", depth)],
        "",
    ]


def horizontal_text(depth):
    """Not rendered by S-52 at all; horizontal clearance is a njord addition."""
    return ["case", present("HORCLR"), ["concat", "hor clr ", clearance("HORCLR", depth)], ""]


def present(key):
    """``has`` alone isn't enough: a zero clearance would render as ``clr 0.0m``."""
    return ["all", ["has", key], [">", ["get", key], 0]]


def clearance(key, depth):
    if depth == Depth.METERS:
        return [
            "concat",
            ["number-format", ["get", key], {"locale": "en-US", "min-fraction-digits": 1, "max-fraction-digits": 1}],
            "m",
        ]
    return ["concat", ["to-string", ["round", ["*", ["get", key], FEET_PER_METER]]], "ft"]
