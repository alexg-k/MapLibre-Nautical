"""Top mark (TOPMAR, code 144). Geometry: Point.

Topmark objects are symbolized through consideration of their platforms, e.g. a buoy. Based on
whether the platform is rigid or floating, the upright or sloping symbol is selected. The
platform comes from ``ChartFeature.associated_layer_names``: any feature sharing the position
makes it floating, none makes it rigid.
"""

from .prelude import *

FLOATING = "FLOATING"
RIGID = "RIGID"

_FLOATING = {
    Topshp.CONE_POINT_UP: "TOPMAR02",
    Topshp.CONE_POINT_DOWN: "TOPMAR04",
    Topshp.SPHERE: "TOPMAR10",
    Topshp.TWO_SPHERE: "TOPMAR12",
    Topshp.CYLINDER_CAN: "TOPMAR13",
    Topshp.BOARD: "TOPMAR14",
    Topshp.X_SHAPE: "TOPMAR65",
    Topshp.UPRIGHT_CROSS: "TOPMAR17",
    Topshp.CUBE_POINT_UP: "TOPMAR16",
    Topshp.TWO_CONES_POINT_TO_POINT: "TOPMAR08",
    Topshp.TWO_CONES_BASE_TO_BASE: "TOPMAR07",
    Topshp.RHOMBUS_DIAMOND: "TOPMAR14",
    Topshp.TWO_CONES_POINTS_UPWARD: "TOPMAR05",
    Topshp.TWO_CONES_POINTS_DOWNWARD: "TOPMAR06",
    Topshp.BESOM_POINT_UP_BROOM_OR_PERCH: "TMARDEF2",
    Topshp.BESOM_POINT_DOWN_BROOM_OR_PERCH: "TMARDEF2",
    Topshp.FLAG: "TMARDEF2",
    Topshp.SPHERE_OVER_RHOMBUS: "TOPMAR10",
    Topshp.SQUARE: "TOPMAR13",
    Topshp.RECTANGLE_HORIZONTAL: "TOPMAR14",
    Topshp.RECTANGLE_VERTICAL: "TOPMAR13",
    Topshp.TRAPEZIUM_UP: "TOPMAR14",
    Topshp.TRAPEZIUM_DOWN: "TOPMAR14",
    Topshp.TRIANGLE_POINT_UP: "TOPMAR02",
    Topshp.TRIANGLE_POINT_DOWN: "TOPMAR04",
    Topshp.CIRCLE: "TOPMAR10",
    Topshp.TWO_UPRIGHT_CROSSES_ONE_OVER_THE_OTHER: "TOPMAR17",
    Topshp.T_SHAPE: "TOPMAR18",
    Topshp.TRIANGLE_POINTING_UP_OVER_A_CIRCLE: "TOPMAR02",
    Topshp.UPRIGHT_CROSS_OVER_A_CIRCLE: "TOPMAR17",
    Topshp.RHOMBUS_OVER_A_CIRCLE: "TOPMAR14",
    Topshp.CIRCLE_OVER_A_TRIANGLE_POINTING_UP: "TOPMAR10",
    Topshp.OTHER_SHAPE: "TMARDEF2",
}

_RIGID = {
    Topshp.CONE_POINT_UP: "TOPMAR22",
    Topshp.CONE_POINT_DOWN: "TOPMAR24",
    Topshp.SPHERE: "TOPMAR30",
    Topshp.TWO_SPHERE: "TOPMAR32",
    Topshp.CYLINDER_CAN: "TOPMAR33",
    Topshp.BOARD: "TOPMAR34",
    Topshp.X_SHAPE: "TOPMAR85",
    Topshp.UPRIGHT_CROSS: "TOPMAR86",
    Topshp.CUBE_POINT_UP: "TOPMAR36",
    Topshp.TWO_CONES_POINT_TO_POINT: "TOPMAR28",
    Topshp.TWO_CONES_BASE_TO_BASE: "TOPMAR27",
    Topshp.RHOMBUS_DIAMOND: "TOPMAR14",
    Topshp.TWO_CONES_POINTS_UPWARD: "TOPMAR25",
    Topshp.TWO_CONES_POINTS_DOWNWARD: "TOPMAR26",
    Topshp.BESOM_POINT_UP_BROOM_OR_PERCH: "TOPMAR88",
    Topshp.BESOM_POINT_DOWN_BROOM_OR_PERCH: "TOPMAR87",
    Topshp.FLAG: "TMARDEF1",
    Topshp.SPHERE_OVER_RHOMBUS: "TOPMAR30",
    Topshp.SQUARE: "TOPMAR33",
    Topshp.RECTANGLE_HORIZONTAL: "TOPMAR34",
    Topshp.RECTANGLE_VERTICAL: "TOPMAR33",
    Topshp.TRAPEZIUM_UP: "TOPMAR34",
    Topshp.TRAPEZIUM_DOWN: "TOPMAR34",
    Topshp.TRIANGLE_POINT_UP: "TOPMAR22",
    Topshp.TRIANGLE_POINT_DOWN: "TOPMAR24",
    Topshp.CIRCLE: "TOPMAR30",
    Topshp.TWO_UPRIGHT_CROSSES_ONE_OVER_THE_OTHER: "TOPMAR86",
    Topshp.T_SHAPE: "TOPMAR89",
    Topshp.TRIANGLE_POINTING_UP_OVER_A_CIRCLE: "TOPMAR22",
    Topshp.UPRIGHT_CROSS_OVER_A_CIRCLE: "TOPMAR86",
    Topshp.RHOMBUS_OVER_A_CIRCLE: "TOPMAR14",
    Topshp.CIRCLE_OVER_A_TRIANGLE_POINTING_UP: "TOPMAR30",
    Topshp.OTHER_SHAPE: "TMARDEF1",
}


class Topmar(Layerable):
    def pre_tile_encode(self, feature, cx):
        assoc = list(feature.associated_layer_names)
        platform = RIGID if not assoc else FLOATING
        feature.props["_PTFM"] = platform
        feature.props["_ASOC"] = assoc
        shape = Topshp.of(feature.props)
        if platform == FLOATING:
            feature.point_symbol(_FLOATING.get(shape, "TMARDEF2"))
        else:
            feature.point_symbol(_RIGID.get(shape, "TMARDEF1"))

    def layers(self, b):
        return [
            b.point_layer_from_symbol(
                icon_offset=Offset.eval_eq("_PTFM", RIGID, eq=(0.0, 0.0), neq=(0.0, -8.0)),
            )
        ]
