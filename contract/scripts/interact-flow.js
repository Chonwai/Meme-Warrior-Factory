const { ethers } = require("hardhat");
const fs = require("fs");

// Flow EVM configuration
const FLOW_EXPLORER_URL = 'https://evm-testnet.flowscan.io';

// Parse command line arguments
const args = process.argv.slice(2);
const FULL_INTERACTION = args.includes("--full");
console.log(FULL_INTERACTION ? "Running in FULL interaction mode" : "Running in CHECK ONLY mode (use --full for full interaction)");

// Load deployment addresses
const loadDeploymentAddresses = () => {
  try {
    const data = fs.readFileSync("flow-deployment-addresses.json", "utf8");
    return JSON.parse(data);
  } catch (error) {
    console.error("Error loading Flow deployment addresses:", error);
    process.exit(1);
  }
};

async function main() {
  const deployData = loadDeploymentAddresses();
  console.log("Interacting with contracts on Flow EVM network");
  
  try {
    // Get signer from hardhat
    const [signer] = await ethers.getSigners();
    console.log("Using account:", signer.address);
    
    // Get contract instances using hardhat's getContractAt
    // This is much more reliable than trying to import artifacts directly
    const token = await ethers.getContractAt("MemeWarriorsToken", deployData.token);
    const factory = await ethers.getContractAt("WarriorFactory", deployData.factory);
    const reward = await ethers.getContractAt("MemeWarriorsReward", deployData.reward);
    
    // Simple check mode
    console.log("\n=== CHECKING DEPLOYED CONTRACTS ===");
    
    // 1. Check token details
    console.log("\n1. Token contract details:");
    try {
      const tokenName = await token.name();
      const tokenSymbol = await token.symbol();
      const tokenDecimals = await token.decimals();
      const tokenTotalSupply = await token.totalSupply();
      
      console.log(`- Name: ${tokenName}`);
      console.log(`- Symbol: ${tokenSymbol}`);
      console.log(`- Decimals: ${tokenDecimals}`);
      console.log(`- Total Supply: ${ethers.utils.formatEther(tokenTotalSupply)}`);
      
      // Get balance of the wallet
      const tokenBalance = await token.balanceOf(signer.address);
      console.log(`- Your Balance: ${ethers.utils.formatEther(tokenBalance)}`);
    } catch (err) {
      console.log(`Error fetching token details: ${err.message}`);
    }
    
    // 2. Check factory details
    console.log("\n2. Factory contract details:");
    try {
      const warriorCount = await factory.getWarriorCount();
      console.log(`- Total Warriors Created: ${warriorCount}`);
      
      const creationFee = await factory.getCreationFee();
      console.log(`- Warrior Creation Fee: ${ethers.utils.formatEther(creationFee)} FLOW`);
      
      const battlefieldWallet = await factory.battlefieldWallet();
      console.log(`- Battlefield Wallet: ${battlefieldWallet}`);
      
      // If warriors exist, display them
      if (warriorCount.toNumber() > 0) {
        console.log("\n3. Warriors created so far:");
        
        // Loop through available warriors
        for (let i = 0; i < Math.min(5, warriorCount.toNumber()); i++) {
          try {
            const warrior = await factory.getWarrior(i);
            console.log(`\nWarrior #${i}:`);
            console.log(`- Name: ${warrior.name}`);
            console.log(`- Symbol: ${warrior.symbol}`);
            console.log(`- Description: ${warrior.description}`);
            console.log(`- Token Address: ${warrior.tokenAddress}`);
            console.log(`- Creator: ${warrior.creator}`);
            console.log(`- Active: ${warrior.active}`);
          } catch (err) {
            console.log(`Error fetching warrior #${i}: ${err.message}`);
          }
        }
        
        if (warriorCount.toNumber() > 5) {
          console.log(`\n...and ${warriorCount.toNumber() - 5} more warriors`);
        }
      }
    } catch (err) {
      console.log(`Error fetching factory details: ${err.message}`);
    }
    
    // 3. Check reward contract details
    console.log("\n3. Reward contract details:");
    try {
      const battleCount = await reward.getBattleCount();
      console.log(`- Total Battles Created: ${battleCount}`);
      
      // If battles exist, display them
      if (battleCount.toNumber() > 0) {
        console.log("\n4. Battles created so far:");
        
        // Loop through available battles
        for (let i = 0; i < Math.min(5, battleCount.toNumber()); i++) {
          try {
            const battle = await reward.getBattle(i);
            console.log(`\nBattle #${i}:`);
            console.log(`- Team 1 ID: ${battle.team1Id}`);
            console.log(`- Team 2 ID: ${battle.team2Id}`);
            console.log(`- Start Time: ${new Date(battle.startTime.toNumber() * 1000).toISOString()}`);
            console.log(`- End Time: ${new Date((battle.startTime.toNumber() + battle.duration) * 1000).toISOString()}`);
            console.log(`- Duration: ${battle.duration} seconds`);
            console.log(`- Reward Pool: ${ethers.utils.formatEther(battle.rewardPool)}`);
            console.log(`- Winner ID: ${battle.winnerId}`);
            console.log(`- Ended: ${battle.ended}`);
          } catch (err) {
            console.log(`Error fetching battle #${i}: ${err.message}`);
          }
        }
        
        if (battleCount.toNumber() > 5) {
          console.log(`\n...and ${battleCount.toNumber() - 5} more battles`);
        }
      }
    } catch (err) {
      console.log(`Error fetching reward details: ${err.message}`);
    }
    
    console.log("\n=== CONTRACT CHECK COMPLETE ===");
    console.log(`\nView your contracts on FlowScan:`);
    console.log(`- Token: ${FLOW_EXPLORER_URL}/address/${token.address}`);
    console.log(`- Factory: ${FLOW_EXPLORER_URL}/address/${factory.address}`);
    console.log(`- Reward: ${FLOW_EXPLORER_URL}/address/${reward.address}`);
    
  } catch (error) {
    console.error("Error during interaction:", error);
    if (error.reason) console.error("Reason:", error.reason);
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  }); 