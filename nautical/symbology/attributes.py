"""S-57 attribute decoders: an enumerated attribute's ID to a named value.

``Watlev.of(props)`` reads a feature's attribute: a single-valued (``E``) attribute answers the
member or ``None`` (absent or unknown), a list (``L``) attribute answers the known members in
order, dropping unknown IDs.
"""

from enum import IntEnum, nonmember

from .colors import Color
from .props import int_value, int_values


class SingleAttribute(IntEnum):
    ATTRIBUTE = nonmember("")

    @classmethod
    def from_id(cls, id_):
        try:
            return cls(id_)
        except ValueError:
            return None

    @classmethod
    def of(cls, props):
        id_ = int_value(props, cls.ATTRIBUTE)
        return None if id_ is None else cls.from_id(id_)


class ListAttribute(IntEnum):
    ATTRIBUTE = nonmember("")

    @classmethod
    def from_id(cls, id_):
        try:
            return cls(id_)
        except ValueError:
            return None

    @classmethod
    def of(cls, props):
        return [m for m in (cls.from_id(i) for i in int_values(props, cls.ATTRIBUTE)) if m is not None]


class Bcnshp(SingleAttribute):
    ATTRIBUTE = nonmember("BCNSHP")
    STAKE_POLE_PERCH_POST = 1
    WHITY = 2
    BEACON_TOWER = 3
    LATTICE_BEACON = 4
    PILE_BEACON = 5
    CAIRN = 6
    BUOYANT_BEACON = 7


class Boyshp(SingleAttribute):
    ATTRIBUTE = nonmember("BOYSHP")
    CONICAL = 1
    CAN = 2
    SPHERICAL = 3
    PILLAR = 4
    SPAR = 5
    BARREL = 6
    SUPERBUOY = 7
    ICEBUOY = 8


class Catbrg(ListAttribute):
    ATTRIBUTE = nonmember("CATBRG")
    FIXED_BRIDGE = 1
    OPENING_BRIDGE = 2
    SWING_BRIDGE = 3
    LIFTING_BRIDGE = 4
    BASCULE_BRIDGE = 5
    PONTOON_BRIDGE = 6
    DRAW_BRIDGE = 7
    TRANSPORTER_BRIDGE = 8
    FOOTBRIDGE = 9
    VIADUCT = 10
    AQUEDUCT = 11
    SUSPENSION_BRIDGE = 12


class Catcam(SingleAttribute):
    ATTRIBUTE = nonmember("CATCAM")
    NORTH_CARDINAL_MARK = 1
    EAST_CARDINAL_MARK = 2
    SOUTH_CARDINAL_MARK = 3
    WEST_CARDINAL_MARK = 4


class Catdam(SingleAttribute):
    ATTRIBUTE = nonmember("CATDAM")
    WEIR = 1
    DAM = 2
    FLOOD_BARRAGE = 3


class Catfif(SingleAttribute):
    ATTRIBUTE = nonmember("CATFIF")
    FISHING_STAKE = 1
    FISH_TRAP = 2
    FISH_WEIR = 3
    TUNNY_NET = 4


class Catgat(SingleAttribute):
    ATTRIBUTE = nonmember("CATGAT")
    FLOOD_BARRAGE_GATE = 2
    CAISSON = 3
    LOCK_GATE = 4
    DYKE_GATE = 5


class Catlam(SingleAttribute):
    ATTRIBUTE = nonmember("CATLAM")
    PORT_HAND_LATERAL_MARK = 1
    STARBOARD_HAND_LATERAL_MARK = 2
    PREFERRED_CHANNEL_TO_STARBOARD_LATERAL_MARK = 3
    PREFERRED_CHANNEL_TO_PORT_LATERAL_MARK = 4


class Catlmk(ListAttribute):
    ATTRIBUTE = nonmember("CATLMK")
    CAIRN = 1
    CEMETERY = 2
    CHIMNEY = 3
    DISH_AERIAL = 4
    FLAGSTAFF_FLAGPOLE = 5
    FLARE_STACK = 6
    MAST = 7
    WINDSOCK = 8
    MONUMENT = 9
    COLUMN_PILLAR = 10
    MEMORIAL_PLAQUE = 11
    OBELISK = 12
    STATUE = 13
    CROSS = 14
    DOME = 15
    RADAR_SCANNER = 16
    TOWER = 17
    WINDMILL = 18
    WINDMOTOR = 19
    SPIRE_MINARET = 20


