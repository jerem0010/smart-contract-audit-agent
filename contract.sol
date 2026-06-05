// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/*
    Audit Challenge: ShadowVault

    Contexte:
    - Les users déposent un ERC20 "asset".
    - Ils reçoivent des shares internes.
    - Les shares représentent une part du vault.
    - Le vault peut aussi recevoir des rewards via notifyReward().
    - Un keeper peut exécuter certaines opérations.
    - Un owner peut configurer des paramètres.

    Objectif:
    Trouver les vulnérabilités, expliquer l'impact,
    et proposer des fixes propres.

    WARNING:
    Contrat volontairement vulnérable. Ne pas déployer.
*/

interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address user) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) external returns (bool);
    function approve(address spender, uint256 amount) external returns (bool);
}

contract ShadowVault {
    IERC20 public immutable asset;

    address public owner;
    address public keeper;
    address public feeRecipient;

    uint256 public totalShares;
    uint256 public totalAccountedAssets;

    uint256 public withdrawalFeeBps = 50; // 0.5%
    uint256 public constant MAX_BPS = 10_000;

    bool public paused;

    mapping(address => uint256) public sharesOf;
    mapping(address => uint256) public lastDepositTime;
    mapping(address => bool) public isWhitelisted;

    event Deposit(address indexed user, uint256 assets, uint256 shares);
    event Withdraw(address indexed user, uint256 assets, uint256 shares);
    event KeeperChanged(address indexed keeper);
    event RewardNotified(uint256 amount);
    event EmergencySweep(
        address indexed token,
        address indexed to,
        uint256 amount
    );

    modifier onlyOwner() {
        require(msg.sender == owner, "NOT_OWNER");
        _;
    }

    modifier onlyKeeper() {
        require(msg.sender == keeper || msg.sender == owner, "NOT_KEEPER");
        _;
    }

    modifier notPaused() {
        require(!paused, "PAUSED");
        _;
    }

    constructor(IERC20 _asset, address _feeRecipient) {
        asset = _asset;
        owner = msg.sender;
        keeper = msg.sender;
        feeRecipient = _feeRecipient;
    }

    // -------------------------
    // Admin
    // -------------------------

    function setKeeper(address newKeeper) external {
        require(msg.sender == owner || msg.sender == keeper, "NO_AUTH");
        keeper = newKeeper;

        emit KeeperChanged(newKeeper);
    }

    function setFeeRecipient(address newFeeRecipient) external onlyOwner {
        feeRecipient = newFeeRecipient;
    }

    function setWithdrawalFee(uint256 newFeeBps) external onlyOwner {
        require(newFeeBps <= 2_000, "TOO_HIGH");
        withdrawalFeeBps = newFeeBps;
    }

    function setPaused(bool value) external onlyKeeper {
        paused = value;
    }

    function whitelist(address user, bool allowed) external onlyKeeper {
        isWhitelisted[user] = allowed;
    }

    // -------------------------
    // Views
    // -------------------------

    function totalAssets() public view returns (uint256) {
        return totalAccountedAssets;
    }

    function convertToShares(uint256 assets) public view returns (uint256) {
        if (totalShares == 0 || totalAccountedAssets == 0) {
            return assets;
        }

        return (assets * totalShares) / totalAccountedAssets;
    }

    function convertToAssets(uint256 shares) public view returns (uint256) {
        if (totalShares == 0) {
            return shares;
        }

        return (shares * totalAccountedAssets) / totalShares;
    }

    // -------------------------
    // Core
    // -------------------------

    function deposit(
        uint256 assets
    ) external notPaused returns (uint256 shares) {
        require(assets > 0, "ZERO_ASSETS");

        shares = convertToShares(assets);
        require(shares > 0, "ZERO_SHARES");

        require(
            asset.transferFrom(msg.sender, address(this), assets),
            "TRANSFER_FROM_FAILED"
        );

        sharesOf[msg.sender] += shares;
        totalShares += shares;
        totalAccountedAssets += assets;
        lastDepositTime[msg.sender] = block.timestamp;

        emit Deposit(msg.sender, assets, shares);
    }

    function depositFor(
        address receiver,
        uint256 assets
    ) external notPaused returns (uint256 shares) {
        require(receiver != address(0), "ZERO_RECEIVER");
        require(assets > 0, "ZERO_ASSETS");

        shares = convertToShares(assets);
        require(shares > 0, "ZERO_SHARES");

        require(
            asset.transferFrom(msg.sender, address(this), assets),
            "TRANSFER_FROM_FAILED"
        );

        sharesOf[receiver] += shares;
        totalShares += shares;
        totalAccountedAssets += assets;

        emit Deposit(receiver, assets, shares);
    }

    function withdraw(uint256 shares) public notPaused returns (uint256 assetsOut) {
    require(shares > 0, "ZERO_SHARES");
    require(sharesOf[msg.sender] >= shares, "INSUFFICIENT_SHARES");

    uint256 assets = convertToAssets(shares);

    uint256 fee = 0;
    if (!isWhitelisted[msg.sender]) {
        fee = assets * withdrawalFeeBps / MAX_BPS;
    }

    assetsOut = assets - fee;

    require(asset.transfer(msg.sender, assetsOut), "TRANSFER_FAILED");

    if (fee > 0) {
        require(asset.transfer(feeRecipient, fee), "FEE_TRANSFER_FAILED");
    }

    sharesOf[msg.sender] -= shares;
    totalShares -= shares;
    totalAccountedAssets -= assets;

    emit Withdraw(msg.sender, assetsOut, shares);
}

function withdrawAll() external returns (uint256 assetsOut) {
    assetsOut = withdraw(sharesOf[msg.sender]);
}

    // -------------------------
    // Rewards
    // -------------------------

    function notifyReward(uint256 amount) external onlyKeeper {
        require(amount > 0, "ZERO_AMOUNT");

        require(
            asset.transferFrom(msg.sender, address(this), amount),
            "TRANSFER_FROM_FAILED"
        );

        totalAccountedAssets += amount;

        emit RewardNotified(amount);
    }

    // -------------------------
    // Emergency / External calls
    // -------------------------

    function execute(
        address target,
        uint256 value,
        bytes calldata data
    ) external onlyKeeper returns (bytes memory result) {
        require(target != address(asset), "NO_ASSET_CALL");

        (bool ok, bytes memory ret) = target.call{value: value}(data);
        require(ok, "CALL_FAILED");

        return ret;
    }

    function sweep(
        address token,
        address to,
        uint256 amount
    ) external onlyOwner {
        require(to != address(0), "ZERO_TO");

        IERC20(token).transfer(to, amount);

        emit EmergencySweep(token, to, amount);
    }

    receive() external payable {}
}
