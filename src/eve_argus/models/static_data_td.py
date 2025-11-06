"""Auto-generated TypedDict definitions for SDE build 3081406.

At the moment these definitions only consider top-level keys and their types.
"""

from typing import NotRequired, TypedDict

BUILD_NUMBER = 3081406

# ------------------------------------------------------------------------------
# Sub-level TypedDict definitions.
# ------------------------------------------------------------------------------


class LocalizedStringDict(TypedDict):
    """TypeDict definition for LocalizedStringDict.

    Source info: SDE file: translationLanguages.jsonl, build: 3081406.
    """

    en: str
    de: str
    fr: str
    ja: str
    zh: str
    ru: str
    ko: str
    es: str


# ------------------------------------------------------------------------------
# File level TypedDict definitions.
# ------------------------------------------------------------------------------


class AgentsInSpaceDict(TypedDict):
    """TypeDict definition for AgentsInSpaceDict.

    Total entries analyzed: 360.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: agentsInSpace.jsonl, build: 3081406
    Key Info:
    {'count': 360,
     'key_info': {'_key': {'int': 360},
                  'dungeonID': {'int': 360},
                  'solarSystemID': {'int': 360},
                  'spawnPointID': {'int': 360},
                  'typeID': {'int': 360}}}.
    """

    _key: int
    dungeonID: int
    solarSystemID: int
    spawnPointID: int
    typeID: int


class AgentTypesDict(TypedDict):
    """TypeDict definition for AgentTypesDict.

    Total entries analyzed: 13.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: agentTypes.jsonl, build: 3081406
    Key Info:
    {'count': 13, 'key_info': {'_key': {'int': 13}, 'name': {'str': 13}}}.
    """

    _key: int
    name: str


class AncestriesDict(TypedDict):
    """TypeDict definition for AncestriesDict.

    Total entries analyzed: 43.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: ancestries.jsonl, build: 3081406
    Key Info:
    {'count': 43,
     'key_info': {'_key': {'int': 43},
                  'bloodlineID': {'int': 43},
                  'charisma': {'int': 43},
                  'description': {'dict': 43},
                  'iconID': {'int': 35},
                  'intelligence': {'int': 43},
                  'memory': {'int': 43},
                  'name': {'dict': 43},
                  'perception': {'int': 43},
                  'shortDescription': {'str': 42},
                  'willpower': {'int': 43}}}.
    """

    _key: int
    bloodlineID: int
    charisma: int
    description: LocalizedStringDict
    iconID: NotRequired[int]
    intelligence: int
    memory: int
    name: LocalizedStringDict
    perception: int
    shortDescription: NotRequired[str]
    willpower: int


class BloodlinesDict(TypedDict):
    """TypeDict definition for BloodlinesDict.

    Total entries analyzed: 18.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: bloodlines.jsonl, build: 3081406
    Key Info:
    {'count': 18,
     'key_info': {'_key': {'int': 18},
                  'charisma': {'int': 18},
                  'corporationID': {'int': 18},
                  'description': {'dict': 18},
                  'iconID': {'int': 15},
                  'intelligence': {'int': 18},
                  'memory': {'int': 18},
                  'name': {'dict': 18},
                  'perception': {'int': 18},
                  'raceID': {'int': 18},
                  'willpower': {'int': 18}}}.
    """

    _key: int
    charisma: int
    corporationID: int
    description: LocalizedStringDict
    iconID: NotRequired[int]
    intelligence: int
    memory: int
    name: LocalizedStringDict
    perception: int
    raceID: int
    willpower: int


class BlueprintsDict(TypedDict):
    """TypeDict definition for BlueprintsDict.

    Total entries analyzed: 5031.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: blueprints.jsonl, build: 3081406
    Key Info:
    {'count': 5031,
     'key_info': {'_key': {'int': 5031},
                  'activities': {'dict': 5031},
                  'blueprintTypeID': {'int': 5031},
                  'maxProductionLimit': {'int': 5031}}}.
    """

    _key: int
    activities: dict
    blueprintTypeID: int
    maxProductionLimit: int


class CategoriesDict(TypedDict):
    """TypeDict definition for CategoriesDict.

    Total entries analyzed: 47.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: categories.jsonl, build: 3081406
    Key Info:
    {'count': 47,
     'key_info': {'_key': {'int': 47},
                  'name': {'dict': 47},
                  'published': {'bool': 47},
                  'iconID': {'int': 13}}}.
    """

    _key: int
    name: LocalizedStringDict
    published: bool
    iconID: NotRequired[int]


class CertificatesDict(TypedDict):
    """TypeDict definition for CertificatesDict.

    Total entries analyzed: 134.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: certificates.jsonl, build: 3081406
    Key Info:
    {'count': 134,
     'key_info': {'_key': {'int': 134},
                  'description': {'dict': 134},
                  'groupID': {'int': 134},
                  'name': {'dict': 134},
                  'recommendedFor': {'list': 79},
                  'skillTypes': {'list': 134}}}.
    """

    _key: int
    description: LocalizedStringDict
    groupID: int
    name: LocalizedStringDict
    recommendedFor: NotRequired[list]
    skillTypes: list