class Catlnd(ListAttribute):
    ATTRIBUTE = nonmember("CATLND")
    FEN = 1
    MARSH = 2
    MOOR_BOG = 3
    HEATHLAND = 4
    MOUNTAIN_RANGE = 5
    LOWLANDS = 6
    CANYON_LANDS = 7
    PADDY_FIELD = 8
    AGRICULTURAL_LAND = 9
    SAVANNA_GRASSLAND = 10
    PARKLAND = 11
    SWAMP = 12
    LANDSLIDE = 13
    LAVA_FLOW = 14
    SALT_PAN = 15
    MORAINE = 16
    CRATER = 17
    CAVE = 18
    ROCK_COLUMN_OR_PINNACLE = 19


class Catmor(SingleAttribute):
    ATTRIBUTE = nonmember("CATMOR")
    DOLPHIN = 1
    DEVIATION_DOLPHIN = 2
    BOLLARD = 3
    TIE_UP_WALL = 4
    POST_OR_PILE = 5
    CHAIN_WIRE_CABLE = 6
    MOORING_BUOY = 7

    def filter_eq(self):
        return ["==", "CATMOR", int(self)]

    def filter_not_eq(self):
        return ["!=", "CATMOR", int(self)]


class Catobs(SingleAttribute):
    ATTRIBUTE = nonmember("CATOBS")
    SNAG_STUMP = 1
    WELLHEAD = 2
    DIFFUSER = 3
    CRIB = 4
    FISH_HAVEN = 5
    FOUL_AREA = 6
    FOUL_GROUND = 7
    ICE_BOOM = 8
    GROUND_TACKLE = 9
    BOOM = 10


class Catpip(ListAttribute):
    ATTRIBUTE = nonmember("CATPIP")
    OUTFALL_PIPE = 2
    INTAKE_PIPE = 3
    SEWER = 4
    BUBBLER_SYSTEM = 5
    SUPPLY_PIPE = 6


class Catpra(SingleAttribute):
    ATTRIBUTE = nonmember("CATPRA")
    QUARRY = 1
    MINE = 2
    STOCKPILE = 3
    POWER_STATION_AREA = 4
    REFINERY_AREA = 5
    TIMBER_YARD = 6
    FACTORY_AREA = 7
    TANK_FARM = 8
    WIND_FARM = 9


class Catrea(ListAttribute):
    ATTRIBUTE = nonmember("CATREA")
    OFFSHORE_SAFETY_ZONE = 1
    NATURE_RESERVE = 4
    BIRD_SANCTUARY = 5
    GAME_PRESERVE = 6
    SEAL_SANCTUARY = 7
    DEGAUSSING_RANGE = 8
    MILITARY_AREA = 9
    HISTORIC_WRECK_AREA = 10
    NAVIGATIONAL_AID_SAFETY_ZONE = 12
    MINEFIELD = 14
    SWIMMING_AREA = 18
    WAITING_AREA = 19
    RESEARCH_AREA = 20
    DREDGING_AREA = 21
    FISH_SANCTUARY = 22
    ECOLOGICAL_RESERVE = 23
    NO_WAKE_AREA = 24
    SWINGING_AREA = 25


