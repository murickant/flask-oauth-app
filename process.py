import requests
import sys
import base64
from urllib.parse import urlencode

# Your Epic app credentials
client_id = "a78d1978-706d-46f9-8ebd-e8eb64e675d9"
client_secret = "RPV3Yr/6ngcxSg2UJHvvVbMTY0wK43s7JtN/PszPv8GeIaTofbrkXhZYM+sYoWDm30rlo5/bKLAE5+iI37mSiQ=="
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
print(f"🔢 Code Length: {len(authorization_code)} characters")

# POST body: only these 3 parameters
data = {
    "grant_type": "authorization_code",
    "code": authorization_code,
    "redirect_uri": redirect_uri
}
encoded_data = urlencode(data)

# Base64-encode "client_id:client_secret"
credentials = f"{client_id}:{client_secret}".encode("utf-8")
encoded_credentials = base64.b64encode(credentials).decode("utf-8")

# Epic requires this header format for confidential clients
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {encoded_credentials}"
}

print("\n🚀 Sending request to Epic for Access Token...")
print(f"🔹 Token URL: {token_url}")
print(f"🔹 Headers: {headers}")
print(f"🔹 Encoded Body: {encoded_data}")

try:
    response = requests.post(token_url, headers=headers, data=encoded_data, timeout=10)
except requests.exceptions.RequestException as e:
    print(f"\n❌ Request failed: {e}")
    sys.exit(1)

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
