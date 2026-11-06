"""Tunnel (TUNNEL, code 151). Geometry: Point, Line, Area.

Attributes: BURDEP, CONDTN, HORACC, HORCLR, NOBJNM, OBJNAM, STATUS, VERACC, VERCLR
"""

from .prelude import *

AREA_FILL_COLORS = [Color.DEPVS]
LINE_COLORS = [Color.CHBLK, Color.CHGRD]


class Tunnel(Layerable):
    def pre_tile_encode(self, feature, cx):
        if float_value(feature.props, "BURDEP") is not None:
            feature.area_color(Color.DEPVS)
            feature.line_color(Color.CHBLK)
        else:
            feature.line_color(Color.CHGRD)
        name = string_value(feature.props, "NOBJNM")
        if name is None:
            name = string_value(feature.props, "OBJNAM")
        if name is not None:
            feature.props["_name"] = name

    def layers(self, b):
        label = Label(prop="_name")
        return [
            b.area_layer_with_fill_colors(AREA_FILL_COLORS),
            b.line_layer_with_colors(LINE_COLORS, style=LineStyle.DASH_LINE, width=1.0),
            b.area_layer_with_text(label, text_color=Color.CHBLK, halo_color=Color.CHWHT),
            b.line_layer_with_label(label, label_color=Color.CHBLK, highlight_color=Color.CHWHT),
            b.point_layer_with_label(label, label_color=Color.CHBLK, highlight_color=Color.CHWHT),
        ]
