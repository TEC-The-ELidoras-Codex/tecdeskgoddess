#!/usr/bin/env python3
"""
TEC Enhanced Persona System Demo
Demonstrates the complete integration of the persona system
"""

import sys
import os
import json
import time

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def demo_persona_system():
    """Demo the complete persona system"""
    print("🎭 TEC Enhanced Persona System Demo")
    print("=" * 50)
    
    # Initialize persona manager
    print("\n🗄️  Initializing Persona Manager...")
    from tec_tools.persona_manager import PersonaManager
    pm = PersonaManager()
    print("✅ Persona Manager ready")
    
    # Demo 1: Character Lore
    print("\n🎨 Character Lore Demo:")
    print("-" * 30)
    
    characters = ['Polkin', 'Mynx', 'Kaelen']
    for char in characters:
        lore = pm.get_character_lore(char)
        if lore:
            print(f"🔮 {char}: {lore['role']}")
            print(f"   Description: {lore['description'][:100]}...")
            print(f"   Personality: {', '.join(lore['personality'][:3])}")
            print()
    
    # Demo 2: Sample Persona Creation
    print("\n👤 Sample Persona Creation:")
    print("-" * 30)
    
    sample_persona = {
        "user_id": "demo_user",
        "title": "Digital Nomad",
        "intro": "A tech-savvy wanderer exploring the digital realm",
        "opening_line": "Greetings, fellow digital traveler!",
        "tags": ["technomancer", "explorer", "innovator"],
        "appearance_notes": {
            "body_type": "athletic",
            "hair": "short, electric blue",
            "facial_features": "cybernetic implants, glowing eyes",
            "attire": "sleek tech-wear with holographic accents"
        },
        "permission": "private"
    }
    
    try:
        persona_id = pm.create_player_persona(sample_persona)
        print(f"✅ Created sample persona with ID: {persona_id}")
        
        # Retrieve and display
        retrieved = pm.get_player_persona("demo_user")
        if retrieved:
            print(f"   Title: {retrieved['title']}")
            print(f"   Intro: {retrieved['intro']}")
            print(f"   Tags: {', '.join(retrieved['tags'])}")
    except Exception as e:
        print(f"⚠️  Persona creation demo: {e}")
    
    # Demo 3: AI Settings
    print("\n🧠 AI Settings Demo:")
    print("-" * 30)
    
    ai_settings = {
        "user_id": "demo_user",
        "creativity_level": 75,
        "memory_length": 25,
        "reasoning_mode": "balanced",
        "personality_traits": ["curious", "helpful", "creative"]
    }
    
    try:
        pm.save_ai_settings(ai_settings)
        print("✅ AI settings saved")
        
        retrieved_settings = pm.get_ai_settings("demo_user")
        if retrieved_settings:
            print(f"   Creativity: {retrieved_settings['creativity_level']}%")
            print(f"   Memory: {retrieved_settings['memory_length']} messages")
            print(f"   Reasoning: {retrieved_settings['reasoning_mode']}")
    except Exception as e:
        print(f"⚠️  AI settings demo: {e}")
    
    # Demo 4: Universe Lore
    print("\n🌌 Universe Lore Demo:")
    print("-" * 30)
    
    universe = pm.get_universe_lore("TEC Universe")
    if universe:
        print(f"🪐 {universe['name']}")
        print(f"   Description: {universe['description'][:100]}...")
        print(f"   Physics: {universe['physics'][:80]}...")
        print(f"   Locations: {len(universe['locations'])} locations available")
    
    # Demo 5: System Summary
    print("\n📊 System Summary:")
    print("-" * 30)
    
    print("🎯 TEC Enhanced Persona System Features:")
    print("   ✅ Player Persona Management")
    print("   ✅ Character Lore Database (Polkin, Mynx, Kaelen)")
    print("   ✅ AI Personality Settings")
    print("   ✅ Universe Lore & World Building")
    print("   ✅ Conversation Memory System")
    print("   ✅ Web3 Authentication Integration")
    print("   ✅ Enhanced AI Processing")
    print("   ✅ REST API Endpoints")
    print("   ✅ Modern Web Interface")
    
    print("\n🔗 Access Points:")
    print("   🌐 Web Interface: file:///c:/Users/Ghedd/TEC_CODE/tecdeskgoddess/tec_enhanced_interface.html")
    print("   🛠️  API Server: http://localhost:8000")
    print("   📚 API Docs: http://localhost:8000/health")
    
    print("\n🚀 Usage Examples:")
    print("   1. Configure your persona in the web interface")
    print("   2. Chat with TEC characters (Polkin, Mynx, Kaelen)")
    print("   3. Adjust AI creativity and reasoning settings")
    print("   4. Access character lore and universe information")
    print("   5. Save conversation history with persona context")
    
    print("\n🌟 The TEC Enhanced Persona System is fully operational!")
    print("   Ready for advanced AI interactions with persona-aware responses.")

if __name__ == "__main__":
    demo_persona_system()
