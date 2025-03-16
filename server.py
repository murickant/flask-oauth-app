import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/callback')
def callback():
    """Handles Epic OAuth callback, extracts authorization code, and exchanges for access token."""
    auth_code = request.args.get('code')
    if not auth_code:
        return "❌ Authorization code missing!", 400

    print(f"✅ Received Authorization Code: {auth_code}")

    # Exchange authorization code for access token
    access_token = exchange_for_access_token(auth_code)
    if not access_token:
        return "❌ Failed to obtain access token!", 400

    # ✅ Save access token to file
    with open("token.txt", "w") as file:
        json.dump({"access_token": access_token}, file)

    print("✅ Access Token Saved!")
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
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"❌ Error exchanging token: {response.json()}")
        return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