class CharacterAttributesDict(TypedDict):
    """TypeDict definition for CharacterAttributesDict.

    Total entries analyzed: 5.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: characterAttributes.jsonl, build: 3081406
    Key Info:
    {'count': 5,
     'key_info': {'_key': {'int': 5},
                  'description': {'str': 5},
                  'iconID': {'int': 5},
                  'name': {'dict': 5},
                  'notes': {'str': 5},
                  'shortDescription': {'str': 5}}}.
    """

    _key: int
    description: str
    iconID: int
    name: LocalizedStringDict
    notes: str
    shortDescription: str


class ContrabandTypesDict(TypedDict):
    """TypeDict definition for ContrabandTypesDict.

    Total entries analyzed: 8.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: contrabandTypes.jsonl, build: 3081406
    Key Info:
    {'count': 8, 'key_info': {'_key': {'int': 8}, 'factions': {'list': 8}}}.
    """

    _key: int
    factions: list


class ControlTowerResourcesDict(TypedDict):
    """TypeDict definition for ControlTowerResourcesDict.

    Total entries analyzed: 44.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: controlTowerResources.jsonl, build: 3081406
    Key Info:
    {'count': 44, 'key_info': {'_key': {'int': 44}, 'resources': {'list': 44}}}.
    """

    _key: int
    resources: list


class CorporationActivitiesDict(TypedDict):
    """TypeDict definition for CorporationActivitiesDict.

    Total entries analyzed: 20.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: corporationActivities.jsonl, build: 3081406
    Key Info:
    {'count': 20, 'key_info': {'_key': {'int': 20}, 'name': {'dict': 20}}}.
    """

    _key: int
    name: LocalizedStringDict


class DebuffCollectionsDict(TypedDict):
    """TypeDict definition for DebuffCollectionsDict.

    Total entries analyzed: 152.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: dbuffCollections.jsonl, build: 3081406
    Key Info:
    {'count': 152,
     'key_info': {'_key': {'int': 152},
                  'aggregateMode': {'str': 152},
                  'developerDescription': {'str': 152},
                  'itemModifiers': {'list': 97},
                  'locationGroupModifiers': {'list': 9},
                  'locationModifiers': {'list': 5},
                  'locationRequiredSkillModifiers': {'list': 49},
                  'operationName': {'str': 152},
                  'showOutputValueInUI': {'str': 152},
                  'displayName': {'dict': 144}}}.
    """

    _key: int
    aggregateMode: str
    developerDescription: str
    itemModifiers: NotRequired[list]
    locationGroupModifiers: NotRequired[list]
    locationModifiers: NotRequired[list]
    locationRequiredSkillModifiers: NotRequired[list]
    operationName: str
    showOutputValueInUI: str
    displayName: LocalizedStringDict


class DogmaAttributeCategoriesDict(TypedDict):
    """TypeDict definition for DogmaAttributeCategoriesDict.

    Total entries analyzed: 37.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: dogmaAttributeCategories.jsonl, build: 3081406
    Key Info:
    {'count': 37,
     'key_info': {'_key': {'int': 37},
                  'description': {'str': 36},
                  'name': {'str': 37}}}.
    """

    _key: int
    description: NotRequired[str]
    name: str


class DogmaAttributesDict(TypedDict):
    """TypeDict definition for DogmaAttributesDict.

    Total entries analyzed: 2775.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: dogmaAttributes.jsonl, build: 3081406
    Key Info:
    {'count': 2775,
     'key_info': {'_key': {'int': 2775},
                  'attributeCategoryID': {'int': 2600},
                  'dataType': {'int': 2775},
                  'defaultValue': {'float': 2775},
                  'description': {'str': 2606},
                  'displayWhenZero': {'bool': 2775},
                  'highIsGood': {'bool': 2775},
                  'name': {'str': 2775},
                  'published': {'bool': 2775},
                  'stackable': {'bool': 2775},
                  'displayName': {'dict': 1224},
                  'iconID': {'int': 1342},
                  'tooltipDescription': {'dict': 66},
                  'tooltipTitle': {'dict': 68},
                  'unitID': {'int': 1323},
                  'chargeRechargeTimeID': {'int': 6},
                  'maxAttributeID': {'int': 27},
                  'minAttributeID': {'int': 1}}}.
    """

    _key: int
    attributeCategoryID: NotRequired[int]
    dataType: int
    defaultValue: float
    description: NotRequired[str]
    displayWhenZero: bool
    highIsGood: bool
    name: str
    published: bool
    stackable: bool
    displayName: LocalizedStringDict
    iconID: NotRequired[int]
    tooltipDescription: LocalizedStringDict
    tooltipTitle: LocalizedStringDict
    unitID: NotRequired[int]
    chargeRechargeTimeID: NotRequired[int]
    maxAttributeID: NotRequired[int]
    minAttributeID: NotRequired[int]


