#!/usr/bin/env python3
"""
TEC Life & Finance Quick Start
Get your AI companion up and running in seconds!
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking TEC environment...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        return False
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded")
    except ImportError:
        print("⚠️ python-dotenv not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "python-dotenv"])
        from dotenv import load_dotenv
        load_dotenv()
    
    # Check critical tokens
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token or github_token == "your_github_token_here":
        print("❌ GitHub token not configured!")
        return False
    
    print("✅ GitHub token configured")
    
    # Check other AI services
    azure_key = os.environ.get("AZURE_AI_KEY_1")
    xai_key = os.environ.get("XAI_API_KEY")
    crypto_key = os.environ.get("CRYPTOCOMPARE_API_KEY")
    
    if azure_key and azure_key != "your_azure_api_key_here":
        print("✅ Azure AI configured")
    if xai_key and xai_key != "your_xai_api_key_here":
        print("✅ XAI configured")
    if crypto_key and crypto_key != "your_cryptocompare_api_key_here":
        print("✅ CryptoCompare configured")
    
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing TEC dependencies...")
    
    required_packages = [
        "flask",
        "requests", 
        "openai",
        "python-dotenv",
        "azure-ai-inference",
        "azure-identity",
        "azure-cognitiveservices-speech"
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} already installed")
        except ImportError:
            print(f"📥 Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)

def test_ai_providers():
    """Test AI provider connections"""
    print("🤖 Testing AI providers...")
    
    # Test GitHub AI
    try:
        from openai import OpenAI
        github_token = os.environ.get("GITHUB_TOKEN")
        
        client = OpenAI(
            base_url="https://models.github.ai/inference",
            api_key=github_token
        )
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": "Hello TEC!"}],
            model="gpt-4o-mini",
            max_tokens=50
        )
        
        print("✅ GitHub AI: Connected")
        print(f"   Response: {response.choices[0].message.content[:50]}...")
        
    except Exception as e:
        print(f"❌ GitHub AI: {str(e)[:50]}...")
    
    # Test Azure AI if configured
    azure_key = os.environ.get("AZURE_AI_KEY_1")
    if azure_key and azure_key != "your_azure_api_key_here":
        try:
            from azure.ai.inference import ChatCompletionsClient
            from azure.ai.inference.models import SystemMessage, UserMessage
            from azure.core.credentials import AzureKeyCredential
            
            endpoint = os.environ.get("AZURE_AI_ENDPOINT")
            client = ChatCompletionsClient(
                endpoint=endpoint,
                credential=AzureKeyCredential(azure_key)
            )
            
            print("✅ Azure AI: Connected")
            
        except Exception as e:
            print(f"❌ Azure AI: {str(e)[:50]}...")

def test_crypto_apis():
    """Test crypto API connections"""
    print("🪙 Testing crypto APIs...")
    
    # Test CryptoCompare
    crypto_key = os.environ.get("CRYPTOCOMPARE_API_KEY")
    if crypto_key and crypto_key != "your_cryptocompare_api_key_here":
        try:
            import requests
            
            url = "https://min-api.cryptocompare.com/data/price"
            params = {
                "fsym": "BTC",
                "tsyms": "USD",
                "api_key": crypto_key
            }
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                btc_price = data.get("USD")
                print(f"✅ CryptoCompare: BTC = ${btc_price:,.2f}")
            else:
                print("❌ CryptoCompare: API call failed")
                
        except Exception as e:
            print(f"❌ CryptoCompare: {str(e)[:50]}...")
    
    # Test CoinMarketCap
    cmc_key = os.environ.get("COINMARKETCAP_API_KEY")
    if cmc_key and cmc_key != "your_coinmarketcap_api_key_here":
        try:
            import requests
            
            url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
            headers = {"X-CMC_PRO_API_KEY": cmc_key}
            params = {"symbol": "BTC", "convert": "USD"}
            
            response = requests.get(url, headers=headers, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                btc_price = data["data"]["BTC"]["quote"]["USD"]["price"]
                print(f"✅ CoinMarketCap: BTC = ${btc_price:,.2f}")
            else:
                print("❌ CoinMarketCap: API call failed")
                
        except Exception as e:
            print(f"❌ CoinMarketCap: {str(e)[:50]}...")

def start_basic_server():
    """Start a basic TEC server"""
    print("🚀 Starting TEC Life & Finance...")
    
    # Create a simple Flask app if agentic_processor doesn't exist
    try:
        from tec_tools.agentic_processor import app
        print("✅ Found agentic_processor, starting enhanced server...")
        
    except ImportError:
        print("⚠️ Creating basic TEC server...")
        
        # Create basic server
        basic_server_code = '''
from flask import Flask, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return {
        "message": "Welcome to TEC Life & Finance!",
        "project": "BITLYFE IS THE NEW SHIT",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.route("/health")
def health():
    return {"status": "healthy", "service": "TEC Life & Finance"}

@app.route("/api/test")
def test_api():
    return {
        "github_ai": bool(os.environ.get("GITHUB_TOKEN")),
        "azure_ai": bool(os.environ.get("AZURE_AI_KEY_1")),
        "crypto_api": bool(os.environ.get("CRYPTOCOMPARE_API_KEY")),
        "message": "TEC APIs ready for action!"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
'''
        
        with open("tec_basic_server.py", "w") as f:
            f.write(basic_server_code)
        
        print("✅ Basic TEC server created")
    
    # Start the server
    print("\n🎯 TEC Life & Finance is ready!")
    print("=" * 50)
    print("🌐 Server: http://localhost:5000")
    print("🔍 Health: http://localhost:5000/health")
    print("🧪 Test API: http://localhost:5000/api/test")
    print("=" * 50)
    print("\n🚀 Starting server... (Press Ctrl+C to stop)")
    
    try:
        if os.path.exists("tec_tools/agentic_processor.py"):
            subprocess.run([sys.executable, "-m", "tec_tools.agentic_processor"])
        else:
            subprocess.run([sys.executable, "tec_basic_server.py"])
    except KeyboardInterrupt:
        print("\n👋 TEC Life & Finance stopped. See you next time!")

def main():
    """Main startup function"""
    print("🛡️ TEC: BITLYFE IS THE NEW SHIT - Quick Start")
    print("⚔️ The Creator's Rebellion - Getting You Up and Running!")
    print("=" * 60)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please fix the issues above.")
        return
    
    # Install dependencies
    install_dependencies()
    
    # Test connections
    test_ai_providers()
    test_crypto_apis()
    
    # Start server
    start_basic_server()

if __name__ == "__main__":
    main()
