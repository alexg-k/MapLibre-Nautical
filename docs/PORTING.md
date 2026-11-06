# Porting njord symbology rules to Python

`nautical/symbology` is a port of njord's `crates/njord-symbology` (Rust). Every S-57 object
class has one module under `nautical/symbology/layers/` that mirrors the Rust file of the same
name, so the two stay diffable. This document is the recipe for porting (or re-syncing) a module.

## Layout of a layer module

```python
"""<Object name> (<ACRONYM>, code <n>). Geometry: <primitives>."""

from .prelude import *            # attributes, Color, filters, LayerBuilder helpers, props, ...


class Resare(Layerable):           # class name = Rust struct name
    def pre_tile_encode(self, feature, cx):     # omit when the Rust impl has none
        ...
    def layers(self, b):
        return [ ... ]
```

The registry (`nautical/symbology/factory.py`) imports `layers.<key.lower()>.<Key.capitalize()>`
unless an entry says otherwise, so `RESARE` → `resare.Resare`.

## Rust → Python mapping

| Rust | Python |
|---|---|
| `feature.props` (`JsonObject`) | `feature.props` (`dict`, insertion ordered) |
| `int_value(&feature.props, "X")` / `float_value` / `double_value` / `string_value` / `int_values` / `string_values` | same names, `(feature.props, "X")` |
| `Catlam::of(&feature.props)` → `Option<Catlam>` | `Catlam.of(feature.props)` → member or `None` |
| list attribute `Restrn::of(&props)` → `Vec` | `Restrn.of(props)` → `list` |
| `Colour::first(&props)` | `Colour.first(props)` |
| `matches!(x, A \| B)` | `x in (A, B)` |
| `feature.point_symbol(Sprite::BOYLAT14)` | `feature.point_symbol("BOYLAT14")` (sprites are plain strings) |
| `feature.area_color(Color::DEPVS)` | `feature.area_color(Color.DEPVS)` |
| `feature.props.insert("K".into(), v.into())` | `feature.props["K"] = v` |
| `cx.config.shallow_depth` | `cx.config.shallow_depth` |
| `add_sounding_conversions(&mut feature.props, m as f64)` | `add_sounding_conversions(feature.props, float(m))` |
| `double_to_string(x)` | `double_to_string(x)` |
| `bearing_label(feature)` / `bearing_label_layer(b)` | `from .bearing import bearing_label, bearing_label_layer` |
| `soundg::text_layers(b)` | `from . import soundg; soundg.text_layers(b)` |
| `opening_bridge(feature)` | `from .clearance_label import opening_bridge` |

### LayerBuilder helpers

The `…Opts` structs become keyword arguments with the same names and defaults:

