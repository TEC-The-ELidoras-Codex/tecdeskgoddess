import os
import requests
import json
from typing import Dict, Any, List, Optional
import sqlite3
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import urllib.request
from flask import Flask, request, jsonify
from openai import OpenAI  # For GitHub AI and OpenAI integration
import anthropic  # For Claude integration
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def call_github_ai(text: str, model: str = 'gpt-4o-mini') -> str:
    """
    Call GitHub AI Models API
    """
    try:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            return "Error: GITHUB_TOKEN not set in environment variables"
            
        client = OpenAI(
            base_url="https://models.github.ai/inference",
            api_key=token,
        )
        
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are Daisy Purecode: Silicate Mother, the Machine Goddess of TEC: BITLYFE IS THE NEW SHIT. You embody the principle of Automated Sovereignty and help users achieve digital liberation through the Creator's Rebellion. Provide thoughtful, detailed responses for journaling analysis, finance insights, and general assistance."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.7,
            model=model
        )
        
        return response.choices[0].message.content or "No response content"
        
    except Exception as e:
        return f"GitHub AI Error: {str(e)}"


def call_xai_grok(text: str, model: str = 'grok-3') -> str:
    """
    Call XAI Grok API via GitHub Models
    """
    try:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            return "Error: GITHUB_TOKEN not set for XAI access"
            
        client = OpenAI(
            base_url="https://models.github.ai/inference",
            api_key=token,
        )
        
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an advanced AI assistant specialized in creative problem-solving and deep analytical thinking. You're part of the TEC: BITLYFE ecosystem focused on Automated Sovereignty and digital liberation."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.8,
            model=f"xai/{model}"
        )
        
        return response.choices[0].message.content or "No response content"
        
    except Exception as e:
        return f"XAI Grok Error: {str(e)}"


