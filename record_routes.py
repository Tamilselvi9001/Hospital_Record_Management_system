import uuid
from flask import Blueprint, request, jsonify
from ..db import db
from ..auth import token_required

record_bp = Blueprint("records", __name__, url_prefix="/api/records")

@record_bp.route("", methods=["GET"])
@token_required
def get_records(current_user):
    role = current_user.get("role")
    patient_id = request.args.get("patient_id")
    specialty = request.args.get("specialty")
    search = request.args.get("search", "").strip().lower()

    query = {}
    if role == "patient":
        query["patient_id"] = current_user["_id"]
    elif patient_id:
        query["patient_id"] = patient_id

    records = db["medical_records"].find(query)

    # Filter in memory if specialty or search
    if specialty and specialty.lower() != "all":
        records = [r for r in records if r.get("specialty", "").lower() == specialty.lower()]

    if search:
        records = [
            r for r in records
            if search in r.get("title", "").lower()
            or search in r.get("doctor_name", "").lower()
            or search in r.get("specialty", "").lower()
            or search in r.get("clinical_notes", "").lower()
            or any(search in s.lower() for s in r.get("symptoms", []))
        ]

    return jsonify({
        "records": records,
        "count": len(records)
    })

@record_bp.route("/<record_id>", methods=["GET"])
@token_required
def get_single_record(current_user, record_id):
    rec = db["medical_records"].find_one({"_id": record_id})
    if not rec:
        return jsonify({"error": "Medical record not found"}), 404
    return jsonify({"record": rec})

@record_bp.route("", methods=["POST"])
@token_required
def add_record(current_user):
    data = request.get_json() or {}
    title = data.get("title")
    date = data.get("date")
    specialty = data.get("specialty", "General Medicine")
    clinical_notes = data.get("clinical_notes", "")
    symptoms = data.get("symptoms", [])
    prescriptions = data.get("prescriptions", [])
    doctor_name = data.get("doctor_name") or current_user.get("name", "Attending Physician")
    patient_id = data.get("patient_id") or current_user["_id"]

    if not title or not date:
        return jsonify({"error": "Title and date are required"}), 400

    new_record = {
        "_id": f"rec-{uuid.uuid4().hex[:8]}",
        "patient_id": patient_id,
        "date": date,
        "title": title,
        "doctor_name": doctor_name,
        "specialty": specialty,
        "hospital": data.get("hospital", "MediVault Clinical Centre"),
        "symptoms": symptoms if isinstance(symptoms, list) else [s.strip() for s in symptoms.split(",") if s.strip()],
        "clinical_notes": clinical_notes,
        "prescriptions": prescriptions if isinstance(prescriptions, list) else [p.strip() for p in prescriptions.split(",") if p.strip()],
        "attachments": data.get("attachments", [
            {"filename": f"Clinical_Summary_{date}.pdf", "size": "1.1 MB", "type": "pdf"}
        ])
    }

    db["medical_records"].insert_one(new_record)

    db["notifications"].insert_one({
        "_id": f"notif-{uuid.uuid4().hex[:8]}",
        "user_id": patient_id,
        "title": "Medical Record Added",
        "message": f"New record '{title}' added to your health vault.",
        "type": "record",
        "time": "Just now",
        "is_read": False,
        "urgent": False
    })

    return jsonify({
        "message": "Medical record stored securely",
        "record": new_record
    }), 201
