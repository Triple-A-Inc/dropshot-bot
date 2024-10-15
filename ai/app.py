import os
from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
from tools import search_items  # Import your tools
from graph import run_vendor_inference, vendor  # Import your graph functions

load_dotenv()  # Load environment variables

app = Flask(__name__)
JIVOCHAT_TOKEN = os.getenv("JIVOCHAT_TOKEN")  # Securely load your token

@app.route('/webhook', methods=['POST'])
def webhook():
    # Verify the token
    auth_header = request.headers.get("Authorization")
    if auth_header != f"Bearer {JIVOCHAT_TOKEN}":
        abort(401)  # Unauthorized access if token does not match

    # Process incoming JivoChat event
    data = request.get_json()
    event_type = data.get("event")

    if event_type == "CLIENT_MESSAGE":
        client_id = data["client_id"]
        message = data["message"]["text"]

        # Run the inference with your vendor AI setup
        response_text = run_vendor_inference(vendor, message, client_id)

        # Return response formatted for JivoChat
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
        return jsonify(response)

    elif event_type == "CHAT_CLOSED":
        return jsonify({"status": "Chat closed"})

    elif event_type == "AGENT_UNAVAILABLE":
        return jsonify({"status": "No agents available, bot will continue"})

    return jsonify({"status": "Event not handled"})

if __name__ == '__main__':
    app.run(port=8000)