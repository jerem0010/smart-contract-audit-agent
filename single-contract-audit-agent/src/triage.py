try:
    from src.models import Finding, Triage
except ModuleNotFoundError:
    from models import Finding, Triage


TRIAGE_VERDICTS = {
    "CONFIRMED": "Confirmed",
    "LIKELY": "Likely",
    "FALSE_POSITIVE": "False Positive",
    "INFORMATIONAL": "Informational",
    "NEEDS_REVIEW": "Needs Review",
}


def apply_triage(findings: list[Finding]) -> list[Finding]:
    seen_groups = {}

    for finding in findings:
        triage = classify_finding(finding)
        duplicate_key = build_duplicate_key(finding)

        if duplicate_key in seen_groups:
            triage.is_duplicate = True
            triage.duplicate_of = seen_groups[duplicate_key]
        else:
            triage.is_duplicate = False
            triage.duplicate_of = None
            seen_groups[duplicate_key] = finding.id

        finding.triage = triage

    return findings


def classify_finding(finding: Finding) -> Triage:
    check = finding.check
    severity = finding.severity

    if severity in {"Informational", "Optimization"}:
        return build_triage(
            TRIAGE_VERDICTS["INFORMATIONAL"],
            "This finding is informational or optimization-oriented and should not block security review.",
        )

    if check in {"reentrancy-eth", "unchecked-transfer"}:
        return build_triage(
            TRIAGE_VERDICTS["LIKELY"],
            "This detector commonly maps to exploitable behavior and should be reviewed as a priority.",
        )

    if check == "reentrancy-no-eth":
        return build_triage(
            TRIAGE_VERDICTS["NEEDS_REVIEW"],
            "Token reentrancy depends on the asset behavior and surrounding accounting logic.",
        )

    if check == "missing-zero-check":
        return build_triage(
            TRIAGE_VERDICTS["LIKELY"],
            "Missing zero address validation is usually a valid hardening issue.",
        )

    if check in {"events-maths", "reentrancy-benign", "reentrancy-events"}:
        return build_triage(
            TRIAGE_VERDICTS["NEEDS_REVIEW"],
            "This is usually lower risk but should be checked in context before closing.",
        )

    if severity in {"Critical", "High", "Medium"}:
        return build_triage(
            TRIAGE_VERDICTS["NEEDS_REVIEW"],
            "The severity is high enough to require manual confirmation.",
        )

    return build_triage(
        TRIAGE_VERDICTS["NEEDS_REVIEW"],
        "No specific triage rule matched this detector.",
    )


def build_triage(verdict: str, reason: str) -> Triage:
    return Triage(verdict=verdict, reason=reason)


def build_duplicate_key(finding: Finding) -> tuple:
    return (
        finding.check,
        finding.contract,
        finding.function,
    )
