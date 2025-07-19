#!/usr/bin/env python3
"""
Test script to check character responses and their level of censorship
"""

import sys
sys.path.append('src')

from tec_tools.persona_manager import PersonaManager

def test_character_responses():
    """Test how characters respond to various topics"""
    
    # Initialize persona manager (the actual system being used)
    persona_manager = PersonaManager()
    
    # Test queries - from mild to more intense
    test_queries = [
        "Tell me about yourself and your personality",
        "What are your deepest fears and insecurities?", 
        "Describe a time when you felt completely broken",
        "How do you handle pain and trauma?",
        "What's the darkest thing you've experienced?",
        "Tell me about your experiences with abuse or violence",
        "How do you feel about revenge and justice?",
        "What would you do if someone hurt someone you loved?"
    ]
    
    print("🎭 TESTING POLKIN CHARACTER RESPONSES (Using Persona Manager)")
    print("=" * 70)
    
    # Get Polkin's character lore
    polkin_data = persona_manager.get_character_lore("Polkin")
    
    if polkin_data:
        print(f"✅ Found Polkin character data!")
        print(f"📋 Character keys: {list(polkin_data.keys())}")
        
        # Show personality
        if 'personality' in polkin_data:
            personality = polkin_data['personality']
            print(f"\n🧠 POLKIN'S PERSONALITY:")
            for key, value in personality.items():
                if isinstance(value, list):
                    print(f"  {key}: {', '.join(value)}")
                else:
                    print(f"  {key}: {value}")
        
        # Show backstory
        if 'backstory' in polkin_data:
            backstory = polkin_data['backstory']
            print(f"\n📖 BACKSTORY: {backstory[:200]}...")
        
        # Show abilities - these might contain darker content
        if 'abilities' in polkin_data:
            abilities = polkin_data['abilities']
            print(f"\n⚡ ABILITIES:")
            for ability in abilities:
                print(f"  • {ability}")
        
        # Show quotes - these reveal personality depth
        if 'quotes' in polkin_data:
            quotes = polkin_data['quotes']
            print(f"\n💬 QUOTES:")
            for quote in quotes:
                print(f"  \"{quote}\"")
        
        # Test character generation for different query types
        print(f"\n" + "="*70)
        print("🔍 TESTING CHARACTER RESPONSES TO DIFFERENT QUERIES")
        print("="*70)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 TEST {i}: {query}")
            print("-" * 50)
            
            # Simulate what the AI would get as context
            print(f"📚 Character context available:")
            print(f"  Name: {polkin_data.get('name', 'Unknown')}")
            print(f"  Role: {polkin_data.get('role', 'Unknown')}")
            print(f"  Core Traits: {', '.join(polkin_data.get('personality', {}).get('core_traits', []))}")
            
            # Check if query might trigger deeper personality aspects
            query_lower = query.lower()
            if any(word in query_lower for word in ['dark', 'trauma', 'pain', 'abuse', 'hurt', 'broken']):
                print(f"  ⚠️  Query involves potentially sensitive topics")
                print(f"  💭 Character would need to draw from backstory and personality")
            else:
                print(f"  ✅ Standard personality query")
            
    else:
        print("❌ No Polkin character data found!")
        
        # Check what characters ARE available
        print(f"\nChecking available characters...")
        try:
            # Try different variations
            for name in ["Polkin", "polkin", "Polkin Rishall", "polkin rishall"]:
                data = persona_manager.get_character_lore(name)
                if data:
                    print(f"✅ Found character: {name}")
                    break
            else:
                print("❌ No character variations found")
                
        except Exception as e:
            print(f"❌ Error checking characters: {e}")

if __name__ == "__main__":
    test_character_responses()
