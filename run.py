import os
import sys

# Ensure app package is in python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"Starting MediVault Flask API Server on http://127.0.0.1:{port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
