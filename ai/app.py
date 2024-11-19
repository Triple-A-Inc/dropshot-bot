import os
import logging
from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
from graph import run_vendor_inference, vendor  # Import your graph functions
import requests
from collections import deque

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)
JIVOCHAT_TOKEN = os.getenv("JIVOCHAT_TOKEN")
PROVIDER_ID = os.getenv("PROVIDER_ID")
JIVOCHAT_RESPONSE_URL = f"https://bot.jivosite.com/webhooks/{PROVIDER_ID}/{JIVOCHAT_TOKEN}"
JIVOCHAT_URL_ENDPOINT = f"/webhook/{JIVOCHAT_TOKEN}"

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Configure console logging
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def send_response_to_jivo(response):
    requests.post(JIVOCHAT_RESPONSE_URL, json=response)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route(JIVOCHAT_URL_ENDPOINT, methods=['POST'])
def webhook():
    logger.info("Webhook endpoint triggered.")

    # Step 2: Process the incoming JivoChat event
    data = request.get_json()
    event_type = data.get("event", "UNKNOWN")
    logger.info(f"Received event type: {event_type}")

    if event_type == "CLIENT_MESSAGE":
        client_id = data.get("client_id", "UNKNOWN")
        message = data.get("message", {}).get("text", "")
        logger.info(f"Processing CLIENT_MESSAGE from client_id={client_id}: {message}")

        try:
            # Step 3: Run vendor inference
            logger.info(f"Running inference for client_id={client_id}...")
            response_text = run_vendor_inference(vendor, message, client_id)

            if response_text.strip() == 'INVITE_AGENT':
                logger.info(f"AI requested to escalate to a human agent for client_id={client_id}.")
                return jsonify({
                    "id": data["id"],
                    "client_id": client_id,
                    "chat_id": data["chat_id"],
                    "event": "INVITE_AGENT"
                })

            if not response_text:
                response_text = "I'm here to help! How can I assist you?"
                logger.info("Inference returned an empty response. Using default response.")

            # Step 4: Prepare the response payload
            response = {
                "id": data["id"],
                "client_id": client_id,
                "chat_id": data["chat_id"],
                "message": {
                    "type": "TEXT",
                    "text": response_text
                },
                "event": "BOT_MESSAGE"
            }

            logger.info(f"Sending response to client_id={client_id}: {response_text}")
            send_response_to_jivo(response)
            return jsonify(response)

        except Exception as e:
            logger.error(f"Error during message processing for client_id={client_id}: {e}", exc_info=True)

            # Step 5: Escalate to an agent if an error occurs
            return jsonify({
                "id": data["id"],
                "client_id": client_id,
                "chat_id": data["chat_id"],
                "event": "INVITE_AGENT"
            })

    elif event_type == "INVITE_AGENT":
        logger.info(f"Escalating to a human agent for client_id={data.get('client_id')}.")
        return jsonify({"status": "Escalation to human agent triggered"})

    elif event_type == "CHAT_CLOSED":
        logger.info("Received CHAT_CLOSED event. Chat session ended.")
        return jsonify({"status": "Chat closed"})

    elif event_type == "AGENT_UNAVAILABLE":
        logger.info("Received AGENT_UNAVAILABLE event. No agents available.")
        return jsonify({"status": "No agents available, bot will continue"})

    # Step 6: Handle unrecognized events
    logger.warning(f"Received unhandled event type: {event_type}")
    return jsonify({"status": "Event not handled"})

if __name__ == '__main__':
    logger.info("Starting Flask app on port 8000.")
    app.run(port=8000)