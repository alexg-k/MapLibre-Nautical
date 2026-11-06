"""Buoy, special purpose/general (BOYSPP, code 19). Geometry: Point."""

from .boylat import boyshp
from .prelude import *

_SPECIAL = {
    Catspm.LANBY_LARGE_AUTOMATIC_NAVIGATIONAL_BUOY: "BOYSUP02",
    Catspm.MARK_WITH_UNKNOWN_PURPOSE: "BOYDEF03",
}


class Boyspp(Layerable):
    def pre_tile_encode(self, feature, cx):
        """The first CATSPM with a symbol of its own wins, else the BOYSHP symbol (``Boylat``)."""
        special = next((_SPECIAL[c] for c in Catspm.of(feature.props) if c in _SPECIAL), None)
        if special is not None:
            feature.point_symbol(special)
        else:
            boyshp(feature)

    def layers(self, b):
        return [b.point_layer_from_symbol()]
