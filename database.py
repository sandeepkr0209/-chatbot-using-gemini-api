from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot_db"]

users_collection = db["users"]
conversation_collection = db["conversations"]

def store_conversation(user_id, user_message, bot_message):
    """Stores user and bot messages in MongoDB."""
    conversation_data = {
        "user_id": user_id,
        "messages": [
            {"sender": "user", "message": user_message, "timestamp": datetime.utcnow()},
            {"sender": "bot", "message": bot_message, "timestamp": datetime.utcnow()},
        ],
    }
    conversation_collection.insert_one(conversation_data)
    print("✅ Conversation stored successfully.")

def get_user_history(user_id, limit=5):
    """Fetches the last few messages from conversation history in MongoDB."""
    history = conversation_collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
    return [msg["messages"] for msg in history]

def store_user_details(user_id, name, email, preferences=None):
    """Stores or updates user details in MongoDB."""
    user_data = {
        "name": name,
        "email": email,
        "preferences": preferences or {},
        "updated_at": datetime.utcnow()
    }
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": user_data},
        upsert=True,
    )
    print("✅ User details stored successfully.")

def get_user_name(user_id):
    """Retrieves the user's name from MongoDB."""
    user = users_collection.find_one({"user_id": user_id})
    return user["name"] if user else "friend"

def get_user_preferences(user_id):
    """Retrieves the user's preferences from MongoDB."""
    user = users_collection.find_one({"user_id": user_id})
    return user.get("preferences", {}) if user else {}

