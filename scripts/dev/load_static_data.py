# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

from pathlib import Path

from esi_link.logging_config import setup_logging
from eve_static_data.raw_jsonl_access import RawJsonFileAccess
from eve_static_data.sde_access_protocol import SdeFileNames

from eve_argus.models import static_data as SD

SCRIPT_NAME = "stub_script"
STATIC_DATA_DIR = Path.home() / "Downloads/eve-online-static-data-3110079-jsonl"
ARGUS_STATIC_DATA_DIR = Path.home() / "projects/tmp/argus_static_data"


def main() -> None:
    access = RawJsonFileAccess(STATIC_DATA_DIR)
    sde_info(access=access, argus_dir=ARGUS_STATIC_DATA_DIR, file_name="sde_info.json")
    regions(access=access, argus_dir=ARGUS_STATIC_DATA_DIR, file_name="regions.json")

    eve_types(
        access=access,
        argus_dir=ARGUS_STATIC_DATA_DIR,
        file_name="eve_types_published.json",
        localized="en",
        only_published=True,
    )
    # eve_types(
    #     access=access,
    #     argus_dir=ARGUS_STATIC_DATA_DIR,
    #     file_name="eve_types_all.json",
    #     localized="en",
    #     only_published=False,
    # )
    blueprints(
        access=access,
        argus_dir=ARGUS_STATIC_DATA_DIR,
        file_name="blueprints.json",
        only_published=True,
    )
    categories(
        access=access,
        argus_dir=ARGUS_STATIC_DATA_DIR,
        file_name="categories.json",
        localized="en",
        only_published=True,
    )
    groups(
        access=access,
        argus_dir=ARGUS_STATIC_DATA_DIR,
        file_name="groups.json",
        localized="en",
        only_published=True,
    )
    market_groups(
        access=access,
        argus_dir=ARGUS_STATIC_DATA_DIR,
        file_name="market_groups.json",
        localized="en",
    )
    meta_groups(
        access=access,
        argus_dir=ARGUS_STATIC_DATA_DIR,
        file_name="meta_groups.json",
        localized="en",
    )
    type_materials(
        access=access,
        argus_dir=ARGUS_STATIC_DATA_DIR,
        file_name="type_materials.json",
    )


def sde_info(access: RawJsonFileAccess, argus_dir: Path, file_name: str) -> None:
    argus_info = SD.SdeInfo.from_sap(access=access)
    file_out = argus_dir / file_name
    argus_info.save_to_disk(file_out, overwrite=True)
    print(f"Wrote SDE info to {file_out}")


def regions(access: RawJsonFileAccess, argus_dir: Path, file_name: str) -> None:
    regions = SD.Regions.from_sap(access=access, localized="en")
    file_out = argus_dir / file_name
    regions.save_to_disk(file_out, overwrite=True)
    print(f"Wrote Regions to {file_out}")


def eve_types(
    access: RawJsonFileAccess,
    argus_dir: Path,
    file_name: str,
    localized: str,
    only_published: bool,
) -> None:
    eve_types = SD.EveTypes.from_sap(
        access=access, localized=localized, only_published=only_published
    )
    file_out = argus_dir / file_name
    eve_types.save_to_disk(file_out, overwrite=True)
    print(f"Wrote Eve Types to {file_out}")


def blueprints(
    access: RawJsonFileAccess, argus_dir: Path, file_name: str, only_published: bool
) -> None:
    blueprints = SD.Blueprints.from_sap(access=access, only_published=only_published)
    file_out = argus_dir / file_name
    blueprints.save_to_disk(file_out, overwrite=True)
    print(f"Wrote Blueprints to {file_out}")


def categories(
    access: RawJsonFileAccess,
    argus_dir: Path,
    file_name: str,
    localized: str,
    only_published: bool,
) -> None:
    categories = SD.Categories.from_sap(
        access=access, localized=localized, only_published=only_published
    )
    file_out = argus_dir / file_name
    categories.save_to_disk(file_out, overwrite=True)
    print(f"Wrote Categories to {file_out}")


def groups(
    access: RawJsonFileAccess,
    argus_dir: Path,
    file_name: str,
    localized: str,
    only_published: bool,
) -> None:
    groups = SD.Groups.from_sap(
        access=access, localized=localized, only_published=only_published
    )
    file_out = argus_dir / file_name
    groups.save_to_disk(file_out, overwrite=True)
    print(f"Wrote Groups to {file_out}")


def market_groups(
    access: RawJsonFileAccess,
    argus_dir: Path,
    file_name: str,
    localized: str,
) -> None:
    market_groups = SD.MarketGroups.from_sap(access=access, localized=localized)
    file_out = argus_dir / file_name
    market_groups.save_to_disk(file_out, overwrite=True)
    print(f"Wrote Market Groups to {file_out}")


def meta_groups(
    access: RawJsonFileAccess,
    argus_dir: Path,
    file_name: str,
    localized: str,
) -> None:
    meta_groups = SD.MetaGroups.from_sap(access=access, localized=localized)
    file_out = argus_dir / file_name
    meta_groups.save_to_disk(file_out, overwrite=True)
    print(f"Wrote Meta Groups to {file_out}")


def type_materials(
    access: RawJsonFileAccess,
    argus_dir: Path,
    file_name: str,
) -> None:
    type_materials = SD.TypeMaterials.from_sap(access=access)
    file_out = argus_dir / file_name
    type_materials.save_to_disk(file_out, overwrite=True)
    print(f"Wrote Type Materials to {file_out}")


if __name__ == "__main__":
    log_dir = Path(f"./logs/script_logs/{SCRIPT_NAME}").resolve()
    print(f"Logging to {log_dir}")
    setup_logging(log_dir)
    main()
