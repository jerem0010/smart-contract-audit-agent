import sys
from datetime import datetime
from pathlib import Path

try:
    from src.parser import extract_findings, sort_findings_by_impact
    from src.report import print_report, write_findings_json, write_markdown_report
    from src.slither import load_slither_results, run_slither
    from src.triage import apply_triage
except ModuleNotFoundError:
    from parser import extract_findings, sort_findings_by_impact
    from report import print_report, write_findings_json, write_markdown_report
    from slither import load_slither_results, run_slither
    from triage import apply_triage


def create_run_directory(target_path: Path) -> Path:
    contract_name = target_path.stem
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    run_dir = Path("reports") / contract_name / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)

    return run_dir


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 src/main.py <solidity-file-or-project>")
        print("Example: python3 src/main.py examples/contract2.sol")
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
    findings = apply_triage(findings)
    findings = sort_findings_by_impact(findings)

    print_report(findings)

    write_markdown_report(findings, report_path, target_path)
    print(f"Markdown report written to {report_path}")

    write_findings_json(findings, findings_path)
    print(f"Findings JSON written to {findings_path}")


if __name__ == "__main__":
    main()
