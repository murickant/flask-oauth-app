import requests
import os
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔹 Epic OAuth Details
CLIENT_ID = "04839623-912f-4e1a-9bfd-a09f529314a0"
TOKEN_URL = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"
REDIRECT_URI = "https://flask-oauth-app-1.onrender.com/callback"

@app.route("/")
def home():
    """Home route to verify server is running."""
    print("✅ Flask server home route accessed.", file=sys.stdout)
    return "✅ Flask server is running on Render!", 200

@app.route("/callback", methods=["GET"])
def callback():
    """Handles Epic's OAuth redirect, extracts authorization code, and exchanges it for an access token."""

    print("🔹 Callback route accessed.", file=sys.stdout)
    print(f"🔍 Full Request URL: {request.url}", file=sys.stdout)
    print(f"🔍 Full Request Params: {request.args}", file=sys.stdout)

    auth_code = request.args.get('code')
    if not auth_code:
        print("❌ No authorization code received!", file=sys.stdout)
        return "❌ No authorization code received!", 400

    print(f"✅ Authorization Code Received: {auth_code}", file=sys.stdout)

    try:
        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID
        }

        print("🔹 Sending request to Epic for token exchange...", file=sys.stdout)
        response = requests.post(TOKEN_URL, data=data)

        print(f"📩 Epic Response Status Code: {response.status_code}", file=sys.stdout)
        print(f"📜 Epic Response: {response.text}", file=sys.stdout)

        if response.status_code == 200:
            access_token = response.json().get("access_token")
            print(f"✅ Access Token Obtained: {access_token}", file=sys.stdout)

            # Save token to a file in Render
            save_path = os.path.join(os.getcwd(), "token.txt")
            try:
                with open(save_path, "w") as f:
                    f.write(access_token)
                print(f"✅ Token successfully saved to: {save_path}", file=sys.stdout)
            except Exception as e:
                print(f"❌ Failed to save token.txt: {e}", file=sys.stdout)

            return jsonify({"message": "✅ Access Token Obtained!", "access_token": access_token}), 200
        else:
            print(f"❌ Token Exchange Failed: {response.json()}", file=sys.stdout)
            return jsonify({"error": "Token Exchange Failed", "details": response.json()}), 400

    except Exception as e:
        print(f"🚨 ERROR: {e}", file=sys.stdout)
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/get_token", methods=["GET"])
def get_token():
    """Serve the stored access token."""
    save_path = os.path.join(os.getcwd(), "token.txt")
    
    if os.path.exists(save_path):
        with open(save_path, "r") as f:
            access_token = f.read().strip()
        print(f"✅ Token retrieved from server: {access_token[:30]}... (truncated)", file=sys.stdout)
        return jsonify({"access_token": access_token}), 200
    else:
        print("❌ No token file found on server.", file=sys.stdout)
        return jsonify({"error": "No token available"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render assigns a dynamic port
    print(f"🚀 Starting Flask server on port {port}...", file=sys.stdout)
    app.run(host="0.0.0.0", port=port, debug=True)
