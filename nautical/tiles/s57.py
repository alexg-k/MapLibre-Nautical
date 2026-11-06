"""S-57 cell reading through GDAL, shaped like njord's ingest.

A :class:`Cell` is one ``.000`` file (GDAL applies the ``.001``... updates beside it). Its
:class:`Chart` row carries the compilation scale, its display zoom and the ``M_COVR`` coverage;
its :class:`Feature` rows carry every set field as GDAL maps it (lists as lists of strings),
plus ``METERS`` on soundings and ``MINZ``/``MAXZ`` next to ``SCAMIN``/``SCAMAX``.
"""

from dataclasses import dataclass, field
from pathlib import Path

from osgeo import gdal, ogr
from shapely import wkb
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import unary_union
from shapely.validation import make_valid

from .tile_system import scale_to_zoom_int

#: ``OGR_S57_OPTIONS``: no spatial primitives, LNAM references, updates applied, one sounding per
#: feature, strings recoded by the cell's lexical level.
S57_OPTIONS = "RETURN_PRIMITIVES=OFF,RETURN_LINKAGES=OFF,LNAM_REFS=ON,UPDATES=APPLY,SPLIT_MULTIPOINT=ON,RECODE_BY_DSSI=ON"

#: The layers never tiled: the DSID metadata record and the spatial primitive layers.
EXCLUDED_LAYERS = {"DSID", "IsolatedNode", "ConnectedNode", "Edge", "Face"}

gdal.UseExceptions()
ogr.UseExceptions()


@dataclass
class Feature:
    layer: str
    props: dict
    geometry: object  # shapely geometry, or None


@dataclass
class Chart:
    name: str
    file_name: str
    path: str
    scale: int
    zoom: int
    coverage: object  # shapely (Multi)Polygon
    dsid: dict
    features: dict = field(default_factory=dict)  # layer -> [Feature]

    @property
    def layers(self):
        return list(self.features.keys())


class Cell:
    def __init__(self, path):
        self.path = Path(path)
        gdal.SetConfigOption("OGR_S57_OPTIONS", S57_OPTIONS)
        self.ds = ogr.Open(str(self.path), 0)
        if self.ds is None:
            raise RuntimeError(f"cannot open {self.path}")

    def layer_names(self):
        return [self.ds.GetLayerByIndex(i).GetName() for i in range(self.ds.GetLayerCount())]

    def read_layer(self, name):
        layer = self.ds.GetLayerByName(name)
        if layer is None:
            return []
        layer.ResetReading()
        is_sounding = name == "SOUNDG"
        out = []
        for f in layer:
            out.append(_read_feature(f, name, is_sounding))
        return out

    def read_chart(self):
        """The chart row and all of its features."""
        chart = self.read_metadata()
        self.read_features(chart)
        return chart

    def read_features(self, chart):
        """Fills ``chart.features`` with every tiled layer of the cell."""
        for layer_name in self.layer_names():
            if layer_name in EXCLUDED_LAYERS:
                continue
            features = self.read_layer(layer_name)
            if features:
                chart.features[layer_name] = features
        return chart

    def read_metadata(self):
        """The chart row alone: name, scale, zoom and coverage."""
        dsid = self.read_layer("DSID")
        if not dsid:
            raise RuntimeError(f"{self.path}: DSID is missing")
        props = dsid[0].props
        scale = _int(props.get("DSPM_CSCL"))
        if scale is None:
            raise RuntimeError(f"{self.path}: DSID DSPM_CSCL is missing")

        polygons = []
        for f in self.read_layer("M_COVR"):
            if _int(f.props.get("CATCOV")) != 1 or f.geometry is None:
                continue
            g = f.geometry
            if isinstance(g, Polygon):
                polygons.append(g)
            elif isinstance(g, MultiPolygon):
                polygons.extend(g.geoms)
        if not polygons:
            raise RuntimeError(f"{self.path}: M_COVR is missing")
        coverage = unary_union(polygons)
        if coverage.geom_type == "Polygon":
            coverage = MultiPolygon([coverage])
        minx, miny, maxx, maxy = coverage.bounds
        center_lat = (miny + maxy) / 2.0

        name = props.get("DSID_DSNM") or self.path.name
        return Chart(
            name=str(name),
            file_name=self.path.name,
            path=str(self.path),
            scale=scale,
            zoom=scale_to_zoom_int(float(scale), center_lat),
            coverage=coverage,
            dsid=props,
        )


