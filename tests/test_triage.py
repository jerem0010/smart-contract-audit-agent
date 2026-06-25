import unittest

from src.triage import apply_triage, classify_finding


class TriageTestCase(unittest.TestCase):
    def test_classify_informational_finding(self):
        triage = classify_finding({
            "check": "solc-version",
            "severity": "Informational",
        })

        self.assertEqual(triage["verdict"], "Informational")

    def test_classify_high_risk_detector_as_likely(self):
        triage = classify_finding({
            "check": "reentrancy-eth",
            "severity": "High",
        })

        self.assertEqual(triage["verdict"], "Likely")

    def test_apply_triage_marks_duplicate_findings(self):
        findings = [
            {
                "id": "S-001",
                "check": "reentrancy-no-eth",
                "severity": "Medium",
                "contract": "Vault",
                "function": "withdraw(uint256)",
            },
            {
                "id": "S-002",
                "check": "reentrancy-no-eth",
                "severity": "Medium",
                "contract": "Vault",
                "function": "withdraw(uint256)",
            },
        ]

        triaged_findings = apply_triage(findings)

        self.assertFalse(triaged_findings[0]["triage"]["is_duplicate"])
        self.assertTrue(triaged_findings[1]["triage"]["is_duplicate"])
        self.assertEqual(triaged_findings[1]["triage"]["duplicate_of"], "S-001")


if __name__ == "__main__":
    unittest.main()
