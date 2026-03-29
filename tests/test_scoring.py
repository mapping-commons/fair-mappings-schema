"""Tests for fair_mappings_schema.scoring — FAIR weight scoring."""

import pytest

from fair_mappings_schema.scoring import score_instance


class TestScoreStructure:
    """Verify the shape of score results."""

    def test_empty_instance(self):
        results = score_instance({})
        assert results["fair_score"] == 0.0
        assert results["total_earned"] == 0.0
        assert results["total_possible"] > 0
        assert len(results["slots"]) > 0

    def test_result_keys(self):
        results = score_instance({})
        assert "slots" in results
        assert "total_earned" in results
        assert "total_possible" in results
        assert "fair_score" in results

    def test_score_between_zero_and_one(self):
        results = score_instance({"id": "x", "license": "MIT"})
        assert 0.0 <= results["fair_score"] <= 1.0


class TestAtomicSlotScoring:
    """Atomic slots: present → full weight, absent → 0."""

    def test_absent_slot_earns_zero(self):
        results = score_instance({})
        id_slot = next(s for s in results["slots"] if s["slot"] == "id")
        assert id_slot["type"] == "atomic"
        assert id_slot["present"] is False
        assert id_slot["earned"] == 0.0

    def test_present_slot_earns_weight(self):
        results = score_instance({"id": "https://example.org/test"})
        id_slot = next(s for s in results["slots"] if s["slot"] == "id")
        assert id_slot["present"] is True
        assert id_slot["earned"] == id_slot["weight"]

    def test_empty_string_counts_as_absent(self):
        results = score_instance({"id": "  "})
        id_slot = next(s for s in results["slots"] if s["slot"] == "id")
        assert id_slot["present"] is False

    def test_none_counts_as_absent(self):
        results = score_instance({"id": None})
        id_slot = next(s for s in results["slots"] if s["slot"] == "id")
        assert id_slot["present"] is False

    def test_all_atomic_slots_present(self):
        data = {
            "id": "x", "name": "x", "description": "x",
            "publication_date": "2024-01-01", "license": "MIT",
            "version": "1.0", "type": "sssom", "mapping_method": "manual",
            "documentation": "http://example.org", "content_url": "http://example.org/f",
        }
        results = score_instance(data)
        atomic_slots = [s for s in results["slots"] if s["type"] == "atomic"]
        for s in atomic_slots:
            assert s["present"] is True, f"{s['slot']} should be present"
            assert s["earned"] == s["weight"]


class TestComplexSlotScoring:
    """Complex slots: weight * completeness(0-1)."""

    def test_absent_complex_slot_earns_zero(self):
        results = score_instance({})
        author_slot = next(s for s in results["slots"] if s["slot"] == "author")
        assert author_slot["type"] == "complex"
        assert author_slot["completeness"] == 0.0
        assert author_slot["earned"] == 0.0

    def test_partial_complex_slot(self):
        data = {"author": {"name": "Alice"}}
        results = score_instance(data)
        author_slot = next(s for s in results["slots"] if s["slot"] == "author")
        assert 0.0 < author_slot["completeness"] < 1.0
        assert author_slot["earned"] == pytest.approx(
            author_slot["weight"] * author_slot["completeness"], abs=0.01,
        )

    def test_full_complex_slot(self):
        data = {"author": {"id": "x", "name": "Alice", "type": "Person"}}
        results = score_instance(data)
        author_slot = next(s for s in results["slots"] if s["slot"] == "author")
        assert author_slot["completeness"] == 1.0
        assert author_slot["earned"] == author_slot["weight"]

    def test_source_partial(self):
        data = {"subject_source": {"id": "HP", "name": "Human Phenotype Ontology"}}
        results = score_instance(data)
        src = next(s for s in results["slots"] if s["slot"] == "subject_source")
        assert 0.0 < src["completeness"] < 1.0
        assert len(src["sub_slots"]) > 2  # Source has many sub-slots

    def test_complex_slot_has_sub_slot_details(self):
        data = {"author": {"name": "Alice"}}
        results = score_instance(data)
        author_slot = next(s for s in results["slots"] if s["slot"] == "author")
        assert "sub_slots" in author_slot
        names = {ss["slot"] for ss in author_slot["sub_slots"]}
        assert "id" in names
        assert "name" in names
        assert "type" in names


class TestScoreConsistency:
    """Total earned should equal sum of slot earned values."""

    def test_total_is_sum_of_slots(self):
        data = {
            "id": "x", "license": "MIT",
            "author": {"name": "Alice"},
            "subject_source": {"id": "HP", "name": "HPO", "type": "ontology"},
        }
        results = score_instance(data)
        slot_sum = sum(s["earned"] for s in results["slots"])
        assert results["total_earned"] == pytest.approx(slot_sum, abs=0.01)

    def test_perfect_score(self):
        """A fully populated instance should score 1.0."""
        data = {
            "id": "x", "name": "x", "description": "x",
            "publication_date": "2024-01-01", "license": "MIT",
            "version": "1.0", "type": "sssom", "mapping_method": "manual",
            "documentation": "http://example.org", "content_url": "http://example.org/f",
            "author": {"id": "a1", "name": "Alice", "type": "Person"},
            "creator": {"id": "c1", "name": "Bob", "type": "Person"},
            "reviewer": {"id": "r1", "name": "Carol", "type": "Person"},
            "subject_source": {
                "id": "HP", "name": "HPO", "version": "2024", "type": "ontology",
                "documentation": "http://hp.org", "content_url": "http://hp.org/hp.owl",
                "content_type": "application/rdf+xml",
                "metadata_url": "http://hp.org/meta", "metadata_type": "text/yaml",
            },
            "object_source": {
                "id": "MP", "name": "MPO", "version": "2024", "type": "ontology",
                "documentation": "http://mp.org", "content_url": "http://mp.org/mp.owl",
                "content_type": "application/rdf+xml",
                "metadata_url": "http://mp.org/meta", "metadata_type": "text/yaml",
            },
        }
        results = score_instance(data)
        assert results["fair_score"] == 1.0

    def test_custom_schema_view(self):
        """Passing an explicit SchemaView should work identically."""
        from fair_mappings_schema.schema import get_schema_view

        sv = get_schema_view()
        r1 = score_instance({"id": "x"})
        r2 = score_instance({"id": "x"}, sv=sv)
        assert r1["fair_score"] == r2["fair_score"]
