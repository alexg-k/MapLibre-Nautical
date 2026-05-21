#!/usr/bin/python3

import json
from pathlib import Path


MIN_ZOOM = 0
MAX_ZOOM = 24
BACKGROUND_COLOR = "#d4eaee"
LINE_COLOR = "#525a5c"
STYLE_FILE = "light-style.json"
CONFIG_FILE = "config.json"

POINT = ["any", ["==", "$type", "Point"]]
POLYGON = ["any", ["==", "$type", "Polygon"]]
POLYGON_OR_LINE = [
    "any",
    ["==", "$type", "Polygon"],
    ["==", "$type", "LineString"],
]

TEXT_LAYOUT = {
    "symbol-placement": "point",
    "text-allow-overlap": True,
    "text-anchor": "center",
    "text-font": ["Roboto Bold"],
    "text-ignore-placement": True,
    "text-justify": "center",
}

BUOY_LAYERS = ["BOYCAR", "BOYINB", "BOYISD", "BOYLAT", "BOYSAW", "BOYSPP"]

# Only object classes, attributes and attribute values which are defined in the
# IHO Object Catalogue (S-57, Appendix A) may be used in an ENC. Object classes
# not represented below are not yet styled by this generator.


def main():
    output_path = Path(__file__).resolve().parent.parent / "output"
    style_file = output_path / STYLE_FILE
    config_file = output_path / CONFIG_FILE
    output_path.mkdir(exist_ok=True)

    charts = find_charts(output_path)
    write_json(style_file, build_style(charts))
    write_json(config_file, build_config())

    print(f"style generated at: {style_file}")
    print(f"config generated at: {config_file}")


def write_json(path, data):
    with path.open("w") as f:
        json.dump(data, f, indent=4)
        f.write("\n")


def find_charts(output_path):
    return {
        chart_file.stem: {"minzoom": MIN_ZOOM, "maxzoom": MAX_ZOOM}
        for chart_file in sorted(output_path.glob("*.mbtiles"))
    }


def build_style(charts):
    return {
        "version": 8,
        "name": "light",
        "sprite": "sprites/rastersymbols-day",
        "glyphs": "fonts/{fontstack}/{range}.pbf",
        "sources": build_sources(charts),
        "layers": build_layers(charts),
    }


def build_config():
    return {
        "options": {
            "paths": {
                "root": "",
                "styles": "",
                "mbtiles": "",
            }
        },
        "styles": {
            "light": {
                "style": STYLE_FILE,
            }
        },
    }


def build_sources(charts):
    return {
        chart_name: {
            "type": "vector",
            "url": f"mbtiles://{chart_name}.mbtiles",
        }
        for chart_name in charts
    }


def build_layers(charts):
    layers = [
        {
            "id": "background",
            "paint": {
                "background-color": BACKGROUND_COLOR,
                "background-opacity": 1,
            },
            "type": "background",
        }
    ]

    for chart_name, zoom in charts.items():
        layers.extend(build_chart_layers(chart_name, zoom))

    return layers


