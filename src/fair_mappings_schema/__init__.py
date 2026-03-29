try:
    from fair_mappings_schema._version import __version__, __version_tuple__
except ImportError:  # pragma: no cover
    __version__ = "0.0.0"
    __version_tuple__ = (0, 0, 0)

from fair_mappings_schema.parsing import load_mapping, parse_sssom_tsv, transform_to_fair
from fair_mappings_schema.schema import get_schema_path, get_schema_view
from fair_mappings_schema.scoring import score_instance

__all__ = [
    "get_schema_path",
    "get_schema_view",
    "load_mapping",
    "parse_sssom_tsv",
    "score_instance",
    "transform_to_fair",
    "validate_instance",
]


def __getattr__(name: str):
    if name == "validate_instance":
        from fair_mappings_schema.validation import validate_instance
        return validate_instance
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
