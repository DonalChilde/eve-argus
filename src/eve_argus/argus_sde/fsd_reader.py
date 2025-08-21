from pathlib import Path
from typing import Any, Self

from yaml import safe_load

from eve_argus.argus_sde.fsd_files_source import (
    FsdSourceManifest,
    calculate_manifest_hashes,
    new_manifest,
)


class FsdReader:
    def __init__(self, manifest: FsdSourceManifest):
        self.manifest = manifest

    @classmethod
    def from_path(cls, source_dir: Path, version: str) -> Self:
        """Create an EveSdeFsdReader from a directory path.

        Generates a new manifest.
        """
        manifest = new_manifest(source_dir, version)
        calculate_manifest_hashes(manifest)
        return cls(manifest=manifest)

    def available_files(self) -> str:
        """List available files in the manifest."""
        # FIXME this is meant for use with cli, output format probably needs changing.
        return "\n".join(
            f"{file.manifest_id} - {file.description}"
            for file in self.manifest.files.values()
        )

    def get_file(self, manifest_id: str) -> Any:
        """Get a file from the manifest by its ID."""
        if manifest_id not in self.manifest.files:
            raise ValueError(f"File with ID {manifest_id} not found in manifest.")
        file_path = self.manifest.root_path / self.manifest.files[manifest_id].path
        if not file_path.is_file():
            raise FileNotFoundError(
                f"File {file_path} does not exist or is not a file."
            )
        with file_path.open("r", encoding="utf-8") as file_handle:
            result = safe_load(file_handle)
        return result
