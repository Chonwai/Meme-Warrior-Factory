from web3 import Web3
from app.config.settings import settings
import json
import os

# Initialize Web3 with Celo mainnet provider (for rewards)
mainnet_web3 = Web3(Web3.HTTPProvider(settings.CELO_MAINNET_RPC_URL))

# Initialize Web3 with testnet provider (for meme soldiers)
testnet_web3 = Web3(Web3.HTTPProvider(settings.CELO_TESTNET_RPC_URL))

# Path to ABI files
ABI_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "abis")

def get_contract_abi(contract_name):
    """Load contract ABI from file"""
    try:
        abi_path = os.path.join(ABI_DIR, f"{contract_name}.json")
        with open(abi_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise Exception(f"ABI file for {contract_name} not found")

def get_mainnet_contract(address, contract_name):
    """Get contract instance on Celo mainnet"""
    abi = get_contract_abi(contract_name)
    return mainnet_web3.eth.contract(address=address, abi=abi)

def get_testnet_contract(address, contract_name):
    """Get contract instance on testnet"""
    abi = get_contract_abi(contract_name)
    return testnet_web3.eth.contract(address=address, abi=abi)

def verify_wallet_balance(wallet_address, network="testnet"):
    """Verify if wallet has enough balance for gas fees"""
    web3_instance = testnet_web3 if network == "testnet" else mainnet_web3
    balance = web3_instance.eth.get_balance(wallet_address)
    return balance > 0  # Just checking if there's any balance, adjust as needed

def deploy_soldier_to_battlefield(wallet_address, token_id, amount_to_deploy):
    """Deploy a meme soldier to the battlefield (on testnet)"""
    # This is a placeholder - actual implementation would call the contract method
    # to transfer tokens to the battlefield contract
    try:
        contract = get_testnet_contract(settings.SOLDIER_CONTRACT_ADDRESS, "MemeSoldier")
        # Example transaction (implementation will depend on your contract)
        # txn = contract.functions.deployToBattlefield(token_id, amount_to_deploy).build_transaction({
        #    'from': wallet_address,
        #    'gas': settings.GAS_LIMIT,
        #    'nonce': testnet_web3.eth.get_transaction_count(wallet_address),
        # })
        # Return transaction hash or other relevant info
        return {
            "success": True,
            "transaction_hash": "0x0000000000000000000000000000000000000000",  # Placeholder
            "amount_deployed": amount_to_deploy
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def distribute_rewards(winner_voter_addresses, battle_id):
    """Distribute reward tokens to voters who voted for the winning soldier (on mainnet)"""
    try:
        contract = get_mainnet_contract(settings.REWARD_CONTRACT_ADDRESS, "RewardToken")
        
        # Example batch distribution of rewards
        # txn = contract.functions.batchDistributeRewards(winner_voter_addresses, battle_id).build_transaction({
        #    'from': settings.REWARD_DISTRIBUTOR_ADDRESS,
        #    'gas': settings.GAS_LIMIT,
        #    'nonce': mainnet_web3.eth.get_transaction_count(settings.REWARD_DISTRIBUTOR_ADDRESS),
        # })
        
        return {
            "success": True,
            "transaction_hash": "0x0000000000000000000000000000000000000000",  # Placeholder
            "recipients_count": len(winner_voter_addresses)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def get_token_metadata(token_id):
    """Get metadata for a meme soldier token from the blockchain (testnet)"""
    try:
        contract = get_testnet_contract(settings.SOLDIER_CONTRACT_ADDRESS, "MemeSoldier")
        # Example call to get token metadata
        # metadata = contract.functions.tokenURI(token_id).call()
        # This is a placeholder - replace with actual contract method call
        return {
            "token_id": token_id,
            "name": f"Meme Soldier #{token_id}",
            "image_url": "https://example.com/image.png",
            "coin_icon_url": "https://example.com/coin_icon.png",
            "attributes": {}
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        } 