def build_chart_layers(chart_name, zoom):
    layers = [
        fill_layer("SEAARE_fill", chart_name, zoom, "SEAARE", BACKGROUND_COLOR),
        fill_layer(
            "DEPARE_fill_2",
            chart_name,
            zoom,
            "DEPARE",
            "#bad5e1",
            filter_=["all", ["==", "$type", "Polygon"], ["<=", "DRVAL1", 9.0]],
        ),
        fill_layer(
            "DEPARE_fill_1",
            chart_name,
            zoom,
            "DEPARE",
            "#73b6ef",
            filter_=["all", ["==", "$type", "Polygon"], ["<=", "DRVAL1", 3.0]],
        ),
        fill_layer(
            "DEPARE_fill_0",
            chart_name,
            zoom,
            "DEPARE",
            "#83b295",
            filter_=[
                "all",
                ["==", "$type", "Polygon"],
                ["<", "DRVAL1", 0.0],
                ["<=", "DRVAL2", 0.0],
            ],
        ),
        line_layer("DEPARE_line", chart_name, zoom, "DEPARE", LINE_COLOR, 0.5),
        line_layer("DEPCNT_line", chart_name, zoom, "DEPCNT", LINE_COLOR, 0.5),
        line_layer(
            "SLCONS_line", chart_name, zoom, "SLCONS", LINE_COLOR, 1, filter_=["all"]
        ),
        fill_layer("PONTON_fill", chart_name, zoom, "PONTON", "#b7911f"),
        line_layer(
            "PONTON_line", chart_name, zoom, "PONTON", LINE_COLOR, 1, filter_=["all"]
        ),
        fill_layer(
            "BRIDGE_fill",
            chart_name,
            zoom,
            "BRIDGE",
            "#B69D40",
            filter_=["all", ["==", "$type", "Polygon"]],
        ),
        line_layer(
            "BRIDGE_line",
            chart_name,
            zoom,
            "BRIDGE",
            LINE_COLOR,
            5,
            filter_=POLYGON_OR_LINE,
        ),
        fill_layer("HULKES_fill", chart_name, zoom, "HULKES", "#B7911F"),
        line_layer(
            "HULKES_line",
            chart_name,
            zoom,
            "HULKES",
            LINE_COLOR,
            1.5,
            filter_=POLYGON_OR_LINE,
        ),
        fill_layer("LNDARE_fill", chart_name, zoom, "LNDARE", "#c9b97a"),
        line_layer(
            "LNDARE_line",
            chart_name,
            zoom,
            "LNDARE",
            LINE_COLOR,
            2,
            filter_=POLYGON_OR_LINE,
        ),
        line_layer(
            "COALNE_line",
            chart_name,
            zoom,
            "COALNE",
            LINE_COLOR,
            2,
            filter_=POLYGON_OR_LINE,
        ),
        buaare_name_layer(chart_name, zoom),
        soundg_layer(chart_name, zoom),
        line_layer(
            "RESARE",
            chart_name,
            zoom,
            "RESARE",
            "#d631c9",
            None,
            paint={
                "line-color": "#d631c9",
                "line-opacity": 1,
                "line-dasharray": [10, 4],
            },
            filter_=None,
        ),
        fill_layer(
            "TSEZNE",
            chart_name,
            zoom,
            "TSEZNE",
            "#d631c9",
            paint={"fill-color": "#d631c9", "fill-opacity": 0.5},
            filter_=["==", "$type", "Polygon"],
        ),
    ]

    layers.extend(buoy_base_layer(layer, chart_name, zoom) for layer in BUOY_LAYERS)
    layers.extend(
        [
            boycar_topmark_layer(chart_name, zoom),
            boylat_topmark_layer(chart_name, zoom),
            lights_layer(chart_name, zoom),
        ]
    )
    return layers


def layer_base(id_prefix, chart_name, zoom, source_layer, type_, id_=None):
    return {
        "id": id_ or f"{id_prefix}_{chart_name}",
        "source": chart_name,
        "source-layer": source_layer,
        "minzoom": zoom["minzoom"],
        "maxzoom": zoom["maxzoom"],
        "type": type_,
    }


def fill_layer(
    id_prefix, chart_name, zoom, source_layer, color, paint=None, filter_=POLYGON
):
    layer = layer_base(id_prefix, chart_name, zoom, source_layer, "fill")
    if filter_ is not None:
        layer["filter"] = filter_
    layer["paint"] = paint or {"fill-color": color}
    return layer


def line_layer(
    id_prefix, chart_name, zoom, source_layer, color, width, paint=None, filter_=POLYGON
):
    layer = layer_base(id_prefix, chart_name, zoom, source_layer, "line")
    if filter_ is not None:
        layer["filter"] = filter_
    layer["paint"] = paint or {"line-color": color, "line-width": width}
    return layer


def symbol_layer(
    id_prefix,
    chart_name,
    zoom,
    source_layer,
    layout,
    paint=None,
    filter_=POINT,
    id_=None,
):
    layer = layer_base(id_prefix, chart_name, zoom, source_layer, "symbol", id_=id_)
    if filter_ is not None:
        layer["filter"] = filter_
    layer["layout"] = layout
    if paint is not None:
        layer["paint"] = paint
    return layer


