const { ethers } = require("hardhat");
const fs = require("fs");

// Celo Mainnet configuration
const CELO_EXPLORER_URL = 'https://explorer.celo.org';

// Always use full interaction mode in this script
const FULL_MODE = true; // Forced to true for this script
const FULL_INTERACTION = true;

console.log("Running in FULL interaction mode");

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
    
    // Check contract details first
    console.log("\n=== CHECKING DEPLOYED CONTRACTS ===");
    
    // 1. Token details
    console.log("\n1. Token contract details:");
    try {
      const tokenName = await token.name();
      const tokenSymbol = await token.symbol();
      const tokenTotalSupply = await token.totalSupply();
      
      console.log(`- Name: ${tokenName}`);
      console.log(`- Symbol: ${tokenSymbol}`);
      console.log(`- Total Supply: ${ethers.utils.formatEther(tokenTotalSupply)}`);
      console.log(`- Address: ${token.address}`);
      
      // Get balance of the signer
      const tokenBalance = await token.balanceOf(signer.address);
      console.log(`- Your Balance: ${ethers.utils.formatEther(tokenBalance)}`);
    } catch (err) {
      console.log(`Error fetching token details: ${err.message}`);
    }
    
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