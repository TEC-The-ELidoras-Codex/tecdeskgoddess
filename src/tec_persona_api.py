#!/usr/bin/env python3
"""
TEC: BITLyfe Player Persona API Endpoints
Enhanced API with persona and moment settings management
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

# Initialize managers
try:
    from tec_tools.database_manager import DatabaseManager
    from tec_tools.persona_manager import PersonaManager
    from tec_tools.web3_auth import Web3AuthManager
    from tec_tools.agentic_processor import AgenticProcessor
    
    db_manager = DatabaseManager()
    persona_manager = PersonaManager()
    web3_auth = Web3AuthManager(config)
    agentic_processor = AgenticProcessor(config)
    
    logger.info("All managers initialized successfully")
except Exception as e:
    logger.error(f"Manager initialization failed: {e}")
    db_manager = None
    persona_manager = None
    web3_auth = None
    agentic_processor = None

# Authentication decorator
def require_auth(f):
    """Decorator to require authentication"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not web3_auth:
            return jsonify({'error': 'Authentication system not available'}), 503
        
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No authentication token provided'}), 401
        
        try:
            token = auth_header.split(' ')[1]
            payload = web3_auth.verify_jwt_token(token)
            if not payload:
                return jsonify({'error': 'Invalid token'}), 401
            
            # Store user info in request context
            request.user_id = payload['user_id']
            request.access_tier = payload.get('access_tier', 'free')
            
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return jsonify({'error': 'Authentication failed'}), 401
    
    return decorated_function

# Health check endpoint
@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'service': 'TEC Persona API',
        'version': '2.1.0',
        'features': {
            'database': db_manager is not None,
            'persona_manager': persona_manager is not None,
            'web3_auth': web3_auth is not None,
            'agentic_processor': agentic_processor is not None
        }
    })

# Player Persona Endpoints
@app.route('/api/persona/player', methods=['POST'])
@require_auth
def save_player_persona():
    """Save or update player persona"""
    try:
        if not persona_manager:
            return jsonify({'error': 'Persona manager not available'}), 503
        
        persona_data = request.get_json()
        if not persona_data:
            return jsonify({'error': 'No persona data provided'}), 400
        
        success = persona_manager.save_player_persona(request.user_id, persona_data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Player persona saved successfully'
            })
        else:
            return jsonify({'error': 'Failed to save persona'}), 500
            
    except Exception as e:
        logger.error(f"Error saving player persona: {e}")
        return jsonify({'error': 'Failed to save persona'}), 500

@app.route('/api/persona/player', methods=['GET'])
@require_auth
def get_player_persona():
    """Get current player persona"""
    try:
        if not persona_manager:
            return jsonify({'error': 'Persona manager not available'}), 503
        
        persona = persona_manager.get_player_persona(request.user_id)
        
        if persona:
            return jsonify(persona)
        else:
            return jsonify({'message': 'No persona found'}), 404
            
    except Exception as e:
        logger.error(f"Error retrieving player persona: {e}")
        return jsonify({'error': 'Failed to retrieve persona'}), 500

@app.route('/api/persona/public', methods=['GET'])
def get_public_personas():
    """Get public player personas for community features"""
    try:
        if not persona_manager:
            return jsonify({'error': 'Persona manager not available'}), 503
        
        limit = request.args.get('limit', 50, type=int)
        personas = persona_manager.get_public_personas(limit)
        
        return jsonify({
            'personas': personas,
            'count': len(personas)
        })
        
    except Exception as e:
        logger.error(f"Error retrieving public personas: {e}")
        return jsonify({'error': 'Failed to retrieve public personas'}), 500

# AI Settings Endpoints
@app.route('/api/ai/settings', methods=['POST'])
@require_auth
def save_ai_settings():
    """Save AI interaction settings"""
    try:
        if not persona_manager:
            return jsonify({'error': 'Persona manager not available'}), 503
        
        settings = request.get_json()
        if not settings:
            return jsonify({'error': 'No settings provided'}), 400
        
        success = persona_manager.save_ai_settings(request.user_id, settings)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'AI settings saved successfully'
            })
        else:
            return jsonify({'error': 'Failed to save settings'}), 500
            
    except Exception as e:
        logger.error(f"Error saving AI settings: {e}")
        return jsonify({'error': 'Failed to save settings'}), 500

