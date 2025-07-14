#!/usr/bin/env python3
"""
TEC: BITLYFE API Key Testing Suite
The Creator's Rebellion - Validate Your API Configuration

This script tests all configured API keys to ensure they're working properly.
"""

import os
import sys
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_api():
    """Test OpenAI API connection"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key.startswith('your_'):
        return "❌ NOT CONFIGURED"
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        # Test with a minimal request
        response = requests.get('https://api.openai.com/v1/models', headers=headers, timeout=10)
        if response.status_code == 200:
            return "✅ WORKING"
        else:
            return f"❌ ERROR: {response.status_code}"
    except Exception as e:
        return f"❌ FAILED: {str(e)[:50]}"

def test_anthropic_api():
    """Test Anthropic Claude API connection"""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key or api_key.startswith('your_'):
        return "❌ NOT CONFIGURED"
    
    try:
        headers = {
            'x-api-key': api_key,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        # Test with a minimal message
        data = {
            'model': 'claude-3-haiku-20240307',
            'max_tokens': 10,
            'messages': [{'role': 'user', 'content': 'Hi'}]
        }
        response = requests.post('https://api.anthropic.com/v1/messages', 
                               headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            return "✅ WORKING"
        else:
            return f"❌ ERROR: {response.status_code}"
    except Exception as e:
        return f"❌ FAILED: {str(e)[:50]}"

def test_xai_api():
    """Test XAI (Grok) API connection"""
    api_key = os.getenv('XAI_API_KEY')
    if not api_key or api_key.startswith('your_'):
        return "❌ NOT CONFIGURED"
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        # XAI uses OpenAI-compatible endpoint
        response = requests.get('https://api.x.ai/v1/models', headers=headers, timeout=10)
        if response.status_code == 200:
            return "✅ WORKING"
        else:
            return f"❌ ERROR: {response.status_code}"
    except Exception as e:
        return f"❌ FAILED: {str(e)[:50]}"

def test_gemini_api():
    """Test Google Gemini API connection"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key.startswith('your_'):
        return "❌ NOT CONFIGURED"
    
    try:
        url = f'https://generativelanguage.googleapis.com/v1/models?key={api_key}'
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return "✅ WORKING"
        else:
            return f"❌ ERROR: {response.status_code}"
    except Exception as e:
        return f"❌ FAILED: {str(e)[:50]}"

def test_github_api():
    """Test GitHub API connection"""
    token = os.getenv('GITHUB_TOKEN')
    if not token or token.startswith('your_'):
        return "❌ NOT CONFIGURED"
    
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
        if response.status_code == 200:
            return "✅ WORKING"
        else:
            return f"❌ ERROR: {response.status_code}"
    except Exception as e:
        return f"❌ FAILED: {str(e)[:50]}"

def test_azure_ai():
    """Test Azure AI Services"""
    api_key = os.getenv('AZURE_API_KEY_1')
    endpoint = os.getenv('AZURE_COGNITIVE_SERVICES_ENDPOINT')
    
    if not api_key or api_key.startswith('your_') or not endpoint:
        return "❌ NOT CONFIGURED"
    
    try:
        headers = {
            'Ocp-Apim-Subscription-Key': api_key,
            'Content-Type': 'application/json'
        }
        # Test endpoint availability
        test_url = f"{endpoint.rstrip('/')}/text/analytics/v3.1/languages"
        response = requests.get(test_url, headers=headers, timeout=10)
        if response.status_code in [200, 400]:  # 400 is OK for test (missing body)
            return "✅ WORKING"
        else:
            return f"❌ ERROR: {response.status_code}"
    except Exception as e:
        return f"❌ FAILED: {str(e)[:50]}"

def test_elevenlabs_api():
    """Test ElevenLabs API connection"""
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key or api_key.startswith('your_'):
        return "❌ NOT CONFIGURED"
    
    try:
        headers = {
            'xi-api-key': api_key
        }
        response = requests.get('https://api.elevenlabs.io/v1/voices', headers=headers, timeout=10)
        if response.status_code == 200:
            return "✅ WORKING"
        else:
            return f"❌ ERROR: {response.status_code}"
    except Exception as e:
        return f"❌ FAILED: {str(e)[:50]}"

def test_coingecko_api():
    """Test CoinGecko API connection"""
    api_key = os.getenv('COINGECKO_API_KEY')
    if not api_key or api_key.startswith('your_'):
        return "❌ NOT CONFIGURED"
    
    try:
        headers = {'x-cg-demo-api-key': api_key} if api_key else {}
        response = requests.get('https://api.coingecko.com/api/v3/ping', headers=headers, timeout=10)
        if response.status_code == 200:
            return "✅ WORKING"
        else:
            return f"❌ ERROR: {response.status_code}"
    except Exception as e:
        return f"❌ FAILED: {str(e)[:50]}"

def main():
    print("🔑 TEC: BITLYFE API Testing Suite")
    print("=" * 50)
    
    # Check if .env exists
    if not Path('.env').exists():
        print("❌ No .env file found!")
        print("Run: python scripts/configure_apis.py")
        return
    
    print("🧪 Testing API Connections...\n")
    
    tests = {
        'OpenAI API': test_openai_api,
        'Anthropic Claude': test_anthropic_api,
        'XAI (Grok)': test_xai_api,
        'Google Gemini': test_gemini_api,
        'GitHub API': test_github_api,
        'Azure AI Services': test_azure_ai,
        'ElevenLabs': test_elevenlabs_api,
        'CoinGecko': test_coingecko_api
    }
    
    results = {}
    for name, test_func in tests.items():
        print(f"Testing {name}...", end=" ")
        result = test_func()
        results[name] = result
        print(result)
    
    print("\n" + "=" * 50)
    print("📊 Summary:")
    
    working = sum(1 for r in results.values() if r.startswith('✅'))
    total = len(results)
    
    print(f"Working APIs: {working}/{total}")
    
    if working >= 2:
        print("✅ GOOD: You have multiple AI providers configured")
        print("🚀 Ready to start TEC: python main.py")
    elif working >= 1:
        print("⚠️  MINIMAL: Consider adding more AI providers for redundancy")
        print("🚀 Can start TEC: python main.py")
    else:
        print("❌ CRITICAL: No working AI APIs found")
        print("📝 Configure APIs: python scripts/configure_apis.py")
    
    print("\n💡 Pro Tip: Configure at least 2-3 AI providers for:")
    print("   • Censorship resistance")
    print("   • Cost optimization") 
    print("   • Reliability/fallback")

if __name__ == "__main__":
    main()
