import logging
logging.basicConfig(level=logging.INFO)
from threading import Lock
from flask import Flask, request, abort
import hmac
import hashlib
import base64
import json
import os
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO)

load_dotenv()
SECRET_KEY = os.getenv("WEBHOOK_SECRET_KEY")

PROCESSED_IDS_FILE = "processed_ids.json"
LATEST_DATA_FILE = "latest_data.json"

processed_ids_lock = Lock()
latest_data_lock = Lock()

processed_ids = set()

# Load processed message IDs from file
if os.path.exists(PROCESSED_IDS_FILE):
    with open(PROCESSED_IDS_FILE, "r") as f:
        processed_ids = set(json.load(f))
else:
    processed_ids = set()

app = Flask(__name__)


def verify_signature(payload, signature, nonce):
    key = (SECRET_KEY + nonce).encode('utf-8')
    computed_hmac = hmac.new(key, payload, hashlib.sha256).digest()
    computed_signature = base64.b64encode(computed_hmac).decode()
    return hmac.compare_digest(computed_signature, signature)

def handle_webhook(payload):
    global processed_ids
    message_id = payload.get("messageId")
    if not message_id:
        logging.info("No messageId found, skipping.")
        return

    with processed_ids_lock:
        if message_id in processed_ids:
            logging.info(f"Duplicate message {message_id}, skipping.")
            return

        logging.info(f"Processing new message {message_id}")
        processed_ids.add(message_id)

        # Limit to last 500 entries
        if len(processed_ids) > 500:
            processed_ids_list = list(processed_ids)[-500:]
            processed_ids = set(processed_ids_list)
        else:
            processed_ids_list = list(processed_ids)

        # Save processed IDs
        with open("processed_ids.json", "w") as f:
            json.dump(processed_ids_list, f)
               

    # Save latest data
    with latest_data_lock:
        with open("latest_data.json", "w") as f:
            json.dump(payload, f, indent=2)
        logging.info("Saved data to latest_data.json")

@app.route('/webhook', methods=['POST'])
def webhook():
    logging.info("Webhook endpoint hit")
    payload = request.data
    logging.info(f"Raw payload: {payload}")
    try:
        data = json.loads(payload)
        logging.info(f"Parsed JSON: {data}")
        handle_webhook(data)
        return '', 200
    except Exception as e:
        logging.error(f"Error parsing JSON: {e}")
        abort(500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)