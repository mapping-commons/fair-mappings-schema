"""CLI for fair-mappings: validate and score MappingSpecification instances."""

import re
import sys
from importlib import resources
from pathlib import Path

import click
import yaml
from linkml.validators.jsonschemavalidator import JsonSchemaDataValidator
from linkml_runtime.utils.schemaview import SchemaView


# ---------------------------------------------------------------------------
# Resource paths — all schemas come from their PyPI packages
# ---------------------------------------------------------------------------

def get_schema_path() -> str:
    """Return the path to the bundled FAIR Mappings schema YAML."""
    return str(resources.files("fair_mappings_schema") / "schema" / "fair_mappings_schema.yaml")


def get_sssom_schema_path() -> str:
    """Return the path to the SSSOM schema YAML (from sssom-schema package)."""
    return str(resources.files("sssom_schema") / "schema" / "sssom_schema.yaml")


def get_linkml_map_schema_path() -> str:
    """Return the path to the LinkML-Map schema YAML (from linkml-map package)."""
    return str(resources.files("linkml_map") / "datamodel" / "transformer_model.yaml")


def get_transformation_path(name: str) -> str:
    """Return the path to a bundled transformation spec."""
    return str(
        resources.files("fair_mappings_schema") / "transformations" / name
    )


def get_mapping_type_choices() -> list[str]:
    """Get valid mapping type values from the schema enum via SchemaView."""
    sv = SchemaView(get_schema_path())
    enum_def = sv.get_enum("MappingSpecificationTypeEnum")
    return list(enum_def.permissible_values.keys())


# Map from mapping type to (source_schema_getter, transform_file, source_class, strip_keys)
TRANSFORM_CONFIG = {
    "sssom": {
        "source_schema": get_sssom_schema_path,
        "transform": "sssom-to-fair.transformation.yaml",
        "source_class": "mapping set",
        "strip_keys": [],
    },
    "linkml_map": {
        "source_schema": get_linkml_map_schema_path,
        "transform": "linkmlmap-to-fair.transformation.yaml",
        "source_class": "TransformationSpecification",
        "strip_keys": [
            "class_derivations", "enum_derivations", "slot_derivations",
            "copy_directives", "schema_patches", "prefixes",
        ],
    },
}


# ---------------------------------------------------------------------------
# Transformation
# ---------------------------------------------------------------------------

def parse_sssom_tsv(filepath: str) -> dict:
    """Parse a .sssom.tsv file and return the mapping set metadata dict.

    Uses sssom-py to parse the #-commented header and first data row.
    """
    from io import StringIO
    from sssom.parsers import parse_sssom_table

    header_lines = []
    tsv_lines = []
    with open(filepath) as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("#"):
                header_lines.append(line)
            elif line.strip() == "":
                continue
            else:
                tsv_lines.append(line)
                if len(tsv_lines) == 2:  # column header + one data row
                    break

    if not header_lines:
        raise click.ClickException(f"No #-commented header found in {filepath}")

    content = "\n".join(header_lines + tsv_lines) + "\n"
    msdf = parse_sssom_table(StringIO(content))
    return msdf.metadata


def transform_to_fair(data: dict, mapping_type: str) -> dict:
    """Transform input data to a FAIR MappingSpecification dict using linkml-map."""
    from linkml_map.transformer.object_transformer import ObjectTransformer

    config = TRANSFORM_CONFIG[mapping_type]
    source_schema = config["source_schema"]()
    transform_path = get_transformation_path(config["transform"])
    source_class = config["source_class"]

    tr = ObjectTransformer(unrestricted_eval=True)
    tr.source_schemaview = SchemaView(source_schema)
    tr.load_transformer_specification(transform_path)

    # Strip keys that cause issues with linkml-map inference
    work = dict(data)
    for key in config["strip_keys"]:
        work.pop(key, None)

    tr.index(work, source_class)
    result = tr.map_object(work, source_class)
    if not result:
        raise click.ClickException(f"Transformation from {mapping_type} produced no output")
    return {k: v for k, v in result.items() if v is not None}


