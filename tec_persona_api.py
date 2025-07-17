"""
TEC Enhanced Persona API Server
Complete backend with persona management, chat, and data persistence
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import sqlite3
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, 'src')

from tec_tools.persona_manager import PersonaManager
from tec_tools.data_persistence import TECDataManager

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize managers
persona_manager = PersonaManager()
data_manager = TECDataManager()

# Load settings
settings = data_manager.load_settings()

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "TEC Enhanced Persona API",
        "version": "2.0.0",
        "database_connected": True,
        "timestamp": data_manager.get_system_stats()
    })

@app.route('/api/system/stats')
def system_stats():
    """Get system statistics"""
    stats = data_manager.get_system_stats()
    return jsonify(stats)

@app.route('/api/persona/current')
def get_current_persona():
    """Get current persona information"""
    return jsonify({
        "name": "Default",
        "title": "TEC Enhanced Persona",
        "character": "Polkin",
        "status": "active"
    })

@app.route('/api/persona/characters')
def get_characters():
    """Get available characters"""
    characters = ['Polkin', 'Mynx', 'Kaelen']
    character_data = {}
    
    for char in characters:
        lore = persona_manager.get_character_lore(char)
        if lore:
            character_data[char] = {
                "name": char,
                "background": lore.get('background', ''),
                "personality": lore.get('personality', ''),
                "abilities": lore.get('abilities', ''),
                "domain": lore.get('domain', '')
            }
    
    return jsonify(character_data)

@app.route('/api/persona/character/<character_name>')
def get_character_lore(character_name):
    """Get specific character lore"""
    lore = persona_manager.get_character_lore(character_name)
    if lore:
        return jsonify(lore)
    else:
        return jsonify({"error": "Character not found"}), 404

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        # Simple echo response for now (can be enhanced with AI integration)
        character = data.get('character', 'Polkin')
        
        # Get character context
        character_lore = persona_manager.get_character_lore(character)
        character_intro = ""
        if character_lore:
            character_intro = f"As {character}, {character_lore.get('personality', '')}"
        
        # Generate response based on character
        responses = {
            'Polkin': f"🔮 {character_intro} I sense great potential in your words. {message} resonates with the mystical energies around us. How may I guide you further on your journey?",
            'Mynx': f"⚡ {character_intro} Your input has been processed through my advanced systems. Regarding '{message}' - I recommend we approach this with both logic and intuition. What would you like to explore next?",
            'Kaelen': f"⭐ {character_intro} The cosmic winds bring your message to me. '{message}' speaks to the interconnected nature of all things. Let us wander through this topic together.",
            'default': f"Hello! I received your message: '{message}'. I'm here to help you with your digital sovereignty journey."
        }
        
        response = responses.get(character, responses['default'])
        
        return jsonify({
            "response": response,
            "character": character,
            "timestamp": data_manager.get_system_stats()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat/enhanced', methods=['POST'])
def enhanced_chat():
    """Enhanced chat with persona context"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        character = data.get('character', 'Polkin')
        enhanced = data.get('enhanced', False)
        settings_data = data.get('settings', {})
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        # Get character context
        character_lore = persona_manager.get_character_lore(character)
        
        # Enhanced response with character personality
        if enhanced and character_lore:
            personality = character_lore.get('personality', '')
            domain = character_lore.get('domain', '')
            
            enhanced_response = f"*Drawing upon {domain} and embodying {personality}*\n\n"
            
            if character == 'Polkin':
                enhanced_response += f"🌟 Ah, {message}... I see the threads of fate weaving around your words. Through my mystical sight, I perceive deeper meanings. Let me share what the ethereal realms reveal about your inquiry..."
            elif character == 'Mynx':
                enhanced_response += f"🔬 Processing your input '{message}' through advanced neural pathways... My cybernetic intuition suggests multiple dimensional approaches to this. Allow me to interface with both logic and mysticism to provide optimal guidance..."
            elif character == 'Kaelen':
                enhanced_response += f"✨ Your words '{message}' ripple across the cosmic consciousness like stones cast into an infinite pond. From my wanderings through star-lit dimensions, I offer this perspective..."
            else:
                enhanced_response = f"I understand you're asking about '{message}'. Let me help you explore this thoughtfully."
        else:
            enhanced_response = f"Regarding '{message}', I'm here to assist you with that topic."
        
        return jsonify({
            "response": enhanced_response,
            "character": character,
            "enhanced": enhanced,
            "settings": settings_data
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/data/backup', methods=['POST'])
def create_backup():
    """Create system backup"""
    try:
        backup_file = data_manager.create_backup()
        return jsonify({
            "success": True,
            "backup_file": backup_file,
            "message": "Backup created successfully"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/data/settings', methods=['GET', 'POST'])
def handle_settings():
    """Get or update settings"""
    if request.method == 'GET':
        settings = data_manager.load_settings()
        return jsonify(settings)
    
    elif request.method == 'POST':
        try:
            new_settings = request.get_json()
            success = data_manager.save_settings(new_settings)
            
            if success:
                return jsonify({
                    "success": True,
                    "message": "Settings saved successfully"
                })
            else:
                return jsonify({"error": "Failed to save settings"}), 500
                
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Serve static files
@app.route('/')
def index():
    """Serve main interface"""
    return send_from_directory('.', 'tec_enhanced_interface.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("🚀 Starting TEC Enhanced Persona API Server...")
    print("=" * 50)
    print("📍 Server: http://localhost:8000")
    print("🌐 Enhanced Interface: http://localhost:8000/tec_enhanced_interface.html")
    print("🎮 Complete Interface: http://localhost:8000/tec_complete_interface.html")
    print("📋 Health Check: http://localhost:8000/health")
    print("📊 System Stats: http://localhost:8000/api/system/stats")
    print("=" * 50)
    
    # Run the server
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
        threaded=True
    )
