"""Beacon, special purpose/general (BCNSPP, code 9). Geometry: Point."""

from .bcnlat import bcnshp
from .prelude import *

_SPECIAL = {
    Catspm.NOTICE_MARK: "NOTBRD11",
    Catspm.REFUGE_BEACON: "BCNSPP13",
    Catspm.MARK_WITH_UNKNOWN_PURPOSE: "BCNDEF13",
}


class Bcnspp(Layerable):
    def pre_tile_encode(self, feature, cx):
        """The first CATSPM with a symbol of its own wins, else the BCNSHP symbol (``Bcnlat``)."""
        special = next((_SPECIAL[c] for c in Catspm.of(feature.props) if c in _SPECIAL), None)
        if special is not None:
            feature.point_symbol(special)
        else:
            bcnshp(feature)

    def layers(self, b):
        return [b.point_layer_from_symbol()]
