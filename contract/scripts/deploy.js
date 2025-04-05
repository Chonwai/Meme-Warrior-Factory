const { ethers } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);
  console.log("Account balance:", (await deployer.getBalance()).toString());
  console.log("Deploying MemeWarriors contracts to", network.name);

  // Get the Contract Factories
  const MemeWarriorsToken = await ethers.getContractFactory("MemeWarriorsToken");
  const WarriorFactory = await ethers.getContractFactory("WarriorFactory");
  
  // Deploy MemeWarriorsToken
  console.log("Deploying MemeWarriorsToken...");
  const memeWarriorsToken = await MemeWarriorsToken.deploy();
  await memeWarriorsToken.deployed();
  console.log("MemeWarriorsToken deployed to:", memeWarriorsToken.address);

  // Deploy WarriorFactory
  console.log("Deploying WarriorFactory...");
  const warriorFactory = await WarriorFactory.deploy();
  await warriorFactory.deployed();
  console.log("WarriorFactory deployed to:", warriorFactory.address);

  // Deploy MemeWarriorsReward with the MemeWarriorsToken address
  console.log("Deploying MemeWarriorsReward...");
  const MemeWarriorsReward = await ethers.getContractFactory("MemeWarriorsReward");
  const memeWarriorsReward = await MemeWarriorsReward.deploy(memeWarriorsToken.address);
  await memeWarriorsReward.deployed();
  console.log("MemeWarriorsReward deployed to:", memeWarriorsReward.address);

  // Set the battlefield wallet in WarriorFactory to the deployer for now
  console.log("Setting up battlefield wallet...");
  await warriorFactory.setBattlefieldWallet(deployer.address);
  console.log("Battlefield wallet set to:", deployer.address);

  console.log("All contracts successfully deployed!");
  console.log({
    MemeWarriorsToken: memeWarriorsToken.address,
    WarriorFactory: warriorFactory.address,
    MemeWarriorsReward: memeWarriorsReward.address
  });
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  }); 