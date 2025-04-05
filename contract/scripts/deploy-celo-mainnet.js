const { ethers, network } = require("hardhat");

async function main() {
  console.log("Starting deployment to Celo Mainnet...");
  console.log("Network:", network.name);

  // Get the deployer account
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);
  console.log("Account balance:", ethers.utils.formatEther(await deployer.getBalance()));

  // Wait for confirmation before proceeding with mainnet deployment
  await manualConfirmation();
  
  // Get current gas price and add buffer
  console.log("Fetching current gas price...");
  const currentGasPrice = await ethers.provider.getGasPrice();
  // Multiply by 1.3 to ensure we're above minimum
  const gasPrice = currentGasPrice.mul(130).div(100);
  console.log(`Current gas price: ${ethers.utils.formatUnits(currentGasPrice, "gwei")} gwei`);
  console.log(`Using gas price: ${ethers.utils.formatUnits(gasPrice, "gwei")} gwei (with 30% buffer)`);

  // Transaction options for Celo Mainnet
  const txOptions = {
    gasLimit: 5000000, // Higher gas limit for mainnet for safety
    gasPrice: gasPrice // Dynamic gas price with buffer
  };

  try {
    // Deploy MemeWarriorsToken
    console.log("\nDeploying MemeWarriorsToken...");
    const MemeWarriorsToken = await ethers.getContractFactory("MemeWarriorsToken");
    const token = await MemeWarriorsToken.deploy(txOptions);
    await token.deployed();
    console.log("MemeWarriorsToken deployed to:", token.address);
    
    // Deploy WarriorFactory
    console.log("\nDeploying WarriorFactory...");
    const WarriorFactory = await ethers.getContractFactory("WarriorFactory");
    const factory = await WarriorFactory.deploy(txOptions);
    await factory.deployed();
    console.log("WarriorFactory deployed to:", factory.address);
    
    // Deploy MemeWarriorsReward
    console.log("\nDeploying MemeWarriorsReward...");
    const MemeWarriorsReward = await ethers.getContractFactory("MemeWarriorsReward");
    const reward = await MemeWarriorsReward.deploy(token.address, txOptions);
    await reward.deployed();
    console.log("MemeWarriorsReward deployed to:", reward.address);
    
    // Set up permissions and initial configurations
    console.log("\nSetting up initial configurations...");
    
    // Approve reward contract to spend tokens for battle rewards
    console.log("Approving tokens for reward contract...");
    const approveTx = await token.approve(
      reward.address, 
      ethers.utils.parseEther("100000"),
      txOptions
    );
    await approveTx.wait();
    console.log("Granted token spending approval to reward contract");

    // Set battlefield wallet in factory
    console.log("Setting battlefield wallet...");
    const setBattlefieldTx = await factory.setBattlefieldWallet(
      deployer.address,
      txOptions
    );
    await setBattlefieldTx.wait();
    console.log("Set battlefield wallet to deployer address");
    
    // Save deployment addresses to a file for reference (separate file for mainnet)
    const fs = require("fs");
    const deployData = {
      token: token.address,
      factory: factory.address,
      reward: reward.address,
      network: "celo_mainnet",
      deployer: deployer.address,
      timestamp: new Date().toISOString()
    };
    
    fs.writeFileSync(
      "celo-mainnet-deployment-addresses.json", 
      JSON.stringify(deployData, null, 2)
    );
    console.log("\nDeployment addresses saved to celo-mainnet-deployment-addresses.json");
    
    console.log("\nDeployment to Celo Mainnet completed successfully!");
    console.log("\nTo verify your contracts on Celo Explorer, run:");
    console.log(`npx hardhat verify --network celo ${token.address}`);
    console.log(`npx hardhat verify --network celo ${factory.address}`);
    console.log(`npx hardhat verify --network celo ${reward.address} "${token.address}"`);
    
    // Alert about verifying after deployment
    console.log("\n⚠️ IMPORTANT: Please verify your contracts on Celo Explorer!");
    console.log("This is essential for transparency and user trust.");
  } catch (error) {
    console.error("Deployment failed:", error);
    console.error("Error details:", error.toString());
    // Print more detailed error info if available
    if (error.error) {
      console.error("Additional error details:", error.error.toString());
    }
    process.exit(1);
  }
}

// Function to require manual confirmation before mainnet deployment
async function manualConfirmation() {
  // This is a safety check for mainnet deployments
  console.log("\n⚠️ WARNING: You are about to deploy to CELO MAINNET! ⚠️");
  console.log("This will use real funds and deploy production contracts.");
  
  // In an actual CLI environment, we'd prompt for confirmation
  // Since we're in a script environment, we'll use a timeout to allow manual cancellation
  console.log("\nWaiting 10 seconds for you to cancel (Ctrl+C) if this is not intended...");
  
  await new Promise(resolve => setTimeout(resolve, 10000));
  console.log("Proceeding with mainnet deployment...");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  }); 