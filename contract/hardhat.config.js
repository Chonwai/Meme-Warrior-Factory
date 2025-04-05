/**
 * @type import('hardhat/config').HardhatUserConfig
 */
require("@nomiclabs/hardhat-waffle");
require("@nomiclabs/hardhat-ethers");
require("dotenv").config();

// Get environment variables (or define defaults)
const PRIVATE_KEY = process.env.PRIVATE_KEY || "0x0000000000000000000000000000000000000000000000000000000000000000";
const ALFAJORES_URL = process.env.ALFAJORES_URL || "https://alfajores-forno.celo-testnet.org";
const CELO_MAINNET_URL = process.env.CELO_MAINNET_URL || "https://forno.celo.org";

module.exports = {
  defaultNetwork: "hardhat",
  networks: {
    hardhat: {
      chainId: 44787 // Celo Alfajores Testnet
    },
    alfajores: {
      url: ALFAJORES_URL,
      accounts: [PRIVATE_KEY],
      chainId: 44787,
      gasPrice: "auto", 
      gasMultiplier: 2,
      gas: 8000000,
      timeout: 300000 // 5 minutes timeout
    },
    celo: {
      url: CELO_MAINNET_URL,
      accounts: [PRIVATE_KEY],
      chainId: 42220,
      gasPrice: "auto",
      gasMultiplier: 2,
      gas: 8000000,
      timeout: 300000 // 5 minutes timeout
    }
  },
  solidity: {
    version: "0.8.17",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      },
      viaIR: true
    }
  },
  resolver: {
    extraImportPaths: ["node_modules"]
  },
  paths: {
    sources: "./contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts"
  },
  mocha: {
    timeout: 120000 // 2 minutes
  }
}; 