import unittest

from src.parser import (
    extract_findings,
    get_detector_results,
    sort_findings_by_impact,
)
from src.report import format_location


class MainTestCase(unittest.TestCase):
    def test_get_detector_results_returns_empty_list_for_missing_results(self):
        self.assertEqual(get_detector_results({}), [])

    def test_extract_findings_normalizes_non_function_parent_location(self):
        slither_data = {
            "results": {
                "detectors": [
                    {
                        "check": "missing-zero-check",
                        "impact": "Low",
                        "confidence": "Medium",
                        "description": "ShadowVault.setKeeper(address).newKeeper lacks a zero-check on:",
                        "elements": [
                            {
                                "type": "variable",
                                "name": "newKeeper",
                                "source_mapping": {
                                    "filename_relative": "examples/contract.sol",
                                    "lines": [90],
                                },
                                "type_specific_fields": {
                                    "parent": {
                                        "type": "function",
                                        "name": "setKeeper",
                                        "type_specific_fields": {
                                            "signature": "setKeeper(address)",
                                            "parent": {
                                                "type": "contract",
                                                "name": "ShadowVault",
                                            },
                                        },
                                    },
                                },
                            },
                        ],
                    }
                ]
            }
        }

        findings = extract_findings(slither_data)

        self.assertEqual(findings[0]["contract"], "ShadowVault")
        self.assertEqual(findings[0]["function"], "setKeeper(address)")
        self.assertEqual(findings[0]["location"]["file"], "examples/contract.sol")
        self.assertEqual(findings[0]["location"]["start_line"], 90)

    def test_format_location_supports_nested_location_schema(self):
        finding = {
            "location": {
                "file": "examples/contract2.sol",
                "start_line": 11,
                "end_line": 19,
            }
        }

        self.assertEqual(format_location(finding), "examples/contract2.sol#11-19")

    def test_sort_findings_by_impact_orders_security_findings_first(self):
        findings = [
            {"severity": "Informational"},
            {"severity": "High"},
            {"severity": "Low"},
            {"severity": "Medium"},
            {"severity": "Optimization"},
        ]

        sorted_findings = sort_findings_by_impact(findings)

        self.assertEqual(
            [finding["severity"] for finding in sorted_findings],
            ["High", "Medium", "Low", "Informational", "Optimization"],
        )


if __name__ == "__main__":
    unittest.main()
