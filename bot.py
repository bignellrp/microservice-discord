import discord
from flask import Flask, request, abort

app = Flask(__name__)
bot = discord.Client()

# Your Discord bot token goes here
DISCORD_BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN"
# Replace with a secure API key for authentication
API_KEY = "YOUR_API_KEY"

@app.route("/api/message", methods=["POST"])
def handle_message():
    data = request.json
    message_content = data["content"]
    message_id = data["id"]
    api_key = request.headers.get("Authorization")

    if not api_key or api_key != f"Bearer {API_KEY}":
        abort(401, "Unauthorized")

    try:
        # Check if the message has been processed before
        if not is_message_processed(message_id):
            response = process_message(message_content)
            store_message_id(message_id)
            return response
        else:
            return "Message already processed."
    except Exception as e:
        # Handle other exceptions gracefully
        abort(500, str(e))

def is_message_processed(message_id):
    # Your implementation to check if the message ID exists in the database or cache
    pass

def store_message_id(message_id):
    # Your implementation to store the message ID in the database or cache
    pass

def process_message(message_content):
    # Your message processing logic goes here
    # Simulating an error for demonstration purposes
    if "error" in message_content.lower():
        raise ValueError("Error in the user's message")
    return "Response to the user's message"

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

bot.run(DISCORD_BOT_TOKEN)
