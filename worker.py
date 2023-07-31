from flask import Flask, request, abort

app = Flask(__name__)

# Replace with a secure API key for authentication
API_KEY = "YOUR_API_KEY"

@app.route("/api/process", methods=["POST"])
def process_message():
    api_key = request.headers.get("Authorization")
    if not api_key or api_key != f"Bearer {API_KEY}":
        abort(401, "Unauthorized")

    try:
        data = request.json
        message_content = data["content"]

        # Your message processing logic goes here
        # Simulating an error for demonstration purposes
        if "error" in message_content.lower():
            raise ValueError("Error in the user's message")
        response = "Response to the user's message"
        return response
    except ValueError as e:
        # Handle specific exceptions
        abort(400, str(e))
    except Exception as e:
        # Handle other exceptions gracefully
        abort(500, str(e))

if __name__ == "__main__":
    app.run(port=5001)  # Replace with the appropriate port number for your setup
