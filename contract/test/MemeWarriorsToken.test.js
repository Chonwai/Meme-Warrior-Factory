const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("MemeWarriorsToken", function () {
  let MemeWarriorsToken;
  let token;
  let owner;
  let addr1;
  let addr2;
  let addrs;

  beforeEach(async function () {
    // Get contract factories
    MemeWarriorsToken = await ethers.getContractFactory("MemeWarriorsToken");
    
    // Get signers
    [owner, addr1, addr2, ...addrs] = await ethers.getSigners();

    // Deploy token
    token = await MemeWarriorsToken.deploy();
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
  });

  describe("Transactions", function () {
    it("Should transfer tokens between accounts", async function () {
      // Transfer 50 tokens from owner to addr1
      await token.transfer(addr1.address, 50);
      const addr1Balance = await token.balanceOf(addr1.address);
      expect(addr1Balance).to.equal(50);

      // Transfer 50 tokens from addr1 to addr2
      await token.connect(addr1).transfer(addr2.address, 50);
      const addr2Balance = await token.balanceOf(addr2.address);
      expect(addr2Balance).to.equal(50);
    });

    it("Should fail if sender doesn't have enough tokens", async function () {
      const initialOwnerBalance = await token.balanceOf(owner.address);

      // Try to send 1 token from addr1 (0 tokens) to owner
      await expect(
        token.connect(addr1).transfer(owner.address, 1)
      ).to.be.revertedWith("ERC20: transfer amount exceeds balance");

      // Owner balance shouldn't have changed
      expect(await token.balanceOf(owner.address)).to.equal(initialOwnerBalance);
    });
  });

  describe("Minting", function () {
    it("Should allow the owner to mint tokens", async function () {
      const initialSupply = await token.totalSupply();
      
      // Mint 1000 tokens to addr1
      await token.mint(addr1.address, 1000);
      
      // Check addr1 balance
      expect(await token.balanceOf(addr1.address)).to.equal(1000);
      
      // Check total supply was increased
      expect(await token.totalSupply()).to.equal(initialSupply.add(1000));
    });

    it("Should not allow non-owners to mint tokens", async function () {
      // Try to mint from non-owner account
      await expect(
        token.connect(addr1).mint(addr2.address, 1000)
      ).to.be.revertedWith("Ownable: caller is not the owner");
    });
  });

  describe("Burning", function () {
    it("Should allow token holders to burn their tokens", async function () {
      // First transfer tokens to addr1
      await token.transfer(addr1.address, 1000);
      
      // Burn 500 tokens from addr1
      await token.connect(addr1).burn(500);
      
      // Check addr1 balance
      expect(await token.balanceOf(addr1.address)).to.equal(500);
    });
  });
}); 