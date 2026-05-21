#!/usr/bin/python3

import json
from pathlib import Path


MIN_ZOOM = 0
MAX_ZOOM = 24
BACKGROUND_COLOR = "#C9EDFF"  # DEPDW
LINE_COLOR = "#4C5B63"  # CHGRD/CSTLN
RESTRICTED_AREA_COLOR = "#c045a5"
LAND_COLOR = "#BFBE8F"  # LANDA
BUILT_AREA_COLOR = "#A19653"  # CHBRN
NO_DATA_COLOR = "#93AEBB"  # NODTA
MAGENTA = "#C045D1"  # CHMGD/TRFCD
CHART_BOUNDARY_COLOR = "#f28c28"
DEPIT_COLOR = "#58AF9C"
DEPVS_COLOR = "#61B7FF"
DEPMS_COLOR = "#82CAFF"
DEPMD_COLOR = "#A7D9FB"
DEPDW_COLOR = BACKGROUND_COLOR
DEPIT_LAND_BLEND_COLOR = "#8CBF98"
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

RESTRICTED_OBJECT_SYMBOLS = {
    "ACHARE": "ACHARE51",  # anchorage area
    "CBLARE": "CBLARE51",  # cable area
    "CTNARE": "CTYARE51",  # caution area
    "DMPGRD": "CHINFO07",  # dumping ground
    "DEPARE": "INFARE51",  # depth area; no dedicated sprite in current assets
    "FAIRWY": "FAIRWY51",  # fairway
    "DRGARE": "INFARE51",  # dredged area; no dedicated sprite in current assets
    "DWRTPT": "DWRTPT51",  # deep water route part
    "MIPARE": "CHINFO06",  # military practice area
    "PIPARE": "INFARE51",  # pipeline area; no dedicated sprite in current assets
    "SWPARE": "SWPARE51",  # swept area
}

POINT_SYMBOLS = {
    "CGUSTA": "CGUSTA02",
    "FOGSIG": "FOGSIG01",
    "HRBFAC": "HRBFAC09",
    "MAGVAR": "MAGVAR01",
    "PILPNT": "PILPNT02",
    "RDOSTA": "RDOSTA02",
    "SISTAW": "SISTAT02",  # closest available signal-station sprite
    "SMCFAC": "SMCFAC02",
    "WEDKLP": "WEDKLP03",
}

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

    for chart_name, zoom in charts.items():
        layers.extend(build_overlay_layers(chart_name, zoom))

    return layers


