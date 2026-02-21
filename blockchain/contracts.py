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
IDENTITY_ABI = [
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}, {"internalType": "bytes32", "name": "commitmentHash", "type": "bytes32"}, {"internalType": "uint256", "name": "expiresAt", "type": "uint256"}],
        "name": "registerIdentity", "outputs": [], "stateMutability": "nonpayable", "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "markKYCVerified", "outputs": [], "stateMutability": "nonpayable", "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "markPhoneVerified", "outputs": [], "stateMutability": "nonpayable", "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "markFaceEnrolled", "outputs": [], "stateMutability": "nonpayable", "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}, {"internalType": "string", "name": "reason", "type": "string"}],
        "name": "blacklistUser", "outputs": [], "stateMutability": "nonpayable", "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "reinstateUser", "outputs": [], "stateMutability": "nonpayable", "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "issuer", "type": "address"}],
        "name": "addIssuer", "outputs": [], "stateMutability": "nonpayable", "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "isVerified",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view", "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "isBlacklisted",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view", "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "identityExists",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view", "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "getIdentityStatus",
        "outputs": [
            {"internalType": "bool", "name": "kycVerified", "type": "bool"},
            {"internalType": "bool", "name": "phoneVerified", "type": "bool"},
            {"internalType": "bool", "name": "faceEnrolled", "type": "bool"},
            {"internalType": "bool", "name": "blacklisted", "type": "bool"},
            {"internalType": "string", "name": "blacklistReason", "type": "string"},
            {"internalType": "uint256", "name": "createdAt", "type": "uint256"},
            {"internalType": "uint256", "name": "expiresAt", "type": "uint256"},
            {"internalType": "bool", "name": "active", "type": "bool"}
        ],
        "stateMutability": "view", "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "user", "type": "address"},
            {"indexed": False, "internalType": "bytes32", "name": "commitmentHash", "type": "bytes32"},
            {"indexed": False, "internalType": "uint256", "name": "expiresAt", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}
        ],
        "name": "IdentityRegistered", "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [{"indexed": True, "internalType": "address", "name": "user", "type": "address"}, {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}],
        "name": "KYCVerified", "type": "event"
    },
]
CREDENTIAL_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "user", "type": "address"},
            {"internalType": "bytes32", "name": "credType", "type": "bytes32"},
            {"internalType": "bytes32", "name": "proofHash", "type": "bytes32"},
            {"internalType": "uint256", "name": "expiresAt", "type": "uint256"}
        ],
        "name": "issueCredential", "outputs": [], "stateMutability": "nonpayable", "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "user", "type": "address"},
            {"internalType": "bytes32", "name": "credType", "type": "bytes32"},
            {"internalType": "string", "name": "reason", "type": "string"}
        ],
        "name": "revokeCredential", "outputs": [], "stateMutability": "nonpayable", "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "user", "type": "address"},
            {"internalType": "bytes32", "name": "credType", "type": "bytes32"}
        ],
        "name": "isCredentialValid",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view", "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "user", "type": "address"},
            {"internalType": "bytes32", "name": "credType", "type": "bytes32"}
        ],
        "name": "hasCredential",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view", "type": "function"
    },
    {
        "inputs": [],
        "name": "KYC_VERIFIED",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view", "type": "function"
    },
    {
        "inputs": [],
        "name": "AGE_18",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view", "type": "function"
    },
    {
        "inputs": [],
        "name": "PHONE_VERIFIED",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view", "type": "function"
    },
    {
        "inputs": [],
        "name": "FACE_ENROLLED",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view", "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "user", "type": "address"},
            {"indexed": True, "internalType": "bytes32", "name": "credType", "type": "bytes32"},
            {"indexed": False, "internalType": "uint256", "name": "expiresAt", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}
        ],
        "name": "CredentialIssued", "type": "event"
    },
]

REPUTATION_ABI =  [
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "recordEventAttendance", "outputs": [], "stateMutability": "nonpayable", "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "recordPlatformVerification", "outputs": [], "stateMutability": "nonpayable", "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "recordSuccessfulTransaction", "outputs": [], "stateMutability": "nonpayable", "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "getTotalScore",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view", "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "isInitialized",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view", "type": "function"
    },
]

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