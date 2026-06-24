# Smart Contract Audit Agent

Prototype audit assistant for Solidity projects using Slither, structured finding extraction, and automated Markdown/JSON report generation.

This is an early learning project exploring how static analysis can be used as the first layer of a smart contract audit workflow.

## What it does

The tool:

- Runs Slither on a Solidity target
- Exports Slither JSON output
- Parses detector results
- Extracts findings
- Sorts findings by impact
- Generates:
  - `report.md`
  - `findings.json`
  - `slither-output.json`

## Pipeline

```txt
Solidity contract
      ↓
Slither static analysis
      ↓
JSON output
      ↓
Finding parser
      ↓
Severity sorting
      ↓
Markdown + JSON audit report
```

## Why this project?

The goal is to experiment with security automation for smart contract audits.

This project is an early step toward a larger audit assistant combining:

- static analysis
- structured finding schemas
- reproducible reports
- LLM-assisted triage
- evaluation against vulnerable contracts

## Usage

```bash
python3 analyze2.py contract.sol
```

## Output

After running the tool, the project can generate:

```txt
report.md
findings.json
slither-output.json
```

## Tech Stack

- Python
- Solidity
- Slither
- Foundry-compatible Solidity projects
- Markdown / JSON report generation


## Roadmap

Possible future improvements:

- Better finding normalization
- Pydantic schemas for structured findings
- Support for full Solidity repositories
- Foundry test integration
- LLM-assisted explanations
- Evaluation on vulnerable-contract datasets
- Precision / recall / F1 scoring


This tool is educational and experimental.  
It should not be used as a replacement for a manual smart contract audit.
