"""Pipeline overhead (PIPOHD, code 85). Geometry: Line.

S-52 lookup: ``LS(SOLD,3,CHGRD)``, plus ``SY(RACNSP01)`` when radar conspicuous (CONRAD 1 or 3).
The ``clr`` text is drawn by ``clearance_label.ClearanceLabel``.
"""

from .prelude import *


class Pipohd(Layerable):
    def pre_tile_encode(self, feature, cx):
        if Conrad.of(feature.props) in (Conrad.RADAR_CONSPICUOUS, Conrad.RADAR_CONSPICUOUS_HAS_RADAR_REFLECTOR):
            feature.line_pattern("RACNSP01")

    def layers(self, b):
        return [
            b.line_layer_with_color(Color.CHGRD, width=2.0),
            b.line_layer_with_pattern(
                include_polygon_lines=False,
                symbol_placement=Placement.LINE_CENTER,
                icon_rotation_alignment=IconRotationAlignment.VIEWPORT,
                icon_allow_overlap=True,
            ),
        ]
