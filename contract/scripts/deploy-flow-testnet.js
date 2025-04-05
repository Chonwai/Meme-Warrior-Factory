const { ethers, network } = require("hardhat");

async function main() {
  console.log("Starting deployment to Flow EVM...");
  console.log("Network:", network.name);

  // Get the deployer account
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);
  console.log("Account balance:", ethers.utils.formatEther(await deployer.getBalance()));

  // Transaction options to use consistently - helps prevent negative gas price issues
  const txOptions = {
    gasLimit: 3000000,
    gasPrice: ethers.utils.parseUnits("10", "gwei") // Use a fixed gas price
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
    
    // Approve reward contract to spend tokens for battle rewards - Use explicit transaction options
    console.log("Approving tokens for reward contract...");
    const approveTx = await token.approve(
      reward.address, 
      ethers.utils.parseEther("100000"),
      txOptions
    );
    await approveTx.wait();
    console.log("Granted token spending approval to reward contract");

    // Set battlefield wallet in factory - Use explicit transaction options
    console.log("Setting battlefield wallet...");
    const setBattlefieldTx = await factory.setBattlefieldWallet(
      deployer.address,
      txOptions
    );
    await setBattlefieldTx.wait();
    console.log("Set battlefield wallet to deployer address");
    
    // Save deployment addresses to a file for reference
    const fs = require("fs");
    const deployData = {
      token: token.address,
      factory: factory.address,
      reward: reward.address,
      network: "flow_testnet",
      deployer: deployer.address,
      timestamp: new Date().toISOString()
    };
    
    fs.writeFileSync(
      "flow-deployment-addresses.json", 
      JSON.stringify(deployData, null, 2)
    );
    console.log("\nDeployment addresses saved to flow-deployment-addresses.json");
    
    console.log("\nDeployment to Flow EVM completed successfully!");
    console.log("\nTo verify your contracts on FlowScan, run:");
    console.log(`npx hardhat verify --network flow_testnet ${token.address}`);
    console.log(`npx hardhat verify --network flow_testnet ${factory.address}`);
    console.log(`npx hardhat verify --network flow_testnet ${reward.address} "${token.address}"`);
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

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });