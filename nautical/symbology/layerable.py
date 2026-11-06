"""The ``Layerable`` contract and its layer helpers.

A :class:`Layerable` is one rule per S-57 object class that (a) adds symbology props to a feature
before it is tiled (:meth:`Layerable.pre_tile_encode`) and (b) contributes the MapLibre layers
that draw those props (:meth:`Layerable.layers`). The key and source layer it is registered
under live in the factory entry, so one class can be registered twice.

The :class:`LayerBuilder` helpers take their required arguments positionally and the optional
ones as keyword arguments, so a centred point symbol reads
``b.point_layer_from_symbol(anchor=Anchor.CENTER)``. Layers are plain dicts in MapLibre's wire
form; :func:`layout` and :func:`paint` build their property blocks from snake_case names.
"""

from dataclasses import dataclass

from . import filters
from .brushes import IconRot, Label, LineStyle, Offset, Symbol
from .colors import Color, ColorLibrary, Depth, Theme

SOURCE = "src_senc"


class Anchor:
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_RIGHT = "bottom-right"
    BOTTOM = "bottom"
    TOP = "top"
    TOP_LEFT = "top-left"
    TOP_RIGHT = "top-right"


class IconRotationAlignment:
    MAP = "map"
    VIEWPORT = "viewport"
    AUTO = "auto"


class IconTextFit:
    NONE = "none"
    WIDTH = "width"
    HEIGHT = "height"
    BOTH = "both"


class LineCap:
    BUTT = "butt"
    ROUND = "round"
    SQUARE = "square"


class LineJoin:
    BEVEL = "bevel"
    ROUND = "round"
    MITER = "miter"


class Placement:
    POINT = "point"
    LINE = "line"
    LINE_CENTER = "line-center"


class TextJustify:
    AUTO = "auto"
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class Font:
    ROBOTO_BOLD = "Roboto Bold"
    ROBOTO_ITALIC = "Roboto Italic"
    ROBOTO_MEDIUM = "Roboto Medium"
    ROBOTO_REGULAR = "Roboto Regular"


class LayerType:
    BACKGROUND = "background"
    FILL = "fill"
    LINE = "line"
    SYMBOL = "symbol"
    CIRCLE = "circle"


_PAINT_KEYS = {
    "text_color": "text-color",
    "text_halo_color": "text-halo-color",
    "text_halo_width": "text-halo-width",
    "background_color": "background-color",
    "background_opacity": "background-opacity",
    "fill_color": "fill-color",
    "fill_opacity": "fill-opacity",
    "fill_pattern": "fill-pattern",
    "line_color": "line-color",
    "line_width": "line-width",
    "line_dash_array": "line-dasharray",
    "line_pattern": "line-pattern",
    "circle_opacity": "circle-opacity",
    "circle_color": "circle-color",
    "circle_stroke_color": "circle-stroke-color",
    "circle_radius": "circle-radius",
    "circle_stroke_width": "circle-stroke-width",
}

_LAYOUT_KEYS = {
    "icon_image": "icon-image",
    "icon_anchor": "icon-anchor",
    "icon_text_fit": "icon-text-fit",
    "icon_text_fit_padding": "icon-text-fit-padding",
    "icon_allow_overlap": "icon-allow-overlap",
    "icon_ignore_placement": "icon-ignore-placement",
    "icon_keep_upright": "icon-keep-upright",
    "icon_rotate": "icon-rotate",
    "icon_size": "icon-size",
    "symbol_spacing": "symbol-spacing",
    "icon_rotation_alignment": "icon-rotation-alignment",
    "text_font": "text-font",
    "text_anchor": "text-anchor",
    "text_justify": "text-justify",
    "text_field": "text-field",
    "text_offset": "text-offset",
    "text_optional": "text-optional",
    "line_join": "line-join",
    "line_cap": "line-cap",
    "icon_offset": "icon-offset",
    "text_allow_overlap": "text-allow-overlap",
    "text_ignore_placement": "text-ignore-placement",
    "text_max_width": "text-max-width",
    "text_size": "text-size",
    "text_padding": "text-padding",
    "symbol_placement": "symbol-placement",
    "symbol_sort_key": "symbol-sort-key",
}


def _block(keys, kw):
    unknown = set(kw) - set(keys)
    if unknown:
        raise TypeError(f"unknown style properties: {sorted(unknown)}")
    return {keys[k]: v for k, v in kw.items() if v is not None}


