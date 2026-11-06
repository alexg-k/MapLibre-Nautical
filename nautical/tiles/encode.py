"""Feature props as they reach the tile: symbolized, filtered and tagged with the chart name."""

import json
from pathlib import Path

from ..symbology.feature import ChartFeature

ATTRIBUTES_FILE = Path(__file__).resolve().parent.parent / "symbology" / "data" / "s57attributes.json"

#: S-57 record bookkeeping that no style reads; dropped to keep tiles small.
BOOKKEEPING = {"RCID", "PRIM", "GRUP", "OBJL", "RVER", "AGEN", "FIDN", "FIDS", "FFPT_RIND", "LNAM_REFS"}


def enumerated_attributes(path=ATTRIBUTES_FILE):
    """The acronyms of the enumerated (``E``) S-57 attributes."""
    with open(path) as f:
        attributes = json.load(f)
    return {k for k, v in attributes.items() if v.get("Attributetype") == "E"}


def filter_props(props, enumerated):
    """njord's prop filter: drops blank strings, zero values of enumerated attributes and empty
    lists, in place."""
    for key in list(props):
        value = props[key]
        if isinstance(value, str):
            if not value.strip() or (value == "0" and key in enumerated):
                del props[key]
        elif isinstance(value, bool):
            continue
        elif isinstance(value, (int, float)):
            if value == 0 and key in enumerated:
                del props[key]
        elif isinstance(value, list):
            if not value:
                del props[key]


def topmar_associations(features_by_layer):
    """LNAM → the distinct layers of the features referencing it through ``LNAM_REFS``, for the
    chart's TOPMAR features (njord's ``topmar_assoc``)."""
    topmars = {f.props.get("LNAM") for f in features_by_layer.get("TOPMAR", []) if f.props.get("LNAM")}
    if not topmars:
        return {}
    by_lnam = {}
    for layer, features in features_by_layer.items():
        for f in features:
            for ref in f.props.get("LNAM_REFS") or []:
                if ref in topmars:
                    by_lnam.setdefault(ref, set()).add(layer)
    return {k: sorted(v) for k, v in by_lnam.items()}


def assign_sector_sheets(names, per_sheet):
    """Spreads the sector icon ``names`` over sheets of at most ``per_sheet`` icons:
    ``{name: sheet_index}``, sorted names in order."""
    names = sorted(set(names))
    per_sheet = max(1, per_sheet)
    return {name: i // per_sheet for i, name in enumerate(names)}


def sector_image_name(name, sheet, sheets):
    """The ``icon-image`` of a sector icon: the bare name when every icon fits the base sheet,
    else ``sectors<k>:<name>`` (MapLibre's multi-sprite form)."""
    if sheets <= 1:
        return name
    return f"sectors{sheet}:{name}"


class Symbolizer:
    """Runs a feature through the symbology and the prop filter."""

    def __init__(self, factory, enumerated=None, drop=BOOKKEEPING):
        self.factory = factory
        self.enumerated = enumerated if enumerated is not None else enumerated_attributes()
        self.drop = set(drop)
        self.sector_icons = set()

    def symbolize(self, layer, props, chart_name, assoc=()):
        feature = ChartFeature(layer=layer, props=dict(props), associated_layer_names=list(assoc))
        self.factory.pre_tile_encode(feature)
        out = feature.props
        for key in self.drop:
            out.pop(key, None)
        filter_props(out, self.enumerated)
        out["NAME"] = chart_name
        si = out.get("SI")
        if si:
            self.sector_icons.add(si)
        return out
