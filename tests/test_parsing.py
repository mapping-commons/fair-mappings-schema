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
from fair_mappings_schema.validation import validate_instance

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

    def test_sssom_creator_ids_and_labels_are_separate_agents(self):
        """creator_id and creator_label are not paired: one of each is two agents."""
        data = {
            "mapping_set_id": "https://example.org/test",
            "creator_id": ["orcid:0000-0002-7356-1779"],
            "creator_label": ["Ada Curator"],
        }
        result = transform_to_fair(data, "sssom")
        assert result["creator"] == [
            {"id": "orcid:0000-0002-7356-1779"},
            {"name": "Ada Curator"},
        ]
        assert validate_instance(result) == []

    def test_sssom_creator_ids_only(self):
        data = {
            "mapping_set_id": "https://example.org/test",
            "creator_id": ["orcid:0000-0002-7356-1779", "orcid:0000-0001-2345-6789"],
        }
        result = transform_to_fair(data, "sssom")
        assert result["creator"] == [
            {"id": "orcid:0000-0002-7356-1779"},
            {"id": "orcid:0000-0001-2345-6789"},
        ]

    def test_sssom_creator_labels_only(self):
        data = {"mapping_set_id": "https://example.org/test", "creator_label": ["Ada Curator"]}
        result = transform_to_fair(data, "sssom")
        assert result["creator"] == [{"name": "Ada Curator"}]
        assert validate_instance(result) == []

    def test_sssom_no_creators(self):
        result = transform_to_fair({"mapping_set_id": "https://example.org/test"}, "sssom")
        assert "creator" not in result

    def test_sssom_mapping_authors_are_not_spec_authors(self, tmp_path):
        """author_id/reviewer_id on a mapping say nothing about the whole specification."""
        p = tmp_path / "authored.sssom.tsv"
        p.write_text(
            SSSOM_TSV_CONTENT.replace("mapping_justification\n", "mapping_justification\tauthor_id\treviewer_id\n")
            .replace("semapv:ManualMappingCuration\n", "semapv:ManualMappingCuration\torcid:1\torcid:2\n")
        )
        data = load_mapping(p, mapping_type="sssom")
        assert "author" not in data
        assert "reviewer" not in data

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

    def test_sssom_dates_become_strings(self, tmp_path):
        """YAML parses unquoted dates in the SSSOM header to date objects."""
        p = tmp_path / "dated.sssom.tsv"
        p.write_text(SSSOM_TSV_CONTENT.replace(
            "#license:",
            "#mapping_set_version: 2026-11-01\n#publication_date: 2026-11-01\n#license:",
        ))
        data = load_mapping(p, mapping_type="sssom")
        assert data["publication_date"] == "2026-11-01"
        assert data["version"] == "2026-11-01"
        assert validate_instance(data) == []

    def test_unquoted_yaml_dates_become_strings(self, tmp_path):
        p = tmp_path / "dated.fms.yml"
        p.write_text("id: x\npublication_date: 2024-06-01\nauthor:\n  - id: y\n    name: 2024-06-01\n")
        data = load_mapping(p)
        assert data["publication_date"] == "2024-06-01"
        assert data["author"][0]["name"] == "2024-06-01"
        assert validate_instance(data) == []
