from pathlib import Path
from yaml import safe_load


class Blueprints:
    def __init__(self, blueprint_yaml_path: Path) -> None:
        with open(blueprint_yaml_path) as file_in:
            self.blueprints_sde = safe_load(file_in)
        pass
