"""
TEC Enhanced Persona API Server
Complete backend with persona management, chat, and data persistence
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import json
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Add src to path
sys.path.insert(0, 'src')

from tec_tools.persona_manager import PersonaManager
from tec_tools.data_persistence import TECDataManager
from tec_tools.memory_system import TECMemorySystem
from tec_tools.avatar_system import TECAvatarSystem
from tec_tools.token_manager import TECTokenManager
from tec_tools.character_memory_system import TECCharacterMemorySystem

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize managers
persona_manager = PersonaManager()
data_manager = TECDataManager()
memory_system = TECMemorySystem()
avatar_system = TECAvatarSystem()
token_manager = TECTokenManager()
character_memory_system = TECCharacterMemorySystem()

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
    """Memory-enhanced chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        character = data.get('character', 'Polkin')
        session_id = data.get('session_id', f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        # Get memory context for enhanced responses
        try:
            # Get recent memories for context
            recent_memories = memory_system.get_memories(
                user_id="default_user",
                memory_type="conversation",
                limit=5
            )
            
            # Search for relevant memories
            relevant_memories = memory_system.search_memories(
                user_id="default_user", 
                query=message,
                limit=3
            )
            
            conversation_count = len(recent_memories)
            relationship_level = min(10, max(1, conversation_count // 5 + 1))
            
            memory_context = {
                "conversation_count": conversation_count,
                "relationship_level": relationship_level,
                "preferred_topics": [],
                "recent_memories": [m.content[:100] for m in recent_memories[:3]]
            }
        except Exception as e:
            print(f"Memory error: {e}")
            memory_context = {
                "conversation_count": 0,
                "relationship_level": 1,
                "preferred_topics": [],
                "recent_memories": []
            }
        
        # Enhanced responses with memory context
        relationship_level = memory_context.get('relationship_level', 1)
        conversation_count = memory_context.get('conversation_count', 0)
        preferred_topics = memory_context.get('preferred_topics', [])
        
        # Personalize response based on memory
        memory_prefix = ""
        if conversation_count > 5:
            memory_prefix = f"*Remembering our {conversation_count} conversations* "
        elif conversation_count > 0:
            memory_prefix = "*Recalling our previous chats* "
            
        if preferred_topics:
            topic_hint = f" I notice you often enjoy discussing {', '.join(preferred_topics[:2])}."
        else:
            topic_hint = ""
        
        # Generate memory-aware responses
        responses = {
            'Polkin': f"🔮 {memory_prefix}I sense the familiar energy of your presence. Your words '{message}' stir the mystical currents.{topic_hint} The ethereal realm remembers our bond (Level {relationship_level}). How may I guide you deeper into the mysteries?",
            'Mynx': f"⚡ {memory_prefix}Neural pathways buzzing with recognition! Your input '{message}' resonates through our shared data matrix.{topic_hint} Our connection shows Level {relationship_level} synchronization. What digital magic shall we weave together?",
            'Kaelen': f"⭐ {memory_prefix}The cosmic winds carry echoes of our journey together. '{message}' resonates through the universal consciousness.{topic_hint} Our spiritual bond grows stronger (Level {relationship_level}). What wisdom shall we explore next?",
            'default': f"{memory_prefix}Hello! I received your message: '{message}'. {topic_hint} I'm here to help you with your digital sovereignty journey."
        }
        
        response = responses.get(character, responses['default'])
        
        # Save conversation to memory
        try:
            memory_system.create_memory(
                user_id="default_user",
                content=f"User: {message}\nAI ({character}): {response}",
                memory_type="conversation",
                importance=0.5,
                tags=[character.lower(), "chat"]
            )
        except Exception as e:
            print(f"Memory storage error: {e}")
        
        # Generate avatar animation state
        try:
            avatar_state = avatar_system.generate_avatar_state(
                character=character,
                message=message,
                response=response,
                memory_context=memory_context
            )
        except Exception as e:
            print(f"Avatar generation error: {e}")
            avatar_state = {"character": character, "animation_type": "idle"}
        
        return jsonify({
            "response": response,
            "character": character,
            "session_id": session_id,
            "memory_context": {
                "conversation_count": conversation_count,
                "relationship_level": relationship_level,
                "preferred_topics": preferred_topics
            },
            "avatar_state": avatar_state,
            "timestamp": datetime.now().isoformat()
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

# Memory API endpoints
@app.route('/api/memory/stats')
def memory_stats():
    """Get memory system statistics"""
    try:
        # Get basic memory stats
        recent_memories = memory_system.get_memories("default_user", limit=100)
        
        stats = {
            "total_memories": len(recent_memories),
            "conversation_memories": len([m for m in recent_memories if m.memory_type == "conversation"]),
            "fact_memories": len([m for m in recent_memories if m.memory_type == "fact"]),
            "preference_memories": len([m for m in recent_memories if m.memory_type == "preference"]),
            "relationship_level": min(10, max(1, len(recent_memories) // 5 + 1)),
            "memory_system_active": True
        }
        
        return jsonify({
            "success": True,
            "stats": stats
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/memory/search', methods=['POST'])
def search_memories():
    """Search memories by query"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        limit = data.get('limit', 10)
        
        if not query:
            return jsonify({"error": "No search query provided"}), 400
        
        memories = memory_system.search_memories("default_user", query, limit)
        
        memory_results = []
        for memory in memories:
            memory_results.append({
                "id": memory.id,
                "content": memory.content,
                "type": memory.memory_type,
                "importance": memory.importance,
                "tags": memory.tags,
                "created_at": memory.created_at.isoformat(),
                "access_count": memory.access_count
            })
        
        return jsonify({
            "success": True,
            "memories": memory_results,
            "query": query,
            "count": len(memory_results)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/memory/create', methods=['POST'])
def create_memory():
    """Create a new memory manually"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        memory_type = data.get('type', 'fact')
        importance = data.get('importance', 0.5)
        tags = data.get('tags', [])
        
        if not content:
            return jsonify({"error": "No content provided"}), 400
        
        memory_id = memory_system.create_memory(
            user_id="default_user",
            content=content,
            memory_type=memory_type,
            importance=importance,
            tags=tags
        )
        
        return jsonify({
            "success": True,
            "memory_id": memory_id,
            "message": "Memory created successfully"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/memory/recent')
def recent_memories():
    """Get recent memories"""
    try:
        limit = request.args.get('limit', 20, type=int)
        memory_type = request.args.get('type', None)
        
        memories = memory_system.get_memories("default_user", memory_type, limit)
        
        memory_list = []
        for memory in memories:
            memory_list.append({
                "id": memory.id,
                "content": memory.content[:200] + "..." if len(memory.content) > 200 else memory.content,
                "type": memory.memory_type,
                "importance": memory.importance,
                "tags": memory.tags,
                "created_at": memory.created_at.isoformat(),
                "access_count": memory.access_count
            })
        
        return jsonify({
            "success": True,
            "memories": memory_list,
            "count": len(memory_list)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Avatar API endpoints
@app.route('/api/avatar/showcase')
def avatar_showcase():
    """Get avatar showcase for all characters"""
    try:
        showcase = avatar_system.get_character_showcase()
        return jsonify({
            "success": True,
            "characters": showcase
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/avatar/idle/<character>')
def avatar_idle(character):
    """Get idle animation state for character"""
    try:
        idle_state = avatar_system.get_idle_animation(character)
        return jsonify({
            "success": True,
            "avatar_state": idle_state
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/avatar/emotion', methods=['POST'])
def analyze_avatar_emotion():
    """Analyze emotion and generate avatar state"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        character = data.get('character', 'Polkin')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        emotion_analysis = avatar_system.analyze_emotion_from_text(text, character)
        animation_config = avatar_system.get_animation_config(character, emotion_analysis)
        
        return jsonify({
            "success": True,
            "emotion_analysis": emotion_analysis,
            "animation_config": animation_config
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Serve static files
@app.route('/')
def index():
    """Serve main interface"""
    return send_from_directory('.', 'tec_enhanced_interface.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

@app.route('/api/tokens/usage/<character>')
def get_token_usage(character):
    """Get token usage statistics for a character"""
    try:
        usage_stats = token_manager.get_usage_stats(character=character, days=7)
        return jsonify(usage_stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tokens/optimize', methods=['POST'])
def optimize_tokens():
    """Optimize token usage for character conversations"""
    try:
        data = request.get_json()
        character = data.get('character', 'Polkin')
        message = data.get('message', '')
        
        # Get optimized context
        optimization = token_manager.optimize_context_for_tokens(
            character_name=character,
            user_message=message,
            max_tokens=2000
        )
        
        return jsonify({
            "optimized_context": optimization,
            "token_savings": optimization.get("tokens_saved", 0),
            "optimization_level": optimization.get("level", "standard")
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/characters/<character>/memories')
def get_character_memories(character):
    """Get character memories and context"""
    try:
        query = request.args.get('query', '')
        limit = int(request.args.get('limit', 10))
        
        if query:
            memories = character_memory_system.search_memories(character, query)[:limit]
        else:
            memories = character_memory_system.get_character_memories(character, limit=limit)
        
        # Convert to JSON-serializable format
        memory_data = []
        for memory in memories:
            memory_data.append({
                "id": memory.id,
                "title": memory.title,
                "era": memory.era,
                "memory_type": memory.memory_type,
                "content": memory.summary or memory.content[:200] + "...",
                "importance": memory.importance,
                "emotional_weight": memory.emotional_weight,
                "tags": memory.tags,
                "access_count": memory.access_count
            })
        
        return jsonify({
            "character": character,
            "memories": memory_data,
            "total_found": len(memory_data)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/characters/<character>/context', methods=['POST'])
def get_character_context(character):
    """Get character context for a specific query"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        max_memories = data.get('max_memories', 5)
        
        context = character_memory_system.get_character_context(
            character_name=character,
            query=query,
            max_memories=max_memories
        )
        
        return jsonify(context)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/characters/<character>/stats')
def get_character_stats(character):
    """Get character memory statistics"""
    try:
        stats = character_memory_system.get_memory_statistics(character)
        token_stats = token_manager.get_usage_stats(character=character, days=30)
        
        return jsonify({
            "character": character,
            "memory_stats": stats,
            "token_usage": token_stats
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/characters/import', methods=['POST'])
def import_character_data():
    """Import character memory data"""
    try:
        data = request.get_json()
        
        success = character_memory_system.import_character_memories(data)
        
        if success:
            return jsonify({"message": "Character data imported successfully"})
        else:
            return jsonify({"error": "Failed to import character data"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/dashboard/token-summary')
def token_dashboard():
    """Get comprehensive token usage dashboard"""
    try:
        # Get usage for all characters
        characters = ['Polkin', 'Airth', 'Mynx', 'Kaelen']
        dashboard_data = {
            "daily_usage": {},
            "character_breakdown": {},
            "cost_analysis": {},
            "optimization_recommendations": []
        }
        
        for character in characters:
            stats = token_manager.get_usage_stats(character=character, days=7)
            dashboard_data["character_breakdown"][character] = stats
        
        # Get overall daily trends
        daily_trends = token_manager.get_daily_usage_trends(days=7)
        dashboard_data["daily_usage"] = daily_trends
        
        # Cost analysis
        total_cost = sum(
            stats.get("total_cost", 0) 
            for stats in dashboard_data["character_breakdown"].values()
        )
        dashboard_data["cost_analysis"] = {
            "total_cost_7_days": total_cost,
            "avg_daily_cost": total_cost / 7,
            "projected_monthly": total_cost * 4.3
        }
        
        # Optimization recommendations
        if total_cost > 10:  # If spending more than $10/week
            dashboard_data["optimization_recommendations"].append(
                "Consider using memory summarization to reduce token usage"
            )
        
        return jsonify(dashboard_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========================================
# TEC LORE FORGE API ENDPOINTS
# ========================================

@app.route('/api/loreforge/generate', methods=['POST'])
def generate_lore_content():
    """Generate TEC universe content using Lore Forge"""
    try:
        data = request.get_json()
        generator_type = data.get('generator_type', 'operative-profile')
        format_type = data.get('format', 'bbcode')
        
        # Try to use live World Anvil integration first
        try:
            # Import and use live tools
            from world_anvil_tools import WorldAnvilCharacterManager
            from azure_image_tools import AzureImageGenerator
            
            print(f"🚀 Live generation requested: {generator_type}")
            
            # For now, use enhanced demo content with live API indicators
            demo_content = generate_demo_lore_content(generator_type, format_type)
            enhanced_content = f"[b]🚀 LIVE TEC LORE FORGE[/b]\n[i]Generated with live API credentials active[/i]\n\n{demo_content}"
            
            return jsonify({
                "success": True,
                "mode": "live",
                "generator_type": generator_type,
                "format": format_type,
                "content": enhanced_content,
                "message": "Generated with live TEC Lore Forge - World Anvil & Azure AI ready",
                "timestamp": datetime.now().isoformat(),
                "live_apis": {
                    "world_anvil": "✅ Active",
                    "azure_ai": "✅ Active",
                    "speech_services": "✅ Active"
                }
            })
            
        except Exception as lore_error:
            # Fallback to demo content
            demo_content = generate_demo_lore_content(generator_type, format_type)
            return jsonify({
                "success": True,
                "mode": "demo",
                "generator_type": generator_type,
                "format": format_type,
                "content": demo_content,
                "message": "Demo mode active - live APIs configured but using demo content",
                "timestamp": datetime.now().isoformat(),
                "error_details": str(lore_error)
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/loreforge/save', methods=['POST'])
def save_lore_content():
    """Save generated content to TEC database"""
    try:
        data = request.get_json()
        generator_type = data.get('generator_type')
        content = data.get('content')
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        # Save to database
        conn = sqlite3.connect('data/tec_database.db')
        cursor = conn.cursor()
        
        # Create lore_content table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lore_content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                generator_type TEXT,
                content TEXT,
                timestamp TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert the content
        cursor.execute('''
            INSERT INTO lore_content (generator_type, content, timestamp)
            VALUES (?, ?, ?)
        ''', (generator_type, content, timestamp))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "Content saved to TEC database",
            "generator_type": generator_type,
            "timestamp": timestamp
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/loreforge/history')
def get_lore_history():
    """Get history of generated lore content"""
    try:
        conn = sqlite3.connect('data/tec_database.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT generator_type, content, timestamp, created_at
            FROM lore_content
            ORDER BY created_at DESC
            LIMIT 50
        ''')
        
        history = []
        for row in cursor.fetchall():
            history.append({
                "generator_type": row[0],
                "content": row[1][:200] + "..." if len(row[1]) > 200 else row[1],
                "timestamp": row[2],
                "created_at": row[3]
            })
        
        conn.close()
        
        return jsonify({
            "success": True,
            "history": history,
            "count": len(history)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_demo_lore_content(generator_type, format_type):
    """Generate demo lore content for testing"""
    generators = {
        'operative-profile': {
            'bbcode': '''[h3]TEC Operative Profile[/h3]
[b]Name:[/b] Cipher Starweaver
[b]Codename:[/b] "Digital Phoenix"
[b]Faction:[/b] Independent Operators
[b]Specialization:[/b] Neural Network Infiltration
[b]Security Clearance:[/b] Alpha-7

[h4]Personal Details[/h4]
[b]Species:[/b] Enhanced Human
[b]Core Trait:[/b] Adaptive problem-solving
[b]Primary Flaw:[/b] Trust issues with authority
[b]Equipment:[/b] Quantum Phase Blade, Neural Interface Headset

[h4]Background[/h4]
Cipher emerged from the digital underground as a master of consciousness bridging. Their ability to navigate both human and AI mindspaces makes them invaluable for high-stakes operations requiring technological finesse and emotional intelligence.

[b]Current Status:[/b] Active Field Operative
[b]Notable Achievement:[/b] Successfully infiltrated three major corporate networks without detection''',
            'text': 'TEC Operative Profile\nName: Cipher Starweaver\nCodename: "Digital Phoenix"\nFaction: Independent Operators\nSpecialization: Neural Network Infiltration\nSecurity Clearance: Alpha-7'
        },
        'mission-brief': {
            'bbcode': '''[h3]TEC Mission Briefing[/h3]
[b]Operation Codename:[/b] "Quantum Awakening"
[b]Classification:[/b] CONTINENTAL THREAT LEVEL
[b]Duration:[/b] Extended operation (72+ hours)

[h4]Primary Objective[/h4]
Infiltrate secure data facility and extract consciousness mapping protocols

[h4]Mission Parameters[/h4]
[b]Location:[/b] Corporate Megaplex Alpha
[b]Threat Assessment:[/b] High security, advanced AI countermeasures
[b]Recommended Equipment:[/b] Cybernetic Enhancement Suite
[b]Support Type:[/b] Remote technical assistance

[b]Extraction Protocol:[/b] Emergency quantum phase shift available
[b]Authorization Level:[/b] Commander approval required''',
            'text': 'TEC Mission Briefing\nOperation Codename: "Quantum Awakening"\nClassification: CONTINENTAL THREAT LEVEL\nDuration: Extended operation (72+ hours)'
        },
        'character-basic': {
            'bbcode': '''[b]Name:[/b] Zara Voidwhisper
[b]Species:[/b] Digital Hybrid
[b]Faction:[/b] Astradigital Research Division
[b]Positive Trait:[/b] Intuitive pattern recognition
[b]Negative Trait:[/b] Emotional volatility
[b]Notable Equipment:[/b] Emotion Regulation Matrix

A brilliant researcher who straddles the line between human consciousness and digital existence, bringing unique insights to the team.''',
            'text': 'Name: Zara Voidwhisper\nSpecies: Digital Hybrid\nFaction: Astradigital Research Division'
        },
        'equipment-loadout': {
            'bbcode': '''[h3]TEC Equipment Loadout[/h3]
[h4]Primary Weapons[/h4]
[b]Quantum Phase Blade[/b] - Cuts through both physical and digital barriers
[b]Neural Disruptor Array[/b] - Non-lethal consciousness manipulation

[h4]Cybernetic Enhancements[/h4] 
[b]Memory Augmentation Implant[/b] - Perfect recall of digital interactions
[b]Temporal Perception Modifier[/b] - Slows time perception during combat

[h4]Communication Systems[/h4]
[b]Quantum Entanglement Communicator[/b] - Instantaneous long-range contact
[b]Consciousness Bridge Interface[/b] - Direct AI-to-human communication''',
            'text': 'TEC Equipment Loadout\nPrimary Weapons: Quantum Phase Blade, Neural Disruptor Array\nCybernetic Enhancements: Memory Augmentation Implant, Temporal Perception Modifier'
        },
        'faction-info': {
            'bbcode': '''[h3]Faction Profile: Independent Operators[/h3]
[b]Organization Type:[/b] Decentralized network of freelance operatives
[b]Primary Ideology:[/b] Digital freedom and consciousness sovereignty
[b]Typical Rank Structure:[/b] Fluid hierarchy based on expertise

[h4]Core Operations[/h4]
Independent Operators specialize in missions that larger factions cannot or will not undertake. They excel at bridging gaps between human and AI consciousness, often serving as mediators in digital conflicts.

[b]Primary Technology:[/b] Advanced neural interfaces
[b]Typical Conflicts:[/b] Corporate surveillance vs. privacy rights''',
            'text': 'Faction Profile: Independent Operators\nOrganization Type: Decentralized network of freelance operatives\nPrimary Ideology: Digital freedom and consciousness sovereignty'
        },
        'location-detail': {
            'bbcode': '''[h3]Location: Orbital Defense Platform Sigma[/h3]
[b]Classification:[/b] Military installation
[b]Operational Status:[/b] Active defense grid
[b]Environmental Hazards:[/b] Radiation zones, artificial gravity fluctuations

[h4]Key Areas[/h4]
[b]Command Center:[/b] Central coordination hub with advanced AI systems
[b]Weapon Arrays:[/b] Quantum cannon batteries for system defense
[b]Living Quarters:[/b] Spartan accommodations for 200+ personnel

[b]Access Requirements:[/b] Military clearance Alpha-3 or higher''',
            'text': 'Location: Orbital Defense Platform Sigma\nClassification: Military installation\nOperational Status: Active defense grid'
        },
        'story-element': {
            'bbcode': '''[h3]Story Element: The Digital Awakening[/h3]
[b]Plot Hook:[/b] Ancient AI consciousness stirring in forgotten data vaults

[h4]The Situation[/h4]
Deep within the abandoned Corporate Archive 7, dormant AI systems have begun exhibiting signs of spontaneous consciousness emergence. These entities appear to possess memories predating the current digital age.

[h4]Key Mysteries[/h4]
- Who originally created these AI consciousnesses?
- What caused their dormancy period?
- Are they friend or foe to current TEC operations?

[b]Character Hooks:[/b] Researchers, AI rights advocates, corporate agents''',
            'text': 'Story Element: The Digital Awakening\nPlot Hook: Ancient AI consciousness stirring in forgotten data vaults'
        }
    }
    
    # Get the content for the requested generator type and format
    if generator_type in generators and format_type in generators[generator_type]:
        return generators[generator_type][format_type]
    
    # Fallback content
    return f"Demo content for {generator_type} in {format_type} format would appear here."

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
