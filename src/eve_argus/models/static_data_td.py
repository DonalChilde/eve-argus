"""Auto-generated TypedDict definitions for SDE build 3081406."""

from typing import NotRequired, TypedDict

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


class MaterialsDict(TypedDict):
    typeID: int
    quantity: int


class SkillsDict(TypedDict):
    typeID: int
    level: int


class ProductsDict(TypedDict):
    typeID: int
    quantity: int
    probability: NotRequired[float]


class ActivityDict(TypedDict):
    materials: list[MaterialsDict]
    skills: list[SkillsDict]
    time: int
    products: NotRequired[list[ProductsDict]]


class ActivitiesDict(TypedDict):
    copying: NotRequired[ActivityDict]
    invention: NotRequired[ActivityDict]
    manufacturing: NotRequired[ActivityDict]
    reaction: NotRequired[ActivityDict]
    research_material: NotRequired[ActivityDict]
    research_time: NotRequired[ActivityDict]


class ColorDict(TypedDict):
    b: float
    g: float
    r: float


class MaterialsMateritalsDict(TypedDict):
    """TypeDict definition for MaterialsMateritalsDict.

    This type is used by TypeMaterialsDict. I expect the naming to be fixed in future
    SDE versions, be the same as MaterialsDict.
    """

    materialTypeID: int
    quantity: int


class SkillTypeDict(TypedDict):
    """TypeDict definition for SkillTypeDict.

    This type is used by CertificatesDict.
    """

    _key: int
    basic: int
    standard: int
    improved: int
    advanced: int
    elite: int


class ContrabandFactionDict(TypedDict):
    """TypeDict definition for ContrabandFactionDict.

    This type is used by ContrabandTypesDict.
    """

    _key: int
    attackMinSec: float
    confiscateMinSec: float
    fineByValue: float
    standingLoss: float


class CTResourceDict(TypedDict):
    """TypeDict definition for CTResourceDict.

    This type is used by ControlTowerResourcesDict.
    """

    factionID: NotRequired[int]
    minSecurityLevel: NotRequired[float]
    purpose: int
    quantity: int
    resourceTypeID: int


class LocationGroupModifierDict(TypedDict):
    """TypeDict definition for LocationGroupModifierDict.

    This type is used by DebuffCollectionsDict.
    """

    dogmaAttributeID: int
    groupID: int


class LocationModifierDict(TypedDict):
    """TypeDict definition for LocationModifierDict.

    This type is used by DebuffCollectionsDict.
    """

    dogmaAttributeID: int


class LocationRequiredSkillModifierDict(TypedDict):
    """TypeDict definition for LocationRequiredSkillModifierDict.

    This type is used by DebuffCollectionsDict.
    """

    dogmaAttributeID: int
    skillID: int


class DogmaEffectModifierInfoDict(TypedDict):
    """TypeDict definition for DogmaEffectModifierInfoDict.

    This type is used by DogmaEffectsDict.
    """

    domain: str
    effectID: NotRequired[int]
    func: str
    groupID: NotRequired[int]
    modifiedAttributeID: int
    modifyingAttributeID: int
    operation: int
    skillTypeID: NotRequired[int]


class AttributeIDDict(TypedDict):
    """TypeDict definition for AttributeIDDict.

    This type is used by DynamicItemAttributesDict.
    """

    _key: int
    highIsGood: NotRequired[bool]
    max: float
    min: float


class InputOutputMappingDict(TypedDict):
    """TypeDict definition for InputOutputMappingDict.

    This type is used by DynamicItemAttributesDict.
    """

    applicableTypes: list[int]
    resultingType: int


class PositionDict(TypedDict):
    """TypeDict definition for PositionDict."""

    x: float
    y: float
    z: float


class AsteroidBeltStatisticsDict(TypedDict):
    """TypeDict definition for AsteroidBeltStatisticsDict.

    This type is used by MapAsteroidBeltsDict.
    """

    density: float
    eccentricity: float
    escapeVelocity: float
    locked: bool
    massDust: float
    massGas: float
    orbitPeriod: float
    orbitRadius: float
    spectralClass: str
    surfaceGravity: float
    temperature: float


class MoonAttributesDict(TypedDict):
    """TypeDict definition for MoonAttributesDict.

    This type is used by MapMoonsDict.
    """

    heightMap1: int
    heightMap2: int
    shaderPreset: int


class MoonStatisticsDict(TypedDict):
    """TypeDict definition for MoonStatisticsDict.

    This type is used by MapMoonsDict.
    """

    density: float
    eccentricity: float
    escapeVelocity: float
    locked: bool
    massDust: float
    massGas: float
    orbitPeriod: float
    orbitRadius: float
    pressure: float
    rotationRate: float
    spectralClass: str
    surfaceGravity: float
    temperature: float


class PlanetAttributesDict(TypedDict):
    """TypeDict definition for PlanetAttributesDict.

    This type is used by MapPlanetsDict.
    """

    heightMap1: int
    heightMap2: int
    population: bool
    shaderPreset: int


class PlanetStatisticsDict(TypedDict):
    """TypeDict definition for PlanetStatisticsDict.

    This type is used by MapPlanetsDict.
    """

    density: float
    eccentricity: float
    escapeVelocity: float
    locked: bool
    massDust: float
    massGas: float
    orbitPeriod: float
    orbitRadius: float
    pressure: float
    rotationRate: float
    spectralClass: str
    surfaceGravity: float
    temperature: float


class StargateDestinationDict(TypedDict):
    """TypeDict definition for StargateDestinationDict.

    This type is used by MapStargatesDict.
    """

    solarSystemID: int
    stargateID: int


class StarStatisticsDict(TypedDict):
    """TypeDict definition for StarStatisticsDict.

    This type is used by MapStarsDict.
    """

    age: float
    life: float
    luminosity: float
    spectralClass: str
    temperature: float


class MasteriesValueDict(TypedDict):
    """TypeDict definition for MasteriesValueDict.

    This type is used by MasteriesDict.
    """

    _key: int
    _value: list[int]


class NpcCharacterSkillsDict(TypedDict):
    """TypeDict definition for NpcCharacterSkillsDict.

    This type is used by NpcCharactersDict.
    """

    typeID: int


class NpcCharacterAgentDict(TypedDict):
    """TypeDict definition for NpcCharacterAgentDict.

    This type is used by NpcCharactersDict.
    """

    agentTypeID: int
    divisionID: int
    isLocator: bool
    level: int


# ------------------------------------------------------------------------------
# File level TypedDict definitions.
# ------------------------------------------------------------------------------


class AgentsInSpaceDict(TypedDict):
    """TypeDict definition for AgentsInSpaceDict.

    Total entries analyzed: 360.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: agentsInSpace.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 360,
     'key_info': {'_key': {'int': 360},
                  'dungeonID': {'int': 360},
                  'solarSystemID': {'int': 360},
                  'spawnPointID': {'int': 360},
                  'typeID': {'int': 360}},
     'source_info': 'SDE file: agentsInSpace.jsonl, build: 3081406'}.
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
    Source info: SDE file: agentTypes.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 13,
     'key_info': {'_key': {'int': 13}, 'name': {'str': 13}},
     'source_info': 'SDE file: agentTypes.jsonl, build: 3081406'}.
    """

    _key: int
    name: str