def build_chart_layers(chart_name, zoom):
    layers = [
        fill_layer("SEAARE_fill", chart_name, zoom, "SEAARE", BACKGROUND_COLOR),
        fill_layer(
            "DEPARE_fill_2",
            chart_name,
            zoom,
            "DEPARE",
            DEPMD_COLOR,
            filter_=["all", ["==", "$type", "Polygon"], ["<=", "DRVAL1", 9.0]],
        ),
        fill_layer(
            "DEPARE_fill_safety",
            chart_name,
            zoom,
            "DEPARE",
            DEPMS_COLOR,
            filter_=["all", ["==", "$type", "Polygon"], ["<=", "DRVAL1", 6.0]],
        ),
        fill_layer(
            "DEPARE_fill_1",
            chart_name,
            zoom,
            "DEPARE",
            DEPVS_COLOR,
            filter_=["all", ["==", "$type", "Polygon"], ["<=", "DRVAL1", 3.0]],
        ),
        fill_layer(
            "DEPARE_fill_0",
            chart_name,
            zoom,
            "DEPARE",
            DEPIT_LAND_BLEND_COLOR,
            filter_=[
                "all",
                ["==", "$type", "Polygon"],
                ["<=", "DRVAL2", 0.0],
            ],
        ),
        line_layer("DEPARE_line", chart_name, zoom, "DEPARE", LINE_COLOR, 0.5),
        line_layer("DEPCNT_line", chart_name, zoom, "DEPCNT", LINE_COLOR, 0.5),
        fill_layer("SLCONS_fill", chart_name, zoom, "SLCONS", LAND_COLOR),
        line_layer(
            "SLCONS_line", chart_name, zoom, "SLCONS", LINE_COLOR, 2, filter_=["all"]
        ),
        fill_layer("PONTON_fill", chart_name, zoom, "PONTON", BUILT_AREA_COLOR),
        line_layer(
            "PONTON_line", chart_name, zoom, "PONTON", LINE_COLOR, 2, filter_=["all"]
        ),
        line_layer(
            "BRIDGE_line",
            chart_name,
            zoom,
            "BRIDGE",
            LINE_COLOR,
            4,
            filter_=POLYGON_OR_LINE,
        ),
        fill_layer("HULKES_fill", chart_name, zoom, "HULKES", BUILT_AREA_COLOR),
        line_layer(
            "HULKES_line",
            chart_name,
            zoom,
            "HULKES",
            LINE_COLOR,
            2,
            filter_=POLYGON_OR_LINE,
        ),
        point_symbol_layer("HULKES", chart_name, zoom, "HULKES01"),
        fill_layer("LNDARE_fill", chart_name, zoom, "LNDARE", LAND_COLOR),
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
            1,
            paint={
                "line-color": LINE_COLOR,
                "line-width": 1,
                "line-dasharray": [5, 5],
            },
            filter_=POLYGON_OR_LINE,
        ),
        resare_line_layer(chart_name, zoom),
        resare_symbol_layer(
            "RESARE_entry", chart_name, zoom, "ENTRES51", [7, 8]
        ),
        resare_symbol_layer(
            "RESARE_anchoring", chart_name, zoom, "ACHRES51", [1, 2]
        ),
        resare_symbol_layer(
            "RESARE_fishing", chart_name, zoom, "FSHRES51", [3, 4, 5, 6]
        ),
        *restricted_object_symbol_layers(chart_name, zoom),
        soundg_layer(chart_name, zoom),
        seaare_name_layer(chart_name, zoom),
        lndare_name_layer(chart_name, zoom),
        fill_layer(
            "TSEZNE",
            chart_name,
            zoom,
            "TSEZNE",
            "#d631c9",
            paint={"fill-color": "#d631c9", "fill-opacity": 0.5},
            filter_=["==", "$type", "Polygon"],
        ),
        *build_njord_layers(chart_name, zoom),
    ]

    layers.extend(buoy_base_layer(layer, chart_name, zoom) for layer in BUOY_LAYERS)
    layers.extend(
        [
            lights_layer(chart_name, zoom),
        ]
    )
    return layers


def build_overlay_layers(chart_name, zoom):
    return [
        line_layer(
            "M_COVR_line",
            chart_name,
            zoom,
            "M_COVR",
            CHART_BOUNDARY_COLOR,
            4,
            paint={
                "line-color": CHART_BOUNDARY_COLOR,
                "line-width": 4,
                "line-opacity": 0.85,
            },
            filter_=POLYGON,
        )
    ]


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


