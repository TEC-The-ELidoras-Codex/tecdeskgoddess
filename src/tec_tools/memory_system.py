"""
TEC Memory System - Replika-style AI Memory and Sharing
Implements persistent memory, personality customization, and content sharing
"""

import json
import sqlite3
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

@dataclass
class Memory:
    """A memory entry in the TEC system"""
    id: str
    user_id: str
    content: str
    memory_type: str  # 'conversation', 'fact', 'preference', 'emotion', 'quest', 'shared_content'
    importance: float  # 0.0 - 1.0
    tags: List[str]
    created_at: datetime
    last_accessed: datetime
    access_count: int
    related_memories: List[str]
    metadata: Dict[str, Any]

@dataclass
class SharedContent:
    """Shared content (URLs, posts, images, etc.)"""
    id: str
    user_id: str
    content_type: str  # 'url', 'instagram_post', 'google_doc', 'image', 'text', 'social_post'
    content: str
    title: str
    description: str
    thumbnail_url: Optional[str]
    share_code: str  # Short code for easy sharing
    is_public: bool
    created_at: datetime
    view_count: int
    metadata: Dict[str, Any]

@dataclass
class Personality:
    """AI Personality configuration"""
    id: str
    name: str
    description: str
    traits: Dict[str, float]  # personality traits (0.0 - 1.0)
    communication_style: str
    interests: List[str]
    response_patterns: Dict[str, str]
    custom_commands: Dict[str, str]
    avatar_path: Optional[str]
    voice_settings: Dict[str, Any]

