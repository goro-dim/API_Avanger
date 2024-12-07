from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='api_requests.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Mock database of credentials
VALID_CREDENTIALS = {
    "admin": "admin123",
    "user": "pass123",
    "guest": "guest123",
}

@app.before_request
def log_request_info():
    # Log incoming request data
    log_data = {
        "path": request.path,
        "method": request.method,
        "ip": request.remote_addr,
        "data": request.get_data(as_text=True),
        "content_length": request.content_length,
    }
    app.logger.info(log_data)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to API Avenger! Use /login or /data for interaction."})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Invalid input"}), 400

    username = data["username"]
    password = data["password"]

    if VALID_CREDENTIALS.get(username) == password:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify({"data": "Sensitive information"}), 200

if __name__ == '__main__':
    app.run(debug=True)
