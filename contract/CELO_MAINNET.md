# MemeWarriors on Celo Mainnet

This document contains information about the MemeWarriors contract deployment on Celo Mainnet, including contract addresses, interactions, and verification details.

## Deployed Contracts

| Contract | Address | Description |
|----------|---------|-------------|
| MemeWarriorsToken | `0xc519A9284B08D334f9a688dA7bA65cE892e73392` | Main token contract for the MemeWarriors platform |
| WarriorFactory | `0x55f59AfF32b077b06de9B6A472808757CAc51517` | Factory contract for creating and managing warriors |
| MemeWarriorsReward | `0xEC1dE75D66d683F672F711a42d69454b475beB30` | Reward mechanism for battles and achievements |

**Deployment Time**: 2025-04-05T21:01:48.986Z  
**Deployer Address**: `0xb3c7b002F7880B644C0395153658FcECb0fe4765`  
**Network**: Celo Mainnet

## Warrior Registry

Below are the warriors created during testing and deployment:

### Warrior #0
- **Name**: Celo Alpha Warrior
- **Symbol**: CALPHAW
- **Description**: The premier alpha warrior on Celo
- **Token Address**: `0x...` (Will be populated after full interaction test)
- **Creator**: `0xb3c7b002F7880B644C0395153658FcECb0fe4765`
- **Created**: April 5, 2025

## Verification Links

All contracts have been verified on Celo Explorer:

- [MemeWarriorsToken](https://explorer.celo.org/address/0xc519A9284B08D334f9a688dA7bA65cE892e73392)
- [WarriorFactory](https://explorer.celo.org/address/0x55f59AfF32b077b06de9B6A472808757CAc51517)
- [MemeWarriorsReward](https://explorer.celo.org/address/0xEC1dE75D66d683F672F711a42d69454b475beB30)

## Interaction Guide

### Basic Contract Information

To check the basic contract information without creating any transactions:

```bash
npm run check:celo-mainnet
```

This will display:
- Token name, symbol, and total supply
- Factory configuration and existing warriors
- Reward system setup and active battles

### Creating a New Warrior

To create a new warrior on mainnet (costs real CELO):

```bash
npm run interact:celo-mainnet:full
```

This will:
1. Display a warning and 10-second countdown
2. Create a new "Celo Alpha Warrior" token
3. Deploy it to the blockchain with 1000 tokens initial supply
4. Show the transaction details and warrior token address

## Architecture

The MemeWarriors platform on Celo Mainnet consists of three primary contracts:

1. **MemeWarriorsToken**: ERC-20 token contract that serves as the main utility token for the platform
2. **WarriorFactory**: Creates and manages warrior NFTs, allowing users to mint their own meme warriors
3. **MemeWarriorsReward**: Handles battles between warriors and distributes rewards to winners

## Security Considerations

- All contracts have been deployed with standard OpenZeppelin libraries
- Ownership controls are in place for administrative functions
- The deployer address (`0xb3c7b002F7880B644C0395153658FcECb0fe4765`) is the initial admin for all contracts
- Gas optimization has been implemented for all transactions

## Technical Details

Creation Fee: 0.01 CELO per warrior
Warrior Token Standard: ERC-20 compatible tokens with mintable supply
Battle System: On-chain random selection with time-based locks

## Maintenance

For future updates or interactions, ensure your wallet has sufficient CELO for gas fees. The contract uses dynamic gas pricing with a 30% buffer over the current network price to ensure transactions are processed. 