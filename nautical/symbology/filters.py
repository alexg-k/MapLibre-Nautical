"""MapLibre filter expressions shared by the layerables.

The ``GT``/``LT`` names are swapped relative to their operators (``GT`` is ``"<"``), as in njord;
read them as "the threshold is greater than the prop".
"""

ANY = "any"
ALL = "all"
GT = "<"
GT_EQ = "<="
LT = ">"
LT_EQ = ">="
EQ = "=="
IS_IN = "in"
NOT_EQ = "!="


def eq_type_line_string_or_polygon():
    return [NOT_EQ, "$type", "Point"]


def eq_type_point_or_polygon():
    return [NOT_EQ, "$type", "LineString"]


def eq_type_line_string():
    return [EQ, "$type", "LineString"]


def eq_type_polygon():
    return [EQ, "$type", "Polygon"]


def eq_type_point():
    return [EQ, "$type", "Point"]


def _case_on(colors, prop, options, theme):
    expr = ["case"]
    for color, hex_ in colors.colors(theme):
        if options is None or color in options:
            expr.append(["==", ["get", prop], str(color)])
            expr.append(hex_)
    expr.append("rgba(255, 255, 255, 0)")
    return expr


def area_fill_color(colors, options, theme):
    """A ``case`` on the ``AC`` prop over the theme's colours (restricted to ``options`` when
    given), defaulting to transparent."""
    return _case_on(colors, "AC", options, theme)


def line_color(colors, options, theme):
    return _case_on(colors, "LC", options, theme)
