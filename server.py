from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from database import store_conversation, get_user_history, store_user_details, get_user_name, get_user_preferences
import logging
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Gemini AI model
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyAPXeMIfmyZb1pNNrqsOfQtsDIMulny_5U')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def home():
    return "Flask server is running with MongoDB!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id", "guest").strip()
    user_message = data.get("message", "").strip()

    logging.info(f"Received message from User ID: {user_id} | Message: {user_message}")

    if not user_message:
        bot_message = "Hello, I'm Dr. SYNO, a psychiatrist here to support your mental well-being. Tell me what's on your mind today."
        store_conversation(user_id, user_message, bot_message)
        return jsonify({"bot_message": bot_message})

    # Retrieve user name and history
    user_name = get_user_name(user_id)
    history = get_user_history(user_id)

    # Check if the user provided their name in the current message
    if "my name is" in user_message.lower():
        user_name = user_message.split("my name is")[-1].strip()
        store_user_details(user_id, user_name, email=None)  # Assuming email is optional here

    prompt = generate_personalized_prompt(user_id, user_message, user_name, history)

    logging.info("Sending prompt to AI model")

    try:
        response = model.generate_content(prompt)
        bot_message = response.text.strip() if hasattr(response, "text") else "I'm here to support you. Can you tell me more about what you're feeling?"

        logging.info(f"AI Response: {bot_message}")
        store_conversation(user_id, user_message, bot_message)
        return jsonify({"bot_message": bot_message})

    except Exception as e:
        logging.error(f"Error generating AI response: {str(e)}")
        return jsonify({"bot_message": "An error occurred while processing your request."}), 500

@app.route("/store_user", methods=["POST"])
def store_user():
    """Stores user details in MongoDB."""
    data = request.json
    user_id = data.get("user_id", "guest").strip()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    preferences = data.get("preferences", {})

    if user_id and name and email:
        try:
            store_user_details(user_id, name, email, preferences)
            logging.info(f"Stored user details: {user_id} -> {name} ({email})")
            return jsonify({"status": "success"}), 200
        except Exception as e:
            logging.error(f"Error storing user details: {str(e)}")
            return jsonify({"status": "failure", "message": "Internal server error"}), 500
    else:
        logging.warning("Invalid data provided for storing user details")
        return jsonify({"status": "failure", "message": "Invalid data"}), 400

@app.route("/store_message", methods=["POST"])
def store_message():
    data = request.json
    user_id = data.get("user_id", "guest").strip()
    user_message = data.get("user_message", "").strip()
    bot_message = data.get("bot_message", "").strip()

    if not user_message or not bot_message:
        return jsonify({"status": "failure", "message": "Invalid data"}), 400

    try:
        store_conversation(user_id, user_message, bot_message)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "failure", "message": str(e)}), 500

def generate_personalized_prompt(user_id, user_message, user_name, history):
    """Generate a personalized prompt for the AI model."""
    history_text = " ".join([msg["message"] for conv in history for msg in conv])
    preferences_text = f"User preferences: {get_user_preferences(user_id)}"

    prompt = f"""
    You are Dr. SYNO, a highly empathetic and professional psychiatrist AI chatbot.
    Your role is to provide thoughtful, therapeutic, and clinically-informed responses.
    Here is the user's conversation history: {history_text}
    {preferences_text}

    User {user_name}: {user_message}

    Respond like a psychiatrist, ensuring empathy, care, and professionalism in your answer.
    """
    return prompt

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