class AncestriesDict(TypedDict):
    """TypeDict definition for AncestriesDict.

    Total entries analyzed: 43.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: ancestries.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 43,
     'key_info': {'_key': {'int': 43},
                  'bloodlineID': {'int': 43},
                  'charisma': {'int': 43},
                  'description': {'dict': 43},
                  'description.de': {'str': 43},
                  'description.en': {'str': 43},
                  'description.es': {'str': 43},
                  'description.fr': {'str': 43},
                  'description.ja': {'str': 43},
                  'description.ko': {'str': 43},
                  'description.ru': {'str': 43},
                  'description.zh': {'str': 43},
                  'iconID': {'int': 35},
                  'intelligence': {'int': 43},
                  'memory': {'int': 43},
                  'name': {'dict': 43},
                  'name.de': {'str': 43},
                  'name.en': {'str': 43},
                  'name.es': {'str': 43},
                  'name.fr': {'str': 43},
                  'name.ja': {'str': 43},
                  'name.ko': {'str': 43},
                  'name.ru': {'str': 43},
                  'name.zh': {'str': 43},
                  'perception': {'int': 43},
                  'shortDescription': {'str': 42},
                  'willpower': {'int': 43}},
     'source_info': 'SDE file: ancestries.jsonl, build: 3081406'}.
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
    Source info: SDE file: bloodlines.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 18,
     'key_info': {'_key': {'int': 18},
                  'charisma': {'int': 18},
                  'corporationID': {'int': 18},
                  'description': {'dict': 18},
                  'description.de': {'str': 18},
                  'description.en': {'str': 18},
                  'description.es': {'str': 18},
                  'description.fr': {'str': 18},
                  'description.ja': {'str': 18},
                  'description.ko': {'str': 18},
                  'description.ru': {'str': 18},
                  'description.zh': {'str': 18},
                  'iconID': {'int': 15},
                  'intelligence': {'int': 18},
                  'memory': {'int': 18},
                  'name': {'dict': 18},
                  'name.de': {'str': 18},
                  'name.en': {'str': 18},
                  'name.es': {'str': 18},
                  'name.fr': {'str': 18},
                  'name.ja': {'str': 18},
                  'name.ko': {'str': 18},
                  'name.ru': {'str': 18},
                  'name.zh': {'str': 18},
                  'perception': {'int': 18},
                  'raceID': {'int': 18},
                  'willpower': {'int': 18}},
     'source_info': 'SDE file: bloodlines.jsonl, build: 3081406'}.
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
    Source info: SDE file: blueprints.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 5031,
     'key_info': {'_key': {'int': 5031},
                  'activities': {'dict': 5031},
                  'activities.copying': {'dict': 4326},
                  'activities.copying.materials': {'dict': 1818, 'list': 1007},
                  'activities.copying.materials.quantity': {'int': 1818},
                  'activities.copying.materials.typeID': {'int': 1818},
                  'activities.copying.skills': {'dict': 2137, 'list': 1020},
                  'activities.copying.skills.level': {'int': 2137},
                  'activities.copying.skills.typeID': {'int': 2137},
                  'activities.copying.time': {'int': 4326},
                  'activities.invention': {'dict': 1105},
                  'activities.invention.materials': {'dict': 2208, 'list': 1104},
                  'activities.invention.materials.quantity': {'int': 2208},
                  'activities.invention.materials.typeID': {'int': 2208},
                  'activities.invention.products': {'dict': 1349, 'list': 1101},
                  'activities.invention.products.probability': {'float': 1341},
                  'activities.invention.products.quantity': {'int': 1349},
                  'activities.invention.products.typeID': {'int': 1349},
                  'activities.invention.skills': {'dict': 3400, 'list': 1104},
                  'activities.invention.skills.level': {'int': 3400},
                  'activities.invention.skills.typeID': {'int': 3400},
                  'activities.invention.time': {'int': 1105},
                  'activities.manufacturing': {'dict': 4828},
                  'activities.manufacturing.materials': {'dict': 26806,
                                                         'list': 4811},
                  'activities.manufacturing.materials.quantity': {'int': 26806},
                  'activities.manufacturing.materials.typeID': {'int': 26806},
                  'activities.manufacturing.products': {'dict': 4805, 'list': 4805},
                  'activities.manufacturing.products.quantity': {'int': 4805},
                  'activities.manufacturing.products.typeID': {'int': 4805},
                  'activities.manufacturing.skills': {'dict': 9109, 'list': 4691},
                  'activities.manufacturing.skills.level': {'int': 9109},
                  'activities.manufacturing.skills.typeID': {'int': 9109},
                  'activities.manufacturing.time': {'int': 4828},
                  'activities.reaction': {'dict': 112},
                  'activities.reaction.materials': {'dict': 384, 'list': 112},
                  'activities.reaction.materials.quantity': {'int': 384},
                  'activities.reaction.materials.typeID': {'int': 384},
                  'activities.reaction.products': {'dict': 112, 'list': 112},
                  'activities.reaction.products.quantity': {'int': 112},
                  'activities.reaction.products.typeID': {'int': 112},
                  'activities.reaction.skills': {'dict': 112, 'list': 112},
                  'activities.reaction.skills.level': {'int': 112},
                  'activities.reaction.skills.typeID': {'int': 112},
                  'activities.reaction.time': {'int': 112},
                  'activities.research_material': {'dict': 4326},
                  'activities.research_material.materials': {'dict': 2576,
                                                             'list': 858},
                  'activities.research_material.materials.quantity': {'int': 2576},
                  'activities.research_material.materials.typeID': {'int': 2576},
                  'activities.research_material.skills': {'dict': 3806,
                                                          'list': 1482},
                  'activities.research_material.skills.level': {'int': 3806},
                  'activities.research_material.skills.typeID': {'int': 3806},
                  'activities.research_material.time': {'int': 4326},
                  'activities.research_time': {'dict': 4326},
                  'activities.research_time.materials': {'dict': 2401, 'list': 813},
                  'activities.research_time.materials.quantity': {'int': 2401},
                  'activities.research_time.materials.typeID': {'int': 2401},
                  'activities.research_time.skills': {'dict': 3693, 'list': 1465},
                  'activities.research_time.skills.level': {'int': 3693},
                  'activities.research_time.skills.typeID': {'int': 3693},
                  'activities.research_time.time': {'int': 4326},
                  'blueprintTypeID': {'int': 5031},
                  'maxProductionLimit': {'int': 5031}},
     'source_info': 'SDE file: blueprints.jsonl, build: 3081406'}.
    """

    _key: int
    activities: ActivitiesDict
    blueprintTypeID: int
    maxProductionLimit: int


class CategoriesDict(TypedDict):
    """TypeDict definition for CategoriesDict.

    Total entries analyzed: 47.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: categories.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 47,
     'key_info': {'_key': {'int': 47},
                  'iconID': {'int': 13},
                  'name': {'dict': 47},
                  'name.de': {'str': 47},
                  'name.en': {'str': 47},
                  'name.es': {'str': 47},
                  'name.fr': {'str': 47},
                  'name.ja': {'str': 47},
                  'name.ko': {'str': 47},
                  'name.ru': {'str': 47},
                  'name.zh': {'str': 47},
                  'published': {'bool': 47}},
     'source_info': 'SDE file: categories.jsonl, build: 3081406'}.
    """

    _key: int
    name: LocalizedStringDict
    published: bool
    iconID: NotRequired[int]


class CertificatesDict(TypedDict):
    """TypeDict definition for CertificatesDict.

    Total entries analyzed: 134.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: certificates.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 134,
     'key_info': {'_key': {'int': 134},
                  'description': {'dict': 134},
                  'description.de': {'str': 134},
                  'description.en': {'str': 134},
                  'description.es': {'str': 134},
                  'description.fr': {'str': 134},
                  'description.ja': {'str': 134},
                  'description.ko': {'str': 134},
                  'description.ru': {'str': 134},
                  'description.zh': {'str': 134},
                  'groupID': {'int': 134},
                  'name': {'dict': 134},
                  'name.de': {'str': 134},
                  'name.en': {'str': 134},
                  'name.es': {'str': 134},
                  'name.fr': {'str': 134},
                  'name.ja': {'str': 134},
                  'name.ko': {'str': 134},
                  'name.ru': {'str': 134},
                  'name.zh': {'str': 134},
                  'recommendedFor': {'list': 79},
                  'skillTypes': {'dict': 881, 'list': 134},
                  'skillTypes._key': {'int': 881},
                  'skillTypes.advanced': {'int': 881},
                  'skillTypes.basic': {'int': 881},
                  'skillTypes.elite': {'int': 881},
                  'skillTypes.improved': {'int': 881},
                  'skillTypes.standard': {'int': 881}},
     'source_info': 'SDE file: certificates.jsonl, build: 3081406'}.
    """

    _key: int
    description: LocalizedStringDict
    groupID: int
    name: LocalizedStringDict
    recommendedFor: NotRequired[list[int]]
    skillTypes: list[SkillTypeDict]


class CharacterAttributesDict(TypedDict):
    """TypeDict definition for CharacterAttributesDict.

    Total entries analyzed: 5.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: characterAttributes.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 5,
     'key_info': {'_key': {'int': 5},
                  'description': {'str': 5},
                  'iconID': {'int': 5},
                  'name': {'dict': 5},
                  'name.de': {'str': 5},
                  'name.en': {'str': 5},
                  'name.es': {'str': 5},
                  'name.fr': {'str': 5},
                  'name.ja': {'str': 5},
                  'name.ko': {'str': 5},
                  'name.ru': {'str': 5},
                  'name.zh': {'str': 5},
                  'notes': {'str': 5},
                  'shortDescription': {'str': 5}},
     'source_info': 'SDE file: characterAttributes.jsonl, build: 3081406'}.
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
    Source info: SDE file: contrabandTypes.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 8,
     'key_info': {'_key': {'int': 8},
                  'factions': {'dict': 50, 'list': 8},
                  'factions._key': {'int': 50},
                  'factions.attackMinSec': {'float': 50},
                  'factions.confiscateMinSec': {'float': 50},
                  'factions.fineByValue': {'float': 50},
                  'factions.standingLoss': {'float': 50}},
     'source_info': 'SDE file: contrabandTypes.jsonl, build: 3081406'}.
    """

    _key: int
    factions: list[ContrabandFactionDict]


class ControlTowerResourcesDict(TypedDict):
    """TypeDict definition for ControlTowerResourcesDict.

    Total entries analyzed: 44.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: controlTowerResources.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 44,
     'key_info': {'_key': {'int': 44},
                  'resources': {'dict': 339, 'list': 44},
                  'resources.factionID': {'int': 252},
                  'resources.minSecurityLevel': {'float': 252},
                  'resources.purpose': {'int': 339},
                  'resources.quantity': {'int': 339},
                  'resources.resourceTypeID': {'int': 339}},
     'source_info': 'SDE file: controlTowerResources.jsonl, build: 3081406'}.
    """

    _key: int
    resources: list[CTResourceDict]


class CorporationActivitiesDict(TypedDict):
    """TypeDict definition for CorporationActivitiesDict.

    Total entries analyzed: 20.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: corporationActivities.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 20,
     'key_info': {'_key': {'int': 20},
                  'name': {'dict': 20},
                  'name.de': {'str': 20},
                  'name.en': {'str': 20},
                  'name.es': {'str': 20},
                  'name.fr': {'str': 20},
                  'name.ja': {'str': 20},
                  'name.ko': {'str': 20},
                  'name.ru': {'str': 20},
                  'name.zh': {'str': 20}},
     'source_info': 'SDE file: corporationActivities.jsonl, build: 3081406'}.
    """

    _key: int
    name: LocalizedStringDict


