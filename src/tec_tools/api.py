from flask import Flask, request, jsonify
from agentic_processor import process_input, load_memories_sqlite
import os

app = Flask(__name__)

# Set your API key here or use environment variable
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_DEFAULT_API_KEY")

@app.route("/api/agentic/process", methods=["POST"])
def process():
    input_type = request.form.get("input_type", "text")
    input_data = request.form.get("input_data", "")
    url = request.form.get("url")
    file = request.files.get("file")
    filepath = None

    # Handle file upload
    if file:
        filepath = f"/tmp/{file.filename}"
        file.save(filepath)

    output = process_input(
        input_data=input_data,
        api_key=API_KEY,
        input_type=input_type,
        filepath=filepath,
        url=url
    )
    # Clean up temp file
    if filepath and os.path.exists(filepath):
        os.remove(filepath)
    return jsonify({"output": output})

@app.route("/api/agentic/memories", methods=["GET"])
def memories():
    memories = load_memories_sqlite()
    return jsonify({"memories": memories})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)