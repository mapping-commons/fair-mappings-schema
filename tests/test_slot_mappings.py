"""Tests for the bundled slot-level SSSOM mapping sets.

Each transformation spec has a companion SSSOM set that records, slot by slot,
how the source format's fields relate to the FAIR Mappings Schema. The two must
describe the same correspondences, so a change to one without the other fails.
"""

import ast
import csv
from pathlib import Path

import pytest
import yaml
from linkml_runtime.utils.schemaview import SchemaView

from fair_mappings_schema.schema import (
    get_linkml_map_schema_path,
    get_slot_mapping_path,
    get_sssom_schema_path,
    get_transformation_path,
)

PURL_BASE = "https://w3id.org/fair-map/"

CASES = {
    "sssom-to-fair": (get_sssom_schema_path, "mapping set"),
    "linkmlmap-to-fair": (get_linkml_map_schema_path, "TransformationSpecification"),
}


def _read_sssom(name: str) -> tuple[dict, list[dict]]:
    lines = Path(get_slot_mapping_path(f"{name}.sssom.tsv")).read_text().splitlines()
    header = "\n".join(line[1:] for line in lines if line.startswith("#"))
    rows = list(csv.DictReader((line for line in lines if not line.startswith("#")), delimiter="\t"))
    return yaml.safe_load(header), rows


def _derived_pairs(name: str) -> set[tuple[str, str]]:
    """(source slot, FAIR slot) pairs derived for MappingSpecification by a transform."""
    schema_path, source_class = CASES[name]
    source_slots = set(SchemaView(schema_path()).class_slots(source_class))
    with open(get_transformation_path(f"{name}.transformation.yaml")) as f:
        spec = yaml.safe_load(f)
    pairs = set()
    for target, derivation in spec["class_derivations"]["MappingSpecification"]["slot_derivations"].items():
        if derivation.get("populated_from"):
            pairs.add((derivation["populated_from"], target))
        elif derivation.get("expr"):
            names = {n.id for n in ast.walk(ast.parse(derivation["expr"])) if isinstance(n, ast.Name)}
            pairs |= {(source, target) for source in names & source_slots}
        # constant `value` derivations (e.g. type) have no source slot
    return pairs


@pytest.mark.parametrize("name", CASES)
def test_slot_mappings_match_transformation(name):
    _, rows = _read_sssom(name)
    listed = {(r["subject_id"].split(":", 1)[1], r["object_id"].split(":", 1)[1]) for r in rows}
    assert listed == _derived_pairs(name)


@pytest.mark.parametrize("name", CASES)
def test_identifiers_are_fair_map_purls(name):
    meta, _ = _read_sssom(name)
    assert meta["mapping_set_id"] == f"{PURL_BASE}mappings/{name}"
    with open(get_transformation_path(f"{name}.transformation.yaml")) as f:
        assert yaml.safe_load(f)["id"] == f"{PURL_BASE}transforms/{name}"


@pytest.mark.parametrize("name", CASES)
def test_curies_use_the_formats_own_namespaces(name):
    meta, rows = _read_sssom(name)
    assert meta["curie_map"]["fairmap"] == PURL_BASE
    schema_path, _ = CASES[name]
    source = SchemaView(schema_path()).schema
    source_prefix = rows[0]["subject_id"].split(":", 1)[0]
    assert meta["curie_map"][source_prefix] == source.prefixes[source.default_prefix].prefix_reference
    assert all(r["object_id"].startswith("fairmap:") for r in rows)
