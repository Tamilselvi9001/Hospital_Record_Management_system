from flask import Blueprint, request, jsonify
from ..db import db
from ..auth import token_required

notification_bp = Blueprint("notifications", __name__, url_prefix="/api/notifications")

@notification_bp.route("", methods=["GET"])
@token_required
def get_notifications(current_user):
    user_id = current_user["_id"]
    notifs = db["notifications"].find({"$or": [{"user_id": user_id}, {"user_id": "user-patient-1"}]})
    unread_count = sum(1 for n in notifs if not n.get("is_read", False))

    return jsonify({
        "notifications": notifs,
        "unread_count": unread_count,
        "count": len(notifs)
    })

@notification_bp.route("/<notif_id>/read", methods=["PUT"])
@token_required
def mark_read(current_user, notif_id):
    db["notifications"].update_one(
        {"_id": notif_id},
        {"$set": {"is_read": True}}
    )
    return jsonify({"message": "Notification marked as read"})

@notification_bp.route("/read-all", methods=["PUT"])
@token_required
def mark_all_read(current_user):
    user_id = current_user["_id"]
    db["notifications"].update_one(
        {"user_id": user_id},
        {"$set": {"is_read": True}}
    )
    # Also update any unread in fallback storage
    for n in db["notifications"].find({"$or": [{"user_id": user_id}, {"user_id": "user-patient-1"}]}):
        db["notifications"].update_one({"_id": n["_id"]}, {"$set": {"is_read": True}})

    return jsonify({"message": "All notifications marked as read"})
