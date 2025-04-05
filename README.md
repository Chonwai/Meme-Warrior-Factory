# MemeWarriors Factory

A cross-chain meme-based trading and battle game platform on Flow EVM and Celo blockchains.

## Overview

MemeWarriors Factory is a platform that combines AI-generated meme art with blockchain technology to create tradable assets that can battle in a game economy. Users can:

1. Generate unique meme soldiers using AI
2. Mint them as blockchain tokens on Flow EVM or Celo
3. Trade their meme warriors with other users
4. Deploy warriors to battles and earn rewards

## Architecture

- Built in Backend as API, AI Agent to handle Warrior image, name and details for coin creation.
   - We utilize gpt-3.5 and openai dall-e2 to save cost, will upgrade to better model later.

- Smart Contract Deployed to Blockchain including Celo Mainnet, Testnet and Flow Testnet.
   - The contract includes Platform Token, Battle Reward, Warrior Factory and Warrior Creation.

- We connect to Metamask for Celo and Flow and World ID inside World App.

The project consists of three main components:

### Backend (FastAPI)

The backend service provides:
- AI-powered meme generation using OpenAI's DALL-E
- User authentication with blockchain wallets
- Database integration for storing user data and meme assets
- API endpoints for meme creation, battle management, and more

### Smart Contracts

The blockchain component includes:
- `MemeWarriorsToken`: Main utility token for the platform
- `WarriorFactory`: Creates and manages warrior NFTs
- `MemeWarriorsReward`: Handles battles and distributes rewards

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
- **Token Address**: `0x...` (Will be populated after full interaction test)
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

For detailed contract documentation, see the [Contract README](./contract/README.md).

### Frontend:
https://github.com/Chonwai/Meme-Warrior-Factory-NextJS/tree/main

The frontend interfaces with both the backend API and blockchain contracts to provide a seamless user experience.

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
```
cd backend
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Set up environment variables (copy .env.example to .env and fill in your values):
```
cp .env.example .env
```

4. Run the server:
```
python run.py
```

The API will be available at http://localhost:8000 with documentation at /docs.

### Contract Setup

1. Navigate to the contract directory:
```
cd contract
```

2. Install dependencies:
```
npm install
```

3. Set up environment variables:
```
cp .env.example .env
```

4. For local testing, run:
```
npm run deploy:local
```

For more details on contract deployment, see the contract directory documentation.

## Key Features

### AI Meme Generation

The system uses OpenAI's DALL-E to generate pixel art based on user prompts. Each prompt is parsed to extract two distinct themes which become the basis for meme soldiers.

### Blockchain Integration

- Cross-chain deployment on Flow EVM Testnet and Celo Mainnet
- ERC-20 token standards for warrior assets
- On-chain battle mechanics with token burning mechanisms
- Verifiable ownership and trading capabilities

### Battle System

Warriors can be deployed to the battlefield where they compete against other warriors. The battle system includes:
- Token staking for battles
- Random selection mechanism for winners
- Reward distribution based on battle outcomes
- Token burning for losing warriors

## Deployment

### Backend Deployment (Vercel)

The backend is configured for deployment on Vercel with:
- Serverless function architecture
- Vercel Blob storage for images
- Environment variable configuration for API keys

### Contract Deployment

Contracts are deployed on:
- Flow EVM Testnet
- Celo Mainnet

For detailed deployment addresses and verification links, see the [Contract README](./contract/README.md).

## License

MIT 