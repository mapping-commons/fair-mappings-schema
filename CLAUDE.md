# CLAUDE.md

- Pypi token is in .env if needed.

## Schema Interaction

- Always use `SchemaView` from `linkml_runtime.utils.schemaview` to interact with the schema programmatically. Do not parse the YAML manually for slot/class/enum lookups.
