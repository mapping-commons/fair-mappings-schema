from pathlib import Path
from .fair_mappings_schema import *  # noqa:F403

THIS_PATH = Path(__file__).parent

SCHEMA_DIRECTORY = THIS_PATH.parent / "schema"
MAIN_SCHEMA_PATH = SCHEMA_DIRECTORY / "fair_mappings_schema.yaml"
