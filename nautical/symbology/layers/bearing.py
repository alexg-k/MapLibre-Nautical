"""The bearing label shared by NAVLNE, RADLNE, RECTRC, RCRTCL and DWRTCL: the S-52 lookups'
``TE('%03.0lf deg','ORIENT',...)``.

Pre-rendered into the tile rather than composed by a style expression because the style spec has
no zero-padding.
"""

import math

from .prelude import *

#: The feature prop carrying the bearing text.
BEARING = "_BRG"


def bearing_label(feature):
    """``_BRG`` from ORIENT, when present."""
    orient = double_value(feature.props, "ORIENT")
    if orient is not None:
        feature.props[BEARING] = format_bearing(orient)


def format_bearing(orient):
    """``%03.0lf deg``: whole degrees (rounded half up), zero padded to three digits."""
    whole = int(math.floor(orient + 0.5))
    return f"{str(whole):0>3} deg"


def bearing_label_layer(b):
    return b.line_layer_with_label(Label(prop=BEARING), label_color=Color.CHBLK, highlight_color=Color.CHWHT)
