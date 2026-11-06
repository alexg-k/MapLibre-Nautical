"""S-52 text group 21, "names for position reporting": ``TE('by %s','OBJNAM',...)`` on buoys,
``TE('bn %s','OBJNAM',...)`` on beacons and daymarks, ``LtV``, ``Prod`` and ``Plt`` on light
vessels, offshore platforms and pilot boarding places, and a plain ``TX(OBJNAM)`` /
``TX(INFORM)`` on bridges and distance marks.

Registered once per class under the key ``<CLASS>_NAME``, after every mark symbol. The text is
composed by a style expression off the raw attribute, so nothing is added to the tile, and the
layer is unfiltered by geometry type and point placed.
"""

from enum import Enum

from .prelude import *


class NamePlacement(Enum):
    """The presentation library's ``TE``/``TX`` justification and offset, in text body units
    (positive y is down); one body is taken as 1.2 em."""

    UPPER_LEFT = (Anchor.BOTTOM_RIGHT, TextJustify.RIGHT, (-1.2, -1.2))
    UPPER_RIGHT = (Anchor.BOTTOM_LEFT, TextJustify.LEFT, (1.2, -1.2))
    # BRIDGE's TX(OBJNAM) is the same spot as its clearance text, so the name goes left instead.
    LEFT = (Anchor.RIGHT, TextJustify.RIGHT, (-1.2, 0.0))
    DISTANCE_MARK = (Anchor.BOTTOM_RIGHT, TextJustify.RIGHT, (2.4, 0.0))

    def layout(self):
        anchor, justify, (x, y) = self.value
        return anchor, justify, Offset.coord(x, y)


class NameLabel(Layerable):
    def __init__(self, object_class, prefix, placement, attribute="OBJNAM"):
        self.object_class = object_class
        self.prefix = prefix
        self.placement = placement
        self.attribute = attribute

    @property
    def key(self):
        return f"{self.object_class}_NAME"

    @property
    def source_layer(self):
        return self.object_class

    @staticmethod
    def all():
        labels = []
        for cls in ["BOYCAR", "BOYINB", "BOYISD", "BOYLAT", "BOYSAW", "BOYSPP", "LITFLT"]:
            labels.append(NameLabel(cls, "by", NamePlacement.UPPER_LEFT))
        for cls in ["BCNCAR", "BCNISD", "BCNLAT", "BCNSAW", "BCNSPP", "DAYMAR"]:
            labels.append(NameLabel(cls, "bn", NamePlacement.UPPER_LEFT))
        labels.append(NameLabel("LITVES", "LtV", NamePlacement.UPPER_LEFT))
        labels.append(NameLabel("OFSPLF", "Prod", NamePlacement.UPPER_RIGHT))
        labels.append(NameLabel("PILBOP", "Plt", NamePlacement.UPPER_RIGHT))
        labels.append(NameLabel("BRIDGE", None, NamePlacement.LEFT))
        labels.append(NameLabel("DISMAR", None, NamePlacement.DISTANCE_MARK, attribute="INFORM"))
        return labels

    def text(self):
        if self.prefix is None:
            return ["get", self.attribute]
        return [
            "case",
            ["has", self.attribute],
            ["concat", f"{self.prefix} ", ["to-string", ["get", self.attribute]]],
            "",
        ]

    def layers(self, b):
        anchor, justify, offset = self.placement.layout()
        return [
            b.layer(
                b.key,
                LayerType.SYMBOL,
                layout=layout(
                    text_font=[Font.ROBOTO_BOLD],
                    text_anchor=anchor,
                    text_justify=justify,
                    text_field=self.text(),
                    text_offset=offset.property(),
                    text_size=14.0,
                    symbol_placement=Placement.POINT,
                ),
                paint=b.label_paint(Color.SNDG2, Color.DEPDW),
            )
        ]
