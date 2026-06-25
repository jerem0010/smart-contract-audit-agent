import unittest

from src.parser import (
    extract_findings,
    get_detector_results,
    sort_findings_by_impact,
)
from src.models import Finding, Location
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

        self.assertIsInstance(findings[0], Finding)
        self.assertEqual(findings[0].contract, "ShadowVault")
        self.assertEqual(findings[0].function, "setKeeper(address)")
        self.assertEqual(findings[0].location.file, "examples/contract.sol")
        self.assertEqual(findings[0].location.start_line, 90)

    def test_format_location_supports_nested_location_schema(self):
        finding = Finding(
            id="S-001",
            tool="slither",
            check="reentrancy-eth",
            title="Reentrancy",
            severity="High",
            confidence="Medium",
            contract="Vault",
            function="withdraw(uint256)",
            location=Location("examples/contract2.sol", 11, 19),
            description="",
            recommendation="",
        )

        self.assertEqual(format_location(finding), "examples/contract2.sol#11-19")

    def test_sort_findings_by_impact_orders_security_findings_first(self):
        findings = [
            build_finding("S-001", "Informational"),
            build_finding("S-002", "High"),
            build_finding("S-003", "Low"),
            build_finding("S-004", "Medium"),
            build_finding("S-005", "Optimization"),
        ]

        sorted_findings = sort_findings_by_impact(findings)

        self.assertEqual(
            [finding.severity for finding in sorted_findings],
            ["High", "Medium", "Low", "Informational", "Optimization"],
        )

    def test_finding_to_dict_preserves_json_shape(self):
        finding = build_finding("S-001", "High")
        output = finding.to_dict()

        self.assertEqual(output["severity"], "High")
        self.assertEqual(output["impact"], "High")
        self.assertEqual(output["filename"], "contract.sol")
        self.assertEqual(output["location"]["file"], "contract.sol")


def build_finding(finding_id: str, severity: str) -> Finding:
    return Finding(
        id=finding_id,
        tool="slither",
        check="test-check",
        title="Test finding",
        severity=severity,
        confidence="Medium",
        contract="Vault",
        function="withdraw(uint256)",
        location=Location("contract.sol", 1, 2),
        description="",
        recommendation="",
    )


if __name__ == "__main__":
    unittest.main()
