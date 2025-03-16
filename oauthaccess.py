import requests

# 🔹 Set your Flask server URL on Render
FLASK_SERVER_URL = "https://flask-oauth-app-1.onrender.com"

# 🔹 Fetch token from Flask server
def get_access_token():
    """Fetch the access token from the Flask server."""
    try:
        response = requests.get(f"{FLASK_SERVER_URL}/get_token")

        if response.status_code == 200:
            access_token = response.json().get("access_token")
            if access_token:
                print(f"✅ Access Token Retrieved: {access_token}")
                return access_token
            else:
                print("❌ No access token found in response.")
        else:
            print(f"❌ Failed to retrieve token. Server Response: {response.text}")
    except Exception as e:
        print(f"🚨 Error: {e}")

    return None

# 🔹 Test API Call Using the Token
def test_api_call():
    access_token = get_access_token()
    if not access_token:
        print("❌ No access token available. Exiting.")
        return

    # 🔹 Epic FHIR API Endpoint
    FHIR_API_URL = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Patient"

    # 🔹 Set Headers with Bearer Token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/fhir+json"
    }

    # 🔹 Make API Request
    response = requests.get(FHIR_API_URL, headers=headers)

    if response.status_code == 200:
        print("✅ API Request Successful:", response.json())
    else:
        print(f"❌ API Request Failed! Status Code: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    test_api_call()