class Catsea(SingleAttribute):
    ATTRIBUTE = nonmember("CATSEA")
    GAT = 2
    BANK = 3
    DEEP = 4
    BAY = 5
    TRENCH = 6
    BASIN = 7
    MUD_FLATS = 8
    REEF = 9
    LEDGE = 10
    CANYON = 11
    NARROWS = 12
    SHOAL = 13
    KNOLL = 14
    RIDGE = 15
    SEAMOUNT = 16
    PINNACLE = 17
    ABYSSAL_PLAIN = 18
    PLATEAU = 19
    SPUR = 20
    SHELF = 21
    TROUGH = 22
    SADDLE = 23
    ABYSSAL_HILLS = 24
    APRON = 25
    ARCHIPELAGIC_APRON = 26
    BORDERLAND = 27
    CONTINENTAL_MARGIN = 28
    CONTINENTAL_RISE = 29
    ESCARPMENT = 30
    FAN = 31
    FRACTURE_ZONE = 32
    GAP = 33
    GUYOT = 34
    HILL = 35
    HOLE = 36
    LEVEE = 37
    MEDIAN_VALLEY = 38
    MOAT = 39
    MOUNTAINS = 40
    PEAK = 41
    PROVINCE = 42
    RISE = 43
    SEACHANNEL = 44
    SEAMOUNT_CHAIN = 45
    SHELF_EDGE = 46
    SILL = 47
    SLOPE = 48
    TERRACE = 49
    VALLEY = 50
    CANAL = 51
    LAKE = 52
    RIVER = 53


class Catsil(SingleAttribute):
    ATTRIBUTE = nonmember("CATSIL")
    SILO_IN_GENERAL = 1
    TANK_IN_GENERAL = 2
    GRAIN_ELEVATOR = 3
    WATER_TOWER = 4


class Catspm(ListAttribute):
    ATTRIBUTE = nonmember("CATSPM")
    FIRING_DANGER_AREA_MARK = 1
    TARGET_MARK = 2
    MARKER_SHIP_MARK = 3
    DEGAUSSING_RANGE_MARK = 4
    BARGE_MARK = 5
    CABLE_MARK = 6
    SPOIL_GROUND_MARK = 7
    OUTFALL_MARK = 8
    ODAS_OCEAN_DATA_ACQUISITION_SYSTEM = 9
    RECORDING_MARK = 10
    SEAPLANE_ANCHORAGE_MARK = 11
    RECREATION_ZONE_MARK = 12
    PRIVATE_MARK = 13
    MOORING_MARK = 14
    LANBY_LARGE_AUTOMATIC_NAVIGATIONAL_BUOY = 15
    LEADING_MARK = 16
    MEASURED_DISTANCE_MARK = 17
    NOTICE_MARK = 18
    TSS_MARK_TRAFFIC_SEPARATION_SCHEME = 19
    ANCHORING_PROHIBITED_MARK = 20
    BERTHING_PROHIBITED_MARK = 21
    OVERTAKING_PROHIBITED_MARK = 22
    TWO_WAY_TRAFFIC_PROHIBITED_MARK = 23
    REDUCED_WAKE_MARK = 24
    SPEED_LIMIT_MARK = 25
    STOP_MARK = 26
    GENERAL_WARNING_MARK = 27
    SOUND_SHIPS_SIREN_MARK = 28
    RESTRICTED_VERTICAL_CLEARENCE_MARK = 29
    MAXIMUM_VESSELS_DRAUGHT_MARK = 30
    RESTRICTED_HORIZONTAL_CLEARANCE_MARK = 31
    STRONG_CURRENT_WARNING_MARK = 32
    BERTHING_PERMITTED_MARK = 33
    OVERHEAD_POWER_CABLE_MARK = 34
    CHANNEL_EDGE_GRADIENT_MARK = 35
    TELEPHONE_MARK = 36
    FERRY_CROSSING_MARK = 37
    PIPLINE_MARK = 39
    ANCHORAGE_MARK = 40
    CLEARING_MARK = 41
    CONTROL_MARK = 42
    DIVING_MARK = 43
    REFUGE_BEACON = 44
    FOUL_GROUND_MARK = 45
    YACHTING_MARK = 46
    HELIPORT_MARK = 47
    GPS_MARK = 48
    SEAPLANE_LANDING_MARK = 49
    ENTRY_PROHIBITED_MARK = 50
    WORK_IN_PROGRESS_MARK = 51
    MARK_WITH_UNKNOWN_PURPOSE = 52


class Cattrk(SingleAttribute):
    ATTRIBUTE = nonmember("CATTRK")
    BASED_ON_A_SYSTEM_OF_MARKS = 1
    NOT_BASED_ON_A_SYSTEM_OF_MARKS = 2


