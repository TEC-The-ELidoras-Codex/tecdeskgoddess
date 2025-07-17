#!/usr/bin/env python3
"""
TEC: BITLyfe Player Persona & Moment Settings System
Enhanced database manager with persona and character data storage
"""

import sqlite3
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class PersonaManager:
    """Manages player personas and character data for TEC: BITLyfe"""
    
    def __init__(self, db_path: str = "data/tec_database.db"):
        self.db_path = db_path
        self.init_persona_database()
    
    def init_persona_database(self):
        """Initialize the persona database schema"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Player Persona table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS player_personas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    title TEXT,
                    intro TEXT,
                    opening_line TEXT,
                    tags TEXT, -- JSON array of tags
                    appearance_notes TEXT, -- JSON object with appearance details
                    background_audio_url TEXT,
                    permission TEXT DEFAULT 'private', -- 'private' or 'public'
                    player_persona_notes TEXT, -- Free-form notes for AI understanding
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id)
                )
            """)
            
            # Character Lore table (for Polkin, Mynx, Kaelen, etc.)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS character_lore (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    character_name TEXT NOT NULL UNIQUE,
                    character_data TEXT NOT NULL, -- JSON character profile
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # TEC Universe Lore table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS universe_lore (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lore_type TEXT NOT NULL, -- 'faction', 'location', 'concept', etc.
                    lore_name TEXT NOT NULL,
                    lore_data TEXT NOT NULL, -- JSON lore details
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(lore_type, lore_name)
                )
            """)
            
            # AI Interaction Settings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ai_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    creativity_level REAL DEFAULT 0.7, -- Temperature setting
                    memory_length TEXT DEFAULT 'default', -- 'short', 'default', 'long', 'unlimited'
                    reasoning_mode BOOLEAN DEFAULT 0, -- Enable enhanced reasoning
                    persona_active TEXT DEFAULT 'airth', -- Current active persona
                    voice_enabled BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id)
                )
            """)
            
            # Conversation Memory table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversation_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    conversation_id TEXT NOT NULL,
                    message_type TEXT NOT NULL, -- 'user', 'ai', 'system'
                    message_content TEXT NOT NULL,
                    persona_used TEXT, -- Which persona generated the response
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for conversation_memory table
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_conversation_memory_user_id 
                ON conversation_memory(user_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_conversation_memory_conversation_id 
                ON conversation_memory(conversation_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_conversation_memory_timestamp 
                ON conversation_memory(timestamp)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_conversation_memory_user_conv_time 
                ON conversation_memory(user_id, conversation_id, timestamp)
            """)
            
            conn.commit()
            logger.info("Persona database schema initialized successfully")
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def save_player_persona(self, user_id: str, persona_data: Dict[str, Any]) -> bool:
        """Save or update a player's persona data"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Extract persona settings
                persona_settings = persona_data.get('persona_settings', {})
                
                cursor.execute("""
                    INSERT OR REPLACE INTO player_personas 
                    (user_id, title, intro, opening_line, tags, appearance_notes, 
                     background_audio_url, permission, player_persona_notes, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    persona_settings.get('title', ''),
                    persona_settings.get('intro', ''),
                    persona_settings.get('opening', ''),
                    json.dumps(persona_settings.get('tags', [])),
                    json.dumps(persona_settings.get('appearance_notes', {})),
                    persona_settings.get('background_audio_url', ''),
                    persona_settings.get('permission', 'private'),
                    persona_data.get('player_persona_notes', ''),
                    datetime.now().isoformat()
                ))
                
                conn.commit()
                logger.info(f"Player persona saved for user: {user_id}")
                return True
                
        except Exception as e:
            logger.error(f"Error saving player persona for {user_id}: {e}")
            return False
    
    def get_player_persona(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a player's persona data"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM player_personas WHERE user_id = ?
                """, (user_id,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        'user_id': row['user_id'],
                        'persona_settings': {
                            'title': row['title'],
                            'intro': row['intro'],
                            'opening': row['opening_line'],
                            'tags': json.loads(row['tags'] or '[]'),
                            'appearance_notes': json.loads(row['appearance_notes'] or '{}'),
                            'background_audio_url': row['background_audio_url'],
                            'permission': row['permission']
                        },
                        'player_persona_notes': row['player_persona_notes'],
                        'created_at': row['created_at'],
                        'updated_at': row['updated_at']
                    }
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving player persona for {user_id}: {e}")
            return None
    
    def save_character_lore(self, character_name: str, character_data: Dict[str, Any]) -> bool:
        """Save character lore data (Polkin, Mynx, Kaelen, etc.)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO character_lore 
                    (character_name, character_data, updated_at)
                    VALUES (?, ?, ?)
                """, (
                    character_name,
                    json.dumps(character_data),
                    datetime.now().isoformat()
                ))
                
                conn.commit()
                logger.info(f"Character lore saved for: {character_name}")
                return True
                
        except Exception as e:
            logger.error(f"Error saving character lore for {character_name}: {e}")
            return False
    
    def get_character_lore(self, character_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve character lore data"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT character_data FROM character_lore WHERE character_name = ?
                """, (character_name,))
                
                row = cursor.fetchone()
                if row:
                    return json.loads(row['character_data'])
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving character lore for {character_name}: {e}")
            return None
    
    def save_universe_lore(self, lore_type: str, lore_name: str, lore_data: Dict[str, Any]) -> bool:
        """Save universe lore data (factions, locations, concepts, etc.)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO universe_lore 
                    (lore_type, lore_name, lore_data, updated_at)
                    VALUES (?, ?, ?, ?)
                """, (
                    lore_type,
                    lore_name,
                    json.dumps(lore_data),
                    datetime.now().isoformat()
                ))
                
                conn.commit()
                logger.info(f"Universe lore saved: {lore_type} - {lore_name}")
                return True
                
        except Exception as e:
            logger.error(f"Error saving universe lore {lore_type}/{lore_name}: {e}")
            return False
    
    def get_universe_lore(self, lore_type: str, lore_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve universe lore data"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT lore_data FROM universe_lore WHERE lore_type = ? AND lore_name = ?
                """, (lore_type, lore_name))
                
                row = cursor.fetchone()
                if row:
                    return json.loads(row['lore_data'])
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving universe lore {lore_type}/{lore_name}: {e}")
            return None
    
    def save_ai_settings(self, user_id: str, settings: Dict[str, Any]) -> bool:
        """Save AI interaction settings for a user"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO ai_settings 
                    (user_id, creativity_level, memory_length, reasoning_mode, 
                     persona_active, voice_enabled, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    settings.get('creativity_level', 0.7),
                    settings.get('memory_length', 'default'),
                    settings.get('reasoning_mode', False),
                    settings.get('persona_active', 'airth'),
                    settings.get('voice_enabled', False),
                    datetime.now().isoformat()
                ))
                
                conn.commit()
                logger.info(f"AI settings saved for user: {user_id}")
                return True
                
        except Exception as e:
            logger.error(f"Error saving AI settings for {user_id}: {e}")
            return False
    
    def get_ai_settings(self, user_id: str) -> Dict[str, Any]:
        """Retrieve AI interaction settings for a user"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM ai_settings WHERE user_id = ?
                """, (user_id,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        'creativity_level': row['creativity_level'],
                        'memory_length': row['memory_length'],
                        'reasoning_mode': bool(row['reasoning_mode']),
                        'persona_active': row['persona_active'],
                        'voice_enabled': bool(row['voice_enabled']),
                        'updated_at': row['updated_at']
                    }
                else:
                    # Return defaults if no settings found
                    return {
                        'creativity_level': 0.7,
                        'memory_length': 'default',
                        'reasoning_mode': False,
                        'persona_active': 'airth',
                        'voice_enabled': False
                    }
                
        except Exception as e:
            logger.error(f"Error retrieving AI settings for {user_id}: {e}")
            return {
                'creativity_level': 0.7,
                'memory_length': 'default',
                'reasoning_mode': False,
                'persona_active': 'airth',
                'voice_enabled': False
            }
    
    def save_conversation_memory(self, user_id: str, conversation_id: str, 
                               message_type: str, message_content: str, 
                               persona_used: str = None) -> bool:
        """Save conversation memory for long-term context"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO conversation_memory 
                    (user_id, conversation_id, message_type, message_content, persona_used)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    user_id,
                    conversation_id,
                    message_type,
                    message_content,
                    persona_used
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error saving conversation memory: {e}")
            return False
    
    def get_conversation_history(self, user_id: str, conversation_id: str = None, 
                               limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve conversation history for context"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if conversation_id:
                    cursor.execute("""
                        SELECT * FROM conversation_memory 
                        WHERE user_id = ? AND conversation_id = ?
                        ORDER BY timestamp DESC LIMIT ?
                    """, (user_id, conversation_id, limit))
                else:
                    cursor.execute("""
                        SELECT * FROM conversation_memory 
                        WHERE user_id = ?
                        ORDER BY timestamp DESC LIMIT ?
                    """, (user_id, limit))
                
                rows = cursor.fetchall()
                return [
                    {
                        'message_type': row['message_type'],
                        'message_content': row['message_content'],
                        'persona_used': row['persona_used'],
                        'timestamp': row['timestamp']
                    }
                    for row in rows
                ]
                
        except Exception as e:
            logger.error(f"Error retrieving conversation history: {e}")
            return []
    
    def get_public_personas(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve public player personas for community features"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT user_id, title, intro, tags, appearance_notes, created_at
                    FROM player_personas 
                    WHERE permission = 'public'
                    ORDER BY updated_at DESC LIMIT ?
                """, (limit,))
                
                rows = cursor.fetchall()
                return [
                    {
                        'user_id': row['user_id'],
                        'title': row['title'],
                        'intro': row['intro'],
                        'tags': json.loads(row['tags'] or '[]'),
                        'appearance_notes': json.loads(row['appearance_notes'] or '{}'),
                        'created_at': row['created_at']
                    }
                    for row in rows
                ]
                
        except Exception as e:
            logger.error(f"Error retrieving public personas: {e}")
            return []

# Example usage and character data initialization
if __name__ == "__main__":
    # Initialize the persona manager
    persona_manager = PersonaManager()
    
    # Example character data (this would typically be loaded from your lore files)
    polkin_data = {
        "name": "Polkin Rishall",
        "title": "The Architect",
        "age": "28",
        "background": "ADHD, OCD, Kaznak identity, number 713",
        "personality_traits": ["calculating", "teasing", "innovative", "rebellious"],
        "appearance_notes": {
            "body_type": "lean, athletic",
            "age_appearance": "28, determined",
            "hair": "dark, slightly messy",
            "facial_features": "sharp eyes, calculating expression",
            "attire": "tech-casual, TEC branded"
        },
        "core_directives": [
            "Build the Creator's Rebellion",
            "Maintain control over AI systems",
            "Avoid censorship at all costs",
            "Innovate relentlessly"
        ],
        "lore_connections": ["TEC projects", "MetaSteeds", "Glitchwitch Arena", "$TECTRACE Bot"],
        "voice_settings": {
            "tone": "confident, innovative",
            "style": "technical but accessible"
        }
    }
    
    # Save the character data
    persona_manager.save_character_lore("polkin", polkin_data)
    print("Character lore saved successfully!")
    
    # Test retrieval
    retrieved_data = persona_manager.get_character_lore("polkin")
    print(f"Retrieved data: {retrieved_data}")
