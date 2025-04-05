# MemeWarriors Smart Contracts

This repository contains the smart contracts for the MemeWarriors platform built on the CELO blockchain.

## Overview

MemeWarriors is a fun and engaging platform where users can:
- Create meme-inspired tokens
- Deploy their warriors to battle
- Vote for warriors in battles
- Earn rewards for successfully predicting battle outcomes

## Project Structure

```
meme-warriors-contract/
├── contracts/               # Smart contract source code
│   ├── core/                # Core contracts
│   │   ├── MemeWarriorsReward.sol
│   │   └── WarriorFactory.sol
│   ├── interfaces/          # Contract interfaces
│   │   ├── IMemeWarriorsReward.sol
│   │   ├── IMemeWarriorsToken.sol
│   │   ├── IWarriorFactory.sol
│   │   └── IWarriorToken.sol
│   └── tokens/              # Token contracts
│       ├── MemeWarriorsToken.sol
│       └── WarriorToken.sol
├── scripts/                 # Deployment scripts
│   └── deploy.js
├── test/                    # Tests
│   ├── MemeWarriorsToken.test.js
│   └── WarriorToken.test.js
├── .env.example             # Example environment variables
├── FUNCTION_GUIDE.md        # Detailed guide for contract functions
├── hardhat.config.js        # Hardhat configuration
├── package.json             # Project dependencies
└── README.md                # This file
```

## Contracts

1. **MemeWarriorsToken**: The main platform token for the MemeWarriors game.
2. **MemeWarriorsReward**: The reward system for users who successfully vote/guess winning teams.
3. **WarriorFactory**: For creating warrior tokens.
4. **WarriorToken**: The ERC20 token representing a single meme warrior.

## Development

### Prerequisites

- Node.js (v14 or later)
- npm or yarn
- A Celo wallet with testnet funds (for Alfajores deployment)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/meme-warriors-contract.git
cd meme-warriors-contract
```

2. Install dependencies:
```bash
npm install
```

3. Copy the environment example file and fill in your private key:
```bash
cp .env.example .env
# Edit .env to add your private key
```

### Compile Contracts

```bash
npx hardhat compile
```

### Run Tests

```bash
npx hardhat test
```

### Testing Guide

For comprehensive testing, you should test the following aspects:

1. **Token functionality**: Basic ERC20 operations like transfer, approve, allowance
2. **WarriorFactory operations**: Creating warriors, deploying to battle, ending battles
3. **Reward system**: Vote distributions, battle management, reward claiming
4. **Controller permissions**: Check that only authorized addresses can burn tokens

Here's a simple test workflow:

1. Deploy all contracts
2. Create some warriors using different accounts
3. Deploy warriors to battle
4. Simulate battles and end them
5. Check token distributions and balances
6. Test the vote and reward system

### Deploy to Alfajores Testnet

```bash
npx hardhat run scripts/deploy.js --network alfajores
```

### Deploy to Celo Mainnet

```bash
npx hardhat run scripts/deploy.js --network celo
```

## Contract Function Guide

For a detailed explanation of all contract functions, their parameters, and usage examples, see the [Function Guide](./FUNCTION_GUIDE.md).

## License

MIT 