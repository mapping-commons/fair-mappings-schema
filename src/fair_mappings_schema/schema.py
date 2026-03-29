"""Resource paths for bundled and dependency schemas."""

from importlib import resources

from linkml_runtime.utils.schemaview import SchemaView


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
    return str(resources.files("fair_mappings_schema") / "transformations" / name)


def get_schema_view(schema_path: str | None = None) -> SchemaView:
    """Return a SchemaView for the given or default FAIR Mappings schema."""
    return SchemaView(schema_path or get_schema_path())


def get_mapping_type_choices() -> list[str]:
    """Get valid mapping type values from the MappingSpecificationTypeEnum."""
    sv = get_schema_view()
    enum_def = sv.get_enum("MappingSpecificationTypeEnum")
    return list(enum_def.permissible_values.keys())