# ---------------------------------------------------------------------------
# Scoring helpers
# ---------------------------------------------------------------------------

def _get_annotation_value(slot, tag: str):
    ann = getattr(slot.annotations, tag, None)
    return ann.value if ann else None


def _is_present(value) -> bool:
    if value is None:
        return False
    if isinstance(value, str) and value.strip() == "":
        return False
    return True


def _evaluate_completeness(
    formula: str, sub_data: dict, sv: SchemaView, target_class: str,
) -> tuple[float, list[dict]]:
    """Evaluate a fair_weight_aggregation_function formula.

    Slot names are replaced with 1 (present) or 0 (absent).
    Returns (completeness_ratio, sub_slot_details).
    """
    sub_slot_details = []
    sub_weights = {}
    for sub_slot_def in sv.class_induced_slots(target_class):
        sub_fw = _get_annotation_value(sub_slot_def, "fair_weight")
        if sub_fw is not None:
            sub_weights[sub_slot_def.name] = float(sub_fw)

    expr = formula
    for slot_name, weight in sub_weights.items():
        present = _is_present(sub_data.get(slot_name))
        indicator = 1 if present else 0
        expr = re.sub(rf"\b{re.escape(slot_name)}\b", str(indicator), expr)
        sub_slot_details.append({
            "slot": slot_name,
            "weight": weight,
            "present": present,
        })

    try:
        completeness = eval(expr)  # noqa: S307
        completeness = max(0.0, min(1.0, completeness))
    except Exception:
        completeness = 0.0

    return round(completeness, 4), sub_slot_details


def score_instance(sv: SchemaView, data: dict) -> dict:
    """Score a MappingSpecification instance dict against schema weights."""
    results = {"slots": [], "total_earned": 0.0, "total_possible": 0.0}

    for slot_def in sv.class_induced_slots("MappingSpecification"):
        fair_weight = _get_annotation_value(slot_def, "fair_weight")
        if fair_weight is None:
            continue
        weight = float(fair_weight)
        formula = _get_annotation_value(slot_def, "fair_weight_aggregation_function")

        if formula:
            target_class = slot_def.range
            sub_data = data.get(slot_def.name)
            if not isinstance(sub_data, dict):
                sub_data = {}
            completeness, sub_details = _evaluate_completeness(
                formula, sub_data, sv, target_class,
            )
            earned = weight * completeness
            results["slots"].append({
                "slot": slot_def.name,
                "type": "complex",
                "weight": weight,
                "target_class": target_class,
                "formula": formula,
                "completeness": completeness,
                "earned": round(earned, 2),
                "sub_slots": sub_details,
            })
        else:
            present = _is_present(data.get(slot_def.name))
            earned = weight if present else 0.0
            results["slots"].append({
                "slot": slot_def.name,
                "type": "atomic",
                "weight": weight,
                "present": present,
                "earned": earned,
            })

        results["total_earned"] += earned
        results["total_possible"] += weight

    if results["total_possible"] > 0:
        results["fair_score"] = round(
            results["total_earned"] / results["total_possible"], 4,
        )
    else:
        results["fair_score"] = 0.0

    return results


def print_score_report(results: dict, input_path: str) -> None:
    """Print a formatted FAIR score report."""
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

    click.echo(f"\nCOMPLEX SLOTS:")
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
# Shared helpers for loading + optional transform
# ---------------------------------------------------------------------------

def _load_and_maybe_transform(input_file: str, mapping_type: str | None) -> dict:
    """Load input data, optionally transforming via linkml-map first.

    For SSSOM: handles both .sssom.tsv (parses header via sssom-py) and YAML.
    For other types with transforms: loads YAML and transforms via linkml-map.
    Without -I: loads YAML as-is (assumes FAIR MappingSpecification).
    """
    if mapping_type == "sssom" and input_file.endswith(".tsv"):
        click.echo("Parsing SSSOM TSV header...")
        data = parse_sssom_tsv(input_file)
    else:
        with open(input_file) as f:
            data = yaml.safe_load(f) or {}

    if mapping_type and mapping_type in TRANSFORM_CONFIG:
        click.echo(f"Transforming from {mapping_type} to FAIR MappingSpecification...")
        data = transform_to_fair(data, mapping_type)
    return data


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

