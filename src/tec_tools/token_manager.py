"""
TEC Token Usage Manager
Tracks API usage, costs, and optimization for character memory systems
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
class TokenUsage:
    """Token usage data structure"""
    session_id: str
    timestamp: str
    character: str
    request_type: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost: float
    model: str = "gemini-pro"
    memory_context_size: int = 0
    avatar_processing: bool = False

@dataclass
class UsageStats:
    """Usage statistics summary"""
    total_tokens: int
    total_cost: float
    requests_count: int
    avg_tokens_per_request: float
    character_breakdown: Dict[str, int]
    daily_usage: Dict[str, int]

class TECTokenManager:
    """Manages token usage tracking and optimization for TEC system"""
    
    def __init__(self, db_path: str = "src/tec_tools/token_usage.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        
        # Token cost estimates (per 1K tokens)
        self.cost_per_1k_tokens = {
            "gemini-pro": 0.0005,  # Estimated
            "github-gpt-4": 0.03,
            "github-gpt-3.5": 0.002,
            "openai-gpt-4": 0.03,
            "openai-gpt-3.5": 0.002
        }
        
        # Memory optimization thresholds
        self.memory_limits = {
            "low_usage": 2000,      # Tokens
            "medium_usage": 5000,   # Tokens
            "high_usage": 8000,     # Tokens
            "max_context": 32000    # Model limit
        }
        
        self.init_database()
        
    def init_database(self):
        """Initialize token usage tracking database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS token_usage (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        character TEXT NOT NULL,
                        request_type TEXT NOT NULL,
                        prompt_tokens INTEGER NOT NULL,
                        completion_tokens INTEGER NOT NULL,
                        total_tokens INTEGER NOT NULL,
                        estimated_cost REAL NOT NULL,
                        model TEXT NOT NULL,
                        memory_context_size INTEGER DEFAULT 0,
                        avatar_processing BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS usage_sessions (
                        session_id TEXT PRIMARY KEY,
                        start_time TEXT NOT NULL,
                        end_time TEXT,
                        character TEXT NOT NULL,
                        total_tokens INTEGER DEFAULT 0,
                        total_cost REAL DEFAULT 0.0,
                        request_count INTEGER DEFAULT 0
                    )
                """)
                
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS optimization_rules (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        character TEXT NOT NULL,
                        memory_limit INTEGER NOT NULL,
                        summarization_threshold INTEGER NOT NULL,
                        priority_keywords TEXT,
                        active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                logger.info("Token usage database initialized")
                
        except Exception as e:
            logger.error(f"Failed to initialize token database: {e}")
    
    def estimate_tokens(self, text: str, model: str = "gemini-pro") -> int:
        """Estimate token count for text"""
        # Simple estimation: ~4 characters per token for most models
        if model.startswith("gpt-4"):
            chars_per_token = 3.5  # GPT-4 is more efficient
        elif model.startswith("gpt-3.5"):
            chars_per_token = 4.0
        elif model.startswith("gemini"):
            chars_per_token = 4.2  # Gemini tokenization
        else:
            chars_per_token = 4.0  # Default
        
        return max(1, int(len(text) / chars_per_token))
    
    def get_token_limits(self, model: str = "gemini-pro") -> Dict[str, int]:
        """Get token limits for different models"""
        limits = {
            "gemini-pro": 32768,
            "gpt-4": 8192,
            "gpt-4-32k": 32768,
            "gpt-3.5-turbo": 4096,
            "gpt-3.5-turbo-16k": 16384
        }
        return {
            "max_tokens": limits.get(model, 4096),
            "recommended_max": int(limits.get(model, 4096) * 0.8)  # Leave buffer
        }
            
    def log_usage(self, model: str, prompt_tokens: int, completion_tokens: int, 
                 character: str = "default", session_id: str = None) -> UsageStats:
        """Log token usage and return stats"""
        if session_id is None:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        total_tokens = prompt_tokens + completion_tokens
        estimated_cost = self.estimate_cost(total_tokens, model)
        
        # Create usage record
        usage = TokenUsage(
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            character=character,
            request_type="chat",
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            estimated_cost=estimated_cost,
            model=model
        )
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Insert usage record
                conn.execute("""
                    INSERT INTO token_usage 
                    (session_id, timestamp, character, request_type, prompt_tokens, 
                     completion_tokens, total_tokens, estimated_cost, model, 
                     memory_context_size, avatar_processing)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    usage.session_id, usage.timestamp, usage.character, usage.request_type,
                    usage.prompt_tokens, usage.completion_tokens, usage.total_tokens,
                    usage.estimated_cost, usage.model, usage.memory_context_size,
                    usage.avatar_processing
                ))
                
                # Update session totals
                conn.execute("""
                    INSERT OR REPLACE INTO usage_sessions 
                    (session_id, start_time, character, total_tokens, total_cost, request_count)
                    VALUES (
                        ?, 
                        COALESCE((SELECT start_time FROM usage_sessions WHERE session_id = ?), ?),
                        ?,
                        COALESCE((SELECT total_tokens FROM usage_sessions WHERE session_id = ?), 0) + ?,
                        COALESCE((SELECT total_cost FROM usage_sessions WHERE session_id = ?), 0.0) + ?,
                        COALESCE((SELECT request_count FROM usage_sessions WHERE session_id = ?), 0) + 1
                    )
                """, (
                    usage.session_id, usage.session_id, usage.timestamp, usage.character,
                    usage.session_id, usage.total_tokens,
                    usage.session_id, usage.estimated_cost,
                    usage.session_id
                ))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Failed to log token usage: {e}")
        
        # Determine optimization level
        optimization_level = "standard"
        if total_tokens > self.memory_limits["high_usage"]:
            optimization_level = "aggressive"
        elif total_tokens > self.memory_limits["medium_usage"]:
            optimization_level = "moderate"
        elif total_tokens < self.memory_limits["low_usage"]:
            optimization_level = "minimal"
        
        return UsageStats(
            total_requests=1,
            total_tokens=total_tokens,
            total_cost=estimated_cost,
            avg_tokens_per_request=total_tokens,
            cost_per_1k_tokens=self.cost_per_1k_tokens.get(model, 0.001),
            optimization_level=optimization_level,
            period_days=1
        )
    
    def optimize_memories_for_tokens(self, memories: List[Dict], max_tokens: int = 2000) -> Dict[str, Any]:
        """Optimize memory context to fit within token limits"""
        if not memories:
            return {
                "optimized_memories": [],
                "total_tokens": 0,
                "optimization_level": "none"
            }
        
        # Calculate tokens for all memories
        total_content = json.dumps(memories)
        total_tokens = self.estimate_tokens(total_content)
        
        if total_tokens <= max_tokens:
            return {
                "optimized_memories": memories,
                "total_tokens": total_tokens,
                "optimization_level": "none"
            }
        
        # Sort memories by importance
        sorted_memories = sorted(memories, key=lambda m: m.get('importance', 0), reverse=True)
        
        optimized_memories = []
        current_tokens = 0
        
        for memory in sorted_memories:
            memory_tokens = self.estimate_tokens(json.dumps(memory))
            
            if current_tokens + memory_tokens <= max_tokens:
                optimized_memories.append(memory)
                current_tokens += memory_tokens
            else:
                # Try to add a summarized version
                summary = memory.get('summary') or memory.get('content', '')[:100] + "..."
                summarized_memory = {
                    **memory,
                    'content': summary
                }
                summary_tokens = self.estimate_tokens(json.dumps(summarized_memory))
                
                if current_tokens + summary_tokens <= max_tokens:
                    optimized_memories.append(summarized_memory)
                    current_tokens += summary_tokens
        
        optimization_level = "minimal"
        if len(optimized_memories) < len(memories) * 0.7:
            optimization_level = "aggressive"
        elif len(optimized_memories) < len(memories) * 0.9:
            optimization_level = "moderate"
        
        return {
            "optimized_memories": optimized_memories,
            "total_tokens": current_tokens,
            "optimization_level": optimization_level
        }
    
    def estimate_cost(self, tokens: int, model: str = "gemini-pro") -> float:
        """Estimate cost for token usage"""
        cost_per_1k = self.cost_per_1k_tokens.get(model, 0.001)
        return (tokens / 1000) * cost_per_1k
    
    def get_usage_stats(self, days: int = 7, character: Optional[str] = None) -> UsageStats:
        """Get usage statistics for specified period"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Base query
                where_clause = "WHERE timestamp >= date('now', '-{} days')".format(days)
                if character:
                    where_clause += f" AND character = '{character}'"
                
                # Total statistics
                cursor = conn.execute(f"""
                    SELECT 
                        SUM(total_tokens) as total_tokens,
                        SUM(estimated_cost) as total_cost,
                        COUNT(*) as requests_count,
                        AVG(total_tokens) as avg_tokens
                    FROM token_usage {where_clause}
                """)
                
                row = cursor.fetchone()
                total_tokens = row[0] or 0
                total_cost = row[1] or 0.0
                requests_count = row[2] or 0
                avg_tokens = row[3] or 0.0
                
                # Character breakdown
                cursor = conn.execute(f"""
                    SELECT character, SUM(total_tokens) 
                    FROM token_usage {where_clause}
                    GROUP BY character
                """)
                character_breakdown = dict(cursor.fetchall())
                
                # Daily usage
                cursor = conn.execute(f"""
                    SELECT DATE(timestamp), SUM(total_tokens)
                    FROM token_usage {where_clause}
                    GROUP BY DATE(timestamp)
                    ORDER BY DATE(timestamp)
                """)
                daily_usage = dict(cursor.fetchall())
                
                return UsageStats(
                    total_tokens=total_tokens,
                    total_cost=total_cost,
                    requests_count=requests_count,
                    avg_tokens_per_request=avg_tokens,
                    character_breakdown=character_breakdown,
                    daily_usage=daily_usage
                )
                
        except Exception as e:
            logger.error(f"Failed to get usage stats: {e}")
            return UsageStats(0, 0.0, 0, 0.0, {}, {})
    
    def optimize_memory_context(self, character: str, current_memories: List[Dict]) -> List[Dict]:
        """Optimize memory context to stay within token limits"""
        try:
            # Estimate tokens for current memories (rough estimate: 4 chars per token)
            total_chars = sum(len(str(memory)) for memory in current_memories)
            estimated_tokens = total_chars // 4
            
            # Check if we need to optimize
            if estimated_tokens <= self.memory_limits["medium_usage"]:
                return current_memories
            
            # Priority-based optimization
            optimized_memories = []
            current_tokens = 0
            target_limit = self.memory_limits["medium_usage"]
            
            # Sort by priority (recent conversations, important memories)
            sorted_memories = sorted(current_memories, key=lambda m: (
                m.get("importance", 5),  # Higher importance first
                m.get("timestamp", ""),  # More recent first
                -len(str(m))  # Shorter memories preferred when equal
            ), reverse=True)
            
            for memory in sorted_memories:
                memory_tokens = len(str(memory)) // 4
                if current_tokens + memory_tokens <= target_limit:
                    optimized_memories.append(memory)
                    current_tokens += memory_tokens
                else:
                    # Try to summarize instead of dropping
                    if memory.get("content"):
                        summary = self.summarize_memory(memory["content"])
                        summary_tokens = len(summary) // 4
                        if current_tokens + summary_tokens <= target_limit:
                            memory_copy = memory.copy()
                            memory_copy["content"] = summary
                            memory_copy["summarized"] = True
                            optimized_memories.append(memory_copy)
                            current_tokens += summary_tokens
            
            logger.info(f"Optimized memories for {character}: {len(current_memories)} -> {len(optimized_memories)} items, ~{current_tokens} tokens")
            return optimized_memories
            
        except Exception as e:
            logger.error(f"Failed to optimize memory context: {e}")
            return current_memories[:10]  # Fallback to first 10 memories
    
    def summarize_memory(self, content: str, max_length: int = 200) -> str:
        """Create a concise summary of memory content"""
        if len(content) <= max_length:
            return content
        
        # Simple extractive summarization
        sentences = content.split('. ')
        if len(sentences) <= 2:
            return content[:max_length] + "..."
        
        # Keep first and last sentence, plus key phrases
        summary_parts = [sentences[0]]
        if len(sentences) > 2:
            summary_parts.append(sentences[-1])
        
        summary = '. '.join(summary_parts)
        if len(summary) > max_length:
            summary = summary[:max_length] + "..."
        
        return summary
    
    def get_character_usage_report(self, character: str, days: int = 30) -> Dict[str, Any]:
        """Get detailed usage report for a specific character"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT 
                        COUNT(*) as total_requests,
                        SUM(total_tokens) as total_tokens,
                        SUM(estimated_cost) as total_cost,
                        AVG(total_tokens) as avg_tokens_per_request,
                        AVG(memory_context_size) as avg_memory_size,
                        SUM(CASE WHEN avatar_processing THEN 1 ELSE 0 END) as avatar_requests
                    FROM token_usage 
                    WHERE character = ? AND timestamp >= date('now', '-{} days')
                """.format(days), (character,))
                
                row = cursor.fetchone()
                
                # Recent sessions
                cursor = conn.execute("""
                    SELECT session_id, start_time, total_tokens, total_cost, request_count
                    FROM usage_sessions 
                    WHERE character = ? AND start_time >= date('now', '-{} days')
                    ORDER BY start_time DESC
                    LIMIT 10
                """.format(days), (character,))
                
                recent_sessions = [
                    {
                        "session_id": row[0],
                        "start_time": row[1],
                        "total_tokens": row[2],
                        "total_cost": row[3],
                        "request_count": row[4]
                    }
                    for row in cursor.fetchall()
                ]
                
                return {
                    "character": character,
                    "period_days": days,
                    "total_requests": row[0] or 0,
                    "total_tokens": row[1] or 0,
                    "total_cost": row[2] or 0.0,
                    "avg_tokens_per_request": row[3] or 0.0,
                    "avg_memory_size": row[4] or 0.0,
                    "avatar_requests": row[5] or 0,
                    "recent_sessions": recent_sessions
                }
                
        except Exception as e:
            logger.error(f"Failed to get character usage report: {e}")
            return {}
    
    def set_optimization_rules(self, character: str, memory_limit: int, 
                             summarization_threshold: int, priority_keywords: List[str] = None):
        """Set optimization rules for a character"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                keywords_json = json.dumps(priority_keywords or [])
                
                conn.execute("""
                    INSERT OR REPLACE INTO optimization_rules
                    (character, memory_limit, summarization_threshold, priority_keywords)
                    VALUES (?, ?, ?, ?)
                """, (character, memory_limit, summarization_threshold, keywords_json))
                
                conn.commit()
                logger.info(f"Set optimization rules for {character}")
                
        except Exception as e:
            logger.error(f"Failed to set optimization rules: {e}")
    
    def get_daily_usage_trend(self, days: int = 30) -> Dict[str, Any]:
        """Get daily usage trends"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT 
                        DATE(timestamp) as date,
                        COUNT(*) as requests,
                        SUM(total_tokens) as tokens,
                        SUM(estimated_cost) as cost,
                        GROUP_CONCAT(DISTINCT character) as characters
                    FROM token_usage 
                    WHERE timestamp >= date('now', '-{} days')
                    GROUP BY DATE(timestamp)
                    ORDER BY DATE(timestamp)
                """.format(days))
                
                daily_data = []
                for row in cursor.fetchall():
                    daily_data.append({
                        "date": row[0],
                        "requests": row[1],
                        "tokens": row[2],
                        "cost": row[3],
                        "characters": row[4].split(',') if row[4] else []
                    })
                
                return {
                    "period_days": days,
                    "daily_data": daily_data,
                    "total_days": len(daily_data)
                }
                
        except Exception as e:
            logger.error(f"Failed to get daily usage trend: {e}")
            return {"period_days": days, "daily_data": [], "total_days": 0}

def create_token_usage(session_id: str, character: str, request_type: str,
                      prompt_tokens: int, completion_tokens: int, model: str = "gemini-pro",
                      memory_context_size: int = 0, avatar_processing: bool = False) -> TokenUsage:
    """Helper function to create TokenUsage object"""
    total_tokens = prompt_tokens + completion_tokens
    manager = TECTokenManager()
    estimated_cost = manager.estimate_cost(total_tokens, model)
    
    return TokenUsage(
        session_id=session_id,
        timestamp=datetime.datetime.now().isoformat(),
        character=character,
        request_type=request_type,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        estimated_cost=estimated_cost,
        model=model,
        memory_context_size=memory_context_size,
        avatar_processing=avatar_processing
    )
