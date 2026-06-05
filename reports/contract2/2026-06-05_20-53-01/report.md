# Mini Slither Report

## Summary

- Total findings: 3

## Findings

### S-001 - reentrancy-eth

- **Impact:** High
- **Confidence:** Medium
- **Contract:** `Vault`
- **Function:** `withdraw(uint256)`
- **Location:** `contract2.sol#11-19`

#### Description

```txt
Reentrancy in Vault.withdraw(uint256) (contract2.sol#11-19):
	External calls:
	- (success,None) = msg.sender.call{value: amount}() (contract2.sol#15)
	State variables written after the call(s):
	- balances[msg.sender] -= amount (contract2.sol#18)
	Vault.balances (contract2.sol#5) can be used in cross function reentrancies:
	- Vault.balances (contract2.sol#5)
	- Vault.deposit() (contract2.sol#7-9)
	- Vault.withdraw(uint256) (contract2.sol#11-19)

```

### S-002 - solc-version

- **Impact:** Informational
- **Confidence:** High
- **Contract:** `N/A`
- **Function:** `N/A`
- **Location:** `N/A`

#### Description

```txt
Version constraint ^0.8.20 contains known severe issues (https://solidity.readthedocs.io/en/latest/bugs.html)
	- VerbatimInvalidDeduplication
	- FullInlinerNonExpressionSplitArgumentEvaluationOrder
	- MissingSideEffectsOnSelectorAccess.
It is used by:
	- ^0.8.20 (contract2.sol#2)

```

### S-003 - low-level-calls

- **Impact:** Informational
- **Confidence:** High
- **Contract:** `Vault`
- **Function:** `withdraw(uint256)`
- **Location:** `contract2.sol#11-19`

#### Description

```txt
Low level call in Vault.withdraw(uint256) (contract2.sol#11-19):
	- (success,None) = msg.sender.call{value: amount}() (contract2.sol#15)

```
