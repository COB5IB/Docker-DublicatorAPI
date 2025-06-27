from flask import Flask, request
import requests
import os
import logging

app = Flask(__name__)

# Log directory setup
log_dir = os.environ.get("LOG_DIR", "/logs")
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "duplicator.log"),
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# Read targets from environment
TARGET1 = os.environ.get("TARGET1")
TARGET2 = os.environ.get("TARGET2")

@app.route('/healthz', methods=['GET'])
def health_check():
    return "OK", 200

@app.route('/', methods=['POST'])
def handle_request():
    data = request.get_data()
    headers = {k: v for k, v in request.headers.items() if k.lower() != 'host'}

    logging.info(f"📥 Incoming data: {data.decode('utf-8')}")

    responses = []

    for target in [TARGET1, TARGET2]:
        try:
            response = requests.post(target, data=data, headers=headers, timeout=5, verify=True)
            responses.append((target, response.status_code))
            logging.info(f"✅ Sent to {target} with status {response.status_code}")
        except Exception as e:
            responses.append((target, str(e)))
            logging.error(f"❌ Error sending to {target}: {e}")

    # Return one of the responses or a failure message
    for _, r in responses:
        if isinstance(r, int) and r == 200:
            return "Forwarded successfully", 200

    return "Forwarding failed", 502

if __name__ == '__main__':
    listen_port = int(os.environ.get("LISTEN_PORT", "5000"))
    app.run(host="0.0.0.0", port=listen_port)


