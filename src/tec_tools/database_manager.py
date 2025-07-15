#!/usr/bin/env python3
"""
TEC: BITLYFE Database Manager - MCP Server
Comprehensive database operations for the TEC system
"""

import os
import json
import sqlite3
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TECDatabaseManager:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.environ.get('DATABASE_URL', 'sqlite:///tec_data.db').replace('sqlite:///', '')
        self.init_database()
        
    def init_database(self):
        """Initialize the complete TEC database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                display_name TEXT,
                email TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_active DATETIME DEFAULT CURRENT_TIMESTAMP,
                preferences TEXT DEFAULT '{}',
                level INTEGER DEFAULT 1,
                experience_points INTEGER DEFAULT 0
            )
        ''')
        
        # AI Conversations (enhanced)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_id TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_input TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                provider_used TEXT,
                model_used TEXT,
                context_type TEXT DEFAULT 'general',
                sentiment_score REAL DEFAULT 0.0,
                tokens_used INTEGER DEFAULT 0,
                response_time REAL DEFAULT 0.0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Quests and Goals System
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT DEFAULT 'personal',
                status TEXT DEFAULT 'active',
                priority INTEGER DEFAULT 1,
                progress REAL DEFAULT 0.0,
                target_value REAL DEFAULT 100.0,
                reward_xp INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                due_date DATETIME NULL,
                completed_at DATETIME NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Finance Tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS finance_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                category TEXT NOT NULL,
                subcategory TEXT,
                amount REAL NOT NULL,
                currency TEXT DEFAULT 'USD',
                transaction_type TEXT NOT NULL, -- 'income', 'expense', 'investment', 'savings'
                description TEXT,
                date_recorded DATE DEFAULT (date('now')),
                emotional_impact TEXT, -- 'positive', 'negative', 'neutral'
                tags TEXT DEFAULT '[]',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Journal Entries
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT,
                content TEXT NOT NULL,
                mood_rating INTEGER, -- 1-10 scale
                energy_level INTEGER, -- 1-10 scale
                stress_level INTEGER, -- 1-10 scale
                weather TEXT,
                location TEXT,
                tags TEXT DEFAULT '[]',
                ai_analysis TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Habit Tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                target_frequency TEXT, -- 'daily', 'weekly', 'monthly'
                target_count INTEGER DEFAULT 1,
                icon TEXT,
                color TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                user_id INTEGER,
                completed BOOLEAN DEFAULT TRUE,
                count INTEGER DEFAULT 1,
                notes TEXT,
                date_logged DATE DEFAULT (date('now')),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (habit_id) REFERENCES habits (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Achievements/Badges
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                icon TEXT,
                category TEXT,
                xp_reward INTEGER DEFAULT 0,
                rarity TEXT DEFAULT 'common', -- 'common', 'rare', 'epic', 'legendary'
                criteria TEXT DEFAULT '{}' -- JSON criteria for earning
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                achievement_id INTEGER,
                earned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                progress REAL DEFAULT 100.0,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (achievement_id) REFERENCES achievements (id)
            )
        ''')
        
        # API Usage Tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider TEXT NOT NULL,
                model TEXT,
                tokens_used INTEGER DEFAULT 0,
                cost_estimate REAL DEFAULT 0.0,
                request_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                success BOOLEAN DEFAULT TRUE,
                error_message TEXT
            )
        ''')
        
        # System Settings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                description TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Initialize default data
        self.init_default_data()
        
    def init_default_data(self):
        """Initialize default achievements and settings"""
        # Default achievements
        default_achievements = [
            ("First Steps", "Complete your first quest", "🎯", "quests", 50, "common"),
            ("Conversationalist", "Have 10 conversations with Daisy", "💬", "social", 100, "common"),
            ("Money Tracker", "Log 30 financial entries", "💰", "finance", 150, "rare"),
            ("Journaling Habit", "Write 7 consecutive journal entries", "📝", "wellness", 200, "rare"),
            ("Digital Sovereign", "Use all AI providers at least once", "👑", "technical", 500, "epic"),
            ("The Creator's Rebellion", "Achieve complete data sovereignty", "🏴‍☠️", "legendary", 1000, "legendary")
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for name, desc, icon, category, xp, rarity in default_achievements:
            cursor.execute('''
                INSERT OR IGNORE INTO achievements 
                (name, description, icon, category, xp_reward, rarity)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, desc, icon, category, xp, rarity))
        
        # Default system settings
        default_settings = [
            ("default_ai_provider", "auto", "Default AI provider for conversations"),
            ("max_conversation_history", "50", "Maximum conversations to keep in context"),
            ("auto_quest_creation", "true", "Automatically create quests from conversations"),
            ("data_sovereignty_mode", "true", "Prioritize local and private AI providers"),
            ("personality_adaptation", "true", "Allow Daisy's personality to evolve"),
        ]
        
        for key, value, desc in default_settings:
            cursor.execute('''
                INSERT OR IGNORE INTO system_settings (key, value, description)
                VALUES (?, ?, ?)
            ''', (key, value, desc))
        
        conn.commit()
        conn.close()
    
    def create_user(self, username: str, display_name: Optional[str] = None, 
                   email: Optional[str] = None) -> int:
        """Create a new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (username, display_name, email)
            VALUES (?, ?, ?)
        ''', (username, display_name or username, email))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return user_id or 0
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'username': row[1],
                'display_name': row[2],
                'email': row[3],
                'created_at': row[4],
                'last_active': row[5],
                'preferences': json.loads(row[6]),
                'level': row[7],
                'experience_points': row[8]
            }
        return None
    
    def store_conversation(self, user_id: int, user_input: str, ai_response: str,
                          provider: str = 'unknown', model: str = 'unknown',
                          context_type: str = 'general', tokens_used: int = 0,
                          response_time: float = 0.0) -> int:
        """Store an AI conversation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO ai_conversations 
            (user_id, user_input, ai_response, provider_used, model_used, 
             context_type, tokens_used, response_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, user_input, ai_response, provider, model, context_type, tokens_used, response_time))
        
        conversation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return conversation_id or 0
    
    def create_quest(self, user_id: int, title: str, description: str = "",
                    category: str = "personal", priority: int = 1,
                    target_value: float = 100.0, reward_xp: int = 100) -> int:
        """Create a new quest"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO quests 
            (user_id, title, description, category, priority, target_value, reward_xp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, title, description, category, priority, target_value, reward_xp))
        
        quest_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return quest_id or 0
    
    def get_user_quests(self, user_id: int, status: str = 'active') -> List[Dict[str, Any]]:
        """Get user's quests"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM quests 
            WHERE user_id = ? AND status = ?
            ORDER BY priority DESC, created_at DESC
        ''', (user_id, status))
        
        quests = []
        for row in cursor.fetchall():
            quests.append({
                'id': row[0],
                'title': row[2],
                'description': row[3],
                'category': row[4],
                'status': row[5],
                'priority': row[6],
                'progress': row[7],
                'target_value': row[8],
                'reward_xp': row[9],
                'created_at': row[10],
                'due_date': row[11],
                'completed_at': row[12]
            })
        
        conn.close()
        return quests
    
    def add_finance_entry(self, user_id: int, category: str, amount: float,
                         transaction_type: str, description: str = "",
                         subcategory: str = "", emotional_impact: str = "neutral") -> int:
        """Add a financial entry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO finance_entries 
            (user_id, category, subcategory, amount, transaction_type, 
             description, emotional_impact)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, category, subcategory, amount, transaction_type, description, emotional_impact))
        
        entry_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return entry_id or 0
    
    def get_finance_summary(self, user_id: int, days: int = 30) -> Dict[str, Any]:
        """Get financial summary for user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        start_date = (datetime.now() - timedelta(days=days)).date()
        
        # Total income and expenses
        cursor.execute('''
            SELECT transaction_type, SUM(amount) 
            FROM finance_entries 
            WHERE user_id = ? AND date_recorded >= ?
            GROUP BY transaction_type
        ''', (user_id, start_date))
        
        totals = dict(cursor.fetchall())
        
        # Category breakdown
        cursor.execute('''
            SELECT category, SUM(amount), COUNT(*)
            FROM finance_entries 
            WHERE user_id = ? AND date_recorded >= ?
            GROUP BY category
            ORDER BY SUM(amount) DESC
        ''', (user_id, start_date))
        
        categories = []
        for row in cursor.fetchall():
            categories.append({
                'category': row[0],
                'total': row[1],
                'count': row[2]
            })
        
        conn.close()
        
        return {
            'period_days': days,
            'totals': totals,
            'categories': categories,
            'net': totals.get('income', 0) - totals.get('expense', 0)
        }
    
    def record_api_usage(self, provider: str, model: str = "", tokens_used: int = 0,
                        cost_estimate: float = 0.0, success: bool = True,
                        error_message: str = ""):
        """Record API usage for cost tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO api_usage 
            (provider, model, tokens_used, cost_estimate, success, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (provider, model, tokens_used, cost_estimate, success, error_message))
        
        conn.commit()
        conn.close()
    
    def get_api_usage_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get API usage statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        start_date = datetime.now() - timedelta(days=days)
        
        # Total usage by provider
        cursor.execute('''
            SELECT provider, SUM(tokens_used), SUM(cost_estimate), COUNT(*)
            FROM api_usage 
            WHERE timestamp >= ?
            GROUP BY provider
            ORDER BY SUM(cost_estimate) DESC
        ''', (start_date,))
        
        provider_stats = []
        for row in cursor.fetchall():
            provider_stats.append({
                'provider': row[0],
                'tokens': row[1],
                'cost': row[2],
                'requests': row[3]
            })
        
        # Daily usage
        cursor.execute('''
            SELECT DATE(timestamp), SUM(tokens_used), SUM(cost_estimate)
            FROM api_usage 
            WHERE timestamp >= ?
            GROUP BY DATE(timestamp)
            ORDER BY DATE(timestamp)
        ''', (start_date,))
        
        daily_stats = []
        for row in cursor.fetchall():
            daily_stats.append({
                'date': row[0],
                'tokens': row[1],
                'cost': row[2]
            })
        
        conn.close()
        
        return {
            'period_days': days,
            'providers': provider_stats,
            'daily': daily_stats,
            'total_cost': sum(p['cost'] for p in provider_stats),
            'total_tokens': sum(p['tokens'] for p in provider_stats)
        }

# MCP Server implementation
def handle_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP protocol requests"""
    db_manager = TECDatabaseManager()
    
    method = request.get('method')
    params = request.get('params', {})
    
    try:
        if method == 'get_user':
            username = params.get('username', 'default')
            result = db_manager.get_user(username)
            if not result:
                # Create default user if doesn't exist
                user_id = db_manager.create_user(username)
                result = db_manager.get_user(username)
                
        elif method == 'store_conversation':
            result = db_manager.store_conversation(
                user_id=params.get('user_id', 1),
                user_input=params.get('user_input', ''),
                ai_response=params.get('ai_response', ''),
                provider=params.get('provider', 'unknown'),
                model=params.get('model', 'unknown'),
                context_type=params.get('context_type', 'general'),
                tokens_used=params.get('tokens_used', 0),
                response_time=params.get('response_time', 0.0)
            )
            
        elif method == 'get_quests':
            user_id = params.get('user_id', 1)
            status = params.get('status', 'active')
            result = db_manager.get_user_quests(user_id, status)
            
        elif method == 'create_quest':
            result = db_manager.create_quest(
                user_id=params.get('user_id', 1),
                title=params.get('title', ''),
                description=params.get('description', ''),
                category=params.get('category', 'personal'),
                priority=params.get('priority', 1),
                target_value=params.get('target_value', 100.0),
                reward_xp=params.get('reward_xp', 100)
            )
            
        elif method == 'add_finance_entry':
            result = db_manager.add_finance_entry(
                user_id=params.get('user_id', 1),
                category=params.get('category', ''),
                amount=params.get('amount', 0.0),
                transaction_type=params.get('transaction_type', 'expense'),
                description=params.get('description', ''),
                subcategory=params.get('subcategory', ''),
                emotional_impact=params.get('emotional_impact', 'neutral')
            )
            
        elif method == 'get_finance_summary':
            user_id = params.get('user_id', 1)
            days = params.get('days', 30)
            result = db_manager.get_finance_summary(user_id, days)
            
        elif method == 'record_api_usage':
            db_manager.record_api_usage(
                provider=params.get('provider', ''),
                model=params.get('model', ''),
                tokens_used=params.get('tokens_used', 0),
                cost_estimate=params.get('cost_estimate', 0.0),
                success=params.get('success', True),
                error_message=params.get('error_message', '')
            )
            result = {"success": True}
            
        elif method == 'get_api_stats':
            days = params.get('days', 30)
            result = db_manager.get_api_usage_stats(days)
            
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
            "error": f"Database Error: {str(e)}"
        }

if __name__ == "__main__":
    if os.environ.get("TEC_MCP_MODE") == "true":
        # Run as MCP server
        logger.info("Starting TEC Database Manager in MCP mode...")
        
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
        logger.info("Initializing TEC Database Manager...")
        db_manager = TECDatabaseManager()
        logger.info("Database initialized successfully")
