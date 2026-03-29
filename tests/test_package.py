"""Tests for top-level package API — imports and basic integration."""

import fair_mappings_schema


class TestPublicAPI:
    """All public names should be importable from the top-level package."""

    def test_get_schema_path(self):
        assert callable(fair_mappings_schema.get_schema_path)

    def test_get_schema_view(self):
        assert callable(fair_mappings_schema.get_schema_view)

    def test_load_mapping(self):
        assert callable(fair_mappings_schema.load_mapping)

    def test_parse_sssom_tsv(self):
        assert callable(fair_mappings_schema.parse_sssom_tsv)

    def test_score_instance(self):
        assert callable(fair_mappings_schema.score_instance)

    def test_transform_to_fair(self):
        assert callable(fair_mappings_schema.transform_to_fair)

    def test_validate_instance(self):
        # Lazy-loaded via __getattr__
        assert callable(fair_mappings_schema.validate_instance)

    def test_version(self):
        assert isinstance(fair_mappings_schema.__version__, str)


class TestIntegration:
    """End-to-end: transform → validate → score via library API."""

    def test_linkml_map_pipeline(self):
        data = fair_mappings_schema.transform_to_fair(
            {"id": "http://example.org/x", "title": "Test", "description": "D",
             "source_schema": "s", "target_schema": "t"},
            "linkml_map",
        )
        errors = fair_mappings_schema.validate_instance(data)
        assert errors == []

        results = fair_mappings_schema.score_instance(data)
        assert 0.0 < results["fair_score"] <= 1.0
        assert results["total_possible"] > 0
