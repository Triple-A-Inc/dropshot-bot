import os
from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
from tools import search_items  # Import your tools
from graph import run_vendor_inference, vendor  # Import your graph functions
import logging

load_dotenv()  # Load environment variables

app = Flask(__name__)
JIVOCHAT_TOKEN = os.getenv("JIVOCHAT_TOKEN")  # Securely load your token

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/webhook/RIrNaX4eb9xNJJk', methods=['POST'])
def webhook():
    # Verify the token
    auth_header = request.headers.get("Authorization")
    if auth_header != f"Bearer {JIVOCHAT_TOKEN}":
        abort(401)  # Unauthorized access if token does not match

    # Process incoming JivoChat event
    data = request.get_json()
    event_type = data.get("event")
    logging.debug(f"Received event: {event_type}")

    if event_type == "CLIENT_MESSAGE":
        client_id = data["client_id"]
        message = data["message"]["text"]

        # Run the inference with your vendor AI setup
        try:
            response_text = run_vendor_inference(vendor, message, client_id)
            if not response_text:
                response_text = "I'm here to help! How can I assist you?"

            # Return response formatted for JivoChat directly in the webhook response
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

            logging.debug(f"Sending response: {response}")
            return jsonify(response)

        except Exception as e:
            logging.error(f"Error processing message: {e}")
            # Optionally escalate to an agent if there's an error
            return jsonify({
                "id": data["id"],
                "client_id": client_id,
                "chat_id": data["chat_id"],
                "event": "INVITE_AGENT"
            })

    elif event_type == "CHAT_CLOSED":
        logging.info("Chat closed by JivoChat.")
        return jsonify({"status": "Chat closed"})

    elif event_type == "AGENT_UNAVAILABLE":
        logging.info("No agents available; bot will continue assisting the client.")
        return jsonify({"status": "No agents available, bot will continue"})

    logging.warning(f"Unhandled event type: {event_type}")
    return jsonify({"status": "Event not handled"})

if __name__ == '__main__':
    app.run(port=8000)