def _read_feature(f, layer_name, is_sounding):
    geom_ref = f.GetGeometryRef()
    geometry = None
    z = None
    if geom_ref is not None:
        if is_sounding and geom_ref.GetCoordinateDimension() >= 3 and geom_ref.GetPointCount() > 0:
            z = geom_ref.GetZ(0)
        try:
            geometry = wkb.loads(bytes(geom_ref.ExportToIsoWkb()))
        except Exception:  # noqa: BLE001
            geometry = None
        if geometry is not None:
            geometry = _repair(geometry)

    props = {}
    if is_sounding and z is not None:
        props["METERS"] = float(z)
    latitude = None
    if geometry is not None and not geometry.is_empty:
        minx, miny, maxx, maxy = geometry.bounds
        latitude = (miny + maxy) / 2.0

    defn = f.GetDefnRef()
    for i in range(defn.GetFieldCount()):
        if not f.IsFieldSetAndNotNull(i):
            continue
        fd = defn.GetFieldDefn(i)
        key = fd.GetName()
        value = _field_value(f, i, fd.GetType())
        if value is None:
            continue
        if key in ("SCAMIN", "SCAMAX"):
            scale = _int(value)
            if scale is not None:
                zoom = scale_to_zoom_int(float(scale), latitude if latitude is not None else 0.0)
                props["MINZ" if key == "SCAMIN" else "MAXZ"] = zoom
        props[key] = value
    return Feature(layer_name, props, geometry)


def _field_value(f, i, ftype):
    if ftype == ogr.OFTInteger:
        return f.GetFieldAsInteger(i)
    if ftype == ogr.OFTInteger64:
        return f.GetFieldAsInteger64(i)
    if ftype == ogr.OFTReal:
        return f.GetFieldAsDouble(i)
    if ftype == ogr.OFTString:
        return f.GetFieldAsString(i)
    if ftype == ogr.OFTStringList:
        return list(f.GetFieldAsStringList(i) or [])
    if ftype == ogr.OFTIntegerList:
        return list(f.GetFieldAsIntegerList(i) or [])
    if ftype == ogr.OFTInteger64List:
        return list(f.GetFieldAsInteger64List(i) or [])
    if ftype == ogr.OFTRealList:
        return list(f.GetFieldAsDoubleList(i) or [])
    if ftype in (ogr.OFTDate, ogr.OFTDateTime, ogr.OFTTime):
        return f.GetFieldAsString(i)
    return f.GetFieldAsString(i)


def _repair(geometry):
    """GDAL's ``makeValid`` equivalent: a repaired geometry of the input's dimension, or None."""
    if geometry.is_valid:
        return geometry
    fixed = make_valid(geometry)
    dim = _dimension(geometry)
    parts = [g for g in _flatten(fixed) if _dimension(g) == dim and not g.is_empty]
    if not parts:
        return None
    if len(parts) == 1:
        return parts[0]
    return unary_union(parts)


def _flatten(geometry):
    if geometry.geom_type == "GeometryCollection":
        for g in geometry.geoms:
            yield from _flatten(g)
    else:
        yield geometry


def _dimension(geometry):
    t = geometry.geom_type
    if t in ("Polygon", "MultiPolygon"):
        return 2
    if t in ("LineString", "MultiLineString", "LinearRing"):
        return 1
    return 0


def _int(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, str):
        try:
            return int(v)
        except ValueError:
            return None
    return None


def find_cells(root):
    """Every ``.000`` file under ``root``, sorted."""
    root = Path(root)
    return sorted(p for p in root.rglob("*.000") if p.is_file())


def chart_summary(chart):
    return {
        "name": chart.name,
        "file": chart.file_name,
        "scale": chart.scale,
        "zoom": chart.zoom,
        "bounds": list(chart.coverage.bounds),
        "layers": {k: len(v) for k, v in chart.features.items()},
    }