def paint(**kw):
    return _block(_PAINT_KEYS, kw)


def layout(**kw):
    return _block(_LAYOUT_KEYS, kw)


@dataclass(frozen=True)
class SymbologyConfig:
    """Depth thresholds in metres (``shallowDepth`` / ``safetyDepth`` / ``deepDepth``)."""

    shallow_depth: float = 3.0
    safety_depth: float = 6.0
    deep_depth: float = 9.0
    debug_tile: bool = False


@dataclass(frozen=True)
class Context:
    """What every rule may read: the depth thresholds and the colour library."""

    config: SymbologyConfig
    colors: ColorLibrary


class Layerable:
    """The symbology rule for one S-57 object class."""

    #: The vector tile layer the style layers read, when it is not the registration key.
    source_layer = None

    def layers(self, b):
        """The style layers, in draw order."""
        raise NotImplementedError

    def pre_tile_encode(self, feature, cx):
        """Adds the symbology props (``SY``, ``AC``, ``LC``, ``AP``, ``LP``, ...) the layers read."""


class LayerBuilder:
    """Builds the layers of one layerable for one style request.

    Helper-made layer ids are numbered by a counter that starts at 1 for every builder
    (``DEPARE_fill_1``, ``DEPARE_fill_2``, ...).
    """

    def __init__(self, cx, key, source_layer, depth, theme, source=SOURCE):
        self.cx = cx
        self.key = key
        self.source_layer = source_layer
        self.depth = depth
        self.theme = theme
        self.source = source
        self._next_id = 0

    @property
    def config(self):
        return self.cx.config

    def next_id(self):
        self._next_id += 1
        return self._next_id

    def color(self, color):
        return self.cx.colors.color_from(color, self.theme)

    def area_fill_color(self, options):
        return filters.area_fill_color(self.cx.colors, options, self.theme)

    def line_color(self, options):
        return filters.line_color(self.cx.colors, options, self.theme)

    def layer(self, id_, kind, **members):
        """A layer of ``kind`` on the chart source and this layerable's source layer."""
        layer = {"id": id_, "type": kind, "source": self.source, "source-layer": self.source_layer}
        for key, value in members.items():
            if value is not None:
                layer[key.replace("_", "-")] = value
        return layer

    def _helper_id(self, infix):
        return f"{self.key}_{infix}{self.next_id()}"

    def label_paint(self, text, halo):
        """The SNDG2 text on a DEPDW halo that most labels use."""
        return paint(text_color=self.color(text), text_halo_color=self.color(halo), text_halo_width=2.5)

    def point_layer_from_symbol(
        self,
        symbol=Symbol.prop(),
        anchor=Anchor.BOTTOM,
        icon_offset=None,
        icon_allow_overlap=True,
        icon_rotate=None,
        icon_rotation_alignment=None,
        filter=None,
    ):
        """A point symbol on point features (``<key>_point_<n>``)."""
        return self.layer(
            self._helper_id("point_"),
            LayerType.SYMBOL,
            filter=filter if filter is not None else [filters.ANY, filters.eq_type_point()],
            layout=layout(
                symbol_placement=Placement.POINT,
                icon_image=symbol.property(),
                icon_anchor=anchor,
                icon_offset=icon_offset.property() if icon_offset else None,
                icon_allow_overlap=icon_allow_overlap,
                icon_rotate=icon_rotate.property() if icon_rotate else None,
                icon_rotation_alignment=icon_rotation_alignment,
            ),
        )

    def point_layer_with_label(
        self,
        label,
        label_color=Color.SNDG2,
        highlight_color=Color.DEPDW,
        text_anchor=None,
        text_justify=TextJustify.CENTER,
        text_offset=None,
    ):
        """A text label on point features (``<key>_label_<n>``)."""
        return self.layer(
            self._helper_id("label_"),
            LayerType.SYMBOL,
            filter=filters.eq_type_point(),
            layout=layout(
                text_font=[Font.ROBOTO_BOLD],
                text_anchor=text_anchor,
                text_justify=text_justify,
                text_field=label.property(),
                text_size=14.0,
                text_offset=text_offset.property() if text_offset else None,
                symbol_placement=Placement.POINT,
            ),
            paint=self.label_paint(label_color, highlight_color),
        )

    def line_layer_with_color(self, color, style=LineStyle.SOLID, layout_=None, width=2.0, filter=None):
        """A line in one fixed colour (``<key>_line_<n>``)."""
        return self.layer(
            self._helper_id("line_"),
            LayerType.LINE,
            filter=filter if filter is not None else filters.eq_type_line_string_or_polygon(),
            layout=layout_,
            paint=paint(line_color=self.color(color), line_width=width, line_dash_array=style.line_dash_array()),
        )

    def line_layer_with_colors(self, options, style=LineStyle.SOLID, width=2.0, filter=None):
        """A line whose colour comes from the ``LC`` prop, one of ``options`` (``<key>_line_<n>``)."""
        return self.layer(
            self._helper_id("line_"),
            LayerType.LINE,
            filter=filter if filter is not None else filters.eq_type_line_string_or_polygon(),
            layout=layout(line_join=LineJoin.ROUND, line_cap=LineCap.ROUND),
            paint=paint(line_color=self.line_color(options), line_width=width, line_dash_array=style.line_dash_array()),
        )

    def line_layer_with_label(self, label, label_color=Color.SNDG2, highlight_color=Color.DEPDW):
        """A text label along line features (``<key>_label_<n>``)."""
        return self.layer(
            self._helper_id("label_"),
            LayerType.SYMBOL,
            filter=filters.eq_type_line_string_or_polygon(),
            layout=layout(
                text_font=[Font.ROBOTO_BOLD],
                text_justify=TextJustify.CENTER,
                text_field=label.property(),
                text_size=14.0,
                symbol_placement=Placement.LINE,
            ),
            paint=self.label_paint(label_color, highlight_color),
        )

    def line_layer_with_pattern(
        self,
        symbol=None,
        include_polygon_lines=True,
        symbol_placement=Placement.LINE,
        icon_rotation_alignment=None,
        icon_allow_overlap=None,
    ):
        """A symbol repeated along lines, and optionally polygon outlines (``<key>_line_symbol_<n>``)."""
        return self.layer(
            self._helper_id("line_symbol_"),
            LayerType.SYMBOL,
            filter=filters.eq_type_line_string_or_polygon() if include_polygon_lines else filters.eq_type_line_string(),
            layout=layout(
                symbol_placement=symbol_placement,
                icon_image=_sprite_or_prop(symbol, "LP"),
                icon_anchor=Anchor.CENTER,
                icon_rotation_alignment=icon_rotation_alignment,
                icon_keep_upright=False,
                icon_allow_overlap=icon_allow_overlap,
            ),
        )

    def line_layer_with_spaced_pattern(self, allow_overlap, symbol=None, icon_rotate=None, icon_size=None, spacing=None):
        """A map-aligned symbol repeated along lines and polygon outlines at a given size and
        spacing (``<key>_line_symbol_<n>``)."""
        return self.layer(
            self._helper_id("line_symbol_"),
            LayerType.SYMBOL,
            filter=filters.eq_type_line_string_or_polygon(),
            layout=layout(
                symbol_placement=Placement.LINE,
                icon_image=_sprite_or_prop(symbol, "LP"),
                icon_rotate=icon_rotate,
                icon_rotation_alignment=IconRotationAlignment.MAP,
                icon_allow_overlap=allow_overlap,
                icon_size=icon_size,
                symbol_spacing=spacing,
            ),
        )

    def line_layer_with_text(self, text_key):
        """The ``text_key`` prop as text along line features (``<key>_line_label<n>``)."""
        return self.layer(
            self._helper_id("line_label"),
            LayerType.SYMBOL,
            filter=filters.eq_type_line_string(),
            layout=layout(
                text_font=[Font.ROBOTO_BOLD],
                text_justify=TextJustify.CENTER,
                text_field=["get", text_key],
                text_size=14.0,
                symbol_placement=Placement.LINE,
            ),
            paint=self.label_paint(Color.SNDG2, Color.DEPDW),
        )

    def area_layer_with_fill_colors(self, options):
        """A polygon fill whose colour comes from the ``AC`` prop, one of ``options`` (``<key>_fill_<n>``)."""
        return self.layer(
            self._helper_id("fill_"),
            LayerType.FILL,
            filter=filters.eq_type_polygon(),
            paint=paint(fill_color=self.area_fill_color(options)),
        )

    def area_layer_with_fill_color(self, color, opacity=None):
        """A polygon fill in one fixed colour, optionally translucent (``<key>_fill_<n>``)."""
        return self.layer(
            self._helper_id("fill_"),
            LayerType.FILL,
            filter=filters.eq_type_polygon(),
            paint=paint(fill_color=self.color(color), fill_opacity=opacity),
        )

    def area_layer_with_fill_pattern(self, symbol=None):
        """A polygon fill pattern: the sprite, or the ``AP`` prop (``<key>_fill_pattern_<n>``)."""
        return self.layer(
            self._helper_id("fill_pattern_"),
            LayerType.FILL,
            filter=filters.eq_type_polygon(),
            paint=paint(fill_pattern=_sprite_or_prop(symbol, "AP")),
        )

    def area_layer_with_single_symbol(
        self, symbol=None, icon_offset=None, anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP
    ):
        """One symbol per polygon (``<key>_area_symbol<n>``)."""
        return self.layer(
            self._helper_id("area_symbol"),
            LayerType.SYMBOL,
            filter=filters.eq_type_polygon(),
            layout=layout(
                symbol_placement=Placement.POINT,
                icon_image=_sprite_or_prop(symbol, "SY"),
                icon_offset=icon_offset,
                icon_anchor=anchor,
                icon_rotation_alignment=icon_rotation_alignment,
            ),
        )

    def area_layer_with_point_symbol(
        self,
        symbol=None,
        anchor=Anchor.CENTER,
        icon_rotate=None,
        icon_rotation_alignment=None,
        icon_allow_overlap=True,
        icon_offset=None,
    ):
        """A polygon's point symbol, unless the feature set ``EA`` (``<key>_area_point<n>``)."""
        return self.layer(
            self._helper_id("area_point"),
            LayerType.SYMBOL,
            filter=[filters.ALL, filters.eq_type_polygon(), ["!=", "EA", True]],
            layout=layout(
                symbol_placement=Placement.POINT,
                icon_image=_sprite_or_prop(symbol, "SY"),
                icon_anchor=anchor,
                icon_rotate=icon_rotate.property() if icon_rotate else None,
                icon_rotation_alignment=icon_rotation_alignment,
                icon_allow_overlap=icon_allow_overlap,
                icon_keep_upright=False,
                icon_offset=icon_offset,
            ),
        )

    def text_layer(
        self, text_field, text_anchor=Anchor.CENTER, text_justify=TextJustify.CENTER, text_offset=None, filter=None
    ):
        """S-52 ``TX``/``TE`` text, point placed, so a point, line or area each get one upright
        label (``<key>_text_<n>``). Unfiltered by geometry type unless ``filter`` is given."""
        return self.layer(
            self._helper_id("text_"),
            LayerType.SYMBOL,
            filter=filter,
            layout=layout(
                text_font=[Font.ROBOTO_BOLD],
                text_anchor=text_anchor,
                text_justify=text_justify,
                text_field=text_field,
                text_offset=text_offset.property() if text_offset else None,
                text_size=14.0,
                symbol_placement=Placement.POINT,
            ),
            paint=self.label_paint(Color.SNDG2, Color.DEPDW),
        )

    def area_layer_with_text(
        self,
        label,
        text_color=Color.CHBLK,
        halo_color=Color.CHWHT,
        text_justify=TextJustify.CENTER,
        text_offset=None,
        text_optional=None,
    ):
        """A text label on points and polygons (``<key>_area_label<n>``)."""
        return self.layer(
            self._helper_id("area_label"),
            LayerType.SYMBOL,
            filter=filters.eq_type_point_or_polygon(),
            layout=layout(
                text_font=[Font.ROBOTO_BOLD],
                text_justify=text_justify,
                text_field=label.property(),
                text_size=14.0,
                text_offset=text_offset.property() if text_offset else None,
                text_optional=text_optional,
            ),
            paint=self.label_paint(text_color, halo_color),
        )


def _sprite_or_prop(symbol, prop):
    """The sprite's name, or a ``["get", prop]`` expression when there is none."""
    return symbol if symbol is not None else ["get", prop]


__all__ = [
    "Anchor",
    "Color",
    "Context",
    "Depth",
    "Font",
    "IconRot",
    "IconRotationAlignment",
    "IconTextFit",
    "Label",
    "LayerBuilder",
    "LayerType",
    "Layerable",
    "LineCap",
    "LineJoin",
    "LineStyle",
    "Offset",
    "Placement",
    "Symbol",
    "SymbologyConfig",
    "TextJustify",
    "Theme",
    "layout",
    "paint",
]
