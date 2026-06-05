# Mini Slither Report

## Summary

- Total findings: 19

## Findings

### S-001 - unchecked-transfer

- **Impact:** High
- **Confidence:** Medium
- **Contract:** `ShadowVault`
- **Function:** `sweep(address,address,uint256)`
- **Location:** `contract.sol#249-259`

#### Description

```txt
ShadowVault.sweep(address,address,uint256) (contract.sol#249-259) ignores return value by IERC20(token).transfer(to,amount) (contract.sol#256)

```

### S-002 - reentrancy-no-eth

- **Impact:** Medium
- **Confidence:** Medium
- **Contract:** `ShadowVault`
- **Function:** `withdraw(uint256)`
- **Location:** `contract.sol#185-209`

#### Description

```txt
Reentrancy in ShadowVault.withdraw(uint256) (contract.sol#185-209):
	External calls:
	- require(bool,string)(asset.transfer(msg.sender,assetsOut),TRANSFER_FAILED) (contract.sol#198)
	- require(bool,string)(asset.transfer(feeRecipient,fee),FEE_TRANSFER_FAILED) (contract.sol#201)
	State variables written after the call(s):
	- sharesOf[msg.sender] -= shares (contract.sol#204)
	ShadowVault.sharesOf (contract.sol#50) can be used in cross function reentrancies:
	- ShadowVault.deposit(uint256) (contract.sol#142-161)
	- ShadowVault.depositFor(address,uint256) (contract.sol#163-183)
	- ShadowVault.sharesOf (contract.sol#50)
	- ShadowVault.withdraw(uint256) (contract.sol#185-209)
	- ShadowVault.withdrawAll() (contract.sol#211-213)
	- totalAccountedAssets -= assets (contract.sol#206)
	ShadowVault.totalAccountedAssets (contract.sol#43) can be used in cross function reentrancies:
	- ShadowVault.convertToAssets(uint256) (contract.sol#130-136)
	- ShadowVault.convertToShares(uint256) (contract.sol#122-128)
	- ShadowVault.deposit(uint256) (contract.sol#142-161)
	- ShadowVault.depositFor(address,uint256) (contract.sol#163-183)
	- ShadowVault.notifyReward(uint256) (contract.sol#219-230)
	- ShadowVault.totalAccountedAssets (contract.sol#43)
	- ShadowVault.totalAssets() (contract.sol#118-120)
	- ShadowVault.withdraw(uint256) (contract.sol#185-209)
	- totalShares -= shares (contract.sol#205)
	ShadowVault.totalShares (contract.sol#42) can be used in cross function reentrancies:
	- ShadowVault.convertToAssets(uint256) (contract.sol#130-136)
	- ShadowVault.convertToShares(uint256) (contract.sol#122-128)
	- ShadowVault.deposit(uint256) (contract.sol#142-161)
	- ShadowVault.depositFor(address,uint256) (contract.sol#163-183)
	- ShadowVault.totalShares (contract.sol#42)
	- ShadowVault.withdraw(uint256) (contract.sol#185-209)

```

### S-003 - reentrancy-no-eth

- **Impact:** Medium
- **Confidence:** Medium
- **Contract:** `ShadowVault`
- **Function:** `depositFor(address,uint256)`
- **Location:** `contract.sol#163-183`

#### Description

```txt
Reentrancy in ShadowVault.depositFor(address,uint256) (contract.sol#163-183):
	External calls:
	- require(bool,string)(asset.transferFrom(msg.sender,address(this),assets),TRANSFER_FROM_FAILED) (contract.sol#173-176)
	State variables written after the call(s):
	- totalAccountedAssets += assets (contract.sol#180)
	ShadowVault.totalAccountedAssets (contract.sol#43) can be used in cross function reentrancies:
	- ShadowVault.convertToAssets(uint256) (contract.sol#130-136)
	- ShadowVault.convertToShares(uint256) (contract.sol#122-128)
	- ShadowVault.deposit(uint256) (contract.sol#142-161)
	- ShadowVault.depositFor(address,uint256) (contract.sol#163-183)
	- ShadowVault.notifyReward(uint256) (contract.sol#219-230)
	- ShadowVault.totalAccountedAssets (contract.sol#43)
	- ShadowVault.totalAssets() (contract.sol#118-120)
	- ShadowVault.withdraw(uint256) (contract.sol#185-209)
	- totalShares += shares (contract.sol#179)
	ShadowVault.totalShares (contract.sol#42) can be used in cross function reentrancies:
	- ShadowVault.convertToAssets(uint256) (contract.sol#130-136)
	- ShadowVault.convertToShares(uint256) (contract.sol#122-128)
	- ShadowVault.deposit(uint256) (contract.sol#142-161)
	- ShadowVault.depositFor(address,uint256) (contract.sol#163-183)
	- ShadowVault.totalShares (contract.sol#42)
	- ShadowVault.withdraw(uint256) (contract.sol#185-209)

```

