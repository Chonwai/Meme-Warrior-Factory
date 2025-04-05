const { ethers } = require("hardhat");
const fs = require("fs");

// Load deployment addresses
const loadDeploymentAddresses = () => {
  try {
    const data = fs.readFileSync("deployment-addresses-local.json", "utf8");
    return JSON.parse(data);
  } catch (error) {
    console.error("Error loading local deployment addresses:", error);
    process.exit(1);
  }
};

async function main() {
  const deployData = loadDeploymentAddresses();
  console.log("Interacting with contracts on network:", deployData.network);
  
  // Get signer
  const [signer] = await ethers.getSigners();
  console.log("Using account:", signer.address);
  
  // Get contract instances
  const token = await ethers.getContractAt("MemeWarriorsToken", deployData.token);
  const factory = await ethers.getContractAt("WarriorFactory", deployData.factory);
  const reward = await ethers.getContractAt("MemeWarriorsReward", deployData.reward);
  
  // Display initial balances
  const tokenBalance = await token.balanceOf(signer.address);
  console.log(`MemeWarriors token balance: ${ethers.utils.formatEther(tokenBalance)}`);
  
  try {
    // 1. Create a warrior
    console.log("\n1. Creating a meme warrior...");
    const initialSupply = ethers.utils.parseEther("1000");
    const createTx = await factory.createWarrior(
      "Doge Warrior",
      "DOGEW",
      "The original meme dog warrior",
      "https://example.com/doge.png",
      initialSupply,
      { value: ethers.utils.parseEther("0.01") }
    );
    
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
    console.log(`- Description: ${warrior.description}`);
    console.log(`- Image URI: ${warrior.imageURI}`);
    console.log(`- Created: ${new Date(warrior.created.toNumber() * 1000).toISOString()}`);
    console.log(`- Creator: ${warrior.creator}`);
    console.log(`- Active: ${warrior.active}`);
    console.log(`- Token address: ${warrior.tokenAddress}`);
    
    // 3. Check warrior token balance
    const warriorTokenBalance = await warriorToken.balanceOf(signer.address);
    console.log(`\n3. Warrior token balance: ${ethers.utils.formatEther(warriorTokenBalance)}`);
    
    // 4. Deploy warrior to battle
    console.log("\n4. Deploying warrior to battle...");
    const deployAmount = ethers.utils.parseEther("100");
    
    // First approve tokens for transfer
    await warriorToken.approve(factory.address, deployAmount);
    console.log("Approved tokens for deployment");
    
    // Then deploy to battle
    await factory.deployWarrior(warriorId, deployAmount);
    console.log(`Deployed ${ethers.utils.formatEther(deployAmount)} warrior tokens to battle`);
    
    // 5. Create a battle
    console.log("\n5. Creating a battle...");
    // Create a second warrior for the battle
    const createTx2 = await factory.createWarrior(
      "Pepe Warrior",
      "PEPEW",
      "The famous frog meme warrior",
      "https://example.com/pepe.png",
      initialSupply,
      { value: ethers.utils.parseEther("0.01") }
    );
    
    const createReceipt2 = await createTx2.wait();
    const event2 = createReceipt2.events.find(e => e.event === "WarriorCreated");
    const warriorId2 = event2.args.warriorId.toNumber();
    
    console.log(`Created second warrior with ID: ${warriorId2}`);
    
    // Set up a battle in the reward contract
    const now = Math.floor(Date.now() / 1000);
    const rewardPool = ethers.utils.parseEther("100");
    
    // First approve tokens for the reward pool
    await token.approve(reward.address, rewardPool);
    console.log("Approved tokens for reward pool");
    
    // Then create the battle
    await reward.createBattle(
      warriorId,      // Team 1
      warriorId2,     // Team 2
      now + 10,       // Start in 10 seconds
      60,             // Duration 1 minute
      rewardPool      // 100 tokens as reward
    );
    console.log("Battle created successfully with 100 tokens as reward");
    
    // 6. Vote in the battle
    console.log("\n6. Voting in the battle...");
    // Wait for the battle to start
    console.log("Waiting for battle to start...");
    await new Promise(resolve => setTimeout(resolve, 10000)); // Wait 10 seconds
    
    await reward.voteForTeam(0, warriorId); // Vote for first warrior
    console.log("Voted for warrior in battle");
    
    // 7. End the battle
    console.log("\n7. Ending the battle...");
    // Wait for the battle to end
    console.log("Waiting for battle to end...");
    await new Promise(resolve => setTimeout(resolve, 60000)); // Wait 1 minute
    
    await reward.endBattle(0, warriorId); // First warrior wins
    console.log("Battle ended, warrior won");
    
    // 8. Claim rewards
    console.log("\n8. Claiming rewards...");
    await reward.claimReward(0);
    console.log("Claimed rewards successfully");
    
    const finalTokenBalance = await token.balanceOf(signer.address);
    console.log(`Final token balance: ${ethers.utils.formatEther(finalTokenBalance)}`);
    
    console.log("\nAll interactions completed successfully!");
  } catch (error) {
    console.error("Error during interaction:", error);
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  }); 