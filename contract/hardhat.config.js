/**
 * @type import('hardhat/config').HardhatUserConfig
 */
require("@nomiclabs/hardhat-waffle");
require("@nomiclabs/hardhat-ethers");
require("@nomicfoundation/hardhat-verify");
require("dotenv").config();

// Get environment variables (or define defaults)
const PRIVATE_KEY = process.env.PRIVATE_KEY || "0x0000000000000000000000000000000000000000000000000000000000000000";
const ALFAJORES_URL = process.env.ALFAJORES_URL || "https://alfajores-forno.celo-testnet.org";
const CELO_MAINNET_URL = process.env.CELO_MAINNET_URL || "https://forno.celo.org";
const FLOW_TESTNET_URL = process.env.FLOW_TESTNET_URL || "https://testnet.evm.nodes.onflow.org";

// Flow EVM configuration from official docs
const FLOW_TESTNET_PARAMS = {
  chainId: '0x221', // Hex value of 545
  url: FLOW_TESTNET_URL,
  nativeCurrency: {
    name: 'Flow',
    symbol: 'FLOW',
    decimals: 18,
  },
  blockExplorerUrl: 'https://evm-testnet.flowscan.io/'
};

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
    },
    // Add Flow Testnet EVM configuration using the official params
    flow_testnet: {
      url: FLOW_TESTNET_PARAMS.url,
      accounts: [PRIVATE_KEY],
      chainId: parseInt(FLOW_TESTNET_PARAMS.chainId, 16), // Convert hex chainId to decimal (545)
      gas: 500000,
      gasPrice: "auto",
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
  etherscan: {
    apiKey: {
      // Not required by blockscout, can be any non-empty string
      'flow_testnet': "abc"
    },
    customChains: [
      {
        network: "flow_testnet",
        chainId: parseInt(FLOW_TESTNET_PARAMS.chainId, 16), // Convert hex chainId to decimal (545)
        urls: {
          apiURL: "https://evm-testnet.flowscan.io/api",
          browserURL: FLOW_TESTNET_PARAMS.blockExplorerUrl
        }
      }
    ]
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