### S-004 - reentrancy-no-eth

- **Impact:** Medium
- **Confidence:** Medium
- **Contract:** `ShadowVault`
- **Function:** `deposit(uint256)`
- **Location:** `contract.sol#142-161`

#### Description

```txt
Reentrancy in ShadowVault.deposit(uint256) (contract.sol#142-161):
	External calls:
	- require(bool,string)(asset.transferFrom(msg.sender,address(this),assets),TRANSFER_FROM_FAILED) (contract.sol#150-153)
	State variables written after the call(s):
	- totalAccountedAssets += assets (contract.sol#157)
	ShadowVault.totalAccountedAssets (contract.sol#43) can be used in cross function reentrancies:
	- ShadowVault.convertToAssets(uint256) (contract.sol#130-136)
	- ShadowVault.convertToShares(uint256) (contract.sol#122-128)
	- ShadowVault.deposit(uint256) (contract.sol#142-161)
	- ShadowVault.depositFor(address,uint256) (contract.sol#163-183)
	- ShadowVault.notifyReward(uint256) (contract.sol#219-230)
	- ShadowVault.totalAccountedAssets (contract.sol#43)
	- ShadowVault.totalAssets() (contract.sol#118-120)
	- ShadowVault.withdraw(uint256) (contract.sol#185-209)
	- totalShares += shares (contract.sol#156)
	ShadowVault.totalShares (contract.sol#42) can be used in cross function reentrancies:
	- ShadowVault.convertToAssets(uint256) (contract.sol#130-136)
	- ShadowVault.convertToShares(uint256) (contract.sol#122-128)
	- ShadowVault.deposit(uint256) (contract.sol#142-161)
	- ShadowVault.depositFor(address,uint256) (contract.sol#163-183)
	- ShadowVault.totalShares (contract.sol#42)
	- ShadowVault.withdraw(uint256) (contract.sol#185-209)

```

### S-005 - events-maths

- **Impact:** Low
- **Confidence:** Medium
- **Contract:** `ShadowVault`
- **Function:** `setWithdrawalFee(uint256)`
- **Location:** `contract.sol#101-104`

#### Description

```txt
ShadowVault.setWithdrawalFee(uint256) (contract.sol#101-104) should emit an event for: 
	- withdrawalFeeBps = newFeeBps (contract.sol#103) 

```

### S-006 - missing-zero-check

- **Impact:** Low
- **Confidence:** Medium
- **Contract:** `N/A`
- **Function:** `N/A`
- **Location:** `N/A`

#### Description

```txt
ShadowVault.setFeeRecipient(address).newFeeRecipient (contract.sol#97) lacks a zero-check on :
		- feeRecipient = newFeeRecipient (contract.sol#98)

```

### S-007 - missing-zero-check

- **Impact:** Low
- **Confidence:** Medium
- **Contract:** `N/A`
- **Function:** `N/A`
- **Location:** `N/A`

#### Description

```txt
ShadowVault.constructor(IERC20,address)._feeRecipient (contract.sol#79) lacks a zero-check on :
		- feeRecipient = _feeRecipient (contract.sol#83)

```

### S-008 - missing-zero-check

- **Impact:** Low
- **Confidence:** Medium
- **Contract:** `N/A`
- **Function:** `N/A`
- **Location:** `N/A`

#### Description

```txt
ShadowVault.setKeeper(address).newKeeper (contract.sol#90) lacks a zero-check on :
		- keeper = newKeeper (contract.sol#92)

```

### S-009 - reentrancy-benign

- **Impact:** Low
- **Confidence:** Medium
- **Contract:** `ShadowVault`
- **Function:** `deposit(uint256)`
- **Location:** `contract.sol#142-161`

#### Description

```txt
Reentrancy in ShadowVault.deposit(uint256) (contract.sol#142-161):
	External calls:
	- require(bool,string)(asset.transferFrom(msg.sender,address(this),assets),TRANSFER_FROM_FAILED) (contract.sol#150-153)
	State variables written after the call(s):
	- lastDepositTime[msg.sender] = block.timestamp (contract.sol#158)
	- sharesOf[msg.sender] += shares (contract.sol#155)

```

### S-010 - reentrancy-benign

- **Impact:** Low
- **Confidence:** Medium
- **Contract:** `ShadowVault`
- **Function:** `depositFor(address,uint256)`
- **Location:** `contract.sol#163-183`

#### Description

