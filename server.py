from flask import Flask, request

app = Flask(__name__)

@app.route('/callback')
def callback():
    auth_code = request.args.get('code')
    return f"✅ Authorization Code: {auth_code}", 200

if __name__ == '__main__':
    app.run(port=3000, host='0.0.0.0')  # REMOVE ssl_context
