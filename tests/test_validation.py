"""Tests for fair_mappings_schema.validation — schema validation."""

import glob
from pathlib import Path

import pytest
import yaml

from fair_mappings_schema.validation import validate_instance

DATA_DIR_VALID = Path(__file__).parent / "data" / "valid"
DATA_DIR_INVALID = Path(__file__).parent / "data" / "invalid"

VALID_FILES = sorted(glob.glob(str(DATA_DIR_VALID / "*.yaml")))
INVALID_FILES = sorted(glob.glob(str(DATA_DIR_INVALID / "*.yaml")))

# Instance paths each invalid fixture must fail on, and nothing else, so a fixture
# rejected for an unrelated reason (e.g. a stray key) cannot pass as a counter example.
EXPECTED_ERROR_PATHS = {
    "MappingSpecification-001.yaml": {"/author/0"},
    "MappingSpecification-002.yaml": {"/subject_source"},
    "MappingSpecification-003.yaml": {"/creator/0", "/creator/1"},
}


def _load(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f) or {}


class TestValidInstances:
    @pytest.mark.parametrize("filepath", VALID_FILES, ids=lambda p: Path(p).name)
    def test_valid_files_pass(self, filepath):
        data = _load(filepath)
        errors = validate_instance(data)
        assert errors == [], f"Expected valid but got: {errors}"


class TestInvalidInstances:
    @pytest.mark.parametrize("filepath", INVALID_FILES, ids=lambda p: Path(p).name)
    def test_invalid_files_fail(self, filepath):
        data = _load(filepath)
        errors = validate_instance(data)
        assert len(errors) > 0, "Expected validation errors"
        error_paths = {error.rsplit(" in ", 1)[-1] for error in errors}
        assert error_paths == EXPECTED_ERROR_PATHS[Path(filepath).name], errors


class TestValidationAPI:
    def test_empty_dict_is_valid(self):
        errors = validate_instance({})
        assert errors == []

    def test_string_author_is_invalid(self):
        errors = validate_instance({"author": "not an object"})
        assert len(errors) > 0

    def test_valid_minimal(self):
        errors = validate_instance({"id": "x", "type": "sssom"})
        assert errors == []

    def test_custom_schema_path(self):
        from fair_mappings_schema.schema import get_schema_path

        errors = validate_instance(
            {"id": "x"}, schema_path=get_schema_path(),
        )
        assert errors == []
