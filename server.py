import requests
import os
from flask import Flask, request

app = Flask(__name__)

# 🔹 Epic OAuth Details
CLIENT_ID = "04839623-912f-4e1a-9bfd-a09f529314a0"
TOKEN_URL = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"
REDIRECT_URI = "https://flask-oauth-app-1.onrender.com/callback"

@app.route("/")
def home():
    """Home route to verify server is running."""
    return "✅ Flask server is running on Render!", 200

@app.route("/callback")
def callback():
    """Handles Epic's OAuth redirect, extracts authorization code, and requests access token."""
    auth_code = request.args.get('code')
    if not auth_code:
        print("❌ No authorization code received!")
        return "❌ No authorization code received!", 400

    print(f"✅ Authorization Code Received: {auth_code}")

    # 🔹 List all files in directory before saving token
    print(f"📂 Current directory: {os.getcwd()}")
    print(f"📁 Files before saving token: {os.listdir(os.getcwd())}")

    # 🔹 Exchange Authorization Code for Access Token
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID
    }

    response = requests.post(TOKEN_URL, data=data)

    print(f"📩 Epic Response Status Code: {response.status_code}")
    print(f"📜 Epic Response: {response.text}")

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print(f"✅ Access Token Obtained: {access_token}")

        # 🔹 Ensure token.txt is saved in the right location
        save_path = os.path.join(os.getcwd(), "token.txt")
        try:
            with open(save_path, "w") as f:
                f.write(access_token)
            print(f"✅ Token successfully saved to: {save_path}")

            # 🔹 List files after saving token to confirm it was written
            print(f"📁 Files after saving token: {os.listdir(os.getcwd())}")

        except Exception as e:
            print(f"❌ Failed to save token.txt: {e}")

        return "✅ Access Token Obtained Successfully! You can close this window.", 200
    else:
        print(f"❌ Token Exchange Failed: {response.json()}")
        return "❌ Token Exchange Failed!", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render assigns a dynamic port
    app.run(host="0.0.0.0", port=port)
