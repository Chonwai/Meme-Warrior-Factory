# Flow EVM Deployment Guide

This guide walks you through deploying the MemeWarriors contracts to Flow's EVM-compatible testnet.

## Prerequisites

1. An Ethereum wallet with private key (like MetaMask)
2. Flow testnet tokens (FLOW)

## Step 1: Add Flow EVM to MetaMask

1. Open MetaMask and click on the network dropdown
2. Select "Add Network"
3. Click "Add Network Manually"
4. Enter the following details:
   - Network Name: Flow Testnet
   - RPC URL: https://testnet.evm.nodes.onflow.org
   - Chain ID: 545
   - Currency Symbol: FLOW
   - Block Explorer URL: https://evm-testnet.flowscan.io/

## Step 2: Get Testnet FLOW Tokens

Visit the Flow Testnet Faucet to get testnet tokens:
https://testnet-faucet.onflow.org/

1. Enter your Flow EVM wallet address (the same address as your Ethereum wallet in MetaMask)
2. Request tokens

## Step 3: Set Up Environment Variables

Create or modify your `.env` file to include your private key:

```
PRIVATE_KEY=your_private_key_here
```

**IMPORTANT**: Never share your private key or commit it to version control.

## Step 4: Deploy to Flow EVM Testnet

Run the deployment script:

```bash
npx hardhat run scripts/deploy-flow.js --network flow_testnet
```

This will:
1. Deploy MemeWarriorsToken, WarriorFactory, and MemeWarriorsReward contracts
2. Configure initial permissions
3. Save the deployment addresses to `flow-deployment-addresses.json`

## Step 5: Verify Contracts (Optional)

Verify your contracts on the Flow EVM Block Explorer:

```bash
# Replace with your actual contract addresses from flow-deployment-addresses.json
npx hardhat verify --network flow_testnet YOUR_TOKEN_ADDRESS
npx hardhat verify --network flow_testnet YOUR_FACTORY_ADDRESS
npx hardhat verify --network flow_testnet YOUR_REWARD_ADDRESS "YOUR_TOKEN_ADDRESS"
```

## Step 6: Interact with Deployed Contracts

Run the interaction script to test your deployed contracts:

```bash
npx hardhat run scripts/interact-flow.js --network flow_testnet
```

This script will:
1. Create warriors
2. Deploy warriors to battle
3. Create and participate in battles
4. End battles and claim rewards

## Viewing Your Contracts and Transactions

You can view your deployed contracts and transactions on the Flow EVM Block Explorer:
https://evm-testnet.flowscan.io/

Enter your wallet address or contract addresses to see details.

## Flow vs. Celo Considerations

While both Flow EVM and Celo are EVM-compatible, there are some differences:

1. **Gas Prices**: Flow EVM may have different gas price dynamics than Celo
2. **Block Times**: Flow has faster block times (around 1 second) compared to Celo
3. **Native Token**: Flow uses FLOW as its native token, rather than CELO

## Troubleshooting

If you encounter issues:

- **Connection Errors**: Make sure you're using the correct RPC endpoint
- **Gas Errors**: Adjust the gas settings in hardhat.config.js
- **Transaction Failures**: Check that you have enough FLOW for gas
- **Verification Issues**: Make sure the contract source matches exactly what was deployed

For more detailed information, refer to the [Flow EVM documentation](https://developers.flow.com/evm). 