const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("WarriorToken", function () {
  let WarriorToken;
  let token;
  let owner;
  let controller;
  let addr1;
  let addr2;

  beforeEach(async function () {
    // Get contract factory
    WarriorToken = await ethers.getContractFactory("WarriorToken");
    
    // Get signers
    [owner, controller, addr1, addr2] = await ethers.getSigners();

    // Deploy token
    token = await WarriorToken.deploy("TestWarrior", "TW", owner.address, 1000);
    await token.deployed();
  });

  describe("Deployment", function () {
    it("Should set the right owner", async function () {
      expect(await token.owner()).to.equal(owner.address);
    });

    it("Should assign the total supply of tokens to the owner", async function () {
      const ownerBalance = await token.balanceOf(owner.address);
      expect(await token.totalSupply()).to.equal(ownerBalance);
    });

    it("Should have the correct name and symbol", async function () {
      expect(await token.name()).to.equal("TestWarrior");
      expect(await token.symbol()).to.equal("TW");
    });
  });

  describe("Transactions", function () {
    it("Should transfer tokens between accounts", async function () {
      // Transfer 100 tokens from owner to addr1
      await token.transfer(addr1.address, 100);
      expect(await token.balanceOf(addr1.address)).to.equal(100);

      // Transfer 50 tokens from addr1 to addr2
      await token.connect(addr1).transfer(addr2.address, 50);
      expect(await token.balanceOf(addr2.address)).to.equal(50);
      expect(await token.balanceOf(addr1.address)).to.equal(50);
    });

    it("Should fail if sender doesn't have enough tokens", async function () {
      await expect(
        token.connect(addr1).transfer(owner.address, 1)
      ).to.be.revertedWith("ERC20: transfer amount exceeds balance");
    });
  });

  describe("Controller functionality", function () {
    it("Should allow the owner to set controllers", async function () {
      // Set controller
      await token.setController(controller.address, true);
      expect(await token.isController(controller.address)).to.equal(true);
      
      // Remove controller
      await token.setController(controller.address, false);
      expect(await token.isController(controller.address)).to.equal(false);
    });

    it("Should not allow non-owners to set controllers", async function () {
      await expect(
        token.connect(addr1).setController(addr2.address, true)
      ).to.be.revertedWith("Ownable: caller is not the owner");
    });

    it("Should allow controllers to burn tokens from other accounts", async function () {
      // Transfer tokens to addr1
      await token.transfer(addr1.address, 200);
      
      // Set controller
      await token.setController(controller.address, true);
      
      // Approve controller to spend tokens
      await token.connect(addr1).approve(controller.address, 100);
      
      // Burn tokens from addr1 by controller
      await token.connect(controller).burnFrom(addr1.address, 100);
      
      // Check balance
      expect(await token.balanceOf(addr1.address)).to.equal(100);
    });

    it("Should not allow non-controllers to burn tokens from other accounts", async function () {
      // Transfer tokens to addr1
      await token.transfer(addr1.address, 200);
      
      // Approve addr2 to spend tokens
      await token.connect(addr1).approve(addr2.address, 100);
      
      // Try to burn tokens from addr1 by addr2 (non-controller)
      await expect(
        token.connect(addr2).burnFrom(addr1.address, 100)
      ).to.be.revertedWith("Caller is not a controller");
    });
  });

  describe("Minting", function () {
    it("Should allow the owner to mint new tokens", async function () {
      const initialSupply = await token.totalSupply();
      
      // Mint new tokens
      await token.mint(addr1.address, 500);
      
      // Check balances
      expect(await token.balanceOf(addr1.address)).to.equal(500);
      expect(await token.totalSupply()).to.equal(initialSupply.add(500));
    });

    it("Should not allow non-owners to mint tokens", async function () {
      await expect(
        token.connect(addr1).mint(addr2.address, 500)
      ).to.be.revertedWith("Ownable: caller is not the owner");
    });
  });
}); 