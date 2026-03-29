"""FAIR weight scoring for MappingSpecification instances."""

from __future__ import annotations

import re

from linkml_runtime.utils.schemaview import SchemaView

from fair_mappings_schema.schema import get_schema_view


# ---------------------------------------------------------------------------
# Helpers
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
    """Evaluate a ``fair_weight_aggregation_function`` formula.

    Slot names are replaced with ``1`` (present) or ``0`` (absent).
    Returns ``(completeness_ratio, sub_slot_details)``.
    """
    sub_slot_details = []
    sub_weights: dict[str, float] = {}
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


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def score_instance(
    data: dict,
    sv: SchemaView | None = None,
    schema_path: str | None = None,
) -> dict:
    """Score a MappingSpecification instance against ``fair_weight`` annotations.

    For atomic slots the full weight is earned when the slot is present.
    For complex slots the weight is scaled by a completeness ratio (0-1)
    derived from the ``fair_weight_aggregation_function`` formula.

    Args:
        data: A MappingSpecification instance dict.
        sv: Pre-built :class:`SchemaView`.  If ``None``, one is created
            from *schema_path* (or the bundled default).
        schema_path: Path to the schema YAML; ignored when *sv* is given.

    Returns:
        A results dict with keys ``slots``, ``total_earned``,
        ``total_possible``, and ``fair_score`` (0-1).
    """
    if sv is None:
        sv = get_schema_view(schema_path)

    results: dict = {"slots": [], "total_earned": 0.0, "total_possible": 0.0}

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