class Catwrk(SingleAttribute):
    ATTRIBUTE = nonmember("CATWRK")
    NON_DANGEROUS_WRECK = 1
    DANGEROUS_WRECK = 2
    DISTRIBUTED_REMAINS_OF_WRECK = 3
    WRECK_SHOWING_MAST_MASTS = 4
    WRECK_SHOWING_ANY_PORTION_OF_HULL_OR_SUPERSTRUCTURE = 5


class Colour(ListAttribute):
    """The S-57 ``COLOUR`` list attribute; :meth:`first` is the one most rules read."""

    ATTRIBUTE = nonmember("COLOUR")
    WHITE = 1
    BLACK = 2
    RED = 3
    GREEN = 4
    BLUE = 5
    YELLOW = 6
    GREY = 7
    BROWN = 8
    AMBER = 9
    VIOLET = 10
    ORANGE = 11
    MAGENTA = 12
    PINK = 13

    @classmethod
    def first(cls, props):
        values = cls.of(props)
        return values[0] if values else None


class Conrad(SingleAttribute):
    ATTRIBUTE = nonmember("CONRAD")
    RADAR_CONSPICUOUS = 1
    NOT_RADAR_CONSPICUOUS = 2
    RADAR_CONSPICUOUS_HAS_RADAR_REFLECTOR = 3


class Convis(SingleAttribute):
    ATTRIBUTE = nonmember("CONVIS")
    VISUAL_CONSPICUOUS = 1
    NOT_VISUAL_CONSPICUOUS = 2


class Functn(ListAttribute):
    ATTRIBUTE = nonmember("FUNCTN")
    HARBOUR_MASTERS_OFFICE = 2
    CUSTOM_OFFICE = 3
    HEALTH_OFFICE = 4
    HOSPITAL = 5
    POST_OFFICE = 6
    HOTEL = 7
    RAILWAY_STATION = 8
    POLICE_STATION = 9
    WATER_POLICE_STATION = 10
    PILOT_OFFICE = 11
    PILOT_LOOKOUT = 12
    BANK_OFFICE = 13
    HEADQUARTERS_FOR_DISTRICT_CONTROL = 14
    TRANSIT_SHED_WAREHOUSE = 15
    FACTORY = 16
    POWER_STATION = 17
    ADMINISTRATIVE = 18
    EDUCATIONAL_FACILITY = 19
    CHURCH = 20
    CHAPEL = 21
    TEMPLE = 22
    PAGODA = 23
    SHINTO_SHRINE = 24
    BUDDHIST_TEMPLE = 25
    MOSQUE = 26
    MARABOUT = 27
    LOOKOUT = 28
    COMMUNICATION = 29
    TELEVISION = 30
    RADIO = 31
    RADAR = 32
    LIGHT_SUPPORT = 33
    MICROWAVE = 34
    COOLING = 35
    OBSERVATION = 36
    TIMEBALL = 37
    CLOCK = 38
    CONTROL = 39
    AIRSHIP_MOORING = 40
    STADIUM = 41
    BUS_STATION = 42


class Prodct(ListAttribute):
    ATTRIBUTE = nonmember("PRODCT")
    OIL = 1
    GAS = 2
    WATER = 3
    STONE = 4
    COAL = 5
    ORE = 6
    CHEMICALS = 7
    DRINKING_WATER = 8
    MILK = 9
    BAUXITE = 10
    COKE = 11
    IRON_INGOTS = 12
    SALT = 13
    SAND = 14
    TIMBER = 15
    SAWDUST_WOOD_CHIPS = 16
    SCRAP_METAL = 17
    LIQUIFIED_NATURAL_GAS = 18
    LIQUIFIED_PETROLEUM_GAS = 19
    WINE = 20
    CEMENT = 21
    GRAIN = 22


class Quasou(ListAttribute):
    ATTRIBUTE = nonmember("QUASOU")
    DEPTH_KNOWN = 1
    DEPTH_UNKNOWN = 2
    DOUBTFUL_SOUNDING = 3
    UNRELIABLE_SOUNDING = 4
    NO_BOTTOM_FOUND_AT_VALUE_SHOWN = 5
    LEAST_DEPTH_KNOWN = 6
    LEAST_DEPTH_UNKNOWN_SAFE_CLEARANCE_AT_VALUE_SHOWN = 7
    VALUE_REPORTED_NOT_SURVEYED = 8
    VALUE_REPORTED_NOT_CONFIRMED = 9
    MAINTAINED_DEPTH = 10
    NOT_REGULARLY_MAINTAINED = 11


