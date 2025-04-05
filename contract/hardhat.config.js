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
      gasPrice: 2000000000
    },
    celo: {
      url: CELO_MAINNET_URL,
      accounts: [PRIVATE_KEY],
      chainId: 42220,
      gasPrice: 2000000000
    }
  },
  solidity: {
    version: "0.8.17",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  paths: {
    sources: "./",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts"
  },
  mocha: {
    timeout: 40000
  }
}; 