class DebuffCollectionsDict(TypedDict):
    """TypeDict definition for DebuffCollectionsDict.

    Total entries analyzed: 152.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: dbuffCollections.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 152,
     'key_info': {'_key': {'int': 152},
                  'aggregateMode': {'str': 152},
                  'developerDescription': {'str': 152},
                  'displayName': {'dict': 144},
                  'displayName.de': {'str': 144},
                  'displayName.en': {'str': 144},
                  'displayName.es': {'str': 144},
                  'displayName.fr': {'str': 144},
                  'displayName.ja': {'str': 144},
                  'displayName.ko': {'str': 144},
                  'displayName.ru': {'str': 144},
                  'displayName.zh': {'str': 144},
                  'itemModifiers': {'dict': 160, 'list': 97},
                  'itemModifiers.dogmaAttributeID': {'int': 160},
                  'locationGroupModifiers': {'dict': 33, 'list': 9},
                  'locationGroupModifiers.dogmaAttributeID': {'int': 33},
                  'locationGroupModifiers.groupID': {'int': 33},
                  'locationModifiers': {'dict': 29, 'list': 5},
                  'locationModifiers.dogmaAttributeID': {'int': 29},
                  'locationRequiredSkillModifiers': {'dict': 93, 'list': 49},
                  'locationRequiredSkillModifiers.dogmaAttributeID': {'int': 93},
                  'locationRequiredSkillModifiers.skillID': {'int': 93},
                  'operationName': {'str': 152},
                  'showOutputValueInUI': {'str': 152}},
     'source_info': 'SDE file: dbuffCollections.jsonl, build: 3081406'}.
    """

    _key: int
    aggregateMode: str
    developerDescription: str
    itemModifiers: list | dict
    locationGroupModifiers: NotRequired[list[LocationGroupModifierDict]]
    locationModifiers: NotRequired[list[LocationModifierDict]]
    locationRequiredSkillModifiers: NotRequired[list[LocationRequiredSkillModifierDict]]
    operationName: str
    showOutputValueInUI: str
    displayName: NotRequired[LocalizedStringDict]


class DogmaAttributeCategoriesDict(TypedDict):
    """TypeDict definition for DogmaAttributeCategoriesDict.

    Total entries analyzed: 37.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: dogmaAttributeCategories.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 37,
     'key_info': {'_key': {'int': 37},
                  'description': {'str': 36},
                  'name': {'str': 37}},
     'source_info': 'SDE file: dogmaAttributeCategories.jsonl, build: 3081406'}.
    """

    _key: int
    description: NotRequired[str]
    name: str


class DogmaAttributesDict(TypedDict):
    """TypeDict definition for DogmaAttributesDict.

    Total entries analyzed: 2775.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: dogmaAttributes.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 2775,
     'key_info': {'_key': {'int': 2775},
                  'attributeCategoryID': {'int': 2600},
                  'chargeRechargeTimeID': {'int': 6},
                  'dataType': {'int': 2775},
                  'defaultValue': {'float': 2775},
                  'description': {'str': 2606},
                  'displayName': {'dict': 1224},
                  'displayName.de': {'str': 1224},
                  'displayName.en': {'str': 1224},
                  'displayName.es': {'str': 1224},
                  'displayName.fr': {'str': 1224},
                  'displayName.ja': {'str': 1224},
                  'displayName.ko': {'str': 1224},
                  'displayName.ru': {'str': 1224},
                  'displayName.zh': {'str': 1224},
                  'displayWhenZero': {'bool': 2775},
                  'highIsGood': {'bool': 2775},
                  'iconID': {'int': 1342},
                  'maxAttributeID': {'int': 27},
                  'minAttributeID': {'int': 1},
                  'name': {'str': 2775},
                  'published': {'bool': 2775},
                  'stackable': {'bool': 2775},
                  'tooltipDescription': {'dict': 66},
                  'tooltipDescription.de': {'str': 66},
                  'tooltipDescription.en': {'str': 66},
                  'tooltipDescription.es': {'str': 66},
                  'tooltipDescription.fr': {'str': 66},
                  'tooltipDescription.ja': {'str': 66},
                  'tooltipDescription.ko': {'str': 66},
                  'tooltipDescription.ru': {'str': 66},
                  'tooltipDescription.zh': {'str': 66},
                  'tooltipTitle': {'dict': 68},
                  'tooltipTitle.de': {'str': 68},
                  'tooltipTitle.en': {'str': 68},
                  'tooltipTitle.es': {'str': 68},
                  'tooltipTitle.fr': {'str': 68},
                  'tooltipTitle.ja': {'str': 68},
                  'tooltipTitle.ko': {'str': 68},
                  'tooltipTitle.ru': {'str': 68},
                  'tooltipTitle.zh': {'str': 68},
                  'unitID': {'int': 1323}},
     'source_info': 'SDE file: dogmaAttributes.jsonl, build: 3081406'}.
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
    displayName: NotRequired[LocalizedStringDict]
    iconID: NotRequired[int]
    tooltipDescription: NotRequired[LocalizedStringDict]
    tooltipTitle: NotRequired[LocalizedStringDict]
    unitID: NotRequired[int]
    chargeRechargeTimeID: NotRequired[int]
    maxAttributeID: NotRequired[int]
    minAttributeID: NotRequired[int]


class DogmaEffectsDict(TypedDict):
    """TypeDict definition for DogmaEffectsDict.

    Total entries analyzed: 3288.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: dogmaEffects.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 3288,
     'key_info': {'_key': {'int': 3288},
                  'description': {'dict': 747},
                  'description.de': {'str': 745},
                  'description.en': {'str': 747},
                  'description.es': {'str': 745},
                  'description.fr': {'str': 745},
                  'description.ja': {'str': 745},
                  'description.ko': {'str': 745},
                  'description.ru': {'str': 745},
                  'description.zh': {'str': 745},
                  'disallowAutoRepeat': {'bool': 3288},
                  'dischargeAttributeID': {'int': 169},
                  'displayName': {'dict': 69},
                  'displayName.de': {'str': 69},
                  'displayName.en': {'str': 69},
                  'displayName.es': {'str': 69},
                  'displayName.fr': {'str': 69},
                  'displayName.ja': {'str': 69},
                  'displayName.ko': {'str': 69},
                  'displayName.ru': {'str': 69},
                  'displayName.zh': {'str': 69},
                  'distribution': {'int': 74},
                  'durationAttributeID': {'int': 221},
                  'effectCategoryID': {'int': 3288},
                  'electronicChance': {'bool': 3288},
                  'falloffAttributeID': {'int': 51},
                  'fittingUsageChanceAttributeID': {'int': 12},
                  'guid': {'str': 1626},
                  'iconID': {'int': 1268},
                  'isAssistance': {'bool': 3288},
                  'isOffensive': {'bool': 3288},
                  'isWarpSafe': {'bool': 3288},
                  'modifierInfo': {'dict': 4866, 'list': 3073},
                  'modifierInfo.domain': {'str': 4866},
                  'modifierInfo.effectID': {'int': 10},
                  'modifierInfo.func': {'str': 4866},
                  'modifierInfo.groupID': {'int': 781},
                  'modifierInfo.modifiedAttributeID': {'int': 4856},
                  'modifierInfo.modifyingAttributeID': {'int': 4856},
                  'modifierInfo.operation': {'int': 4856},
                  'modifierInfo.skillTypeID': {'int': 2331},
                  'name': {'str': 3288},
                  'npcActivationChanceAttributeID': {'int': 19},
                  'npcUsageChanceAttributeID': {'int': 7},
                  'propulsionChance': {'bool': 3288},
                  'published': {'bool': 3288},
                  'rangeAttributeID': {'int': 195},
                  'rangeChance': {'bool': 3288},
                  'resistanceAttributeID': {'int': 39},
                  'trackingSpeedAttributeID': {'int': 6}},
     'source_info': 'SDE file: dogmaEffects.jsonl, build: 3081406'}.
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
    description: NotRequired[LocalizedStringDict]
    displayName: NotRequired[LocalizedStringDict]
    iconID: NotRequired[int]
    modifierInfo: NotRequired[list[DogmaEffectModifierInfoDict]]
    npcUsageChanceAttributeID: NotRequired[int]
    npcActivationChanceAttributeID: NotRequired[int]
    fittingUsageChanceAttributeID: NotRequired[int]
    resistanceAttributeID: NotRequired[int]


class DogmaUnitsDict(TypedDict):
    """TypeDict definition for DogmaUnitsDict.

    Total entries analyzed: 60.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: dogmaUnits.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 60,
     'key_info': {'_key': {'int': 60},
                  'description': {'dict': 44},
                  'description.de': {'str': 44},
                  'description.en': {'str': 44},
                  'description.es': {'str': 44},
                  'description.fr': {'str': 44},
                  'description.ja': {'str': 44},
                  'description.ko': {'str': 44},
                  'description.ru': {'str': 44},
                  'description.zh': {'str': 44},
                  'displayName': {'dict': 56},
                  'displayName.de': {'str': 56},
                  'displayName.en': {'str': 56},
                  'displayName.es': {'str': 56},
                  'displayName.fr': {'str': 56},
                  'displayName.ja': {'str': 56},
                  'displayName.ko': {'str': 56},
                  'displayName.ru': {'str': 56},
                  'displayName.zh': {'str': 56},
                  'name': {'str': 60}},
     'source_info': 'SDE file: dogmaUnits.jsonl, build: 3081406'}.
    """

    _key: int
    description: NotRequired[LocalizedStringDict]
    displayName: NotRequired[LocalizedStringDict]
    name: str


