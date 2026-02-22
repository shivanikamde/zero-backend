# from flask import Blueprint, request, jsonify
# from models.user_model import create_user, find_user_by_email
# from utils.hash_utils import hash_password, check_password
# from config import SECRET_KEY
# import jwt
# import datetime

# auth = Blueprint("auth", __name__)

# @auth.route("/signup", methods=["POST"])
# def signup():
#     data = request.json

#     username = data.get("username")
#     email = data.get("email")
#     pwd = data.get("pwd")
#     confirmPwd = data.get("confirmpwd")

#     if pwd != confirmPwd:
#         return jsonify({"message": "Passwords do not match"}), 400

#     if find_user_by_email(email):
#         return jsonify({"message": "User already exists"}), 400

#     hashed_pw = hash_password(pwd)

#     user = {
#         "username": username,
#         "email": email,
#         "password": hashed_pw,
#         "isKYCVerified": False
#     }

#     create_user(user)

#     return jsonify({"message": "Signup successful"}), 201


# @auth.route("/login", methods=["POST"])
# def login():
#     data = request.json

#     email = data.get("email")
#     pwd = data.get("pwd")

#     user = find_user_by_email(email)

#     if not user:
#         return jsonify({"message": "User not found"}), 404

#     if not check_password(user["password"], pwd):
#         return jsonify({"message": "Invalid credentials"}), 401

#     token = jwt.encode({
#         "email": email,
#         "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
#     }, SECRET_KEY, algorithm="HS256")

#     return jsonify({
#         "message": "Login successful",
#         "token": token
#     })  

#version 2
from flask import Blueprint, request, jsonify
from models.user_model import create_user, find_user_by_email
from utils.hash_utils import hash_password, check_password
from config import SECRET_KEY
import jwt
import datetime
import hashlib
import qrcode
import base64
from io import BytesIO

auth = Blueprint("auth", __name__)

# ───────────────── SIGNUP ─────────────────
@auth.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    role = data.get("role", "user")
    email = data.get("email")
    username = data.get("username")
    pwd = data.get("password")   # ✅ FIXED (was pwd)

    # ✅ Validate required fields
    if not email or not username or not pwd:
        return jsonify({"error": "Email, username and password are required"}), 400

    # ✅ Check if already exists
    if find_user_by_email(email):
        return jsonify({"message": "Account already exists"}), 400

    user = {
        "email": email,
        "username": username,
        "password": hash_password(pwd),
        "role": role,
        "createdAt": datetime.datetime.utcnow()
    }

    # ───────── USER EXTRA DATA ─────────
    if role == "user":
        # Generate hash automatically
        unique_string = email + str(datetime.datetime.utcnow())
        generated_hash = hashlib.sha256(unique_string.encode()).hexdigest()

        # Generate QR code
        qr = qrcode.make(generated_hash)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()

        user.update({
            "hash": generated_hash,
            "qrCodeImage": qr_base64,
            "reputationScore": 0
        })

    # ───────── VALIDATOR EXTRA DATA ─────────
    if role == "validator":
        user.update({
            "eventsCount": 0,
            "acceptedCount": 0,
            "rejectedCount": 0
        })

    create_user(user)

    return jsonify({"message": f"{role} signup successful"}), 201


# ───────────────── LOGIN ─────────────────
@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    email = data.get("email")
    pwd = data.get("password")   # ✅ FIXED (was pwd)

    if not email or not pwd:
        return jsonify({"error": "Email and password required"}), 400

    user = find_user_by_email(email)

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not check_password(user["password"], pwd):
        return jsonify({"message": "Invalid credentials"}), 401

    token = jwt.encode({
        "email": user["email"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "token": token,
        "role": user["role"]
    })