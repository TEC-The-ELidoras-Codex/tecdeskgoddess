#!/usr/bin/env python3
"""
TEC: BITLYFE - Enhanced Database with Personalization & Memory System
Replika-style customization and quest management
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TECPersonalizationDB:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), 'tec_personalization.db')
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize the enhanced database with personalization tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User profile table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            ai_companion_name TEXT DEFAULT 'Daisy Purecode',
            personality_traits TEXT DEFAULT '{}',
            avatar_settings TEXT DEFAULT '{}',
            preferences TEXT DEFAULT '{}',
            level INTEGER DEFAULT 1,
            total_xp INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Enhanced memory system
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            content TEXT NOT NULL,
            category TEXT,
            importance_score INTEGER DEFAULT 1,
            tags TEXT DEFAULT '[]',
            emotional_context TEXT,
            related_quest_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_profile (id)
        )
        ''')
        
        # Quest system
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS quests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            quest_type TEXT DEFAULT 'custom',
            status TEXT DEFAULT 'active',
            xp_reward INTEGER DEFAULT 50,
            progress INTEGER DEFAULT 0,
            max_progress INTEGER DEFAULT 100,
            difficulty TEXT DEFAULT 'easy',
            tags TEXT DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_profile (id)
        )
        ''')
        
        # Enhanced conversation history with context
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_message TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            context_data TEXT DEFAULT '{}',
            emotional_tone TEXT,
            session_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_profile (id)
        )
        ''')
        
        # Achievements system
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            icon TEXT,
            xp_value INTEGER DEFAULT 100,
            unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_profile (id)
        )
        ''')
        
        # Personal facts and preferences
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS personal_facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            fact_type TEXT NOT NULL,
            fact_value TEXT NOT NULL,
            confidence_score REAL DEFAULT 1.0,
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_profile (id)
        )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Enhanced TEC database initialized successfully")

    def create_user_profile(self, username: str, ai_companion_name: str = "Daisy Purecode") -> int:
        """Create a new user profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            INSERT INTO user_profile (username, ai_companion_name)
            VALUES (?, ?)
            ''', (username, ai_companion_name))
            
            user_id = cursor.lastrowid
            conn.commit()
            
            # Create default quests for new user
            self._create_default_quests(user_id)
            
            logger.info(f"Created user profile for {username} with ID {user_id}")
            return user_id
            
        except sqlite3.IntegrityError:
            logger.warning(f"User {username} already exists")
            cursor.execute('SELECT id FROM user_profile WHERE username = ?', (username,))
            return cursor.fetchone()[0]
        finally:
            conn.close()

    def get_user_profile(self, user_id: int) -> Optional[Dict]:
        """Get user profile with all customizations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM user_profile WHERE id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        if row:
            columns = [description[0] for description in cursor.description]
            profile = dict(zip(columns, row))
            
            # Parse JSON fields
            profile['personality_traits'] = json.loads(profile['personality_traits'])
            profile['avatar_settings'] = json.loads(profile['avatar_settings'])
            profile['preferences'] = json.loads(profile['preferences'])
            
            conn.close()
            return profile
        
        conn.close()
        return None

    def update_ai_companion_name(self, user_id: int, new_name: str) -> bool:
        """Update the AI companion's name"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        UPDATE user_profile 
        SET ai_companion_name = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        ''', (new_name, user_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        if success:
            logger.info(f"Updated AI companion name to '{new_name}' for user {user_id}")
        
        return success

    def add_memory(self, user_id: int, content: str, category: str = "general", 
                   importance: int = 1, tags: List[str] = None, 
                   emotional_context: str = None) -> int:
        """Add a memory with context and categorization"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        tags_json = json.dumps(tags or [])
        
        cursor.execute('''
        INSERT INTO memories (user_id, content, category, importance_score, tags, emotional_context)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, content, category, importance, tags_json, emotional_context))
        
        memory_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Added memory {memory_id} for user {user_id}: {category}")
        return memory_id

    def get_relevant_memories(self, user_id: int, keywords: List[str] = None, 
                            category: str = None, limit: int = 10) -> List[Dict]:
        """Retrieve relevant memories for context"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
        SELECT * FROM memories 
        WHERE user_id = ?
        '''
        params = [user_id]
        
        if category:
            query += ' AND category = ?'
            params.append(category)
        
        if keywords:
            # Simple keyword matching - can be enhanced with vector search later
            keyword_conditions = ' OR '.join(['content LIKE ?' for _ in keywords])
            query += f' AND ({keyword_conditions})'
            params.extend([f'%{keyword}%' for keyword in keywords])
        
        query += ' ORDER BY importance_score DESC, created_at DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        columns = [description[0] for description in cursor.description]
        memories = []
        
        for row in rows:
            memory = dict(zip(columns, row))
            memory['tags'] = json.loads(memory['tags'])
            memories.append(memory)
        
        conn.close()
        return memories

    def create_quest(self, user_id: int, title: str, description: str = "", 
                    quest_type: str = "custom", xp_reward: int = 50,
                    difficulty: str = "easy", tags: List[str] = None) -> int:
        """Create a new quest"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        tags_json = json.dumps(tags or [])
        
        cursor.execute('''
        INSERT INTO quests (user_id, title, description, quest_type, xp_reward, difficulty, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, title, description, quest_type, xp_reward, difficulty, tags_json))
        
        quest_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Created quest {quest_id} for user {user_id}: {title}")
        return quest_id

    def get_active_quests(self, user_id: int) -> List[Dict]:
        """Get all active quests for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM quests 
        WHERE user_id = ? AND status = 'active'
        ORDER BY created_at DESC
        ''', (user_id,))
        
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        quests = []
        for row in rows:
            quest = dict(zip(columns, row))
            quest['tags'] = json.loads(quest['tags'])
            quests.append(quest)
        
        conn.close()
        return quests

    def complete_quest(self, quest_id: int) -> bool:
        """Mark a quest as completed and award XP"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get quest details
        cursor.execute('SELECT user_id, xp_reward FROM quests WHERE id = ?', (quest_id,))
        quest_data = cursor.fetchone()
        
        if not quest_data:
            conn.close()
            return False
        
        user_id, xp_reward = quest_data
        
        # Update quest status
        cursor.execute('''
        UPDATE quests 
        SET status = 'completed', completed_at = CURRENT_TIMESTAMP
        WHERE id = ?
        ''', (quest_id,))
        
        # Award XP to user
        cursor.execute('''
        UPDATE user_profile 
        SET total_xp = total_xp + ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        ''', (xp_reward, user_id))
        
        # Check for level up (every 1000 XP = 1 level)
        cursor.execute('SELECT total_xp FROM user_profile WHERE id = ?', (user_id,))
        total_xp = cursor.fetchone()[0]
        new_level = (total_xp // 1000) + 1
        
        cursor.execute('''
        UPDATE user_profile 
        SET level = ?
        WHERE id = ?
        ''', (new_level, user_id))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Completed quest {quest_id}, awarded {xp_reward} XP")
        return True

    def add_conversation(self, user_id: int, user_message: str, ai_response: str,
                        emotional_tone: str = None, session_id: str = None,
                        context_data: Dict = None) -> int:
        """Add conversation with enhanced context tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        context_json = json.dumps(context_data or {})
        
        cursor.execute('''
        INSERT INTO conversations (user_id, user_message, ai_response, context_data, emotional_tone, session_id)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, user_message, ai_response, context_json, emotional_tone, session_id))
        
        conversation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Extract important information for memory storage
        self._extract_memory_from_conversation(user_id, user_message, ai_response)
        
        return conversation_id

    def _extract_memory_from_conversation(self, user_id: int, user_message: str, ai_response: str):
        """Extract important information from conversations for memory storage"""
        # Simple keyword-based extraction - can be enhanced with NLP
        important_keywords = [
            'my name is', 'i am', 'i like', 'i love', 'i hate', 'i want', 'my goal',
            'remember', 'important', 'birthday', 'anniversary', 'favorite'
        ]
        
        message_lower = user_message.lower()
        for keyword in important_keywords:
            if keyword in message_lower:
                self.add_memory(
                    user_id=user_id,
                    content=user_message,
                    category="personal_info",
                    importance=3,
                    tags=["conversation", "important"]
                )
                break

    def _create_default_quests(self, user_id: int):
        """Create default quests for new users"""
        default_quests = [
            {
                "title": "Customize Your AI Companion",
                "description": "Give your AI companion a unique name and personality",
                "quest_type": "setup",
                "xp_reward": 100,
                "tags": ["first_time", "customization"]
            },
            {
                "title": "Share Something About Yourself",
                "description": "Tell your AI companion about your interests or goals",
                "quest_type": "social",
                "xp_reward": 75,
                "tags": ["getting_started", "personal"]
            },
            {
                "title": "Explore the Quest System",
                "description": "Complete your first custom quest",
                "quest_type": "tutorial",
                "xp_reward": 50,
                "tags": ["tutorial", "quests"]
            }
        ]
        
        for quest in default_quests:
            self.create_quest(user_id, **quest)

# Initialize the enhanced database
def init_personalization_system():
    """Initialize the enhanced personalization system"""
    db = TECPersonalizationDB()
    logger.info("TEC Personalization System initialized")
    return db

if __name__ == "__main__":
    # Test the system
    db = init_personalization_system()
    
    # Create a test user
    user_id = db.create_user_profile("TestUser", "My Custom AI")
    
    # Add some memories
    db.add_memory(user_id, "I love coding in Python", "interests", 3, ["coding", "python"])
    db.add_memory(user_id, "My birthday is in December", "personal", 5, ["birthday", "personal"])
    
    # Create a custom quest
    quest_id = db.create_quest(user_id, "Learn TensorFlow", "Complete a TensorFlow tutorial", "learning", 150)
    
    print("Personalization system test completed successfully!")
