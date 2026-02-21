from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

SEPOLIA_RPC = os.getenv("SEPOLIA_RPC")
w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC))

IDENTITY_REGISTRY = Web3.to_checksum_address(os.getenv("IDENTITY_REGISTRY"))
CREDENTIAL_REGISTRY = Web3.to_checksum_address(os.getenv("CREDENTIAL_REGISTRY"))
REPUTATION_REGISTRY = Web3.to_checksum_address(os.getenv("REPUTATION_REGISTRY"))

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ACCOUNT = w3.eth.account.from_key(PRIVATE_KEY)

# Add ABI here (paste your contract ABI)
IDENTITY_ABI = []
CREDENTIAL_ABI = []
REPUTATION_ABI = []

identity_contract = w3.eth.contract(
    address=IDENTITY_REGISTRY,
    abi=IDENTITY_ABI
)

credential_contract = w3.eth.contract(
    address=CREDENTIAL_REGISTRY,
    abi=CREDENTIAL_ABI
)

reputation_contract = w3.eth.contract(
    address=REPUTATION_REGISTRY,
    abi=REPUTATION_ABI
)