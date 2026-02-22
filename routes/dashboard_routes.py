from flask import Blueprint, request, jsonify
from models.user_model import find_user_by_email, update_validator_stats
from config import SECRET_KEY
import jwt

dashboard = Blueprint("dashboard", __name__)

def get_user_from_token(token):
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return find_user_by_email(decoded["email"])


@dashboard.route("/profile", methods=["GET"])
def profile():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"message": "Token missing"}), 401

    try:
        user = get_user_from_token(token)
        user.pop("password", None)
        return jsonify(user)
    except:
        return jsonify({"message": "Invalid token"}), 401


@dashboard.route("/validator/stats", methods=["GET"])
def validator_stats():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"message": "Token missing"}), 401

    try:
        user = get_user_from_token(token)

        if user["role"] != "validator":
            return jsonify({"message": "Access denied"}), 403

        return jsonify({
            "eventsCount": user.get("eventsCount", 0),
            "acceptedCount": user.get("acceptedCount", 0),
            "rejectedCount": user.get("rejectedCount", 0)
        })
    except:
        return jsonify({"message": "Invalid token"}), 401


@dashboard.route("/validator/update", methods=["POST"])
def update_validator():
    token = request.headers.get("Authorization")
    data = request.json

    if not token:
        return jsonify({"message": "Token missing"}), 401

    try:
        user = get_user_from_token(token)

        if user["role"] != "validator":
            return jsonify({"message": "Access denied"}), 403

        action = data.get("action")  # accept / reject / event
        update_validator_stats(user["email"], action)

        return jsonify({"message": "Updated"})
    except:
        return jsonify({"message": "Invalid token"}), 401