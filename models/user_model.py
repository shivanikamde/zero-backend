from config import db

users_collection = db["users"]

def create_user(user_data):
    return users_collection.insert_one(user_data)

def find_user_by_email(email):
    return users_collection.find_one({"email": email})

def update_user_kyc(email):
    return users_collection.update_one(
        {"email": email},
        {"$set": {"isKYCVerified": True}}
    )