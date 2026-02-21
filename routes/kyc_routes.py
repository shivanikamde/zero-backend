from flask import Blueprint, request, jsonify
from blockchain.register_user import register_user
from blockchain.qr_service import generate_qr_payload, validate_qr
from utils.encryption_utils import encrypt_key, decrypt_key
from models.user_model import (
    find_user_by_email,
    update_user_blockchain,
    find_user_by_wallet
)

kyc = Blueprint("kyc", __name__)


# ✅ Register user on blockchain AFTER login
@kyc.route("/register-onchain", methods=["POST"])
def register_onchain():

    data = request.json
    email = data.get("email")
    aadhaar_hash = data.get("aadhaar_hash")

    user = find_user_by_email(email)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Call blockchain registration
    result = register_user(
        aadhaar_hash,
        True,
        True,
        True
    )

    wallet_address = result["wallet_address"]
    private_key = result["private_key"]
    commitment = result["commitment"]

    # 🔐 Encrypt private key before storing
    encrypted_key = encrypt_key(private_key)

    # Save to MongoDB
    update_user_blockchain(
        email,
        wallet_address,
        encrypted_key,
        commitment
    )

    return jsonify({
        "message": "User registered on-chain successfully",
        "wallet_address": wallet_address
    })


# ✅ Generate QR (NO private key from frontend)
@kyc.route("/generate-qr", methods=["POST"])
def generate_qr():

    data = request.json
    wallet_address = data.get("wallet_address")

    user = find_user_by_wallet(wallet_address)
    if not user:
        return jsonify({"error": "User not found"}), 404

    encrypted_key = user.get("encrypted_private_key")

    # 🔓 Decrypt private key internally
    private_key = decrypt_key(encrypted_key)

    qr_data = generate_qr_payload(
        private_key,
        wallet_address
    )

    return jsonify(qr_data)


# ✅ Validate QR
@kyc.route("/validate-qr", methods=["POST"])
def validate():
    result = validate_qr(request.json)
    return jsonify(result)