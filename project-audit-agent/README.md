# Project Audit Agent

Scaffold for the next version of the smart contract audit agent.

This version is intended to analyze larger Solidity repositories instead of focusing on a single contract file.

## Planned Direction

- Run Slither against full Solidity projects
- Support Foundry-style repositories
- Normalize findings across multiple contracts
- Group findings by contract, function, and vulnerability family
- Generate project-level Markdown and JSON reports

## Expected Usage

```bash
python3 src/main.py <solidity-project-path>
```
