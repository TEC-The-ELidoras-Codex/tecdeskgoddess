#!/usr/bin/env python3
"""
TEC AI System Test
Test all configured AI providers
"""
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_tec_api():
    """Test the TEC API endpoint"""
    url = "http://127.0.0.1:5000/api/agentic/process"
    
    test_data = {
        "message": "Hello TEC! Test all AI providers and tell me about digital sovereignty.",
        "user_id": "test_user",
        "session_id": "test_session"
    }
    
    try:
        print("🧪 Testing TEC API...")
        response = requests.post(url, json=test_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ TEC API Response:")
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure TEC backend is running")
    except Exception as e:
        print(f"❌ Test Error: {e}")

def check_ai_providers():
    """Check which AI providers are configured"""
    providers = {
        "Gemini": os.getenv("GEMINI_API_KEY"),
        "OpenAI": os.getenv("OPENAI_API_KEY"), 
        "Anthropic": os.getenv("ANTHROPIC_API_KEY"),
        "GitHub AI": os.getenv("GITHUB_TOKEN"),
        "Azure AI": os.getenv("AZURE_AI_KEY_1"),
        "XAI": os.getenv("XAI_API_KEY")
    }
    
    print("🤖 AI Provider Status:")
    for name, key in providers.items():
        status = "✅ Configured" if key and key != "your_api_key_here" else "❌ Missing"
        print(f"  {name}: {status}")

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║               TEC: BITLYFE IS THE NEW SHIT                   ║")
    print("║                    AI System Test                            ║")
    print("║                'The Creator's Rebellion'                     ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    check_ai_providers()
    print()
    test_tec_api()
