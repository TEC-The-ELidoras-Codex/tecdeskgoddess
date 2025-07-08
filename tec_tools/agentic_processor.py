import os
import requests
import json
from typing import Optional, List

# Simple memory system (can be replaced with a DB later)
MEMORY_FILE = os.path.join(os.path.dirname(__file__), 'tec_memories.json')


def save_memory(entry: dict):
    memories = load_memories()
    memories.append(entry)
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memories, f, ensure_ascii=False, indent=2)

def load_memories() -> List[dict]:
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def process_text(text: str, api_key: str, model: str = 'gemini-2.0-flash') -> Optional[str]:
    """
    Send text to Gemini API and return the processed script/story.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': api_key
    }
    data = {
        "contents": [
            {"parts": [{"text": text}]}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        # Extract the generated text (may need to adjust based on API response)
        try:
            return result['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            return str(result)
    else:
        return f"Error: {response.status_code} {response.text}"


def process_input(input_data: str, api_key: str, input_type: str = 'text') -> str:
    """
    Main entry: process text, file, or URL input.
    """
    if input_type == 'text':
        output = process_text(input_data, api_key)
        save_memory({"input": input_data, "output": output})
        return output
    # TODO: Add file and URL processing
    return "Input type not supported yet."


def get_memories() -> List[dict]:
    return load_memories()

# Example usage:
# result = process_input("Your rant here...", api_key="YOUR_API_KEY")
# print(result)
