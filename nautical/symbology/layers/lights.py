"""Light (LIGHTS, code 75). Geometry: Point."""

from ..light_description import LightDescription
from .prelude import *

#: The light description text before the height (see ``light_description``).
DESCRIPTION_HEAD = "_LDH"
#: The light description text after the height.
DESCRIPTION_TAIL = "_LDT"
FEET_PER_METER = 3.28084


class Lights(Layerable):
    def pre_tile_encode(self, feature, cx):
        """The flare by the first colour, plus ``SI``, the name of the sector icon (carrying the
        bearings and every theme's colours) for a sector light or a major light (VALNMR >= 10,
        drawn as an all-round arc)."""
        first = Colour.first(feature.props)
        if first == Colour.RED:
            feature.point_symbol("LIGHTS11")
            feature.line_color(Color.LITRD)
            light_color = Color.LITRD
        elif first == Colour.GREEN:
            feature.point_symbol("LIGHTS12")
            feature.line_color(Color.LITGN)
            light_color = Color.LITGN
        elif first in (Colour.YELLOW, Colour.WHITE, Colour.AMBER, Colour.ORANGE):
            feature.point_symbol("LIGHTS13")
            feature.line_color(Color.LITYW)
            light_color = Color.LITYW
        else:
            feature.line_color(Color.LITYW)
            feature.point_symbol("LITDEF11")
            light_color = Color.LITYW

        sectr1 = double_value(feature.props, "SECTR1")
        sectr2 = double_value(feature.props, "SECTR2")
        valnmr = double_value(feature.props, "VALNMR")
        major_light = valnmr is not None and valnmr >= 10.0

        def colors(color):
            return "_".join(
                cx.colors.color_from(color, Theme(mode)) for mode in (ThemeMode.DAY, ThemeMode.DUSK, ThemeMode.NIGHT)
            )

        radius = {Color.LITRD: 68, Color.LITGN: 74}.get(light_color, 80)

        if major_light or (sectr1 is not None and sectr2 is not None):
            s1 = double_to_string(sectr1 if sectr1 is not None else 0.0)
            s2 = double_to_string(sectr2 if sectr2 is not None else 0.0)
            feature.props["SI"] = f"sector_{s1}_{s2}_{colors(light_color)}_{colors(Color.CHBLK)}_{radius}"

        # S-52 LIGHTS05: the LITDSN text is not used for sector lights (clutter). A major light
        # drawn with an all-round arc still gets one.
        if sectr1 is None or sectr2 is None:
            d = LightDescription.of(feature.props)
            if d is not None:
                feature.props[DESCRIPTION_HEAD] = d.head
                feature.props[DESCRIPTION_TAIL] = d.tail

    def layers(self, b):
        return [
            b.point_layer_from_symbol(
                anchor=Anchor.BOTTOM,
                icon_allow_overlap=True,
                icon_rotate=IconRot(degrees=135.0),
                filter=[filters.ALL, filters.eq_type_point(), ["!has", "SI"]],
            ),
            b.layer(
                "LIGHTS_sector",
                LayerType.SYMBOL,
                filter=[filters.ALL, filters.eq_type_point(), ["has", "SI"]],
                layout=layout(
                    symbol_placement=Placement.POINT,
                    icon_image=["get", "SI"],
                    icon_anchor=Anchor.CENTER,
                    icon_allow_overlap=True,
                    icon_ignore_placement=True,
                    icon_size=1.0,
                    icon_rotation_alignment=IconRotationAlignment.MAP,
                ),
            ),
            _description(b),
        ]


def _description(b):
    """S-52 LIGHTS05 writes the description left justified, vertically centred, two text bodies
    right of the light."""
    return b.layer(
        f"{b.key}_description",
        LayerType.SYMBOL,
        filter=[filters.ALL, filters.eq_type_point(), ["has", DESCRIPTION_HEAD]],
        layout=layout(
            text_font=[Font.ROBOTO_BOLD],
            text_anchor=Anchor.LEFT,
            text_justify=TextJustify.LEFT,
            text_field=_description_text(b.depth),
            text_offset=Offset.coord(2.0, 0.0).property(),
            text_size=14.0,
            symbol_placement=Placement.POINT,
        ),
        paint=b.label_paint(Color.SNDG2, Color.DEPDW),
    )


def _description_text(depth):
    return [
        "concat",
        ["get", DESCRIPTION_HEAD],
        ["case", ["all", ["has", "HEIGHT"], [">", ["get", "HEIGHT"], 0]], _height(depth), ""],
        ["get", DESCRIPTION_TAIL],
    ]


def _height(depth):
    if depth == Depth.METERS:
        return [
            "concat",
            ["number-format", ["get", "HEIGHT"], {"locale": "en-US", "min-fraction-digits": 0, "max-fraction-digits": 1}],
            "m",
        ]
    return ["concat", ["to-string", ["round", ["*", ["get", "HEIGHT"], FEET_PER_METER]]], "ft"]