class DogmaEffectsDict(TypedDict):
    """TypeDict definition for DogmaEffectsDict.

    Total entries analyzed: 3288.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: dogmaEffects.jsonl, build: 3081406
    Key Info:
    {'count': 3288,
     'key_info': {'_key': {'int': 3288},
                  'disallowAutoRepeat': {'bool': 3288},
                  'dischargeAttributeID': {'int': 169},
                  'durationAttributeID': {'int': 221},
                  'effectCategoryID': {'int': 3288},
                  'electronicChance': {'bool': 3288},
                  'guid': {'str': 1626},
                  'isAssistance': {'bool': 3288},
                  'isOffensive': {'bool': 3288},
                  'isWarpSafe': {'bool': 3288},
                  'name': {'str': 3288},
                  'propulsionChance': {'bool': 3288},
                  'published': {'bool': 3288},
                  'rangeChance': {'bool': 3288},
                  'distribution': {'int': 74},
                  'falloffAttributeID': {'int': 51},
                  'rangeAttributeID': {'int': 195},
                  'trackingSpeedAttributeID': {'int': 6},
                  'description': {'dict': 747},
                  'displayName': {'dict': 69},
                  'iconID': {'int': 1268},
                  'modifierInfo': {'list': 3073},
                  'npcUsageChanceAttributeID': {'int': 7},
                  'npcActivationChanceAttributeID': {'int': 19},
                  'fittingUsageChanceAttributeID': {'int': 12},
                  'resistanceAttributeID': {'int': 39}}}.
    """

    _key: int
    disallowAutoRepeat: bool
    dischargeAttributeID: NotRequired[int]
    durationAttributeID: NotRequired[int]
    effectCategoryID: int
    electronicChance: bool
    guid: NotRequired[str]
    isAssistance: bool
    isOffensive: bool
    isWarpSafe: bool
    name: str
    propulsionChance: bool
    published: bool
    rangeChance: bool
    distribution: NotRequired[int]
    falloffAttributeID: NotRequired[int]
    rangeAttributeID: NotRequired[int]
    trackingSpeedAttributeID: NotRequired[int]
    description: LocalizedStringDict
    displayName: LocalizedStringDict
    iconID: NotRequired[int]
    modifierInfo: NotRequired[list]
    npcUsageChanceAttributeID: NotRequired[int]
    npcActivationChanceAttributeID: NotRequired[int]
    fittingUsageChanceAttributeID: NotRequired[int]
    resistanceAttributeID: NotRequired[int]


class DogmaUnitsDict(TypedDict):
    """TypeDict definition for DogmaUnitsDict.

    Total entries analyzed: 60.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: dogmaUnits.jsonl, build: 3081406
    Key Info:
    {'count': 60,
     'key_info': {'_key': {'int': 60},
                  'description': {'dict': 44},
                  'displayName': {'dict': 56},
                  'name': {'str': 60}}}.
    """

    _key: int
    description: LocalizedStringDict
    displayName: LocalizedStringDict
    name: str


class DynamicItemAttributesDict(TypedDict):
    """TypeDict definition for DynamicItemAttributesDict.

    Total entries analyzed: 376.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: dynamicItemAttributes.jsonl, build: 3081406
    Key Info:
    {'count': 376,
     'key_info': {'_key': {'int': 376},
                  'attributeIDs': {'list': 376},
                  'inputOutputMapping': {'list': 376}}}.
    """

    _key: int
    attributeIDs: list
    inputOutputMapping: list


class FactionsDict(TypedDict):
    """TypeDict definition for FactionsDict.

    Total entries analyzed: 27.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: factions.jsonl, build: 3081406
    Key Info:
    {'count': 27,
     'key_info': {'_key': {'int': 27},
                  'corporationID': {'int': 26},
                  'description': {'dict': 27},
                  'flatLogo': {'str': 18},
                  'flatLogoWithName': {'str': 6},
                  'iconID': {'int': 27},
                  'memberRaces': {'list': 27},
                  'militiaCorporationID': {'int': 6},
                  'name': {'dict': 27},
                  'shortDescription': {'dict': 4},
                  'sizeFactor': {'float': 27},
                  'solarSystemID': {'int': 27},
                  'uniqueName': {'bool': 27}}}.
    """

    _key: int
    corporationID: NotRequired[int]
    description: LocalizedStringDict
    flatLogo: NotRequired[str]
    flatLogoWithName: NotRequired[str]
    iconID: int
    memberRaces: list
    militiaCorporationID: NotRequired[int]
    name: LocalizedStringDict
    shortDescription: LocalizedStringDict
    sizeFactor: float
    solarSystemID: int
    uniqueName: bool


class GraphicsDict(TypedDict):
    """TypeDict definition for GraphicsDict.

    Total entries analyzed: 5503.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: graphics.jsonl, build: 3081406
    Key Info:
    {'count': 5503,
     'key_info': {'_key': {'int': 5503},
                  'graphicFile': {'str': 2351},
                  'iconFolder': {'str': 2565},
                  'sofFactionName': {'str': 3658},
                  'sofHullName': {'str': 3080},
                  'sofRaceName': {'str': 3853},
                  'sofMaterialSetID': {'int': 90},
                  'sofLayout': {'list': 53}}}.
    """

    _key: int
    graphicFile: NotRequired[str]
    iconFolder: NotRequired[str]
    sofFactionName: NotRequired[str]
    sofHullName: NotRequired[str]
    sofRaceName: NotRequired[str]
    sofMaterialSetID: NotRequired[int]
    sofLayout: NotRequired[list]


class GroupsDict(TypedDict):
    """TypeDict definition for GroupsDict.

    Total entries analyzed: 1557.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: groups.jsonl, build: 3081406
    Key Info:
    {'count': 1557,
     'key_info': {'_key': {'int': 1557},
                  'anchorable': {'bool': 1557},
                  'anchored': {'bool': 1557},
                  'categoryID': {'int': 1557},
                  'fittableNonSingleton': {'bool': 1557},
                  'name': {'dict': 1557},
                  'published': {'bool': 1557},
                  'useBasePrice': {'bool': 1557},
                  'iconID': {'int': 763}}}.
    """

    _key: int
    anchorable: bool
    anchored: bool
    categoryID: int
    fittableNonSingleton: bool
    name: LocalizedStringDict
    published: bool
    useBasePrice: bool
    iconID: NotRequired[int]


