#!/usr/bin/env python3
"""
Debug API responses to understand the error
"""

import requests
import json

def debug_api():
    """Debug what's wrong with the API"""
    
    base_url = "http://localhost:8000"
    
    # Test simple query first
    print("🔍 DEBUGGING API RESPONSE")
    print("=" * 50)
    
    try:
        # Simple test message
        chat_data = {
            "message": "Hello, who are you?"
        }
        
        print(f"📤 Sending request: {chat_data}")
        
        response = requests.post(
            f"{base_url}/chat",
            json=chat_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📥 Response Status: {response.status_code}")
        print(f"📥 Response Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"📥 Response JSON: {json.dumps(response_data, indent=2)}")
        except:
            print(f"📥 Response Text: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    debug_api()
