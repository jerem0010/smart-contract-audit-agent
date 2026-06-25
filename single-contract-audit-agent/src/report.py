import json
from pathlib import Path

try:
    from src.models import Finding
except ModuleNotFoundError:
    from models import Finding


def print_report(findings: list[Finding]) -> None:
    print("Mini Slither Report")
    print("===================")
    print()

    if not findings:
        print("No findings found.")
        return

    for finding in findings:
        print(f"{finding.id} - {finding.title}")
        print(f"Severity: {finding.severity}")
        print(f"Confidence: {finding.confidence}")
        print(f"Contract: {finding.contract or 'N/A'}")
        print(f"Function: {finding.function or 'N/A'}")
        print(f"Location: {format_location(finding)}")
        print(f"Triage: {format_triage_summary(finding)}")
        print()
        print(finding.description)
        print("-" * 80)


def format_location(finding: Finding) -> str:
    return finding.location.format()


def format_triage_summary(finding: Finding) -> str:
    if finding.triage is None:
        return "Needs Review"

    if finding.triage.is_duplicate:
        return f"{finding.triage.verdict} (duplicate of {finding.triage.duplicate_of})"

    return finding.triage.verdict


def count_findings_by_severity(findings: list[Finding]) -> dict[str, int]:
    counts = {
        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0,
        "Informational": 0,
        "Optimization": 0,
    }

    for finding in findings:
        severity = finding.severity or "Unknown"
        counts[severity] = counts.get(severity, 0) + 1

    return counts


def count_findings_by_triage_verdict(findings: list[Finding]) -> dict[str, int]:
    counts = {}

    for finding in findings:
        verdict = finding.triage.verdict if finding.triage else "Needs Review"
        counts[verdict] = counts.get(verdict, 0) + 1

    return counts


def count_duplicate_findings(findings: list[Finding]) -> int:
    return sum(1 for finding in findings if finding.triage and finding.triage.is_duplicate)


def write_markdown_report(findings: list[Finding], output_path: Path, target_path: Path) -> None:
    severity_counts = count_findings_by_severity(findings)
    triage_counts = count_findings_by_triage_verdict(findings)
    lines = []

    lines.append("# Smart Contract Audit Report")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(f"- Target: `{target_path}`")
    lines.append(f"- Tool: Slither")
    lines.append(f"- Total findings: {len(findings)}")
    lines.append(f"- High or above: {severity_counts.get('Critical', 0) + severity_counts.get('High', 0)}")
    lines.append(f"- Medium: {severity_counts.get('Medium', 0)}")
    lines.append(f"- Low: {severity_counts.get('Low', 0)}")
    lines.append(f"- Informational: {severity_counts.get('Informational', 0)}")
    lines.append(f"- Duplicate findings: {count_duplicate_findings(findings)}")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- `{target_path}`")
    lines.append("")

    if not findings:
        lines.append("No findings found.")
        output_path.write_text("\n".join(lines))
        return

    lines.append("## Severity Breakdown")
    lines.append("")
    lines.append("| Severity | Count |")
    lines.append("| --- | ---: |")
    for severity in ["Critical", "High", "Medium", "Low", "Informational", "Optimization"]:
        lines.append(f"| {severity} | {severity_counts.get(severity, 0)} |")

    lines.append("")
    lines.append("## Triage Breakdown")
    lines.append("")
    lines.append("| Verdict | Count |")
    lines.append("| --- | ---: |")
    for verdict in ["Likely", "Needs Review", "Informational", "Confirmed", "False Positive"]:
        lines.append(f"| {verdict} | {triage_counts.get(verdict, 0)} |")

    lines.append("")
    lines.append("## Findings Summary")
    lines.append("")
    lines.append("| ID | Severity | Triage | Confidence | Title | Location |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for finding in findings:
        lines.append(
            f"| {finding.id} | {finding.severity} | {format_triage_summary(finding)} | "
            f"{finding.confidence} | "
            f"{finding.title} | `{format_location(finding)}` |"
        )

    lines.append("")
    lines.append("## Detailed Findings")
    lines.append("")

    for finding in findings:
        location = format_location(finding)

        lines.append(f"### {finding.id} - {finding.title}")
        lines.append("")
        lines.append(f"- **Severity:** {finding.severity}")
        lines.append(f"- **Confidence:** {finding.confidence}")
        lines.append(f"- **Check:** `{finding.check}`")
        lines.append(f"- **Contract:** `{finding.contract or 'N/A'}`")
        lines.append(f"- **Function:** `{finding.function or 'N/A'}`")
        lines.append(f"- **Location:** `{location}`")
        lines.append(f"- **Status:** {finding.status}")
        lines.append(f"- **Triage:** {format_triage_summary(finding)}")
        lines.append("")
        lines.append("#### Triage Reason")
        lines.append("")
        triage_reason = finding.triage.reason if finding.triage else "No triage reason available."
        lines.append(triage_reason)
        lines.append("")
        lines.append("#### Description")
        lines.append("")
        lines.append("```txt")
        lines.append(finding.description or "")
        lines.append("```")
        lines.append("")
        lines.append("#### Recommendation")
        lines.append("")
        lines.append(finding.recommendation)
        lines.append("")

    output_path.write_text("\n".join(lines))


def write_findings_json(findings: list[Finding], output_path: Path) -> None:
    output = {
        "findings": [finding.to_dict() for finding in findings]
    }

    output_path.write_text(json.dumps(output, indent=2))