def buaare_name_layer(chart_name, zoom):
    layout = {
        **TEXT_LAYOUT,
        "text-field": ["get", "OBJNAM"],
        "text-size": 9,
    }
    return symbol_layer(
        "BUAARE_name",
        chart_name,
        zoom,
        "BUAARE",
        layout,
        paint={"text-color": "#ffffff"},
        id_=f"BUAARE_name{chart_name}",
    )


def soundg_layer(chart_name, zoom):
    layout = {
        **TEXT_LAYOUT,
        "text-field": ["get", "METERS"],
        "text-size": 11,
    }
    return symbol_layer(
        "SOUNDG",
        chart_name,
        zoom,
        "SOUNDG",
        layout,
        paint={
            "text-color": [
                "case",
                ["<=", ["get", "METERS"], 9.0],
                "#070707",
                "#7d898c",
            ],
            "text-halo-color": BACKGROUND_COLOR,
            "text-halo-width": 1.5,
        },
    )


def buoy_base_layer(source_layer, chart_name, zoom):
    return symbol_layer(
        f"{source_layer}_base",
        chart_name,
        zoom,
        source_layer,
        {
            "icon-allow-overlap": True,
            "icon-anchor": "bottom",
            "icon-image": buoy_icon_expression(),
            "icon-keep-upright": True,
            "symbol-placement": "point",
        },
    )


def buoy_icon_expression():
    return [
        "match",
        ["get", "BOYSHP"],
        1,
        [
            "match",
            ["get", "COLOUR"],
            "1",
            "BOYCON01",
            "3",
            "BOYCON60",
            "4",
            "BOYCON61",
            "6",
            "BOYCON62",
            "6,3",
            "BOYCON62",
            "2,3,2",
            "BOYCON63",
            "2",
            "BOYCON64",
            "4,1,4,1,4",
            "BOYCON65",
            "3,4,3",
            "BOYCON66",
            "4,3,4",
            "BOYCON67",
            "4,3",
            "BOYCON68",
            "2,6",
            "BOYCON69",
            "6,2",
            "BOYCON70",
            "2,6,2",
            "BOYCON71",
            "6,2,6",
            "BOYCON72",
            "4,1",
            "BOYCON73",
            "1,11",
            "BOYCON77",
            "3,1",
            "BOYCON78",
            "3,4",
            "BOYCON79",
            "1,11,1",
            "BOYCON80",
            "5,3,1,5",
            "BOYCON81",
            "BOYCON01",
        ],
        2,
        [
            "match",
            ["get", "COLOUR"],
            "3",
            "BOYCAN60",
            "4",
            "BOYCAN61",
            "1",
            "BOYCAN62",
            "6",
            "BOYCAN63",
            "6,3",
            "BOYCAN63",
            "2",
            "BOYCAN64",
            "2,6",
            "BOYCAN68",
            "6,2",
            "BOYCAN69",
            "2,6,2",
            "BOYCAN70",
            "6,2,6",
            "BOYCAN71",
            "3,4,3",
            "BOYCAN73",
            "1,3",
            "BOYCAN74",
            "3,4",
            "BOYCAN75",
            "2,3,2",
            "BOYCAN76",
            "1,11",
            "BOYCAN77",
            "1,11,1",
            "BOYCAN78",
            "11",
            "BOYCAN79",
            "3,1",
            "BOYCAN80",
            "11,1",
            "BOYCAN81",
            "3,1,3,1,3",
            "BOYCAN82",
            "3,1,3,1",
            "BOYCAN83",
            "BOYCAN65",
        ],
        3,
        [
            "match",
            ["get", "COLOUR"],
            "1",
            "BOYSPH05",
            "3",
            "BOYSPH60",
            "4",
            "BOYSPH61",
            "6",
            "BOYSPH62",
            "6,3",
            "BOYSPH62",
            "1,3,1,3,1",
            "BOYSPH65",
            "3,4,3",
            "BOYSPH66",
            "4,3,4",
            "BOYSPH67",
            "2,6",
            "BOYSPH68",
            "6,2",
            "BOYSPH69",
            "2,6,2",
            "BOYSPH70",
            "6,2,6",
            "BOYSPH71",
            "3,4",
            "BOYSPH74",
            "4,3",
            "BOYSPH75",
            "1,11",
            "BOYSPH76",
            "3,1",
            "BOYSPH78",
            "BOYSPH01",
        ],
        4,
        [
            "match",
            ["get", "COLOUR"],
            "3",
            "BOYPIL60",
            "4",
            "BOYPIL61",
            "6",
            "BOYPIL62",
            "6,3",
            "BOYPIL62",
            "6,3,6",
            "BOYPIL62",
            "2",
            "BOYPIL63",
            "11",
            "BOYPIL64",
            "7",
            "BOYPIL65",
            "3,4,3",
            "BOYPIL66",
            "4,3,4",
            "BOYPIL67",
            "2,6",
            "BOYPIL68",
            "6,2",
            "BOYPIL69",
            "2,6,2",
            "BOYPIL70",
            "6,2,6",
            "BOYPIL71",
            "2,3,2",
            "BOYPIL72",
            "3,1",
            ["match", ["get", "COLPAT"], "2", "BOYPIL73", "BOYPIL76"],
            "3,4",
            "BOYPIL74",
            "4,3",
            "BOYPIL75",
            "4,1",
            "BOYPIL77",
            "3,1,3,1",
            "BOYPIL78",
            "4,1,3,1",
            "BOYPIL79",
            "3,6",
            "BOYPIL80",
            "1,11",
            "BOYPIL81",
            "BOYPIL01",
        ],
        5,
        [
            "match",
            ["get", "COLOUR"],
            "11,1,11,1",
            "BOYSPR04",
            "1",
            "BOYSPR05",
            "3",
            "BOYSPR60",
            "4",
            "BOYSPR61",
            "6",
            "BOYSPR62",
            "6,3",
            "BOYSPR62",
            "6,3,6",
            "BOYSPR62",
            "3,1,3",
            "BOYSPR65",
            "2,6",
            "BOYSPR68",
            "6,2",
            "BOYSPR69",
            "2,6,2",
            "BOYSPR70",
            "6,2,6",
            "BOYSPR71",
            "2,3,2",
            "BOYSPR72",
            "BOYSPR01",
        ],
        6,
        [
            "match",
            ["get", "COLOUR"],
            "2",
            "BOYBAR60",
            "4",
            "BOYBAR61",
            "6",
            "BOYBAR62",
            "6,3",
            "BOYBAR62",
            "BOYBAR01",
        ],
        7,
        "BOYSUP01",
        8,
        "BOYSPR01",
        "",
    ]


