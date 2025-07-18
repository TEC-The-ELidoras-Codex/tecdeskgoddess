"""
TEC Enhanced Character Memory System
Handles rich character lore, memories, and personality development
"""

import json
import sqlite3
import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

@dataclass
class CharacterMemory:
    """Enhanced character memory structure"""
    id: Optional[int]
    character_name: str
    title: str
    era: str
    memory_type: str  # Core Identity, Traumatic, Transformative, etc.
    content: str
    importance: int  # 1-10 scale
    emotional_weight: float  # -1.0 to 1.0 (negative to positive)
    tags: List[str]
    connected_memories: List[int]  # IDs of related memories
    access_count: int
    last_accessed: Optional[str]
    created_at: str
    summary: Optional[str] = None

@dataclass
class CharacterPersonality:
    """Character personality and traits"""
    character_name: str
    core_traits: List[str]
    speech_patterns: str
    motivations: str
    fears: List[str]
    strengths: List[str]
    relationships: Dict[str, str]
    evolution_notes: str
    current_mood: str
    last_updated: str

class TECCharacterMemorySystem:
    """Enhanced memory system for complex character personalities"""
    
    def __init__(self, db_path: str = "src/tec_tools/character_memories.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        
        # Memory importance thresholds
        self.importance_levels = {
            "core_identity": 10,
            "traumatic": 9,
            "transformative": 8,
            "pivotal": 7,
            "spiritual": 6,
            "foundational": 6,
            "sacrificial": 8,
            "empathetic": 5,
            "analytical": 4,
            "observational": 3
        }
        
        self.init_database()
        
    def init_database(self):
        """Initialize character memory database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Character memories table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS character_memories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        character_name TEXT NOT NULL,
                        title TEXT NOT NULL,
                        era TEXT NOT NULL,
                        memory_type TEXT NOT NULL,
                        content TEXT NOT NULL,
                        importance INTEGER NOT NULL,
                        emotional_weight REAL DEFAULT 0.0,
                        tags TEXT,  -- JSON array
                        connected_memories TEXT,  -- JSON array of IDs
                        access_count INTEGER DEFAULT 0,
                        last_accessed TEXT,
                        summary TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Character personalities table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS character_personalities (
                        character_name TEXT PRIMARY KEY,
                        core_traits TEXT NOT NULL,  -- JSON array
                        speech_patterns TEXT NOT NULL,
                        motivations TEXT NOT NULL,
                        fears TEXT,  -- JSON array
                        strengths TEXT,  -- JSON array
                        relationships TEXT,  -- JSON object
                        evolution_notes TEXT,
                        current_mood TEXT,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Memory access log
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS memory_access_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        memory_id INTEGER NOT NULL,
                        character_name TEXT NOT NULL,
                        access_context TEXT,
                        relevance_score REAL,
                        triggered_by TEXT,
                        accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (memory_id) REFERENCES character_memories (id)
                    )
                """)
                
                # Character interaction history
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS character_interactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        character_name TEXT NOT NULL,
                        interaction_type TEXT NOT NULL,
                        context TEXT,
                        memories_recalled TEXT,  -- JSON array of memory IDs
                        emotional_state TEXT,
                        response_quality INTEGER,  -- 1-10 rating
                        user_feedback TEXT,
                        interaction_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                logger.info("Character memory database initialized")
                
        except Exception as e:
            logger.error(f"Failed to initialize character memory database: {e}")
    
    def import_character_memories(self, character_data: Dict[str, Any]) -> bool:
        """Import character memories from JSON structure"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                for character in character_data.get("characters", []):
                    character_name = character["name"]
                    
                    for memory_data in character.get("memories", []):
                        # Calculate importance based on memory type
                        importance = self.importance_levels.get(
                            memory_data["memory_type"].lower().replace(" ", "_"), 5
                        )
                        
                        # Analyze emotional weight from content
                        emotional_weight = self.analyze_emotional_weight(memory_data["content"])
                        
                        # Extract tags from content and memory type
                        tags = self.extract_tags(memory_data)
                        
                        # Create summary for long memories
                        summary = self.create_summary(memory_data["content"]) if len(memory_data["content"]) > 500 else None
                        
                        conn.execute("""
                            INSERT OR REPLACE INTO character_memories
                            (character_name, title, era, memory_type, content, importance, 
                             emotional_weight, tags, connected_memories, summary)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            character_name,
                            memory_data["title"],
                            memory_data["era"],
                            memory_data["memory_type"],
                            memory_data["content"],
                            importance,
                            emotional_weight,
                            json.dumps(tags),
                            json.dumps([]),  # Will be populated later
                            summary
                        ))
                
                conn.commit()
                logger.info(f"Imported memories for {len(character_data.get('characters', []))} characters")
                return True
                
        except Exception as e:
            logger.error(f"Failed to import character memories: {e}")
            return False
    
    def analyze_emotional_weight(self, content: str) -> float:
        """Analyze emotional weight of memory content"""
        # Simple keyword-based emotion analysis
        positive_words = ["love", "joy", "success", "triumph", "peace", "beauty", "hope", "salvation"]
        negative_words = ["pain", "trauma", "abuse", "death", "loss", "betrayal", "fear", "suffering", "broken", "despair"]
        
        content_lower = content.lower()
        positive_score = sum(1 for word in positive_words if word in content_lower)
        negative_score = sum(1 for word in negative_words if word in content_lower)
        
        total_score = positive_score + negative_score
        if total_score == 0:
            return 0.0
        
        # Normalize to -1.0 to 1.0 range
        weight = (positive_score - negative_score) / max(total_score, 1)
        return max(-1.0, min(1.0, weight))
    
    def extract_tags(self, memory_data: Dict[str, Any]) -> List[str]:
        """Extract relevant tags from memory data"""
        tags = [memory_data["era"], memory_data["memory_type"]]
        
        # Extract key concepts from content
        content = memory_data["content"].lower()
        key_concepts = [
            "music", "trauma", "family", "magic", "technology", "sacrifice", 
            "power", "divine", "relationship", "identity", "transformation",
            "spiritual", "pain", "love", "death", "rebirth", "memory"
        ]
        
        for concept in key_concepts:
            if concept in content:
                tags.append(concept)
        
        return list(set(tags))
    
    def create_summary(self, content: str, max_length: int = 150) -> str:
        """Create a concise summary of memory content"""
        if len(content) <= max_length:
            return content
        
        # Extract key sentences (first, last, and any with strong emotional words)
        sentences = content.split('. ')
        key_sentences = []
        
        if sentences:
            key_sentences.append(sentences[0])  # First sentence
            
            # Look for emotionally significant sentences
            emotional_keywords = ["pain", "love", "death", "power", "transformation", "sacrifice"]
            for sentence in sentences[1:-1]:
                if any(keyword in sentence.lower() for keyword in emotional_keywords):
                    key_sentences.append(sentence)
                    break
            
            if len(sentences) > 1:
                key_sentences.append(sentences[-1])  # Last sentence
        
        summary = '. '.join(key_sentences)
        if len(summary) > max_length:
            summary = summary[:max_length] + "..."
        
        return summary
    
    def get_character_memories(self, character_name: str, 
                             memory_types: Optional[List[str]] = None,
                             limit: int = 10) -> List[CharacterMemory]:
        """Get character memories filtered by type and importance"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                query = """
                    SELECT id, character_name, title, era, memory_type, content, 
                           importance, emotional_weight, tags, connected_memories,
                           access_count, last_accessed, summary, created_at
                    FROM character_memories 
                    WHERE character_name = ?
                """
                params = [character_name]
                
                if memory_types:
                    placeholders = ','.join(['?' for _ in memory_types])
                    query += f" AND memory_type IN ({placeholders})"
                    params.extend(memory_types)
                
                query += " ORDER BY importance DESC, access_count ASC LIMIT ?"
                params.append(limit)
                
                cursor = conn.execute(query, params)
                memories = []
                
                for row in cursor.fetchall():
                    memory = CharacterMemory(
                        id=row[0],
                        character_name=row[1],
                        title=row[2],
                        era=row[3],
                        memory_type=row[4],
                        content=row[5],
                        importance=row[6],
                        emotional_weight=row[7],
                        tags=json.loads(row[8]) if row[8] else [],
                        connected_memories=json.loads(row[9]) if row[9] else [],
                        access_count=row[10],
                        last_accessed=row[11],
                        summary=row[12],
                        created_at=row[13]
                    )
                    memories.append(memory)
                
                return memories
                
        except Exception as e:
            logger.error(f"Failed to get character memories: {e}")
            return []
    
    def search_memories(self, character_name: str, query: str, 
                       context_type: Optional[str] = None) -> List[CharacterMemory]:
        """Search character memories by content relevance"""
        try:
            query_terms = query.lower().split()
            memories = self.get_character_memories(character_name, limit=50)
            
            scored_memories = []
            for memory in memories:
                score = self.calculate_relevance_score(memory, query_terms, context_type)
                if score > 0:
                    scored_memories.append((memory, score))
            
            # Sort by relevance score and return top matches
            scored_memories.sort(key=lambda x: x[1], reverse=True)
            return [memory for memory, score in scored_memories[:10]]
            
        except Exception as e:
            logger.error(f"Failed to search memories: {e}")
            return []
    
    def calculate_relevance_score(self, memory: CharacterMemory, query_terms: List[str], 
                                context_type: Optional[str] = None) -> float:
        """Calculate relevance score for a memory"""
        score = 0.0
        content_lower = memory.content.lower()
        title_lower = memory.title.lower()
        
        # Term matching in content and title
        for term in query_terms:
            if term in title_lower:
                score += 3.0  # Title matches are important
            if term in content_lower:
                score += 1.0
            if term in memory.tags:
                score += 2.0
        
        # Memory type relevance
        if context_type:
            if context_type.lower() in memory.memory_type.lower():
                score += 2.0
        
        # Importance boost
        score += memory.importance * 0.1
        
        # Emotional weight consideration
        score += abs(memory.emotional_weight) * 0.5
        
        return score
    
    def log_memory_access(self, memory_id: int, character_name: str, 
                         access_context: str, relevance_score: float = 0.0,
                         triggered_by: str = "user_query"):
        """Log memory access for analytics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Log the access
                conn.execute("""
                    INSERT INTO memory_access_log
                    (memory_id, character_name, access_context, relevance_score, triggered_by)
                    VALUES (?, ?, ?, ?, ?)
                """, (memory_id, character_name, access_context, relevance_score, triggered_by))
                
                # Update access count for the memory
                conn.execute("""
                    UPDATE character_memories 
                    SET access_count = access_count + 1, 
                        last_accessed = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (memory_id,))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Failed to log memory access: {e}")
    
    def get_character_context(self, character_name: str, query: str, 
                            max_memories: int = 5) -> Dict[str, Any]:
        """Get relevant character context for a query"""
        try:
            # Search for relevant memories
            relevant_memories = self.search_memories(character_name, query)[:max_memories]
            
            # Get character personality if available
            personality = self.get_character_personality(character_name)
            
            # Log memory accesses
            for memory in relevant_memories:
                if memory.id:
                    self.log_memory_access(
                        memory.id, character_name, query, 
                        triggered_by="context_generation"
                    )
            
            return {
                "character_name": character_name,
                "relevant_memories": [
                    {
                        "title": memory.title,
                        "era": memory.era,
                        "memory_type": memory.memory_type,
                        "content": memory.summary or memory.content,
                        "importance": memory.importance,
                        "emotional_weight": memory.emotional_weight,
                        "tags": memory.tags
                    }
                    for memory in relevant_memories
                ],
                "personality": personality,
                "context_summary": self.generate_context_summary(relevant_memories),
                "total_memories": len(relevant_memories)
            }
            
        except Exception as e:
            logger.error(f"Failed to get character context: {e}")
            return {"character_name": character_name, "relevant_memories": [], "total_memories": 0}
    
    def generate_context_summary(self, memories: List[CharacterMemory]) -> str:
        """Generate a brief context summary from memories"""
        if not memories:
            return "No relevant memories found."
        
        eras = list(set(memory.era for memory in memories))
        memory_types = list(set(memory.memory_type for memory in memories))
        
        summary = f"Drawing from {len(memories)} memories spanning {', '.join(eras)}. "
        summary += f"Key themes: {', '.join(memory_types)}. "
        
        # Add emotional context
        avg_emotional_weight = sum(memory.emotional_weight for memory in memories) / len(memories)
        if avg_emotional_weight > 0.3:
            summary += "Generally positive emotional context."
        elif avg_emotional_weight < -0.3:
            summary += "Generally difficult/traumatic emotional context."
        else:
            summary += "Mixed emotional context."
        
        return summary
    
    def get_character_personality(self, character_name: str) -> Optional[Dict[str, Any]]:
        """Get character personality data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT core_traits, speech_patterns, motivations, fears, 
                           strengths, relationships, evolution_notes, current_mood
                    FROM character_personalities 
                    WHERE character_name = ?
                """, (character_name,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        "core_traits": json.loads(row[0]) if row[0] else [],
                        "speech_patterns": row[1],
                        "motivations": row[2],
                        "fears": json.loads(row[3]) if row[3] else [],
                        "strengths": json.loads(row[4]) if row[4] else [],
                        "relationships": json.loads(row[5]) if row[5] else {},
                        "evolution_notes": row[6],
                        "current_mood": row[7]
                    }
                
        except Exception as e:
            logger.error(f"Failed to get character personality: {e}")
        
        return None
    
    def get_memory_statistics(self, character_name: str) -> Dict[str, Any]:
        """Get memory usage statistics for a character"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Basic memory counts
                cursor = conn.execute("""
                    SELECT 
                        COUNT(*) as total_memories,
                        AVG(importance) as avg_importance,
                        AVG(emotional_weight) as avg_emotional_weight,
                        SUM(access_count) as total_accesses
                    FROM character_memories 
                    WHERE character_name = ?
                """, (character_name,))
                
                stats = cursor.fetchone()
                
                # Memory type breakdown
                cursor = conn.execute("""
                    SELECT memory_type, COUNT(*) 
                    FROM character_memories 
                    WHERE character_name = ?
                    GROUP BY memory_type
                """, (character_name,))
                
                memory_types = dict(cursor.fetchall())
                
                # Era breakdown
                cursor = conn.execute("""
                    SELECT era, COUNT(*) 
                    FROM character_memories 
                    WHERE character_name = ?
                    GROUP BY era
                """, (character_name,))
                
                eras = dict(cursor.fetchall())
                
                return {
                    "character_name": character_name,
                    "total_memories": stats[0] or 0,
                    "avg_importance": stats[1] or 0.0,
                    "avg_emotional_weight": stats[2] or 0.0,
                    "total_accesses": stats[3] or 0,
                    "memory_types": memory_types,
                    "eras": eras
                }
                
        except Exception as e:
            logger.error(f"Failed to get memory statistics: {e}")
            return {"character_name": character_name, "total_memories": 0}
