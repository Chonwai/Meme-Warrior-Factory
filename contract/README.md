# MemeWarriors Smart Contracts

This repository contains the smart contracts for the MemeWarriors platform built on the CELO and Flow blockchains.

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
│   ├── deploy.js            # Celo deployment
│   ├── deploy-local.js      # Local Hardhat network deployment
│   ├── deploy-flow.js       # Flow EVM deployment
│   ├── interact.js          # Interaction script for Celo
│   ├── interact-local.js    # Local interaction script
│   └── interact-flow.js     # Flow EVM interaction script
├── test/                    # Tests
│   ├── MemeWarriorsToken.test.js
│   └── WarriorToken.test.js
├── .env.example             # Example environment variables
├── FUNCTION_GUIDE.md        # Detailed guide for contract functions
├── LOCAL_TESTING.md         # Guide for local development and testing
├── FLOW_DEPLOYMENT.md       # Guide for deploying to Flow EVM
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
- A wallet with testnet funds (for Alfajores or Flow testnet deployment)

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
npm run compile
```

### Run Tests

```bash
npm test
```

### Testing Guide

For comprehensive testing, you should test the following aspects:

1. **Token functionality**: Basic ERC20 operations like transfer, approve, allowance
2. **WarriorFactory operations**: Creating warriors, deploying to battle, ending battles
3. **Reward system**: Vote distributions, battle management, reward claiming
4. **Controller permissions**: Check that only authorized addresses can burn tokens

For detailed local testing instructions, see [LOCAL_TESTING.md](./LOCAL_TESTING.md).

## Deployment Options

### 1. Local Development (Recommended for testing)

For local development and testing:

```bash
# Start a local Hardhat node in one terminal
npx hardhat node

# Deploy to local node in another terminal
npm run deploy:local

# Interact with local deployment
npm run interact:local
```

### 2. Deploy to Celo Alfajores Testnet

```bash
npm run deploy:alfajores
```

### 3. Deploy to Flow EVM Testnet

```bash
npm run deploy:flow
```

For detailed instructions on Flow EVM deployment, see [FLOW_DEPLOYMENT.md](./FLOW_DEPLOYMENT.md).

### 4. Deploy to Celo Mainnet (Production)

```bash
npx hardhat run scripts/deploy.js --network celo
```

## Contract Function Guide

For a detailed explanation of all contract functions, their parameters, and usage examples, see the [Function Guide](./FUNCTION_GUIDE.md).

## Multi-Chain Support

This project supports deployment to:
- Celo (Mainnet and Alfajores testnet)
- Flow EVM (Testnet)
- Local Hardhat network (for development)

The contracts are written in Solidity and can be deployed to any EVM-compatible blockchain.

## License

MIT 