#!/usr/bin/env python3
"""Check what's in the TEC database"""

import sqlite3
import os

def check_database():
    db_files = ['tec_database.db', 'data/tec_database.db']
    
    for db_file in db_files:
        if os.path.exists(db_file):
            print(f"📁 Found database: {db_file}")
            
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                
                # Check tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                print(f"🗂️  Tables: {[t[0] for t in tables]}")
                
                # Check memories table if it exists
                if any('memories' in str(t) for t in tables):
                    cursor.execute("SELECT COUNT(*) FROM memories")
                    count = cursor.fetchone()[0]
                    print(f"📚 Total memories: {count}")
                    
                    if count > 0:
                        cursor.execute("SELECT character_name, COUNT(*) FROM memories GROUP BY character_name")
                        chars = cursor.fetchall()
                        print(f"👥 Characters: {chars}")
                        
                        # Show some sample memories
                        cursor.execute("SELECT character_name, title, memory_type, emotional_weight FROM memories LIMIT 5")
                        samples = cursor.fetchall()
                        print(f"📖 Sample memories:")
                        for sample in samples:
                            print(f"   {sample[0]}: {sample[1]} ({sample[2]}, weight: {sample[3]})")
                
                conn.close()
                
            except Exception as e:
                print(f"❌ Error reading {db_file}: {e}")
        else:
            print(f"❌ Database not found: {db_file}")

if __name__ == "__main__":
    check_database()
