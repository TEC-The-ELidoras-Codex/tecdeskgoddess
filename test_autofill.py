#!/usr/bin/env python3
"""
Test the AI Autofill Persona Feature
Tests the new /api/persona/autofill endpoint
"""

import requests
import json

def test_autofill_endpoint():
    """Test the AI autofill persona generation"""
    
    # Test different themes
    themes = ['balanced', 'mystical', 'tech', 'rebel', 'light', 'dark']
    
    print("🤖 Testing AI Persona Autofill Feature")
    print("=" * 50)
    
    for theme in themes:
        print(f"\n🎨 Testing {theme.upper()} theme...")
        
        try:
            # Test with random faction
            response = requests.post('http://localhost:8000/api/persona/autofill', 
                json={'theme': theme})
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    persona = data['persona']
                    print(f"✅ Success! Generated: {persona['title']}")
                    print(f"   Faction: {data['faction']}")
                    print(f"   Opening: {persona['opening']}")
                    print(f"   Tags: {persona['tags']}")
                    print(f"   Appearance: {persona['appearance']['body_type']}, {persona['appearance']['hair']}")
                else:
                    print(f"❌ API Error: {data.get('error', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Connection Error: {e}")
    
    # Test with specific faction
    print(f"\n🏛️ Testing with specific faction...")
    try:
        response = requests.post('http://localhost:8000/api/persona/autofill', 
            json={'theme': 'mystical', 'faction': 'Ethereal Architects'})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                persona = data['persona']
                print(f"✅ Success! Generated: {persona['title']}")
                print(f"   Faction: {data['faction']}")
                print(f"   Theme: {data['theme']}")
                print(f"   Introduction: {persona['introduction'][:100]}...")
            else:
                print(f"❌ API Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    
    print("\n🎉 AI Autofill Test Complete!")

if __name__ == "__main__":
    test_autofill_endpoint()