class DynamicItemAttributesDict(TypedDict):
    """TypeDict definition for DynamicItemAttributesDict.

    Total entries analyzed: 376.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: dynamicItemAttributes.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 376,
     'key_info': {'_key': {'int': 376},
                  'attributeIDs': {'dict': 1800, 'list': 376},
                  'attributeIDs._key': {'int': 1800},
                  'attributeIDs.highIsGood': {'bool': 12},
                  'attributeIDs.max': {'float': 1800},
                  'attributeIDs.min': {'float': 1800},
                  'inputOutputMapping': {'dict': 376, 'list': 376},
                  'inputOutputMapping.applicableTypes': {'list': 376},
                  'inputOutputMapping.resultingType': {'int': 376}},
     'source_info': 'SDE file: dynamicItemAttributes.jsonl, build: 3081406'}.
    """

    _key: int
    attributeIDs: list[AttributeIDDict]
    inputOutputMapping: list[InputOutputMappingDict]


class FactionsDict(TypedDict):
    """TypeDict definition for FactionsDict.

    Total entries analyzed: 27.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: factions.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 27,
     'key_info': {'_key': {'int': 27},
                  'corporationID': {'int': 26},
                  'description': {'dict': 27},
                  'description.de': {'str': 27},
                  'description.en': {'str': 27},
                  'description.es': {'str': 27},
                  'description.fr': {'str': 27},
                  'description.ja': {'str': 27},
                  'description.ko': {'str': 27},
                  'description.ru': {'str': 27},
                  'description.zh': {'str': 27},
                  'flatLogo': {'str': 18},
                  'flatLogoWithName': {'str': 6},
                  'iconID': {'int': 27},
                  'memberRaces': {'list': 27},
                  'militiaCorporationID': {'int': 6},
                  'name': {'dict': 27},
                  'name.de': {'str': 27},
                  'name.en': {'str': 27},
                  'name.es': {'str': 27},
                  'name.fr': {'str': 27},
                  'name.ja': {'str': 27},
                  'name.ko': {'str': 27},
                  'name.ru': {'str': 27},
                  'name.zh': {'str': 27},
                  'shortDescription': {'dict': 4},
                  'shortDescription.de': {'str': 4},
                  'shortDescription.en': {'str': 4},
                  'shortDescription.es': {'str': 4},
                  'shortDescription.fr': {'str': 4},
                  'shortDescription.ja': {'str': 4},
                  'shortDescription.ko': {'str': 4},
                  'shortDescription.ru': {'str': 4},
                  'shortDescription.zh': {'str': 4},
                  'sizeFactor': {'float': 27},
                  'solarSystemID': {'int': 27},
                  'uniqueName': {'bool': 27}},
     'source_info': 'SDE file: factions.jsonl, build: 3081406'}.
    """

    _key: int
    corporationID: NotRequired[int]
    description: LocalizedStringDict
    flatLogo: NotRequired[str]
    flatLogoWithName: NotRequired[str]
    iconID: int
    memberRaces: list[int]
    militiaCorporationID: NotRequired[int]
    name: LocalizedStringDict
    shortDescription: NotRequired[LocalizedStringDict]
    sizeFactor: float
    solarSystemID: int
    uniqueName: bool


class GraphicsDict(TypedDict):
    """TypeDict definition for GraphicsDict.

    Total entries analyzed: 5503.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: graphics.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 5503,
     'key_info': {'_key': {'int': 5503},
                  'graphicFile': {'str': 2351},
                  'iconFolder': {'str': 2565},
                  'sofFactionName': {'str': 3658},
                  'sofHullName': {'str': 3080},
                  'sofLayout': {'list': 53},
                  'sofMaterialSetID': {'int': 90},
                  'sofRaceName': {'str': 3853}},
     'source_info': 'SDE file: graphics.jsonl, build: 3081406'}.
    """

    _key: int
    graphicFile: NotRequired[str]
    iconFolder: NotRequired[str]
    sofFactionName: NotRequired[str]
    sofHullName: NotRequired[str]
    sofRaceName: NotRequired[str]
    sofMaterialSetID: NotRequired[int]
    sofLayout: NotRequired[list[str]]


class GroupsDict(TypedDict):
    """TypeDict definition for GroupsDict.

    Total entries analyzed: 1557.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: groups.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 1557,
     'key_info': {'_key': {'int': 1557},
                  'anchorable': {'bool': 1557},
                  'anchored': {'bool': 1557},
                  'categoryID': {'int': 1557},
                  'fittableNonSingleton': {'bool': 1557},
                  'iconID': {'int': 763},
                  'name': {'dict': 1557},
                  'name.de': {'str': 1557},
                  'name.en': {'str': 1557},
                  'name.es': {'str': 1557},
                  'name.fr': {'str': 1557},
                  'name.ja': {'str': 1557},
                  'name.ko': {'str': 1557},
                  'name.ru': {'str': 1557},
                  'name.zh': {'str': 1557},
                  'published': {'bool': 1557},
                  'useBasePrice': {'bool': 1557}},
     'source_info': 'SDE file: groups.jsonl, build: 3081406'}.
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
    Source info: SDE file: icons.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 4355,
     'key_info': {'_key': {'int': 4355}, 'iconFile': {'str': 4355}},
     'source_info': 'SDE file: icons.jsonl, build: 3081406'}.
    """

    _key: int
    iconFile: str


class LandmarksDict(TypedDict):
    """TypeDict definition for LandmarksDict.

    Total entries analyzed: 45.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: landmarks.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 45,
     'key_info': {'_key': {'int': 45},
                  'description': {'dict': 45},
                  'description.de': {'str': 45},
                  'description.en': {'str': 45},
                  'description.es': {'str': 45},
                  'description.fr': {'str': 45},
                  'description.ja': {'str': 45},
                  'description.ko': {'str': 45},
                  'description.ru': {'str': 45},
                  'description.zh': {'str': 45},
                  'iconID': {'int': 19},
                  'locationID': {'int': 10},
                  'name': {'dict': 45},
                  'name.de': {'str': 45},
                  'name.en': {'str': 45},
                  'name.es': {'str': 45},
                  'name.fr': {'str': 45},
                  'name.ja': {'str': 45},
                  'name.ko': {'str': 45},
                  'name.ru': {'str': 45},
                  'name.zh': {'str': 45},
                  'position': {'dict': 45},
                  'position.x': {'float': 45},
                  'position.y': {'float': 45},
                  'position.z': {'float': 45}},
     'source_info': 'SDE file: landmarks.jsonl, build: 3081406'}.
    """

    _key: int
    description: LocalizedStringDict
    name: LocalizedStringDict
    position: PositionDict
    iconID: NotRequired[int]
    locationID: NotRequired[int]


class MapAsteroidBeltsDict(TypedDict):
    """TypeDict definition for MapAsteroidBeltsDict.

    Total entries analyzed: 40928.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: mapAsteroidBelts.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 40928,
     'key_info': {'_key': {'int': 40928},
                  'celestialIndex': {'int': 40928},
                  'orbitID': {'int': 40928},
                  'orbitIndex': {'int': 40928},
                  'position': {'dict': 40928},
                  'position.x': {'float': 40928},
                  'position.y': {'float': 40928},
                  'position.z': {'float': 40928},
                  'radius': {'float': 40226},
                  'solarSystemID': {'int': 40928},
                  'statistics': {'dict': 40226},
                  'statistics.density': {'float': 40226},
                  'statistics.eccentricity': {'float': 40226},
                  'statistics.escapeVelocity': {'float': 40226},
                  'statistics.locked': {'bool': 40226},
                  'statistics.massDust': {'float': 40226},
                  'statistics.massGas': {'float': 24847},
                  'statistics.orbitPeriod': {'float': 40226},
                  'statistics.orbitRadius': {'float': 40226},
                  'statistics.rotationRate': {'float': 40226},
                  'statistics.spectralClass': {'str': 40226},
                  'statistics.surfaceGravity': {'float': 40226},
                  'statistics.temperature': {'float': 40226},
                  'typeID': {'int': 40928},
                  'uniqueName': {'dict': 46},
                  'uniqueName.de': {'str': 46},
                  'uniqueName.en': {'str': 46},
                  'uniqueName.es': {'str': 46},
                  'uniqueName.fr': {'str': 46},
                  'uniqueName.ja': {'str': 46},
                  'uniqueName.ko': {'str': 46},
                  'uniqueName.ru': {'str': 46},
                  'uniqueName.zh': {'str': 46}},
     'source_info': 'SDE file: mapAsteroidBelts.jsonl, build: 3081406'}.
    """

    _key: int
    celestialIndex: int
    orbitID: int
    orbitIndex: int
    position: PositionDict
    radius: NotRequired[float]
    solarSystemID: int
    statistics: NotRequired[AsteroidBeltStatisticsDict]
    typeID: int
    uniqueName: NotRequired[LocalizedStringDict]


class MapConstellationsDict(TypedDict):
    """TypeDict definition for MapConstellationsDict.

    Total entries analyzed: 1175.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: mapConstellations.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 1175,
     'key_info': {'_key': {'int': 1175},
                  'factionID': {'int': 377},
                  'name': {'dict': 1175},
                  'name.de': {'str': 1175},
                  'name.en': {'str': 1175},
                  'name.es': {'str': 1175},
                  'name.fr': {'str': 1175},
                  'name.ja': {'str': 1175},
                  'name.ko': {'str': 1175},
                  'name.ru': {'str': 1175},
                  'name.zh': {'str': 1175},
                  'position': {'dict': 1175},
                  'position.x': {'float': 1175},
                  'position.y': {'float': 1175},
                  'position.z': {'float': 1175},
                  'regionID': {'int': 1175},
                  'solarSystemIDs': {'list': 1175},
                  'wormholeClassID': {'int': 1141}},
     'source_info': 'SDE file: mapConstellations.jsonl, build: 3081406'}.
    """

    _key: int
    factionID: NotRequired[int]
    name: LocalizedStringDict
    position: PositionDict
    regionID: int
    solarSystemIDs: list[int]
    wormholeClassID: NotRequired[int]


