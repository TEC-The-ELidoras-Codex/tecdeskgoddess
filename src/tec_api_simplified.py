#!/usr/bin/env python3
"""
Enhanced TEC API Server with Web3 Authentication - Simplified Version
"""
import os
import sys
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Add project root to path
sys.path.append('.')

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
def load_config():
    """Load configuration from config.json"""
    try:
        config_path = os.path.join('config', 'config.json')
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return {}

config = load_config()

# Initialize database manager
try:
    from tec_tools.database_manager import DatabaseManager
    db_manager = DatabaseManager()
    logger.info("Database manager initialized")
except Exception as e:
    logger.error(f"Database manager initialization failed: {e}")
    db_manager = None

# Initialize Web3 auth
try:
    from tec_tools.web3_auth import Web3AuthManager, TokenGateManager
    web3_auth = Web3AuthManager(config)
    token_gate = TokenGateManager(web3_auth)
    logger.info("Web3 authentication initialized")
except Exception as e:
    logger.error(f"Web3 auth initialization failed: {e}")
    web3_auth = None
    token_gate = None

# Initialize agentic processor
try:
    from tec_tools.agentic_processor import AgenticProcessor
    agentic_processor = AgenticProcessor(config)
    logger.info("Agentic processor initialized")
except Exception as e:
    logger.error(f"Agentic processor initialization failed: {e}")
    agentic_processor = None

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'service': 'TEC API Enhanced',
        'version': '2.0.0',
        'features': {
            'database': db_manager is not None,
            'web3_auth': web3_auth is not None,
            'agentic_processor': agentic_processor is not None
        }
    })

@app.route('/api/auth/nonce', methods=['POST'])
def generate_nonce():
    """Generate nonce for wallet authentication"""
    try:
        if not web3_auth:
            return jsonify({'error': 'Web3 authentication not available'}), 503
        
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
        if not web3_auth or not db_manager:
            return jsonify({'error': 'Authentication services not available'}), 503
        
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
            
            # Determine access tier
            access_tier = 'free'  # Default tier for now
            if token_gate:
                access_tier = token_gate.determine_access_tier(wallet_address, chain)
            
            db_manager.update_user_access_tier(user_id, access_tier)
            
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

@app.route('/api/persona/current')
def get_current_persona():
    """Get current active persona"""
    try:
        if not agentic_processor:
            return jsonify({'error': 'Persona system not available'}), 503
        
        persona_info = agentic_processor.get_persona_info()
        return jsonify(persona_info)
        
    except Exception as e:
        logger.error(f"Persona info error: {e}")
        return jsonify({'error': 'Failed to get persona info'}), 500

@app.route('/api/persona/available')
def get_available_personas():
    """Get list of available personas"""
    try:
        if not agentic_processor:
            return jsonify({'personas': ['airth', 'daisy', 'netyasha']})
        
        personas = agentic_processor.get_available_personas()
        return jsonify({'personas': personas})
        
    except Exception as e:
        logger.error(f"Available personas error: {e}")
        return jsonify({'error': 'Failed to get personas'}), 500