class IconsDict(TypedDict):
    """TypeDict definition for IconsDict.

    Total entries analyzed: 4355.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: icons.jsonl, build: 3081406
    Key Info:
    {'count': 4355, 'key_info': {'_key': {'int': 4355}, 'iconFile': {'str': 4355}}}.
    """

    _key: int
    iconFile: str


class LandmarksDict(TypedDict):
    """TypeDict definition for LandmarksDict.

    Total entries analyzed: 45.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: landmarks.jsonl, build: 3081406
    Key Info:
    {'count': 45,
     'key_info': {'_key': {'int': 45},
                  'description': {'dict': 45},
                  'name': {'dict': 45},
                  'position': {'dict': 45},
                  'iconID': {'int': 19},
                  'locationID': {'int': 10}}}.
    """

    _key: int
    description: LocalizedStringDict
    name: LocalizedStringDict
    position: dict
    iconID: NotRequired[int]
    locationID: NotRequired[int]


class MapAsteroidBeltsDict(TypedDict):
    """TypeDict definition for MapAsteroidBeltsDict.

    Total entries analyzed: 40928.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: mapAsteroidBelts.jsonl, build: 3081406
    Key Info:
    {'count': 40928,
     'key_info': {'_key': {'int': 40928},
                  'celestialIndex': {'int': 40928},
                  'orbitID': {'int': 40928},
                  'orbitIndex': {'int': 40928},
                  'position': {'dict': 40928},
                  'radius': {'float': 40226},
                  'solarSystemID': {'int': 40928},
                  'statistics': {'dict': 40226},
                  'typeID': {'int': 40928},
                  'uniqueName': {'dict': 46}}}.
    """

    _key: int
    celestialIndex: int
    orbitID: int
    orbitIndex: int
    position: dict
    radius: NotRequired[float]
    solarSystemID: int
    statistics: NotRequired[dict]
    typeID: int
    uniqueName: LocalizedStringDict


class MapConstellationsDict(TypedDict):
    """TypeDict definition for MapConstellationsDict.

    Total entries analyzed: 1175.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: mapConstellations.jsonl, build: 3081406
    Key Info:
    {'count': 1175,
     'key_info': {'_key': {'int': 1175},
                  'factionID': {'int': 377},
                  'name': {'dict': 1175},
                  'position': {'dict': 1175},
                  'regionID': {'int': 1175},
                  'solarSystemIDs': {'list': 1175},
                  'wormholeClassID': {'int': 1141}}}.
    """

    _key: int
    factionID: NotRequired[int]
    name: LocalizedStringDict
    position: dict
    regionID: int
    solarSystemIDs: list
    wormholeClassID: NotRequired[int]


class MapMoonsDict(TypedDict):
    """TypeDict definition for MapMoonsDict.

    Total entries analyzed: 342170.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: mapMoons.jsonl, build: 3081406
    Key Info:
    {'count': 342170,
     'key_info': {'_key': {'int': 342170},
                  'attributes': {'dict': 342170},
                  'celestialIndex': {'int': 342170},
                  'orbitID': {'int': 342170},
                  'orbitIndex': {'int': 342170},
                  'position': {'dict': 342170},
                  'radius': {'float': 342170},
                  'solarSystemID': {'int': 342170},
                  'statistics': {'dict': 340806},
                  'typeID': {'int': 342170},
                  'npcStationIDs': {'list': 3801},
                  'uniqueName': {'dict': 137}}}.
    """

    _key: int
    attributes: dict
    celestialIndex: int
    orbitID: int
    orbitIndex: int
    position: dict
    radius: float
    solarSystemID: int
    statistics: NotRequired[dict]
    typeID: int
    npcStationIDs: NotRequired[list]
    uniqueName: LocalizedStringDict


class MapPlanetsDict(TypedDict):
    """TypeDict definition for MapPlanetsDict.

    Total entries analyzed: 67961.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: mapPlanets.jsonl, build: 3081406
    Key Info:
    {'count': 67961,
     'key_info': {'_key': {'int': 67961},
                  'asteroidBeltIDs': {'list': 17277},
                  'attributes': {'dict': 67961},
                  'celestialIndex': {'int': 67961},
                  'moonIDs': {'list': 51460},
                  'orbitID': {'int': 67961},
                  'position': {'dict': 67961},
                  'radius': {'int': 67961},
                  'solarSystemID': {'int': 67961},
                  'statistics': {'dict': 67961},
                  'typeID': {'int': 67961},
                  'npcStationIDs': {'list': 1098},
                  'uniqueName': {'dict': 43}}}.
    """

    _key: int
    asteroidBeltIDs: NotRequired[list]
    attributes: dict
    celestialIndex: int
    moonIDs: NotRequired[list]
    orbitID: int
    position: dict
    radius: int
    solarSystemID: int
    statistics: dict
    typeID: int
    npcStationIDs: NotRequired[list]
    uniqueName: LocalizedStringDict