def build_njord_layers(chart_name, zoom):
    layers = [
        # Shore, inland water, and area objects.
        fill_layer("BUAARE_fill", chart_name, zoom, "BUAARE", BUILT_AREA_COLOR),
        line_layer("BUAARE_line", chart_name, zoom, "BUAARE", LINE_COLOR, 1, filter_=POLYGON_OR_LINE),
        fill_layer("BUISGL_fill", chart_name, zoom, "BUISGL", LAND_COLOR),
        fill_layer("DAMCON_fill", chart_name, zoom, "DAMCON", LAND_COLOR),
        line_layer("DAMCON_line", chart_name, zoom, "DAMCON", LINE_COLOR, 1, filter_=POLYGON_OR_LINE),
        fill_layer("FORSTC_fill", chart_name, zoom, "FORSTC", BUILT_AREA_COLOR),
        line_layer("FORSTC_line", chart_name, zoom, "FORSTC", LINE_COLOR, 1, filter_=POLYGON_OR_LINE),
        fill_layer("HRBFAC_fill", chart_name, zoom, "HRBFAC", "#ead5ee"),
        fill_layer("LAKARE_fill", chart_name, zoom, "LAKARE", BACKGROUND_COLOR),
        line_layer("LAKARE_line", chart_name, zoom, "LAKARE", LINE_COLOR, 1),
        fill_layer("RIVERS_fill", chart_name, zoom, "RIVERS", BACKGROUND_COLOR),
        line_layer("RIVERS_line", chart_name, zoom, "RIVERS", LINE_COLOR, 1, filter_=POLYGON_OR_LINE),
        fill_layer("SBDARE_fill", chart_name, zoom, "SBDARE", NO_DATA_COLOR),
        fill_layer("LNDRGN_fill", chart_name, zoom, "LNDRGN", LAND_COLOR),
        fill_layer("SILTNK_fill", chart_name, zoom, "SILTNK", BUILT_AREA_COLOR),
        line_layer("SILTNK_line", chart_name, zoom, "SILTNK", LINE_COLOR, 1, filter_=POLYGON_OR_LINE),
        fill_layer("SMCFAC_fill", chart_name, zoom, "SMCFAC", "#ead5ee"),
        line_layer("WEDKLP_line", chart_name, zoom, "WEDKLP", "#669966", 1, filter_=POLYGON_OR_LINE),
        # Cables, pipelines, fairways, tracks, and restricted/caution areas.
        dashed_line_layer("CBLOHD_line", chart_name, zoom, "CBLOHD", LINE_COLOR, 0.5, [10, 5]),
        dashed_line_layer("CBLSUB_line", chart_name, zoom, "CBLSUB", MAGENTA, 1, [6, 3]),
        dashed_line_layer("PIPSOL_line", chart_name, zoom, "PIPSOL", LINE_COLOR, 1, [5, 3]),
        dashed_line_layer("CTNARE_line", chart_name, zoom, "CTNARE", MAGENTA, 1, [5, 3]),
        dashed_line_layer("DMPGRD_line", chart_name, zoom, "DMPGRD", MAGENTA, 1, [5, 3]),
        dredged_area_fill_layer(chart_name, zoom),
        dashed_line_layer("DRGARE_line", chart_name, zoom, "DRGARE", LINE_COLOR, 0.5, [5, 3]),
        dashed_line_layer("FAIRWY_line", chart_name, zoom, "FAIRWY", LINE_COLOR, 0.5, [10, 5]),
        dashed_line_layer("RECTRC_line", chart_name, zoom, "RECTRC", LINE_COLOR, 0.5, [10, 5]),
        rectrc_symbol_layer(chart_name, zoom),
        # Beacons, marks, stations, facilities, and hazards.
        bcnlat_layer(chart_name, zoom),
        bcnspp_layer(chart_name, zoom),
        daymar_layer(chart_name, zoom),
        lndmrk_layer(chart_name, zoom),
        lndrgn_name_layer(chart_name, zoom),
        siltnk_layer(chart_name, zoom),
        obstrn_layer(chart_name, zoom),
        uwtroc_layer(chart_name, zoom),
        wrecks_layer(chart_name, zoom),
    ]

    for source_layer, icon in POINT_SYMBOLS.items():
        layers.append(point_symbol_layer(source_layer, chart_name, zoom, icon))

    layers.extend(
        [
            point_symbol_layer("DAMCON", chart_name, zoom, "CHINFO06"),
            point_symbol_layer("BUAARE", chart_name, zoom, "BUAARE02"),
            point_symbol_layer("CTNARE", chart_name, zoom, "CHINFO06"),
            point_symbol_layer("DMPGRD", chart_name, zoom, "CHINFO07"),
            point_symbol_layer("FORSTC", chart_name, zoom, "FORSTC11"),
        ]
    )
    return layers


def dashed_line_layer(id_prefix, chart_name, zoom, source_layer, color, width, dasharray):
    return line_layer(
        id_prefix,
        chart_name,
        zoom,
        source_layer,
        color,
        width,
        paint={
            "line-color": color,
            "line-width": width,
            "line-dasharray": dasharray,
        },
        filter_=POLYGON_OR_LINE,
    )


def point_symbol_layer(source_layer, chart_name, zoom, icon, layout=None, id_prefix=None, filter_=None):
    symbol_layout = {
        "icon-allow-overlap": True,
        "icon-image": icon,
        "symbol-placement": "point",
    }
    if layout:
        symbol_layout.update(layout)
    return symbol_layer(
        id_prefix or source_layer,
        chart_name,
        zoom,
        source_layer,
        symbol_layout,
        filter_=filter_,
    )