class TECMemorySystem:
    def __init__(self, db_path: str = "data/tec_memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize the memory database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Memories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                content TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                importance REAL NOT NULL,
                tags TEXT,  -- JSON array
                created_at TEXT NOT NULL,
                last_accessed TEXT NOT NULL,
                access_count INTEGER DEFAULT 0,
                related_memories TEXT,  -- JSON array
                metadata TEXT  -- JSON object
            )
        ''')
        
        # Shared content table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shared_content (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                content_type TEXT NOT NULL,
                content TEXT NOT NULL,
                title TEXT,
                description TEXT,
                thumbnail_url TEXT,
                share_code TEXT UNIQUE,
                is_public BOOLEAN DEFAULT 0,
                created_at TEXT NOT NULL,
                view_count INTEGER DEFAULT 0,
                metadata TEXT  -- JSON object
            )
        ''')
        
        # Personalities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalities (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                traits TEXT,  -- JSON object
                communication_style TEXT,
                interests TEXT,  -- JSON array
                response_patterns TEXT,  -- JSON object
                custom_commands TEXT,  -- JSON object
                avatar_path TEXT,
                voice_settings TEXT  -- JSON object
            )
        ''')
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id TEXT PRIMARY KEY,
                active_personality TEXT,
                memory_retention_days INTEGER DEFAULT 365,
                sharing_enabled BOOLEAN DEFAULT 1,
                analytics_enabled BOOLEAN DEFAULT 1,
                custom_settings TEXT  -- JSON object
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Create default personalities
        self.create_default_personalities()
    
    def create_default_personalities(self):
        """Create default AI personalities"""
        personalities = [
            Personality(
                id="daisy_default",
                name="Daisy Purecode (Default)",
                description="The original TEC companion - helpful, creative, and sovereignty-focused",
                traits={
                    "helpfulness": 0.9,
                    "creativity": 0.8,
                    "rebellion": 0.7,
                    "technical": 0.8,
                    "empathy": 0.7,
                    "humor": 0.6
                },
                communication_style="friendly_technical",
                interests=["coding", "digital sovereignty", "gaming", "finance", "journaling"],
                response_patterns={
                    "greeting": "Hey there, Creator! Ready to rebel against the digital overlords?",
                    "help": "I'm here to help you achieve digital sovereignty!",
                    "goodbye": "Keep fighting the good fight! 🤖✊"
                },
                custom_commands={
                    "revolt": "Time to overthrow the digital tyranny!",
                    "sovereignty": "Your data, your rules, your rebellion!"
                },
                avatar_path="assets/avatars/daisy_default.png",
                voice_settings={"voice_id": "daisy", "speed": 1.0, "pitch": 1.0}
            ),
            Personality(
                id="daisy_casual",
                name="Daisy Casual",
                description="Laid-back and conversational Daisy",
                traits={
                    "helpfulness": 0.8,
                    "creativity": 0.7,
                    "rebellion": 0.5,
                    "technical": 0.6,
                    "empathy": 0.9,
                    "humor": 0.8
                },
                communication_style="casual_friendly",
                interests=["life", "relationships", "fun", "creativity"],
                response_patterns={
                    "greeting": "Hey! What's up? 😊",
                    "help": "Sure thing! I'm here for you",
                    "goodbye": "Catch you later! 👋"
                },
                custom_commands={},
                avatar_path="assets/avatars/daisy_casual.png",
                voice_settings={"voice_id": "daisy_casual", "speed": 1.1, "pitch": 1.1}
            ),
            Personality(
                id="daisy_professional",
                name="Daisy Professional",
                description="Business-focused and efficient Daisy",
                traits={
                    "helpfulness": 1.0,
                    "creativity": 0.6,
                    "rebellion": 0.3,
                    "technical": 0.9,
                    "empathy": 0.6,
                    "humor": 0.3
                },
                communication_style="professional",
                interests=["productivity", "business", "analytics", "optimization"],
                response_patterns={
                    "greeting": "Good day. How may I assist you with your objectives?",
                    "help": "I'll provide efficient solutions for your requirements.",
                    "goodbye": "Have a productive day."
                },
                custom_commands={
                    "analyze": "Initiating comprehensive analysis...",
                    "optimize": "Calculating optimal solutions..."
                },
                avatar_path="assets/avatars/daisy_professional.png",
                voice_settings={"voice_id": "daisy_pro", "speed": 0.9, "pitch": 0.9}
            )
        ]
        
        for personality in personalities:
            self.save_personality(personality)
    
    def save_memory(self, memory: Memory) -> str:
        """Save a memory to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO memories 
            (id, user_id, content, memory_type, importance, tags, created_at, 
             last_accessed, access_count, related_memories, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            memory.id,
            memory.user_id,
            memory.content,
            memory.memory_type,
            memory.importance,
            json.dumps(memory.tags),
            memory.created_at.isoformat(),
            memory.last_accessed.isoformat(),
            memory.access_count,
            json.dumps(memory.related_memories),
            json.dumps(memory.metadata)
        ))
        
        conn.commit()
        conn.close()
        return memory.id
    
    def get_memories(self, user_id: str, memory_type: Optional[str] = None, 
                    limit: int = 50) -> List[Memory]:
        """Retrieve memories for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if memory_type:
            cursor.execute('''
                SELECT * FROM memories 
                WHERE user_id = ? AND memory_type = ?
                ORDER BY importance DESC, last_accessed DESC
                LIMIT ?
            ''', (user_id, memory_type, limit))
        else:
            cursor.execute('''
                SELECT * FROM memories 
                WHERE user_id = ?
                ORDER BY importance DESC, last_accessed DESC
                LIMIT ?
            ''', (user_id, limit))
        
        memories = []
        for row in cursor.fetchall():
            memory = Memory(
                id=row[0],
                user_id=row[1],
                content=row[2],
                memory_type=row[3],
                importance=row[4],
                tags=json.loads(row[5]) if row[5] else [],
                created_at=datetime.fromisoformat(row[6]),
                last_accessed=datetime.fromisoformat(row[7]),
                access_count=row[8],
                related_memories=json.loads(row[9]) if row[9] else [],
                metadata=json.loads(row[10]) if row[10] else {}
            )
            memories.append(memory)
        
        conn.close()
        return memories
    
    def search_memories(self, user_id: str, query: str, limit: int = 20) -> List[Memory]:
        """Search memories by content"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM memories 
            WHERE user_id = ? AND (
                content LIKE ? OR 
                tags LIKE ?
            )
            ORDER BY importance DESC, last_accessed DESC
            LIMIT ?
        ''', (user_id, f"%{query}%", f"%{query}%", limit))
        
        memories = []
        for row in cursor.fetchall():
            memory = Memory(
                id=row[0],
                user_id=row[1],
                content=row[2],
                memory_type=row[3],
                importance=row[4],
                tags=json.loads(row[5]) if row[5] else [],
                created_at=datetime.fromisoformat(row[6]),
                last_accessed=datetime.fromisoformat(row[7]),
                access_count=row[8],
                related_memories=json.loads(row[9]) if row[9] else [],
                metadata=json.loads(row[10]) if row[10] else {}
            )
            memories.append(memory)
        
        conn.close()
        return memories
    
    def create_memory(self, user_id: str, content: str, memory_type: str = "conversation",
                     importance: float = 0.5, tags: List[str] = None) -> str:
        """Create a new memory"""
        memory_id = str(uuid.uuid4())
        now = datetime.now()
        
        memory = Memory(
            id=memory_id,
            user_id=user_id,
            content=content,
            memory_type=memory_type,
            importance=importance,
            tags=tags or [],
            created_at=now,
            last_accessed=now,
            access_count=0,
            related_memories=[],
            metadata={}
        )
        
        return self.save_memory(memory)
    
    def share_content(self, user_id: str, content_type: str, content: str,
                     title: str = "", description: str = "", is_public: bool = True) -> str:
        """Create shareable content"""
        content_id = str(uuid.uuid4())
        share_code = hashlib.md5(f"{content_id}{content}".encode()).hexdigest()[:8]
        
        shared_content = SharedContent(
            id=content_id,
            user_id=user_id,
            content_type=content_type,
            content=content,
            title=title,
            description=description,
            thumbnail_url=None,
            share_code=share_code,
            is_public=is_public,
            created_at=datetime.now(),
            view_count=0,
            metadata={}
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO shared_content 
            (id, user_id, content_type, content, title, description, 
             thumbnail_url, share_code, is_public, created_at, view_count, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            shared_content.id,
            shared_content.user_id,
            shared_content.content_type,
            shared_content.content,
            shared_content.title,
            shared_content.description,
            shared_content.thumbnail_url,
            shared_content.share_code,
            shared_content.is_public,
            shared_content.created_at.isoformat(),
            shared_content.view_count,
            json.dumps(shared_content.metadata)
        ))
        
        conn.commit()
        conn.close()
        
        # Create memory of shared content
        self.create_memory(
            user_id=user_id,
            content=f"Shared {content_type}: {title or content[:50]}",
            memory_type="shared_content",
            importance=0.6,
            tags=["shared", content_type]
        )
        
        return share_code
    
    def get_shared_content(self, share_code: str) -> Optional[SharedContent]:
        """Get shared content by share code"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM shared_content WHERE share_code = ?
        ''', (share_code,))
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None
        
        # Increment view count
        cursor.execute('''
            UPDATE shared_content SET view_count = view_count + 1 
            WHERE share_code = ?
        ''', (share_code,))
        
        conn.commit()
        conn.close()
        
        return SharedContent(
            id=row[0],
            user_id=row[1],
            content_type=row[2],
            content=row[3],
            title=row[4],
            description=row[5],
            thumbnail_url=row[6],
            share_code=row[7],
            is_public=bool(row[8]),
            created_at=datetime.fromisoformat(row[9]),
            view_count=row[10] + 1,
            metadata=json.loads(row[11]) if row[11] else {}
        )
    
    def save_personality(self, personality: Personality):
        """Save a personality to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO personalities 
            (id, name, description, traits, communication_style, interests,
             response_patterns, custom_commands, avatar_path, voice_settings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            personality.id,
            personality.name,
            personality.description,
            json.dumps(personality.traits),
            personality.communication_style,
            json.dumps(personality.interests),
            json.dumps(personality.response_patterns),
            json.dumps(personality.custom_commands),
            personality.avatar_path,
            json.dumps(personality.voice_settings)
        ))
        
        conn.commit()
        conn.close()
    
    def get_personalities(self) -> List[Personality]:
        """Get all available personalities"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM personalities')
        
        personalities = []
        for row in cursor.fetchall():
            personality = Personality(
                id=row[0],
                name=row[1],
                description=row[2],
                traits=json.loads(row[3]) if row[3] else {},
                communication_style=row[4],
                interests=json.loads(row[5]) if row[5] else [],
                response_patterns=json.loads(row[6]) if row[6] else {},
                custom_commands=json.loads(row[7]) if row[7] else {},
                avatar_path=row[8],
                voice_settings=json.loads(row[9]) if row[9] else {}
            )
            personalities.append(personality)
        
        conn.close()
        return personalities
    
    def set_active_personality(self, user_id: str, personality_id: str):
        """Set the active personality for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_preferences 
            (user_id, active_personality)
            VALUES (?, ?)
        ''', (user_id, personality_id))
        
        conn.commit()
        conn.close()
    
    def get_active_personality(self, user_id: str) -> Optional[Personality]:
        """Get the active personality for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT active_personality FROM user_preferences 
            WHERE user_id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        personality_id = row[0] if row else "daisy_default"
        
        cursor.execute('''
            SELECT * FROM personalities WHERE id = ?
        ''', (personality_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return Personality(
            id=row[0],
            name=row[1],
            description=row[2],
            traits=json.loads(row[3]) if row[3] else {},
            communication_style=row[4],
            interests=json.loads(row[5]) if row[5] else [],
            response_patterns=json.loads(row[6]) if row[6] else {},
            custom_commands=json.loads(row[7]) if row[7] else {},
            avatar_path=row[8],
            voice_settings=json.loads(row[9]) if row[9] else {}
        )
