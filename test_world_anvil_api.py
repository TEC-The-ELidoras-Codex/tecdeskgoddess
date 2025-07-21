#!/usr/bin/env python3
"""
🎯 TEC Lore Forge - Live API Test
Test actual World Anvil API connection with your credentials
"""

import sys
import os

# Add current directory to path
sys.path.append('.')

# Import our secure credentials
try:
    import api_credentials
    api_credentials.setup_api_credentials()
    print("🔐 API credentials loaded successfully!")
except ImportError:
    print("❌ Could not load api_credentials.py")
    exit(1)

# Test World Anvil API connection
import requests

def test_world_anvil_connection():
    """Test if we can connect to World Anvil API"""
    
    token = os.getenv('WORLD_ANVIL_TOKEN')
    if not token:
        print("❌ WORLD_ANVIL_TOKEN not found in environment")
        return False
        
    print(f"🔑 Testing World Anvil API with token: {token[:20]}...{token[-20:]}")
    
    # Test API connection
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        # Test with a simple API call to get user info
        response = requests.get(
            "https://www.worldanvil.com/api/boromir/user",
            headers=headers,
            timeout=10
        )
        
        print(f"📡 API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Connected to World Anvil successfully!")
            print(f"👤 User: {user_data.get('username', 'Unknown')}")
            return True
        elif response.status_code == 401:
            print("❌ Authentication failed - check your API token")
            return False
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False

def test_world_anvil_worlds():
    """Test if we can get user's worlds"""
    
    token = os.getenv('WORLD_ANVIL_TOKEN')
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(
            "https://www.worldanvil.com/api/boromir/worlds",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            worlds = response.json()
            print(f"🌍 Found {len(worlds.get('data', []))} worlds:")
            
            for world in worlds.get('data', [])[:3]:  # Show first 3 worlds
                print(f"   • {world.get('title', 'Untitled')} (ID: {world.get('id')})")
                
            return worlds.get('data', [])
        else:
            print(f"❌ Could not fetch worlds: {response.status_code}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching worlds: {e}")
        return []

if __name__ == "__main__":
    print("🎯 TEC LORE FORGE - LIVE API TEST")
    print("=" * 50)
    
    # Test API connection
    if test_world_anvil_connection():
        print("\n🌍 Testing World Access...")
        worlds = test_world_anvil_worlds()
        
        if worlds:
            print(f"\n🚀 TEC Lore Forge is ready for deployment!")
            print(f"💡 Use world ID from above in your notebook for live generator creation")
        else:
            print(f"\n⚠️  No worlds found - you may need to create a world in World Anvil first")
    else:
        print(f"\n❌ API connection failed - please check your credentials")
        
    print("\n" + "=" * 50)
