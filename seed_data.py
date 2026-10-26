import bcrypt
import datetime

def hash_pw(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

DEMO_USERS = [
    {
        "_id": "user-patient-1",
        "name": "Kavya Nair",
        "email": "patient@medivault.com",
        "password_hash": hash_pw("Patient@123"),
        "role": "patient",
        "phone": "+91 98450 12345",
        "age": 28,
        "gender": "Female",
        "blood_group": "O+",
        "abha_id": "91-4523-8819-2041",
        "address": "Indiranagar, Bangalore, Karnataka - 560038",
        "allergies": ["Penicillin", "Sulfa drugs"],
        "chronic_conditions": ["Mild Hypertension", "Borderline Pre-diabetes"],
        "emergency_contact": "Rohan Nair (Brother) - +91 98450 67890",
        "insurance_provider": "Star Health Comprehensive",
        "insurance_policy": "SH-POL-884920-2026",
        "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80"
    },
    {
        "_id": "user-doctor-1",
        "name": "Dr. Arun Kumar",
        "email": "doctor@medivault.com",
        "password_hash": hash_pw("Doctor@123"),
        "role": "doctor",
        "phone": "+91 98112 34567",
        "specialty": "Cardiology",
        "qualifications": "MBBS, MD (Cardiology), FACC",
        "hospital": "Apollo Specialty Hospitals, Bangalore",
        "experience": "14 years",
        "rating": 4.9,
        "reviews_count": 184,
        "consultation_fee": 800,
        "availability": "Available Today",
        "reg_number": "MCI-2014-48291",
        "bio": "Senior Consultant Cardiologist specializing in preventive cardiology, hypertensive heart disease, echocardiography and cardiac rehabilitation.",
        "avatar": "https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=150&auto=format&fit=crop&q=80"
    },
    {
        "_id": "user-admin-1",
        "name": "Dr. Sarah Jenkins",
        "email": "admin@medivault.com",
        "password_hash": hash_pw("Admin@123"),
        "role": "admin",
        "title": "Hospital System Administrator & Chief Medical Officer",
        "department": "MediVault Central Operations",
        "phone": "+91 98100 99999",
        "avatar": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80"
    }
]

ALL_DOCTORS = [
    {
        "_id": "doc-1",
        "name": "Dr. Arun Kumar",
        "email": "doctor@medivault.com",
        "specialty": "Cardiology",
        "qualifications": "MBBS, MD (Cardiology), FACC",
        "hospital": "Apollo Specialty Hospitals",
        "experience": "14 years",
        "rating": 4.9,
        "reviews_count": 184,
        "consultation_fee": 800,
        "availability": "Available Today",
        "reg_number": "MCI-2014-48291",
        "next_slot": "Today, 04:00 PM",
        "bio": "Senior Consultant Cardiologist specializing in preventive cardiology and hypertension.",
        "avatar": "https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=150&auto=format&fit=crop&q=80"
    },
    {
        "_id": "doc-2",
        "name": "Dr. Meera Nambiar",
        "email": "meera.nambiar@medivault.com",
        "specialty": "General Medicine",
        "qualifications": "MBBS, MD (Internal Medicine)",
        "hospital": "Fortis Hospital, Bannerghatta",
        "experience": "10 years",
        "rating": 4.8,
        "reviews_count": 142,
        "consultation_fee": 600,
        "availability": "Available Today",
        "reg_number": "MCI-2016-19382",
        "next_slot": "Today, 05:30 PM",
        "bio": "Internal Medicine physician dedicated to chronic metabolic disorder management and lifestyle health.",
        "avatar": "https://images.unsplash.com/photo-1594824813633-890251754020?w=150&auto=format&fit=crop&q=80"
    },
    {
        "_id": "doc-3",
        "name": "Dr. Rajesh Sharma",
        "email": "rajesh.sharma@medivault.com",
        "specialty": "Neurology",
        "qualifications": "MBBS, DM (Neurology), FINR",
        "hospital": "Manipal Hospital, Old Airport Rd",
        "experience": "18 years",
        "rating": 4.95,
        "reviews_count": 210,
        "consultation_fee": 1000,
        "availability": "Next available tomorrow",
        "reg_number": "MCI-2008-09124",
        "next_slot": "Tomorrow, 11:00 AM",
        "bio": "Leading clinical neurologist treating migraines, neuromuscular disorders, neuropathy and stroke recovery.",
        "avatar": "https://images.unsplash.com/photo-1537368910025-700350fe46c7?w=150&auto=format&fit=crop&q=80"
    },
    {
        "_id": "doc-4",
        "name": "Dr. Priya Sundaram",
        "email": "priya.sundaram@medivault.com",
        "specialty": "Orthopedics",
        "qualifications": "MBBS, MS (Ortho), Fellowship Spine",
        "hospital": "Aster CMI Hospital, Hebbal",
        "experience": "12 years",
        "rating": 4.7,
        "reviews_count": 98,
        "consultation_fee": 750,
        "availability": "Available Today",
        "reg_number": "MCI-2013-58190",
        "next_slot": "Today, 06:15 PM",
        "bio": "Specialist in joint health, ergonomic posture recovery, spine care, and sports trauma prevention.",
        "avatar": "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=150&auto=format&fit=crop&q=80"
    },
    {
        "_id": "doc-5",
        "name": "Dr. Siddharth Rao",
        "email": "siddharth.rao@medivault.com",
        "specialty": "Dermatology",
        "qualifications": "MBBS, MD (Dermatology, Venereology & Leprosy)",
        "hospital": "Columbia Asia Hospital, Whitefield",
        "experience": "8 years",
        "rating": 4.85,
        "reviews_count": 115,
        "consultation_fee": 650,
        "availability": "Available Today",
        "reg_number": "MCI-2018-72019",
        "next_slot": "Today, 03:30 PM",
        "bio": "Clinical and aesthetic dermatologist offering personalized treatments for eczema, acne, and allergy triggers.",
        "avatar": "https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=150&auto=format&fit=crop&q=80"
    }
]

INITIAL_APPOINTMENTS = [
    {
        "_id": "apt-1",
        "patient_id": "user-patient-1",
        "patient_name": "Kavya Nair",
        "doctor_id": "doc-1",
        "doctor_name": "Dr. Arun Kumar",
        "specialty": "Cardiology",
        "hospital": "Apollo Specialty Hospitals",
        "date": "2026-10-26",
        "time": "10:30 AM",
        "type": "In-Person Consultation",
        "status": "Confirmed",
        "reason": "Routine Cardiology Follow-up & ECG Review",
        "fee": 800,
        "notes": "Patient reports blood pressure is well tolerated on Telmisartan. Review ECG trace."
    },
    {
        "_id": "apt-2",
        "patient_id": "user-patient-1",
        "patient_name": "Kavya Nair",
        "doctor_id": "doc-2",
        "doctor_name": "Dr. Meera Nambiar",
        "specialty": "General Medicine",
        "hospital": "Fortis Hospital",
        "date": "2026-10-28",
        "time": "02:30 PM",
        "type": "Video Call",
        "status": "Confirmed",
        "reason": "Metabolic review & HbA1c diet planning",
        "fee": 600,
        "notes": "Tele-consultation to evaluate fasting sugar logs and dietary adherence."
    },
    {
        "_id": "apt-3",
        "patient_id": "user-patient-1",
        "patient_name": "Kavya Nair",
        "doctor_id": "doc-3",
        "doctor_name": "Dr. Rajesh Sharma",
        "specialty": "Neurology",
        "hospital": "Manipal Hospital",
        "date": "2026-11-02",
        "time": "11:00 AM",
        "type": "In-Person Consultation",
        "status": "Pending",
        "reason": "Occasional tension headache assessment",
        "fee": 1000,
        "notes": "Awaiting appointment confirmation from clinic reception."
    },
    {
        "_id": "apt-4",
        "patient_id": "user-patient-1",
        "patient_name": "Kavya Nair",
        "doctor_id": "doc-4",
        "doctor_name": "Dr. Priya Sundaram",
        "specialty": "Orthopedics",
        "hospital": "Aster CMI Hospital",
        "date": "2026-11-08",
        "time": "04:15 PM",
        "type": "In-Person Consultation",
        "status": "Pending",
        "reason": "Posture & upper back ergonomic assessment",
        "fee": 750,
        "notes": "Work from home neck and shoulder strain assessment."
    },
    {
        "_id": "apt-5",
        "patient_id": "user-patient-1",
        "patient_name": "Kavya Nair",
        "doctor_id": "doc-1",
        "doctor_name": "Dr. Arun Kumar",
        "specialty": "Cardiology",
        "hospital": "Apollo Specialty Hospitals",
        "date": "2026-10-10",
        "time": "10:00 AM",
        "type": "In-Person Consultation",
        "status": "Completed",
        "reason": "Hypertensive baseline assessment",
        "fee": 800,
        "notes": "Baseline BP evaluated at 134/88. Started on Telmisartan 40mg."
    },
    {
        "_id": "apt-6",
        "patient_id": "user-patient-1",
        "patient_name": "Kavya Nair",
        "doctor_id": "doc-2",
        "doctor_name": "Dr. Meera Nambiar",
        "specialty": "General Medicine",
        "hospital": "Fortis Hospital",
        "date": "2026-09-15",
        "time": "03:00 PM",
        "type": "Video Call",
        "status": "Completed",
        "reason": "Seasonal allergy consultation",
        "fee": 600,
        "notes": "Allergic rhinitis symptoms treated with antihistamines."
    }
]

INITIAL_LAB_REPORTS = [
    {
        "_id": "lab-1",
        "patient_id": "user-patient-1",
        "test_name": "Complete Blood Count - Platelets",
        "category": "Hematology",
        "result_value": "142",
        "unit": "x10^3/uL",
        "reference_range": "150 - 450",
        "status": "Low",
        "date": "2026-10-22",
        "ordered_by": "Dr. Arun Kumar",
        "notes": "Slight thrombocytopenia. Recommend follow-up CBC in 4 weeks."
    },
    {
        "_id": "lab-2",
        "patient_id": "user-patient-1",
        "test_name": "Fasting Blood Sugar (FBS)",
        "category": "Biochemistry",
        "result_value": "108",
        "unit": "mg/dL",
        "reference_range": "70 - 99",
        "status": "High",
        "date": "2026-10-22",
        "ordered_by": "Dr. Meera Nambiar",
        "notes": "Impaired fasting glucose indicative of pre-diabetic state."
    },
    {
        "_id": "lab-3",
        "patient_id": "user-patient-1",
        "test_name": "HbA1c (Glycated Hemoglobin)",
        "category": "Biochemistry",
        "result_value": "6.4",
        "unit": "%",
        "reference_range": "4.0 - 5.6",
        "status": "High",
        "date": "2026-10-22",
        "ordered_by": "Dr. Meera Nambiar",
        "notes": "HbA1c prediabetes range (5.7 - 6.4%). Continue low glycemic diet and exercise."
    },
    {
        "_id": "lab-4",
        "patient_id": "user-patient-1",
        "test_name": "Serum Creatinine",
        "category": "Renal Panel",
        "result_value": "0.9",
        "unit": "mg/dL",
        "reference_range": "0.6 - 1.2",
        "status": "Normal",
        "date": "2026-10-22",
        "ordered_by": "Dr. Arun Kumar",
        "notes": "Kidney filtration rate is normal."
    },
    {
        "_id": "lab-5",
        "patient_id": "user-patient-1",
        "test_name": "Lipid Profile - LDL Cholesterol",
        "category": "Biochemistry",
        "result_value": "148",
        "unit": "mg/dL",
        "reference_range": "< 100",
        "status": "High",
        "date": "2026-10-20",
        "ordered_by": "Dr. Arun Kumar",
        "notes": "Elevated atherogenic lipoprotein. Adhere strictly to Atorvastatin 20mg."
    },
    {
        "_id": "lab-6",
        "patient_id": "user-patient-1",
        "test_name": "Lipid Profile - HDL Cholesterol",
        "category": "Biochemistry",
        "result_value": "52",
        "unit": "mg/dL",
        "reference_range": "> 50",
        "status": "Normal",
        "date": "2026-10-20",
        "ordered_by": "Dr. Arun Kumar",
        "notes": "Good protective cholesterol within healthy threshold."
    },
    {
        "_id": "lab-7",
        "patient_id": "user-patient-1",
        "test_name": "Serum Potassium (K+)",
        "category": "Biochemistry",
        "result_value": "5.6",
        "unit": "mEq/L",
        "reference_range": "3.5 - 5.0",
        "status": "Critical",
        "date": "2026-10-22",
        "ordered_by": "Dr. Arun Kumar",
        "notes": "URGENT: Hyperkalemia detected. Review ARB medications and repeat test within 48h."
    },
    {
        "_id": "lab-8",
        "patient_id": "user-patient-1",
        "test_name": "Thyroid Stimulating Hormone (TSH)",
        "category": "Endocrinology",
        "result_value": "2.4",
        "unit": "uIU/mL",
        "reference_range": "0.4 - 4.0",
        "status": "Normal",
        "date": "2026-10-18",
        "ordered_by": "Dr. Meera Nambiar",
        "notes": "Euthyroid state. Thyroid function normal."
    },
    {
        "_id": "lab-9",
        "patient_id": "user-patient-1",
        "test_name": "Vitamin D3 (25-Hydroxy)",
        "category": "Endocrinology",
        "result_value": "18",
        "unit": "ng/mL",
        "reference_range": "30 - 100",
        "status": "Low",
        "date": "2026-10-18",
        "ordered_by": "Dr. Meera Nambiar",
        "notes": "Deficiency noted. Prescribed Vitamin D3 60k IU weekly replenishment."
    },
    {
        "_id": "lab-10",
        "patient_id": "user-patient-1",
        "test_name": "Liver Function - ALT / SGPT",
        "category": "Hepatic Panel",
        "result_value": "32",
        "unit": "U/L",
        "reference_range": "7 - 56",
        "status": "Normal",
        "date": "2026-10-18",
        "ordered_by": "Dr. Arun Kumar",
        "notes": "Liver enzyme clearance is optimal."
    }
]

INITIAL_PRESCRIPTIONS = [
    {
        "_id": "rx-1",
        "patient_id": "user-patient-1",
        "doctor_name": "Dr. Arun Kumar",
        "doctor_specialty": "Cardiology",
        "condition": "Hyperlipidemia & Atherosclerosis Prophylaxis",
        "prescribed_date": "2026-10-20",
        "valid_until": "2026-11-20",
        "status": "Active",
        "refills_remaining": 2,
        "refill_due_in_days": 18,
        "medicines": [
            {
                "name": "Atorvastatin 20mg (Lipitor)",
                "dosage": "1 tablet daily after dinner at bedtime",
                "frequency": "0-0-1",
                "duration": "30 days",
                "instructions": "Take at consistent hour; avoid grapefruit juice."
            }
        ]
    },
    {
        "_id": "rx-2",
        "patient_id": "user-patient-1",
        "doctor_name": "Dr. Meera Nambiar",
        "doctor_specialty": "General Medicine",
        "condition": "Impaired Fasting Glucose (Pre-Diabetes)",
        "prescribed_date": "2026-09-25",
        "valid_until": "2026-10-30",
        "status": "Active",
        "refills_remaining": 1,
        "refill_due_in_days": 5,
        "alert": "Refill due in 5 days! Action needed.",
        "medicines": [
            {
                "name": "Metformin 500mg (Glucophage SR)",
                "dosage": "1 tablet twice daily with morning & evening meals",
                "frequency": "1-0-1",
                "duration": "60 days",
                "instructions": "Take with meals to minimize gastrointestinal discomfort."
            }
        ]
    },
    {
        "_id": "rx-3",
        "patient_id": "user-patient-1",
        "doctor_name": "Dr. Arun Kumar",
        "doctor_specialty": "Cardiology",
        "condition": "Essential Hypertension (Stage 1)",
        "prescribed_date": "2026-10-10",
        "valid_until": "2026-11-10",
        "status": "Active",
        "refills_remaining": 3,
        "refill_due_in_days": 15,
        "medicines": [
            {
                "name": "Telmisartan 40mg (Micardis)",
                "dosage": "1 tablet once daily morning after breakfast",
                "frequency": "1-0-0",
                "duration": "30 days",
                "instructions": "Monitor home blood pressure 3 times weekly."
            }
        ]
    },
    {
        "_id": "rx-4",
        "patient_id": "user-patient-1",
        "doctor_name": "Dr. Meera Nambiar",
        "doctor_specialty": "General Medicine",
        "condition": "Hypovitaminosis D3 replenishment",
        "prescribed_date": "2026-08-10",
        "valid_until": "2026-10-05",
        "status": "Completed",
        "refills_remaining": 0,
        "refill_due_in_days": 0,
        "medicines": [
            {
                "name": "Cholecalciferol 60,000 IU (D3 Must)",
                "dosage": "1 capsule once weekly every Sunday with milk",
                "frequency": "Once weekly",
                "duration": "8 weeks",
                "instructions": "Completed 8-week course. Maintenance dose pending."
            }
        ]
    }
]

INITIAL_MEDICAL_RECORDS = [
    {
        "_id": "rec-1",
        "patient_id": "user-patient-1",
        "date": "2026-10-22",
        "title": "Hypertensive Heart Disease Evaluation & ECG",
        "doctor_name": "Dr. Arun Kumar",
        "specialty": "Cardiology",
        "hospital": "Apollo Specialty Hospitals",
        "symptoms": ["Occasional Palpitations", "Mild Exertional Dyspnea", "Stress"],
        "clinical_notes": "Patient presents for 2-week review following initiation of Telmisartan 40mg. Resting BP 122/82 mmHg. Resting heart rate 72 bpm regular. S1/S2 normal without gallops. Standard 12-lead ECG reveals sinus rhythm with normal axis.",
        "prescriptions": ["Telmisartan 40mg", "Atorvastatin 20mg"],
        "attachments": [
            {"filename": "12_Lead_ECG_Apollo_Oct2026.pdf", "size": "1.2 MB", "type": "pdf"},
            {"filename": "Echocardiogram_Summary.pdf", "size": "2.4 MB", "type": "pdf"}
        ]
    },
    {
        "_id": "rec-2",
        "patient_id": "user-patient-1",
        "date": "2026-10-15",
        "title": "Type 2 Diabetes Routine Check & Metabolic Panel",
        "doctor_name": "Dr. Meera Nambiar",
        "specialty": "General Medicine",
        "hospital": "Fortis Hospital",
        "symptoms": ["Mild Afternoon Fatigue", "Increased Thirst"],
        "clinical_notes": "Follow-up metabolic assessment. FBS slightly elevated at 108 mg/dL with HbA1c at 6.4%. Reinforced carbohydrate restriction and daily 30-min brisk walking.",
        "prescriptions": ["Metformin 500mg SR"],
        "attachments": [
            {"filename": "Metabolic_Panel_Oct2026.pdf", "size": "840 KB", "type": "pdf"}
        ]
    },
    {
        "_id": "rec-3",
        "patient_id": "user-patient-1",
        "date": "2026-09-28",
        "title": "Acute Migraine & Tension Headache Review",
        "doctor_name": "Dr. Rajesh Sharma",
        "specialty": "Neurology",
        "hospital": "Manipal Hospital",
        "symptoms": ["Throbbing Left Frontal Pain", "Photophobia", "Computer Screen Sensitivity"],
        "clinical_notes": "Episodes triggered primarily by protracted screen exposure (>9 hours daily). Cranial nerve examination entirely intact. No focal neurological deficits. Brain MRI reviewed and confirmed normal.",
        "prescriptions": ["Rizatriptan 10mg PRN", "Magnesium Glycinate 400mg"],
        "attachments": [
            {"filename": "Brain_MRI_Report_Manipal.pdf", "size": "3.8 MB", "type": "pdf"}
        ]
    },
    {
        "_id": "rec-4",
        "patient_id": "user-patient-1",
        "date": "2026-08-10",
        "title": "Annual Comprehensive Health & Executive Checkup",
        "doctor_name": "Dr. Sarah Jenkins",
        "specialty": "General Medicine",
        "hospital": "MediVault Central Operations",
        "symptoms": ["Annual Preventive Screening"],
        "clinical_notes": "Comprehensive annual baseline physical. Vitals within anticipated parameters. Ultrasound whole abdomen unremarkable. Mild Vitamin D3 insufficiency flagged.",
        "prescriptions": ["Cholecalciferol 60k IU"],
        "attachments": [
            {"filename": "Executive_Health_Comprehensive_2026.pdf", "size": "5.1 MB", "type": "pdf"}
        ]
    }
]

INITIAL_NOTIFICATIONS = [
    {
        "_id": "notif-1",
        "user_id": "user-patient-1",
        "title": "Prescription Refill Due",
        "message": "Metformin 500mg refill is due in 5 days. Tap to request refill directly from pharmacy.",
        "type": "prescription",
        "time": "10 minutes ago",
        "is_read": False,
        "urgent": False
    },
    {
        "_id": "notif-2",
        "user_id": "user-patient-1",
        "title": "Critical Lab Result Flagged",
        "message": "Serum Potassium result flagged High (5.6 mEq/L). Immediate review recommended.",
        "type": "lab",
        "time": "2 hours ago",
        "is_read": False,
        "urgent": True
    },
    {
        "_id": "notif-3",
        "user_id": "user-patient-1",
        "title": "Appointment Tomorrow at 10:30 AM",
        "message": "Reminder: Routine Cardiology Follow-up with Dr. Arun Kumar at Apollo Specialty.",
        "type": "appointment",
        "time": "5 hours ago",
        "is_read": False,
        "urgent": False
    },
    {
        "_id": "notif-4",
        "user_id": "user-patient-1",
        "title": "Medical Record Added",
        "message": "Dr. Arun Kumar uploaded ECG trace and consultation notes from Oct 22 visit.",
        "type": "record",
        "time": "3 days ago",
        "is_read": True,
        "urgent": False
    }
]

INITIAL_VITALS = {
    "patient_id": "user-patient-1",
    "health_score": 78,
    "health_score_delta": "+4 vs last month",
    "health_status": "Moderate",
    "concerns_flagged": 2,
    "bp": "122/82",
    "bp_status": "Normal Controlled",
    "heart_rate": 72,
    "hr_status": "Normal Sinus",
    "glucose": 108,
    "glucose_status": "Pre-diabetic",
    "spo2": 99,
    "weight_kg": 64.5,
    "bmi": 22.8,
    "history": [
        {"date": "Oct 18", "bp_systolic": 132, "bp_diastolic": 86, "hr": 78, "glucose": 114},
        {"date": "Oct 20", "bp_systolic": 128, "bp_diastolic": 84, "hr": 75, "glucose": 110},
        {"date": "Oct 22", "bp_systolic": 124, "bp_diastolic": 82, "hr": 74, "glucose": 106},
        {"date": "Oct 24", "bp_systolic": 122, "bp_diastolic": 82, "hr": 72, "glucose": 108}
    ]
}

def seed_database(db):
    """Populates initial data if collections are empty."""
    # Check users
    if db["users"].count_documents() == 0:
        for u in DEMO_USERS:
            db["users"].insert_one(u)

    # Check doctors
    if db["doctors"].count_documents() == 0:
        for d in ALL_DOCTORS:
            db["doctors"].insert_one(d)

    # Check appointments
    if db["appointments"].count_documents() == 0:
        for a in INITIAL_APPOINTMENTS:
            db["appointments"].insert_one(a)

    # Check lab reports
    if db["lab_reports"].count_documents() == 0:
        for lr in INITIAL_LAB_REPORTS:
            db["lab_reports"].insert_one(lr)

    # Check prescriptions
    if db["prescriptions"].count_documents() == 0:
        for rx in INITIAL_PRESCRIPTIONS:
            db["prescriptions"].insert_one(rx)

    # Check medical records
    if db["medical_records"].count_documents() == 0:
        for rec in INITIAL_MEDICAL_RECORDS:
            db["medical_records"].insert_one(rec)

    # Check notifications
    if db["notifications"].count_documents() == 0:
        for n in INITIAL_NOTIFICATIONS:
            db["notifications"].insert_one(n)

    # Check vitals
    if db["vitals"].count_documents() == 0:
        db["vitals"].insert_one(INITIAL_VITALS)
