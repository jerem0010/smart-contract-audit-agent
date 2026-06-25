# Smart Contract Audit Agent

Prototype audit assistant for Solidity projects using Slither, structured finding extraction, and automated Markdown/JSON report generation.

This is an early learning project exploring how static analysis can be used as the first layer of a smart contract audit workflow.

## What it does

The tool:

- Runs Slither on a Solidity target
- Exports Slither JSON output
- Parses detector results
- Extracts findings
- Applies deterministic triage rules
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
Triage rules
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
python3 src/main.py examples/contract2.sol
```

You can pass either a single Solidity file or a Solidity project supported by Slither.

## Output

After running the tool, the project can generate:

```txt
report.md
findings.json
slither-output.json
```

## Project Structure

```txt
src/main.py      CLI entrypoint and pipeline orchestration
src/models.py    Dataclasses for findings, locations, and triage
src/slither.py   Slither execution and JSON loading
src/parser.py    Slither detector normalization into findings
src/triage.py    Deterministic triage rules
src/report.py    Console, Markdown, and JSON reporting
```

## Tests

```bash
python3 -m unittest
```

## Tech Stack

- Python
- Solidity
- Slither
- Foundry-compatible Solidity projects
- Markdown / JSON report generation


## Roadmap

Possible future improvements:

- Pydantic schemas for structured findings
- Support for full Solidity repositories
- Foundry test integration
- LLM-assisted explanations
- Evaluation on vulnerable-contract datasets
- Precision / recall / F1 scoring
