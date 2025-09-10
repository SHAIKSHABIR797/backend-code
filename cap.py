from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("SUPABASE_URL:", SUPABASE_URL)
print("SUPABASE_KEY:", SUPABASE_KEY[:10] if SUPABASE_KEY else None)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
CORS(app)  # <-- allow requests from your frontend

@app.route("/")
def index():
    return "Backend is running 🚀", 200

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
