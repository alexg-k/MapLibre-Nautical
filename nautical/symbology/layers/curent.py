"""Current - non - gravitational (CURENT, code 36). Geometry: Point."""

from ..props import as_f32
from .prelude import *


class Curent(Layerable):
    def pre_tile_encode(self, feature, cx):
        if float_value(feature.props, "ORIENT") is not None:
            feature.point_symbol("CURENT01")
        else:
            feature.point_symbol("CURDEF01")

        point_label = string_value(feature.props, "OBJNAM") or ""
        current_velocity = float_value(feature.props, "CURVEL")
        if current_velocity is not None and current_velocity > 0.0:
            if point_label:
                point_label += " "
            point_label += f"{float_to_string(current_velocity)} kts (max)"
        if point_label.strip():
            feature.props["_PL"] = point_label

    def layers(self, b):
        return [
            b.point_layer_from_symbol(icon_rotate=IconRot(prop="ORIENT")),
            b.point_layer_with_label(
                Label(prop="INFORM"),
                text_justify=TextJustify.LEFT,
                text_anchor=Anchor.BOTTOM_LEFT,
                text_offset=Offset.coord(2.0, 0.0),
            ),
            b.point_layer_with_label(
                Label(prop="_PL"),
                text_anchor=Anchor.BOTTOM_RIGHT,
                text_justify=TextJustify.RIGHT,
                text_offset=Offset.coord(-2.0, 0.0),
            ),
        ]


def float_to_string(x):
    """The shortest ``f32`` decimal, printed by :func:`double_to_string` (``1.0``, not ``1``)."""
    for precision in range(1, 10):
        text = f"{x:.{precision}g}"
        if as_f32(float(text)) == x:
            return double_to_string(float(text))
    return double_to_string(x)
