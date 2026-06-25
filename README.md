# Smart Contract Audit Agent Workspace

This repository now contains two audit-agent versions:

```txt
single-contract-audit-agent/   Current prototype for one Solidity target
project-audit-agent/           New project-level version scaffold
```

## Current Version

```bash
cd single-contract-audit-agent
python3 src/main.py examples/contract2.sol
python3 -m unittest
```

## New Version

`project-audit-agent/` is reserved for the next implementation, focused on auditing larger Solidity projects with Slither.
