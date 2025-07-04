#!/usr/bin/python3

import os

script_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.dirname(script_path)
output_path = os.path.dirname(parent_path + "/output/")
output_file = output_path + "/light-style.json"
print("file generated at: " + output_file)


# dict = 'name': ("file", "minzoom", "maxzoom") 
charts = {}
for file in os.listdir(output_path):
    filename = os.fsdecode(file)
    if filename.endswith(".mbtiles"): 
        charts[os.path.splitext(filename)[0]] = (os.path.join(output_path, filename), 0, 24)

# optional: adjust minzoom and maxzoom values to your liking:
#charts['US4NY1JH'][1] = 10 # adjust minzoom
#charts['US4NY1JH'][2] = 20 # adjust maxzoom

################################################################################
with open(output_file, "w") as f:
    f.write('{\n')
    f.write('    "version": 8,\n')
    f.write('    "name": "light",\n')
    #f.write('    "sprite": "file://' + output_path + '/sprites/rastersymbols-day",\n')
    #f.write('    "glyphs": "file://' + output_path + '/fonts/{fontstack}/{range}.pbf",\n')
    f.write('    "sprite": "sprites/rastersymbols-day",\n')
    f.write('    "glyphs": "fonts/{fontstack}/{range}.pbf",\n')

    f.write('    "sources": {\n')
    for key in charts:
        f.write('       "' + key + '": {\n')
        f.write('            "type": "vector",\n')
        #f.write('            "url": "mbtiles://' + charts[key][0] + '"\n')
        f.write('            "url": "mbtiles://' + key + '.mbtiles"\n')
        f.write('        }')
        # if last source in dict then do not add a comma at the end
        if (key != [*charts.keys()][-1]):
            f.write(',')
        f.write('\n')
    f.write('    },\n')

    f.write('    "layers": [\n')
    f.write('        {\n')
    f.write('            "id": "background",\n')
    f.write('            "paint": {\n')
    f.write('                "background-color": "#d4eaee",\n')
    f.write('                "background-opacity": 1\n')
    f.write('            },\n')
    f.write('            "type": "background"\n')
    f.write('        },\n')
    for key in charts:
        # The following is a list of those object classes allowed in an ENC and the geometric primitives allowed for each of them (P = point, L = line, A = area, N = none)
        # SEAARE P A
        f.write('        {\n')
        f.write('            "filter": [\n')
        f.write('                "any",\n')
        f.write('                [\n')
        f.write('                    "==",\n')
        f.write('                    "$type",\n')
        f.write('                    "Polygon"\n')
        f.write('                ]\n')
        f.write('            ],\n')
        f.write('            "id": "SEAARE_fill_' + key + '",\n')
        f.write('            "paint": {\n')
        f.write('                "fill-color": "#d4eaee"\n')
        f.write('            },\n')
        f.write('            "source": "' + key + '",\n')
        f.write('            "source-layer": "SEAARE",\n')
        f.write('            "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('            "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('            "type": "fill"\n')
        f.write('        },\n')
        # DEPARE L A
        f.write('        {\n')
        f.write('            "filter": [\n')
        f.write('                "all",\n')
        f.write('                [\n')
        f.write('                    "==",\n')
        f.write('                    "$type",\n')
        f.write('                    "Polygon"\n')
        f.write('                ],\n')
        f.write('                [\n')
        f.write('                    "<=",\n')
        f.write('                    "DRVAL1",\n')
        f.write('                    9.0\n')
        f.write('                ]\n')
        f.write('            ],\n')
        f.write('            "id": "DEPARE_fill_2_' + key + '",\n')
        f.write('            "paint": {\n')
        f.write('                "fill-color": "#bad5e1"\n')
        f.write('            },\n')
        f.write('            "source": "' + key + '",\n')
        f.write('            "source-layer": "DEPARE",\n')
        f.write('            "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('            "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('            "type": "fill"\n')
        f.write('        },\n')
        f.write('        {\n')
        f.write('            "filter": [\n')
        f.write('                "all",\n')
        f.write('                [\n')
        f.write('                    "==",\n')
        f.write('                    "$type",\n')
        f.write('                    "Polygon"\n')
        f.write('                ],\n')
        f.write('                [\n')
        f.write('                    "<=",\n')
        f.write('                    "DRVAL1",\n')
        f.write('                    3.0\n')
        f.write('                ]\n')
        f.write('            ],\n')
        f.write('            "id": "DEPARE_fill_1_' + key + '",\n')
        f.write('            "paint": {\n')
        f.write('                "fill-color": "#73b6ef"\n')
        f.write('            },\n')
        f.write('            "source": "' + key + '",\n')
        f.write('            "source-layer": "DEPARE",\n')
        f.write('            "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('            "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('            "type": "fill"\n')
        f.write('        },\n')
        f.write('        {\n')
        f.write('           "filter": [\n')
        f.write('               "all",\n')
        f.write('               [\n')
        f.write('                   "==",\n')
        f.write('                   "$type",\n')
        f.write('                   "Polygon"\n')
        f.write('               ],\n')
        f.write('               [\n')
        f.write('                   "<",\n')
        f.write('                   "DRVAL1",\n')
        f.write('                   0.0\n')
        f.write('               ],\n')
        f.write('               [\n')
        f.write('                   "<=",\n')
        f.write('                   "DRVAL2",\n')
        f.write('                   0.0\n')
        f.write('               ]\n')
        f.write('           ],\n')
        f.write('            "id": "DEPARE_fill_0_' + key + '",\n')
        f.write('            "paint": {\n')
        f.write('                "fill-color": "#83b295"\n')
        f.write('            },\n')
        f.write('            "source": "' + key + '",\n')
        f.write('            "source-layer": "DEPARE",\n')
        f.write('            "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('            "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('            "type": "fill"\n')
        f.write('        },\n')
        f.write('        {\n')
        f.write('            "filter": [\n')
        f.write('                "any",\n')
        f.write('                [\n')
        f.write('                    "==",\n')
        f.write('                    "$type",\n')
        f.write('                    "Polygon"\n')
        f.write('                ]\n')
        f.write('            ],\n')
        f.write('            "id": "DEPARE_line_' + key + '",\n')
        f.write('            "paint": {\n')
        f.write('                "line-color": "#525a5c",\n')
        f.write('                "line-width": 0.5\n')
        f.write('            },\n')
        f.write('            "source": "' + key + '",\n')
        f.write('            "source-layer": "DEPARE",\n')
        f.write('            "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('            "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('            "type": "line"\n')
        f.write('        },\n')
        # DEPCNT L
        f.write('        {\n')
        f.write('            "filter": [\n')
        f.write('                "any",\n')
        f.write('                [\n')
        f.write('                    "==",\n')
        f.write('                    "$type",\n')
        f.write('                    "Polygon"\n')
        f.write('                ]\n')
        f.write('            ],\n')
        f.write('            "id": "DEPCNT_line_' + key + '",\n')
        f.write('            "paint": {\n')
        f.write('                "line-color": "#525a5c",\n')
        f.write('                "line-width": 0.5\n')
        f.write('            },\n')
        f.write('            "source": "' + key + '",\n')
        f.write('            "source-layer": "DEPCNT",\n')
        f.write('            "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('            "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('            "type": "line"\n')
        f.write('        },\n')
        # SLCONS P L A
        f.write('        {\n')
        f.write('            "filter": [\n')
        f.write('                "all"\n')
        f.write('            ],\n')
        f.write('            "id": "SLCONS_line_' + key + '",\n')
        f.write('            "paint": {\n')
        f.write('                "line-color": "#525a5c",\n')
        f.write('                "line-width": 1\n')
        f.write('            },\n')
        f.write('            "source": "' + key + '",\n')
        f.write('            "source-layer": "SLCONS",\n')
        f.write('            "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('            "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('            "type": "line"\n')
        f.write('        },\n')
        # PONTON L A
        f.write('        {\n')
        f.write('            "filter": [\n')
        f.write('                "any",\n')
        f.write('                [\n')
        f.write('                    "==",\n')
        f.write('                    "$type",\n')
        f.write('                    "Polygon"\n')
        f.write('                ]\n')
        f.write('            ],\n')
        f.write('            "id": "PONTON_fill_' + key + '",\n')
        f.write('            "paint": {\n')
        f.write('                "fill-color": "#b7911f"\n')
        f.write('            },\n')
        f.write('            "source": "' + key + '",\n')
        f.write('            "source-layer": "PONTON",\n')
        f.write('            "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('            "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('            "type": "fill"\n')
        f.write('        },\n')
        f.write('        {\n')
        f.write('            "filter": [\n')
        f.write('                "all"\n')
        f.write('            ],\n')
        f.write('            "id": "PONTON_line_' + key + '",\n')
        f.write('            "paint": {\n')
        f.write('                "line-color": "#525a5c",\n')
        f.write('                "line-width": 1\n')
        f.write('            },\n')
        f.write('            "source": "' + key + '",\n')
        f.write('            "source-layer": "PONTON",\n')
        f.write('            "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('            "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('            "type": "line"\n')
        f.write('        },\n')
        # BRIDGE P L A
        f.write('        {\n')
        f.write('            "filter": [\n')
        f.write('                "all",\n')
        f.write('                [\n')
        f.write('                    "==",\n')
        f.write('                    "$type",\n')
        f.write('                    "Polygon"\n')
        f.write('                ]\n')
        f.write('            ],\n')
        f.write('            "id": "BRIDGE_fill_' + key + '",\n')
        f.write('            "paint": {\n')
        f.write('                "fill-color": "#B69D40"\n')
        f.write('            },\n')
        f.write('            "source": "' + key + '",\n')
        f.write('            "source-layer": "BRIDGE",\n')
        f.write('            "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('            "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('            "type": "fill"\n')
        f.write('        },\n')
        f.write('        {\n')
        f.write('            "filter": [\n')
        f.write('                "any",\n')
        f.write('                [\n')
        f.write('                    "==",\n')
        f.write('                    "$type",\n')
        f.write('                    "Polygon"\n')
        f.write('                ],\n')
        f.write('                [\n')
        f.write('                    "==",\n')
        f.write('                    "$type",\n')
        f.write('                    "LineString"\n')
        f.write('                ]\n')
        f.write('            ],\n')
        f.write('            "id": "BRIDGE_line_' + key + '",\n')
        f.write('            "paint": {\n')
        f.write('                "line-color": "#525a5c",\n')
        f.write('                "line-width": 5\n')
        f.write('            },\n')
        f.write('            "source": "' + key + '",\n')
        f.write('            "source-layer": "BRIDGE",\n')
        f.write('            "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('            "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('            "type": "line"\n')
        f.write('        },\n')
        # HULKES P A
        f.write('        {\n')
        f.write('            "filter": [\n')
        f.write('                "any",\n')
        f.write('                [\n')
        f.write('                    "==",\n')
        f.write('                    "$type",\n')
        f.write('                    "Polygon"\n')
        f.write('                ]\n')
        f.write('            ],\n')
        f.write('            "id": "HULKES_fill_' + key + '",\n')
        f.write('            "paint": {\n')
        f.write('                "fill-color": "#B7911F"\n')
        f.write('            },\n')
        f.write('            "source": "' + key + '",\n')
        f.write('            "source-layer": "HULKES",\n')
        f.write('            "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('            "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('            "type": "fill"\n')
        f.write('        },\n')
        f.write('        {\n')
        f.write('            "filter": [\n')
        f.write('                "any",\n')
        f.write('                [\n')
        f.write('                    "==",\n')
        f.write('                    "$type",\n')
        f.write('                    "Polygon"\n')
        f.write('                ],\n')
        f.write('                [\n')
        f.write('                    "==",\n')
        f.write('                    "$type",\n')
        f.write('                    "LineString"\n')
        f.write('                ]\n')
        f.write('            ],\n')
        f.write('            "id": "HULKES_line_' + key + '",\n')
        f.write('            "paint": {\n')
        f.write('                "line-color": "#525a5c",\n')
        f.write('                "line-width": 1.5\n')
        f.write('            },\n')
        f.write('            "source": "' + key + '",\n')
        f.write('            "source-layer": "HULKES",\n')
        f.write('            "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('            "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('            "type": "line"\n')
        f.write('        },\n')
        # LNDARE P L A
        f.write('       {\n')
        f.write('           "filter": [\n')
        f.write('               "any",\n')
        f.write('               [\n')
        f.write('                   "==",\n')
        f.write('                   "$type",\n')
        f.write('                   "Polygon"\n')
        f.write('               ]\n')
        f.write('           ],\n')
        f.write('           "id": "LNDARE_fill_' + key + '",\n')
        f.write('           "paint": {\n')
        f.write('               "fill-color": "#c9b97a"\n')
        f.write('           },\n')
        f.write('           "source": "' + key + '",\n')
        f.write('           "source-layer": "LNDARE",\n')
        f.write('           "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('           "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('           "type": "fill"\n')
        f.write('       },\n')
        f.write('       {\n')
        f.write('           "filter": [\n')
        f.write('               "any",\n')
        f.write('               [\n')
        f.write('                   "==",\n')
        f.write('                   "$type",\n')
        f.write('                   "Polygon"\n')
        f.write('               ],\n')
        f.write('               [\n')
        f.write('                   "==",\n')
        f.write('                   "$type",\n')
        f.write('                   "LineString"\n')
        f.write('               ]\n')
        f.write('           ],\n')
        f.write('           "id": "LNDARE_line_' + key + '",\n')
        f.write('           "paint": {\n')
        f.write('               "line-color": "#525a5c",\n')
        f.write('               "line-width": 2\n')
        f.write('           },\n')
        f.write('           "source": "' + key + '",\n')
        f.write('           "source-layer": "LNDARE",\n')
        f.write('           "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('           "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('           "type": "line"\n')
        f.write('       },\n')
        # LNDRGN P A
        # COALNE L
        f.write('       {\n')
        f.write('           "filter": [\n')
        f.write('               "any",\n')
        f.write('               [\n')
        f.write('                   "==",\n')
        f.write('                   "$type",\n')
        f.write('                   "Polygon"\n')
        f.write('               ],\n')
        f.write('               [\n')
        f.write('                   "==",\n')
        f.write('                   "$type",\n')
        f.write('                   "LineString"\n')
        f.write('               ]\n')
        f.write('           ],\n')
        f.write('           "id": "COALNE_line_' + key + '",\n')
        f.write('           "paint": {\n')
        f.write('               "line-color": "#525a5c",\n')
        f.write('               "line-width": 2\n')
        f.write('           },\n')
        f.write('           "source": "' + key + '",\n')
        f.write('           "source-layer": "COALNE",\n')
        f.write('           "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('           "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('           "type": "line"\n')
        f.write('       },\n')
        # BUAARE P A
        f.write('       {\n')
        f.write('           "filter": [\n')
        f.write('               "any",\n')
        f.write('               [\n')
        f.write('                   "==",\n')
        f.write('                   "$type",\n')
        f.write('                   "Point"\n')
        f.write('               ]\n')
        f.write('           ],\n')
        f.write('           "id": "BUAARE_name' + key + '",\n')
        f.write('           "layout": {\n')
        f.write('               "symbol-placement": "point",\n')
        f.write('               "text-allow-overlap": true,\n')
        f.write('               "text-anchor": "center",\n')
        f.write('               "text-field": [\n')
        f.write('                   "get",\n')
        f.write('                   "OBJNAM"\n')
        f.write('               ],\n')
        f.write('               "text-font": [\n')
        f.write('                   "Roboto Bold"\n')
        f.write('               ],\n')
        f.write('               "text-ignore-placement": true,\n')
        f.write('               "text-justify": "center",\n')
        f.write('               "text-size": 9\n')
        f.write('           },\n')
        f.write('           "paint": {\n')
        f.write('               "text-color": "#ffffff"\n')
        f.write('           },\n')
        f.write('           "source": "' + key + '",\n')
        f.write('           "source-layer": "BUAARE",\n')
        f.write('           "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('           "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('           "type": "symbol"\n')
        f.write('       },\n')
        # SOUNDG P
        f.write('       {\n')
        f.write('           "filter": [\n')
        f.write('               "any",\n')
        f.write('               [\n')
        f.write('                   "==",\n')
        f.write('                   "$type",\n')
        f.write('                   "Point"\n')
        f.write('               ]\n')
        f.write('           ],\n')
        f.write('           "id": "SOUNDG_' + key + '",\n')
        f.write('           "layout": {\n')
        f.write('               "symbol-placement": "point",\n')
        f.write('               "text-allow-overlap": true,\n')
        f.write('               "text-anchor": "center",\n')
        f.write('               "text-field": [\n')
        f.write('                   "get",\n')
        f.write('                   "METERS"\n')
        f.write('               ],\n')
        f.write('               "text-font": [\n')
        f.write('                   "Roboto Bold"\n')
        f.write('               ],\n')
        f.write('               "text-ignore-placement": true,\n')
        f.write('               "text-justify": "center",\n')
        f.write('               "text-size": 11\n')
        f.write('           },\n')
        f.write('           "paint": {\n')
        f.write('               "text-color": [\n')
        f.write('                   "case",\n')
        f.write('                   [\n')
        f.write('                       "<=",\n')
        f.write('                       [\n')
        f.write('                           "get",\n')
        f.write('                           "METERS"\n')
        f.write('                       ],\n')
        f.write('                       9.0\n')
        f.write('                   ],\n')
        f.write('                   "#070707",\n')
        f.write('                   "#7d898c"\n')
        f.write('               ],\n')
        f.write('               "text-halo-color": "#d4eaee",\n')
        f.write('               "text-halo-width": 1.5\n')
        f.write('           },\n')
        f.write('           "source": "' + key + '",\n')
        f.write('           "source-layer": "SOUNDG",\n')
        f.write('           "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('           "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('           "type": "symbol"\n')
        f.write('       },\n')
        # RESARE A
        f.write('       {\n')
        f.write('           "id": "RESARE_' + key + '",\n')
        f.write('           "type": "line",\n')
        f.write('           "source": "' + key + '",\n')
        f.write('           "source-layer": "RESARE",\n')
        f.write('           "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('           "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('           "paint": {\n')
        f.write('               "line-color": "#d631c9",\n')
        f.write('               "line-opacity": 1,\n')
        f.write('               "line-dasharray": [10, 4]\n')
        f.write('           }\n')
        f.write('       },\n')
        # TSEZNE A
        f.write('       {\n')
        f.write('           "id": "TSEZNE_' + key + '",\n')
        f.write('           "type": "fill",\n')
        f.write('           "source": "' + key + '",\n')
        f.write('           "source-layer": "TSEZNE",\n')
        f.write('           "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('           "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('           "filter": [ "==", "$type", "Polygon" ],\n')
        f.write('           "paint": {\n')
        f.write('               "fill-color": "#d631c9",\n')
        f.write('               "fill-opacity": 0.5\n')
        f.write('           }\n')
        f.write('       },\n')
        # BOYCAR P
        # BOYINB P
        # BOYISD P
        # BOYLAT P
        # BOYSAM P
        # BCNSPP P
        # BOYSPP P
        for layer in ['BOYCAR', 'BOYINB', 'BOYISD', 'BOYLAT', 'BOYSAW', 'BOYSPP']: 
            f.write('       {\n')
            f.write('           "filter": ["any", ["==", "$type", "Point"]],\n')
            f.write('           "id": "' + layer + '_base_' + key + '",\n')
            f.write('           "layout": {\n')
            f.write('               "icon-allow-overlap": true,\n')
            f.write('               "icon-anchor": "bottom",\n')
            f.write('               "icon-image": [\n')
            f.write('                   "match", ["get", "BOYSHP"],\n')
            f.write('                       1, ["match", ["get", "COLOUR"],\n')
            f.write('                           "1", "BOYCON01",\n')
            f.write('                           "3", "BOYCON60",\n')
            f.write('                           "4", "BOYCON61",\n')
            f.write('                           "6", "BOYCON62",\n')
            f.write('                           "6,3", "BOYCON62",\n') # WORKAROUND: Yellow with red not available
            f.write('                           "2,3,2", "BOYCON63",\n')
            f.write('                           "2", "BOYCON64",\n')
            f.write('                           "4,1,4,1,4", "BOYCON65",\n')
            f.write('                           "3,4,3", "BOYCON66",\n')
            f.write('                           "4,3,4", "BOYCON67",\n')
            f.write('                           "4,3", "BOYCON68",\n')
            f.write('                           "2,6", "BOYCON69",\n')
            f.write('                           "6,2", "BOYCON70",\n')
            f.write('                           "2,6,2", "BOYCON71",\n')
            f.write('                           "6,2,6", "BOYCON72",\n')
            f.write('                           "4,1", "BOYCON73",\n')
            f.write('                           "1,11", "BOYCON77",\n')
            f.write('                           "3,1", "BOYCON78",\n') # TODO: also check for COLPAT == vertical_stripes
            f.write('                           "3,4", "BOYCON79",\n')
            f.write('                           "1,11,1", "BOYCON80",\n')
            f.write('                           "5,3,1,5", "BOYCON81",\n')
            f.write('                           "BOYCON01"\n')
            f.write('                       ],\n')
            f.write('                       2, ["match", ["get", "COLOUR"],\n')
            f.write('                           "3", "BOYCAN60",\n')
            f.write('                           "4", "BOYCAN61",\n')
            f.write('                           "1", "BOYCAN62",\n')
            f.write('                           "6", "BOYCAN63",\n')
            f.write('                           "6,3", "BOYCAN63",\n') # WORKAROUND: Yellow with red not available
            f.write('                           "2", "BOYCAN64",\n')
            f.write('                           "2,6", "BOYCAN68",\n')
            f.write('                           "6,2", "BOYCAN69",\n')
            f.write('                           "2,6,2", "BOYCAN70",\n')
            f.write('                           "6,2,6", "BOYCAN71",\n')
            f.write('                           "3,4,3", "BOYCAN73",\n')
            f.write('                           "1,3", "BOYCAN74",\n') # TODO: also check for COLPAT == vertical_stripes
            f.write('                           "3,4", "BOYCAN75",\n')
            f.write('                           "2,3,2", "BOYCAN76",\n')
            f.write('                           "1,11", "BOYCAN77",\n')
            f.write('                           "1,11,1", "BOYCAN78",\n')
            f.write('                           "11", "BOYCAN79",\n')
            f.write('                           "3,1", "BOYCAN80",\n')
            f.write('                           "11,1", "BOYCAN81",\n')
            f.write('                           "3,1,3,1,3", "BOYCAN82",\n')
            f.write('                           "3,1,3,1", "BOYCAN83",\n')
            f.write('                           "BOYCAN65"\n')
            f.write('                       ],\n')
            f.write('                       3, ["match", ["get", "COLOUR"],\n')
            f.write('                           "1", "BOYSPH05",\n')
            f.write('                           "3", "BOYSPH60",\n')
            f.write('                           "4", "BOYSPH61",\n')
            f.write('                           "6", "BOYSPH62",\n')
            f.write('                           "6,3", "BOYSPH62",\n') # WORKAROUND: Yellow with red not available
            f.write('                           "1,3,1,3,1", "BOYSPH65",\n') # TODO: also check for COLPAT == vertical_stripes
            f.write('                           "3,4,3", "BOYSPH66",\n')
            f.write('                           "4,3,4", "BOYSPH67",\n')
            f.write('                           "2,6", "BOYSPH68",\n')
            f.write('                           "6,2", "BOYSPH69",\n')
            f.write('                           "2,6,2", "BOYSPH70",\n')
            f.write('                           "6,2,6", "BOYSPH71",\n')
            f.write('                           "3,4", "BOYSPH74",\n')
            f.write('                           "4,3", "BOYSPH75",\n')
            f.write('                           "1,11", "BOYSPH76",\n')
            f.write('                           "3,1", "BOYSPH78",\n') # TODO: also check for COLPAT == vertical_stripes
            f.write('                           "BOYSPH01"\n')
            f.write('                       ],\n')
            f.write('                       4, ["match", ["get", "COLOUR"],\n')
            f.write('                           "3", "BOYPIL60",\n')
            f.write('                           "4", "BOYPIL61",\n')
            f.write('                           "6", "BOYPIL62",\n')
            f.write('                           "6,3", "BOYPIL62",\n') # WORKAROUND: Yellow with red not available
            f.write('                           "6,3,6", "BOYPIL62",\n') # WORKAROUND: Yellow with red not available
            f.write('                           "2", "BOYPIL63",\n')
            f.write('                           "11", "BOYPIL64",\n')
            f.write('                           "7", "BOYPIL65",\n')
            f.write('                           "3,4,3", "BOYPIL66",\n')
            f.write('                           "4,3,4", "BOYPIL67",\n')
            f.write('                           "2,6", "BOYPIL68",\n')
            f.write('                           "6,2", "BOYPIL69",\n')
            f.write('                           "2,6,2", "BOYPIL70",\n')
            f.write('                           "6,2,6", "BOYPIL71",\n')
            f.write('                           "2,3,2", "BOYPIL72",\n')
            f.write('                           "3,1", ["match", ["get", "COLPAT"],\n')
            f.write('                               "2", "BOYPIL73",\n')
            f.write('                               "BOYPIL76"\n')
            f.write('                           ],\n')
            f.write('                           "3,4", "BOYPIL74",\n')
            f.write('                           "4,3", "BOYPIL75",\n')
            f.write('                           "4,1", "BOYPIL77",\n')
            f.write('                           "3,1,3,1", "BOYPIL78",\n')
            f.write('                           "4,1,3,1", "BOYPIL79",\n')
            f.write('                           "3,6", "BOYPIL80",\n')
            f.write('                           "1,11", "BOYPIL81",\n')
            f.write('                           "BOYPIL01"\n')
            f.write('                       ],\n')
            f.write('                       5, ["match", ["get", "COLOUR"],\n')
            f.write('                           "11,1,11,1", "BOYSPR04",\n')
            f.write('                           "1", "BOYSPR05",\n')
            f.write('                           "3", "BOYSPR60",\n')
            f.write('                           "4", "BOYSPR61",\n')
            f.write('                           "6", "BOYSPR62",\n')
            f.write('                           "6,3", "BOYSPR62",\n') # WORKAROUND: Yellow with red not available
            f.write('                           "6,3,6", "BOYSPR62",\n') # WORKAROUND: Yellow with red not available
            f.write('                           "3,1,3", "BOYSPR65",\n')
            f.write('                           "2,6", "BOYSPR68",\n')
            f.write('                           "6,2", "BOYSPR69",\n')
            f.write('                           "2,6,2", "BOYSPR70",\n')
            f.write('                           "6,2,6", "BOYSPR71",\n')
            f.write('                           "2,3,2", "BOYSPR72",\n')
            f.write('                           "BOYSPR01"\n')
            f.write('                       ],\n')
            f.write('                       6, ["match", ["get", "COLOUR"],\n')
            f.write('                           "2", "BOYBAR60",\n')
            f.write('                           "4", "BOYBAR61",\n')
            f.write('                           "6", "BOYBAR62",\n')
            f.write('                           "6,3", "BOYBAR62",\n') # WORKAROUND: Yellow with red not available
            f.write('                           "BOYBAR01"\n')
            f.write('                       ],\n')
            f.write('                       7, "BOYSUP01",\n')
            f.write('                       8, "BOYSPR01",\n')
            f.write('                       ""\n')
            f.write('               ],\n')
            f.write('               "icon-keep-upright": true,\n')
            f.write('               "symbol-placement": "point"\n')
            f.write('           },\n')
            f.write('           "source": "' + key + '",\n')
            f.write('           "source-layer": "' + layer + '",\n')
            f.write('           "minzoom": ' + str(charts[key][1]) + ',\n')
            f.write('           "maxzoom": ' + str(charts[key][2]) + ',\n')
            f.write('           "type": "symbol"\n')
            f.write('       },\n')
        # BOYCAR TOPMARK
        f.write('       {\n')
        f.write('           "filter": ["any", ["==", "$type", "Point"]],\n')
        f.write('           "id": "BOYCAR_topmark_' + key + '",\n')
        f.write('           "layout": {\n')
        f.write('               "icon-allow-overlap": true,\n')
        f.write('               "icon-anchor": "bottom",\n')
        f.write('               "icon-offset": [6, -19],\n')
        f.write('               "icon-image": ["match", ["get", "CATCAM"],\n')
        f.write('                   1, "BOYCAR01",\n')
        f.write('                   2, "BOYCAR02",\n')
        f.write('                   3, "BOYCAR03",\n')
        f.write('                   4, "BOYCAR04",\n')
        f.write('                   ""\n')
        f.write('               ],\n')
        f.write('               "icon-keep-upright": true,\n')
        f.write('               "symbol-placement": "point"\n')
        f.write('           },\n')
        f.write('           "source": "' + key + '",\n')
        f.write('           "source-layer": "BOYCAR",\n')
        f.write('           "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('           "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('           "type": "symbol"\n')
        f.write('       },\n')
        # BOYLAT TOPMARK
        f.write('       {\n')
        f.write('           "filter": ["any", ["==", "$type", "Point"]],\n')
        f.write('           "id": "BOYLAT' + key + '",\n')
        f.write('           "layout": {\n')
        f.write('               "icon-allow-overlap": true,\n')
        f.write('               "icon-anchor": "bottom",\n')
        f.write('               "icon-offset": [4, -19],\n')
        f.write('               "icon-image": ["match", ["get", "CATLAM"],\n')
        f.write('                   1, "BOYLAT24",\n') # REGION A
        f.write('                   2, "BOYLAT13",\n') # REGION A
        f.write('                   ""\n')
        f.write('               ],\n')
        f.write('               "icon-keep-upright": true,\n')
        f.write('               "symbol-placement": "point"\n')
        f.write('           },\n')
        f.write('           "source": "' + key + '",\n')
        f.write('           "source-layer": "BOYLAT",\n')
        f.write('           "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('           "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('           "type": "symbol"\n')
        f.write('       },\n')
        # BOYSSP TOPMARK
        #f.write('       {\n')
        #f.write('           "filter": ["any", ["==", "$type", "Point"]],\n')
        #f.write('           "id": "BOYSSP' + key + '",\n')
        #f.write('           "layout": {\n')
        #f.write('               "icon-allow-overlap": true,\n')
        #f.write('               "icon-anchor": "bottom",\n')
        #f.write('               "icon-offset": [4, -19],\n')
        #f.write('               "icon-image": ["match", ["get", "CATSPM"],\n')
        #f.write('                   1, "BOYSPP15",\n') # TODO
        #f.write('                   2, "BOYSPP15",\n') # TODO
        #f.write('                   3, "BOYSPP15",\n') # TODO
        #f.write('                   4, "BOYSPP15",\n') # TODO
        #f.write('                   5, "BOYSPP15",\n') # TODO
        #f.write('                   6, "BOYSPP15",\n') # TODO
        #f.write('                   7, "BOYSPP15",\n') # TODO
        #f.write('                   8, "BOYSPP15",\n') # TODO
        #f.write('                   9, "BOYSPP15",\n') # TODO
        #f.write('                   10, "BOYSPP15",\n') # TODO
        #f.write('                   11, "BOYSPP15",\n') # TODO
        #f.write('                   12, "BOYSPP15",\n') # TODO
        #f.write('                   13, "BOYSPP15",\n') # TODO
        #f.write('                   14, "BOYSPP15",\n') # TODO
        #f.write('                   15, "BOYSPP15",\n') # TODO
        #f.write('                   16, "BOYSPP15",\n') # TODO
        #f.write('                   17, "BOYSPP15",\n') # TODO
        #f.write('                   18, "BOYSPP15",\n') # TODO
        #f.write('                   19, "BOYSPP15",\n') # TODO
        #f.write('                   20, "BOYSPP15",\n') # TODO
        #f.write('                   21, "BOYSPP15",\n') # TODO
        #f.write('                   22, "BOYSPP15",\n') # TODO
        #f.write('                   23, "BOYSPP15",\n') # TODO
        #f.write('                   24, "BOYSPP15",\n') # TODO
        #f.write('                   25, "BOYSPP15",\n') # TODO
        #f.write('                   26, "BOYSPP15",\n') # TODO
        #f.write('                   28, "BOYSPP15",\n') # TODO
        #f.write('                   29, "BOYSPP15",\n') # TODO
        #f.write('                   30, "BOYSPP15",\n') # TODO
        #f.write('                   31, "BOYSPP15",\n') # TODO
        #f.write('                   32, "BOYSPP15",\n') # TODO
        #f.write('                   33, "BOYSPP15",\n') # TODO
        #f.write('                   34, "BOYSPP15",\n') # TODO
        #f.write('                   35, "BOYSPP15",\n') # TODO
        #f.write('                   36, "BOYSPP15",\n') # TODO
        #f.write('                   37, "BOYSPP15",\n') # TODO
        #f.write('                   38, "BOYSPP15",\n') # TODO
        #f.write('                   39, "BOYSPP15",\n') # TODO
        #f.write('                   40, "BOYSPP15",\n') # TODO
        #f.write('                   41, "BOYSPP15",\n') # TODO
        #f.write('                   42, "BOYSPP15",\n') # TODO
        #f.write('                   43, "BOYSPP15",\n') # TODO
        #f.write('                   44, "BOYSPP15",\n') # TODO
        #f.write('                   45, "BOYSPP15",\n') # TODO
        #f.write('                   46, "BOYSPP15",\n') # TODO
        #f.write('                   47, "BOYSPP15",\n') # TODO
        #f.write('                   48, "BOYSPP15",\n') # TODO
        #f.write('                   49, "BOYSPP15",\n') # TODO
        #f.write('                   50, "BOYSPP15",\n') # TODO
        #f.write('                   51, "BOYSPP15",\n') # TODO
        #f.write('                   52, "BOYSPP15",\n') # TODO
        #f.write('                   53, "BOYSPP15",\n') # TODO
        #f.write('                   54, "BOYSPP15",\n') # TODO
        #f.write('                   55, "BOYSPP15",\n') # TODO
        #f.write('                   56, "BOYSPP15",\n') # TODO
        #f.write('                   ""\n')
        #f.write('               ],\n')
        #f.write('               "icon-keep-upright": true,\n')
        #f.write('               "symbol-placement": "point"\n')
        #f.write('           },\n')
        #f.write('           "source": "' + key + '",\n')
        #f.write('           "source-layer": "BOYSSP",\n')
        #f.write('           "minzoom": ' + str(charts[key][1]) + ',\n')
        #f.write('           "maxzoom": ' + str(charts[key][2]) + ',\n')
        #f.write('           "type": "symbol"\n')
        #f.write('       },\n')
        # LIGHTS P
        f.write('       {\n')
        f.write('           "filter": [\n')
        f.write('               "any",\n')
        f.write('               [\n')
        f.write('                   "==",\n')
        f.write('                   "$type",\n')
        f.write('                   "Point"\n')
        f.write('               ]\n')
        f.write('           ],\n')
        f.write('           "id": "LIGHTS_' + key + '",\n')
        f.write('           "layout": {\n')
        f.write('               "icon-allow-overlap": true,\n')
        f.write('               "icon-anchor": "top-left",\n')
        f.write('               "icon-image": [\n')
        f.write('                   "case",\n')
        f.write('                   [\n')
        f.write('                       "==",\n')
        f.write('                       [\n')
        f.write('                           "get",\n')
        f.write('                           "CATCAM"\n')
        f.write('                       ],\n')
        f.write('                       2\n')
        f.write('                   ],\n')
        f.write('                   "K",\n')
        f.write('                   "SY"\n')
        f.write('               ],\n')
        f.write('               "icon-keep-upright": false,\n')
        f.write('               "symbol-placement": "point"\n')
        f.write('           },\n')
        f.write('           "source": "' + key + '",\n')
        f.write('           "source-layer": "LIGHTS",\n')
        f.write('           "minzoom": ' + str(charts[key][1]) + ',\n')
        f.write('           "maxzoom": ' + str(charts[key][2]) + ',\n')
        f.write('           "type": "symbol"\n')
        f.write('       },\n')
        # ACHARE P A
        # ACHBRT P A
        # ADMARE A
        # AIRARE P A
        # BCNCAR P
        # BCNISD P
        # BCNLAT P
        # BCNSAW P
        # BERTHS P L A
        # BUISGL P A
        # CANALS L A
        # CAUSWY L A
        # CBLARE A
        # CBLOHD L
        # CBLSUB L
        # CGUSTA P
        # CHKPNT P A
        # CONVYR L A
        # CONZNE A
        # COSARE A
        # CRANES P A
        # CTNARE P A
        # CTRPNT P
        # CTSARE P A
        # CURENT P
        # CUSZNE A
        # DAMCON P L A
        # DAYMAR P
        # DISMAR P
        # DOCARE A
        # DRGARE A
        # DRYDOC A
        # DMPGRD P A
        # DYKCON L A
        # DWRTCL L
        # DWRTPT A
        # EXEZNE A
        # FAIRWY A
        # FERYRT L A
        # FLODOC L A
        # FNCLNE L
        # FOGSIG P
        # FORSTC P L A
        # FRPARE A
        # FSHFAC P L A
        # FSHGRD A
        # FSHZNE A
        # GATCON P L A
        # GRIDRN P A
        # HRBARE A
        # HRBFAC P A
        # ICEARE A
        # ICNARE P A
        # ISTZNE A
        # LAKARE A
        # LNDELV P L
        # LNDMRK P L A
        # LITFLT P
        # LITVES P
        # LOCMAG P L A
        # LOGPON P A
        # LOKBSN A
        # MAGVAR P L A
        # MARCUL P L A
        # MIPARE P A
        # MORFAC P L A
        # NAVLNE L
        # OBSTRN P L A
        # OFSPLF P A
        # OSPARE A
        # OILBAR L
        # PILBOP P A
        # PILPNT P
        # PIPARE P A
        # PIPOHD L
        # PIPSOL P L
        # PRCARE P A
        # PRDARE P A
        # PYLONS P A
        # RADLNE L
        # RADRNG A
        # RADRFL P
        # RADSTA P
        # RAILWY L
        # RAPIDS P L A
        # RCRTCL L
        # RCTLPT P A
        # RDOCAL P L
        # RDOSTA P
        # RECTRC L A
        # RETRFL P
        # RIVERS L A
        # ROADWY P L A
        # RSCSTA P
        # RTPBCN P
        # RUNWAY P L A
        # SBDARE P L A
        # SILTNK P A
        # SISTAT P
        # SISTAW P
        # SLOTOP L
        # SLOGRD P A
        # SMCFAC P A
        # SNDWAV P L A
        # SPLARE P A
        # SPRING P
        # STSLNE L
        # SUBTLN A
        # SWPARE A
        # TESARE A
        # TIDEWY L A
        # TOPMAR P
        # TSELNE L
        # TSSBND L
        # TSSCRS A
        # TSSLPT A
        # TSSRON A
        # TUNNEL P L A
        # TWRTPT A
        # UNSARE A
        # UWTROC P
        # VEGATN P L A
        # WATFAL P L
        # WATTUR P L A
        # WEDKLP P A
        # WRECKS P A
        # C_AGGR N
        # C_ASSO N
        # M_ACCY A
        # M_COVR A
        # M_CSCL A
        # M_HOPA A
        # M_NPUB P A
        # M_NSYS A
        # M_QUAL A
        # M_SDAT A
        # M_SREL L A
        # M_VDAT A
        # T_HMON P A
        # T_NHMN P A
        # T_TIMS P A
        # TS_FEB P A
        # TS_PAD P A
        # TS_PNH P A
        # TS_PRH P A
        # TS-TIS P A

    # delete commma after the last layer
    f.seek(0, 2) # seek to end of file; f.seek(0, os.SEEK_END) is legal
    f.seek(f.tell() - 2, 0) # seek to the second last char of file; f.seek(f.tell()-2, os.SEEK_SET) is legal
    f.truncate()
    # close JSON brackets
    f.write('\n')
    f.write('    ]\n')
    f.write('}\n')

# Only object classes, attributes and attribute values which are defined in the IHO Object Catalogue (S-57, Appendix A) may be used in an ENC. Of the object classes defined in the IHO Object catalogue, the following ones are prohibited for use in ENC:
# CANBNK
# LAKSHR
# RIVBNK
# SQUARE
# M_HDAT
# M_PROD
# M_UNIT
# C_STAC
# $AREAS
# $LINES
# $CSYMB
# $COMPS
# $TEXTS
