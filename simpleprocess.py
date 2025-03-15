import requests
import sys
import urllib.parse

# Your Epic app credentials
client_id = "04839623-912f-4e1a-9bfd-a09f529314a0"
redirect_uri = "https://flask-oauth-app-1.onrender.com/callback"
token_url = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"

# Read authorization code from file
try:
    with open("auth_code.txt", "r") as file:
        authorization_code = file.read().strip()
except FileNotFoundError:
    print("\n❌ Error: Could not find `auth_code.txt`. Ensure you paste the full code.")
    sys.exit(1)

# Debugging: Print authorization code before sending request
print(f"\n🔍 Authorization Code Length: {len(authorization_code)} characters")
print(f"🔍 First 50 chars: {authorization_code[:50]}...")
print(f"🔍 Last 50 chars: {authorization_code[-50:]}...")

# Ensure the code is NOT encoded
authorization_code = urllib.parse.unquote(authorization_code)

# Construct the request payload
data = {
    "grant_type": "authorization_code",
    "code": authorization_code,
    "redirect_uri": redirect_uri,
    "client_id": client_id
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

print("\n🚀 Sending request to Epic for Access Token (Public Client)...")
print(f"🔹 Token URL: {token_url}")
print(f"🔹 Redirect URI: {redirect_uri}")
print(f"🔹 Sending Authorization Code: {authorization_code}")

# Send the token request
response = requests.post(token_url, headers=headers, data=data)

# Print the response
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