def bcnlat_layer(chart_name, zoom):
    return point_symbol_layer(
        "BCNLAT",
        chart_name,
        zoom,
        [
            "match",
            ["get", "BCNSHP"],
            1,
            "BCNLAT21",
            2,
            "BCNLAT22",
            3,
            "BCNLAT15",
            4,
            "BCNLAT16",
            5,
            "BCNSAW21",
            6,
            "BCNSPP21",
            7,
            "CAIRNS11",
            "BCNDEF13",
        ],
    )


def bcnspp_layer(chart_name, zoom):
    return point_symbol_layer(
        "BCNSPP",
        chart_name,
        zoom,
        [
            "match",
            ["to-string", ["get", "CATSPM"]],
            "9",
            "NOTBRD11",
            "10",
            "NOTBRD11",
            "13",
            "BCNSPP13",
            "BCNDEF13",
        ],
    )


def daymar_layer(chart_name, zoom):
    return point_symbol_layer(
        "DAYMAR",
        chart_name,
        zoom,
        [
            "match",
            ["get", "TOPSHP"],
            1,
            "DAYSQR01",
            4,
            "DAYSQR01",
            2,
            "DAYTRI01",
            3,
            "DAYTRI05",
            "DAYSQR01",
        ],
        layout={"icon-offset": [0, -10]},
    )


def lndmrk_layer(chart_name, zoom):
    return point_symbol_layer(
        "LNDMRK",
        chart_name,
        zoom,
        [
            "match",
            ["get", "CATLMK"],
            2,
            "CAIRNS11",
            3,
            "CHIMNY11",
            5,
            "TOWERS01",
            7,
            "MSTCON14",
            12,
            "WIMCON11",
            15,
            "DOMES011",
            "TOWERS01",
        ],
    )


def lndrgn_name_layer(chart_name, zoom):
    return symbol_layer(
        "LNDRGN_name",
        chart_name,
        zoom,
        "LNDRGN",
        {
            **TEXT_LAYOUT,
            "text-allow-overlap": False,
            "text-field": ["get", "OBJNAM"],
            "text-ignore-placement": False,
            "text-optional": True,
            "text-size": 10,
        },
        paint={"text-color": "#5b542e"},
        filter_=["has", "OBJNAM"],
    )


def siltnk_layer(chart_name, zoom):
    return point_symbol_layer(
        "SILTNK",
        chart_name,
        zoom,
        [
            "match",
            ["get", "CATSIL"],
            1,
            "SILBUI11",
            2,
            "TNKCON12",
            3,
            "TOWERS01",
            "SILBUI01",
        ],
    )


def dredged_area_fill_layer(chart_name, zoom):
    return fill_layer(
        "DRGARE_fill",
        chart_name,
        zoom,
        "DRGARE",
        "#bad5e1",
        paint={
            "fill-color": [
                "case",
                ["<=", ["coalesce", ["get", "DRVAL1"], 999], 0.0],
                DEPIT_COLOR,
                ["<=", ["coalesce", ["get", "DRVAL1"], 999], 3.0],
                DEPVS_COLOR,
                ["<=", ["coalesce", ["get", "DRVAL1"], 999], 6.0],
                DEPMS_COLOR,
                ["<=", ["coalesce", ["get", "DRVAL1"], 999], 9.0],
                DEPMD_COLOR,
                BACKGROUND_COLOR,
            ],
            "fill-opacity": 0.65,
        },
    )


def rectrc_symbol_layer(chart_name, zoom):
    return symbol_layer(
        "RECTRC_symbol",
        chart_name,
        zoom,
        "RECTRC",
        {
            "icon-allow-overlap": True,
            "icon-image": [
                "match",
                ["get", "TRAFIC"],
                1,
                "RECTRC55",
                2,
                "RECTRC56",
                3,
                "RECTRC57",
                "RECDEF51",
            ],
            "icon-rotation-alignment": "map",
            "symbol-placement": "line",
            "symbol-spacing": 120,
        },
        filter_=["==", "$type", "LineString"],
    )


