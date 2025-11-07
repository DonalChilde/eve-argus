"""Access the SDE stored as raw JSONL files."""

from collections.abc import Iterable
from enum import StrEnum
from pathlib import Path
from typing import Any

from eve_argus.helpers.jsonl_reader import read_jsonl_dicts
from eve_argus.sde.sde_access_protocol import SdeAccessProtocol


class SdeFileNames(StrEnum):
    AGENTS_IN_SPACE = "agentsInSpace.jsonl"
    AGENT_TYPES = "agentTypes.jsonl"
    ANCESTRIES = "ancestries.jsonl"
    BLOODLINES = "bloodlines.jsonl"
    BLUEPRINTS = "blueprints.jsonl"
    CATEGORIES = "categories.jsonl"
    CERTIFICATES = "certificates.jsonl"
    CHARACTER_ATTRIBUTES = "characterAttributes.jsonl"
    CONTRABAND_TYPES = "contrabandTypes.jsonl"
    CONTROL_TOWER_RESOURCES = "controlTowerResources.jsonl"
    CORPORATION_ACTIVITIES = "corporationActivities.jsonl"
    DEBUFF_COLLECTIONS = "dbuffCollections.jsonl"
    DOGMA_ATTRIBUTE_CATEGORIES = "dogmaAttributeCategories.jsonl"
    DOGMA_ATTRIBUTES = "dogmaAttributes.jsonl"
    DOGMA_EFFECTS = "dogmaEffects.jsonl"
    DOGMA_UNITS = "dogmaUnits.jsonl"
    DYNAMIC_ITEM_ATTRIBUTES = "dynamicItemAttributes.jsonl"
    FACTIONS = "factions.jsonl"
    GRAPHICS = "graphics.jsonl"
    GROUPS = "groups.jsonl"
    ICONS = "icons.jsonl"
    LANDMARKS = "landmarks.jsonl"
    MAP_ASTEROID_BELTS = "mapAsteroidBelts.jsonl"
    MAP_CONSTELLATIONS = "mapConstellations.jsonl"
    MAP_MOONS = "mapMoons.jsonl"
    MAP_PLANETS = "mapPlanets.jsonl"
    MAP_REGIONS = "mapRegions.jsonl"
    MAP_SOLAR_SYSTEMS = "mapSolarSystems.jsonl"
    MAP_STARGATES = "mapStargates.jsonl"
    MAP_STARS = "mapStars.jsonl"
    MARKET_GROUPS = "marketGroups.jsonl"
    MASTERIES = "masteries.jsonl"
    META_GROUPS = "metaGroups.jsonl"
    NPC_CHARACTERS = "npcCharacters.jsonl"
    NPC_CORPORATION_DIVISIONS = "npcCorporationDivisions.jsonl"
    NPC_CORPORATIONS = "npcCorporations.jsonl"
    NPC_STATIONS = "npcStations.jsonl"
    PLANET_RESOURCES = "planetResources.jsonl"
    PLANET_SCHEMATICS = "planetSchematics.jsonl"
    RACES = "races.jsonl"
    SDE_INFO = "_sde.jsonl"
    SKIN_LICENSES = "skinLicenses.jsonl"
    SKIN_MATERIALS = "skinMaterials.jsonl"
    SKINS = "skins.jsonl"
    SOVEREIGNTY_UPGRADES = "sovereigntyUpgrades.jsonl"
    STATION_OPERATIONS = "stationOperations.jsonl"
    STATION_SERVICES = "stationServices.jsonl"
    TRANSLATION_LANGUAGES = "translationLanguages.jsonl"
    TYPE_BONUS = "typeBonus.jsonl"
    TYPE_DOGMA = "typeDogma.jsonl"
    TYPE_MATERIALS = "typeMaterials.jsonl"
    TYPES = "types.jsonl"


class RawJsonAccess(SdeAccessProtocol):
    def __init__(self, sde_directory: Path) -> None:
        """Initialize the RawJsonAccess with the SDE directory."""
        self.sde_directory = sde_directory

    def jsonl_iter(self, sde_file: SdeFileNames) -> Iterable[dict[str, Any]]:
        """Get an iterator over the JSON objects in a JSONL SDE file.

        Args:
            sde_file: The SDE file to read.

        Returns:
            An iterator over the JSON objects in the file.
        """
        file_path = self.sde_directory / sde_file
        if not file_path.exists():
            raise FileNotFoundError(f"SDE file not found at {file_path}")
        return read_jsonl_dicts(file_path)

    def build_number(self) -> int:
        """Get the SDE build number.

        Returns:
            The SDE build number as an integer.
        """
        info = next(iter(self.jsonl_iter(SdeFileNames.SDE_INFO)))
        build_number = info.get("buildNumber")
        if build_number is None:
            raise ValueError("Build number not found in SDE info file")
        return int(build_number)

    def blueprints(self) -> Iterable[dict[str, Any]]:
        """Get an iterator over the blueprints in the SDE.

        Returns:
            An iterator over the blueprint JSON objects.
        """
        return self.jsonl_iter(SdeFileNames.BLUEPRINTS)

    def sde_info(self) -> dict:
        """Get the SDE info as a dictionary."""
        info = next(iter(self.jsonl_iter(SdeFileNames.SDE_INFO)))
        return info
