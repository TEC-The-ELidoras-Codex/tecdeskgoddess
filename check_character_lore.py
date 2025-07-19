#!/usr/bin/env python3
"""Check the character lore in the data database"""

import sqlite3
import os

def check_character_lore():
    db_file = 'data/tec_database.db'
    
    if not os.path.exists(db_file):
        print(f"❌ Database not found: {db_file}")
        return
        
    print(f"📁 Checking database: {db_file}")
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Check character_lore table
        cursor.execute("PRAGMA table_info(character_lore)")
        columns = cursor.fetchall()
        print(f"📋 character_lore columns: {[col[1] for col in columns]}")
        
        cursor.execute("SELECT COUNT(*) FROM character_lore")
        count = cursor.fetchone()[0]
        print(f"📚 Total character lore entries: {count}")
        
        if count > 0:
            cursor.execute("SELECT character_name, COUNT(*) FROM character_lore GROUP BY character_name")
            chars = cursor.fetchall()
            print(f"👥 Characters with lore: {chars}")
            
            # Show Polkin's lore
            cursor.execute("SELECT title, lore_type, emotional_weight, tags FROM character_lore WHERE character_name = 'Polkin Rishall' LIMIT 10")
            polkin_lore = cursor.fetchall()
            print(f"\n🎭 POLKIN RISHALL LORE:")
            for lore in polkin_lore:
                print(f"   📖 {lore[0]} ({lore[1]}) - Weight: {lore[2]} - Tags: {lore[3]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error reading database: {e}")

if __name__ == "__main__":
    check_character_lore()