def boycar_topmark_layer(chart_name, zoom):
    return symbol_layer(
        "BOYCAR_topmark",
        chart_name,
        zoom,
        "BOYCAR",
        {
            "icon-allow-overlap": True,
            "icon-anchor": "bottom",
            "icon-offset": [6, -19],
            "icon-image": [
                "match",
                ["get", "CATCAM"],
                1,
                "BOYCAR01",
                2,
                "BOYCAR02",
                3,
                "BOYCAR03",
                4,
                "BOYCAR04",
                "",
            ],
            "icon-keep-upright": True,
            "symbol-placement": "point",
        },
    )


def boylat_topmark_layer(chart_name, zoom):
    return symbol_layer(
        "BOYLAT",
        chart_name,
        zoom,
        "BOYLAT",
        {
            "icon-allow-overlap": True,
            "icon-anchor": "bottom",
            "icon-offset": [4, -19],
            "icon-image": ["match", ["get", "CATLAM"], 1, "BOYLAT24", 2, "BOYLAT13", ""],
            "icon-keep-upright": True,
            "symbol-placement": "point",
        },
        id_=f"BOYLAT{chart_name}",
    )


def lights_layer(chart_name, zoom):
    return symbol_layer(
        "LIGHTS",
        chart_name,
        zoom,
        "LIGHTS",
        {
            "icon-allow-overlap": True,
            "icon-anchor": "top-left",
            "icon-image": ["case", ["==", ["get", "CATCAM"], 2], "K", "SY"],
            "icon-keep-upright": False,
            "symbol-placement": "point",
        },
    )


if __name__ == "__main__":
    main()