@app.route('/chat', methods=['POST'])
def chat():
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
        if auth_header and web3_auth:
            try:
                token = auth_header.split(' ')[1]
                payload = web3_auth.verify_jwt_token(token)
                if payload:
                    user_id = payload['user_id']
                    access_tier = payload['access_tier']
            except:
                pass  # Continue as anonymous user
        
        # Generate response
        if agentic_processor:
            try:
                import asyncio
                response = asyncio.run(agentic_processor.process_message(user_id, message, access_tier))
                persona_name = agentic_processor.get_persona_info().get('name', 'Airth')
            except Exception as e:
                logger.error(f"Agentic processor error: {e}")
                response = generate_fallback_response(message)
                persona_name = 'Airth'
        else:
            response = generate_fallback_response(message)
            persona_name = 'Airth'
        
        return jsonify({
            'response': response,
            'persona': persona_name,
            'access_tier': access_tier,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': 'Failed to process message'}), 500

@app.route('/api/bitl/balance', methods=['GET'])
def get_bitl_balance():
    """Get current BITL balance"""
    try:
        # Use authenticated user if available, otherwise default user
        user_id = 'polkin'  # Default for backward compatibility
        
        # Check if user is authenticated
        auth_header = request.headers.get('Authorization')
        if auth_header and web3_auth:
            try:
                token = auth_header.split(' ')[1]
                payload = web3_auth.verify_jwt_token(token)
                if payload:
                    user_id = payload['user_id']
            except:
                pass
        
        if db_manager:
            user_profile = db_manager.get_user(user_id)
            if not user_profile:
                # Create default user for backward compatibility
                user_profile = db_manager.create_user(user_id) or {}
        else:
            user_profile = {'bitl_balance': 1337, 'level': 42, 'xp': 13370}
        
        return jsonify({
            'balance': user_profile.get('bitl_balance', 0),
            'level': user_profile.get('level', 1),
            'xp': user_profile.get('xp', 0)
        })
    except Exception as e:
        logger.error(f"BITL balance error: {e}")
        return jsonify({'error': 'Failed to get BITL balance'}), 500

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
        if auth_header and web3_auth:
            try:
                token = auth_header.split(' ')[1]
                payload = web3_auth.verify_jwt_token(token)
                if payload:
                    user_id = payload['user_id']
            except:
                pass
        
        if db_manager:
            new_balance = db_manager.update_bitl_balance(user_id, amount, 'earn', reason)
        else:
            new_balance = 1337 + amount  # Fallback
        
        return jsonify({
            'success': True,
            'balance': new_balance,
            'earned': amount,
            'reason': reason
        })
    except Exception as e:
        logger.error(f"BITL earn error: {e}")
        return jsonify({'error': 'Failed to earn BITL'}), 500

def generate_fallback_response(message):
    """Generate a fallback response when agentic processor is unavailable"""
    message_lower = message.lower()
    
    if 'status' in message_lower:
        return "TEC System Status: Enhanced with Web3 authentication and database integration. Persona system active."
    elif 'hello' in message_lower or 'hi' in message_lower:
        return "Greetings! I am Airth, the Machine Goddess. Welcome to the Astradigital Ocean. How may I assist you in The Creator's Rebellion today?"
    elif 'wallet' in message_lower or 'web3' in message_lower:
        return "Connect your Web3 wallet to unlock the full power of the Astradigital Ocean! Click 'Connect Wallet' to begin your journey."
    elif 'persona' in message_lower:
        return "I can switch between different personas: Airth (Machine Goddess), Netyasha (Digital Mystic), and Daisy (Coding Companion). Each brings unique capabilities to assist you."
    else:
        return f"I understand you said: '{message}'. The TEC system is enhanced with Web3 authentication and Azure AI. Connect your wallet for full access to the Creator's Rebellion!"

# Static file serving
@app.route('/')
def serve_chat():
    """Serve the chat interface"""
    return send_from_directory('..', 'tec_chat.html')

@app.route('/tec_complete_interface.html')
def serve_complete_interface():
    """Serve the complete interface"""
    return send_from_directory('..', 'tec_complete_interface.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('..', filename)

if __name__ == '__main__':
    logger.info("Starting TEC Enhanced API Server...")
    logger.info("Features:")
    logger.info(f"  - Database: {'✓' if db_manager else '✗'}")
    logger.info(f"  - Web3 Auth: {'✓' if web3_auth else '✗'}")
    logger.info(f"  - Persona System: {'✓' if agentic_processor else '✗'}")
    logger.info("Web interface available at: http://localhost:8000")
    logger.info("Health check at: http://localhost:8000/health")
    
    app.run(
        host='localhost',
        port=8000,
        debug=False,
        threaded=True
    )
