"""Tests for fair_mappings_schema.parsing — loading, SSSOM TSV, transforms."""

import textwrap
from pathlib import Path

import pytest
import yaml

from fair_mappings_schema.parsing import (
    TRANSFORM_CONFIG,
    load_mapping,
    parse_sssom_tsv,
    transform_to_fair,
)

DATA_DIR_VALID = Path(__file__).parent / "data" / "valid"

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SSSOM_TSV_CONTENT = textwrap.dedent("""\
    #mapping_set_id: https://example.org/mappings/test
    #mapping_set_title: Test Mappings
    #mapping_set_description: A test mapping set
    #license: https://creativecommons.org/licenses/by/4.0/
    #curie_map:
    #  HP: http://purl.obolibrary.org/obo/HP_
    #  MP: http://purl.obolibrary.org/obo/MP_
    subject_id\tsubject_label\tpredicate_id\tobject_id\tobject_label\tmapping_justification
    HP:0000001\tAll\tskos:exactMatch\tMP:0000001\tAll\tsemapv:ManualMappingCuration
""")

LINKML_MAP_SPEC = {
    "id": "https://example.org/transforms/test",
    "title": "Test Transform",
    "description": "A test transformation spec",
    "source_schema": "source.yaml",
    "target_schema": "target.yaml",
    "class_derivations": {"Foo": {"populated_from": "Bar"}},
    "prefixes": {"ex": "https://example.org/"},
}


@pytest.fixture()
def sssom_tsv_file(tmp_path):
    p = tmp_path / "test.sssom.tsv"
    p.write_text(SSSOM_TSV_CONTENT)
    return p


@pytest.fixture()
def linkml_map_file(tmp_path):
    p = tmp_path / "test.transformation.yaml"
    with open(p, "w") as f:
        yaml.dump(LINKML_MAP_SPEC, f)
    return p


@pytest.fixture()
def fair_instance_file(tmp_path):
    data = {"id": "https://example.org/fair", "name": "Test", "type": "other"}
    p = tmp_path / "test.fms.yml"
    with open(p, "w") as f:
        yaml.dump(data, f)
    return p


# ---------------------------------------------------------------------------
# parse_sssom_tsv
# ---------------------------------------------------------------------------

class TestParseSssomTsv:
    def test_parse_from_file(self, sssom_tsv_file):
        meta = parse_sssom_tsv(sssom_tsv_file)
        assert isinstance(meta, dict)
        assert meta.get("mapping_set_id") == "https://example.org/mappings/test"
        assert "license" in meta

    def test_parse_from_lines(self):
        lines = SSSOM_TSV_CONTENT.splitlines()
        meta = parse_sssom_tsv(lines)
        assert meta.get("mapping_set_title") == "Test Mappings"

    def test_no_header_raises(self, tmp_path):
        p = tmp_path / "no_header.tsv"
        p.write_text("col1\tcol2\nval1\tval2\n")
        with pytest.raises(ValueError, match="No #-commented header"):
            parse_sssom_tsv(p)


# ---------------------------------------------------------------------------
# transform_to_fair
# ---------------------------------------------------------------------------

class TestTransformToFair:
    def test_sssom_transform(self):
        data = {
            "mapping_set_id": "https://example.org/test",
            "mapping_set_title": "Test",
            "license": "CC-BY-4.0",
            "subject_source": "HP",
            "object_source": "MP",
        }
        result = transform_to_fair(data, "sssom")
        assert result["type"] == "sssom"
        assert result["id"] == "https://example.org/test"
        assert result["name"] == "Test"

    def test_linkml_map_transform(self):
        work = dict(LINKML_MAP_SPEC)
        result = transform_to_fair(work, "linkml_map")
        assert result["type"] == "linkml_map"
        assert result["id"] == LINKML_MAP_SPEC["id"]
        assert result["name"] == LINKML_MAP_SPEC["title"]

    def test_linkml_map_strips_derivation_keys(self):
        """class_derivations etc. should be stripped before transform."""
        work = dict(LINKML_MAP_SPEC)
        result = transform_to_fair(work, "linkml_map")
        assert "class_derivations" not in result

    def test_unknown_type_raises(self):
        with pytest.raises(KeyError):
            transform_to_fair({}, "nonexistent_type")

    def test_transform_config_keys(self):
        for key in TRANSFORM_CONFIG:
            cfg = TRANSFORM_CONFIG[key]
            assert "source_schema" in cfg
            assert "transform" in cfg
            assert "source_class" in cfg


# ---------------------------------------------------------------------------
# load_mapping
# ---------------------------------------------------------------------------

class TestLoadMapping:
    def test_load_plain_yaml(self, fair_instance_file):
        data = load_mapping(fair_instance_file)
        assert data["id"] == "https://example.org/fair"
        assert data["type"] == "other"

    def test_load_with_linkml_map_transform(self, linkml_map_file):
        data = load_mapping(linkml_map_file, mapping_type="linkml_map")
        assert data["type"] == "linkml_map"
        assert "id" in data

    def test_load_sssom_tsv(self, sssom_tsv_file):
        data = load_mapping(sssom_tsv_file, mapping_type="sssom")
        assert data["type"] == "sssom"
        assert "id" in data

    def test_load_valid_example_as_is(self):
        path = DATA_DIR_VALID / "MappingSpecification-001.yaml"
        data = load_mapping(path)
        assert isinstance(data, dict)
        assert "type" in data

    def test_accepts_path_object(self, fair_instance_file):
        data = load_mapping(Path(fair_instance_file))
        assert data["id"] == "https://example.org/fair"
