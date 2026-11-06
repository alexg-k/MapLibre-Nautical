"""The registry of layerables in draw order."""

import importlib

from .colors import ColorLibrary
from .layerable import Context, LayerBuilder, SymbologyConfig

LAYERS_PACKAGE = __name__.rsplit(".", 1)[0] + ".layers"


class Entry:
    """A layerable under its key.

    The key is the S-57 object class for most entries, or a custom key such as the lower-case
    inland twins; :meth:`LayerFactory.pre_tile_encode` dispatches by matching it to the feature's
    layer, and helper-made layer ids start with it. The layerable is built on first use from
    ``module`` / ``class_name`` (or a ready instance / factory callable).
    """

    def __init__(self, key, module=None, class_name=None, instance=None, factory=None, base=False, **kwargs):
        self.key = key
        #: A Natural Earth base-map layer, drawn from the base source when the factory has one.
        self.base = base
        self._module = module
        self._class_name = class_name
        self._instance = instance
        self._factory = factory
        self._kwargs = kwargs

    @property
    def layerable(self):
        if self._instance is None:
            if self._factory is not None:
                self._instance = self._factory()
            else:
                module = importlib.import_module(f"{LAYERS_PACKAGE}.{self._module}")
                self._instance = getattr(module, self._class_name)(**self._kwargs)
        return self._instance

    @property
    def source_layer(self):
        return self.layerable.source_layer or self.key

    def layers(self, cx, depth, theme, source):
        b = LayerBuilder(cx, self.key, self.source_layer, depth, theme, source)
        return self.layerable.layers(b)


def _e(key, module=None, class_name=None, **kwargs):
    if module is None:
        module = key.lower()
    if class_name is None:
        class_name = key.capitalize()
    return Entry(key, module, class_name, **kwargs)


def base_layers():
    """The Natural Earth layers under the charts."""
    return [
        Entry("BACKGROUND", "background", "Background"),
        Entry("ocean", "base", "Ocean", base=True),
        Entry("bathymetry", "base", "Bathymetry", base=True),
        Entry("glaciated_areas", "base", "GlaciatedAreas", base=True),
        Entry("reefs", "base", "Reefs", base=True),
        Entry("LAND", "base", "Land", base=True),
        Entry("playas", "base", "Playas", base=True),
        Entry("RIVERSLAKECENTERLINES", "base", "RiversLakeCenterlines", base=True),
        Entry("LAKES", "base", "Lakes", base=True),
        Entry("antarctic_ice_shelves_polys", "base", "AntarcticIceShelves", base=True),
        Entry("MINORISLANDS", "base", "MinorIslands", base=True),
        Entry("coastline", "base", "Coastline", base=True),
    ]


