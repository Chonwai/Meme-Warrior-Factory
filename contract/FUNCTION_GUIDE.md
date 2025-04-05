# MemeWarriors Smart Contract Function Guide

This guide documents all the functions available in the MemeWarriors smart contracts, explaining their purpose, parameters, and usage.

## Table of Contents

1. [MemeWarriorsToken](#memewarriorstoken)
2. [WarriorToken](#warriortoken)
3. [WarriorFactory](#warriorfactory)
4. [MemeWarriorsReward](#memewarriorsreward)

---

## MemeWarriorsToken

The main platform token for the MemeWarriors game.

### Constructor

```solidity
constructor()
```

Creates the MemeWarriorsToken with name "MemeWarriors" and symbol "MWAR". Mints 1,000,000 tokens to the contract deployer.

### Functions

#### `mint`

```solidity
function mint(address to, uint256 amount) public onlyOwner
```

**Description:** Mints new tokens to the specified address. Only callable by the contract owner.

**Parameters:**
- `to`: The address that will receive the minted tokens
- `amount`: The amount of tokens to mint

**Usage Example:**
```javascript
await memeWarriorsToken.mint("0x123...", ethers.utils.parseEther("1000"));
```

#### `burn`

```solidity
function burn(uint256 amount) public
```

**Description:** Burns (destroys) a specific amount of tokens from the caller's balance.

**Parameters:**
- `amount`: The amount of tokens to burn

**Usage Example:**
```javascript
await memeWarriorsToken.burn(ethers.utils.parseEther("500"));
```

#### `decimals`

```solidity
function decimals() public view virtual override returns (uint8)
```

**Description:** Returns the number of decimals used by the token (18).

**Returns:** The number of decimals (18)

**Usage Example:**
```javascript
const decimals = await memeWarriorsToken.decimals();
console.log(decimals); // 18
```

---

## WarriorToken

ERC20 token representing a specific Meme Warrior.

### Constructor

```solidity
constructor(string memory name, string memory symbol, address initialOwner, uint256 initialSupply)
```

Creates a new WarriorToken with the specified name, symbol, owner, and supply.

**Parameters:**
- `name`: Token name (e.g., "Cool Doge Warrior")
- `symbol`: Token symbol (e.g., "CDW")
- `initialOwner`: The address that will own the token contract
- `initialSupply`: Initial supply of tokens to mint

### Functions

#### `setController`

```solidity
function setController(address controller, bool status) external onlyOwner
```

**Description:** Sets or removes an address as a controller. Controllers have permission to burn tokens from any address.

**Parameters:**
- `controller`: Address to set as controller
- `status`: True to add, false to remove

**Usage Example:**
```javascript
await warriorToken.setController("0x456...", true);
```

#### `isController`

```solidity
function isController(address account) external view returns (bool)
```

**Description:** Checks if an address is a controller.

**Parameters:**
- `account`: Address to check

**Returns:** True if the address is a controller, false otherwise

**Usage Example:**
```javascript
const isController = await warriorToken.isController("0x456...");
console.log(isController); // true or false
```

#### `mint`

```solidity
function mint(address to, uint256 amount) external onlyOwner
```

**Description:** Mints new tokens to the specified address. Only callable by the contract owner.

**Parameters:**
- `to`: Address to mint tokens to
- `amount`: Amount of tokens to mint

**Usage Example:**
```javascript
await warriorToken.mint("0x789...", ethers.utils.parseEther("100"));
```

#### `burnFrom`

```solidity
function burnFrom(address account, uint256 amount) public override onlyController
```

**Description:** Burns tokens from a specific account. Only callable by controllers.

**Parameters:**
- `account`: Address to burn tokens from
- `amount`: Amount of tokens to burn

**Usage Example:**
```javascript
await warriorToken.burnFrom("0x789...", ethers.utils.parseEther("50"));
```

---

## WarriorFactory

Factory contract for creating and managing Meme Warrior tokens.

### Constructor

```solidity
constructor()
```

Initializes the WarriorFactory with the deployer as both the owner and fee collector.

### Functions

#### `createWarrior`

```solidity
function createWarrior(
    string memory _name,
    string memory _symbol,
    string memory _description,
    string memory _imageURI,
    uint256 _initialSupply
) external payable returns (uint256)
```

**Description:** Creates a new Meme Warrior token with the specified parameters. Requires payment for platform fee.

**Parameters:**
- `_name`: Token name
- `_symbol`: Token symbol
- `_description`: Warrior description
- `_imageURI`: URI to the warrior image
- `_initialSupply`: Initial token supply

**Returns:** The ID of the created warrior

**Usage Example:**
```javascript
const warriorId = await warriorFactory.createWarrior(
    "Doge Warrior",
    "DOGEW",
    "A warrior based on the Doge meme",
    "https://example.com/doge.png",
    ethers.utils.parseEther("1000"),
    { value: ethers.utils.parseEther("0.1") }
);
```

#### `deployWarrior`

```solidity
function deployWarrior(uint256 _warriorId, uint256 _amount) external
```

**Description:** Deploys a warrior to battle by transferring tokens to the battlefield wallet.

**Parameters:**
- `_warriorId`: ID of the warrior to deploy
- `_amount`: Amount of tokens to deploy

**Usage Example:**
```javascript
await warriorFactory.deployWarrior(1, ethers.utils.parseEther("100"));
```

#### `endBattle`

```solidity
function endBattle(uint256 _winnerWarriorId, uint256 _loserWarriorId, uint256 _burnAmount) external onlyBattlefield
```

**Description:** Ends a battle and burns loser tokens. Only callable by the battlefield wallet.

**Parameters:**
- `_winnerWarriorId`: ID of the winning warrior
- `_loserWarriorId`: ID of the losing warrior
- `_burnAmount`: Amount of loser tokens to burn

**Usage Example:**
```javascript
await warriorFactory.endBattle(1, 2, ethers.utils.parseEther("50"));
```

#### `retireWarrior`

```solidity
function retireWarrior(uint256 _warriorId) external
```

**Description:** Retires a warrior from battle. Only callable by the warrior creator or contract owner.

**Parameters:**
- `_warriorId`: ID of the warrior to retire

**Usage Example:**
```javascript
await warriorFactory.retireWarrior(1);
```

#### `getWarrior`

```solidity
function getWarrior(uint256 _warriorId) external view returns (
    string memory name,
    string memory description,
    string memory imageURI,
    uint256 created,
    address creator,
    bool active,
    address tokenAddress
)
```

**Description:** Gets warrior metadata.

**Parameters:**
- `_warriorId`: ID of the warrior

**Returns:** Warrior metadata (name, description, imageURI, creation time, creator, active status, token address)

**Usage Example:**
```javascript
const warrior = await warriorFactory.getWarrior(1);
console.log(warrior.name, warrior.description, warrior.active);
```

#### `getUserWarriors`

```solidity
function getUserWarriors(address _user) external view returns (uint256[] memory)
```

**Description:** Gets a user's warriors.

**Parameters:**
- `_user`: Address of the user

**Returns:** Array of warrior IDs created by the user

**Usage Example:**
```javascript
const warriorIds = await warriorFactory.getUserWarriors("0x123...");
console.log(warriorIds); // [1, 3, 5]
```

#### `setPlatformFee`

```solidity
function setPlatformFee(uint256 _newFee) external onlyOwner
```

**Description:** Sets the platform fee in basis points (100 = 1%). Only callable by the contract owner.

**Parameters:**
- `_newFee`: New fee in basis points

**Usage Example:**
```javascript
await warriorFactory.setPlatformFee(300); // 3%
```

#### `setFeeCollector`

```solidity
function setFeeCollector(address _newCollector) external onlyOwner
```

**Description:** Sets the fee collector address. Only callable by the contract owner.

**Parameters:**
- `_newCollector`: New fee collector address

**Usage Example:**
```javascript
await warriorFactory.setFeeCollector("0x789...");
```

#### `setBattlefieldWallet`

```solidity
function setBattlefieldWallet(address _newBattlefieldWallet) external onlyOwner
```

**Description:** Sets the battlefield wallet address. Only callable by the contract owner.

**Parameters:**
- `_newBattlefieldWallet`: New battlefield wallet address

**Usage Example:**
```javascript
await warriorFactory.setBattlefieldWallet("0xabc...");
```

---

## MemeWarriorsReward

Reward system for the MemeWarriors game.

### Constructor

```solidity
constructor(address _tokenAddress)
```

Initializes the MemeWarriorsReward contract with the MemeWarriorsToken address.

**Parameters:**
- `_tokenAddress`: Address of the MemeWarriorsToken contract

### Functions

#### `createBattle`

```solidity
function createBattle(
    uint256 _team1Id,
    uint256 _team2Id,
    uint256 _startTime,
    uint256 _duration,
    uint256 _rewardPool
) external onlyOwner
```

**Description:** Creates a new battle between two teams. Only callable by the contract owner.

**Parameters:**
- `_team1Id`: ID of the first team
- `_team2Id`: ID of the second team
- `_startTime`: Start time of the battle (Unix timestamp)
- `_duration`: Duration of the battle in seconds
- `_rewardPool`: Initial reward pool for the battle

**Usage Example:**
```javascript
const now = Math.floor(Date.now() / 1000);
await memeWarriorsReward.createBattle(
    1, // Team 1 ID
    2, // Team 2 ID
    now + 3600, // Start 1 hour from now
    7200, // Duration 2 hours
    ethers.utils.parseEther("1000") // 1000 tokens as reward
);
```

#### `voteForTeam`

```solidity
function voteForTeam(uint256 _battleId, uint256 _teamId) external
```

**Description:** Casts a vote for a team in a battle.

**Parameters:**
- `_battleId`: ID of the battle
- `_teamId`: ID of the team to vote for

**Usage Example:**
```javascript
await memeWarriorsReward.voteForTeam(0, 1); // Vote for team 1 in battle 0
```

#### `endBattle`

```solidity
function endBattle(uint256 _battleId, uint256 _winningTeamId) external onlyOwner
```

**Description:** Ends a battle and sets the winning team. Only callable by the contract owner.

**Parameters:**
- `_battleId`: ID of the battle
- `_winningTeamId`: ID of the winning team

**Usage Example:**
```javascript
await memeWarriorsReward.endBattle(0, 2); // Team 2 wins battle 0
```

#### `claimReward`

```solidity
function claimReward(uint256 _battleId) external
```

**Description:** Claims rewards for correct votes in a battle.

**Parameters:**
- `_battleId`: ID of the battle to claim rewards for

**Usage Example:**
```javascript
await memeWarriorsReward.claimReward(0);
```

#### `getBattle`

```solidity
function getBattle(uint256 _battleId) external view returns (
    uint256 team1Id,
    uint256 team2Id,
    uint256 startTime,
    uint256 endTime,
    uint256 winningTeamId,
    bool isEnded,
    uint256 totalVotes,
    uint256 rewardPool
)
```

**Description:** Gets battle details.

**Parameters:**
- `_battleId`: ID of the battle

**Returns:** Battle details (team IDs, start/end times, winner, status, votes, reward pool)

**Usage Example:**
```javascript
const battle = await memeWarriorsReward.getBattle(0);
console.log(battle.isEnded, battle.winningTeamId, battle.totalVotes);
```

#### `setTokenAddress`

```solidity
function setTokenAddress(address _newTokenAddress) external onlyOwner
```

**Description:** Changes the token address. Only callable by the contract owner.

**Parameters:**
- `_newTokenAddress`: Address of the new token contract

**Usage Example:**
```javascript
await memeWarriorsReward.setTokenAddress("0xdef...");
``` 