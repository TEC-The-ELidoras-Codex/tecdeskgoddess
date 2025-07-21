#!/usr/bin/env python3
"""
🔐 TEC Lore Forge - Secure Environment Setup
This script safely sets environment variables for API credentials
"""

import os
import subprocess
import sys

def setup_environment():
    """Setup environment variables for TEC Lore Forge"""
    
    print("🔐 TEC LORE FORGE - SECURE ENVIRONMENT SETUP")
    print("=" * 50)
    
    # Get credentials from user input (not hardcoded)
    print("Please enter your API credentials:")
    world_anvil_key = input("World Anvil API Key: ").strip()
    github_token = input("GitHub Token: ").strip()
    
    # Set environment variables for current session
    os.environ['WORLD_ANVIL_API_KEY'] = world_anvil_key
    os.environ['GITHUB_TOKEN'] = github_token
    
    print("✅ Environment variables set for current session")
    print("✅ World Anvil API Key: CONFIGURED")
    print("✅ GitHub Token: CONFIGURED")
    
    # For PowerShell persistent environment (Windows)
    if sys.platform == "win32":
        try:
            # Set user environment variables
            subprocess.run([
                "powershell", "-Command", 
                f"[Environment]::SetEnvironmentVariable('WORLD_ANVIL_API_KEY', '{world_anvil_key}', 'User')"
            ], check=True, capture_output=True)
            
            subprocess.run([
                "powershell", "-Command",
                f"[Environment]::SetEnvironmentVariable('GITHUB_TOKEN', '{github_token}', 'User')"
            ], check=True, capture_output=True)
            
            print("✅ Persistent environment variables set for Windows user")
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Could not set persistent environment variables: {e}")
            print("Environment variables are set for current session only")
    
    print("\n🚀 TEC Lore Forge is ready for live deployment!")
    print("🎯 You can now run the notebook with real API credentials")
    
    return True

if __name__ == "__main__":
    setup_environment()
