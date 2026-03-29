"""Parse and transform mapping specifications into FAIR Mappings Schema format."""

from __future__ import annotations

from collections.abc import Iterable
from io import StringIO
from pathlib import Path

import yaml
from linkml_runtime.utils.schemaview import SchemaView

from fair_mappings_schema.schema import (
    get_linkml_map_schema_path,
    get_sssom_schema_path,
    get_transformation_path,
)

# ---------------------------------------------------------------------------
# Transform configuration per mapping type
# ---------------------------------------------------------------------------

TRANSFORM_CONFIG: dict[str, dict] = {
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
# Public API
# ---------------------------------------------------------------------------

def parse_sssom_tsv(source: str | Path | Iterable[str]) -> dict:
    """Parse a .sssom.tsv source and return the mapping set metadata dict.

    Uses sssom-py to parse the ``#``-commented header and first data row.

    Args:
        source: A file path, or an iterable of lines (e.g. from
            ``response.iter_lines(decode_unicode=True)``).

    Returns:
        Metadata dict suitable for passing to :func:`transform_to_fair`.

    Raises:
        ValueError: If the source contains no ``#``-commented header.
    """
    from sssom.parsers import parse_sssom_table

    header_lines: list[str] = []
    tsv_lines: list[str] = []

    if isinstance(source, (str, Path)):
        f = open(source)
    else:
        f = iter(source)

    try:
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
    finally:
        if isinstance(source, (str, Path)):
            f.close()

    if not header_lines:
        raise ValueError(f"No #-commented header found in {source}")

    content = "\n".join(header_lines + tsv_lines) + "\n"
    msdf = parse_sssom_table(StringIO(content))
    return msdf.metadata


def transform_to_fair(data: dict, mapping_type: str) -> dict:
    """Transform a source-format dict into a FAIR MappingSpecification dict.

    Uses linkml-map with the bundled transformation specification for the
    given *mapping_type*.

    Args:
        data: Source metadata dict (e.g. SSSOM metadata or LinkML-Map spec).
        mapping_type: One of the keys in :data:`TRANSFORM_CONFIG`
            (currently ``"sssom"`` or ``"linkml_map"``).

    Returns:
        A dict conforming to the FAIR Mappings MappingSpecification class.

    Raises:
        KeyError: If *mapping_type* has no registered transform.
        ValueError: If the transformation produces no output.
    """
    from linkml_map.transformer.object_transformer import ObjectTransformer

    config = TRANSFORM_CONFIG[mapping_type]
    source_schema = config["source_schema"]()
    transform_path = get_transformation_path(config["transform"])
    source_class = config["source_class"]

    tr = ObjectTransformer(unrestricted_eval=True)
    tr.source_schemaview = SchemaView(source_schema)
    tr.load_transformer_specification(transform_path)

    work = dict(data)
    for key in config["strip_keys"]:
        work.pop(key, None)

    tr.index(work, source_class)
    result = tr.map_object(work, source_class)
    if not result:
        raise ValueError(f"Transformation from {mapping_type} produced no output")
    return {k: v for k, v in result.items() if v is not None}


def load_mapping(
    input_file: str | Path,
    mapping_type: str | None = None,
) -> dict:
    """Load a mapping specification, optionally transforming it to FAIR format.

    This is the main entry point for library users.  It handles:

    * SSSOM ``.tsv`` files (header parsing via sssom-py).
    * YAML/JSON files for any supported mapping type.
    * Plain FAIR MappingSpecification YAML (when *mapping_type* is ``None``).

    Args:
        input_file: Path to the input file.
        mapping_type: If given, transform from this type to FAIR format.
            Must be a key in :data:`TRANSFORM_CONFIG` (e.g. ``"sssom"``,
            ``"linkml_map"``), or ``None`` to load as-is.

    Returns:
        A dict conforming to the FAIR Mappings MappingSpecification class.
    """
    input_file = str(input_file)

    if mapping_type == "sssom" and input_file.endswith(".tsv"):
        data = parse_sssom_tsv(input_file)
    else:
        with open(input_file) as f:
            data = yaml.safe_load(f) or {}

    if mapping_type and mapping_type in TRANSFORM_CONFIG:
        data = transform_to_fair(data, mapping_type)

    return data
