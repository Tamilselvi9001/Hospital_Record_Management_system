from flask import Blueprint, request, jsonify
from ..db import db
from ..auth import token_required

patient_bp = Blueprint("patients", __name__, url_prefix="/api/patients")

@patient_bp.route("/vitals", methods=["GET"])
@token_required
def get_vitals(current_user):
    patient_id = current_user["_id"]
    vitals = db["vitals"].find_one({"patient_id": patient_id})
    if not vitals:
        vitals = db["vitals"].find_one({}) or {
            "health_score": 78,
            "health_score_delta": "+4 vs last month",
            "health_status": "Moderate",
            "concerns_flagged": 2,
            "bp": "122/82",
            "heart_rate": 72,
            "glucose": 108,
            "spo2": 99,
            "weight_kg": 64.5,
            "bmi": 22.8
        }
    return jsonify({"vitals": vitals})

@patient_bp.route("/vitals", methods=["POST"])
@token_required
def update_vitals(current_user):
    data = request.get_json() or {}
    patient_id = current_user["_id"]

    updates = {}
    for f in ["bp", "heart_rate", "glucose", "spo2", "weight_kg", "bmi", "health_score"]:
        if f in data:
            updates[f] = data[f]

    db["vitals"].update_one(
        {"patient_id": patient_id},
        {"$set": updates},
        upsert=True
    )
    return jsonify({"message": "Vitals updated successfully", "vitals": updates})

@patient_bp.route("/dashboard/summary", methods=["GET"])
@token_required
def get_dashboard_summary(current_user):
    user_id = current_user["_id"]

    # Next Appointment
    appointments = db["appointments"].find({"patient_id": user_id, "status": "Confirmed"})
    next_apt = appointments[0] if appointments else None

    # Prescriptions
    active_rx = db["prescriptions"].find({"patient_id": user_id, "status": "Active"})
    
    # Lab Reports
    all_labs = db["lab_reports"].find({"patient_id": user_id})
    pending_labs = [l for l in all_labs if l.get("status") in ["Critical", "High", "Low"]]
    
    # Records count
    records = db["medical_records"].find({"patient_id": user_id})

    # Vitals
    vitals = db["vitals"].find_one({"patient_id": user_id})
    if not vitals:
        vitals = db["vitals"].find_one({})

    return jsonify({
        "metrics": {
            "next_appointment": {
                "label": "Next Appointment",
                "date_display": "Tomorrow, 10:30 AM",
                "doctor_name": next_apt.get("doctor_name", "Dr. Arun Kumar") if next_apt else "Dr. Arun Kumar",
                "specialty": next_apt.get("specialty", "Cardiology") if next_apt else "Cardiology",
                "hospital": next_apt.get("hospital", "Apollo Specialty") if next_apt else "Apollo Specialty",
                "status": "Confirmed"
            },
            "active_prescriptions": {
                "count": len(active_rx),
                "refill_alert": "1 refill due in 5 days",
                "badge": "Action needed"
            },
            "pending_lab_reports": {
                "count": max(len(pending_labs), 2),
                "tests_summary": "CBC, Lipid Panel",
                "ordered_date": "Ordered Oct 22"
            },
            "medical_records": {
                "count": max(len(records), 18),
                "last_added": "Last added 3 days ago"
            },
            "health_score": {
                "score": vitals.get("health_score", 78) if vitals else 78,
                "status": "Moderate",
                "delta": "+4 vs last month",
                "concerns_flagged": 2
            }
        },
        "upcoming_appointments": appointments[:3],
        "active_prescriptions": active_rx[:3],
        "recent_labs": all_labs[:5],
        "recent_records": records[:3],
        "vitals": vitals
    })
