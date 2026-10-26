import uuid
import datetime
from flask import Blueprint, request, jsonify
from ..db import db
from ..auth import token_required

ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")

DEMO_AI_ANALYSIS = {
    "document_name": "Blood_Report_Aug2026.pdf",
    "analysis_id": "ai-rep-884920",
    "analyzed_at": "2026-10-25T14:30:00Z",
    "model_version": "MediVault BioClinical LLM v4.2",
    "executive_summary": "Overall physiological status demonstrates controlled cardiovascular baseline on current ARB therapy, however 2 notable biomarkers require attention: Serum Potassium (5.6 mEq/L) is elevated beyond standard range, and atherogenic LDL Cholesterol (148 mg/dL) remains higher than recommended targets for cardiovascular risk prophylaxis. Impaired fasting glucose (108 mg/dL) and HbA1c (6.4%) confirm a pre-diabetic state.",
    "severity": "High Attention Required",
    "flagged_biomarkers": [
        {
            "biomarker": "Serum Potassium (K+)",
            "measured_value": "5.6 mEq/L",
            "reference_range": "3.5 - 5.0 mEq/L",
            "severity": "Critical",
            "badge_color": "rose",
            "clinical_significance": "Elevated potassium (hyperkalemia) can impact myocardial conduction. Because you are currently taking Telmisartan (an ARB that conserves potassium), this warrants immediate clinical correlation with your cardiologist Dr. Arun Kumar."
        },
        {
            "biomarker": "LDL Cholesterol",
            "measured_value": "148 mg/dL",
            "reference_range": "< 100 mg/dL",
            "severity": "High",
            "badge_color": "amber",
            "clinical_significance": "Atherogenic lipid fraction is above optimal thresholds. Supports continuing statin therapy (Atorvastatin 20mg) alongside dietary reduction in saturated fats."
        },
        {
            "biomarker": "HbA1c (Glycated Hemoglobin)",
            "measured_value": "6.4 %",
            "reference_range": "4.0 - 5.6 %",
            "severity": "High",
            "badge_color": "amber",
            "clinical_significance": "Indicates 90-day average blood sugar in the upper pre-diabetes band (5.7 - 6.4%). Adherence to Metformin 500mg SR and portion control is strongly recommended."
        },
        {
            "biomarker": "Vitamin D3 (25-OH)",
            "measured_value": "18 ng/mL",
            "reference_range": "30 - 100 ng/mL",
            "severity": "Deficient",
            "badge_color": "sky",
            "clinical_significance": "Hypovitaminosis D3 can exacerbate fatigue, musculoskeletal aches, and impaired calcium absorption. Weekly replenishment regimen suggested."
        }
    ],
    "normal_biomarkers_count": 6,
    "questions_for_doctor": [
        "Given my potassium level of 5.6 mEq/L, should my Telmisartan dosage be adjusted or should we repeat the serum electrolyte panel next week?",
        "Do I need to restrict high-potassium foods like bananas, coconut water, and spinach temporarily?",
        "Should my Atorvastatin dose remain at 20mg or be titrated given LDL is 148 mg/dL?",
        "What target HbA1c should we aim for over the next 3 to 6 months with lifestyle and Metformin?"
    ],
    "lifestyle_recommendations": [
        "Electrolytes: Avoid potassium-based salt substitutes and potassium supplements until reviewed by Dr. Arun Kumar.",
        "Cardiovascular Diet: Increase soluble fiber (oats, legumes, psyllium husk) to promote LDL clearance.",
        "Activity: Maintain 150 minutes per week of moderate-intensity aerobic exercise (brisk walking, cycling) to improve peripheral insulin sensitivity.",
        "Hydration: Maintain consistent daily fluid intake (2.2 - 2.5 Liters) unless contraindicated."
    ],
    "disclaimer": "MediVault AI provides educational interpretation based on clinical reference ranges. It is an auxiliary decision aid and does not constitute formal medical diagnosis. Always consult your licensed healthcare physician."
}

@ai_bp.route("/analyze-report", methods=["POST"])
@token_required
def analyze_report(current_user):
    data = request.get_json(silent=True) or {}
    use_demo = data.get("use_demo", False)
    
    # If file was uploaded via multipart/form-data
    if "file" in request.files:
        uploaded_file = request.files["file"]
        filename = uploaded_file.filename
    else:
        filename = data.get("filename", "Blood_Report_Aug2026.pdf")

    # Generate or retrieve analysis
    analysis = dict(DEMO_AI_ANALYSIS)
    analysis["analysis_id"] = f"ai-{uuid.uuid4().hex[:8]}"
    analysis["document_name"] = filename
    analysis["analyzed_at"] = datetime.datetime.utcnow().isoformat()
    analysis["patient_name"] = current_user.get("name", "Kavya Nair")

    # Save to user's reports collection
    db["ai_reports"].insert_one(analysis)

    return jsonify({
        "message": "AI Medical Analysis completed successfully",
        "analysis": analysis
    })

@ai_bp.route("/history", methods=["GET"])
@token_required
def get_ai_history(current_user):
    reports = db["ai_reports"].find({})
    return jsonify({
        "reports": reports if reports else [DEMO_AI_ANALYSIS],
        "count": len(reports) if reports else 1
    })