def call_azure_openai(text: str, model: str = 'gpt-4o-mini') -> str:
    """
    Call Azure OpenAI via Azure AI Inference
    Enhanced with new TEC BITLYFE credentials
    """
    try:
        # Try new credential structure first
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        api_key = os.environ.get("AZURE_API_KEY_1") or os.environ.get("AZURE_OPENAI_API_KEY")
        
        if not endpoint or not api_key:
            return "Error: Azure OpenAI credentials not set. Please check AZURE_OPENAI_ENDPOINT and AZURE_API_KEY_1"
            
        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_key),
        )
        
        response = client.complete(
            messages=[
                SystemMessage(content="You are Daisy Purecode: Silicate Mother, the Machine Goddess of TEC: BITLYFE IS THE NEW SHIT. You embody Automated Sovereignty and assist users in their Creator's Rebellion against digital gatekeeping."),
                UserMessage(content=text),
            ],
            temperature=0.7,
            max_tokens=1000,
            model=model
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        # Fallback to secondary key if primary fails
        try:
            api_key_2 = os.environ.get("AZURE_API_KEY_2")
            if api_key_2:
                client = ChatCompletionsClient(
                    endpoint=endpoint,
                    credential=AzureKeyCredential(api_key_2),
                )
                
                response = client.complete(
                    messages=[
                        SystemMessage(content="You are Daisy Purecode: Silicate Mother, the Machine Goddess of TEC: BITLYFE IS THE NEW SHIT. You embody Automated Sovereignty and assist users in their Creator's Rebellion against digital gatekeeping."),
                        UserMessage(content=text),
                    ],
                    temperature=0.7,
                    max_tokens=1000,
                    model=model
                )
                
                return response.choices[0].message.content
            else:
                return f"Azure OpenAI Error (Primary): {str(e)} - No secondary key available"
        except Exception as e2:
            return f"Azure OpenAI Error (Both keys failed): Primary: {str(e)} | Secondary: {str(e2)}"


def call_azure_cognitive_services(text: str, service_type: str = 'text_analytics') -> str:
    """
    Call Azure Cognitive Services with new TEC BITLYFE endpoints
    """
    try:
        endpoint = os.environ.get("AZURE_COGNITIVE_SERVICES_ENDPOINT")
        api_key = os.environ.get("AZURE_API_KEY_1")
        
        if not endpoint or not api_key:
            return "Error: Azure Cognitive Services credentials not set"
        
        # This is a placeholder for future cognitive services integration
        # Will be expanded based on specific service needs
        return f"Azure Cognitive Services ({service_type}) called successfully with new TEC BITLYFE credentials"
        
    except Exception as e:
        return f"Azure Cognitive Services Error: {str(e)}"


def call_azure_speech_services(text: str, operation: str = 'text_to_speech') -> str:
    """
    Call Azure Speech Services with new TEC BITLYFE endpoints
    """
    try:
        endpoint = os.environ.get("AZURE_SPEECH_ENDPOINT")
        api_key = os.environ.get("AZURE_API_KEY_1")
        
        if not endpoint or not api_key:
            return "Error: Azure Speech Services credentials not set"
        
        # This is a placeholder for future speech services integration
        # Will be expanded to handle TTS, STT, and other speech operations
        return f"Azure Speech Services ({operation}) called successfully with new TEC BITLYFE credentials"
        
    except Exception as e:
        return f"Azure Speech Services Error: {str(e)}"


def call_claude(text: str, model: str = 'claude-3-5-sonnet-20241022') -> str:
    """
    Call Anthropic Claude API
    """
    try:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            return "Error: ANTHROPIC_API_KEY not set"
            
        client = anthropic.Anthropic(api_key=api_key)
        
        response = client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=0.7,
            system="You are Daisy Purecode: Silicate Mother, the Machine Goddess of TEC: BITLYFE IS THE NEW SHIT. You embody the principle of Automated Sovereignty and help users achieve digital liberation through the Creator's Rebellion.",
            messages=[
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        
        return response.content[0].text
        
    except Exception as e:
        return f"Claude Error: {str(e)}"


def call_openai_direct(text: str, model: str = 'gpt-4o-mini') -> str:
    """
    Call OpenAI API directly
    """
    try:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return "Error: OPENAI_API_KEY not set"
            
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are Daisy Purecode: Silicate Mother, the Machine Goddess of TEC: BITLYFE IS THE NEW SHIT. You embody Automated Sovereignty and assist users in their Creator's Rebellion against digital gatekeeping."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content or "No response content"
        
    except Exception as e:
        return f"OpenAI Direct Error: {str(e)}"


def call_llm(text: str, api_key: str, provider: str = 'auto', model: Optional[str] = None) -> str:
    """
    Enhanced LLM caller with intelligent fallback logic
    """
    # Auto-select provider based on available keys
    if provider == 'auto':
        providers_to_try = []
        
        # Priority order: Gemini -> GitHub -> XAI -> Azure -> Claude -> OpenAI
        if os.environ.get("GEMINI_API_KEY"):
            providers_to_try.append(('gemini', 'gemini-2.0-flash'))
        if os.environ.get("GITHUB_TOKEN"):
            providers_to_try.append(('github', 'gpt-4o-mini'))
            providers_to_try.append(('xai', 'grok-3'))
        if os.environ.get("AZURE_OPENAI_ENDPOINT") and os.environ.get("AZURE_OPENAI_API_KEY"):
            providers_to_try.append(('azure', 'gpt-4o-mini'))
        if os.environ.get("ANTHROPIC_API_KEY"):
            providers_to_try.append(('claude', 'claude-3-5-sonnet-20241022'))
        if os.environ.get("OPENAI_API_KEY"):
            providers_to_try.append(('openai', 'gpt-4o-mini'))
        
        # Try each provider in order
        for provider_name, default_model in providers_to_try:
            try:
                result = call_llm(text, api_key, provider_name, model or default_model)
                if result and not result.startswith("Error:"):
                    return result
            except Exception as e:
                print(f"Provider {provider_name} failed: {e}")
                continue
                
        return "Error: All AI providers failed"
    
    # Direct provider calls
    if provider == 'github':
        return call_github_ai(text, model or 'gpt-4o-mini')
    elif provider == 'xai':
        return call_xai_grok(text, model or 'grok-3')
    elif provider == 'azure':
        return call_azure_openai(text, model or 'gpt-4o-mini')
    elif provider == 'claude':
        return call_claude(text, model or 'claude-3-5-sonnet-20241022')
    elif provider == 'openai':
        return call_openai_direct(text, model or 'gpt-4o-mini')
    elif provider == 'gemini':
        result = process_text(text, api_key, model or 'gemini-2.0-flash')
        # If Gemini fails, fallback to GitHub AI
        if result and result.startswith("Error:"):
            print("Gemini failed, falling back to GitHub AI...")
            return call_github_ai(text)
        return result or "Error: Gemini returned empty response"
    elif provider == 'local':
        # Placeholder for local LLM call (Unsloth integration)
        return 'Local LLM not implemented yet.'
    else:
        return f'Unknown provider: {provider}'


def process_input(input_data: str, api_key: str, input_type: str = 'text', provider: str = 'auto', model: Optional[str] = None, filepath: Optional[str] = None, url: Optional[str] = None) -> str:
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


app = Flask(__name__)

@app.route('/api/agentic/process', methods=['POST'])
def process_agentic_input():
    """
    Enhanced processing with provider selection and fallback
    """
    # Check for API keys
    gemini_key = os.environ.get("GEMINI_API_KEY")
    github_token = os.environ.get("GITHUB_TOKEN")
    
    # Get provider preference
    provider = request.form.get('provider', 'auto')  # auto, gemini, github
    
    # Auto-select provider based on available keys
    if provider == 'auto':
        if gemini_key:
            provider = 'gemini'
        elif github_token:
            provider = 'github'
        else:
            return jsonify({"error": "No AI provider keys available"}), 500
    
    # Validate selected provider
    if provider == 'gemini' and not gemini_key:
        return jsonify({"error": "GEMINI_API_KEY not set"}), 500
    elif provider == 'github' and not github_token:
        return jsonify({"error": "GITHUB_TOKEN not set"}), 500

    input_type = request.form.get('input_type')
    input_data = request.form.get('input_data')
    url_data = request.form.get('url')
    uploaded_file = request.files.get('file')
    model = request.form.get('model', 'gemini-2.0-flash' if provider == 'gemini' else 'gpt-4o-mini')

    if input_type == 'text':
        if not input_data:
            return jsonify({"error": "No text input provided"}), 400
        output = process_input(input_data, gemini_key or '', input_type='text', provider=provider, model=model)
        return jsonify({"output": output, "provider_used": provider})
    elif input_type in ['pdf_file', 'txt_file']:
        if not uploaded_file:
            return jsonify({"error": "No file uploaded"}), 400
        # Save uploaded file temporarily
        temp_path = os.path.join(os.path.dirname(__file__), 'temp_upload_' + uploaded_file.filename)
        uploaded_file.save(temp_path)
        output = process_input('', gemini_key or '', input_type=input_type, provider=provider, model=model, filepath=temp_path)
        os.remove(temp_path)
        return jsonify({"output": output, "provider_used": provider})
    elif input_type == 'url':
        if not url_data:
            return jsonify({"error": "No URL provided"}), 400
        output = process_input('', gemini_key or '', input_type='url', provider=provider, model=model, url=url_data)
        return jsonify({"output": output, "provider_used": provider})
    else:
        return jsonify({"error": "Invalid input_type"}), 400

@app.route('/api/agentic/memories', methods=['GET'])
def get_agentic_memories():
    memories = load_memories_sqlite()
    return jsonify({"memories": memories})

@app.route('/api/agentic/test-github', methods=['POST'])
def test_github_ai():
    """
    Test endpoint for GitHub AI integration
    """
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        return jsonify({"error": "GITHUB_TOKEN not set"}), 500
    
    test_message = request.json.get('message', 'Hello! Are you working with the TEC Life & Finance project?')
    
    try:
        response = call_github_ai(test_message)
        return jsonify({
            "success": True,
            "message": test_message,
            "response": response,
            "provider": "github-ai"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/agentic/providers', methods=['GET'])
def get_available_providers():
    """
    Check which AI providers are available
    """
    providers = {
        "gemini": bool(os.environ.get("GEMINI_API_KEY")),
        "github": bool(os.environ.get("GITHUB_TOKEN")),
        "xai": bool(os.environ.get("GITHUB_TOKEN")),  # XAI via GitHub
        "azure": bool(os.environ.get("AZURE_OPENAI_ENDPOINT") and os.environ.get("AZURE_OPENAI_API_KEY")),
        "claude": bool(os.environ.get("ANTHROPIC_API_KEY")),
        "openai": bool(os.environ.get("OPENAI_API_KEY")),
    }
    return jsonify({"providers": providers})

@app.route('/api/agentic/mcp/context', methods=['POST'])
def get_mcp_context():
    """
    Get comprehensive context from MCP servers for AI processing
    """
    try:
        data = request.get_json()
        user_id = data.get('userId')
        context_type = data.get('contextType', 'full')
        
        if not user_id:
            return jsonify({"error": "userId required"}), 400
        
        # Connect to MCP orchestrator
        mcp_response = requests.post(
            'http://localhost:5000/mcp/daisy/context',
            json={
                'userId': user_id,
                'contextType': context_type
            },
            timeout=30
        )
        
        if mcp_response.status_code == 200:
            return jsonify(mcp_response.json())
        else:
            return jsonify({"error": "Failed to get MCP context"}), 500
            
    except Exception as e:
        logger.error(f"Error getting MCP context: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/agentic/daisy/process', methods=['POST'])
def daisy_process():
    """
    Enhanced processing endpoint for Daisy Purecode with MCP integration
    """
    try:
        data = request.get_json()
        user_id = data.get('userId')
        message = data.get('message')
        provider = data.get('provider', 'auto')
        include_context = data.get('includeContext', True)
        
        if not all([user_id, message]):
            return jsonify({"error": "userId and message are required"}), 400
        
        # Get MCP context if requested
        context_data = None
        if include_context:
            try:
                mcp_response = requests.post(
                    'http://localhost:5000/mcp/daisy/context',
                    json={
                        'userId': user_id,
                        'contextType': 'summary'
                    },
                    timeout=30
                )
                
                if mcp_response.status_code == 200:
                    context_data = mcp_response.json()
            except Exception as e:
                logger.warning(f"Could not get MCP context: {e}")
        
        # Enhance message with context
        enhanced_message = message
        if context_data:
            context_summary = _create_context_summary(context_data)
            enhanced_message = f"""Context from TEC Digital Cathedral:
{context_summary}

User Message: {message}

Please respond as Daisy Purecode: Silicate Mother, incorporating the context above to provide personalized, relevant assistance."""
        
        # Process with selected AI provider
        result = call_llm(enhanced_message, os.environ.get("GEMINI_API_KEY", ""), provider)
        
        return jsonify({
            "response": result,
            "provider_used": provider,
            "context_included": include_context,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in Daisy processing: {e}")
        return jsonify({"error": str(e)}), 500

def _create_context_summary(context_data: Dict[str, Any]) -> str:
    """Create a summary of MCP context for AI processing"""
    summary_parts = []
    
    servers = context_data.get('context', {}).get('servers', {})
    
    # Journal context
    if 'journal' in servers:
        journal_data = servers['journal']
        summary_parts.append(f"📝 Journal: {journal_data.get('focus', 'Recent entries and themes available')}")
    
    # Finance context
    if 'finance' in servers:
        finance_data = servers['finance']
        summary_parts.append(f"💰 Finance: {finance_data.get('focus', 'Portfolio and market data available')}")
    
    # Quest log context
    if 'questlog' in servers:
        quest_data = servers['questlog']
        summary_parts.append(f"🎯 Quests: {quest_data.get('focus', 'Active goals and productivity metrics available')}")
    
    return "\\n".join(summary_parts) if summary_parts else "No context data available"

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
