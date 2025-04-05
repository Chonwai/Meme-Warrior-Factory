const { ethers } = require("hardhat");
const fs = require("fs");

// Celo Mainnet configuration
const CELO_EXPLORER_URL = 'https://explorer.celo.org';

// Check for full interaction mode:
// 1. Via command line args
// 2. Via script name (if it contains "full")
// 3. Via hardhat args string (if it contains "--full")
// 4. Via FULL_MODE parameter below (set to true for full mode)
const FULL_MODE = false; // Set this to true to force full mode
const scriptArgs = process.argv.slice(2);
const scriptName = process.argv[1] || '';
const FULL_INTERACTION = 
  FULL_MODE ||
  scriptArgs.includes("--full") || 
  scriptName.includes("full") || 
  (process.env.HARDHAT_ARGUMENTS || '').includes("--full");

console.log(FULL_INTERACTION ? "Running in FULL interaction mode" : "Running in CHECK ONLY mode");

// Load deployment addresses
const loadDeploymentAddresses = () => {
  try {
    const data = fs.readFileSync("celo-mainnet-deployment-addresses.json", "utf8");
    return JSON.parse(data);
  } catch (error) {
    console.error("Error loading Celo mainnet deployment addresses:", error);
    process.exit(1);
  }
};

async function main() {
  const deployData = loadDeploymentAddresses();
  console.log("Interacting with contracts on Celo Mainnet");
  
  try {
    // Get signer from hardhat
    const [signer] = await ethers.getSigners();
    console.log("Using account:", signer.address);
    
    // Get current gas price and add buffer
    console.log("Fetching current gas price...");
    const currentGasPrice = await ethers.provider.getGasPrice();
    // Multiply by 1.3 to ensure we're above minimum
    const gasPrice = currentGasPrice.mul(130).div(100);
    console.log(`Current gas price: ${ethers.utils.formatUnits(currentGasPrice, "gwei")} gwei`);
    console.log(`Using gas price: ${ethers.utils.formatUnits(gasPrice, "gwei")} gwei (with 30% buffer)`);
    
    // Transaction options for Celo Mainnet
    const txOptions = {
      gasLimit: 5000000,
      gasPrice: gasPrice
    };
    
    // Get contract instances using hardhat's getContractAt
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
      
      // Get balance of the signer
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
      console.log(`- Warrior Creation Fee: ${ethers.utils.formatEther(creationFee)} CELO`);
      
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
    console.log(`\nView your contracts on Celo Explorer:`);
    console.log(`- Token: ${CELO_EXPLORER_URL}/address/${token.address}`);
    console.log(`- Factory: ${CELO_EXPLORER_URL}/address/${factory.address}`);
    console.log(`- Reward: ${CELO_EXPLORER_URL}/address/${reward.address}`);
    
    // Run the full interaction demo if requested
    if (FULL_INTERACTION) {
      // Ask for confirmation before performing real transactions on mainnet
      await mainnetConfirmation();
      
      console.log("\n=== STARTING FULL INTERACTION DEMO ON MAINNET ===");
      
      // 1. Create a warrior
      console.log("\n1. Creating a meme warrior...");
      const initialSupply = ethers.utils.parseEther("1000");
      const createOptions = {
        ...txOptions,
        value: ethers.utils.parseEther("0.01")
      };
      
      const createTx = await factory.createWarrior(
        "Celo Alpha Warrior",
        "CALPHAW",
        "The premier alpha warrior on Celo",
        "https://example.com/alpha.png",
        initialSupply,
        createOptions
      );
      
      console.log("Waiting for transaction to be mined...");
      const createReceipt = await createTx.wait();
      const event = createReceipt.events.find(e => e.event === "WarriorCreated");
      const warriorId = event.args.warriorId.toNumber();
      const warriorTokenAddress = event.args.tokenAddress;
      
      console.log(`Created warrior with ID: ${warriorId}`);
      console.log(`Warrior token contract: ${warriorTokenAddress}`);
      
      // Get warrior token instance
      const warriorToken = await ethers.getContractAt("WarriorToken", warriorTokenAddress);
      
      // 2. Get warrior details
      console.log("\n2. Getting warrior details...");
      const warrior = await factory.getWarrior(warriorId);
      console.log("Warrior details:");
      console.log(`- Name: ${warrior.name}`);
      console.log(`- Symbol: ${warrior.symbol}`);
      console.log(`- Description: ${warrior.description}`);
      console.log(`- Image URI: ${warrior.imageURI}`);
      console.log(`- Created: ${new Date(warrior.created.toNumber() * 1000).toISOString()}`);
      console.log(`- Creator: ${warrior.creator}`);
      console.log(`- Active: ${warrior.active}`);
      console.log(`- Token address: ${warrior.tokenAddress}`);
      
      // 3. Check warrior token balance
      const warriorTokenBalance = await warriorToken.balanceOf(signer.address);
      console.log(`\n3. Warrior token balance: ${ethers.utils.formatEther(warriorTokenBalance)}`);
      
      console.log("\n=== MAINNET INTERACTION SUMMARY ===");
      console.log(`Created new warrior: ${warrior.name} (ID: ${warriorId})`);
      console.log(`Warrior token address: ${warriorTokenAddress}`);
      console.log(`View on Celo Explorer: ${CELO_EXPLORER_URL}/address/${warriorTokenAddress}`);
    }
  } catch (error) {
    console.error("Error during interaction:", error);
    if (error.reason) console.error("Reason:", error.reason);
  }
}

// Function to require manual confirmation before mainnet transactions
async function mainnetConfirmation() {
  console.log("\n⚠️ WARNING: You are about to perform real transactions on CELO MAINNET! ⚠️");
  console.log("This will use real funds and create actual warriors and battles.");
  
  // In an interactive CLI environment, we'd prompt for confirmation
  console.log("\nWaiting 10 seconds for you to cancel (Ctrl+C) if this is not intended...");
  
  await new Promise(resolve => setTimeout(resolve, 10000));
  console.log("Proceeding with mainnet transactions...");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });