import requests
import webbrowser
from urllib.parse import urlencode, quote_plus

# Your Epic app credentials
client_id = "a78d1978-706d-46f9-8ebd-e8eb64e675d9"
client_secret = "RPV3Yr/6ngcxSg2UJHvvVbMTY0wK43s7JtN/PszPv8GeIaTofbrkXhZYM+sYoWDm30rlo5/bKLAE5+iI37mSiQ=="
redirect_uri = "https://1a0b-2601-547-c701-efc0-348c-1f24-9125-cd06.ngrok-free.app"  # Must match exactly with Epic's registration

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

# Step 2: Get Authorization Code (User must copy from the browser URL)
authorization_code = input("\n🔑 Paste the authorization code from the redirect URL: ").strip()

# Step 3: Exchange Authorization Code for Access Token
token_url = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

data = {
    "grant_type": "authorization_code",
    "code": authorization_code,
    "redirect_uri": redirect_uri  # Must match exactly
}

# Send request with Basic Authentication
response = requests.post(token_url, auth=(client_id, client_secret), headers=headers, data=data)

# Step 4: Handle the Response
if response.status_code == 200:
    token_info = response.json()
    print("\n✅ Access Token Received!")
    print(f"🔓 Access Token: {token_info.get('access_token')}")
    print(f"⏳ Expires In: {token_info.get('expires_in')} seconds")
else:
    print("\n❌ Failed to obtain token")
    print(f"❗ Status Code: {response.status_code}")
    print(f"📩 Response: {response.text}")