class MapMoonsDict(TypedDict):
    """TypeDict definition for MapMoonsDict.

    Total entries analyzed: 342170.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: mapMoons.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 342170,
     'key_info': {'_key': {'int': 342170},
                  'attributes': {'dict': 342170},
                  'attributes.heightMap1': {'int': 342170},
                  'attributes.heightMap2': {'int': 342170},
                  'attributes.shaderPreset': {'int': 342170},
                  'celestialIndex': {'int': 342170},
                  'npcStationIDs': {'list': 3801},
                  'orbitID': {'int': 342170},
                  'orbitIndex': {'int': 342170},
                  'position': {'dict': 342170},
                  'position.x': {'float': 342170},
                  'position.y': {'float': 342170},
                  'position.z': {'float': 342170},
                  'radius': {'float': 342170},
                  'solarSystemID': {'int': 342170},
                  'statistics': {'dict': 340806},
                  'statistics.density': {'float': 340806},
                  'statistics.eccentricity': {'float': 340806},
                  'statistics.escapeVelocity': {'float': 340806},
                  'statistics.locked': {'bool': 340806},
                  'statistics.massDust': {'float': 340806},
                  'statistics.massGas': {'float': 340805},
                  'statistics.orbitPeriod': {'float': 340806},
                  'statistics.orbitRadius': {'float': 340806},
                  'statistics.pressure': {'float': 340806},
                  'statistics.rotationRate': {'float': 340806},
                  'statistics.spectralClass': {'str': 340806},
                  'statistics.surfaceGravity': {'float': 340806},
                  'statistics.temperature': {'float': 340806},
                  'typeID': {'int': 342170},
                  'uniqueName': {'dict': 137},
                  'uniqueName.de': {'str': 137},
                  'uniqueName.en': {'str': 137},
                  'uniqueName.es': {'str': 137},
                  'uniqueName.fr': {'str': 137},
                  'uniqueName.ja': {'str': 137},
                  'uniqueName.ko': {'str': 137},
                  'uniqueName.ru': {'str': 137},
                  'uniqueName.zh': {'str': 137}},
     'source_info': 'SDE file: mapMoons.jsonl, build: 3081406'}.
    """

    _key: int
    attributes: MoonAttributesDict
    celestialIndex: int
    orbitID: int
    orbitIndex: int
    position: PositionDict
    radius: float
    solarSystemID: int
    statistics: NotRequired[MoonStatisticsDict]
    typeID: int
    npcStationIDs: NotRequired[list[int]]
    uniqueName: NotRequired[LocalizedStringDict]


class MapPlanetsDict(TypedDict):
    """TypeDict definition for MapPlanetsDict.

    Total entries analyzed: 67961.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: mapPlanets.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 67961,
     'key_info': {'_key': {'int': 67961},
                  'asteroidBeltIDs': {'list': 17277},
                  'attributes': {'dict': 67961},
                  'attributes.heightMap1': {'int': 67961},
                  'attributes.heightMap2': {'int': 67961},
                  'attributes.population': {'bool': 67961},
                  'attributes.shaderPreset': {'int': 67961},
                  'celestialIndex': {'int': 67961},
                  'moonIDs': {'list': 51460},
                  'npcStationIDs': {'list': 1098},
                  'orbitID': {'int': 67961},
                  'position': {'dict': 67961},
                  'position.x': {'float': 67961},
                  'position.y': {'float': 67961},
                  'position.z': {'float': 67961},
                  'radius': {'int': 67961},
                  'solarSystemID': {'int': 67961},
                  'statistics': {'dict': 67961},
                  'statistics.density': {'float': 67961},
                  'statistics.eccentricity': {'float': 67961},
                  'statistics.escapeVelocity': {'float': 67961},
                  'statistics.locked': {'bool': 67961},
                  'statistics.massDust': {'float': 67961},
                  'statistics.massGas': {'float': 67577},
                  'statistics.orbitPeriod': {'float': 67577},
                  'statistics.orbitRadius': {'float': 67577},
                  'statistics.pressure': {'float': 67961},
                  'statistics.rotationRate': {'float': 67961},
                  'statistics.spectralClass': {'str': 67961},
                  'statistics.surfaceGravity': {'float': 67912},
                  'statistics.temperature': {'float': 67961},
                  'typeID': {'int': 67961},
                  'uniqueName': {'dict': 43},
                  'uniqueName.de': {'str': 43},
                  'uniqueName.en': {'str': 43},
                  'uniqueName.es': {'str': 43},
                  'uniqueName.fr': {'str': 43},
                  'uniqueName.ja': {'str': 43},
                  'uniqueName.ko': {'str': 43},
                  'uniqueName.ru': {'str': 43},
                  'uniqueName.zh': {'str': 43}},
     'source_info': 'SDE file: mapPlanets.jsonl, build: 3081406'}.
    """

    _key: int
    asteroidBeltIDs: NotRequired[list[int]]
    attributes: PlanetAttributesDict
    celestialIndex: int
    moonIDs: NotRequired[list[int]]
    orbitID: int
    position: dict
    radius: int
    solarSystemID: int
    statistics: NotRequired[PlanetStatisticsDict]
    typeID: int
    npcStationIDs: NotRequired[list[int]]
    uniqueName: NotRequired[LocalizedStringDict]


class MapRegionsDict(TypedDict):
    """TypeDict definition for MapRegionsDict.

    Total entries analyzed: 113.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: mapRegions.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 113,
     'key_info': {'_key': {'int': 113},
                  'constellationIDs': {'list': 113},
                  'description': {'dict': 69},
                  'description.de': {'str': 69},
                  'description.en': {'str': 69},
                  'description.es': {'str': 69},
                  'description.fr': {'str': 69},
                  'description.ja': {'str': 69},
                  'description.ko': {'str': 69},
                  'description.ru': {'str': 69},
                  'description.zh': {'str': 69},
                  'factionID': {'int': 32},
                  'name': {'dict': 113},
                  'name.de': {'str': 113},
                  'name.en': {'str': 113},
                  'name.es': {'str': 113},
                  'name.fr': {'str': 113},
                  'name.ja': {'str': 113},
                  'name.ko': {'str': 113},
                  'name.ru': {'str': 113},
                  'name.zh': {'str': 113},
                  'nebulaID': {'int': 113},
                  'position': {'dict': 113},
                  'position.x': {'float': 113},
                  'position.y': {'float': 113},
                  'position.z': {'float': 113},
                  'wormholeClassID': {'int': 109}},
     'source_info': 'SDE file: mapRegions.jsonl, build: 3081406'}.
    """

    _key: int
    constellationIDs: list
    description: NotRequired[LocalizedStringDict]
    factionID: NotRequired[int]
    name: LocalizedStringDict
    nebulaID: int
    position: PositionDict
    wormholeClassID: NotRequired[int]


class MapSolarSystemsDict(TypedDict):
    """TypeDict definition for MapSolarSystemsDict.

    Total entries analyzed: 8437.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: mapSolarSystems.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 8437,
     'key_info': {'_key': {'int': 8437},
                  'border': {'bool': 1997},
                  'constellationID': {'int': 8437},
                  'corridor': {'bool': 1920},
                  'disallowedAnchorCategories': {'list': 538},
                  'disallowedAnchorGroups': {'list': 26},
                  'factionID': {'int': 16},
                  'fringe': {'bool': 782},
                  'hub': {'bool': 2678},
                  'international': {'bool': 108},
                  'luminosity': {'float': 5431},
                  'name': {'dict': 8437},
                  'name.de': {'str': 8437},
                  'name.en': {'str': 8437},
                  'name.es': {'str': 8437},
                  'name.fr': {'str': 8437},
                  'name.ja': {'str': 8437},
                  'name.ko': {'str': 8437},
                  'name.ru': {'str': 8437},
                  'name.zh': {'str': 8437},
                  'planetIDs': {'list': 8035},
                  'position': {'dict': 8437},
                  'position.x': {'float': 8437},
                  'position.y': {'float': 8437},
                  'position.z': {'float': 8437},
                  'radius': {'float': 8437},
                  'regionID': {'int': 8437},
                  'regional': {'bool': 537},
                  'securityClass': {'str': 5140},
                  'securityStatus': {'float': 8437},
                  'starID': {'int': 8036},
                  'stargateIDs': {'list': 5215},
                  'visualEffect': {'str': 129},
                  'wormholeClassID': {'int': 692}},
     'source_info': 'SDE file: mapSolarSystems.jsonl, build: 3081406'}.
    """

    _key: int
    border: NotRequired[bool]
    constellationID: int
    hub: NotRequired[bool]
    international: NotRequired[bool]
    luminosity: NotRequired[float]
    name: LocalizedStringDict
    planetIDs: NotRequired[list[int]]
    position: PositionDict
    radius: float
    regionID: int
    regional: NotRequired[bool]
    securityClass: NotRequired[str]
    securityStatus: float
    starID: NotRequired[int]
    stargateIDs: NotRequired[list[int]]
    corridor: NotRequired[bool]
    fringe: NotRequired[bool]
    wormholeClassID: NotRequired[int]
    visualEffect: NotRequired[str]
    disallowedAnchorCategories: NotRequired[list[int]]
    disallowedAnchorGroups: NotRequired[list[int]]
    factionID: NotRequired[int]


