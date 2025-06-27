import os
import logging
import requests
from flask import Flask, request, Response
from urllib.parse import urljoin

# Disable proxy if defined in environment
for var in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"]:
    os.environ.pop(var, None)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# Environment vars
TARGET1 = os.environ.get("TARGET1")
TARGET2 = os.environ.get("TARGET2")
LISTEN_PORT = int(os.environ.get("LISTEN_PORT", 6000))
FORWARD_TIMEOUT = int(os.environ.get("FORWARD_TIMEOUT", 5))
AUTH_USERNAME = os.environ.get("AUTH_USERNAME")
AUTH_PASSWORD = os.environ.get("AUTH_PASSWORD")
VERIFY_SSL = os.environ.get("VERIFY_SSL", "false").lower() == "true"

# Flask app
app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['POST'])
@app.route('/<path:path>', methods=['POST'])
def handle_request(path):
    data = request.get_data()
    headers = {k: v for k, v in request.headers.items() if k.lower() != 'host'}

    # Full path with optional query string
    full_path = request.full_path if request.query_string else f'/{path}'

    logging.info(f"📥 Method: {request.method}, Path: {full_path}, Data: {data.decode('utf-8', 'ignore')}")
    responses = []

    for target in filter(None, [TARGET1, TARGET2]):
        try:
            target_url = urljoin(target, full_path)
            response = requests.post(
                target_url,
                headers=headers,
                data=data,
                auth=(AUTH_USERNAME, AUTH_PASSWORD),
                timeout=FORWARD_TIMEOUT,
                verify=VERIFY_SSL,
                proxies={}  # Proxy devre dışı bırakıldı
            )
            responses.append((target_url, response.status_code))
            logging.info(f"✅ Sent to {target_url} with status {response.status_code}")

            # İlk başarılı yanıttan dön
            if response.status_code < 400:
                content_type = response.headers.get("Content-Type", "")
                if "xml" in content_type.lower():
                    return Response(response.content, status=response.status_code, content_type=content_type)
                else:
                    logging.warning(f"⚠️ Non-XML response from {target_url}: {content_type}")
                    return Response(response.text, status=response.status_code, content_type=content_type or "text/plain")

        except Exception as e:
            responses.append((target, str(e)))
            logging.error(f"❌ Error sending to {target}: {e}")

    return f"❌ Forwarding failed: {responses}", 502

@app.route('/healthz', methods=['GET'])
def healthz():
    return "OK", 200

if __name__ == "__main__":
    logging.info(f"🚀 Starting duplicator on port {LISTEN_PORT}")
    app.run(host="0.0.0.0", port=LISTEN_PORT)
