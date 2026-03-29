"""Tests for fair_mappings_schema.schema — resource paths and SchemaView."""

from pathlib import Path

from linkml_runtime.utils.schemaview import SchemaView

from fair_mappings_schema.schema import (
    get_linkml_map_schema_path,
    get_mapping_type_choices,
    get_schema_path,
    get_schema_view,
    get_sssom_schema_path,
    get_transformation_path,
)


class TestResourcePaths:
    def test_schema_path_exists(self):
        assert Path(get_schema_path()).is_file()

    def test_sssom_schema_path_exists(self):
        assert Path(get_sssom_schema_path()).is_file()

    def test_linkml_map_schema_path_exists(self):
        assert Path(get_linkml_map_schema_path()).is_file()

    def test_transformation_path_sssom(self):
        p = get_transformation_path("sssom-to-fair.transformation.yaml")
        assert Path(p).is_file()

    def test_transformation_path_linkmlmap(self):
        p = get_transformation_path("linkmlmap-to-fair.transformation.yaml")
        assert Path(p).is_file()


class TestSchemaView:
    def test_get_schema_view_default(self):
        sv = get_schema_view()
        assert isinstance(sv, SchemaView)
        assert sv.get_class("MappingSpecification") is not None

    def test_get_schema_view_explicit(self):
        sv = get_schema_view(get_schema_path())
        assert sv.get_class("Agent") is not None

    def test_mapping_specification_has_fair_weights(self):
        sv = get_schema_view()
        slots = sv.class_induced_slots("MappingSpecification")
        slot_names = {s.name for s in slots}
        assert "id" in slot_names
        assert "license" in slot_names

        # All slots should have fair_weight annotation
        for slot in sv.class_induced_slots("MappingSpecification"):
            fw = getattr(slot.annotations, "fair_weight", None)
            assert fw is not None, f"Slot {slot.name} missing fair_weight"

    def test_complex_slots_have_aggregation_formula(self):
        sv = get_schema_view()
        complex_slots = ["author", "creator", "reviewer", "subject_source", "object_source"]
        for slot in sv.class_induced_slots("MappingSpecification"):
            if slot.name in complex_slots:
                formula = getattr(slot.annotations, "fair_weight_aggregation_function", None)
                assert formula is not None, (
                    f"Complex slot {slot.name} missing fair_weight_aggregation_function"
                )


class TestMappingTypeChoices:
    def test_returns_list(self):
        choices = get_mapping_type_choices()
        assert isinstance(choices, list)
        assert len(choices) > 0

    def test_contains_known_types(self):
        choices = get_mapping_type_choices()
        assert "sssom" in choices
        assert "linkml_map" in choices
        assert "r2rml" in choices
