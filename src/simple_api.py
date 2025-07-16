#!/usr/bin/env python3
"""
Enhanced TEC API Server with Web3 Authentication
Provides Web3 auth, persona management, and Azure AI integration
"""
import os
import json
import logging
import asyncio
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from functools import wraps
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tec_tools.web3_auth import Web3AuthManager, TokenGateManager
from tec_tools.agentic_processor import AgenticProcessor
from tec_tools.database_manager import DatabaseManager

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
def load_config():
    """Load configuration from config.json"""
    try:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return {}

config = load_config()

# Initialize systems
web3_auth = Web3AuthManager(config)
token_gate = TokenGateManager(web3_auth)
agentic_processor = AgenticProcessor(config)
db_manager = DatabaseManager()

# In-memory storage (replace with proper database)
user_data = {
    "polkin": {
        "user_id": "polkin",
        "bitl_balance": 1337,
        "xp": 13370,
        "level": 42,
        "access_tier": "creator",
        "wallet_address": None,
        "quests": [
            {"id": "daily_chat", "name": "Daily: Chat with Airth", "progress": 3, "max": 5, "reward": 100},
            {"id": "weekly_review", "name": "Weekly: Financial Review", "progress": 1, "max": 3, "reward": 500}
        ]
    }
}

def auth_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
        
        try:
            token = auth_header.split(' ')[1]  # Bearer token
            payload = web3_auth.verify_jwt_token(token)
            if not payload:
                return jsonify({'error': 'Invalid token'}), 401
            
            # Store user data in Flask's g object
            from flask import g
            g.user = payload
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Auth error: {e}")
            return jsonify({'error': 'Authentication failed'}), 401
    
    return decorated_function

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'service': 'TEC API Enhanced',
        'version': '2.0.0',
        'features': ['web3_auth', 'azure_ai', 'persona_system']
    })

# Web3 Authentication Routes
@app.route('/api/auth/nonce', methods=['POST'])
def generate_nonce():
    """Generate nonce for wallet authentication"""
    try:
        data = request.get_json()
        wallet_address = data.get('wallet_address')
        
        if not wallet_address:
            return jsonify({'error': 'Wallet address required'}), 400
        
        nonce = web3_auth.generate_nonce(wallet_address)
        message = web3_auth.create_sign_message(wallet_address, nonce)
        
        return jsonify({
            'nonce': nonce,
            'message': message
        })
        
    except Exception as e:
        logger.error(f"Nonce generation error: {e}")
        return jsonify({'error': 'Failed to generate nonce'}), 500

