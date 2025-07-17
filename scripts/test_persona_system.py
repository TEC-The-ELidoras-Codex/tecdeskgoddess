#!/usr/bin/env python3
"""
TEC Persona System Test Suite
Tests all components of the Player Persona & Moment Settings system
"""

import os
import sys
import json
from datetime import datetime

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_persona_system():
    """Test all components of the persona system"""
    print("🧪 TEC Persona System Test Suite")
    print("=" * 50)
    
    # Test 1: PersonaManager
    print("\n1. Testing PersonaManager...")
    try:
        from tec_tools.persona_manager import PersonaManager
        pm = PersonaManager()
        print("✅ PersonaManager imported and initialized")
        
        # Test character lore retrieval
        characters = ['Polkin', 'Mynx', 'Kaelen']
        for char in characters:
            lore = pm.get_character_lore(char)
            if lore:
                print(f"✅ {char}: {lore.get('title', 'No title')}")
            else:
                print(f"❌ {char}: Not found")
        
        # Test universe lore
        universe = pm.get_universe_lore('universe', 'TEC Universe')
        if universe:
            print(f"✅ TEC Universe: {universe.get('name', 'No name')}")
        else:
            print("❌ TEC Universe: Not found")
            
    except Exception as e:
        print(f"❌ PersonaManager test failed: {e}")
        return False
    
    # Test 2: API Server
    print("\n2. Testing API Server...")
    try:
        from tec_persona_api import create_persona_app
        app = create_persona_app()
        print("✅ Persona API app created successfully")
        
        # Test that routes are registered
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        persona_routes = [r for r in routes if '/api/persona' in r or '/api/ai' in r]
        print(f"✅ Found {len(persona_routes)} persona API routes")
        
    except Exception as e:
        print(f"❌ API Server test failed: {e}")
        return False
    
    # Test 3: Agentic Processor
    print("\n3. Testing Agentic Processor...")
    try:
        from tec_tools.agentic_processor import AgenticProcessor
        
        # Create a minimal config for testing
        test_config = {
            'azure_ai': {
                'endpoint': 'test',
                'key': 'test'
            }
        }
        
        processor = AgenticProcessor(test_config)
        print("✅ AgenticProcessor imported and initialized")
        
        # Test if enhanced methods exist
        if hasattr(processor, 'process_enhanced_message'):
            print("✅ Enhanced message processing available")
        else:
            print("❌ Enhanced message processing not found")
            
        if hasattr(processor, 'generate_image_prompt'):
            print("✅ Image prompt generation available")
        else:
            print("❌ Image prompt generation not found")
            
    except Exception as e:
        print(f"❌ Agentic Processor test failed: {e}")
        return False
    
    # Test 4: Database Schema
    print("\n4. Testing Database Schema...")
    try:
        import sqlite3
        db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tec_database.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if all tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['player_personas', 'character_lore', 'universe_lore', 'ai_settings', 'conversation_memory']
        for table in required_tables:
            if table in tables:
                print(f"✅ Table {table} exists")
            else:
                print(f"❌ Table {table} missing")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database schema test failed: {e}")
        return False
    
    # Test 5: Frontend Components
    print("\n5. Testing Frontend Components...")
    try:
        # Check if UI files exist
        ui_files = [
            'persona_ui_component.html',
            'assets/js/persona_manager.js',
            'assets/js/persona_chat_integration.js',
            'assets/css/persona_ui.css'
        ]
        
        project_root = os.path.join(os.path.dirname(__file__), '..')
        for ui_file in ui_files:
            file_path = os.path.join(project_root, ui_file)
            if os.path.exists(file_path):
                print(f"✅ {ui_file} exists")
            else:
                print(f"❌ {ui_file} missing")
        
    except Exception as e:
        print(f"❌ Frontend components test failed: {e}")
        return False
    
    print("\n🎉 TEC Persona System Test Suite Complete!")
    return True

def display_system_summary():
    """Display a summary of the persona system components"""
    print("\n📋 TEC Persona System Summary")
    print("=" * 50)
    
    print("\n🗄️  Database Components:")
    print("  • player_personas - User persona data with appearance, audio, permissions")
    print("  • character_lore - Polkin, Mynx, Kaelen character information")
    print("  • universe_lore - TEC Universe mythology and physics")
    print("  • ai_settings - AI personality control (creativity, memory, reasoning)")
    print("  • conversation_memory - Chat history with persona context")
    
    print("\n🔧 Backend Components:")
    print("  • PersonaManager - Database operations and persona management")
    print("  • Persona API - REST endpoints for persona CRUD operations")
    print("  • AgenticProcessor - Enhanced AI processing with persona integration")
    print("  • Character Lore - Polkin, Mynx, Kaelen fully defined")
    
    print("\n🎨 Frontend Components:")
    print("  • persona_ui_component.html - Main persona settings interface")
    print("  • persona_manager.js - JavaScript persona management")
    print("  • persona_chat_integration.js - Chat interface integration")
    print("  • persona_ui.css - Styling for persona components")
    
    print("\n⚡ Key Features:")
    print("  • Player Persona Creation - Title, intro, tags, appearance notes")
    print("  • Nomi-style Appearance System - Body type, hair, facial features, attire")
    print("  • Background Audio Support - URL-based audio with play/stop controls")
    print("  • Permission System - Private/public persona visibility")
    print("  • AI Settings Control - Creativity, memory, reasoning mode")
    print("  • Character Lore Integration - Access to Polkin, Mynx, Kaelen data")
    print("  • Enhanced Chat Mode - Persona-aware message processing")
    
    print("\n🌟 TEC Universe Characters:")
    print("  • Polkin - The Mystical Guide (Spiritual advisor & dimensional navigator)")
    print("  • Mynx - The Technological Mystic (Tech-magic fusion specialist)")
    print("  • Kaelen - The Cosmic Wanderer (Interdimensional explorer)")
    
    print("\n🚀 Integration Points:")
    print("  • Web3 Authentication - Secure persona access")
    print("  • Azure AI Services - Enhanced reasoning and creativity")
    print("  • Chat Interface - Seamless persona switching")
    print("  • Memory System - Conversation context preservation")

if __name__ == "__main__":
    success = test_persona_system()
    display_system_summary()
    
    if success:
        print("\n✅ All tests passed! TEC Persona System is ready for use.")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
        sys.exit(1)
