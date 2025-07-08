import os
import requests
import json
from typing import Optional, List
import sqlite3
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import urllib.request

# Simple memory system (can be replaced with a DB later)
MEMORY_FILE = os.path.join(os.path.dirname(__file__), 'tec_memories.json')

# SQLite memory system
SQLITE_DB = os.path.join(os.path.dirname(__file__), 'tec_memories.db')


def init_db():
    conn = sqlite3.connect(SQLITE_DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memories
                 (id INTEGER PRIMARY KEY, input TEXT, output TEXT)''')
    conn.commit()
    conn.close()


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


def save_memory_sqlite(entry: dict):
    conn = sqlite3.connect(SQLITE_DB)
    c = conn.cursor()
    c.execute('INSERT INTO memories (input, output) VALUES (?, ?)', (entry['input'], entry['output']))
    conn.commit()
    conn.close()


def load_memories_sqlite() -> list:
    conn = sqlite3.connect(SQLITE_DB)
    c = conn.cursor()
    c.execute('SELECT input, output FROM memories')
    rows = c.fetchall()
    conn.close()
    return [{'input': row[0], 'output': row[1]} for row in rows]


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


def read_txt_file(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def read_pdf_file(filepath: str) -> str:
    reader = PdfReader(filepath)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text


def scrape_url(url: str) -> str:
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()


# Modular LLM API wrapper

def call_llm(text: str, api_key: str, provider: str = 'gemini', model: str = 'gemini-2.0-flash') -> str:
    if provider == 'gemini':
        return process_text(text, api_key, model)
    elif provider == 'openai':
        # Placeholder for OpenAI call
        return 'OpenAI API not implemented yet.'
    elif provider == 'local':
        # Placeholder for local LLM call
        return 'Local LLM not implemented yet.'
    else:
        return 'Unknown provider.'


def process_input(input_data: str, api_key: str, input_type: str = 'text', provider: str = 'gemini', model: str = 'gemini-2.0-flash', filepath: str = None, url: str = None) -> str:
    init_db()
    if input_type == 'text':
        output = call_llm(input_data, api_key, provider, model)
        save_memory_sqlite({"input": input_data, "output": output})
        return output
    elif input_type == 'txt_file' and filepath:
        text = read_txt_file(filepath)
        output = call_llm(text, api_key, provider, model)
        save_memory_sqlite({"input": text, "output": output})
        return output
    elif input_type == 'pdf_file' and filepath:
        text = read_pdf_file(filepath)
        output = call_llm(text, api_key, provider, model)
        save_memory_sqlite({"input": text, "output": output})
        return output
    elif input_type == 'url' and url:
        text = scrape_url(url)
        output = call_llm(text, api_key, provider, model)
        save_memory_sqlite({"input": text, "output": output})
        return output
    else:
        return "Input type not supported or missing parameters."
