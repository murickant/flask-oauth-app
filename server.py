import requests
import os
import sys  # Ensure logs are written to stdout
from flask import Flask, request

app = Flask(__name__)

# 🔹 Force all logs to be printed in Render
print("🚀 Flask Server Starting...", file=sys.stdout)

# 🔹 Epic OAuth Details
CLIENT_ID = "04839623-912f-4e1a-9bfd-a09f529314a0"
TOKEN_URL = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"
REDIRECT_URI = "https://flask-oauth-app-1.onrender.com/callback"

@app.route("/")
def home():
    """Home route to verify server is running."""
    print("✅ Flask server home route accessed.", file=sys.stdout)
    return "✅ Flask server is running on Render!", 200

@app.route("/callback")
def callback():
    """Handles Epic's OAuth redirect, extracts authorization code, and requests access token."""
    
    print("🔹 Callback route accessed.", file=sys.stdout)

    # Print full request URL for debugging
    full_request_url = request.url
    print(f"🔍 Full Request URL: {full_request_url}", file=sys.stdout)

    # Extract the authorization code from the URL
    auth_code = request.args.get('code')

    if not auth_code:
        print("❌ No authorization code received!", file=sys.stdout)
        return "❌ No authorization code received!", 400

    print(f"✅ Authorization Code Received: {auth_code}", file=sys.stdout)

    return "✅ Authorization Code Captured! Check Render logs.", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render assigns a dynamic port
    print(f"🚀 Starting Flask server on port {port}...", file=sys.stdout)
    app.run(host="0.0.0.0", port=port, debug=True)
