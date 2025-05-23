const { ethers, network } = require("hardhat");

async function main() {
  console.log("Starting deployment...");

  // Get the deployer account
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);
  console.log("Account balance:", (await deployer.getBalance()).toString());
  console.log("Network:", network.name);

  try {
    // Deploy MemeWarriorsToken
    console.log("\nDeploying MemeWarriorsToken...");
    const MemeWarriorsToken = await ethers.getContractFactory("MemeWarriorsToken");
    const token = await MemeWarriorsToken.deploy();
    await token.deployed();
    console.log("MemeWarriorsToken deployed to:", token.address);
    
    // Deploy WarriorFactory
    console.log("\nDeploying WarriorFactory...");
    const WarriorFactory = await ethers.getContractFactory("WarriorFactory");
    const factory = await WarriorFactory.deploy();
    await factory.deployed();
    console.log("WarriorFactory deployed to:", factory.address);
    
    // Deploy MemeWarriorsReward
    console.log("\nDeploying MemeWarriorsReward...");
    const MemeWarriorsReward = await ethers.getContractFactory("MemeWarriorsReward");
    const reward = await MemeWarriorsReward.deploy(token.address);
    await reward.deployed();
    console.log("MemeWarriorsReward deployed to:", reward.address);
    
    // Set up permissions - optional setup step
    console.log("\nSetting up permissions...");
    
    // Approve reward contract to spend tokens for battle rewards
    await token.approve(reward.address, ethers.utils.parseEther("100000"));
    console.log("Granted token spending approval to reward contract");
    
    // Save deployment addresses to a file for reference
    const fs = require("fs");
    const deployData = {
      token: token.address,
      factory: factory.address,
      reward: reward.address,
      network: network.name,
      deployer: deployer.address,
      timestamp: new Date().toISOString()
    };
    
    fs.writeFileSync(
      "deployment-addresses.json", 
      JSON.stringify(deployData, null, 2)
    );
    console.log("\nDeployment addresses saved to deployment-addresses.json");
    
    console.log("\nDeployment completed successfully!");
  } catch (error) {
    console.error("Deployment failed:", error);
    process.exit(1);
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  }); 