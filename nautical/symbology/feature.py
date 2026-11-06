"""The chart feature the layerables symbolize, and its symbology prop setters."""

from dataclasses import dataclass, field


@dataclass
class ChartFeature:
    """An S-57 feature's props, as GDAL maps them, that a layerable enriches in place.

    ``associated_layer_names`` are the object classes of the features that share this feature's
    position (through ``LNAM_REFS``); only TOPMAR reads it, to tell a floating platform (a buoy)
    from a rigid one (a beacon).
    """

    layer: str
    props: dict = field(default_factory=dict)
    geometry_type: str | None = None
    associated_layer_names: list = field(default_factory=list)

    def exclude_area_point_symbol(self):
        """Sets ``EA``, which keeps ``area_layer_with_point_symbol`` off the area."""
        self.props["EA"] = True

    def point_symbol(self, symbol):
        self.props["SY"] = str(symbol)

    def point_symbol_n(self, symbol, num):
        self.props[f"SY{num}"] = str(symbol)

    def area_pattern(self, pattern):
        self.props["AP"] = str(pattern)

    def area_color(self, color):
        self.props["AC"] = str(color)

    def line_pattern(self, pattern):
        self.props["LP"] = str(pattern)

    def line_color(self, color):
        self.props["LC"] = str(color)
