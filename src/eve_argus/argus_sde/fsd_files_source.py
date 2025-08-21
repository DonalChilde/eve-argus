"""A manifest that represents the file structure of the Eve SDE FSD."""

from hashlib import md5
from pathlib import Path
from typing import TypedDict

from pydantic import BaseModel

from eve_argus.snippets.hash.file_hash import hash_file


class SourceManifestFile(BaseModel):
    manifest_id: str
    name: str
    description: str
    path: Path
    hash: str = ""


class SourceManifestFileTD(TypedDict):
    manifest_id: str
    name: str
    description: str
    path: str
    hash: str


class FsdSourceManifest(BaseModel):
    root_path: Path
    version: str = ""
    """A string used to identify the FSD version. Possibly download date as there is no
    official version information."""
    files: dict[str, SourceManifestFile] = {}


EXPECTED_FILES: dict[str, SourceManifestFileTD] = {
    "agentsInSpace": {
        "manifest_id": "agentsInSpace",
        "name": "Agents In Space",
        "description": "A description for Agents In Space",
        "path": "agentsInSpace.yaml",
        "hash": "",
    },
    "agents": {
        "manifest_id": "agents",
        "name": "Agents",
        "description": "A description for Agents",
        "path": "agents.yaml",
        "hash": "",
    },
    "ancestries": {
        "manifest_id": "ancestries",
        "name": "Ancestries",
        "description": "A description for Ancestries",
        "path": "ancestries.yaml",
        "hash": "",
    },
    "bloodlines": {
        "manifest_id": "bloodlines",
        "name": "Bloodlines",
        "description": "A description for Bloodlines",
        "path": "bloodlines.yaml",
        "hash": "",
    },
    "blueprints": {
        "manifest_id": "blueprints",
        "name": "Blueprints",
        "description": "A description for Blueprints",
        "path": "blueprints.yaml",
        "hash": "",
    },
    "categories": {
        "manifest_id": "categories",
        "name": "Categories",
        "description": "A description for Categories",
        "path": "categories.yaml",
        "hash": "",
    },
    "certificates": {
        "manifest_id": "certificates",
        "name": "Certificates",
        "description": "A description for Certificates",
        "path": "certificates.yaml",
        "hash": "",
    },
    "characterAttributes": {
        "manifest_id": "characterAttributes",
        "name": "Character Attributes",
        "description": "A description for Character Attributes",
        "path": "characterAttributes.yaml",
        "hash": "",
    },
    "contrabandTypes": {
        "manifest_id": "contrabandTypes",
        "name": "Contraband Types",
        "description": "A description for Contraband Types",
        "path": "contrabandTypes.yaml",
        "hash": "",
    },
    "controlTowerResources": {
        "manifest_id": "controlTowerResources",
        "name": "Control Tower Resources",
        "description": "A description for Control Tower Resources",
        "path": "controlTowerResources.yaml",
        "hash": "",
    },
    "corporationActivities": {
        "manifest_id": "corporationActivities",
        "name": "Corporation Activities",
        "description": "A description for Corporation Activities",
        "path": "corporationActivities.yaml",
        "hash": "",
    },
    "dogmaAttributeCategories": {
        "manifest_id": "dogmaAttributeCategories",
        "name": "Dogma Attribute Categories",
        "description": "A description for Dogma Attribute Categories",
        "path": "dogmaAttributeCategories.yaml",
        "hash": "",
    },
    "dogmaAttributes": {
        "manifest_id": "dogmaAttributes",
        "name": "Dogma Attributes",
        "description": "A description for Dogma Attributes",
        "path": "dogmaAttributes.yaml",
        "hash": "",
    },
    "dogmaEffects": {
        "manifest_id": "dogmaEffects",
        "name": "Dogma Effects",
        "description": "A description for Dogma Effects",
        "path": "dogmaEffects.yaml",
        "hash": "",
    },
    "factions": {
        "manifest_id": "factions",
        "name": "Factions",
        "description": "A description for Factions",
        "path": "factions.yaml",
        "hash": "",
    },
    "graphicIDs": {
        "manifest_id": "graphicIDs",
        "name": "Graphic IDs",
        "description": "A description for Graphic IDs",
        "path": "graphicIDs.yaml",
        "hash": "",
    },
    "groups": {
        "manifest_id": "groups",
        "name": "Groups",
        "description": "A description for Groups",
        "path": "groups.yaml",
        "hash": "",
    },
    "iconIDs": {
        "manifest_id": "iconIDs",
        "name": "Icon IDs",
        "description": "A description for Icon IDs",
        "path": "iconIDs.yaml",
        "hash": "",
    },
    "marketGroups": {
        "manifest_id": "marketGroups",
        "name": "Market Groups",
        "description": "A description for Market Groups",
        "path": "marketGroups.yaml",
        "hash": "",
    },
    "metaGroups": {
        "manifest_id": "metaGroups",
        "name": "Meta Groups",
        "description": "A description for Meta Groups",
        "path": "metaGroups.yaml",
        "hash": "",
    },
    "npcCorporationDivisions": {
        "manifest_id": "npcCorporationDivisions",
        "name": "NPC Corporation Divisions",
        "description": "A description for NPC Corporation Divisions",
        "path": "npcCorporationDivisions.yaml",
        "hash": "",
    },
    "npcCorporations": {
        "manifest_id": "npcCorporations",
        "name": "NPC Corporations",
        "description": "A description for NPC Corporations",
        "path": "npcCorporations.yaml",
        "hash": "",
    },
    "planetResources": {
        "manifest_id": "planetResources",
        "name": "Planet Resources",
        "description": "A description for Planet Resources",
        "path": "planetResources.yaml",
        "hash": "",
    },
    "planetSchematics": {
        "manifest_id": "planetSchematics",
        "name": "Planet Schematics",
        "description": "A description for Planet Schematics",
        "path": "planetSchematics.yaml",
        "hash": "",
    },
    "races": {
        "manifest_id": "races",
        "name": "Races",
        "description": "A description for Races",
        "path": "races.yaml",
        "hash": "",
    },
    "researchAgents": {
        "manifest_id": "researchAgents",
        "name": "Research Agents",
        "description": "A description for Research Agents",
        "path": "researchAgents.yaml",
        "hash": "",
    },
    "skinLicenses": {
        "manifest_id": "skinLicenses",
        "name": "Skin Licenses",
        "description": "A description for Skin Licenses",
        "path": "skinLicenses.yaml",
        "hash": "",
    },
    "skinMaterials": {
        "manifest_id": "skinMaterials",
        "name": "Skin Materials",
        "description": "A description for Skin Materials",
        "path": "skinMaterials.yaml",
        "hash": "",
    },
    "skins": {
        "manifest_id": "skins",
        "name": "Skins",
        "description": "A description for Skins",
        "path": "skins.yaml",
        "hash": "",
    },
    "sovereigntyUpgrades": {
        "manifest_id": "sovereigntyUpgrades",
        "name": "Sovereignty Upgrades",
        "description": "A description for Sovereignty Upgrades",
        "path": "sovereigntyUpgrades.yaml",
        "hash": "",
    },
    "stationOperations": {
        "manifest_id": "stationOperations",
        "name": "Station Operations",
        "description": "A description for Station Operations",
        "path": "stationOperations.yaml",
        "hash": "",
    },
    "stationServices": {
        "manifest_id": "stationServices",
        "name": "Station Services",
        "description": "A description for Station Services",
        "path": "stationServices.yaml",
        "hash": "",
    },
    "tournamentRuleSets": {
        "manifest_id": "tournamentRuleSets",
        "name": "Tournament Rule Sets",
        "description": "A description for Tournament Rule Sets",
        "path": "tournamentRuleSets.yaml",
        "hash": "",
    },
    "translationLanguages": {
        "manifest_id": "translationLanguages",
        "name": "Translation Languages",
        "description": "A description for Translation Languages",
        "path": "translationLanguages.yaml",
        "hash": "",
    },
    "typeDogma": {
        "manifest_id": "typeDogma",
        "name": "Type Dogma",
        "description": "A description for Type Dogma",
        "path": "typeDogma.yaml",
        "hash": "",
    },
    "typeMaterials": {
        "manifest_id": "typeMaterials",
        "name": "Type Materials",
        "description": "A description for Type Materials",
        "path": "typeMaterials.yaml",
        "hash": "",
    },
    "types": {
        "manifest_id": "types",
        "name": "Types",
        "description": "A description for Types",
        "path": "types.yaml",
        "hash": "",
    },
}


def new_manifest(source_path: Path, version: str = "") -> FsdSourceManifest:
    """Create a new FSD source manifest with expected files."""
    manifest = FsdSourceManifest(root_path=source_path, version=version)
    for key, value in EXPECTED_FILES.items():
        manifest.files[key] = SourceManifestFile(
            manifest_id=value["manifest_id"],
            name=value["name"],
            description=value["description"],
            path=Path(value["path"]),
            hash=value["hash"],
        )
    return manifest


def verify_files_present(manifest: FsdSourceManifest) -> None:
    """Verify that all expected files are present in the FSD source manifest."""
    missing_files = [
        file.name for file in manifest.files.values() if not file.path.exists()
    ]
    if missing_files:
        raise FileNotFoundError(
            f"FSD directory {manifest.root_path} is missing files: {', '.join(missing_files)}"
        )


def calculate_manifest_hashes(manifest: FsdSourceManifest) -> None:
    """Update the hashes of the files in the FSD source manifest."""
    for file in manifest.files.values():
        file.hash = hash_file(file.path, hasher=md5())


def verify_file_hashes(manifest: FsdSourceManifest) -> None:
    """Verify that the hashes of the files in the FSD source manifest match the expected values."""
    mismatched_files = [
        file.name
        for file in manifest.files.values()
        if file.hash != hash_file(file.path, hasher=md5())
    ]
    if mismatched_files:
        raise ValueError(
            f"FSD Directory {manifest.root_path} hash mismatch for files: {', '.join(mismatched_files)}"
        )


# TODO refine this before use, needs better error message to identify the difference between manifests
def compare_hashes(
    manifest: FsdSourceManifest, compare_with: FsdSourceManifest
) -> None:
    """Compare the hashes of the files in two FSD source manifests."""
    mismatched_files = [
        file.name
        for file in manifest.files.values()
        if file.hash != compare_with.files.get(file.name, "").hash  # type: ignore
    ]
    if mismatched_files:
        raise ValueError(
            f"FSD Directory {manifest.root_path} hash mismatch for files: {', '.join(mismatched_files)}"
        )
