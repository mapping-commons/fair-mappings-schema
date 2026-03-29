"""Schema validation for MappingSpecification instances."""

from __future__ import annotations

from linkml.validators.jsonschemavalidator import JsonSchemaDataValidator

from fair_mappings_schema.schema import get_schema_path


def validate_instance(
    data: dict,
    schema_path: str | None = None,
    target_class: str = "MappingSpecification",
) -> list[str]:
    """Validate a MappingSpecification instance dict against the schema.

    Args:
        data: A MappingSpecification instance dict.
        schema_path: Path to the schema YAML (default: bundled schema).
        target_class: Class to validate against.

    Returns:
        An empty list if valid, or a list of error messages.
    """
    schema = schema_path or get_schema_path()
    validator = JsonSchemaDataValidator(schema)
    try:
        validator.validate_dict(data, target_class=target_class)
        return []
    except Exception as e:
        return str(e).splitlines()
