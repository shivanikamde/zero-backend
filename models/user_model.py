from config import db
from datetime import datetime

users_collection = db["users"]


# ✅ Create user with default blockchain fields
def create_user(user_data):

    user_data.update({
        "wallet_address": None,
        "encrypted_private_key": None,
        "commitment_hash": None,
        "isKYCVerified": False,
        "created_at": datetime.utcnow()
    })

    return users_collection.insert_one(user_data)


# ✅ Find user by email
def find_user_by_email(email):
    return users_collection.find_one({"email": email})


# ✅ Update KYC verification status
def update_user_kyc(email):
    return users_collection.update_one(
        {"email": email},
        {"$set": {"isKYCVerified": True}}
    )


# ✅ Save blockchain details after on-chain registration
def update_user_blockchain(email, wallet_address, encrypted_private_key, commitment_hash):
    return users_collection.update_one(
        {"email": email},
        {
            "$set": {
                "wallet_address": wallet_address,
                "encrypted_private_key": encrypted_private_key,
                "commitment_hash": commitment_hash,
                "isKYCVerified": True
            }
        }
    )


# ✅ Find user by wallet address (for QR validation use)
def find_user_by_wallet(wallet_address):
    return users_collection.find_one({"wallet_address": wallet_address})