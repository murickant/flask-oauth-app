import requests
import sys

# Your Epic app credentials (Public Client: no client_secret)
client_id = "04839623-912f-4e1a-9bfd-a09f529314a0"
redirect_uri = "https://flask-oauth-app-1.onrender.com/callback"
token_url = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"

# Read authorization code from file
try:
    with open("auth_code.txt", "r") as file:
        authorization_code = file.read().strip()
except FileNotFoundError:
    print("\n❌ Error: Could not find `auth_code.txt`. Please create the file and paste the authorization code inside.")
    sys.exit(1)

print(f"\n🔍 Using Authorization Code (truncated): {authorization_code[:50]}...")

# Correct OAuth Token Request Data (no client secret)
data = {
    "grant_type": "authorization_code",
    "code": authorization_code,
    "redirect_uri": redirect_uri,
    "client_id": client_id  # Only client_id, no client_secret
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

print("\n🚀 Sending request to Epic for Access Token (Public Client)...")

# Send POST request
try:
    response = requests.post(token_url, headers=headers, data=data, timeout=10)  # ✅ No need for urlencode()
except requests.exceptions.RequestException as e:
    print(f"\n❌ Request failed: {e}")
    sys.exit(1)

# Output response
print(f"\n📩 Epic Response Status Code: {response.status_code}")
print(f"📜 Epic Response Text: {response.text}")

# Handle response
if response.status_code == 200:
    token_info = response.json()
    print("\n✅ Access Token Received!")
    print(f"🔓 Access Token: {token_info.get('access_token')}")
    print(f"⏳ Expires In: {token_info.get('expires_in')} seconds")
else:
    print("\n❌ Failed to obtain token")
    print(f"❗ Status Code: {response.status_code}")
    print(f"📩 Response: {response.text}")
