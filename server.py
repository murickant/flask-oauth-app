from flask import Flask, request
import urllib.parse

app = Flask(__name__)

@app.route('/callback')
def callback():
    auth_code = request.args.get('code')

    if not auth_code:
        return "❌ No authorization code received!", 400

    # Decode the authorization code
    decoded_auth_code = urllib.parse.unquote(auth_code)

    # Debugging: Print extracted and decoded auth code
    print(f"\n🔍 Raw Authorization Code: {auth_code}")
    print(f"🔍 Decoded Authorization Code: {decoded_auth_code}")
    print(f"🔢 Length: {len(decoded_auth_code)} characters")

    return f"✅ Authorization Code: {decoded_auth_code}", 200

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), port=3000, host='127.0.0.1')