@app.route('/api/ai/settings', methods=['GET'])
@require_auth
def get_ai_settings():
    """Get AI interaction settings"""
    try:
        if not persona_manager:
            return jsonify({'error': 'Persona manager not available'}), 503
        
        settings = persona_manager.get_ai_settings(request.user_id)
        return jsonify(settings)
        
    except Exception as e:
        logger.error(f"Error retrieving AI settings: {e}")
        return jsonify({'error': 'Failed to retrieve settings'}), 500

# Character Lore Endpoints
@app.route('/api/lore/character/<character_name>', methods=['GET'])
@require_auth
def get_character_lore(character_name):
    """Get character lore data"""
    try:
        if not persona_manager:
            return jsonify({'error': 'Persona manager not available'}), 503
        
        character_data = persona_manager.get_character_lore(character_name)
        
        if character_data:
            return jsonify(character_data)
        else:
            return jsonify({'message': f'No lore found for character: {character_name}'}), 404
            
    except Exception as e:
        logger.error(f"Error retrieving character lore: {e}")
        return jsonify({'error': 'Failed to retrieve character lore'}), 500

@app.route('/api/lore/character/<character_name>', methods=['POST'])
@require_auth
def save_character_lore(character_name):
    """Save character lore data (admin only)"""
    try:
        if not persona_manager:
            return jsonify({'error': 'Persona manager not available'}), 503
        
        # TODO: Add admin role check
        if request.access_tier != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        character_data = request.get_json()
        if not character_data:
            return jsonify({'error': 'No character data provided'}), 400
        
        success = persona_manager.save_character_lore(character_name, character_data)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Character lore saved for: {character_name}'
            })
        else:
            return jsonify({'error': 'Failed to save character lore'}), 500
            
    except Exception as e:
        logger.error(f"Error saving character lore: {e}")
        return jsonify({'error': 'Failed to save character lore'}), 500

