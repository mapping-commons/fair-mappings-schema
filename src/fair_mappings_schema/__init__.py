try:
    from fair_mappings_schema._version import __version__, __version_tuple__
except ImportError:  # pragma: no cover
    __version__ = "0.0.0"
    __version_tuple__ = (0, 0, 0)

from fair_mappings_schema.cli import (
    get_schema_path,
    parse_sssom_tsv,
    score_instance,
    transform_to_fair,
)

__all__ = [
    "get_schema_path",
    "parse_sssom_tsv",
    "score_instance",
    "transform_to_fair",
]
