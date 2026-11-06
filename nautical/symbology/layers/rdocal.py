"""Radio calling-in point (RDOCAL, code 104). Geometry: Point, Line."""

from .prelude import *


class Rdocal(Layerable):
    def pre_tile_encode(self, feature, cx):
        if "ORIENT" in feature.props and Trafic.of(feature.props) is not None:
            feature.point_symbol("RDOCAL02")
        else:
            feature.point_symbol("RCLDEF01")
        # S-52: TE('Nr %s','OBJNAM',...,1,-1,...) above TE('ch %s','COMCHA',...,1,1,...), both
        # left justified one text body right of the symbol.
        lines = []
        objnam = string_value(feature.props, "OBJNAM")
        if objnam is not None:
            lines.append(f"Nr {objnam}")
        comcha = string_value(feature.props, "COMCHA")
        if comcha is not None:
            lines.append(f"ch {comcha}")
        if lines:
            feature.props["_L"] = "\n".join(lines)

    def layers(self, b):
        return [
            b.point_layer_from_symbol(icon_rotate=IconRot(prop="ORIENT")),
            b.area_layer_with_point_symbol(icon_rotate=IconRot(prop="ORIENT")),
            b.line_layer_with_label(Label(prop="_L")),
            b.point_layer_with_label(
                Label(prop="_L"),
                label_color=Color.CHBLK,
                highlight_color=Color.CHWHT,
                text_anchor=Anchor.LEFT,
                text_justify=TextJustify.LEFT,
                text_offset=Offset.coord(1.2, 0.0),
            ),
        ]
