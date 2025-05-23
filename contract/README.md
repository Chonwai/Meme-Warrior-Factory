# MemeWarriors Contract Platform

Cross-chain meme trading game platform deployed on both Flow EVM and Celo blockchains.

## Overview

MemeWarriors is a blockchain-based platform that allows users to create, trade, and battle with meme-themed warriors. The platform is deployed on both Flow EVM Testnet and Celo Mainnet.

## Deployed Contracts

### Celo Mainnet

| Contract | Address | Description |
|----------|---------|-------------|
| MemeWarriorsToken | `0xc519A9284B08D334f9a688dA7bA65cE892e73392` | Main token contract for the MemeWarriors platform |
| WarriorFactory | `0x55f59AfF32b077b06de9B6A472808757CAc51517` | Factory contract for creating and managing warriors |
| MemeWarriorsReward | `0xEC1dE75D66d683F672F711a42d69454b475beB30` | Reward mechanism for battles and achievements |

**Deployment Time**: 2025-04-05T21:01:48.986Z  
**Deployer Address**: `0xb3c7b002F7880B644C0395153658FcECb0fe4765`  
**Network**: Celo Mainnet

#### Warrior Registry (Celo Mainnet)

Warriors created during testing and deployment:

##### Warrior #0
- **Name**: Celo Alpha Warrior
- **Symbol**: CALPHAW
- **Description**: The premier alpha warrior on Celo
- **Creator**: `0xb3c7b002F7880B644C0395153658FcECb0fe4765`
- **Created**: April 5, 2025

#### Verification Links (Celo Mainnet)

- [MemeWarriorsToken](https://explorer.celo.org/address/0xc519A9284B08D334f9a688dA7bA65cE892e73392)
- [WarriorFactory](https://explorer.celo.org/address/0x55f59AfF32b077b06de9B6A472808757CAc51517)
- [MemeWarriorsReward](https://explorer.celo.org/address/0xEC1dE75D66d683F672F711a42d69454b475beB30)

### Flow EVM Testnet

| Contract | Address | Description |
|----------|---------|-------------|
| MemeWarriorsToken | `0xC4a479F0DF1090C2546f400Ab1b0Ee70a3243Ca2` | Main token contract for the MemeWarriors platform |
| WarriorFactory | `0x6c4b9e235E3e48bFeDec228c10c5951915044D0E` | Factory contract for creating and managing warriors |
| MemeWarriorsReward | `0x820651EEa47d9f9A86364D4b3e6c83D0691f0664` | Reward mechanism for battles and achievements |

**Deployment Time**: 2025-04-05T16:40:17.643Z  
**Deployer Address**: `0xb3c7b002F7880B644C0395153658FcECb0fe4765`  
**Network**: Flow EVM Testnet

#### Verification Links (Flow EVM Testnet)

- [MemeWarriorsToken](https://evm-testnet.flowscan.io/address/0xC4a479F0DF1090C2546f400Ab1b0Ee70a3243Ca2)
- [WarriorFactory](https://evm-testnet.flowscan.io/address/0x6c4b9e235E3e48bFeDec228c10c5951915044D0E)
- [MemeWarriorsReward](https://evm-testnet.flowscan.io/address/0x820651EEa47d9f9A86364D4b3e6c83D0691f0664)

Additional details about Flow EVM Testnet deployment are available in the `flow-deployment-addresses.json` file and `FLOW_DEPLOYMENT.md`.

### Celo Testnet (Alfajores)

For testing purposes, we also have deployments on Celo Alfajores Testnet. These deployments are meant for development and testing before moving to mainnet.

Details about Celo Testnet deployment and interaction can be found in the `deployment-addresses.json` file and script documentation.

## Getting Started

### Prerequisites

1. Node.js and npm installed
2. A wallet with private key and enough tokens on the target network
3. Environment variables set up in `.env` file:
   ```
   PRIVATE_KEY=your_private_key_here
   ```

### Installation

```bash
npm install
```

### Deployment

#### Deploy to Flow EVM Testnet

```bash
npm run deploy:flow-testnet
```

#### Deploy to Celo Mainnet

⚠️ **WARNING: This will deploy to MAINNET and use real funds** ⚠️

```bash
npm run deploy:celo-mainnet
```

## Interaction Guide

### Celo Mainnet

#### Basic Contract Information

To check the basic contract information without creating any transactions:

```bash
npm run check:celo-mainnet
```

This will display:
- Token name, symbol, and total supply
- Factory configuration and existing warriors
- Reward system setup and active battles

#### Creating a New Warrior

To create a new warrior on mainnet (costs real CELO):

```bash
npm run interact:celo-mainnet:full
```

This will:
1. Display a warning and 10-second countdown
2. Create a new "Celo Alpha Warrior" token
3. Deploy it to the blockchain with 1000 tokens initial supply
4. Show the transaction details and warrior token address

### Flow EVM Testnet

#### Basic Contract Information

```bash
npm run check:flow
```

#### Interaction (Check Mode)

```bash
npm run interact:flow
```

#### Interaction (Full Mode)

```bash
npm run interact:flow -- --full
```

## Architecture

The MemeWarriors platform consists of three primary contracts:

1. **MemeWarriorsToken**: ERC-20 token contract that serves as the main utility token for the platform
2. **WarriorFactory**: Creates and manages warrior NFTs, allowing users to mint their own meme warriors
3. **MemeWarriorsReward**: Handles battles between warriors and distributes rewards to winners

## Technical Details

- Creation Fee: 0.01 CELO/FLOW per warrior
- Warrior Token Standard: ERC-20 compatible tokens with mintable supply
- Battle System: On-chain random selection with time-based locks

## Security Considerations

- All contracts have been deployed with standard OpenZeppelin libraries
- Ownership controls are in place for administrative functions
- The deployer address is the initial admin for all contracts
- Gas optimization has been implemented for all transactions

## Maintenance

For future updates or interactions, ensure your wallet has sufficient tokens for gas fees. The contract uses dynamic gas pricing with a 30% buffer over the current network price to ensure transactions are processed.

## License

MIT 