class MapRegionsDict(TypedDict):
    """TypeDict definition for MapRegionsDict.

    Total entries analyzed: 113.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: mapRegions.jsonl, build: 3081406
    Key Info:
    {'count': 113,
     'key_info': {'_key': {'int': 113},
                  'constellationIDs': {'list': 113},
                  'description': {'dict': 69},
                  'factionID': {'int': 32},
                  'name': {'dict': 113},
                  'nebulaID': {'int': 113},
                  'position': {'dict': 113},
                  'wormholeClassID': {'int': 109}}}.
    """

    _key: int
    constellationIDs: list
    description: LocalizedStringDict
    factionID: NotRequired[int]
    name: LocalizedStringDict
    nebulaID: int
    position: dict
    wormholeClassID: NotRequired[int]


class MapSolarSystemsDict(TypedDict):
    """TypeDict definition for MapSolarSystemsDict.

    Total entries analyzed: 8437.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: mapSolarSystems.jsonl, build: 3081406
    Key Info:
    {'count': 8437,
     'key_info': {'_key': {'int': 8437},
                  'border': {'bool': 1997},
                  'constellationID': {'int': 8437},
                  'hub': {'bool': 2678},
                  'international': {'bool': 108},
                  'luminosity': {'float': 5431},
                  'name': {'dict': 8437},
                  'planetIDs': {'list': 8035},
                  'position': {'dict': 8437},
                  'radius': {'float': 8437},
                  'regionID': {'int': 8437},
                  'regional': {'bool': 537},
                  'securityClass': {'str': 5140},
                  'securityStatus': {'float': 8437},
                  'starID': {'int': 8036},
                  'stargateIDs': {'list': 5215},
                  'corridor': {'bool': 1920},
                  'fringe': {'bool': 782},
                  'wormholeClassID': {'int': 692},
                  'visualEffect': {'str': 129},
                  'disallowedAnchorCategories': {'list': 538},
                  'disallowedAnchorGroups': {'list': 26},
                  'factionID': {'int': 16}}}.
    """

    _key: int
    border: NotRequired[bool]
    constellationID: int
    hub: NotRequired[bool]
    international: NotRequired[bool]
    luminosity: NotRequired[float]
    name: LocalizedStringDict
    planetIDs: NotRequired[list]
    position: dict
    radius: float
    regionID: int
    regional: NotRequired[bool]
    securityClass: NotRequired[str]
    securityStatus: float
    starID: NotRequired[int]
    stargateIDs: NotRequired[list]
    corridor: NotRequired[bool]
    fringe: NotRequired[bool]
    wormholeClassID: NotRequired[int]
    visualEffect: NotRequired[str]
    disallowedAnchorCategories: NotRequired[list]
    disallowedAnchorGroups: NotRequired[list]
    factionID: NotRequired[int]


class MapStargatesDict(TypedDict):
    """TypeDict definition for MapStargatesDict.

    Total entries analyzed: 13776.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: mapStargates.jsonl, build: 3081406
    Key Info:
    {'count': 13776,
     'key_info': {'_key': {'int': 13776},
                  'destination': {'dict': 13776},
                  'position': {'dict': 13776},
                  'solarSystemID': {'int': 13776},
                  'typeID': {'int': 13776}}}.
    """

    _key: int
    destination: dict
    position: dict
    solarSystemID: int
    typeID: int


class MapStarsDict(TypedDict):
    """TypeDict definition for MapStarsDict.

    Total entries analyzed: 8036.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: mapStars.jsonl, build: 3081406
    Key Info:
    {'count': 8036,
     'key_info': {'_key': {'int': 8036},
                  'radius': {'int': 8036},
                  'solarSystemID': {'int': 8036},
                  'statistics': {'dict': 8036},
                  'typeID': {'int': 8036}}}.
    """

    _key: int
    radius: int
    solarSystemID: int
    statistics: dict
    typeID: int


class MarketGroupsDict(TypedDict):
    """TypeDict definition for MarketGroupsDict.

    Total entries analyzed: 2039.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: marketGroups.jsonl, build: 3081406
    Key Info:
    {'count': 2039,
     'key_info': {'_key': {'int': 2039},
                  'description': {'dict': 1565},
                  'hasTypes': {'bool': 2039},
                  'iconID': {'int': 2009},
                  'name': {'dict': 2039},
                  'parentGroupID': {'int': 2020}}}.
    """

    _key: int
    description: LocalizedStringDict
    hasTypes: bool
    iconID: NotRequired[int]
    name: LocalizedStringDict
    parentGroupID: NotRequired[int]


class MasteriesDict(TypedDict):
    """TypeDict definition for MasteriesDict.

    Total entries analyzed: 460.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: masteries.jsonl, build: 3081406
    Key Info:
    {'count': 460, 'key_info': {'_key': {'int': 460}, '_value': {'list': 460}}}.
    """

    _key: int
    _value: list


class MetaGroupsDict(TypedDict):
    """TypeDict definition for MetaGroupsDict.

    Total entries analyzed: 13.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: metaGroups.jsonl, build: 3081406
    Key Info:
    {'count': 13,
     'key_info': {'_key': {'int': 13},
                  'color': {'dict': 10},
                  'name': {'dict': 13},
                  'iconID': {'int': 12},
                  'iconSuffix': {'str': 12},
                  'description': {'dict': 3}}}.
    """

    _key: int
    color: NotRequired[dict]
    name: LocalizedStringDict
    iconID: NotRequired[int]
    iconSuffix: NotRequired[str]
    description: LocalizedStringDict