class MapStargatesDict(TypedDict):
    """TypeDict definition for MapStargatesDict.

    Total entries analyzed: 13776.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: mapStargates.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 13776,
     'key_info': {'_key': {'int': 13776},
                  'destination': {'dict': 13776},
                  'destination.solarSystemID': {'int': 13776},
                  'destination.stargateID': {'int': 13776},
                  'position': {'dict': 13776},
                  'position.x': {'float': 13776},
                  'position.y': {'float': 13776},
                  'position.z': {'float': 13776},
                  'solarSystemID': {'int': 13776},
                  'typeID': {'int': 13776}},
     'source_info': 'SDE file: mapStargates.jsonl, build: 3081406'}.
    """

    _key: int
    destination: StargateDestinationDict
    position: PositionDict
    solarSystemID: int
    typeID: int


class MapStarsDict(TypedDict):
    """TypeDict definition for MapStarsDict.

    Total entries analyzed: 8036.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: mapStars.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 8036,
     'key_info': {'_key': {'int': 8036},
                  'radius': {'int': 8036},
                  'solarSystemID': {'int': 8036},
                  'statistics': {'dict': 8036},
                  'statistics.age': {'float': 8036},
                  'statistics.life': {'float': 8036},
                  'statistics.luminosity': {'float': 8036},
                  'statistics.spectralClass': {'str': 8036},
                  'statistics.temperature': {'float': 8036},
                  'typeID': {'int': 8036}},
     'source_info': 'SDE file: mapStars.jsonl, build: 3081406'}.
    """

    _key: int
    radius: int
    solarSystemID: int
    statistics: StarStatisticsDict
    typeID: int


class MarketGroupsDict(TypedDict):
    """TypeDict definition for MarketGroupsDict.

    Total entries analyzed: 2039.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: marketGroups.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 2039,
     'key_info': {'_key': {'int': 2039},
                  'description': {'dict': 1565},
                  'description.de': {'str': 1564},
                  'description.en': {'str': 1565},
                  'description.es': {'str': 1564},
                  'description.fr': {'str': 1564},
                  'description.ja': {'str': 1564},
                  'description.ko': {'str': 1564},
                  'description.ru': {'str': 1564},
                  'description.zh': {'str': 1564},
                  'hasTypes': {'bool': 2039},
                  'iconID': {'int': 2009},
                  'name': {'dict': 2039},
                  'name.de': {'str': 2038},
                  'name.en': {'str': 2039},
                  'name.es': {'str': 2038},
                  'name.fr': {'str': 2038},
                  'name.ja': {'str': 2038},
                  'name.ko': {'str': 2038},
                  'name.ru': {'str': 2038},
                  'name.zh': {'str': 2038},
                  'parentGroupID': {'int': 2020}},
     'source_info': 'SDE file: marketGroups.jsonl, build: 3081406'}.
    """

    _key: int
    description: NotRequired[LocalizedStringDict]
    hasTypes: bool
    iconID: NotRequired[int]
    name: LocalizedStringDict
    parentGroupID: NotRequired[int]


class MasteriesDict(TypedDict):
    """TypeDict definition for MasteriesDict.

    Total entries analyzed: 460.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: masteries.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 460,
     'key_info': {'_key': {'int': 460},
                  '_value': {'dict': 2300, 'list': 460},
                  '_value._key': {'int': 2300},
                  '_value._value': {'list': 2300}},
     'source_info': 'SDE file: masteries.jsonl, build: 3081406'}.
    """

    _key: int
    _value: list[MasteriesValueDict]


class MetaGroupsDict(TypedDict):
    """TypeDict definition for MetaGroupsDict.

    Total entries analyzed: 13.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: metaGroups.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 13,
     'key_info': {'_key': {'int': 13},
                  'color': {'dict': 10},
                  'color.b': {'float': 10},
                  'color.g': {'float': 10},
                  'color.r': {'float': 10},
                  'description': {'dict': 3},
                  'description.de': {'str': 3},
                  'description.en': {'str': 3},
                  'description.es': {'str': 3},
                  'description.fr': {'str': 3},
                  'description.ja': {'str': 3},
                  'description.ko': {'str': 3},
                  'description.ru': {'str': 3},
                  'description.zh': {'str': 3},
                  'iconID': {'int': 12},
                  'iconSuffix': {'str': 12},
                  'name': {'dict': 13},
                  'name.de': {'str': 13},
                  'name.en': {'str': 13},
                  'name.es': {'str': 13},
                  'name.fr': {'str': 13},
                  'name.ja': {'str': 13},
                  'name.ko': {'str': 13},
                  'name.ru': {'str': 13},
                  'name.zh': {'str': 13}},
     'source_info': 'SDE file: metaGroups.jsonl, build: 3081406'}.
    """

    _key: int
    color: NotRequired[ColorDict]
    name: LocalizedStringDict
    iconID: NotRequired[int]
    iconSuffix: NotRequired[str]
    description: NotRequired[LocalizedStringDict]


