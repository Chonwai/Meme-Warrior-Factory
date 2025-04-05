const { ethers, network } = require("hardhat");

async function main() {
  console.log("Starting local deployment...");
  console.log("Network:", network.name);

  // Get the deployer account
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);
  console.log("Account balance:", ethers.utils.formatEther(await deployer.getBalance()));

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
    
    // Set up permissions and initial configurations
    console.log("\nSetting up initial configurations...");
    
    // Approve reward contract to spend tokens for battle rewards
    await token.approve(reward.address, ethers.utils.parseEther("100000"));
    console.log("Granted token spending approval to reward contract");

    // Set battlefield wallet in factory
    await factory.setBattlefieldWallet(deployer.address);
    console.log("Set battlefield wallet to deployer address");
    
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
      "deployment-addresses-local.json", 
      JSON.stringify(deployData, null, 2)
    );
    console.log("\nDeployment addresses saved to deployment-addresses-local.json");
    
    console.log("\nLocal deployment completed successfully!");
    console.log("\nTo test these contracts, run:");
    console.log("  npx hardhat run scripts/interact.js --network localhost");
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