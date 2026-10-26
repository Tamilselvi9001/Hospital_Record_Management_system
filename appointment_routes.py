import uuid
from flask import Blueprint, request, jsonify
from ..db import db
from ..auth import token_required

appointment_bp = Blueprint("appointments", __name__, url_prefix="/api/appointments")

@appointment_bp.route("", methods=["GET"])
@token_required
def get_appointments(current_user):
    role = current_user.get("role")
    user_id = current_user.get("_id")

    query = {}
    if role == "patient":
        query = {"patient_id": user_id}
    elif role == "doctor":
        # match doctor_id or doctor_name
        doc_record = db["doctors"].find_one({"email": current_user.get("email")})
        doc_id = doc_record["_id"] if doc_record else user_id
        query = {"$or": [{"doctor_id": doc_id}, {"doctor_name": current_user.get("name")}]}
    
    # Admin gets all appointments
    status_filter = request.args.get("status")
    if status_filter and status_filter.lower() != "all":
        query["status"] = status_filter

    appointments = db["appointments"].find(query)
    # Sort appointments by date
    return jsonify({
        "appointments": appointments,
        "count": len(appointments)
    })

@appointment_bp.route("", methods=["POST"])
@token_required
def book_appointment(current_user):
    data = request.get_json() or {}
    doctor_id = data.get("doctor_id")
    doctor_name = data.get("doctor_name")
    date = data.get("date")
    time = data.get("time")
    apt_type = data.get("type", "In-Person Consultation")
    reason = data.get("reason", "General Consultation")
    notes = data.get("notes", "")

    if not date or not time:
        return jsonify({"error": "Date and time are required"}), 400

    doctor = None
    if doctor_id:
        doctor = db["doctors"].find_one({"_id": doctor_id})
    if not doctor and doctor_name:
        doctor = db["doctors"].find_one({"name": doctor_name})
    if not doctor:
        # Pick default doctor
        doctor = db["doctors"].find_one({})

    new_apt = {
        "_id": f"apt-{uuid.uuid4().hex[:8]}",
        "patient_id": current_user["_id"],
        "patient_name": current_user.get("name", "Patient"),
        "doctor_id": doctor["_id"] if doctor else "doc-1",
        "doctor_name": doctor.get("name", "Dr. Arun Kumar") if doctor else "Dr. Arun Kumar",
        "specialty": doctor.get("specialty", "General Medicine") if doctor else "General Medicine",
        "hospital": doctor.get("hospital", "Apollo Specialty Hospitals") if doctor else "Apollo Specialty Hospitals",
        "date": date,
        "time": time,
        "type": apt_type,
        "status": "Confirmed",
        "reason": reason,
        "fee": doctor.get("consultation_fee", 800) if doctor else 800,
        "notes": notes
    }

    db["appointments"].insert_one(new_apt)

    # Add a notification
    db["notifications"].insert_one({
        "_id": f"notif-{uuid.uuid4().hex[:8]}",
        "user_id": current_user["_id"],
        "title": "Appointment Confirmed",
        "message": f"Appointment booked with {new_apt['doctor_name']} on {date} at {time}.",
        "type": "appointment",
        "time": "Just now",
        "is_read": False,
        "urgent": False
    })

    return jsonify({
        "message": "Appointment scheduled successfully",
        "appointment": new_apt
    }), 201

@appointment_bp.route("/<appointment_id>/reschedule", methods=["PUT"])
@token_required
def reschedule_appointment(current_user, appointment_id):
    data = request.get_json() or {}
    new_date = data.get("date")
    new_time = data.get("time")

    if not new_date or not new_time:
        return jsonify({"error": "New date and time are required"}), 400

    apt = db["appointments"].find_one({"_id": appointment_id})
    if not apt:
        return jsonify({"error": "Appointment not found"}), 404

    db["appointments"].update_one(
        {"_id": appointment_id},
        {"$set": {"date": new_date, "time": new_time, "status": "Confirmed"}}
    )

    db["notifications"].insert_one({
        "_id": f"notif-{uuid.uuid4().hex[:8]}",
        "user_id": apt.get("patient_id", current_user["_id"]),
        "title": "Appointment Rescheduled",
        "message": f"Your appointment with {apt.get('doctor_name')} has been moved to {new_date} at {new_time}.",
        "type": "appointment",
        "time": "Just now",
        "is_read": False,
        "urgent": False
    })

    updated = db["appointments"].find_one({"_id": appointment_id})
    return jsonify({"message": "Appointment rescheduled successfully", "appointment": updated})

@appointment_bp.route("/<appointment_id>/cancel", methods=["PUT"])
@token_required
def cancel_appointment(current_user, appointment_id):
    apt = db["appointments"].find_one({"_id": appointment_id})
    if not apt:
        return jsonify({"error": "Appointment not found"}), 404

    db["appointments"].update_one(
        {"_id": appointment_id},
        {"$set": {"status": "Cancelled"}}
    )

    db["notifications"].insert_one({
        "_id": f"notif-{uuid.uuid4().hex[:8]}",
        "user_id": apt.get("patient_id", current_user["_id"]),
        "title": "Appointment Cancelled",
        "message": f"Appointment with {apt.get('doctor_name')} for {apt.get('date')} was cancelled.",
        "type": "appointment",
        "time": "Just now",
        "is_read": False,
        "urgent": False
    })

    return jsonify({"message": "Appointment cancelled successfully"})

@appointment_bp.route("/<appointment_id>/status", methods=["PUT"])
@token_required
def update_status(current_user, appointment_id):
    data = request.get_json() or {}
    status = data.get("status")
    if not status:
        return jsonify({"error": "Status is required"}), 400

    db["appointments"].update_one(
        {"_id": appointment_id},
        {"$set": {"status": status}}
    )
    return jsonify({"message": f"Appointment marked as {status}"})
