from flask import Flask, request, jsonify, render_template
from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables from .env locally (ignored on Render)
load_dotenv()

# ✅ Use environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# 🔍 Debug: Confirm variables (remove for production)
print("SUPABASE_URL:", SUPABASE_URL)
print("SUPABASE_KEY:", SUPABASE_KEY[:10] if SUPABASE_KEY else None)

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

# --------- Routes ---------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/events", methods=["GET"])
def get_events():
    response = supabase.table("events").select("*").execute()
    return jsonify(response.data), 200

@app.route("/events", methods=["POST"])
def create_event():
    data = request.json
    if not data.get("event_name") or not data.get("event_date"):
        return jsonify({"error": "event_name and event_date are required"}), 400
    response = supabase.table("events").insert(data).execute()
    return jsonify(response.data), 201

@app.route("/register", methods=["POST"])
def register_event():
    data = request.json
    if not data.get("event_id") or not data.get("username"):
        return jsonify({"error": "event_id and username are required"}), 400
    response = supabase.table("registrations").insert(data).execute()
    return jsonify(response.data), 201

@app.route("/registrations/<int:event_id>", methods=["GET"])
def get_registrations(event_id):
    response = supabase.table("registrations").select("*").eq("event_id", event_id).execute()
    return jsonify(response.data), 200

# ✅ Ready for Render / Gunicorn
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
