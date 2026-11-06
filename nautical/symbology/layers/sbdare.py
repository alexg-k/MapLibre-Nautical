"""Seabed area (SBDARE, code 116). Geometry: Point, Line, Area.

S-52 lookups: ``TX(NATSUR,1,2,2,'15110',0,0,CHBLK,25)`` on every geometry, centred, plus
``LS(SOLD,1,CHGRD)`` on a line and ``LS(DASH,1,CHGRD)`` around an area whose WATLEV is 3 (always
under water) or 4 (covers and uncovers). No fill.

Not done: an intertidal (WATLEV 4) rock, lava or coral area is filled with the RCKLDG01 pattern
in place of the text, but that pattern is vector-only in the presentation library and isn't in
the sprite sheets, so those areas get the text instead.
"""

from .prelude import *

NATURE_OF_SURFACE = "_NS"
DASHED_OUTLINE = "_DO"

_NATSUR_ABBREVIATIONS = {
    1: "M",
    2: "Cy",
    3: "Si",
    4: "S",
    5: "St",
    6: "G",
    7: "P",
    8: "Cb",
    9: "R",
    11: "R",
    14: "Co",
    17: "Sh",
    18: "R",
}


class Sbdare(Layerable):
    def pre_tile_encode(self, feature, cx):
        text = natsur(int_values(feature.props, "NATSUR"))
        if text is not None:
            feature.props[NATURE_OF_SURFACE] = text
        if int_value(feature.props, "WATLEV") in (3, 4):
            feature.props[DASHED_OUTLINE] = True

    def layers(self, b):
        return [
            b.line_layer_with_color(Color.CHGRD, width=1.0, filter=filters.eq_type_line_string()),
            b.line_layer_with_color(
                Color.CHGRD,
                width=1.0,
                style=LineStyle.DASH_LINE,
                filter=[filters.ALL, filters.eq_type_polygon(), ["has", DASHED_OUTLINE]],
            ),
            b.text_layer(["get", NATURE_OF_SURFACE], filter=["has", NATURE_OF_SURFACE]),
        ]


def natsur(values):
    """PresLib 4.0 Part I §14.6.3 "Nature of seabed abbreviations" - space separated, "to reduce
    undue clutter ... " M S G" rather than "Mud Sand Gravel"". Lava and boulders abbreviate
    to ``R``, the same as rock, so repeats are dropped. ``None`` when nothing maps."""
    parts = []
    for v in values:
        abbreviation = _NATSUR_ABBREVIATIONS.get(v)
        if abbreviation is not None and abbreviation not in parts:
            parts.append(abbreviation)
    return " ".join(parts) if parts else None