```txt
Reentrancy in ShadowVault.depositFor(address,uint256) (contract.sol#163-183):
	External calls:
	- require(bool,string)(asset.transferFrom(msg.sender,address(this),assets),TRANSFER_FROM_FAILED) (contract.sol#173-176)
	State variables written after the call(s):
	- sharesOf[receiver] += shares (contract.sol#178)

```

### S-011 - reentrancy-benign

- **Impact:** Low
- **Confidence:** Medium
- **Contract:** `ShadowVault`
- **Function:** `notifyReward(uint256)`
- **Location:** `contract.sol#219-230`

#### Description

```txt
Reentrancy in ShadowVault.notifyReward(uint256) (contract.sol#219-230):
	External calls:
	- require(bool,string)(asset.transferFrom(msg.sender,address(this),amount),TRANSFER_FROM_FAILED) (contract.sol#222-225)
	State variables written after the call(s):
	- totalAccountedAssets += amount (contract.sol#227)

```

### S-012 - reentrancy-events

- **Impact:** Low
- **Confidence:** Medium
- **Contract:** `ShadowVault`
- **Function:** `sweep(address,address,uint256)`
- **Location:** `contract.sol#249-259`

#### Description

```txt
Reentrancy in ShadowVault.sweep(address,address,uint256) (contract.sol#249-259):
	External calls:
	- IERC20(token).transfer(to,amount) (contract.sol#256)
	Event emitted after the call(s):
	- EmergencySweep(token,to,amount) (contract.sol#258)

```

### S-013 - reentrancy-events

- **Impact:** Low
- **Confidence:** Medium
- **Contract:** `ShadowVault`
- **Function:** `depositFor(address,uint256)`
- **Location:** `contract.sol#163-183`

#### Description

```txt
Reentrancy in ShadowVault.depositFor(address,uint256) (contract.sol#163-183):
	External calls:
	- require(bool,string)(asset.transferFrom(msg.sender,address(this),assets),TRANSFER_FROM_FAILED) (contract.sol#173-176)
	Event emitted after the call(s):
	- Deposit(receiver,assets,shares) (contract.sol#182)

```

### S-014 - reentrancy-events

- **Impact:** Low
- **Confidence:** Medium
- **Contract:** `ShadowVault`
- **Function:** `withdraw(uint256)`
- **Location:** `contract.sol#185-209`

#### Description

```txt
Reentrancy in ShadowVault.withdraw(uint256) (contract.sol#185-209):
	External calls:
	- require(bool,string)(asset.transfer(msg.sender,assetsOut),TRANSFER_FAILED) (contract.sol#198)
	- require(bool,string)(asset.transfer(feeRecipient,fee),FEE_TRANSFER_FAILED) (contract.sol#201)
	Event emitted after the call(s):
	- Withdraw(msg.sender,assetsOut,shares) (contract.sol#208)

```

### S-015 - reentrancy-events

- **Impact:** Low
- **Confidence:** Medium
- **Contract:** `ShadowVault`
- **Function:** `notifyReward(uint256)`
- **Location:** `contract.sol#219-230`

#### Description

```txt
Reentrancy in ShadowVault.notifyReward(uint256) (contract.sol#219-230):
	External calls:
	- require(bool,string)(asset.transferFrom(msg.sender,address(this),amount),TRANSFER_FROM_FAILED) (contract.sol#222-225)
	Event emitted after the call(s):
	- RewardNotified(amount) (contract.sol#229)

```

### S-016 - reentrancy-events

- **Impact:** Low
- **Confidence:** Medium
- **Contract:** `ShadowVault`
- **Function:** `deposit(uint256)`
- **Location:** `contract.sol#142-161`

#### Description

```txt
Reentrancy in ShadowVault.deposit(uint256) (contract.sol#142-161):
	External calls:
	- require(bool,string)(asset.transferFrom(msg.sender,address(this),assets),TRANSFER_FROM_FAILED) (contract.sol#150-153)
	Event emitted after the call(s):
	- Deposit(msg.sender,assets,shares) (contract.sol#160)

```

### S-017 - solc-version

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
	- ^0.8.20 (contract.sol#2)

```

### S-018 - low-level-calls

- **Impact:** Informational
- **Confidence:** High
- **Contract:** `ShadowVault`
- **Function:** `execute(address,uint256,bytes)`
- **Location:** `contract.sol#236-247`

#### Description

```txt
Low level call in ShadowVault.execute(address,uint256,bytes) (contract.sol#236-247):
	- (ok,ret) = target.call{value: value}(data) (contract.sol#243)

```

### S-019 - immutable-states

- **Impact:** Optimization
- **Confidence:** High
- **Contract:** `N/A`
- **Function:** `N/A`
- **Location:** `N/A`

#### Description

```txt
ShadowVault.owner (contract.sol#38) should be immutable 

```
