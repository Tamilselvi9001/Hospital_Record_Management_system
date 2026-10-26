import uuid
from flask import Blueprint, request, jsonify
from ..db import db
from ..auth import hash_password, verify_password, generate_token, token_required

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/demo-accounts", methods=["GET"])
def get_demo_accounts():
    return jsonify({
        "patient": {"email": "patient@medivault.com", "password": "Patient@123", "role": "patient", "name": "Kavya Nair"},
        "doctor": {"email": "doctor@medivault.com", "password": "Doctor@123", "role": "doctor", "name": "Dr. Arun Kumar"},
        "admin": {"email": "admin@medivault.com", "password": "Admin@123", "role": "admin", "name": "Dr. Sarah Jenkins"}
    })

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = db["users"].find_one({"email": email})
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    if not verify_password(password, user.get("password_hash", "")):
        return jsonify({"error": "Invalid email or password"}), 401

    token = generate_token(user)
    user_safe = dict(user)
    user_safe.pop("password_hash", None)

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": user_safe
    })

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    role = data.get("role", "patient").strip().lower()

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), 400

    if role not in ["patient", "doctor", "admin"]:
        role = "patient"

    existing = db["users"].find_one({"email": email})
    if existing:
        return jsonify({"error": "An account with this email already exists"}), 409

    new_user = {
        "_id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "password_hash": hash_password(password),
        "role": role,
        "phone": data.get("phone", "+91 98000 00000"),
        "gender": data.get("gender", "Not specified"),
        "blood_group": data.get("blood_group", "O+"),
        "abha_id": f"91-{uuid.uuid4().hex[:4].upper()}-{uuid.uuid4().hex[4:8].upper()}-2026",
        "address": data.get("address", "Bangalore, India"),
        "allergies": data.get("allergies", []),
        "chronic_conditions": data.get("chronic_conditions", []),
        "insurance_provider": "MediCare Shield",
        "insurance_policy": f"POL-{uuid.uuid4().hex[:6].upper()}",
        "avatar": f"https://api.dicebear.com/7.x/initials/svg?seed={name}"
    }

    if role == "doctor":
        new_user["specialty"] = data.get("specialty", "General Medicine")
        new_user["qualifications"] = data.get("qualifications", "MBBS, MD")
        new_user["hospital"] = data.get("hospital", "MediVault General Hospital")
        new_user["consultation_fee"] = data.get("consultation_fee", 500)
        new_user["experience"] = data.get("experience", "5 years")
        new_user["availability"] = "Available Today"
        new_user["rating"] = 5.0
        new_user["reviews_count"] = 1
        
        # Add to doctors collection as well
        db["doctors"].insert_one({
            "_id": new_user["_id"],
            "name": new_user["name"],
            "email": new_user["email"],
            "specialty": new_user["specialty"],
            "qualifications": new_user["qualifications"],
            "hospital": new_user["hospital"],
            "consultation_fee": new_user["consultation_fee"],
            "experience": new_user["experience"],
            "availability": new_user["availability"],
            "rating": 5.0,
            "reviews_count": 1,
            "avatar": new_user["avatar"]
        })

    db["users"].insert_one(new_user)
    token = generate_token(new_user)
    safe_user = dict(new_user)
    safe_user.pop("password_hash", None)

    return jsonify({
        "message": "Account created successfully",
        "token": token,
        "user": safe_user
    }), 201

@auth_bp.route("/me", methods=["GET"])
@token_required
def get_current_user(current_user):
    return jsonify({"user": current_user})

@auth_bp.route("/profile", methods=["PUT"])
@token_required
def update_profile(current_user):
    data = request.get_json() or {}
    allowed_fields = [
        "name", "phone", "gender", "blood_group", "address", 
        "allergies", "chronic_conditions", "emergency_contact",
        "insurance_provider", "insurance_policy"
    ]
    updates = {}
    for f in allowed_fields:
        if f in data:
            updates[f] = data[f]

    if updates:
        db["users"].update_one({"_id": current_user["_id"]}, {"$set": updates})
        updated_user = db["users"].find_one({"_id": current_user["_id"]})
        updated_user.pop("password_hash", None)
        return jsonify({"message": "Profile updated successfully", "user": updated_user})

    return jsonify({"message": "No updates applied", "user": current_user})
