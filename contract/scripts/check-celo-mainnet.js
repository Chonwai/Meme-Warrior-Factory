const { ethers } = require("hardhat");
const fs = require("fs");

// Celo Mainnet configuration
const CELO_EXPLORER_URL = 'https://explorer.celo.org';

// Utility to find deployment addresses
const findDeploymentAddresses = () => {
  try {
    // Try to read from celo-mainnet-deployment-addresses.json
    const data = fs.readFileSync("celo-mainnet-deployment-addresses.json", "utf8");
    return JSON.parse(data);
  } catch (error) {
    console.error("Couldn't find celo-mainnet-deployment-addresses.json");
    console.log("Checking for recent deployment...");
    
    // Try to guess the latest deployment from deployment logs or console output
    try {
      const files = fs.readdirSync(".");
      const deploymentFiles = files.filter(f => f.startsWith("celo-mainnet-deployment-") && f.endsWith(".log"));
      
      if (deploymentFiles.length > 0) {
        // Sort by creation time, get the newest
        const latestFile = deploymentFiles.sort((a, b) => {
          return fs.statSync(b).mtime.getTime() - fs.statSync(a).mtime.getTime();
        })[0];
        
        console.log(`Found deployment log: ${latestFile}`);
        
        // Try to parse addresses from the deployment log
        const content = fs.readFileSync(latestFile, "utf8");
        
        // Extract contract addresses with simple regex
        const tokenMatch = content.match(/Token deployed to: (0x[a-fA-F0-9]{40})/);
        const factoryMatch = content.match(/Factory deployed to: (0x[a-fA-F0-9]{40})/);
        const rewardMatch = content.match(/Reward deployed to: (0x[a-fA-F0-9]{40})/);
        
        if (tokenMatch && factoryMatch && rewardMatch) {
          return {
            token: tokenMatch[1],
            factory: factoryMatch[1],
            reward: rewardMatch[1],
            network: "celo_mainnet"
          };
        }
      }
      
      console.error("Couldn't find deployment addresses.");
      process.exit(1);
    } catch (err) {
      console.error("Error while looking for deployment:", err);
      process.exit(1);
    }
  }
};

async function main() {
  // Start with basic checking
  console.log("Checking Celo Mainnet deployment status...");
  
  // Get contract addresses
  const deployData = findDeploymentAddresses();
  console.log("\nFound deployed contracts:");
  console.log(`- Token: ${deployData.token}`);
  console.log(`- Factory: ${deployData.factory}`);
  console.log(`- Reward: ${deployData.reward}`);
  
  // Get the current account
  const [signer] = await ethers.getSigners();
  console.log(`\nUsing account: ${signer.address}`);
  
  // Check if contract code exists at each address
  const provider = ethers.provider;
  
  console.log("\nVerifying contracts exist on-chain...");
  
  // Check token
  let code = await provider.getCode(deployData.token);
  if (code !== "0x") {
    console.log("✅ Token contract code exists");
    
    try {
      // Try to load the contract
      const token = await ethers.getContractAt("MemeWarriorsToken", deployData.token);
      const name = await token.name();
      const symbol = await token.symbol();
      const totalSupply = await token.totalSupply();
      
      console.log(`   Name: ${name}`);
      console.log(`   Symbol: ${symbol}`);
      console.log(`   Total Supply: ${ethers.utils.formatEther(totalSupply)}`);
      
      // Get our balance
      const balance = await token.balanceOf(signer.address);
      console.log(`   Your Balance: ${ethers.utils.formatEther(balance)}`);
    } catch (err) {
      console.log("❌ Error reading token contract:", err.message);
    }
  } else {
    console.log("❌ No code found at token address");
  }
  
  // Check factory
  code = await provider.getCode(deployData.factory);
  if (code !== "0x") {
    console.log("✅ Factory contract code exists");
    
    try {
      // Try to load the contract
      const factory = await ethers.getContractAt("WarriorFactory", deployData.factory);
      const owner = await factory.owner();
      const count = await factory.getWarriorCount();
      
      console.log(`   Owner: ${owner}`);
      console.log(`   Warrior Count: ${count}`);
    } catch (err) {
      console.log("❌ Error reading factory contract:", err.message);
    }
  } else {
    console.log("❌ No code found at factory address");
  }
  
  // Check reward
  code = await provider.getCode(deployData.reward);
  if (code !== "0x") {
    console.log("✅ Reward contract code exists");
    
    try {
      // Try to load the contract
      const reward = await ethers.getContractAt("MemeWarriorsReward", deployData.reward);
      const tokenAddress = await reward.tokenAddress();
      const battleCount = await reward.getBattleCount();
      
      console.log(`   Token Address: ${tokenAddress}`);
      console.log(`   Battle Count: ${battleCount}`);
    } catch (err) {
      console.log("❌ Error reading reward contract:", err.message);
    }
  } else {
    console.log("❌ No code found at reward address");
  }
  
  console.log("\nDeployment check complete.");
  console.log(`\nView your contracts on Celo Explorer:`);
  console.log(`- Token: ${CELO_EXPLORER_URL}/address/${deployData.token}`);
  console.log(`- Factory: ${CELO_EXPLORER_URL}/address/${deployData.factory}`);
  console.log(`- Reward: ${CELO_EXPLORER_URL}/address/${deployData.reward}`);
}

// Run the async function
main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  }); 