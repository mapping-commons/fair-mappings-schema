"""CLI for fair-mappings: parse and validate mapping specifications."""

from __future__ import annotations

import sys
from pathlib import Path

import click
import yaml

from fair_mappings_schema.parsing import load_mapping
from fair_mappings_schema.schema import get_mapping_type_choices
from fair_mappings_schema.validation import validate_instance

# ---------------------------------------------------------------------------
# Shared Click type for -I / --mapping-type
# ---------------------------------------------------------------------------

_MAPPING_TYPE_CHOICES: list[str] | None = None


def _get_type_choices() -> list[str]:
    global _MAPPING_TYPE_CHOICES
    if _MAPPING_TYPE_CHOICES is None:
        _MAPPING_TYPE_CHOICES = get_mapping_type_choices()
    return _MAPPING_TYPE_CHOICES


class MappingTypeChoice(click.ParamType):
    """Click parameter type validated against MappingSpecificationTypeEnum."""
    name = "mapping_type"

    def get_metavar(self, param):
        return "[" + "|".join(_get_type_choices()) + "]"

    def convert(self, value, param, ctx):
        choices = _get_type_choices()
        if value not in choices:
            self.fail(
                f"Invalid mapping type '{value}'. "
                f"Choose from: {', '.join(choices)}",
                param, ctx,
            )
        return value


MAPPING_TYPE = MappingTypeChoice()

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

@click.group()
@click.version_option(package_name="fair-mappings")
def cli():
    """FAIR Mappings Schema tools: parse and validate mapping specifications."""


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "-I", "--mapping-type", type=MAPPING_TYPE, required=True,
    help="Input mapping type (e.g. sssom, linkml_map).",
)
@click.option(
    "-o", "--output", "output_file", default=None, type=click.Path(),
    help="Output file path (default: <input_stem>.fms.yml).",
)
def parse(input_file: str, mapping_type: str, output_file: str | None):
    """Parse a mapping specification into FAIR Mappings Schema format."""
    data = load_mapping(input_file, mapping_type)

    if output_file is None:
        stem = Path(input_file).stem
        if "." in stem:
            stem = stem.rsplit(".", 1)[0]
        output_file = str(Path(input_file).parent / f"{stem}.fms.yml")

    with open(output_file, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    click.echo(f"Wrote {output_file}")


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "-I", "--mapping-type", type=MAPPING_TYPE, default=None,
    help="Input mapping type. If set, transforms before validating.",
)
@click.option(
    "--schema", "schema_path", default=None, type=click.Path(exists=True),
    help="Path to FAIR Mappings schema YAML (default: bundled).",
)
@click.option(
    "--target-class", default="MappingSpecification",
    help="Class to validate against (default: MappingSpecification).",
)
def validate(input_file: str, mapping_type: str | None, schema_path: str | None, target_class: str):
    """Validate a MappingSpecification YAML instance against the schema."""
    data = load_mapping(input_file, mapping_type)
    errors = validate_instance(data, schema_path=schema_path, target_class=target_class)
    if errors:
        click.echo(f"INVALID: {input_file}", err=True)
        for e in errors:
            click.echo(e, err=True)
        sys.exit(1)
    click.echo(f"OK: {input_file} is valid.")


if __name__ == "__main__":
    cli()
