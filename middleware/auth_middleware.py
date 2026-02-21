import jwt
from flask import request, jsonify
from config import SECRET_KEY

def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token missing"}), 401

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = decoded
        except:
            return jsonify({"message": "Invalid or expired token"}), 401

        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper