#!/usr/bin/env python3
"""Check the actual character data structure"""

import sqlite3
import json
import os

def check_character_data():
    db_file = 'data/tec_database.db'
    
    if not os.path.exists(db_file):
        print(f"❌ Database not found: {db_file}")
        return
        
    print(f"📁 Checking database: {db_file}")
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Get Polkin's data
        cursor.execute("SELECT character_name, character_data FROM character_lore WHERE character_name LIKE '%Polkin%'")
        polkin_data = cursor.fetchall()
        
        for name, data in polkin_data:
            print(f"\n🎭 CHARACTER: {name}")
            print("=" * 50)
            
            try:
                char_json = json.loads(data)
                print(f"📋 Data structure keys: {list(char_json.keys())}")
                
                # Check for memories
                if 'memories' in char_json:
                    memories = char_json['memories']
                    print(f"📚 Memories count: {len(memories)}")
                    
                    for i, memory in enumerate(memories[:5], 1):
                        print(f"\n  {i}. {memory.get('title', 'No Title')}")
                        print(f"     Type: {memory.get('memory_type', 'Unknown')}")
                        print(f"     Weight: {memory.get('emotional_weight', 'Unknown')}")
                        print(f"     Tags: {memory.get('tags', [])}")
                        content = memory.get('content', '')
                        print(f"     Content: {content[:100]}...")
                
                # Check personality
                if 'personality' in char_json:
                    personality = char_json['personality']
                    print(f"\n🧠 PERSONALITY:")
                    for key, value in personality.items():
                        print(f"  {key}: {value}")
                        
            except json.JSONDecodeError as e:
                print(f"❌ Error parsing JSON: {e}")
                print(f"Raw data: {data[:200]}...")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error reading database: {e}")

if __name__ == "__main__":
    check_character_data()