# Enhanced Chat Endpoint with Persona Integration
@app.route('/api/chat/enhanced', methods=['POST'])
@require_auth
def enhanced_chat():
    """Enhanced chat with persona integration and AI settings"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        conversation_id = data.get('conversation_id', f"conv_{request.user_id}_{datetime.now().timestamp()}")
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get user's AI settings
        ai_settings = persona_manager.get_ai_settings(request.user_id) if persona_manager else {}
        
        # Get user's player persona
        player_persona = persona_manager.get_player_persona(request.user_id) if persona_manager else None
        
        # Get conversation history for context
        conversation_history = persona_manager.get_conversation_history(
            request.user_id, conversation_id, 
            limit=20 if ai_settings.get('memory_length') == 'short' else 100
        ) if persona_manager else []
        
        # Save user message to memory
        if persona_manager:
            persona_manager.save_conversation_memory(
                request.user_id, conversation_id, 'user', message
            )
        
        # Generate AI response with enhanced context
        if agentic_processor:
            try:
                import asyncio
                
                # Create enhanced context for AI
                enhanced_context = {
                    'user_id': request.user_id,
                    'access_tier': request.access_tier,
                    'ai_settings': ai_settings,
                    'player_persona': player_persona,
                    'conversation_history': conversation_history,
                    'conversation_id': conversation_id
                }
                
                response = asyncio.run(
                    agentic_processor.process_enhanced_message(message, enhanced_context)
                )
                
                current_persona = ai_settings.get('persona_active', 'airth')
                
                # Save AI response to memory
                if persona_manager:
                    persona_manager.save_conversation_memory(
                        request.user_id, conversation_id, 'ai', response, current_persona
                    )
                
                return jsonify({
                    'response': response,
                    'persona': current_persona,
                    'conversation_id': conversation_id,
                    'ai_settings': ai_settings,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Enhanced chat processing error: {e}")
                return jsonify({'error': 'Failed to process enhanced message'}), 500
        else:
            # Fallback response
            return jsonify({
                'response': f"Enhanced TEC system received: '{message}'. Full AI processing will be available once the agentic processor is initialized.",
                'persona': ai_settings.get('persona_active', 'airth'),
                'conversation_id': conversation_id,
                'timestamp': datetime.now().isoformat()
            })
            
    except Exception as e:
        logger.error(f"Enhanced chat error: {e}")
        return jsonify({'error': 'Failed to process enhanced chat'}), 500

# Prompt Generation Endpoints
@app.route('/api/prompt/image', methods=['POST'])
@require_auth
def generate_image_prompt():
    """Generate image prompts using character lore and player persona"""
    try:
        data = request.get_json()
        character_name = data.get('character_name', '')
        setting = data.get('setting', '')
        style = data.get('style', 'cyberpunk')
        description = data.get('description', '')
        
        if not character_name:
            return jsonify({'error': 'Character name required'}), 400
        
        # Get character lore
        character_data = persona_manager.get_character_lore(character_name) if persona_manager else None
        
        # Get player persona for context
        player_persona = persona_manager.get_player_persona(request.user_id) if persona_manager else None
        
        # Generate image prompt using AI
        if agentic_processor:
            try:
                import asyncio
                
                prompt_context = {
                    'character_data': character_data,
                    'player_persona': player_persona,
                    'setting': setting,
                    'style': style,
                    'description': description
                }
                
                image_prompt = asyncio.run(
                    agentic_processor.generate_image_prompt(prompt_context)
                )
                
                return jsonify({
                    'image_prompt': image_prompt,
                    'character_name': character_name,
                    'setting': setting,
                    'style': style,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Image prompt generation error: {e}")
                return jsonify({'error': 'Failed to generate image prompt'}), 500
        else:
            return jsonify({'error': 'AI processor not available'}), 503
            
    except Exception as e:
        logger.error(f"Image prompt error: {e}")
        return jsonify({'error': 'Failed to generate image prompt'}), 500

@app.route('/api/prompt/story', methods=['POST'])
@require_auth
def generate_story_prompt():
    """Generate story prompts using character lore and player persona"""
    try:
        data = request.get_json()
        characters = data.get('characters', [])
        setting = data.get('setting', '')
        theme = data.get('theme', '')
        length = data.get('length', 'short')
        
        if not characters:
            return jsonify({'error': 'At least one character required'}), 400
        
        # Get character lore for all characters
        character_data = {}
        if persona_manager:
            for char in characters:
                char_data = persona_manager.get_character_lore(char)
                if char_data:
                    character_data[char] = char_data
        
        # Get player persona for context
        player_persona = persona_manager.get_player_persona(request.user_id) if persona_manager else None
        
        # Generate story prompt using AI
        if agentic_processor:
            try:
                import asyncio
                
                prompt_context = {
                    'character_data': character_data,
                    'player_persona': player_persona,
                    'setting': setting,
                    'theme': theme,
                    'length': length
                }
                
                story_prompt = asyncio.run(
                    agentic_processor.generate_story_prompt(prompt_context)
                )
                
                return jsonify({
                    'story_prompt': story_prompt,
                    'characters': characters,
                    'setting': setting,
                    'theme': theme,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Story prompt generation error: {e}")
                return jsonify({'error': 'Failed to generate story prompt'}), 500
        else:
            return jsonify({'error': 'AI processor not available'}), 503
            
    except Exception as e:
        logger.error(f"Story prompt error: {e}")
        return jsonify({'error': 'Failed to generate story prompt'}), 500

# Legacy endpoints for backward compatibility
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
            
            # Initialize default AI settings
            if persona_manager:
                persona_manager.save_ai_settings(user_id, {
                    'creativity_level': 0.7,
                    'memory_length': 'default',
                    'reasoning_mode': False,
                    'persona_active': 'airth',
                    'voice_enabled': False
                })
            
            return jsonify({
                'success': True,
                'token': auth_result['token'],
                'user_data': user_record,
                'access_tier': auth_result['user_data'].get('access_tier', 'free')
            })
        else:
            return jsonify(auth_result), 401
            
    except Exception as e:
        logger.error(f"Signature verification error: {e}")
        return jsonify({'error': 'Authentication failed'}), 500

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
    logger.info("Starting TEC Enhanced Persona API Server...")
    logger.info("Features:")
    logger.info(f"  - Database: {'✓' if db_manager else '✗'}")
    logger.info(f"  - Persona Manager: {'✓' if persona_manager else '✗'}")
    logger.info(f"  - Web3 Auth: {'✓' if web3_auth else '✗'}")
    logger.info(f"  - Agentic Processor: {'✓' if agentic_processor else '✗'}")
    logger.info("Web interface available at: http://localhost:8000")
    logger.info("Health check at: http://localhost:8000/health")
    
    app.run(
        host='localhost',
        port=8000,
        debug=False,
        threaded=True
    )

def create_persona_app():
    """Create and configure the persona Flask app for testing"""
    return app
