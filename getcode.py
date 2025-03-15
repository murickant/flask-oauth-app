import requests
import webbrowser
from urllib.parse import urlencode, quote_plus

# Your Epic app credentials
client_id = "a78d1978-706d-46f9-8ebd-e8eb64e675d9"
redirect_uri = "https://flask-oauth-app-1.onrender.com/callback"  # Must match EXACTLY with Epic's registration

auth_url = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/authorize"

params = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": redirect_uri,  
    "scope": "patient.read",
    "state": "randomstring123"  # Used for security
}

# Construct full authorization URL
full_auth_url = f"{auth_url}?{urlencode(params)}"

# Open browser for user login
print(f"➡️ Open this URL in your browser and log in to authorize:\n{full_auth_url}")
webbrowser.open(full_auth_url)

print("\n📩 After logging in, Epic should redirect you to your registered callback URL.")
print("✅ Check your browser's address bar for `?code=...` and copy that value.")
print("👉 Paste it into `auth_code.txt` before running `process_auth_code.py`")