class NpcCharactersDict(TypedDict):
    """TypeDict definition for NpcCharactersDict.

    Total entries analyzed: 11302.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: npcCharacters.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 11302,
     'key_info': {'_key': {'int': 11302},
                  'agent': {'dict': 10878},
                  'agent.agentTypeID': {'int': 10878},
                  'agent.divisionID': {'int': 10878},
                  'agent.isLocator': {'bool': 10878},
                  'agent.level': {'int': 10878},
                  'ancestryID': {'int': 11101},
                  'bloodlineID': {'int': 11302},
                  'careerID': {'int': 11098},
                  'ceo': {'bool': 11302},
                  'corporationID': {'int': 11302},
                  'description': {'str': 24},
                  'gender': {'bool': 11302},
                  'locationID': {'int': 11256},
                  'name': {'dict': 11302},
                  'name.de': {'str': 11302},
                  'name.en': {'str': 11302},
                  'name.es': {'str': 11302},
                  'name.fr': {'str': 11302},
                  'name.ja': {'str': 11302},
                  'name.ko': {'str': 11302},
                  'name.ru': {'str': 11302},
                  'name.zh': {'str': 11302},
                  'raceID': {'int': 11302},
                  'schoolID': {'int': 11095},
                  'skills': {'dict': 1145, 'list': 421},
                  'skills.typeID': {'int': 1145},
                  'specialityID': {'int': 11096},
                  'startDate': {'str': 11185},
                  'uniqueName': {'bool': 11302}},
     'source_info': 'SDE file: npcCharacters.jsonl, build: 3081406'}.
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
    skills: NotRequired[list[NpcCharacterSkillsDict]]
    ancestryID: NotRequired[int]
    careerID: NotRequired[int]
    schoolID: NotRequired[int]
    specialityID: NotRequired[int]
    agent: NotRequired[NpcCharacterAgentDict]
    description: NotRequired[str]


class NpcCorporationDivisionsDict(TypedDict):
    """TypeDict definition for NpcCorporationDivisionsDict.

    Total entries analyzed: 10.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: npcCorporationDivisions.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 10,
     'key_info': {'_key': {'int': 10},
                  'description': {'dict': 5},
                  'description.de': {'str': 5},
                  'description.en': {'str': 5},
                  'description.es': {'str': 5},
                  'description.fr': {'str': 5},
                  'description.ja': {'str': 5},
                  'description.ko': {'str': 5},
                  'description.ru': {'str': 5},
                  'description.zh': {'str': 5},
                  'displayName': {'str': 9},
                  'internalName': {'str': 10},
                  'leaderTypeName': {'dict': 10},
                  'leaderTypeName.de': {'str': 10},
                  'leaderTypeName.en': {'str': 10},
                  'leaderTypeName.es': {'str': 10},
                  'leaderTypeName.fr': {'str': 10},
                  'leaderTypeName.ja': {'str': 10},
                  'leaderTypeName.ko': {'str': 10},
                  'leaderTypeName.ru': {'str': 10},
                  'leaderTypeName.zh': {'str': 10},
                  'name': {'dict': 10},
                  'name.de': {'str': 10},
                  'name.en': {'str': 10},
                  'name.es': {'str': 10},
                  'name.fr': {'str': 10},
                  'name.ja': {'str': 10},
                  'name.ko': {'str': 10},
                  'name.ru': {'str': 10},
                  'name.zh': {'str': 10}},
     'source_info': 'SDE file: npcCorporationDivisions.jsonl, build: 3081406'}.
    """

    _key: int
    displayName: NotRequired[str]
    internalName: str
    leaderTypeName: LocalizedStringDict
    name: LocalizedStringDict
    description: NotRequired[LocalizedStringDict]


class NpcCorporationsDict(TypedDict):
    """TypeDict definition for NpcCorporationsDict.

    Total entries analyzed: 283.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: npcCorporations.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 283,
     'key_info': {'_key': {'int': 283},
                  'allowedMemberRaces': {'list': 212},
                  'ceoID': {'int': 260},
                  'corporationTrades': {'dict': 17563, 'list': 184},
                  'corporationTrades._key': {'int': 17563},
                  'corporationTrades._value': {'float': 17563},
                  'deleted': {'bool': 283},
                  'description': {'dict': 280},
                  'description.de': {'str': 279},
                  'description.en': {'str': 280},
                  'description.es': {'str': 280},
                  'description.fr': {'str': 280},
                  'description.ja': {'str': 280},
                  'description.ko': {'str': 280},
                  'description.ru': {'str': 279},
                  'description.zh': {'str': 280},
                  'divisions': {'dict': 251, 'list': 118},
                  'divisions._key': {'int': 251},
                  'divisions.divisionNumber': {'int': 251},
                  'divisions.leaderID': {'int': 251},
                  'divisions.size': {'int': 251},
                  'enemyID': {'int': 250},
                  'exchangeRates': {'dict': 146, 'list': 1},
                  'exchangeRates._key': {'int': 146},
                  'exchangeRates._value': {'float': 146},
                  'extent': {'str': 283},
                  'factionID': {'int': 273},
                  'friendID': {'int': 246},
                  'hasPlayerPersonnelManager': {'bool': 283},
                  'iconID': {'int': 252},
                  'initialPrice': {'int': 283},
                  'investors': {'dict': 406, 'list': 227},
                  'investors._key': {'int': 406},
                  'investors._value': {'int': 406},
                  'lpOfferTables': {'list': 181},
                  'mainActivityID': {'int': 266},
                  'memberLimit': {'int': 283},
                  'minSecurity': {'float': 283},
                  'minimumJoinStanding': {'int': 283},
                  'name': {'dict': 283},
                  'name.de': {'str': 283},
                  'name.en': {'str': 283},
                  'name.es': {'str': 283},
                  'name.fr': {'str': 283},
                  'name.ja': {'str': 283},
                  'name.ko': {'str': 283},
                  'name.ru': {'str': 283},
                  'name.zh': {'str': 283},
                  'raceID': {'int': 257},
                  'secondaryActivityID': {'int': 34},
                  'sendCharTerminationMessage': {'bool': 283},
                  'shares': {'int': 283},
                  'size': {'str': 283},
                  'sizeFactor': {'float': 189},
                  'solarSystemID': {'int': 261},
                  'stationID': {'int': 262},
                  'taxRate': {'float': 283},
                  'tickerName': {'str': 283},
                  'uniqueName': {'bool': 283}},
     'source_info': 'SDE file: npcCorporations.jsonl, build: 3081406'}.
    """

    _key: int
    ceoID: NotRequired[int]
    deleted: bool
    description: NotRequired[LocalizedStringDict]
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
    corporationTrades: list | dict
    divisions: list | dict
    enemyID: NotRequired[int]
    factionID: NotRequired[int]
    friendID: NotRequired[int]
    iconID: NotRequired[int]
    investors: list | dict
    lpOfferTables: NotRequired[list]
    mainActivityID: NotRequired[int]
    raceID: NotRequired[int]
    sizeFactor: NotRequired[float]
    solarSystemID: NotRequired[int]
    secondaryActivityID: NotRequired[int]
    exchangeRates: NotRequired[list | dict]


class NpcStationsDict(TypedDict):
    """TypeDict definition for NpcStationsDict.

    Total entries analyzed: 5154.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: npcStations.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 5154,
     'key_info': {'_key': {'int': 5154},
                  'celestialIndex': {'int': 5153},
                  'operationID': {'int': 5154},
                  'orbitID': {'int': 5154},
                  'orbitIndex': {'int': 3968},
                  'ownerID': {'int': 5154},
                  'position': {'dict': 5154},
                  'position.x': {'float': 5154},
                  'position.y': {'float': 5154},
                  'position.z': {'float': 5154},
                  'reprocessingEfficiency': {'float': 5154},
                  'reprocessingHangarFlag': {'int': 5154},
                  'reprocessingStationsTake': {'float': 5154},
                  'solarSystemID': {'int': 5154},
                  'typeID': {'int': 5154},
                  'useOperationName': {'bool': 5154}},
     'source_info': 'SDE file: npcStations.jsonl, build: 3081406'}.
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
    Source info: SDE file: planetResources.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 25798,
     'key_info': {'_key': {'int': 25798},
                  'cycle_minutes': {'int': 3462},
                  'harvest_silo_max': {'int': 3462},
                  'maturation_cycle_minutes': {'int': 3462},
                  'maturation_percent': {'int': 3462},
                  'mature_silo_max': {'int': 3462},
                  'power': {'int': 12126},
                  'reagent_harvest_amount': {'int': 3462},
                  'reagent_type_id': {'int': 3462},
                  'workforce': {'int': 10210}},
     'source_info': 'SDE file: planetResources.jsonl, build: 3081406'}.
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
    Source info: SDE file: planetSchematics.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 68,
     'key_info': {'_key': {'int': 68},
                  'cycleTime': {'int': 68},
                  'name': {'dict': 68},
                  'name.de': {'str': 68},
                  'name.en': {'str': 68},
                  'name.es': {'str': 68},
                  'name.fr': {'str': 68},
                  'name.ja': {'str': 68},
                  'name.ko': {'str': 68},
                  'name.ru': {'str': 68},
                  'name.zh': {'str': 68},
                  'pins': {'list': 68},
                  'types': {'dict': 203, 'list': 68},
                  'types._key': {'int': 203},
                  'types.isInput': {'bool': 203},
                  'types.quantity': {'int': 203}},
     'source_info': 'SDE file: planetSchematics.jsonl, build: 3081406'}.
    """

    _key: int
    cycleTime: int
    name: LocalizedStringDict
    pins: list
    types: list | dict


class RacesDict(TypedDict):
    """TypeDict definition for RacesDict.

    Total entries analyzed: 11.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: races.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 11,
     'key_info': {'_key': {'int': 11},
                  'description': {'dict': 8},
                  'description.de': {'str': 8},
                  'description.en': {'str': 8},
                  'description.es': {'str': 8},
                  'description.fr': {'str': 8},
                  'description.ja': {'str': 8},
                  'description.ko': {'str': 8},
                  'description.ru': {'str': 8},
                  'description.zh': {'str': 8},
                  'iconID': {'int': 5},
                  'name': {'dict': 11},
                  'name.de': {'str': 11},
                  'name.en': {'str': 11},
                  'name.es': {'str': 11},
                  'name.fr': {'str': 11},
                  'name.ja': {'str': 11},
                  'name.ko': {'str': 11},
                  'name.ru': {'str': 11},
                  'name.zh': {'str': 11},
                  'shipTypeID': {'int': 4},
                  'skills': {'dict': 200, 'list': 4},
                  'skills._key': {'int': 200},
                  'skills._value': {'int': 200}},
     'source_info': 'SDE file: races.jsonl, build: 3081406'}.
    """

    _key: int
    description: NotRequired[LocalizedStringDict]
    iconID: NotRequired[int]
    name: LocalizedStringDict
    shipTypeID: NotRequired[int]
    skills: list | dict


class SdeInfoDict(TypedDict):
    """TypeDict definition for SdeInfoDict.

    Total entries analyzed: 1.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: _sde.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 1,
     'key_info': {'_key': {'str': 1},
                  'buildNumber': {'int': 1},
                  'releaseDate': {'str': 1}},
     'source_info': 'SDE file: _sde.jsonl, build: 3081406'}.
    """

    _key: str
    buildNumber: int
    releaseDate: str


class SkinLicensesDict(TypedDict):
    """TypeDict definition for SkinLicensesDict.

    Total entries analyzed: 11528.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: skinLicenses.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 11528,
     'key_info': {'_key': {'int': 11528},
                  'duration': {'int': 11528},
                  'isSingleUse': {'bool': 4246},
                  'licenseTypeID': {'int': 11528},
                  'skinID': {'int': 11528}},
     'source_info': 'SDE file: skinLicenses.jsonl, build: 3081406'}.
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
    Source info: SDE file: skinMaterials.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 824,
     'key_info': {'_key': {'int': 824},
                  'displayName': {'dict': 822},
                  'displayName.de': {'str': 821},
                  'displayName.en': {'str': 822},
                  'displayName.es': {'str': 821},
                  'displayName.fr': {'str': 821},
                  'displayName.ja': {'str': 821},
                  'displayName.ko': {'str': 817},
                  'displayName.ru': {'str': 821},
                  'displayName.zh': {'str': 821},
                  'materialSetID': {'int': 824}},
     'source_info': 'SDE file: skinMaterials.jsonl, build: 3081406'}.
    """

    _key: int
    displayName: NotRequired[LocalizedStringDict]
    materialSetID: int


class SkinsDict(TypedDict):
    """TypeDict definition for SkinsDict.

    Total entries analyzed: 6699.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: skins.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 6699,
     'key_info': {'_key': {'int': 6699},
                  'allowCCPDevs': {'bool': 6699},
                  'internalName': {'str': 6699},
                  'isStructureSkin': {'bool': 939},
                  'skinDescription': {'dict': 2391},
                  'skinDescription.de': {'str': 2387},
                  'skinDescription.en': {'str': 2391},
                  'skinDescription.es': {'str': 2387},
                  'skinDescription.fr': {'str': 2387},
                  'skinDescription.ja': {'str': 2387},
                  'skinDescription.ko': {'str': 2376},
                  'skinDescription.ru': {'str': 2387},
                  'skinDescription.zh': {'str': 2387},
                  'skinMaterialID': {'int': 6699},
                  'types': {'list': 6699},
                  'visibleSerenity': {'bool': 6699},
                  'visibleTranquility': {'bool': 6699}},
     'source_info': 'SDE file: skins.jsonl, build: 3081406'}.
    """

    _key: int
    allowCCPDevs: bool
    internalName: str
    skinMaterialID: int
    types: list
    visibleSerenity: bool
    visibleTranquility: bool
    isStructureSkin: NotRequired[bool]
    skinDescription: NotRequired[LocalizedStringDict]


class SovereigntyUpgradesDict(TypedDict):
    """TypeDict definition for SovereigntyUpgradesDict.

    Total entries analyzed: 27.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: sovereigntyUpgrades.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 27,
     'key_info': {'_key': {'int': 27},
                  'fuel_hourly_upkeep': {'int': 4},
                  'fuel_startup_cost': {'int': 4},
                  'fuel_type_id': {'int': 4},
                  'mutually_exclusive_group': {'str': 27},
                  'power_allocation': {'int': 27},
                  'workforce_allocation': {'int': 27}},
     'source_info': 'SDE file: sovereigntyUpgrades.jsonl, build: 3081406'}.
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
    Source info: SDE file: stationOperations.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 66,
     'key_info': {'_key': {'int': 66},
                  'activityID': {'int': 66},
                  'border': {'float': 66},
                  'corridor': {'float': 66},
                  'description': {'dict': 54},
                  'description.de': {'str': 54},
                  'description.en': {'str': 54},
                  'description.es': {'str': 54},
                  'description.fr': {'str': 54},
                  'description.ja': {'str': 54},
                  'description.ko': {'str': 54},
                  'description.ru': {'str': 54},
                  'description.zh': {'str': 54},
                  'fringe': {'float': 66},
                  'hub': {'float': 66},
                  'manufacturingFactor': {'float': 66},
                  'operationName': {'dict': 66},
                  'operationName.de': {'str': 66},
                  'operationName.en': {'str': 66},
                  'operationName.es': {'str': 66},
                  'operationName.fr': {'str': 66},
                  'operationName.ja': {'str': 66},
                  'operationName.ko': {'str': 66},
                  'operationName.ru': {'str': 66},
                  'operationName.zh': {'str': 66},
                  'ratio': {'float': 66},
                  'researchFactor': {'float': 66},
                  'services': {'list': 66},
                  'stationTypes': {'dict': 224, 'list': 47},
                  'stationTypes._key': {'int': 224},
                  'stationTypes._value': {'int': 224}},
     'source_info': 'SDE file: stationOperations.jsonl, build: 3081406'}.
    """

    _key: int
    activityID: int
    border: float
    corridor: float
    description: NotRequired[LocalizedStringDict]
    fringe: float
    hub: float
    manufacturingFactor: float
    operationName: LocalizedStringDict
    ratio: float
    researchFactor: float
    services: list
    stationTypes: list | dict


class StationServicesDict(TypedDict):
    """TypeDict definition for StationServicesDict.

    Total entries analyzed: 27.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: stationServices.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 27,
     'key_info': {'_key': {'int': 27},
                  'description': {'dict': 1},
                  'description.de': {'str': 1},
                  'description.en': {'str': 1},
                  'description.es': {'str': 1},
                  'description.fr': {'str': 1},
                  'description.ja': {'str': 1},
                  'description.ko': {'str': 1},
                  'description.ru': {'str': 1},
                  'description.zh': {'str': 1},
                  'serviceName': {'dict': 27},
                  'serviceName.de': {'str': 27},
                  'serviceName.en': {'str': 27},
                  'serviceName.es': {'str': 27},
                  'serviceName.fr': {'str': 27},
                  'serviceName.ja': {'str': 27},
                  'serviceName.ko': {'str': 27},
                  'serviceName.ru': {'str': 27},
                  'serviceName.zh': {'str': 27}},
     'source_info': 'SDE file: stationServices.jsonl, build: 3081406'}.
    """

    _key: int
    serviceName: LocalizedStringDict
    description: NotRequired[LocalizedStringDict]


class TranslationLanguagesDict(TypedDict):
    """TypeDict definition for TranslationLanguagesDict.

    Total entries analyzed: 8.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: translationLanguages.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 8,
     'key_info': {'_key': {'str': 8}, 'name': {'str': 8}},
     'source_info': 'SDE file: translationLanguages.jsonl, build: 3081406'}.
    """

    _key: str
    name: str


class TypeBonusDict(TypedDict):
    """TypeDict definition for TypeBonusDict.

    Total entries analyzed: 628.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: typeBonus.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 628,
     'key_info': {'_key': {'int': 628},
                  'iconID': {'int': 62},
                  'miscBonuses': {'dict': 341, 'list': 71},
                  'miscBonuses.bonus': {'float': 297, 'int': 8},
                  'miscBonuses.bonusText': {'dict': 341},
                  'miscBonuses.bonusText.de': {'str': 341},
                  'miscBonuses.bonusText.en': {'str': 341},
                  'miscBonuses.bonusText.es': {'str': 341},
                  'miscBonuses.bonusText.fr': {'str': 341},
                  'miscBonuses.bonusText.ja': {'str': 341},
                  'miscBonuses.bonusText.ko': {'str': 341},
                  'miscBonuses.bonusText.ru': {'str': 341},
                  'miscBonuses.bonusText.zh': {'str': 341},
                  'miscBonuses.importance': {'int': 341},
                  'miscBonuses.isPositive': {'bool': 268},
                  'miscBonuses.unitID': {'int': 305},
                  'roleBonuses': {'dict': 1763, 'list': 468},
                  'roleBonuses.bonus': {'float': 826, 'int': 280},
                  'roleBonuses.bonusText': {'dict': 1763},
                  'roleBonuses.bonusText.de': {'str': 1763},
                  'roleBonuses.bonusText.en': {'str': 1763},
                  'roleBonuses.bonusText.es': {'str': 1763},
                  'roleBonuses.bonusText.fr': {'str': 1763},
                  'roleBonuses.bonusText.ja': {'str': 1763},
                  'roleBonuses.bonusText.ko': {'str': 1763},
                  'roleBonuses.bonusText.ru': {'str': 1763},
                  'roleBonuses.bonusText.zh': {'str': 1763},
                  'roleBonuses.importance': {'int': 1763},
                  'roleBonuses.unitID': {'int': 1107},
                  'types': {'dict': 761, 'list': 517},
                  'types._key': {'int': 761},
                  'types._value': {'dict': 1598, 'list': 761},
                  'types._value.bonus': {'float': 1045, 'int': 536},
                  'types._value.bonusText': {'dict': 1598},
                  'types._value.bonusText.de': {'str': 1594},
                  'types._value.bonusText.en': {'str': 1598},
                  'types._value.bonusText.es': {'str': 1594},
                  'types._value.bonusText.fr': {'str': 1594},
                  'types._value.bonusText.ja': {'str': 1594},
                  'types._value.bonusText.ko': {'str': 1594},
                  'types._value.bonusText.ru': {'str': 1594},
                  'types._value.bonusText.zh': {'str': 1594},
                  'types._value.importance': {'int': 1598},
                  'types._value.unitID': {'int': 1581}},
     'source_info': 'SDE file: typeBonus.jsonl, build: 3081406'}.
    """

    _key: int
    roleBonuses: list | dict
    types: list | dict
    iconID: NotRequired[int]
    miscBonuses: NotRequired[list | dict]


class TypeDogmaDict(TypedDict):
    """TypeDict definition for TypeDogmaDict.

    Total entries analyzed: 25788.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: typeDogma.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 25788,
     'key_info': {'_key': {'int': 25788},
                  'dogmaAttributes': {'dict': 614971, 'list': 25788},
                  'dogmaAttributes.attributeID': {'int': 614971},
                  'dogmaAttributes.value': {'float': 614971},
                  'dogmaEffects': {'dict': 51969, 'list': 15393},
                  'dogmaEffects.effectID': {'int': 51969},
                  'dogmaEffects.isDefault': {'bool': 51969}},
     'source_info': 'SDE file: typeDogma.jsonl, build: 3081406'}.
    """

    _key: int
    dogmaAttributes: list | dict
    dogmaEffects: list | dict


class TypeMaterialsDict(TypedDict):
    """TypeDict definition for TypeMaterialsDict.

    Total entries analyzed: 9430.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: typeMaterials.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 9430,
     'key_info': {'_key': {'int': 9430},
                  'materials': {'dict': 46392, 'list': 9430},
                  'materials.materialTypeID': {'int': 46392},
                  'materials.quantity': {'int': 46392}},
     'source_info': 'SDE file: typeMaterials.jsonl, build: 3081406'}.
    """

    _key: int
    materials: list[MaterialsMateritalsDict]


class TypesDict(TypedDict):
    """TypeDict definition for TypesDict.

    Total entries analyzed: 50535.
    This TypedDict was auto-generated and only considers top-level keys.
    Source info: SDE file: types.jsonl, build: 3081406.
    Sig info:
    {'dict_count': 50535,
     'key_info': {'_key': {'int': 50535},
                  'basePrice': {'float': 13725},
                  'capacity': {'float': 9450},
                  'description': {'dict': 32726},
                  'description.de': {'str': 32670},
                  'description.en': {'str': 32726},
                  'description.es': {'str': 32671},
                  'description.fr': {'str': 32667},
                  'description.ja': {'str': 32671},
                  'description.ko': {'str': 32667},
                  'description.ru': {'str': 32670},
                  'description.zh': {'str': 32670},
                  'factionID': {'int': 1320},
                  'graphicID': {'int': 17458},
                  'groupID': {'int': 50535},
                  'iconID': {'int': 21967},
                  'marketGroupID': {'int': 18840},
                  'mass': {'float': 20285},
                  'metaGroupID': {'int': 13253},
                  'name': {'dict': 50535},
                  'name.de': {'str': 50469},
                  'name.en': {'str': 50535},
                  'name.es': {'str': 50470},
                  'name.fr': {'str': 50468},
                  'name.ja': {'str': 50470},
                  'name.ko': {'str': 50460},
                  'name.ru': {'str': 50469},
                  'name.zh': {'str': 50471},
                  'portionSize': {'int': 50535},
                  'published': {'bool': 50535},
                  'raceID': {'int': 22508},
                  'radius': {'float': 14867},
                  'soundID': {'int': 4956},
                  'variationParentTypeID': {'int': 4739},
                  'volume': {'float': 45132}},
     'source_info': 'SDE file: types.jsonl, build: 3081406'}.
    """

    _key: int
    groupID: int
    mass: NotRequired[float]
    name: LocalizedStringDict
    portionSize: int
    published: bool
    volume: NotRequired[float]
    radius: NotRequired[float]
    description: NotRequired[LocalizedStringDict]
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
