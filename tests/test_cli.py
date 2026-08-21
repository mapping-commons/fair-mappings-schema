"""Tests for fair_mappings_schema.cli — Click CLI commands."""

import textwrap
from pathlib import Path

import yaml
from click.testing import CliRunner

from fair_mappings_schema.cli import cli

DATA_DIR_VALID = Path(__file__).parent / "data" / "valid"

SSSOM_TSV_CONTENT = textwrap.dedent("""\
    #mapping_set_id: https://example.org/mappings/cli-test
    #mapping_set_title: CLI Test Mappings
    #license: https://creativecommons.org/licenses/by/4.0/
    #curie_map:
    #  HP: http://purl.obolibrary.org/obo/HP_
    subject_id\tsubject_label\tpredicate_id\tobject_id\tobject_label\tmapping_justification
    HP:0000001\tAll\tskos:exactMatch\tHP:0000001\tAll\tsemapv:ManualMappingCuration
""")

runner = CliRunner()


class TestCLIHelp:
    def test_main_help(self):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "parse" in result.output
        assert "validate" in result.output

    def test_version(self):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "version" in result.output


class TestValidateCommand:
    def test_valid_file(self):
        f = str(DATA_DIR_VALID / "MappingSpecification-001.yaml")
        result = runner.invoke(cli, ["validate", f])
        assert result.exit_code == 0
        assert "OK" in result.output

    def test_invalid_file(self, tmp_path):
        p = tmp_path / "bad.yaml"
        p.write_text(yaml.dump({"author": "not an object"}))
        result = runner.invoke(cli, ["validate", str(p)])
        assert result.exit_code == 1
        assert "INVALID" in result.output

    def test_validate_with_mapping_type(self, tmp_path):
        spec = {
            "id": "https://example.org/t",
            "title": "T",
            "source_schema": "s.yaml",
            "target_schema": "t.yaml",
        }
        p = tmp_path / "spec.yaml"
        p.write_text(yaml.dump(spec))
        result = runner.invoke(cli, ["validate", "-I", "linkml_map", str(p)])
        assert result.exit_code == 0
        assert "OK" in result.output


class TestParseCommand:
    def test_parse_linkml_map(self, tmp_path):
        spec = {
            "id": "https://example.org/t",
            "title": "Test",
            "source_schema": "s.yaml",
            "target_schema": "t.yaml",
        }
        inp = tmp_path / "spec.transformation.yaml"
        inp.write_text(yaml.dump(spec))
        out = tmp_path / "output.fms.yml"

        result = runner.invoke(cli, ["parse", "-I", "linkml_map", str(inp), "-o", str(out)])
        assert result.exit_code == 0
        assert out.exists()
        data = yaml.safe_load(out.read_text())
        assert data["type"] == "linkml_map"

    def test_parse_sssom_tsv(self, tmp_path):
        inp = tmp_path / "test.sssom.tsv"
        inp.write_text(SSSOM_TSV_CONTENT)
        out = tmp_path / "output.fms.yml"

        result = runner.invoke(cli, ["parse", "-I", "sssom", str(inp), "-o", str(out)])
        assert result.exit_code == 0
        data = yaml.safe_load(out.read_text())
        assert data["type"] == "sssom"
        assert data["id"] == "https://example.org/mappings/cli-test"

    def test_parse_default_output_name(self, tmp_path):
        spec = {"id": "x", "title": "T", "source_schema": "s", "target_schema": "t"}
        inp = tmp_path / "myspec.transformation.yaml"
        inp.write_text(yaml.dump(spec))

        result = runner.invoke(cli, ["parse", "-I", "linkml_map", str(inp)])
        assert result.exit_code == 0
        expected = tmp_path / "myspec.fms.yml"
        assert expected.exists()

    def test_parse_requires_mapping_type(self, tmp_path):
        p = tmp_path / "test.yaml"
        p.write_text("{}")
        result = runner.invoke(cli, ["parse", str(p)])
        assert result.exit_code != 0
        assert "Missing" in result.output or "required" in result.output.lower()

    def test_parse_invalid_mapping_type(self, tmp_path):
        p = tmp_path / "test.yaml"
        p.write_text("{}")
        result = runner.invoke(cli, ["parse", "-I", "bogus", str(p)])
        assert result.exit_code != 0


class TestRoundTrip:
    """Parse → validate round-trip."""

    def test_parse_then_validate(self, tmp_path):
        spec = {
            "id": "https://example.org/rt",
            "title": "Round Trip",
            "description": "Testing round trip",
            "source_schema": "s.yaml",
            "target_schema": "t.yaml",
        }
        inp = tmp_path / "spec.yaml"
        inp.write_text(yaml.dump(spec))
        out = tmp_path / "parsed.fms.yml"

        # Parse
        r = runner.invoke(cli, ["parse", "-I", "linkml_map", str(inp), "-o", str(out)])
        assert r.exit_code == 0

        # Validate parsed output (no -I needed)
        r = runner.invoke(cli, ["validate", str(out)])
        assert r.exit_code == 0
        assert "OK" in r.output