# Build mapping-type choices dynamically from schema enum
_MAPPING_TYPE_CHOICES = None


def _get_type_choices():
    global _MAPPING_TYPE_CHOICES
    if _MAPPING_TYPE_CHOICES is None:
        _MAPPING_TYPE_CHOICES = get_mapping_type_choices()
    return _MAPPING_TYPE_CHOICES


class MappingTypeChoice(click.ParamType):
    """Click type that validates against MappingSpecificationTypeEnum."""
    name = "mapping_type"

    def get_metavar(self, param):
        return "[" + "|".join(_get_type_choices()) + "]"

    def convert(self, value, param, ctx):
        choices = _get_type_choices()
        if value not in choices:
            self.fail(
                f"Invalid mapping type '{value}'. Choose from: {', '.join(choices)}",
                param, ctx,
            )
        return value


MAPPING_TYPE = MappingTypeChoice()


@click.group()
@click.version_option(package_name="fair-mappings")
def cli():
    """FAIR Mappings Schema tools: validate and score mapping specifications."""


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "-I", "--mapping-type", type=MAPPING_TYPE, required=True,
    help="Input mapping type (e.g. sssom, linkml_map).",
)
@click.option(
    "-o", "--output", "output_file", default=None,
    type=click.Path(),
    help="Output file path (default: <input_stem>.fms.yml).",
)
def parse(input_file: str, mapping_type: str, output_file: str | None):
    """Parse a mapping specification into FAIR Mappings Schema format.

    Transforms the input file from the given mapping type into a
    FAIR MappingSpecification YAML file (.fms.yml).
    """
    data = _load_and_maybe_transform(input_file, mapping_type)

    if output_file is None:
        stem = Path(input_file).stem
        # Strip double extensions like .sssom from .sssom.tsv
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
    help="Input mapping type (e.g. sssom, linkml_map). "
         "If set, transforms input to FAIR MappingSpecification first.",
)
@click.option(
    "--schema", "schema_path", default=None,
    type=click.Path(exists=True),
    help="Path to FAIR Mappings schema YAML (default: bundled schema).",
)
@click.option(
    "--target-class", default="MappingSpecification",
    help="Class to validate against (default: MappingSpecification).",
)
def validate(input_file: str, mapping_type: str | None, schema_path: str | None, target_class: str):
    """Validate a MappingSpecification YAML instance against the schema."""
    data = _load_and_maybe_transform(input_file, mapping_type)
    schema = schema_path or get_schema_path()

    validator = JsonSchemaDataValidator(schema)
    try:
        validator.validate_dict(data, target_class=target_class)
        click.echo(f"OK: {input_file} is valid.")
    except Exception as e:
        click.echo(f"INVALID: {input_file}", err=True)
        click.echo(str(e), err=True)
        sys.exit(1)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "-I", "--mapping-type", type=MAPPING_TYPE, default=None,
    help="Input mapping type (e.g. sssom, linkml_map). "
         "If set, transforms input to FAIR MappingSpecification first.",
)
@click.option(
    "--schema", "schema_path", default=None,
    type=click.Path(exists=True),
    help="Path to FAIR Mappings schema YAML (default: bundled schema).",
)
def score(input_file: str, mapping_type: str | None, schema_path: str | None):
    """Score the FAIRness of a MappingSpecification instance (0-1)."""
    data = _load_and_maybe_transform(input_file, mapping_type)
    schema = schema_path or get_schema_path()
    sv = SchemaView(schema)

    results = score_instance(sv, data)
    print_score_report(results, input_file)


if __name__ == "__main__":
    cli()
