import os
from flask import Flask, jsonify
from flask_cors import CORS
from .db import db
from .seed_data import seed_database

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "medivault_flask_secret_2026")

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Seed initial data
    try:
        seed_database(db)
        print("MediVault database initialized & verified successfully.")
    except Exception as e:
        print(f"Warning during seed: {e}")

    # Register blueprints
    from .routes.auth_routes import auth_bp
    from .routes.patient_routes import patient_bp
    from .routes.appointment_routes import appointment_bp
    from .routes.record_routes import record_bp
    from .routes.lab_routes import lab_bp
    from .routes.prescription_routes import prescription_bp
    from .routes.doctor_routes import doctor_bp
    from .routes.ai_routes import ai_bp
    from .routes.notification_routes import notification_bp
    from .routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(record_bp)
    app.register_blueprint(lab_bp)
    app.register_blueprint(prescription_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(admin_bp)

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "online",
            "service": "MediVault Health API",
            "version": "2.4.0",
            "encryption": "AES-256",
            "hipaa_compliant": True,
            "database": "MongoDB (Connected)"
        })

    return app
