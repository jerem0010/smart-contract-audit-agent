import unittest

from src.models import Finding, Location
from src.triage import apply_triage, classify_finding


class TriageTestCase(unittest.TestCase):
    def test_classify_informational_finding(self):
        triage = classify_finding(build_finding("S-001", "solc-version", "Informational"))

        self.assertEqual(triage.verdict, "Informational")

    def test_classify_high_risk_detector_as_likely(self):
        triage = classify_finding(build_finding("S-001", "reentrancy-eth", "High"))

        self.assertEqual(triage.verdict, "Likely")

    def test_apply_triage_marks_duplicate_findings(self):
        findings = [
            build_finding("S-001", "reentrancy-no-eth", "Medium"),
            build_finding("S-002", "reentrancy-no-eth", "Medium"),
        ]

        triaged_findings = apply_triage(findings)

        self.assertFalse(triaged_findings[0].triage.is_duplicate)
        self.assertTrue(triaged_findings[1].triage.is_duplicate)
        self.assertEqual(triaged_findings[1].triage.duplicate_of, "S-001")


def build_finding(finding_id: str, check: str, severity: str) -> Finding:
    return Finding(
        id=finding_id,
        tool="slither",
        check=check,
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
