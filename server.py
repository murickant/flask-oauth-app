import requests
from flask import Flask, request

app = Flask(__name__)

# 🔹 Epic OAuth Details
CLIENT_ID = "04839623-912f-4e1a-9bfd-a09f529314a0"
TOKEN_URL = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"
REDIRECT_URI = "https://flask-oauth-app-1.onrender.com/callback"

ACCESS_TOKEN = None  # Store token globally (or save to a database/file)

@app.route('/callback')
def callback():
    """Handles Epic's OAuth redirect, extracts authorization code, and requests access token."""
    global ACCESS_TOKEN
    auth_code = request.args.get('code')
    print(f"✅ Authorization Code Received: {auth_code}")

    # Exchange authorization code for access token
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID
    }
    response = requests.post(TOKEN_URL, data=data)
    
    if response.status_code == 200:
        ACCESS_TOKEN = response.json()["access_token"]
        print(f"✅ Access Token Obtained: {ACCESS_TOKEN}")
        return "Access Token Obtained Successfully! You can close this window.", 200
    else:
        print(f"❌ Token Exchange Failed: {response.json()}")
        return "Token Exchange Failed", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Render will handle deployment