def standard_layers():
    """The S-57 object classes drawn on every chart."""
    e = [
        # land / base layers
        _e("DEPARE"),
        _e("LNDARE"),
        _e("SLOGRD"),
        _e("LAKARE"),
        _e("LAKSHR"),
        _e("BUISGL"),
        _e("BUAARE"),
        Entry("OBSTRNAREA", "obstrn", "ObstrnArea"),
        _e("SLCONS"),
        _e("LNDRGN"),
        _e("DRGARE"),
        _e("ICEARE"),
        _e("COALNE"),
        _e("CAUSWY"),
        _e("CANALS"),
        _e("RIVERS"),
        _e("AIRARE"),
        _e("RUNWAY"),
        _e("DYKCON"),
        _e("SILTNK"),
        _e("CTRPNT"),
        _e("LNDELV"),
        _e("CGUSTA"),
        # water boundary layers
        _e("UNSARE"),
        _e("LOKBSN"),
        _e("TSSLPT"),
        _e("TSSBND"),
        _e("TSELNE"),
        _e("TWRTPT"),
        _e("TSEZNE"),
        _e("TCTLPT"),
        _e("TSSCRS"),
        _e("TSSRON"),
        _e("DWRTPT"),
        _e("DWRTCL"),
        _e("MIPARE"),
        _e("LOGPON"),
        _e("ICNARE"),
        _e("ACHBRT"),
        _e("ACHARE"),
        _e("CBLARE"),
        _e("CBLSUB"),
        _e("CBLOHD"),
        _e("PIPOHD"),
        _e("RESARE"),
        _e("CTNARE"),
        _e("CTSARE"),
        _e("WEDKLP"),
        _e("FAIRWY"),
        _e("FNCLNE"),
        _e("FERYRT"),
        _e("FSHGRD"),
        _e("FSHFAC"),
        _e("SPLARE"),
        _e("MARCUL"),
        _e("FORSTC"),
        _e("DMPGRD"),
        _e("PIPARE"),
        _e("SUBTLN"),
        _e("ISTZNE"),
        _e("RECTRC"),
        _e("RCTLPT"),
        _e("NAVLNE"),
        _e("RCRTCL"),
        _e("RADLNE"),
        _e("RADRNG"),
        _e("RADRFL"),
        _e("RADSTA"),
        _e("RTPBCN"),
        _e("RDOCAL"),
        _e("DISMAR"),
        _e("SWPARE"),
        _e("TUNNEL"),
        _e("CHKPNT"),
        _e("PRCARE"),
        _e("SNDWAV"),
        _e("SBDARE"),
        _e("TIDEWY"),
        _e("BERTHS"),
        # obstructions
        _e("HULKES"),
        _e("PONTON"),
        _e("MORFAC"),
        _e("BRIDGE"),
        _e("CONVYR"),
        _e("DAMCON"),
        _e("DOCARE"),
        _e("FLODOC"),
        _e("GATCON"),
        _e("OFSPLF"),
        _e("OILBAR"),
        _e("CRANES"),
        _e("PYLONS"),
        _e("DAYMAR"),
        _e("PILBOP"),
        _e("PILPNT"),
        _e("OBSTRN"),
        _e("WRECKS"),
        _e("UWTROC"),
        _e("OSPARE"),
        _e("SISTAT"),
        _e("SISTAW"),
        # low pri labels
        Entry("LNDARELABEL", "lndare_label", "LndareLabel"),
        _e("SEAARE"),
        # buoys and markers
        _e("NEWOBJ"),
        _e("FOGSIG"),
        _e("BCNCAR"),
        _e("BCNISD"),
        _e("BCNLAT"),
        _e("BCNSAW"),
        _e("BCNSPP"),
        _e("BOYCAR"),
        _e("BOYINB"),
        _e("BOYISD"),
        _e("BOYLAT"),
        _e("BOYSAW"),
        _e("BOYSPP"),
        _e("LNDMRK"),
        _e("ACHPNT"),
        _e("RETRFL"),
        _e("TOPMAR"),
        # high pri labels
        _e("SOUNDG"),
    ]
    # clearance text is S-52 display-base, so it goes above the symbology of the objects it
    # annotates - see clearance_label
    for cls in ["BRIDGE", "CBLOHD", "PIPOHD", "CONVYR", "CRANES", "GATCON"]:
        e.append(Entry(f"{cls}_CLEARANCE", "clearance_label", "ClearanceLabel", object_class=cls))
    e.extend(
        [
            _e("CURENT"),
            # lights
            _e("LITFLT"),
            _e("LITVES"),
            _e("LIGHTS"),
            _e("PRDARE"),
        ]
    )
    # S-52 text group 21, names for position reporting - after every mark symbol and the light
    # descriptions so the names win placement - see name_label
    from .layers.name_label import NameLabel

    for label in NameLabel.all():
        e.append(Entry(label.key, instance=label))
    return e


def inland_layers():
    """Inland ENC classes, and the inland twins of three standard classes under lower-case keys."""
    return [
        _e("lokbsn", "lokbsn", "Lokbsn"),
        _e("HRBBSN"),
        _e("NOTMRK"),
        _e("LKBSPT"),
        _e("EXCNST"),
        _e("achbrt", "achbrt", "Achbrt"),
        _e("achare", "achare", "Achare"),
    ]


def extra_layers():
    """Layers outside S-57: the ``PLY`` coverage outline."""
    return [_e("PLY")]


class LayerFactory:
    """Every registered layerable in draw order, with the config and colours the rules read."""

    def __init__(self, config=None, colors=None, source="src_senc", base_source=None):
        """``source`` is the chart tile source's id, ``base_source`` the Natural Earth base map's
        (the chart source when None, as njord serves both from one source)."""
        config = config or SymbologyConfig()
        colors = colors or ColorLibrary.load()
        self.cx = Context(config, colors)
        self.source = source
        self.base_source = base_source or source
        self.entries = base_layers() + standard_layers() + inland_layers() + extra_layers()
        if config.debug_tile:
            self.entries.append(_e("DEBUG"))
        keys = [e.key for e in self.entries]
        duplicates = {k for k in keys if keys.count(k) > 1}
        if duplicates:
            raise ValueError(f"duplicate layerable keys {sorted(duplicates)}")
        self._by_key = {e.key: e for e in self.entries}

    def get(self, key):
        return self._by_key.get(key)

    def layers(self, depth, theme):
        """The complete layer list of one style."""
        return [
            layer
            for e in self.entries
            for layer in e.layers(self.cx, depth, theme, self.base_source if e.base else self.source)
        ]

    def pre_tile_encode(self, feature):
        """Runs the layerable registered under the feature's layer, if any."""
        e = self.get(feature.layer)
        if e is not None:
            e.layerable.pre_tile_encode(feature, self.cx)