class Restrn(ListAttribute):
    ATTRIBUTE = nonmember("RESTRN")
    ANCHORING_PROHIBITED = 1
    ANCHORING_RESTRICTED = 2
    FISHING_PROHIBITED = 3
    FISHING_RESTRICTED = 4
    TRAWLING_PROHIBITED = 5
    TRAWLING_RESTRICTED = 6
    ENTRY_PROHIBITED = 7
    ENTRY_RESTRICTED = 8
    DREDGING_PROHIBITED = 9
    DREDGING_RESTRICTED = 10
    DIVING_PROHIBITED = 11
    DIVING_RESTRICTED = 12
    NO_WAKE = 13
    AREA_TO_BE_AVOIDED = 14
    CONSTRUCTION_PROHIBITED = 15


class Topshp(SingleAttribute):
    ATTRIBUTE = nonmember("TOPSHP")
    CONE_POINT_UP = 1
    CONE_POINT_DOWN = 2
    SPHERE = 3
    TWO_SPHERE = 4
    CYLINDER_CAN = 5
    BOARD = 6
    X_SHAPE = 7
    UPRIGHT_CROSS = 8
    CUBE_POINT_UP = 9
    TWO_CONES_POINT_TO_POINT = 10
    TWO_CONES_BASE_TO_BASE = 11
    RHOMBUS_DIAMOND = 12
    TWO_CONES_POINTS_UPWARD = 13
    TWO_CONES_POINTS_DOWNWARD = 14
    BESOM_POINT_UP_BROOM_OR_PERCH = 15
    BESOM_POINT_DOWN_BROOM_OR_PERCH = 16
    FLAG = 17
    SPHERE_OVER_RHOMBUS = 18
    SQUARE = 19
    RECTANGLE_HORIZONTAL = 20
    RECTANGLE_VERTICAL = 21
    TRAPEZIUM_UP = 22
    TRAPEZIUM_DOWN = 23
    TRIANGLE_POINT_UP = 24
    TRIANGLE_POINT_DOWN = 25
    CIRCLE = 26
    TWO_UPRIGHT_CROSSES_ONE_OVER_THE_OTHER = 27
    T_SHAPE = 28
    TRIANGLE_POINTING_UP_OVER_A_CIRCLE = 29
    UPRIGHT_CROSS_OVER_A_CIRCLE = 30
    RHOMBUS_OVER_A_CIRCLE = 31
    CIRCLE_OVER_A_TRIANGLE_POINTING_UP = 32
    OTHER_SHAPE = 33


class Trafic(SingleAttribute):
    ATTRIBUTE = nonmember("TRAFIC")
    INBOUND = 1
    OUTBOUND = 2
    ONE_WAY = 3
    TWO_WAY = 4


class Watlev(SingleAttribute):
    ATTRIBUTE = nonmember("WATLEV")
    PARTLY_SUBMERGED_AT_HIGH_WATER = 1
    ALWAYS_DRY = 2
    ALWAYS_UNDER_WATER_SUBMERGED = 3
    COVERS_AND_UNCOVERS = 4
    AWASH = 5
    SUBJECT_TO_INUNDATION_OR_FLOODING = 6
    FLOATING = 7


class DepthColor(IntEnum):
    """The depth-area colour bands and their S-52 colour tokens."""

    DEEP_WATER = 1
    MEDIUM_DEPTH = 2
    SAFETY_DEPTH = 3
    VERY_SHALLOW = 4
    COVERS_UNCOVERS = 5

    def color(self):
        return {
            DepthColor.DEEP_WATER: Color.DEPDW,
            DepthColor.MEDIUM_DEPTH: Color.DEPMD,
            DepthColor.SAFETY_DEPTH: Color.DEPMS,
            DepthColor.VERY_SHALLOW: Color.DEPVS,
            DepthColor.COVERS_UNCOVERS: Color.DEPIT,
        }[self]
