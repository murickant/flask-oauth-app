import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/callback')
def callback():
    """Handles Epic OAuth callback, extracts authorization code, and exchanges for access token."""
    print(f"🔍 Full request args: {request.args}")  # ✅ Debugging line

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

    print(f"🔑 Access Token Received: {access_token}")  # ✅ Debugging line

    # ✅ Save access token to file
    try:
        with open("token.txt", "w") as file:
            json.dump({"access_token": access_token}, file)
        print("✅ Access Token Saved to token.txt!")
    except Exception as e:
        print(f"❌ Failed to save token: {e}")
        return "❌ Error saving access token!", 500

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
    
    # ✅ Log the full response from Epic
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