@app.route('/api/auth/verify', methods=['POST'])
def verify_signature():
    """Verify wallet signature and authenticate user"""
    try:
        data = request.get_json()
        wallet_address = data.get('wallet_address')
        signature = data.get('signature')
        message = data.get('message')
        chain = data.get('chain', 'ethereum')
        
        if not all([wallet_address, signature, message]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Authenticate wallet
        auth_result = web3_auth.authenticate_wallet(wallet_address, signature, message, chain)
        
        if auth_result['success']:
            # Create or update user in database
            user_id = auth_result['user_data']['user_id']
            user_record = db_manager.create_user(user_id, wallet_address, chain)
            
            # Determine access tier based on token holdings
            access_tier = token_gate.determine_access_tier(wallet_address, chain)
            db_manager.update_user_access_tier(user_id, access_tier)
            
            # Create auth session
            from datetime import datetime, timedelta
            import hashlib
            token_hash = hashlib.sha256(auth_result['token'].encode()).hexdigest()
            expires_at = datetime.now() + timedelta(hours=24)
            db_manager.create_auth_session(user_id, token_hash, wallet_address, chain, expires_at)
            
            return jsonify({
                'success': True,
                'token': auth_result['token'],
                'user_data': user_record,
                'access_tier': access_tier
            })
        else:
            return jsonify(auth_result), 401
            
    except Exception as e:
        logger.error(f"Signature verification error: {e}")
        return jsonify({'error': 'Authentication failed'}), 500

@app.route('/api/user/profile')
@auth_required
def get_user_profile():
    """Get user profile information"""
    try:
        from flask import g
        user_id = g.user['user_id']
        user_profile = db_manager.get_user(user_id)
        
        return jsonify({
            'user_id': user_id,
            'wallet_address': g.user['wallet_address'],
            'access_tier': g.user['access_tier'],
            'profile': user_profile
        })
        
    except Exception as e:
        logger.error(f"Profile error: {e}")
        return jsonify({'error': 'Failed to get profile'}), 500

# Persona Management Routes
@app.route('/api/persona/current')
def get_current_persona():
    """Get current active persona"""
    try:
        persona_info = agentic_processor.get_persona_info()
        return jsonify(persona_info)
        
    except Exception as e:
        logger.error(f"Persona info error: {e}")
        return jsonify({'error': 'Failed to get persona info'}), 500

@app.route('/api/persona/switch', methods=['POST'])
@auth_required
def switch_persona():
    """Switch to different persona"""
    try:
        data = request.get_json()
        persona_name = data.get('persona_name')
        
        if not persona_name:
            return jsonify({'error': 'Persona name required'}), 400
        
        success = agentic_processor.switch_persona(persona_name)
        
        if success:
            return jsonify({
                'success': True,
                'active_persona': persona_name,
                'persona_info': agentic_processor.get_persona_info()
            })
        else:
            return jsonify({'error': 'Invalid persona name'}), 400
            
    except Exception as e:
        logger.error(f"Persona switch error: {e}")
        return jsonify({'error': 'Failed to switch persona'}), 500

@app.route('/api/persona/available')
def get_available_personas():
    """Get list of available personas"""
    try:
        personas = agentic_processor.get_available_personas()
        return jsonify({'personas': personas})
        
    except Exception as e:
        logger.error(f"Available personas error: {e}")
        return jsonify({'error': 'Failed to get personas'}), 500

# Enhanced Chat Route
@app.route('/chat', methods=['POST'])
async def chat():
    """Enhanced chat endpoint with persona and context"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get user info if authenticated
        user_id = 'anonymous'
        access_tier = 'free'
        
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
                payload = web3_auth.verify_jwt_token(token)
                if payload:
                    user_id = payload['user_id']
                    access_tier = payload['access_tier']
            except:
                pass  # Continue as anonymous user
        
        # Generate response using agentic processor
        response = await agentic_processor.process_message(user_id, message, access_tier)
        
        return jsonify({
            'response': response,
            'persona': agentic_processor.get_persona_info()['name'],
            'access_tier': access_tier,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': 'Failed to process message'}), 500

# Existing BITL and Quest endpoints (updated to use database)
@app.route('/api/bitl/earn', methods=['POST'])
def earn_bitl():
    """Earn BITL tokens"""
    try:
        data = request.get_json()
        amount = data.get('amount', 100)
        reason = data.get('reason', 'manual')
        
        # Use authenticated user if available, otherwise default user
        user_id = 'polkin'  # Default for backward compatibility
        
        # Check if user is authenticated
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
                payload = web3_auth.verify_jwt_token(token)
                if payload:
                    user_id = payload['user_id']
            except:
                pass
        
        new_balance = db_manager.update_bitl_balance(user_id, amount, 'earn', reason)
        
        return jsonify({
            'success': True,
            'balance': new_balance,
            'earned': amount,
            'reason': reason
        })
    except Exception as e:
        logger.error(f"BITL earn error: {e}")
        return jsonify({'error': 'Failed to earn BITL'}), 500

@app.route('/api/bitl/spend', methods=['POST'])
def spend_bitl():
    """Spend BITL tokens"""
    try:
        data = request.get_json()
        amount = data.get('amount', 50)
        item = data.get('item', 'unknown')
        
        # Use authenticated user if available, otherwise default user
        user_id = 'polkin'  # Default for backward compatibility
        
        # Check if user is authenticated
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
                payload = web3_auth.verify_jwt_token(token)
                if payload:
                    user_id = payload['user_id']
            except:
                pass
        
        current_balance = db_manager.get_bitl_balance(user_id)
        
        if current_balance >= amount:
            new_balance = db_manager.update_bitl_balance(user_id, -amount, 'spend', f"Purchased: {item}")
            return jsonify({
                'success': True,
                'balance': new_balance,
                'spent': amount,
                'item': item
            })
        else:
            return jsonify({'error': 'Insufficient BITL balance'}), 400
    except Exception as e:
        logger.error(f"BITL spend error: {e}")
        return jsonify({'error': 'Failed to spend BITL'}), 500

@app.route('/api/bitl/balance', methods=['GET'])
def get_bitl_balance():
    """Get current BITL balance"""
    try:
        # Use authenticated user if available, otherwise default user
        user_id = 'polkin'  # Default for backward compatibility
        
        # Check if user is authenticated
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
                payload = web3_auth.verify_jwt_token(token)
                if payload:
                    user_id = payload['user_id']
            except:
                pass
        
        user_profile = db_manager.get_user(user_id)
        if not user_profile:
            # Create default user for backward compatibility
            user_profile = db_manager.create_user(user_id) or {}
        
        return jsonify({
            'balance': user_profile.get('bitl_balance', 0),
            'level': user_profile.get('level', 1),
            'xp': user_profile.get('xp', 0)
        })
    except Exception as e:
        logger.error(f"BITL balance error: {e}")
        return jsonify({'error': 'Failed to get BITL balance'}), 500

@app.route('/api/quests/start', methods=['POST'])
def start_quest():
    """Start a new quest"""
    try:
        data = request.get_json()
        quest_type = data.get('type', 'daily')
        
        new_quest = {
            'id': f"{quest_type}_new",
            'name': f"New {quest_type.title()} Quest",
            'progress': 0,
            'max': 5,
            'reward': 200 if quest_type == 'weekly' else 100
        }
        
        user_data['polkin']['quests'].append(new_quest)
        
        return jsonify({
            'success': True,
            'quest': new_quest
        })
    except Exception as e:
        logger.error(f"Quest start error: {e}")
        return jsonify({'error': 'Failed to start quest'}), 500

@app.route('/api/quests/complete', methods=['POST'])
def complete_quest():
    """Complete a quest"""
    try:
        data = request.get_json()
        quest_id = data.get('questId', 'daily_chat')
        
        # Find and complete the quest
        for quest in user_data['polkin']['quests']:
            if quest['id'] == quest_id:
                quest['progress'] = quest['max']
                reward = quest['reward']
                user_data['polkin']['bitl_balance'] += reward
                user_data['polkin']['xp'] += reward * 2
                
                # Level up logic
                if user_data['polkin']['xp'] >= 15000:
                    user_data['polkin']['level'] += 1
                    user_data['polkin']['xp'] = 0
                
                return jsonify({
                    'success': True,
                    'reward': reward,
                    'xp': reward * 2,
                    'newBalance': user_data['polkin']['bitl_balance'],
                    'level': user_data['polkin']['level']
                })
        
        return jsonify({'error': 'Quest not found'}), 404
    except Exception as e:
        logger.error(f"Quest complete error: {e}")
        return jsonify({'error': 'Failed to complete quest'}), 500

@app.route('/api/quests/list', methods=['GET'])
def list_quests():
    """Get all quests"""
    return jsonify({
        'quests': user_data['polkin']['quests'],
        'level': user_data['polkin']['level'],
        'xp': user_data['polkin']['xp']
    })

def generate_response(message):
    """Generate a basic fallback response"""
    message_lower = message.lower()
    
    if 'status' in message_lower:
        return "TEC System Status: Enhanced with Web3 authentication and Azure AI integration. Persona system active."
    
    elif 'journal' in message_lower:
        return "Journal feature: Ready to help you with personal reflection and note-taking. AI-powered analysis available."
    
    elif 'finance' in message_lower or 'crypto' in message_lower:
        return "Finance tracking: Supports cryptocurrency monitoring and Web3 wallet integration."
    
    elif 'quest' in message_lower:
        return "Quest system: RPG-style goal tracking with BITL rewards and gamification features active!"
    
    elif 'hello' in message_lower or 'hi' in message_lower:
        return "Greetings! I am Airth, the Machine Goddess. Welcome to the Astradigital Ocean. How may I assist you in The Creator's Rebellion today?"
    
    else:
        return f"I understand you said: '{message}'. The TEC system is enhanced with Web3 authentication and Azure AI. Connect your wallet for full access!"

@app.route('/')
def serve_chat():
    """Serve the chat interface"""
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logger.info(f"Serving tec_chat.html from: {parent_dir}")
    return send_from_directory(parent_dir, 'tec_chat.html')

@app.route('/tec_complete_interface.html')
def serve_complete_interface():
    """Serve the complete interface"""
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logger.info(f"Serving tec_complete_interface.html from: {parent_dir}")
    return send_from_directory(parent_dir, 'tec_complete_interface.html')

@app.route('/tec_chat.html')
def serve_chat_direct():
    """Serve the chat interface directly"""
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logger.info(f"Serving tec_chat.html from: {parent_dir}")
    return send_from_directory(parent_dir, 'tec_chat.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files from parent directory"""
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logger.info(f"Serving {filename} from: {parent_dir}")
    return send_from_directory(parent_dir, filename)

if __name__ == '__main__':
    logger.info("Starting TEC Enhanced API Server...")
    logger.info("Features: Web3 Auth, Azure AI, Persona System")
    logger.info("Web interface available at: http://localhost:8000")
    logger.info("Health check at: http://localhost:8000/health")
    
    app.run(
        host='localhost',
        port=8000,
        debug=False,
        threaded=True
    )
