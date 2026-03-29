"""CLI for fair-mappings: parse, validate, and score mapping specifications."""

from __future__ import annotations

import sys
from pathlib import Path

import click
import yaml

from fair_mappings_schema.parsing import load_mapping
from fair_mappings_schema.schema import get_mapping_type_choices, get_schema_view
from fair_mappings_schema.scoring import score_instance
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
# Report formatting
# ---------------------------------------------------------------------------


def _print_score_report(results: dict, input_path: str) -> None:
    click.echo(f"\n{'=' * 70}")
    click.echo(f"  FAIR Score Report: {input_path}")
    click.echo(f"{'=' * 70}\n")

    click.echo("ATOMIC SLOTS:")
    click.echo(f"  {'Slot':<25} {'Weight':>6} {'Present':>8} {'Earned':>7}")
    click.echo(f"  {'-' * 25} {'-' * 6} {'-' * 8} {'-' * 7}")
    for s in results["slots"]:
        if s["type"] != "atomic":
            continue
        mark = "YES" if s["present"] else "---"
        click.echo(
            f"  {s['slot']:<25} {s['weight']:>6.0f} {mark:>8} {s['earned']:>7.1f}",
        )

    click.echo("\nCOMPLEX SLOTS:")
    for s in results["slots"]:
        if s["type"] != "complex":
            continue
        click.echo(
            f"\n  {s['slot']} "
            f"(weight={s['weight']:.0f}, completeness={s['completeness']:.2f}, "
            f"earned={s['earned']:.2f})",
        )
        click.echo(f"    Formula: {s['formula']}")
        click.echo(f"    {'Sub-slot':<23} {'Weight':>6} {'Present':>8}")
        click.echo(f"    {'-' * 23} {'-' * 6} {'-' * 8}")
        for ss in s["sub_slots"]:
            mark = "YES" if ss["present"] else "---"
            click.echo(f"    {ss['slot']:<23} {ss['weight']:>6.0f} {mark:>8}")

    click.echo(f"\n{'=' * 70}")
    click.echo(
        f"  EARNED:     {results['total_earned']:.2f} / "
        f"{results['total_possible']:.0f}",
    )
    click.echo(
        f"  FAIR SCORE: {results['fair_score']:.4f}  "
        f"({results['fair_score'] * 100:.1f}%)",
    )
    click.echo(f"{'=' * 70}\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

@click.group()
@click.version_option(package_name="fair-mappings")
def cli():
    """FAIR Mappings Schema tools: parse, validate, and score mapping specifications."""


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


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "-I", "--mapping-type", type=MAPPING_TYPE, default=None,
    help="Input mapping type. If set, transforms before scoring.",
)
@click.option(
    "--schema", "schema_path", default=None, type=click.Path(exists=True),
    help="Path to FAIR Mappings schema YAML (default: bundled).",
)
def score(input_file: str, mapping_type: str | None, schema_path: str | None):
    """Score the FAIRness of a MappingSpecification instance (0-1)."""
    data = load_mapping(input_file, mapping_type)
    sv = get_schema_view(schema_path)
    results = score_instance(data, sv=sv)
    _print_score_report(results, input_file)


if __name__ == "__main__":
    cli()
