# MemeWarriors Contract Deployment Guide

This guide explains how to deploy and interact with the MemeWarriors contracts on both Flow EVM Testnet and Celo Mainnet.

## Prerequisites

1. Node.js and npm installed
2. A wallet with private key and enough tokens on the target network
3. Environment variables set up in `.env` file:
   ```
   PRIVATE_KEY=your_private_key_here
   ```

## Flow EVM Testnet Deployment

### Step 1: Deploy Contracts to Flow EVM Testnet

Run the deployment script:

```bash
npm run deploy:flow-testnet
```

This will:
1. Deploy MemeWarriorsToken, WarriorFactory, and MemeWarriorsReward contracts
2. Set up initial configurations
3. Save deployment addresses to `flow-deployment-addresses.json`

### Step 2: Check Deployment Status

To verify the contracts were deployed correctly:

```bash
npm run check:flow
```

This will:
1. Check if contracts exist on-chain
2. Display basic contract information
3. Show links to FlowScan explorer

### Step 3: Interact with Flow Contracts

For basic contract interaction:

```bash
npm run interact:flow
```

For full interaction mode (creating warriors, etc.):

```bash
npm run interact:flow -- --full
```

## Celo Mainnet Deployment

### Step 1: Deploy Contracts to Celo Mainnet

⚠️ **WARNING: This will deploy to MAINNET and use real funds** ⚠️

Run the deployment script:

```bash
npm run deploy:celo-mainnet
```

This will:
1. Wait 10 seconds to allow cancellation (since this is mainnet)
2. Deploy all contracts to Celo Mainnet
3. Set up initial configurations
4. Save deployment addresses to `celo-mainnet-deployment-addresses.json`

### Step 2: Check Deployment Status

To verify the contracts were deployed correctly:

```bash
npm run check:celo-mainnet
```

### Step 3: Interact with Celo Mainnet Contracts

For basic contract information:

```bash
npm run interact:celo-mainnet
```

For full interaction mode (with additional safety checks):

```bash
npm run interact:celo-mainnet -- --full
```

## Contract Verification

### Verifying on Flow EVM Testnet

```bash
# Replace with your actual contract addresses from flow-deployment-addresses.json
npx hardhat verify --network flow_testnet YOUR_TOKEN_ADDRESS
npx hardhat verify --network flow_testnet YOUR_FACTORY_ADDRESS
npx hardhat verify --network flow_testnet YOUR_REWARD_ADDRESS "YOUR_TOKEN_ADDRESS"
```

### Verifying on Celo Mainnet

```bash
# Replace with your actual contract addresses from celo-mainnet-deployment-addresses.json
npx hardhat verify --network celo YOUR_TOKEN_ADDRESS
npx hardhat verify --network celo YOUR_FACTORY_ADDRESS
npx hardhat verify --network celo YOUR_REWARD_ADDRESS "YOUR_TOKEN_ADDRESS"
```

## Troubleshooting

### Common Issues

1. **Gas Errors**: If you encounter gas-related errors, try increasing the `gasLimit` in the deployment script.

2. **Transaction Failures**: Make sure you have enough tokens for gas fees on the target network.

3. **Network Connection Issues**: Check that the RPC endpoints in `hardhat.config.js` are correct and accessible.

4. **Verification Failures**: Make sure compiler settings match exactly between deployment and verification.

### Getting Help

If you encounter issues, check the error messages for details or reach out to the development team for assistance. 