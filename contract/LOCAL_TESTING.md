# Local Development and Testing Guide for MemeWarriors

This guide will walk you through setting up, deploying, and testing the MemeWarriors contracts locally.

## Prerequisites

- Node.js (v14 or later)
- npm or yarn
- Hardhat installed

## Step 1: Clone and Install Dependencies

```bash
git clone https://github.com/your-username/meme-warriors-contract.git
cd meme-warriors-contract
npm install
```

## Step 2: Compile the Contracts

```bash
npx hardhat compile
```

If compilation is successful, you're ready to test the contracts locally.

## Step 3: Start a Local Hardhat Node

In a separate terminal window, start a local Hardhat node:

```bash
npx hardhat node
```

This will start a local Ethereum node with pre-funded accounts for testing.

## Step 4: Deploy Contracts Locally

In a new terminal window, deploy the contracts to your local node:

```bash
npx hardhat run scripts/deploy-local.js --network localhost
```

This will:
1. Deploy all required contracts
2. Set up initial permissions
3. Save deployment addresses to `deployment-addresses-local.json`

## Step 5: Interact with Contracts

Now you can run the interaction script to test the contracts:

```bash
npx hardhat run scripts/interact-local.js --network localhost
```

This script will:
1. Create two warriors
2. Deploy warriors to battle
3. Create a battle
4. Vote in the battle
5. End the battle
6. Claim rewards

## Step 6: Check the Results

After running the interaction script, you should see output showing:
- The created warriors
- Battle details
- Token balances before and after claiming rewards

## Local Testing Workflow

For ongoing development, follow this workflow:

1. Make changes to the contracts
2. Run `npx hardhat compile` to compile changes
3. Restart the local node if necessary
4. Redeploy with `npx hardhat run scripts/deploy-local.js --network localhost`
5. Test with `npx hardhat run scripts/interact-local.js --network localhost`

## Troubleshooting

If you encounter any issues:

- **Nonce errors**: Restart the Hardhat node and redeploy
- **Gas errors**: Check the Hardhat config and adjust gas settings
- **Transaction failures**: Check error messages for requirements/conditions not met

## Moving to Testnet

When you're ready to deploy to Alfajores testnet:

1. Get testnet CELO from the faucet (https://faucet.celo.org)
2. Set up your `.env` file with your private key
3. Deploy with `npx hardhat run scripts/deploy.js --network alfajores` 