def obstrn_layer(chart_name, zoom):
    return point_symbol_layer(
        "OBSTRN",
        chart_name,
        zoom,
        [
            "case",
            ["<=", ["coalesce", ["get", "VALSOU"], 999], 9.0],
            "DANGER01",
            ["==", ["get", "WATLEV"], 3],
            "OBSTRN01",
            ["==", ["get", "WATLEV"], 5],
            "OBSTRN03",
            "OBSTRN01",
        ],
    )


def uwtroc_layer(chart_name, zoom):
    return point_symbol_layer(
        "UWTROC",
        chart_name,
        zoom,
        [
            "match",
            ["get", "WATLEV"],
            3,
            "UWTROC04",
            4,
            "UWTROC03",
            5,
            "UWTROC03",
            "ISODGR01",
        ],
    )


def wrecks_layer(chart_name, zoom):
    return point_symbol_layer(
        "WRECKS",
        chart_name,
        zoom,
        [
            "case",
            ["<=", ["coalesce", ["get", "VALSOU"], 999], 9.0],
            "DANGER01",
            ["==", ["get", "CATWRK"], 1],
            "WRECKS01",
            ["==", ["get", "WATLEV"], 3],
            "WRECKS04",
            ["==", ["get", "WATLEV"], 5],
            "WRECKS05",
            "WRECKS04",
        ],
    )


def resare_line_layer(chart_name, zoom):
    return line_layer(
        "RESARE_line",
        chart_name,
        zoom,
        "RESARE",
        RESTRICTED_AREA_COLOR,
        1,
        paint={
            "line-color": RESTRICTED_AREA_COLOR,
            "line-width": 1,
            "line-opacity": 0.65,
            "line-dasharray": [3, 2],
        },
        filter_=["==", ["geometry-type"], "Polygon"],
    )


def resare_symbol_layer(id_prefix, chart_name, zoom, icon, restrictions):
    return symbol_layer(
        id_prefix,
        chart_name,
        zoom,
        "RESARE",
        {
            "icon-allow-overlap": False,
            "icon-image": icon,
            "symbol-placement": "point",
        },
        filter_=["all", ["==", ["geometry-type"], "Polygon"], restrn_filter(restrictions)],
    )


def restricted_object_symbol_layers(chart_name, zoom):
    return [
        symbol_layer(
            f"{source_layer}_restricted",
            chart_name,
            zoom,
            source_layer,
            {
                "icon-allow-overlap": False,
                "icon-image": icon,
                "symbol-placement": "point",
            },
            filter_=["all", ["==", ["geometry-type"], "Polygon"], ["has", "RESTRN"]],
        )
        for source_layer, icon in RESTRICTED_OBJECT_SYMBOLS.items()
    ]


def restrn_filter(restrictions):
    values = []
    for restriction in restrictions:
        values.extend([restriction, str(restriction)])
    restrictions_property = ["coalesce", ["get", "RESTRN"], ["literal", []]]
    return ["any", *[["in", value, restrictions_property] for value in values]]


def seaare_name_layer(chart_name, zoom):
    layout = {
        **TEXT_LAYOUT,
        "text-anchor": "left",
        "text-allow-overlap": False,
        "text-field": ["get", "OBJNAM"],
        "text-ignore-placement": False,
        "text-offset": [4, 2],
        "text-optional": True,
        "text-size": 14,
    }
    return symbol_layer(
        "SEAARE_name",
        chart_name,
        zoom,
        "SEAARE",
        layout,
        paint={
            "text-color": "#070707",
            "text-halo-color": BACKGROUND_COLOR,
            "text-halo-width": 2.5,
        },
        filter_=["has", "OBJNAM"],
    )


def lndare_name_layer(chart_name, zoom):
    layout = {
        **TEXT_LAYOUT,
        "text-allow-overlap": False,
        "text-field": ["get", "OBJNAM"],
        "text-ignore-placement": False,
        "text-optional": True,
        "text-size": 14,
    }
    return symbol_layer(
        "LNDARE_name",
        chart_name,
        zoom,
        "LNDARE",
        layout,
        paint={
            "text-color": "#070707",
            "text-halo-color": LAND_COLOR,
            "text-halo-width": 2.5,
        },
        filter_=["has", "OBJNAM"],
    )