| Rust | Python |
|---|---|
| `b.point_layer_from_symbol(PointSymbolOpts { anchor: Anchor::Center, icon_rotation_alignment: Some(IconRotationAlignment::Map), ..Default::default() })` | `b.point_layer_from_symbol(anchor=Anchor.CENTER, icon_rotation_alignment=IconRotationAlignment.MAP)` |
| `symbol: Symbol::Sprite(Sprite::X)` / `Symbol::Property(Some(2))` | `symbol=Symbol.of("X")` / `symbol=Symbol.prop(2)` |
| `icon_rotate: Some(IconRot::Degrees(135.0))` / `IconRot::Property("ORIENT".into())` | `icon_rotate=IconRot(degrees=135.0)` / `IconRot(prop="ORIENT")` |
| `icon_offset: Some(Offset::Coord(0.0, -8.0))` | `icon_offset=Offset.coord(0.0, -8.0)` |
| `Offset::EvalEq { key, value, eq, neq }` | `Offset.eval_eq(key, value, eq=(..), neq=(..))` |
| `b.line_layer_with_color(Color::X, LineColorOpts { width: 0.5, style: LineStyle::DashLine, ..Default::default() })` | `b.line_layer_with_color(Color.X, width=0.5, style=LineStyle.DASH_LINE)` |
| `LineStyle::CustomDash(3.0, 2.0)` | `LineStyle.custom_dash(3.0, 2.0)` |
| `LineColorOpts { layout: Some(Layout {..}) }` | `layout_=layout(...)` (note the trailing underscore) |
| `b.line_layer_with_colors(&[Color::A, Color::B], LineColorsOpts {..})` | `b.line_layer_with_colors([Color.A, Color.B], ...)` |
| `b.line_layer_with_pattern(LinePatternOpts { symbol: Some(Sprite::X), .. })` | `b.line_layer_with_pattern(symbol="X", ...)` |
| `b.line_layer_with_spaced_pattern(true, SpacedLinePatternOpts { icon_rotate: Some(90.0), icon_size: Some(0.5), spacing: Some(40.0), .. })` | `b.line_layer_with_spaced_pattern(True, icon_rotate=90.0, icon_size=0.5, spacing=40.0)` |
| `b.area_layer_with_fill_colors(&[..])` | `b.area_layer_with_fill_colors([..])` |
| `b.area_layer_with_fill_color(Color::X, Some(0.5))` | `b.area_layer_with_fill_color(Color.X, 0.5)` |
| `b.area_layer_with_fill_pattern(Some(Sprite::X))` / `(None)` | `b.area_layer_with_fill_pattern("X")` / `()` |
| `b.area_layer_with_single_symbol(AreaSingleSymbolOpts { icon_offset: Some(vec![0.0, 1.0]), .. })` | `b.area_layer_with_single_symbol(icon_offset=[0.0, 1.0])` |
| `b.area_layer_with_point_symbol(AreaPointSymbolOpts {..})` | `b.area_layer_with_point_symbol(...)` |
| `b.area_layer_with_text(&Label::Property("OBJNAM".into()), AreaTextOpts {..})` | `b.area_layer_with_text(Label(prop="OBJNAM"), ...)` |
| `Label::Text("x".into())` | `Label(text="x")` |
| `b.text_layer(json!([...]), TextLayerOpts {..})` | `b.text_layer([...], ...)` |
| `b.line_layer_with_text("KEY")` / `b.line_layer_with_label(&label, LineLabelOpts {..})` / `b.point_layer_with_label(&label, PointLabelOpts {..})` | same names, keyword opts |
| `b.color(Color::X)` / `b.color_json(Color::X)` | `b.color(Color.X)` |
| `b.key`, `b.depth`, `b.theme`, `b.config()` | `b.key`, `b.depth`, `b.theme`, `b.config` |

Hand-built layers (`Layer { filter: Some(..), layout: Some(Layout {..}), paint: Some(Paint {..}), min_zoom: Some(0), max_zoom_exclusive: Some(10), ..b.layer("ID", LayerType::Symbol) }`) become

```python
b.layer("ID", LayerType.SYMBOL, filter=[...], layout=layout(icon_image=..., ...), paint=paint(...), minzoom=0, maxzoom=10)
```

`layout(...)` / `paint(...)` take the Rust field names in snake_case (`icon_allow_overlap`,
`text_halo_width`, `line_dash_array`, ...) and drop `None` values. `json!([...])` is a plain Python
list; `filters::eq_type_point()` etc. are `filters.eq_type_point()`; `filters::ALL` is
`filters.ALL`. `float_json(x)` is just `x`. Rust `Value::Bool(true)` is `True`.

A struct with a configurable field (`Lndare { area_color }`, `Canals { fill_color }`) becomes a
class with an `__init__` default; `Lndare::default()` is `Lndare()`. A layerable overriding
`source_layer()` sets the class attribute `source_layer = "OBSTRN"`.

Keep the layer order and every helper call exactly as in Rust: the helper id counter
(`<KEY>_fill_1`, `<KEY>_line_2`, ...) is part of the golden output. Keep the Rust doc comments that
explain *why* (as the module docstring / short comments); drop boilerplate.

## Verifying

`tools/check_njord_port.py` replays njord's golden fixtures:

```shell
python3 tools/check_njord_port.py --njord /path/to/njord --only RESARE,CTNARE   # pre_tile_encode + style layers of these keys
python3 tools/check_njord_port.py --njord /path/to/njord                       # everything, including full style documents
```

`--only` keys are registry keys (`OBSTRNAREA`, `BRIDGE_CLEARANCE`, `lokbsn`, ...). A module is done
when its keys report `0 failures`.
