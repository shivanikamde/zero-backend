from flask import Blueprint, jsonify, request
from middleware.auth_middleware import token_required
from models.user_model import update_user_kyc

kyc = Blueprint("kyc", __name__)

@kyc.route("/validate-aadhar", methods=["POST"])
@token_required
def validate_aadhar():
    user_email = request.user["email"]

    # Here you would normally verify Aadhaar via API
    # For now we simulate verification

    update_user_kyc(user_email)

    return jsonify({"message": "Aadhaar validated successfully"})