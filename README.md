# Smart Contract Audit Agent

Small Python tool to parse Slither results and generate simple audit reports.

This is an early learning project.

## What it does

- Runs Slither on a Solidity file
- Parses Slither JSON output
- Extracts findings
- Sorts findings by impact
- Generates:
  - `report.md`
  - `findings.json`
  - `slither-output.json`

## Usage

```bash
python3 analyze2.py contract.sol
