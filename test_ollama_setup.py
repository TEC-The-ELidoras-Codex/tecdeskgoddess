#!/usr/bin/env python3
"""
Simple Ollama Test Script for TEC: BITLYFE
Part of TEC Clean Architecture Protocol TEC_ARCH_071925_V1
"""

import subprocess
import requests
import json
import sys

def check_ollama():
    """Check if Ollama is installed and running"""
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ Ollama not found")
            return False
    except FileNotFoundError:
        print("❌ Ollama not installed")
        return False

def list_models():
    """List installed Ollama models"""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if result.returncode == 0:
            print("📋 Installed models:")
            print(result.stdout)
            return True
        else:
            print("❌ Failed to list models")
            return False
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return False

def install_model(model_name="llama3.2:3b"):
    """Install a model via Ollama"""
    print(f"📥 Installing {model_name}...")
    try:
        result = subprocess.run(["ollama", "pull", model_name], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Successfully installed {model_name}")
            return True
        else:
            print(f"❌ Failed to install {model_name}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing model: {e}")
        return False

def test_model(model_name="llama3.2:3b"):
    """Test model with RPG prompt"""
    print(f"🧪 Testing {model_name}...")
    
    test_prompt = "You are Thorin, a wise dwarven blacksmith in a fantasy RPG. A player just entered your shop. Greet them warmly and offer your services in 2-3 sentences."
    
    try:
        result = subprocess.run(
            ["ollama", "run", model_name, test_prompt], 
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            response = result.stdout.strip()
            print("✅ Model test successful!")
            print(f"🎭 NPC Response:\n{response}")
            return True
        else:
            print(f"❌ Model test failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Model test timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing model: {e}")
        return False

def test_api_call(model_name="llama3.2:3b"):
    """Test Ollama API directly"""
    print(f"🔌 Testing Ollama API with {model_name}...")
    
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model_name,
        "prompt": "You are an AI assistant. Say hello in exactly 5 words.",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ API test successful!")
            print(f"📝 Response: {result.get('response', 'No response')}")
            return True
        else:
            print(f"❌ API test failed: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ API connection failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 50)
    print("🤖 TEC: BITLYFE - Ollama Setup Test")
    print("=" * 50)
    
    # Step 1: Check Ollama installation
    if not check_ollama():
        print("\n❌ Please install Ollama first: https://ollama.ai/")
        sys.exit(1)
    
    # Step 2: List current models
    print("\n" + "="*30)
    list_models()
    
    # Step 3: Offer to install recommended model
    print("\n" + "="*30)
    model_choice = input("Install llama3.2:3b (recommended for 12GB RAM)? [y/N]: ").lower()
    
    if model_choice == 'y':
        if install_model("llama3.2:3b"):
            model_name = "llama3.2:3b"
        else:
            print("Trying smaller model...")
            if install_model("llama3.2:1b"):
                model_name = "llama3.2:1b"
            else:
                print("❌ Failed to install any model")
                sys.exit(1)
    else:
        model_name = input("Enter model name to test (or press Enter for llama3.2:3b): ").strip()
        if not model_name:
            model_name = "llama3.2:3b"
    
    # Step 4: Test the model
    print("\n" + "="*30)
    if test_model(model_name):
        print("\n" + "="*30)
        test_api_call(model_name)
    
    # Step 5: Instructions for TEC integration
    print("\n" + "="*50)
    print("🎯 Next Steps:")
    print("1. Run: python tec_enhanced_api.py")
    print("2. Visit: http://localhost:5000/health")
    print("3. Test NPC creation: /api/game/npc/create")
    print("4. Ready for AI-powered NPCs! 🎮")
    print("="*50)

if __name__ == "__main__":
    main()
