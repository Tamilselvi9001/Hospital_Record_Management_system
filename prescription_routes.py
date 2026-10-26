import uuid
from flask import Blueprint, request, jsonify
from ..db import db
from ..auth import token_required

prescription_bp = Blueprint("prescriptions", __name__, url_prefix="/api/prescriptions")

@prescription_bp.route("/stats", methods=["GET"])
@token_required
def get_rx_stats(current_user):
    role = current_user.get("role")
    query = {}
    if role == "patient":
        query["patient_id"] = current_user["_id"]

    all_rx = db["prescriptions"].find(query)
    active = sum(1 for r in all_rx if r.get("status") == "Active")
    completed = sum(1 for r in all_rx if r.get("status") == "Completed")
    refills_due = sum(1 for r in all_rx if r.get("refill_due_in_days", 999) <= 7 and r.get("status") == "Active")
    
    total_meds = 0
    for r in all_rx:
        total_meds += len(r.get("medicines", []))

    return jsonify({
        "active": active,
        "completed": completed,
        "total_medicines": total_meds,
        "refills_due": refills_due,
        "total": len(all_rx)
    })

@prescription_bp.route("", methods=["GET"])
@token_required
def get_prescriptions(current_user):
    role = current_user.get("role")
    query = {}
    if role == "patient":
        query["patient_id"] = current_user["_id"]

    status = request.args.get("status")
    search = request.args.get("search", "").strip().lower()

    rx_list = db["prescriptions"].find(query)

    if status and status.lower() != "all":
        rx_list = [r for r in rx_list if r.get("status", "").lower() == status.lower()]

    if search:
        rx_list = [
            r for r in rx_list
            if search in r.get("condition", "").lower()
            or search in r.get("doctor_name", "").lower()
            or any(search in m.get("name", "").lower() for m in r.get("medicines", []))
        ]

    return jsonify({
        "prescriptions": rx_list,
        "count": len(rx_list)
    })

@prescription_bp.route("", methods=["POST"])
@token_required
def create_prescription(current_user):
    data = request.get_json() or {}
    condition = data.get("condition")
    medicines = data.get("medicines", [])
    patient_id = data.get("patient_id") or current_user["_id"]
    doctor_name = data.get("doctor_name") or current_user.get("name", "Dr. Arun Kumar")
    doctor_specialty = data.get("doctor_specialty") or current_user.get("specialty", "Cardiology")
    refills = data.get("refills", 2)
    valid_until = data.get("valid_until", "2026-11-25")

    if not condition or not medicines:
        return jsonify({"error": "Condition and at least one medicine are required"}), 400

    new_rx = {
        "_id": f"rx-{uuid.uuid4().hex[:8]}",
        "patient_id": patient_id,
        "doctor_name": doctor_name,
        "doctor_specialty": doctor_specialty,
        "condition": condition,
        "prescribed_date": "2026-10-25",
        "valid_until": valid_until,
        "status": "Active",
        "refills_remaining": int(refills),
        "refill_due_in_days": 30,
        "medicines": medicines
    }

    db["prescriptions"].insert_one(new_rx)

    db["notifications"].insert_one({
        "_id": f"notif-{uuid.uuid4().hex[:8]}",
        "user_id": patient_id,
        "title": "New Prescription Issued",
        "message": f"{doctor_name} issued a new prescription for {condition}.",
        "type": "prescription",
        "time": "Just now",
        "is_read": False,
        "urgent": False
    })

    return jsonify({
        "message": "Prescription issued successfully",
        "prescription": new_rx
    }), 201

@prescription_bp.route("/<prescription_id>/refill", methods=["PUT"])
@token_required
def request_refill(current_user, prescription_id):
    rx = db["prescriptions"].find_one({"_id": prescription_id})
    if not rx:
        return jsonify({"error": "Prescription not found"}), 404

    refills_remaining = rx.get("refills_remaining", 0)
    if refills_remaining <= 0:
        return jsonify({"error": "No refills remaining for this prescription. Please consult your physician."}), 400

    new_refills = refills_remaining - 1
    db["prescriptions"].update_one(
        {"_id": prescription_id},
        {"$set": {
            "refills_remaining": new_refills,
            "refill_due_in_days": 30,
            "alert": None
        }}
    )

    db["notifications"].insert_one({
        "_id": f"notif-{uuid.uuid4().hex[:8]}",
        "user_id": rx.get("patient_id", current_user["_id"]),
        "title": "Prescription Refill Requested",
        "message": f"Refill requested for {rx.get('condition')}. Forwarded to Apollo Pharmacy.",
        "type": "prescription",
        "time": "Just now",
        "is_read": False,
        "urgent": False
    })

    return jsonify({
        "message": "Refill order submitted successfully. Pharmacy processing in progress.",
        "refills_remaining": new_refills
    })