class NpcCharactersDict(TypedDict):
    """TypeDict definition for NpcCharactersDict.

    Total entries analyzed: 11302.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: npcCharacters.jsonl, build: 3081406
    Key Info:
    {'count': 11302,
     'key_info': {'_key': {'int': 11302},
                  'bloodlineID': {'int': 11302},
                  'ceo': {'bool': 11302},
                  'corporationID': {'int': 11302},
                  'gender': {'bool': 11302},
                  'locationID': {'int': 11256},
                  'name': {'dict': 11302},
                  'raceID': {'int': 11302},
                  'startDate': {'str': 11185},
                  'uniqueName': {'bool': 11302},
                  'skills': {'list': 421},
                  'ancestryID': {'int': 11101},
                  'careerID': {'int': 11098},
                  'schoolID': {'int': 11095},
                  'specialityID': {'int': 11096},
                  'agent': {'dict': 10878},
                  'description': {'str': 24}}}.
    """

    _key: int
    bloodlineID: int
    ceo: bool
    corporationID: int
    gender: bool
    locationID: NotRequired[int]
    name: LocalizedStringDict
    raceID: int
    startDate: NotRequired[str]
    uniqueName: bool
    skills: NotRequired[list]
    ancestryID: NotRequired[int]
    careerID: NotRequired[int]
    schoolID: NotRequired[int]
    specialityID: NotRequired[int]
    agent: NotRequired[dict]
    description: NotRequired[str]


class NpcCorporationDivisionsDict(TypedDict):
    """TypeDict definition for NpcCorporationDivisionsDict.

    Total entries analyzed: 10.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: npcCorporationDivisions.jsonl, build: 3081406
    Key Info:
    {'count': 10,
     'key_info': {'_key': {'int': 10},
                  'displayName': {'str': 9},
                  'internalName': {'str': 10},
                  'leaderTypeName': {'dict': 10},
                  'name': {'dict': 10},
                  'description': {'dict': 5}}}.
    """

    _key: int
    displayName: NotRequired[str]
    internalName: str
    leaderTypeName: dict
    name: LocalizedStringDict
    description: LocalizedStringDict


class NpcCorporationsDict(TypedDict):
    """TypeDict definition for NpcCorporationsDict.

    Total entries analyzed: 283.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: npcCorporations.jsonl, build: 3081406
    Key Info:
    {'count': 283,
     'key_info': {'_key': {'int': 283},
                  'ceoID': {'int': 260},
                  'deleted': {'bool': 283},
                  'description': {'dict': 280},
                  'extent': {'str': 283},
                  'hasPlayerPersonnelManager': {'bool': 283},
                  'initialPrice': {'int': 283},
                  'memberLimit': {'int': 283},
                  'minSecurity': {'float': 283},
                  'minimumJoinStanding': {'int': 283},
                  'name': {'dict': 283},
                  'sendCharTerminationMessage': {'bool': 283},
                  'shares': {'int': 283},
                  'size': {'str': 283},
                  'stationID': {'int': 262},
                  'taxRate': {'float': 283},
                  'tickerName': {'str': 283},
                  'uniqueName': {'bool': 283},
                  'allowedMemberRaces': {'list': 212},
                  'corporationTrades': {'list': 184},
                  'divisions': {'list': 118},
                  'enemyID': {'int': 250},
                  'factionID': {'int': 273},
                  'friendID': {'int': 246},
                  'iconID': {'int': 252},
                  'investors': {'list': 227},
                  'lpOfferTables': {'list': 181},
                  'mainActivityID': {'int': 266},
                  'raceID': {'int': 257},
                  'sizeFactor': {'float': 189},
                  'solarSystemID': {'int': 261},
                  'secondaryActivityID': {'int': 34},
                  'exchangeRates': {'list': 1}}}.
    """

    _key: int
    ceoID: NotRequired[int]
    deleted: bool
    description: NotRequired[dict]
    extent: str
    hasPlayerPersonnelManager: bool
    initialPrice: int
    memberLimit: int
    minSecurity: float
    minimumJoinStanding: int
    name: LocalizedStringDict
    sendCharTerminationMessage: bool
    shares: int
    size: str
    stationID: NotRequired[int]
    taxRate: float
    tickerName: str
    uniqueName: bool
    allowedMemberRaces: NotRequired[list]
    corporationTrades: NotRequired[list]
    divisions: NotRequired[list]
    enemyID: NotRequired[int]
    factionID: NotRequired[int]
    friendID: NotRequired[int]
    iconID: NotRequired[int]
    investors: NotRequired[list]
    lpOfferTables: NotRequired[list]
    mainActivityID: NotRequired[int]
    raceID: NotRequired[int]
    sizeFactor: NotRequired[float]
    solarSystemID: NotRequired[int]
    secondaryActivityID: NotRequired[int]
    exchangeRates: NotRequired[list]


class NpcStationsDict(TypedDict):
    """TypeDict definition for NpcStationsDict.

    Total entries analyzed: 5154.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: npcStations.jsonl, build: 3081406
    Key Info:
    {'count': 5154,
     'key_info': {'_key': {'int': 5154},
                  'celestialIndex': {'int': 5153},
                  'operationID': {'int': 5154},
                  'orbitID': {'int': 5154},
                  'orbitIndex': {'int': 3968},
                  'ownerID': {'int': 5154},
                  'position': {'dict': 5154},
                  'reprocessingEfficiency': {'float': 5154},
                  'reprocessingHangarFlag': {'int': 5154},
                  'reprocessingStationsTake': {'float': 5154},
                  'solarSystemID': {'int': 5154},
                  'typeID': {'int': 5154},
                  'useOperationName': {'bool': 5154}}}.
    """

    _key: int
    celestialIndex: NotRequired[int]
    operationID: int
    orbitID: int
    orbitIndex: NotRequired[int]
    ownerID: int
    position: dict
    reprocessingEfficiency: float
    reprocessingHangarFlag: int
    reprocessingStationsTake: float
    solarSystemID: int
    typeID: int
    useOperationName: bool


class PlanetResourcesDict(TypedDict):
    """TypeDict definition for PlanetResourcesDict.

    Total entries analyzed: 25798.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: planetResources.jsonl, build: 3081406
    Key Info:
    {'count': 25798,
     'key_info': {'_key': {'int': 25798},
                  'power': {'int': 12126},
                  'workforce': {'int': 10210},
                  'cycle_minutes': {'int': 3462},
                  'harvest_silo_max': {'int': 3462},
                  'maturation_cycle_minutes': {'int': 3462},
                  'maturation_percent': {'int': 3462},
                  'mature_silo_max': {'int': 3462},
                  'reagent_harvest_amount': {'int': 3462},
                  'reagent_type_id': {'int': 3462}}}.
    """

    _key: int
    power: NotRequired[int]
    workforce: NotRequired[int]
    cycle_minutes: NotRequired[int]
    harvest_silo_max: NotRequired[int]
    maturation_cycle_minutes: NotRequired[int]
    maturation_percent: NotRequired[int]
    mature_silo_max: NotRequired[int]
    reagent_harvest_amount: NotRequired[int]
    reagent_type_id: NotRequired[int]


class PlanetSchematicsDict(TypedDict):
    """TypeDict definition for PlanetSchematicsDict.

    Total entries analyzed: 68.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: planetSchematics.jsonl, build: 3081406
    Key Info:
    {'count': 68,
     'key_info': {'_key': {'int': 68},
                  'cycleTime': {'int': 68},
                  'name': {'dict': 68},
                  'pins': {'list': 68},
                  'types': {'list': 68}}}.
    """

    _key: int
    cycleTime: int
    name: LocalizedStringDict
    pins: list
    types: list


class RacesDict(TypedDict):
    """TypeDict definition for RacesDict.

    Total entries analyzed: 11.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: races.jsonl, build: 3081406
    Key Info:
    {'count': 11,
     'key_info': {'_key': {'int': 11},
                  'description': {'dict': 8},
                  'iconID': {'int': 5},
                  'name': {'dict': 11},
                  'shipTypeID': {'int': 4},
                  'skills': {'list': 4}}}.
    """

    _key: int
    description: NotRequired[dict]
    iconID: NotRequired[int]
    name: LocalizedStringDict
    shipTypeID: NotRequired[int]
    skills: NotRequired[list]


class SdeInfoDict(TypedDict):
    """TypeDict definition for SdeInfoDict.

    Total entries analyzed: 1.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: _sde.jsonl, build: 3081406
    Key Info:
    {'count': 1,
     'key_info': {'_key': {'str': 1},
                  'buildNumber': {'int': 1},
                  'releaseDate': {'str': 1}}}.
    """

    _key: str
    buildNumber: int
    releaseDate: str


class SkinLicensesDict(TypedDict):
    """TypeDict definition for SkinLicensesDict.

    Total entries analyzed: 11528.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: skinLicenses.jsonl, build: 3081406
    Key Info:
    {'count': 11528,
     'key_info': {'_key': {'int': 11528},
                  'duration': {'int': 11528},
                  'licenseTypeID': {'int': 11528},
                  'skinID': {'int': 11528},
                  'isSingleUse': {'bool': 4246}}}.
    """

    _key: int
    duration: int
    licenseTypeID: int
    skinID: int
    isSingleUse: NotRequired[bool]


class SkinMaterialsDict(TypedDict):
    """TypeDict definition for SkinMaterialsDict.

    Total entries analyzed: 824.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: skinMaterials.jsonl, build: 3081406
    Key Info:
    {'count': 824,
     'key_info': {'_key': {'int': 824},
                  'displayName': {'dict': 822},
                  'materialSetID': {'int': 824}}}.
    """

    _key: int
    displayName: NotRequired[dict]
    materialSetID: int


class SkinsDict(TypedDict):
    """TypeDict definition for SkinsDict.

    Total entries analyzed: 6699.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: skins.jsonl, build: 3081406
    Key Info:
    {'count': 6699,
     'key_info': {'_key': {'int': 6699},
                  'allowCCPDevs': {'bool': 6699},
                  'internalName': {'str': 6699},
                  'skinMaterialID': {'int': 6699},
                  'types': {'list': 6699},
                  'visibleSerenity': {'bool': 6699},
                  'visibleTranquility': {'bool': 6699},
                  'isStructureSkin': {'bool': 939},
                  'skinDescription': {'dict': 2391}}}.
    """

    _key: int
    allowCCPDevs: bool
    internalName: str
    skinMaterialID: int
    types: list
    visibleSerenity: bool
    visibleTranquility: bool
    isStructureSkin: NotRequired[bool]
    skinDescription: NotRequired[dict]


