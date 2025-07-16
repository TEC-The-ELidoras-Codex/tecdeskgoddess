#!/usr/bin/env python3
"""
Database Manager for TEC: BITLyfe
Handles persistent storage for user data, authentication, and Web3 integration
"""
import os
import json
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from contextlib import contextmanager
import hashlib

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages SQLite database operations for TEC: BITLyfe"""
    
    def __init__(self, db_path: str = "tec_database.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,
                    wallet_address TEXT UNIQUE,
                    chain TEXT,
                    access_tier TEXT DEFAULT 'free',
                    bitl_balance INTEGER DEFAULT 0,
                    xp INTEGER DEFAULT 0,
                    level INTEGER DEFAULT 1,
                    avatar_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    last_activity TIMESTAMP
                )
            ''')
            
            # Authentication sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS auth_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    token_hash TEXT NOT NULL,
                    wallet_address TEXT NOT NULL,
                    chain TEXT NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            # Quests table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS quests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    quest_id TEXT NOT NULL,
                    quest_name TEXT NOT NULL,
                    quest_type TEXT DEFAULT 'daily',
                    progress INTEGER DEFAULT 0,
                    max_progress INTEGER DEFAULT 1,
                    reward INTEGER DEFAULT 100,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            # Transactions table for BITL tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bitl_transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    transaction_type TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    balance_after INTEGER NOT NULL,
                    reason TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            # Conversation history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    persona TEXT DEFAULT 'airth',
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            # NFT Holdings table (for access tier determination)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS nft_holdings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    wallet_address TEXT NOT NULL,
                    chain TEXT NOT NULL,
                    collection_name TEXT NOT NULL,
                    contract_address TEXT NOT NULL,
                    token_id TEXT,
                    quantity INTEGER DEFAULT 1,
                    last_verified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            conn.commit()
            logger.info("Database initialized successfully")
    
    @contextmanager
    def get_connection(self):
        """Get database connection with automatic cleanup"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        try:
            yield conn
        finally:
            conn.close()
    
    def create_user(self, user_id: str, wallet_address: Optional[str] = None, chain: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Create a new user"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    INSERT INTO users (user_id, wallet_address, chain, last_login)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, wallet_address, chain, datetime.now()))
                
                conn.commit()
                return self.get_user(user_id)
                
            except sqlite3.IntegrityError:
                # User already exists, update wallet info
                cursor.execute('''
                    UPDATE users 
                    SET wallet_address = ?, chain = ?, last_login = ?
                    WHERE user_id = ?
                ''', (wallet_address, chain, datetime.now(), user_id))
                
                conn.commit()
                return self.get_user(user_id)
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by user_id"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
    
    def get_user_by_wallet(self, wallet_address: str) -> Optional[Dict[str, Any]]:
        """Get user by wallet address"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE wallet_address = ?', (wallet_address,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
    
    def update_user_activity(self, user_id: str):
        """Update user's last activity timestamp"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users 
                SET last_activity = ?
                WHERE user_id = ?
            ''', (datetime.now(), user_id))
            conn.commit()
    
    def update_user_access_tier(self, user_id: str, access_tier: str):
        """Update user's access tier"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users 
                SET access_tier = ?
                WHERE user_id = ?
            ''', (access_tier, user_id))
            conn.commit()
    
    def create_auth_session(self, user_id: str, token_hash: str, wallet_address: str, chain: str, expires_at: datetime):
        """Create authentication session"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO auth_sessions (user_id, token_hash, wallet_address, chain, expires_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, token_hash, wallet_address, chain, expires_at))
            conn.commit()
    
    def get_auth_session(self, token_hash: str) -> Optional[Dict[str, Any]]:
        """Get authentication session by token hash"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM auth_sessions 
                WHERE token_hash = ? AND expires_at > ?
            ''', (token_hash, datetime.now()))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
    
    def cleanup_expired_sessions(self):
        """Remove expired authentication sessions"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM auth_sessions 
                WHERE expires_at < ?
            ''', (datetime.now(),))
            conn.commit()
    
    def update_bitl_balance(self, user_id: str, amount: int, transaction_type: str, reason: Optional[str] = None) -> int:
        """Update BITL balance and record transaction"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get current balance
            cursor.execute('SELECT bitl_balance FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            current_balance = row['bitl_balance'] if row else 0
            
            # Calculate new balance
            new_balance = current_balance + amount
            
            # Ensure balance doesn't go negative
            if new_balance < 0:
                new_balance = 0
                amount = -current_balance
            
            # Update user balance
            cursor.execute('''
                UPDATE users 
                SET bitl_balance = ?
                WHERE user_id = ?
            ''', (new_balance, user_id))
            
            # Record transaction
            cursor.execute('''
                INSERT INTO bitl_transactions (user_id, transaction_type, amount, balance_after, reason)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, transaction_type, amount, new_balance, reason))
            
            conn.commit()
            return new_balance
    
    def get_bitl_balance(self, user_id: str) -> int:
        """Get user's BITL balance"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT bitl_balance FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            return row['bitl_balance'] if row else 0
    
    def create_quest(self, user_id: str, quest_id: str, quest_name: str, quest_type: str = 'daily', 
                    max_progress: int = 1, reward: int = 100) -> Dict[str, Any]:
        """Create a new quest"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO quests (user_id, quest_id, quest_name, quest_type, max_progress, reward)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, quest_id, quest_name, quest_type, max_progress, reward))
            
            quest_db_id = cursor.lastrowid
            conn.commit()
            
            return {
                'id': quest_db_id,
                'quest_id': quest_id,
                'quest_name': quest_name,
                'quest_type': quest_type,
                'progress': 0,
                'max_progress': max_progress,
                'reward': reward,
                'status': 'active'
            }
    
    def get_user_quests(self, user_id: str, status: str = 'active') -> List[Dict[str, Any]]:
        """Get user's quests"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM quests 
                WHERE user_id = ? AND status = ?
                ORDER BY created_at DESC
            ''', (user_id, status))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def update_quest_progress(self, user_id: str, quest_id: str, progress: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """Update quest progress"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get current quest
            cursor.execute('''
                SELECT * FROM quests 
                WHERE user_id = ? AND quest_id = ? AND status = 'active'
                ORDER BY created_at DESC LIMIT 1
            ''', (user_id, quest_id))
            
            quest = cursor.fetchone()
            if not quest:
                return None
            
            # Update progress (increment by 1 if not specified)
            new_progress = progress if progress is not None else quest['progress'] + 1
            
            # Check if quest is completed
            status = 'completed' if new_progress >= quest['max_progress'] else 'active'
            completed_at = datetime.now() if status == 'completed' else None
            
            cursor.execute('''
                UPDATE quests 
                SET progress = ?, status = ?, completed_at = ?
                WHERE id = ?
            ''', (new_progress, status, completed_at, quest['id']))
            
            conn.commit()
            
            # Return updated quest
            cursor.execute('SELECT * FROM quests WHERE id = ?', (quest['id'],))
            return dict(cursor.fetchone())
    
    def add_conversation(self, user_id: str, role: str, content: str, persona: str = 'airth'):
        """Add message to conversation history"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO conversations (user_id, persona, role, content)
                VALUES (?, ?, ?, ?)
            ''', (user_id, persona, role, content))
            conn.commit()
    
    def get_conversation_history(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get conversation history"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM conversations 
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def update_nft_holdings(self, user_id: str, wallet_address: str, chain: str, 
                           collection_name: str, contract_address: str, quantity: int = 1):
        """Update NFT holdings for access tier calculation"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if record exists
            cursor.execute('''
                SELECT id FROM nft_holdings 
                WHERE user_id = ? AND wallet_address = ? AND chain = ? AND collection_name = ?
            ''', (user_id, wallet_address, chain, collection_name))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing record
                cursor.execute('''
                    UPDATE nft_holdings 
                    SET quantity = ?, last_verified = ?
                    WHERE id = ?
                ''', (quantity, datetime.now(), existing['id']))
            else:
                # Insert new record
                cursor.execute('''
                    INSERT INTO nft_holdings (user_id, wallet_address, chain, collection_name, contract_address, quantity)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, wallet_address, chain, collection_name, contract_address, quantity))
            
            conn.commit()
    
    def get_nft_holdings(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's NFT holdings"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM nft_holdings 
                WHERE user_id = ?
                ORDER BY last_verified DESC
            ''', (user_id,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get user data
            user = self.get_user(user_id)
            if not user:
                return {}
            
            # Get quest stats
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_quests,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_quests,
                    SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_quests
                FROM quests 
                WHERE user_id = ?
            ''', (user_id,))
            
            quest_stats = dict(cursor.fetchone())
            
            # Get transaction stats
            cursor.execute('''
                SELECT 
                    SUM(CASE WHEN transaction_type = 'earn' THEN amount ELSE 0 END) as total_earned,
                    SUM(CASE WHEN transaction_type = 'spend' THEN amount ELSE 0 END) as total_spent,
                    COUNT(*) as total_transactions
                FROM bitl_transactions 
                WHERE user_id = ?
            ''', (user_id,))
            
            transaction_stats = dict(cursor.fetchone())
            
            # Get NFT holdings count
            cursor.execute('''
                SELECT COUNT(*) as nft_collections
                FROM nft_holdings 
                WHERE user_id = ?
            ''', (user_id,))
            
            nft_stats = dict(cursor.fetchone())
            
            return {
                'user': user,
                'quests': quest_stats,
                'transactions': transaction_stats,
                'nfts': nft_stats
            }
