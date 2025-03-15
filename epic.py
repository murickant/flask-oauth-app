import requests
import webbrowser
import sys
from urllib.parse import urlencode, quote_plus

# Your Epic app credentials
client_id = "a78d1978-706d-46f9-8ebd-e8eb64e675d9"
client_secret = "RPV3Yr/6ngcxSg2UJHvvVbMTY0wK43s7JtN/PszPv8GeIaTofbrkXhZYM+sYoWDm30rlo5/bKLAE5+iI37mSiQ=="
redirect_uri = "https://flask-oauth-app-1.onrender.com/callback"  # Must match exactly with Epic's registration

# Ensure redirect_uri is properly URL-encoded
encoded_redirect_uri = quote_plus(redirect_uri)

# Step 1: Generate the Authorization URL
auth_url = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/authorize"

params = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": redirect_uri,  # Epic requires the original URI, not encoded here
    "scope": "patient.read",
    "state": "randomstring123"  # Used for security
}

# Construct full authorization URL
full_auth_url = f"{auth_url}?{urlencode(params)}"

# Open browser for user login
print(f"➡️ Open this URL in your browser and log in to authorize:\n{full_auth_url}")
webbrowser.open(full_auth_url)

# Step 2: Get Authorization Code from File
print("\n📩 Awaiting authorization code...")
try:
    with open("auth_code.txt", "r") as file:
        authorization_code = file.read().strip()
except FileNotFoundError:
    print("\n❌ Error: Could not find auth_code.txt. Please create the file and paste the authorization code inside.")
    sys.exit(1)

# 🔥 Debugging: Print input length and detect hidden issues
print(f"\n🔍 Debug: Captured Authorization Code ({len(authorization_code)} characters) → {authorization_code[:50]}...")

# Step 3: Exchange Authorization Code for Access Token
token_url = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

data = {
    "grant_type": "authorization_code",
    "code": authorization_code,
    "redirect_uri": redirect_uri,  # Must match exactly
    "client_id": client_id,  # 🔥 Fix: Epic requires these in the body
    "client_secret": client_secret
}

# 🔥 Debug: Print request data before sending
print("\n🚀 Sending request to Epic's token endpoint...")
print(f"🔹 Token URL: {token_url}")
print(f"🔹 Headers: {headers}")

# Send request to Epic for Access Token
try:
    response = requests.post(token_url, headers=headers, data=data, timeout=10)  # Add timeout
except requests.exceptions.RequestException as e:
    print(f"\n❌ Request failed: {e}")
    sys.exit(1)

# Step 4: Handle the Response
print(f"\n📩 Epic Response Status Code: {response.status_code}")
print(f"📜 Epic Response Text: {response.text}")

if response.status_code == 200:
    token_info = response.json()
    print("\n✅ Access Token Received!")
    print(f"🔓 Access Token: {token_info.get('access_token')}")
    print(f"⏳ Expires In: {token_info.get('expires_in')} seconds")
else:
    print("\n❌ Failed to obtain token")
    print(f"❗ Status Code: {response.status_code}")
    print(f"📩 Response: {response.text}")