def soundg_layer(chart_name, zoom):
    layout = {
        **TEXT_LAYOUT,
        "text-allow-overlap": True,
        "text-field": ["to-string", ["get", "DEPTH"]],
        "text-ignore-placement": False,
        "text-size": 16,
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
                ["<=", ["get", "DEPTH"], 9.0],
                "#070707",
                "#7d898c",
            ],
            "text-halo-color": BACKGROUND_COLOR,
            "text-halo-width": 2.5,
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
            "icon-image": buoy_icon_expression(source_layer),
            "icon-keep-upright": True,
            "symbol-placement": "point",
        },
    )


def buoy_icon_expression(source_layer):
    if source_layer == "BOYCAR":
        return ["match", ["get", "CATCAM"], 1, "BOYCAR01", 2, "BOYCAR02", 3, "BOYCAR03", 4, "BOYCAR04", "BOYDEF03"]
    if source_layer == "BOYINB":
        return "BOYMOR11"
    if source_layer == "BOYISD":
        return "BOYISD12"
    if source_layer == "BOYLAT":
        return boylat_icon_expression()
    if source_layer == "BOYSAW":
        return first_colour_icon("BOYSAW12", "BOYSPP11", "BOYSPP11", "BOYSPP11")
    if source_layer == "BOYSPP":
        return [
            "match",
            ["to-string", ["get", "CATSPM"]],
            "15",
            "BOYSUP02",
            "52",
            "BOYDEF03",
            boyshp_icon_expression(),
        ]

    return boyshp_icon_expression()


def light_icon_expression():
    return [
        "match",
        first_colour_expression(),
        "3",
        "LIGHTS11",
        "4",
        "LIGHTS12",
        "1",
        "LIGHTS13",
        "6",
        "LIGHTS13",
        "LIGHTS13",
    ]


def first_colour_expression():
    return ["slice", ["to-string", ["get", "COLOUR"]], 0, 1]


def first_colour_icon(red, green, black, default):
    return [
        "match",
        first_colour_expression(),
        "3",
        red,
        "4",
        green,
        "2",
        black,
        default,
    ]


def boylat_icon_expression():
    return [
        "match",
        ["get", "CATLAM"],
        1,
        rhomboid_buoy_icon(),
        3,
        rhomboid_buoy_icon(),
        2,
        half_triangle_buoy_icon(),
        4,
        half_triangle_buoy_icon(),
        boyshp_icon_expression(),
    ]


def boyshp_icon_expression():
    return [
        "match",
        ["get", "BOYSHP"],
        1,
        half_triangle_buoy_icon(),
        2,
        rhomboid_buoy_icon(),
        3,
        circle_buoy_icon(),
        4,
        stake_buoy_icon(),
        5,
        stake_buoy_icon(),
        6,
        circle_buoy_icon(),
        7,
        circle_buoy_icon(),
        8,
        circle_buoy_icon(),
        "BOYDEF03",
    ]


def half_triangle_buoy_icon():
    return first_colour_icon("BOYLAT14", "BOYLAT13", "BOYSPP15", "BOYSPP15")


def rhomboid_buoy_icon():
    return first_colour_icon("BOYLAT24", "BOYLAT23", "BOYSPP25", "BOYSPP25")


def circle_buoy_icon():
    return first_colour_icon("BOYSAW12", "BOYSPP11", "BOYSPP11", "BOYSPP11")


def stake_buoy_icon():
    return first_colour_icon("BCNLAT21", "BCNLAT22", "BCNSAW21", "BCNSPP21")


def lights_layer(chart_name, zoom):
    return symbol_layer(
        "LIGHTS",
        chart_name,
        zoom,
        "LIGHTS",
        {
            "icon-allow-overlap": True,
            "icon-anchor": "bottom",
            "icon-image": light_icon_expression(),
            "icon-rotate": 135,
            "symbol-placement": "point",
        },
    )


if __name__ == "__main__":
    main()
