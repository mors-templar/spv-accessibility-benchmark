"""Check evidence and result rules using synthetic review records."""

import copy
import json
import unittest
from pathlib import Path

try:
    import jsonschema
except ImportError:
    jsonschema = None


@unittest.skipIf(jsonschema is None, "jsonschema is needed for schema validation")
class ReviewRecordSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).with_name("review-record.schema.json")
        cls.schema = json.loads(path.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(cls.schema)
        cls.validator = jsonschema.Draft202012Validator(cls.schema)
        cls.record = {
            "schema_version": "0.1.0", "review_id": "review-01", "artifact_id": "case-01",
            "artifact_sha256": "a" * 64, "artifact_hash_scope": "manifest",
            "reviewer": {"reviewer_id": "reviewer-01", "relevant_experience": "recorded separately"},
            "environment": {"operating_system": "test", "browser": "test", "viewport": {"width": 1280, "height": 720},
                            "zoom_percent": 100, "input_methods": ["keyboard"], "assistive_technology": None},
            "masking": {"condition_hidden": True, "suspected_unmasking": None},
            "checks": [{"check_id": "KBD-01", "category": "wcag", "criterion": "2.1.1",
                        "state": "page", "procedure": "Operate the requested control with a keyboard.",
                        "result": "PASS", "reason": "The control operated.",
                        "evidence": [{"kind": "manual_observation", "description": "Observed activation.", "reference": None}]}],
            "limitations": ["Screen-reader behavior was not tested."],
        }

    def test_pass_with_evidence_is_valid(self):
        self.validator.validate(self.record)

    def test_pass_without_evidence_is_invalid(self):
        record = copy.deepcopy(self.record)
        record["checks"][0]["evidence"] = []
        self.assertTrue(list(self.validator.iter_errors(record)))

    def test_unassessed_check_can_have_no_evidence(self):
        record = copy.deepcopy(self.record)
        record["checks"][0]["result"] = "UNASSESSABLE"
        record["checks"][0]["evidence"] = []
        self.validator.validate(record)

    def test_wcag_check_requires_a_criterion_number(self):
        record = copy.deepcopy(self.record)
        record["checks"][0]["criterion"] = None
        self.assertTrue(list(self.validator.iter_errors(record)))


if __name__ == "__main__":
    unittest.main()
