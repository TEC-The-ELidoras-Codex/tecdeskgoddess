#!/usr/bin/env python3
"""
TEC: BITLYFE API Key Configuration Wizard
The Creator's Rebellion - Secure API Setup

This script helps you securely configure API keys for the TEC system.
"""

import os
import sys
from pathlib import Path

def main():
    print("🔑 TEC: BITLYFE API Configuration Wizard")
    print("=" * 50)
    
    # Create .env file from template if it doesn't exist
    env_file = Path(".env")
    template_file = Path("config/.env.template")
    
    if not env_file.exists() and template_file.exists():
        print("📋 Creating .env from template...")
        import shutil
        shutil.copy(template_file, env_file)
        print("✅ .env file created")
    
    print("\n🚨 SECURITY WARNING:")
    print("- NEVER commit API keys to git repositories")
    print("- Store keys securely and rotate them regularly")
    print("- Monitor usage in provider dashboards")
    
    print("\n📖 For detailed setup instructions, see:")
    print("   docs/API_CONFIGURATION_GUIDE.md")
    
    print("\n🔧 API Keys You Need to Configure:")
    
    # Check which keys are configured
    required_keys = {
        'GITHUB_TOKEN': 'GitHub AI Models (Required for Copilot)',
        'OPENAI_API_KEY': 'OpenAI GPT-4, DALL-E (Recommended)',
        'ANTHROPIC_API_KEY': 'Claude AI (Recommended)', 
        'XAI_API_KEY': 'Grok/XAI (Uncensored AI)',
        'GEMINI_API_KEY': 'Google Gemini (Free tier)',
        'AZURE_API_KEY_1': 'Azure AI Services (Your TEC resource)',
        'ELEVENLABS_API_KEY': 'Voice/Audio (Optional)',
        'COINGECKO_API_KEY': 'Crypto data (Optional)'
    }
    
    # Load current .env
    env_vars = {}
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    
    print("\n📊 Current Configuration Status:")
    for key, description in required_keys.items():
        value = env_vars.get(key, '')
        if value and not value.startswith('your_') and len(value) > 10:
            status = "✅ CONFIGURED"
        else:
            status = "❌ MISSING"
        print(f"   {status} {key}: {description}")
    
    print("\n🚀 Next Steps:")
    print("1. Edit .env file with your actual API keys")
    print("2. Run: python scripts/test_api_keys.py")
    print("3. Start TEC: python main.py")
    
    # Offer to open .env file
    try:
        import subprocess
        response = input("\n📝 Open .env file for editing? (y/n): ").lower()
        if response == 'y':
            if sys.platform == "win32":
                subprocess.run(['notepad', str(env_file)])
            elif sys.platform == "darwin":
                subprocess.run(['open', str(env_file)])
            else:
                subprocess.run(['nano', str(env_file)])
    except:
        print(f"💡 Manually edit: {env_file}")

if __name__ == "__main__":
    main()