class SovereigntyUpgradesDict(TypedDict):
    """TypeDict definition for SovereigntyUpgradesDict.

    Total entries analyzed: 27.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: sovereigntyUpgrades.jsonl, build: 3081406
    Key Info:
    {'count': 27,
     'key_info': {'_key': {'int': 27},
                  'fuel_hourly_upkeep': {'int': 4},
                  'fuel_startup_cost': {'int': 4},
                  'fuel_type_id': {'int': 4},
                  'mutually_exclusive_group': {'str': 27},
                  'power_allocation': {'int': 27},
                  'workforce_allocation': {'int': 27}}}.
    """

    _key: int
    fuel_hourly_upkeep: NotRequired[int]
    fuel_startup_cost: NotRequired[int]
    fuel_type_id: NotRequired[int]
    mutually_exclusive_group: str
    power_allocation: int
    workforce_allocation: int


class StationOperationsDict(TypedDict):
    """TypeDict definition for StationOperationsDict.

    Total entries analyzed: 66.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: stationOperations.jsonl, build: 3081406
    Key Info:
    {'count': 66,
     'key_info': {'_key': {'int': 66},
                  'activityID': {'int': 66},
                  'border': {'float': 66},
                  'corridor': {'float': 66},
                  'description': {'dict': 54},
                  'fringe': {'float': 66},
                  'hub': {'float': 66},
                  'manufacturingFactor': {'float': 66},
                  'operationName': {'dict': 66},
                  'ratio': {'float': 66},
                  'researchFactor': {'float': 66},
                  'services': {'list': 66},
                  'stationTypes': {'list': 47}}}.
    """

    _key: int
    activityID: int
    border: float
    corridor: float
    description: NotRequired[dict]
    fringe: float
    hub: float
    manufacturingFactor: float
    operationName: LocalizedStringDict
    ratio: float
    researchFactor: float
    services: list
    stationTypes: NotRequired[list]


class StationServicesDict(TypedDict):
    """TypeDict definition for StationServicesDict.

    Total entries analyzed: 27.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: stationServices.jsonl, build: 3081406
    Key Info:
    {'count': 27,
     'key_info': {'_key': {'int': 27},
                  'serviceName': {'dict': 27},
                  'description': {'dict': 1}}}.
    """

    _key: int
    serviceName: LocalizedStringDict
    description: NotRequired[LocalizedStringDict]


class TranslationLanguagesDict(TypedDict):
    """TypeDict definition for TranslationLanguagesDict.

    Total entries analyzed: 8.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: translationLanguages.jsonl, build: 3081406
    Key Info:
    {'count': 8, 'key_info': {'_key': {'str': 8}, 'name': {'str': 8}}}.
    """

    _key: str
    name: str


class TypeBonusDict(TypedDict):
    """TypeDict definition for TypeBonusDict.

    Total entries analyzed: 628.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: typeBonus.jsonl, build: 3081406
    Key Info:
    {'count': 628,
     'key_info': {'_key': {'int': 628},
                  'roleBonuses': {'list': 468},
                  'types': {'list': 517},
                  'iconID': {'int': 62},
                  'miscBonuses': {'list': 71}}}.
    """

    _key: int
    roleBonuses: NotRequired[list]
    types: NotRequired[list]
    iconID: NotRequired[int]
    miscBonuses: NotRequired[list]


class TypeDogmaDict(TypedDict):
    """TypeDict definition for TypeDogmaDict.

    Total entries analyzed: 25788.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: typeDogma.jsonl, build: 3081406
    Key Info:
    {'count': 25788,
     'key_info': {'_key': {'int': 25788},
                  'dogmaAttributes': {'list': 25788},
                  'dogmaEffects': {'list': 15393}}}.
    """

    _key: int
    dogmaAttributes: list
    dogmaEffects: NotRequired[list]


class TypeMaterialsDict(TypedDict):
    """TypeDict definition for TypeMaterialsDict.

    Total entries analyzed: 9430.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: typeMaterials.jsonl, build: 3081406
    Key Info:
    {'count': 9430,
     'key_info': {'_key': {'int': 9430}, 'materials': {'list': 9430}}}.
    """

    _key: int
    materials: list


class TypesDict(TypedDict):
    """TypeDict definition for TypesDict.

    Total entries analyzed: 50535.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: types.jsonl, build: 3081406
    Key Info:
    {'count': 50535,
     'key_info': {'_key': {'int': 50535},
                  'groupID': {'int': 50535},
                  'mass': {'float': 20285},
                  'name': {'dict': 50535},
                  'portionSize': {'int': 50535},
                  'published': {'bool': 50535},
                  'volume': {'float': 45132},
                  'radius': {'float': 14867},
                  'description': {'dict': 32726},
                  'graphicID': {'int': 17458},
                  'soundID': {'int': 4956},
                  'iconID': {'int': 21967},
                  'raceID': {'int': 22508},
                  'basePrice': {'float': 13725},
                  'marketGroupID': {'int': 18840},
                  'capacity': {'float': 9450},
                  'metaGroupID': {'int': 13253},
                  'variationParentTypeID': {'int': 4739},
                  'factionID': {'int': 1320}}}.
    """

    _key: int
    groupID: int
    mass: NotRequired[float]
    name: LocalizedStringDict
    portionSize: int
    published: bool
    volume: NotRequired[float]
    radius: NotRequired[float]
    description: LocalizedStringDict
    graphicID: NotRequired[int]
    soundID: NotRequired[int]
    iconID: NotRequired[int]
    raceID: NotRequired[int]
    basePrice: NotRequired[float]
    marketGroupID: NotRequired[int]
    capacity: NotRequired[float]
    metaGroupID: NotRequired[int]
    variationParentTypeID: NotRequired[int]
    factionID: NotRequired[int]
