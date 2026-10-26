import uuid
from flask import Blueprint, request, jsonify
from ..db import db
from ..auth import token_required

lab_bp = Blueprint("lab_reports", __name__, url_prefix="/api/lab-reports")

@lab_bp.route("/stats", methods=["GET"])
@token_required
def get_lab_stats(current_user):
    role = current_user.get("role")
    query = {}
    if role == "patient":
        query["patient_id"] = current_user["_id"]

    reports = db["lab_reports"].find(query)
    total = len(reports)
    normal = sum(1 for r in reports if r.get("status") == "Normal")
    critical = sum(1 for r in reports if r.get("status") == "Critical")
    high = sum(1 for r in reports if r.get("status") == "High")
    low = sum(1 for r in reports if r.get("status") == "Low")
    abnormal = high + low + critical

    return jsonify({
        "total": total,
        "normal": normal,
        "abnormal": abnormal,
        "critical": critical,
        "high": high,
        "low": low
    })

@lab_bp.route("", methods=["GET"])
@token_required
def get_lab_reports(current_user):
    role = current_user.get("role")
    query = {}
    if role == "patient":
        query["patient_id"] = current_user["_id"]

    status = request.args.get("status")
    search = request.args.get("search", "").strip().lower()

    reports = db["lab_reports"].find(query)

    if status and status.lower() != "all":
        reports = [r for r in reports if r.get("status", "").lower() == status.lower()]

    if search:
        reports = [
            r for r in reports
            if search in r.get("test_name", "").lower()
            or search in r.get("category", "").lower()
            or search in r.get("ordered_by", "").lower()
            or search in r.get("notes", "").lower()
        ]

    return jsonify({
        "reports": reports,
        "count": len(reports)
    })

@lab_bp.route("/<report_id>", methods=["GET"])
@token_required
def get_report(current_user, report_id):
    rep = db["lab_reports"].find_one({"_id": report_id})
    if not rep:
        return jsonify({"error": "Report not found"}), 404
    return jsonify({"report": rep})

@lab_bp.route("", methods=["POST"])
@token_required
def create_lab_report(current_user):
    data = request.get_json() or {}
    test_name = data.get("test_name")
    category = data.get("category", "General")
    result_value = data.get("result_value")
    unit = data.get("unit", "")
    reference_range = data.get("reference_range", "")
    status = data.get("status", "Normal")
    ordered_by = data.get("ordered_by") or current_user.get("name", "Dr. Arun Kumar")
    patient_id = data.get("patient_id") or current_user["_id"]
    date = data.get("date")

    if not test_name or not result_value:
        return jsonify({"error": "Test name and result value are required"}), 400

    new_report = {
        "_id": f"lab-{uuid.uuid4().hex[:8]}",
        "patient_id": patient_id,
        "test_name": test_name,
        "category": category,
        "result_value": str(result_value),
        "unit": unit,
        "reference_range": reference_range,
        "status": status,
        "date": date or "2026-10-25",
        "ordered_by": ordered_by,
        "notes": data.get("notes", "")
    }

    db["lab_reports"].insert_one(new_report)

    if status == "Critical":
        db["notifications"].insert_one({
            "_id": f"notif-{uuid.uuid4().hex[:8]}",
            "user_id": patient_id,
            "title": f"Critical Lab Flag: {test_name}",
            "message": f"Result {result_value} {unit} flagged Critical ({reference_range}). Clinical review required.",
            "type": "lab",
            "time": "Just now",
            "is_read": False,
            "urgent": True
        })

    return jsonify({
        "message": "Lab report saved",
        "report": new_report
    }), 201
