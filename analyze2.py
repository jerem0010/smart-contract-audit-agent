import json
import sys
import subprocess
from datetime import datetime
from pathlib import Path

def create_run_directory(target_path: Path) -> Path:
    contract_name = target_path.stem
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    run_dir = Path("reports") / contract_name / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)

    return run_dir

def run_slither(target_path: Path, output_path: Path) -> None:
    command = [
        "slither",
        str(target_path),
        "--json",
        str(output_path),
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    if not output_path.exists():
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError("Slither did not generate the JSON output file.")

def load_slither_results(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")

    return json.loads(path.read_text())

def extract_location(detector: dict) -> dict:
    elements = detector.get("elements", [])

    for element in elements:
        if element.get("type") == "function":
            source_mapping = element.get("source_mapping", {})
            type_specific_fields = element.get("type_specific_fields", {})

            parent = type_specific_fields.get("parent", {})
            contract_name = parent.get("name")

            signature = type_specific_fields.get("signature")
            function_name = signature or element.get("name")

            lines = source_mapping.get("lines", [])

            return {
                "contract": contract_name,
                "function": function_name,
                "filename": source_mapping.get("filename_relative"),
                "start_line": min(lines) if lines else None,
                "end_line": max(lines) if lines else None,
            }

    return {
        "contract": None,
        "function": None,
        "filename": None,
        "start_line": None,
        "end_line": None,
    }

def extract_findings(slither_data: dict) -> list[dict]:
    detectors = slither_data["results"]["detectors"]

    findings = []

    for i, detector in enumerate(detectors, start=1):
        location = extract_location(detector)

        finding = {
            "id": f"S-{i:03d}",
            "check": detector.get("check"),
            "impact": detector.get("impact"),
            "confidence": detector.get("confidence"),
            "contract": location["contract"],
            "function": location["function"],
            "filename": location["filename"],
            "start_line": location["start_line"],
            "end_line": location["end_line"],
            "description": detector.get("description"),
        }

        findings.append(finding)

    return findings

def sort_findings_by_impact(findings: list[dict]) -> list[dict]:
    impact_order = {
        "High": 0,
        "Medium": 1,
        "Low": 2,
        "Informational": 3,
    }

    return sorted(
        findings,
        key=lambda finding: impact_order.get(finding["impact"], 999),
    )


def print_report(findings: list[dict]) -> None:
    print("Mini Slither Report")
    print("===================")
    print()

    if not findings:
        print("No findings found.")
        return

    for finding in findings:
        print(f"{finding['id']} - {finding['check']}")
        print(f"Impact: {finding['impact']}")
        print(f"Confidence: {finding['confidence']}")
        print(f"Contract: {finding['contract'] or 'N/A'}")
        print(f"Function: {finding['function'] or 'N/A'}")
        print(f"Location: {format_location(finding)}")
        print()
        print(finding["description"])
        print("-" * 80)

def format_location(finding: dict) -> str:
    filename = finding.get("filename")
    start_line = finding.get("start_line")
    end_line = finding.get("end_line")

    if filename is None or start_line is None or end_line is None:
        return "N/A"

    return f"{filename}#{start_line}-{end_line}"


def write_markdown_report(findings: list[dict], output_path: Path) -> None:
    lines = []

    lines.append("# Mini Slither Report")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total findings: {len(findings)}")
    lines.append("")

    if not findings:
        lines.append("No findings found.")
        output_path.write_text("\n".join(lines))
        return

    lines.append("## Findings")
    lines.append("")

    for finding in findings:
        location = format_location(finding)

        lines.append(f"### {finding['id']} - {finding['check']}")
        lines.append("")
        lines.append(f"- **Impact:** {finding['impact']}")
        lines.append(f"- **Confidence:** {finding['confidence']}")
        lines.append(f"- **Contract:** `{finding['contract'] or 'N/A'}`")
        lines.append(f"- **Function:** `{finding['function'] or 'N/A'}`")
        lines.append(f"- **Location:** `{location}`")
        lines.append("")
        lines.append("#### Description")
        lines.append("")
        lines.append("```txt")
        lines.append(finding["description"] or "")
        lines.append("```")
        lines.append("")

    output_path.write_text("\n".join(lines))

def write_findings_json(findings: list[dict], output_path: Path) -> None:
    output = {
        "findings": findings
    }

    output_path.write_text(json.dumps(output, indent=2))
    


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 analyze2.py <solidity-file>")
        print("Example: python3 analyze2.py contract.sol")
        sys.exit(1)

    target_path = Path(sys.argv[1])

    if not target_path.exists():
        print(f"Error: target file not found: {target_path}")
        sys.exit(1)

    run_dir = create_run_directory(target_path)

    slither_path = run_dir / "slither-output.json"
    report_path = run_dir / "report.md"
    findings_path = run_dir / "findings.json"

    print(f"Analyzing: {target_path}")
    print(f"Output directory: {run_dir}")
    print()

    run_slither(target_path, slither_path)

    slither_data = load_slither_results(slither_path)
    findings = extract_findings(slither_data)
    findings = sort_findings_by_impact(findings)

    print_report(findings)

    write_markdown_report(findings, report_path)
    print(f"Markdown report written to {report_path}")

    write_findings_json(findings, findings_path)
    print(f"Findings JSON written to {findings_path}")


if __name__ == "__main__":
    main()