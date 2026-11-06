"""Sounding (SOUNDG, code 129). Geometry: Point.

Drying heights (S-52 PresLib SNDFRM04): the depth parts in the tile are negative, so every text
field renders ``abs`` of its part, the shallow colour applies, and the layers that draw the whole
number carry the SOUNDSA1 underline, fitted to the digits with icon-text-fit.

The text layers are module functions because ``obstrn`` reuses them.
"""

from .prelude import *

TEXT_SIZE = 16.0


class Soundg(Layerable):
    def pre_tile_encode(self, feature, cx):
        meters = double_value(feature.props, "METERS")
        if meters is not None:
            add_sounding_conversions(feature.props, meters)

    def layers(self, b):
        return text_layers(b)


def text_layers(b):
    """The depth text layers for the builder's depth unit."""
    key = b.key
    if b.depth == Depth.FATHOMS:
        return [
            _single_text(b, f"{key}_fathoms", "FATHOMS", "FATHOMS_FT"),
            _primary_text_layer(b, f"{key}_fathoms_offset", "FATHOMS", "FATHOMS_FT"),
            _sub_text_layer(b, f"{key}_fathoms_feet_offset", "FATHOMS_FT"),
        ]
    if b.depth == Depth.METERS:
        return [
            _single_text(b, f"{key}_meters", "METERS_W", "METERS_T"),
            _primary_text_layer(b, f"{key}_meters_offset", "METERS_W", "METERS_T"),
            _sub_text_layer(b, f"{key}_meters_tenths_offset", "METERS_T"),
        ]
    return [_single_text(b, f"{key}_feet", "FEET", None)]


def _sort_key_by_depth():
    # Ascending METERS gives shallower (more safety-critical) soundings priority on collisions.
    return ["get", "METERS"]


def _abs_text(key):
    return ["to-string", ["abs", ["get", key]]]


def _drying_underline(layout_):
    """S-52 SOUNDSA1, the drying-height underline, only for negative soundings. The icon takes no
    part in collision detection, so the symbol places on its text alone."""
    return {
        **layout_,
        **layout(
            icon_image=["case", ["<", ["get", "METERS"], 0], "SOUNDSA1", ""],
            icon_text_fit=IconTextFit.BOTH,
            icon_text_fit_padding=[0.0, 0.0, 3.0, 0.0],
            icon_allow_overlap=True,
            icon_ignore_placement=True,
        ),
    }


def _paint(b):
    return paint(text_color=_text_color(b), text_halo_color=b.color(Color.DEPDW), text_halo_width=2.5)


def _deep_depth(b):
    return b.config.deep_depth


def _single_text(b, id_, text_key, sub_text_key):
    if sub_text_key is not None:
        filter_ = [
            filters.ALL,
            filters.eq_type_point(),
            [filters.ANY, [">=", "METERS", _deep_depth(b)], ["==", sub_text_key, 0]],
        ]
    else:
        filter_ = filters.eq_type_point()
    return b.layer(
        id_,
        LayerType.SYMBOL,
        filter=filter_,
        layout=_drying_underline(
            layout(
                text_font=[Font.ROBOTO_BOLD],
                text_anchor=Anchor.CENTER,
                text_justify=TextJustify.CENTER,
                text_field=_abs_text(text_key),
                text_allow_overlap=False,
                text_ignore_placement=False,
                text_size=TEXT_SIZE,
                symbol_placement=Placement.POINT,
                symbol_sort_key=_sort_key_by_depth(),
            )
        ),
        paint=_paint(b),
    )


def _primary_text_layer(b, id_, text_key, sub_text_key):
    """Whole-number depth, anchored so it sits up-and-left of the feature point; paired with
    the sub text layer whose top-left anchor sits just right of the same point."""
    return b.layer(
        id_,
        LayerType.SYMBOL,
        filter=[filters.ALL, filters.eq_type_point(), ["!=", sub_text_key, 0], ["<", "METERS", _deep_depth(b)]],
        layout=_drying_underline(
            layout(
                text_font=[Font.ROBOTO_BOLD],
                text_anchor=Anchor.BOTTOM_RIGHT,
                text_offset=[0.0, 0.6],
                text_justify=TextJustify.CENTER,
                text_field=_abs_text(text_key),
                text_allow_overlap=False,
                text_ignore_placement=False,
                text_size=TEXT_SIZE,
                text_padding=0.0,
                symbol_placement=Placement.POINT,
                symbol_sort_key=_sort_key_by_depth(),
            )
        ),
        paint=_paint(b),
    )


def _sub_text_layer(b, id_, text_key):
    return b.layer(
        id_,
        LayerType.SYMBOL,
        filter=[filters.ALL, filters.eq_type_point(), ["!=", text_key, 0], ["<", "METERS", _deep_depth(b)]],
        layout=layout(
            text_font=[Font.ROBOTO_BOLD],
            text_anchor=Anchor.TOP_LEFT,
            text_offset=[0.1, 0.0],
            text_justify=TextJustify.CENTER,
            text_field=_abs_text(text_key),
            text_allow_overlap=False,
            text_ignore_placement=False,
            text_size=TEXT_SIZE - 4.0,
            text_padding=0.0,
            symbol_placement=Placement.POINT,
            symbol_sort_key=_sort_key_by_depth(),
        ),
        paint=_paint(b),
    )


def _text_color(b):
    return ["case", ["<=", ["get", "METERS"], _deep_depth(b)], b.color(Color.SNDG2), b.color(Color.SNDG1)]
