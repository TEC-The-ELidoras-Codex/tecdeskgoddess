from flask import Flask, request, jsonify
from flask_cors import CORS
from .agentic_processor import process_input, load_memories_sqlite
from .enhanced_ai import enhanced_process_input
import os
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for web interface

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set your API key here or use environment variable
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_DEFAULT_API_KEY")

@app.route("/api/agentic/process", methods=["POST"])
def process():
    try:
        # Handle both form data and JSON
        if request.is_json:
            data = request.get_json()
            input_data = data.get("message", "")
            user_id = data.get("user_id", "anonymous")
            session_id = data.get("session_id", "default")
            preferred_provider = data.get("preferred_provider", "auto")
            input_type = "text"
            url = None
            file = None
        else:
            input_type = request.form.get("input_type", "text")
            input_data = request.form.get("input_data", "")
            url = request.form.get("url")
            file = request.files.get("file")
            user_id = request.form.get("user_id", "anonymous")
            session_id = request.form.get("session_id", "default")
            preferred_provider = request.form.get("preferred_provider", "auto")

        filepath = None

        # Handle file upload
        if file:
            filepath = f"/tmp/{file.filename}"
            file.save(filepath)

        logger.info(f"Processing request from user {user_id}, session {session_id}, provider: {preferred_provider}")
        
        # Use enhanced AI for better responses
        if input_type == "text" and not file and not url:
            # Use enhanced AI for text-only requests
            result = enhanced_process_input(
                message=input_data,
                user_id=user_id,
                session_id=session_id,
                provider=preferred_provider
            )
            
            return jsonify(result)
        else:
            # Use original processor for file/URL handling
            output = process_input(
                input_data=input_data,
                api_key=API_KEY,
                input_type=input_type,
                filepath=filepath,
                url=url,
                provider=preferred_provider
            )
            
            # Clean up temp file
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
                
            return jsonify({
                "output": output,
                "status": "success",
                "user_id": user_id,
                "session_id": session_id,
                "provider": preferred_provider
            })
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route("/api/agentic/memories", methods=["GET"])
def memories():
    memories = load_memories_sqlite()
    return jsonify({"memories": memories})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)