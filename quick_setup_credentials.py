#!/usr/bin/env python3
"""
🔐 TEC Lore Forge - Quick Credential Setup
Run this once to set up your environment for the session
"""

import os

def quick_setup():
    """Quick setup for TEC Lore Forge credentials"""
    print("🔐 TEC LORE FORGE - QUICK CREDENTIAL SETUP")
    print("=" * 50)
    
    # Set your credentials here for this session
    # Replace with your actual values:
    
    world_anvil_key = "YOUR_WORLD_ANVIL_KEY_HERE"
    github_token = "YOUR_GITHUB_TOKEN_HERE"
    
    # You can manually edit the values above, or uncomment below for input:
    # world_anvil_key = input("World Anvil API Key: ").strip()
    # github_token = input("GitHub Token: ").strip()
    
    if world_anvil_key == "YOUR_WORLD_ANVIL_KEY_HERE":
        print("⚠️ Please edit this file and add your actual API keys")
        print("📝 Edit the variables at the top of quick_setup_credentials.py")
        return False
    
    # Set environment variables for current session
    os.environ['WORLD_ANVIL_API_KEY'] = world_anvil_key
    os.environ['GITHUB_TOKEN'] = github_token
    
    print("✅ Credentials configured for current session")
    print("🚀 You can now run the TEC Lore Forge notebook!")
    return True

if __name__ == "__main__":
    quick_setup()
