from flask import Flask, request
import requests
import os
import logging
import sys

app = Flask(__name__)

# Log directory setup
log_dir = os.environ.get("LOG_DIR", "/logs")
os.makedirs(log_dir, exist_ok=True)

# Logging configuration: hem dosyaya hem stdout'a log yaz
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "duplicator.log")),
        logging.StreamHandler(sys.stdout)
    ]
)

# Read targets from environment
TARGET1 = os.environ.get("TARGET1")
TARGET2 = os.environ.get("TARGET2")

if not TARGET1 or not TARGET2:
    logging.error("❌ TARGET1 and TARGET2 environment variables must be set.")
    exit(1)

# Read timeout from environment
try:
    FORWARD_TIMEOUT = int(os.environ.get("FORWARD_TIMEOUT", "5"))
except ValueError:
    logging.warning("⚠️ Invalid FORWARD_TIMEOUT value, using default of 5 seconds.")
    FORWARD_TIMEOUT = 5

@app.route('/healthz', methods=['GET'])
def health_check():
    return "OK", 200

@app.route('/', methods=['POST'])
def handle_request():
    data = request.get_data()
    headers = {k: v for k, v in request.headers.items() if k.lower() != 'host'}

    logging.info(f"📥 Method: {request.method}, Headers: {headers}, Data: {data.decode('utf-8')}")

    responses = []

    for target in [TARGET1, TARGET2]:
        try:
            response = requests.post(
                target,
                data=data,
                headers=headers,
                timeout=FORWARD_TIMEOUT,
                verify=True
            )
            responses.append((target, response.status_code, response.text))
            logging.info(f"✅ Sent to {target} with status {response.status_code}")
        except Exception as e:
            responses.append((target, None, str(e)))
            logging.error(f"❌ Error sending to {target}: {e}")

    # Return success if any target returned 200
    for target, status, body in responses:
        if status == 200:
            return f"✅ Forwarded successfully to {target}", 200

    # If all failed
    return f"❌ Forwarding failed: {responses}", 502

if __name__ == '__main__':
    listen_port = int(os.environ.get("LISTEN_PORT", "6000"))
    logging.info(f"🚀 Starting duplicator on port {listen_port}")
    app.run(host="0.0.0.0", port=listen_port)
