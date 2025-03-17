import json
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Import CORS

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for frontend requests

# ✅ Render PostgreSQL Connection Details
DB_CONFIG = {
    "dbname": "epic_mvp",
    "user": "epic_mvp_user",  
    "password": "YQKJzPMVFUHCqYkdVeom8SI4aCEHatLh",
    "host": "dpg-cvbo45tds78s73an1fvg-a.virginia-postgres.render.com",
    "port": "5432"
}

def connect_db():
    """Connects to PostgreSQL database and prints error if fails."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return None

def setup_database():
    """Ensures required tables exist."""
    conn = connect_db()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS access_tokens (
                id SERIAL PRIMARY KEY,
                token TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id SERIAL PRIMARY KEY,
                mrn TEXT UNIQUE NOT NULL,
                data JSONB,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        conn.commit()
        conn.close()
        print("✅ PostgreSQL tables 'access_tokens' and 'patients' are ready!")
    except Exception as e:
        print(f"❌ Database setup error: {e}")

def save_token_to_db(access_token):
    """Saves the access token to PostgreSQL and prints debug messages."""
    conn = connect_db()
    if not conn:
        print("❌ No database connection. Token not saved.")
        return

    try:
        print(f"📝 Saving token to database: {access_token[:10]}... (truncated)")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO access_tokens (token) VALUES (%s);", (access_token,))
        conn.commit()
        conn.close()
        print(f"✅ Access Token Successfully Saved: {access_token[:10]}... (truncated)")
    except Exception as e:
        print(f"❌ Failed to save token to database: {e}")

@app.route('/callback')
def callback():
    """Handles Epic OAuth callback and saves token to PostgreSQL."""
    print(f"🔍 Full request args: {request.args}")

    auth_code = request.args.get('code')
    if not auth_code:
        print("❌ Authorization code missing!")
        return "❌ Authorization code missing!", 400

    print(f"✅ Received Authorization Code: {auth_code}")

    # Exchange authorization code for access token
    access_token = exchange_for_access_token(auth_code)
    if not access_token:
        print("❌ Failed to obtain access token!")
        return "❌ Failed to obtain access token!", 400

    print(f"🔑 Access Token Received: {access_token[:10]}... (truncated)")

    # ✅ Ensure database is ready and save token
    setup_database()
    save_token_to_db(access_token)

    return "✅ Access Token Obtained Successfully! You can close this window."

def exchange_for_access_token(auth_code):
    """Sends request to Epic to exchange auth code for access token."""
    import requests

    TOKEN_URL = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"
    CLIENT_ID = "04839623-912f-4e1a-9bfd-a09f529314a0"
    REDIRECT_URI = "https://flask-oauth-app-1.onrender.com/callback"

    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID
    }

    response = requests.post(TOKEN_URL, data=data)
    
    try:
        response_json = response.json()
    except json.JSONDecodeError:
        print(f"❌ Epic returned an invalid response: {response.text}")
        return None

    if response.status_code == 200:
        print(f"✅ Successfully obtained token: {response_json}")
        return response_json.get("access_token")
    else:
        print(f"❌ Error exchanging token: {response_json}")
        return None

@app.route('/patients', methods=['GET'])
def get_patients():
    """Fetches stored patient data from PostgreSQL for frontend display."""
    conn = connect_db()
    if not conn:
        return jsonify({"error": "❌ Database connection failed!"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT mrn, data FROM patients;")
        patients = [{"mrn": row[0], "data": row[1]} for row in cursor.fetchall()]
        conn.close()
        
        if not patients:
            return jsonify({"message": "No patient data found!"}), 200
        
        return jsonify(patients)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    setup_database()
    app.run(host="0.0.0.0", port=5000, debug=True)
