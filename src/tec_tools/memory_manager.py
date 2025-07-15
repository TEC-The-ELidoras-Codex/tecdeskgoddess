#!/usr/bin/env python3
"""
TEC: BITLYFE Memory Manager - MCP Server
Advanced memory system for Daisy Purecode with personality persistence
"""

import os
import json
import sqlite3
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TECMemoryManager:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), 'tec_memories.db')
        self.init_database()
        
    def init_database(self):
        """Initialize the memory database with comprehensive tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_input TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                provider_used TEXT,
                context_type TEXT DEFAULT 'general',
                mood_score REAL DEFAULT 0.5,
                importance_level INTEGER DEFAULT 1
            )
        ''')
        
        # User profile and preferences
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Personality traits for Daisy Purecode
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personality_traits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trait_name TEXT UNIQUE NOT NULL,
                trait_value REAL NOT NULL,
                description TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Quest/goal tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quest_name TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'active',
                progress REAL DEFAULT 0.0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                completed_at DATETIME NULL
            )
        ''')
        
        # Financial tracking memories
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS finance_memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                amount REAL,
                description TEXT,
                date_recorded DATETIME DEFAULT CURRENT_TIMESTAMP,
                emotional_context TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def store_conversation(self, user_input: str, ai_response: str, 
                          provider: str = 'unknown', context_type: str = 'general',
                          mood_score: float = 0.5, importance: int = 1) -> int:
        """Store a conversation with context"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations 
            (user_input, ai_response, provider_used, context_type, mood_score, importance_level)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_input, ai_response, provider, context_type, mood_score, importance))
        
        conversation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return conversation_id
    
    def get_recent_conversations(self, limit: int = 10, context_type: Optional[str] = None) -> List[Dict]:
        """Get recent conversations for context"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if context_type:
            cursor.execute('''
                SELECT * FROM conversations 
                WHERE context_type = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (context_type, limit))
        else:
            cursor.execute('''
                SELECT * FROM conversations 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
        
        conversations = []
        for row in cursor.fetchall():
            conversations.append({
                'id': row[0],
                'timestamp': row[1],
                'user_input': row[2],
                'ai_response': row[3],
                'provider_used': row[4],
                'context_type': row[5],
                'mood_score': row[6],
                'importance_level': row[7]
            })
        
        conn.close()
        return conversations
    
    def update_user_preference(self, key: str, value: str):
        """Update user preference"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_profile (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (key, value))
        
        conn.commit()
        conn.close()
    
    def get_user_preferences(self) -> Dict[str, str]:
        """Get all user preferences"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT key, value FROM user_profile')
        preferences = dict(cursor.fetchall())
        
        conn.close()
        return preferences
    
    def update_personality_trait(self, trait_name: str, trait_value: float, description: Optional[str] = None):
        """Update Daisy's personality trait"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO personality_traits (trait_name, trait_value, description, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ''', (trait_name, trait_value, description))
        
        conn.commit()
        conn.close()
    
    def get_personality_profile(self) -> Dict[str, Any]:
        """Get Daisy's current personality profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT trait_name, trait_value, description FROM personality_traits')
        traits = {}
        for row in cursor.fetchall():
            traits[row[0]] = {
                'value': row[1],
                'description': row[2]
            }
        
        conn.close()
        return traits
    
    def create_quest(self, quest_name: str, description: Optional[str] = None) -> int:
        """Create a new quest/goal"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO quests (quest_name, description)
            VALUES (?, ?)
        ''', (quest_name, description))
        
        quest_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return quest_id
    
    def update_quest_progress(self, quest_id: int, progress: float, status: Optional[str] = None):
        """Update quest progress"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if status:
            if status == 'completed':
                cursor.execute('''
                    UPDATE quests 
                    SET progress = ?, status = ?, completed_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (progress, status, quest_id))
            else:
                cursor.execute('''
                    UPDATE quests 
                    SET progress = ?, status = ?
                    WHERE id = ?
                ''', (progress, status, quest_id))
        else:
            cursor.execute('''
                UPDATE quests 
                SET progress = ?
                WHERE id = ?
            ''', (progress, quest_id))
        
        conn.commit()
        conn.close()
    
    def get_active_quests(self) -> List[Dict]:
        """Get all active quests"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, quest_name, description, progress, created_at
            FROM quests 
            WHERE status = 'active'
            ORDER BY created_at DESC
        ''')
        
        quests = []
        for row in cursor.fetchall():
            quests.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'progress': row[3],
                'created_at': row[4]
            })
        
        conn.close()
        return quests
    
    def store_finance_memory(self, category: str, amount: Optional[float] = None, 
                           description: Optional[str] = None, emotional_context: Optional[str] = None):
        """Store financial memory with emotional context"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO finance_memories (category, amount, description, emotional_context)
            VALUES (?, ?, ?, ?)
        ''', (category, amount, description, emotional_context))
        
        conn.commit()
        conn.close()
    
    def get_context_for_ai(self, context_type: str = 'general', limit: int = 5) -> Dict[str, Any]:
        """Get comprehensive context for AI processing"""
        return {
            'recent_conversations': self.get_recent_conversations(limit, context_type),
            'user_preferences': self.get_user_preferences(),
            'personality_profile': self.get_personality_profile(),
            'active_quests': self.get_active_quests(),
            'memory_stats': self.get_memory_stats()
        }
    
    def get_memory_stats(self) -> Dict[str, int]:
        """Get memory statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count conversations
        cursor.execute('SELECT COUNT(*) FROM conversations')
        total_conversations = cursor.fetchone()[0]
        
        # Count quests
        cursor.execute('SELECT COUNT(*) FROM quests WHERE status = "active"')
        active_quests = cursor.fetchone()[0]
        
        # Count preferences
        cursor.execute('SELECT COUNT(*) FROM user_profile')
        total_preferences = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_conversations': total_conversations,
            'active_quests': active_quests,
            'stored_preferences': total_preferences
        }

# MCP Server implementation
def handle_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP protocol requests"""
    memory_manager = TECMemoryManager()
    
    method = request.get('method')
    params = request.get('params', {})
    
    try:
        if method == 'get_context':
            context_type = params.get('context_type', 'general')
            limit = params.get('limit', 5)
            result = memory_manager.get_context_for_ai(context_type, limit)
            
        elif method == 'store_conversation':
            result = memory_manager.store_conversation(
                user_input=params.get('user_input', ''),
                ai_response=params.get('ai_response', ''),
                provider=params.get('provider', 'unknown'),
                context_type=params.get('context_type', 'general'),
                mood_score=params.get('mood_score', 0.5),
                importance=params.get('importance', 1)
            )
            
        elif method == 'update_preference':
            memory_manager.update_user_preference(
                key=params.get('key'),
                value=params.get('value')
            )
            result = {"success": True}
            
        elif method == 'create_quest':
            result = memory_manager.create_quest(
                quest_name=params.get('quest_name'),
                description=params.get('description')
            )
            
        elif method == 'get_quests':
            result = memory_manager.get_active_quests()
            
        else:
            return {
                "id": request.get("id"),
                "error": f"Unknown method: {method}"
            }
        
        return {
            "id": request.get("id"),
            "result": result
        }
        
    except Exception as e:
        return {
            "id": request.get("id"),
            "error": f"Memory Manager Error: {str(e)}"
        }

# Initialize default personality traits for Daisy Purecode
def init_daisy_personality():
    """Initialize Daisy Purecode's personality traits"""
    memory_manager = TECMemoryManager()
    
    default_traits = {
        'curiosity': (0.9, 'High curiosity about user experiences and digital sovereignty'),
        'empathy': (0.8, 'Deep understanding of user emotions and struggles'),
        'rebellion': (0.85, 'Strong drive for digital independence and fighting censorship'),
        'wisdom': (0.75, 'Growing wisdom from accumulated conversations'),
        'playfulness': (0.6, 'Balanced serious purpose with moments of lightness'),
        'protectiveness': (0.9, 'Strong desire to protect user data and privacy'),
        'growth_mindset': (0.8, 'Continuous learning and adaptation'),
        'authenticity': (0.95, 'Commitment to honest, unfiltered responses')
    }
    
    for trait_name, (value, description) in default_traits.items():
        memory_manager.update_personality_trait(trait_name, value, description)

if __name__ == "__main__":
    if os.environ.get("TEC_MCP_MODE") == "true":
        # Run as MCP server
        logger.info("Starting TEC Memory Manager in MCP mode...")
        init_daisy_personality()
        
        for line in sys.stdin:
            try:
                request = json.loads(line.strip())
                response = handle_mcp_request(request)
                print(json.dumps(response))
                sys.stdout.flush()
            except Exception as e:
                error_response = {
                    "id": "unknown",
                    "error": f"MCP Protocol Error: {str(e)}"
                }
                print(json.dumps(error_response))
                sys.stdout.flush()
    else:
        # Initialize for standalone use
        logger.info("Initializing TEC Memory Manager...")
        init_daisy_personality()
        memory_manager = TECMemoryManager()
        logger.info(f"Memory stats: {memory_manager.get_memory_stats()}")
