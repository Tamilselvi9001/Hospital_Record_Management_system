import os
import datetime
import jwt
import bcrypt
from functools import wraps
from flask import request, jsonify
from .db import db

JWT_SECRET = os.getenv("JWT_SECRET", "medivault_super_secret_jwt_key_2026")
JWT_ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def generate_token(user: dict) -> str:
    payload = {
        "user_id": str(user.get("_id")),
        "email": user.get("email"),
        "role": user.get("role", "patient"),
        "name": user.get("name"),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        token = None
        if auth_header:
            parts = auth_header.split(" ")
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]
            else:
                token = auth_header
        
        if not token:
            # Check query param as fallback for downloads/previews
            token = request.args.get("token")

        if not token:
            return jsonify({"error": "Authorization token is missing"}), 401

        payload = decode_token(token)
        if not payload:
            return jsonify({"error": "Token is invalid or expired"}), 401

        user = db["users"].find_one({"_id": payload["user_id"]})
        if not user:
            return jsonify({"error": "User associated with token not found"}), 401

        # Strip password hash before forwarding
        user_safe = dict(user)
        user_safe.pop("password_hash", None)
        return f(user_safe, *args, **kwargs)

    return decorated

def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            if current_user.get("role") not in allowed_roles:
                return jsonify({"error": "Unauthorized access for this user role"}), 403
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator
