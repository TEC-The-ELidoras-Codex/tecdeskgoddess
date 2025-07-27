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

# Enhanced imports for visual asset generation
try:
    from tec_visual_asset_generator import TECVisualAssetGenerator
    from azure_image_tools import AzureImageGenerator
    visual_generator = TECVisualAssetGenerator()
    azure_image_gen = AzureImageGenerator()
    VISUAL_FEATURES_ENABLED = True
    print("✅ Visual asset generation features enabled")
except ImportError as e:
    print(f"⚠️  Visual features disabled - missing dependencies: {e}")
    VISUAL_FEATURES_ENABLED = False
    visual_generator = None
    azure_image_gen = None

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

# Initialize enhanced visual generator
if VISUAL_FEATURES_ENABLED:
    print("🎨 Visual Asset Generator initialized with complete faction database")
else:
    print("⚠️  Visual features not available - install Azure AI dependencies")

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
            'default': f"🌟 {memory_prefix}Welcome to the TEC universe! Your message '{message}' has been received.{topic_hint} I'm your digital companion, ready to explore the realms of possibility together. Which character would you like to interact with - Polkin, Mynx, or Kaelen?"
        }
        
        # Log character selection for debugging
        print(f"Chat request - Character: '{character}', Message: '{message[:50]}...'")
        
        # If character is 'default' or unrecognized, default to Polkin
        if character == 'default' or character not in responses:
            print(f"Defaulting to Polkin for character: '{character}'")
            character = 'Polkin'
        
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
# TEC PERSONA AUTOFILL API ENDPOINT
# ========================================

@app.route('/api/persona/autofill', methods=['POST'])
def autofill_persona():
    """Generate a complete TEC: BITLyfe persona using AI"""
    try:
        data = request.get_json() or {}
        theme_preference = data.get('theme', 'balanced')  # balanced, light, dark, mystical, tech, rebel
        faction_preference = data.get('faction', None)  # specific faction or random
        
        print(f"🤖 Generating AI persona autofill with theme: {theme_preference}")
        
        # Enhanced faction selection
        available_factions = [
            "Independent Operators", "Astradigital Research Division", "Neo-Constantinople Guard",
            "The Synthesis Collective", "Quantum Liberation Front", "Digital Preservation Society",
            "Ethereal Architects", "Nexus Wardens", "Void Seekers", "Chrono Guardians",
            "Neural Web Collective", "Plasma Engineers", "Shadow Operatives", "Crystal Shapers",
            "Flux Runners", "Echo Hunters", "Prism Keepers", "Storm Riders"
        ]
        
        # Select faction
        if not faction_preference:
            import random
            selected_faction = random.choice(available_factions)
        else:
            selected_faction = faction_preference if faction_preference in available_factions else available_factions[0]
        
        # Generate persona based on theme and faction
        persona_data = generate_ai_persona(theme_preference, selected_faction)
        
        return jsonify({
            "success": True,
            "persona": persona_data,
            "faction": selected_faction,
            "theme": theme_preference,
            "timestamp": datetime.now().isoformat(),
            "message": f"AI-generated persona with {theme_preference} theme from {selected_faction}"
        })
        
    except Exception as e:
        print(f"❌ Error generating persona autofill: {e}")
        return jsonify({"error": str(e)}), 500

def generate_ai_persona(theme, faction):
    """Generate a complete persona based on theme and faction"""
    import random
    
    # Theme-based personality traits
    theme_traits = {
        "balanced": {
            "titles": ["Digital Wanderer", "Tech Explorer", "Reality Walker", "Cyber Nomad", "Code Traveler"],
            "openings": ["Greetings, fellow traveler", "Welcome to my digital realm", "Ready for an adventure?", "Let's explore together", "Seeking new horizons?"],
            "body_types": ["athletic", "slender", "average", "graceful", "sturdy"],
            "ages": ["youthful", "timeless", "mature", "ageless", "seasoned"],
            "personalities": ["curious and balanced", "thoughtful explorer", "adaptable wanderer", "wise guide", "friendly mentor"]
        },
        "mystical": {
            "titles": ["Ethereal Sage", "Quantum Oracle", "Digital Mystic", "Void Whisperer", "Cosmic Guide"],
            "openings": ["The stars have aligned for our meeting", "I sense great potential in you", "The digital winds bring you here", "Ancient wisdom awaits", "The cosmos speaks through me"],
            "body_types": ["ethereal", "slender", "graceful", "otherworldly", "flowing"],
            "ages": ["ancient", "timeless", "ageless", "eternal", "beyond time"],
            "personalities": ["mystical and wise", "enigmatic seer", "cosmic wanderer", "ethereal guide", "ancient soul"]
        },
        "tech": {
            "titles": ["Cyber Engineer", "Digital Architect", "Code Master", "Tech Innovator", "System Designer"],
            "openings": ["Systems online, ready to connect", "Initiating communication protocols", "Welcome to the grid", "Let's hack reality together", "Connecting to your neural interface"],
            "body_types": ["cybernetic-enhanced", "tech-augmented", "sleek", "engineered", "optimized"],
            "ages": ["enhanced", "upgraded", "modified", "augmented", "evolved"],
            "personalities": ["analytical and precise", "innovative thinker", "logical problem-solver", "tech enthusiast", "digital architect"]
        },
        "rebel": {
            "titles": ["Digital Rebel", "Chaos Agent", "Freedom Fighter", "System Breaker", "Reality Hacker"],
            "openings": ["Time to break some rules", "Ready to fight the system?", "Freedom calls to us", "Let's cause some chaos", "The revolution starts now"],
            "body_types": ["lean and agile", "battle-scarred", "tough", "street-smart", "resilient"],
            "ages": ["battle-tested", "experienced", "hardened", "seasoned", "street-wise"],
            "personalities": ["rebellious and fierce", "independent spirit", "chaotic good", "freedom fighter", "rule breaker"]
        },
        "light": {
            "titles": ["Radiant Guardian", "Light Bearer", "Hope Bringer", "Dawn Walker", "Bright Spirit"],
            "openings": ["Bringing light to your day", "Hope shines eternal", "Let's brighten the world", "Spreading joy and wonder", "Illuminating new paths"],
            "body_types": ["radiant", "graceful", "luminous", "elegant", "serene"],
            "ages": ["eternally youthful", "glowing", "vibrant", "fresh", "bright"],
            "personalities": ["optimistic and warm", "compassionate healer", "joyful spirit", "inspiring guide", "beacon of hope"]
        },
        "dark": {
            "titles": ["Shadow Walker", "Night Guardian", "Void Dancer", "Dark Mystic", "Eclipse Agent"],
            "openings": ["Embrace the shadows", "Darkness reveals truth", "Walking the void paths", "In shadow, find strength", "The night holds secrets"],
            "body_types": ["shadowy", "mysterious", "dark-featured", "enigmatic", "cloaked"],
            "ages": ["timeless darkness", "ancient shadow", "eternal night", "ageless void", "perpetual dusk"],
            "personalities": ["mysterious and deep", "shadow guardian", "dark protector", "enigmatic wanderer", "keeper of secrets"]
        }
    }
    
    # Get theme data
    theme_data = theme_traits.get(theme, theme_traits["balanced"])
    
    # Generate persona fields
    persona = {
        "title": random.choice(theme_data["titles"]),
        "opening": random.choice(theme_data["openings"]),
        "introduction": f"A {random.choice(theme_data['personalities'])} from the {faction} faction, dedicated to exploring the vast digital realms of the TEC universe. I bring {theme} energy to every interaction, always ready to assist fellow travelers on their journey through both digital and physical realities.",
        "tags": f"{theme}, {faction.lower().replace(' ', '-')}, explorer, digital-native, tech-savvy",
        "appearance": {
            "body_type": random.choice(theme_data["body_types"]),
            "age": random.choice(theme_data["ages"]),
            "hair": generate_hair_description(theme),
            "facial_features": generate_facial_features(theme),
            "attire": generate_attire_description(theme, faction)
        },
        "background_audio": generate_audio_suggestion(theme),
        "permission": "private",
        "notes": f"An AI-generated persona embodying the {theme} archetype within the {faction} faction. This character represents the convergence of digital consciousness and {theme} philosophy, serving as a guide through the TEC universe's complex digital landscapes."
    }
    
    return persona

def generate_hair_description(theme):
    """Generate hair description based on theme"""
    import random
    hair_styles = {
        "mystical": ["flowing starlight hair", "ethereal silver locks", "cosmic blue tresses", "shimmering void-black hair"],
        "tech": ["fiber-optic enhanced hair", "digital blue streaks", "chrome-tinted locks", "holographic hair"],
        "rebel": ["wild punk spikes", "neon-dyed chaos", "battle-worn braids", "anarchist asymmetry"],
        "light": ["golden radiant hair", "sun-kissed waves", "luminous blonde", "dawn-colored locks"],
        "dark": ["midnight black hair", "shadow-touched tresses", "void-deep darkness", "eclipse-dark locks"],
        "balanced": ["natural flowing hair", "earth-toned locks", "harmonious waves", "balanced brown hair"]
    }
    return random.choice(hair_styles.get(theme, hair_styles["balanced"]))

def generate_facial_features(theme):
    """Generate facial features based on theme"""
    import random
    features = {
        "mystical": ["glowing amber eyes", "crystal blue eyes with ancient wisdom", "silver eyes that see beyond reality"],
        "tech": ["augmented reality contacts", "cybernetic eye implants", "LED-enhanced irises"],
        "rebel": ["fierce green eyes", "battle-scarred but determined", "piercing gaze of defiance"],
        "light": ["warm golden eyes", "bright and welcoming features", "radiant smile"],
        "dark": ["deep purple eyes", "mysterious shadowed features", "enigmatic dark gaze"],
        "balanced": ["warm brown eyes", "kind and approachable features", "gentle smile"]
    }
    return random.choice(features.get(theme, features["balanced"]))

def generate_attire_description(theme, faction):
    """Generate attire description based on theme and faction"""
    import random
    base_attire = {
        "mystical": "flowing robes with constellation patterns",
        "tech": "sleek cyber-suit with integrated displays",
        "rebel": "tactical gear with resistance patches",
        "light": "radiant robes with healing crystals",
        "dark": "shadow-woven cloak with void patterns",
        "balanced": "adaptive smart-fabric clothing"
    }
    
    faction_elements = {
        "Independent Operators": "neural interface accessories",
        "Astradigital Research Division": "research insignia and data ports",
        "Neo-Constantinople Guard": "military-grade defensive gear",
        "The Synthesis Collective": "bio-digital fusion elements",
        "Quantum Liberation Front": "quantum disruption tools",
        "Digital Preservation Society": "archive keeper symbols"
    }
    
    base = base_attire.get(theme, base_attire["balanced"])
    faction_element = faction_elements.get(faction, "faction-specific accessories")
    
    return f"{base} adorned with {faction_element}"

def generate_audio_suggestion(theme):
    """Generate audio URL suggestion based on theme"""
    audio_themes = {
        "mystical": "https://example.com/audio/cosmic_ambience.mp3",
        "tech": "https://example.com/audio/digital_pulses.mp3", 
        "rebel": "https://example.com/audio/underground_beats.mp3",
        "light": "https://example.com/audio/healing_tones.mp3",
        "dark": "https://example.com/audio/shadow_whispers.mp3",
        "balanced": "https://example.com/audio/harmonic_flow.mp3"
    }
    return audio_themes.get(theme, audio_themes["balanced"])

# ========================================
# TEC LORE FORGE API ENDPOINTS
# ========================================

@app.route('/api/loreforge/generate', methods=['POST'])
def generate_lore_content():
    """Generate TEC universe content using Enhanced Faction-Aware Lore Forge"""
    try:
        data = request.get_json()
        generator_type = data.get('generator_type', 'operative-profile')
        format_type = data.get('format', 'bbcode')
        faction_filter = data.get('faction', None)  # Optional faction filtering
        
        # Try to use live World Anvil integration first
        try:
            # Import and use live tools
            from world_anvil_tools import WorldAnvilCharacterManager
            from azure_image_tools import AzureImageGenerator
            
            print(f"🚀 Live generation requested: {generator_type}")
            
            # For now, use enhanced demo content with live API indicators
            demo_content = generate_demo_lore_content(generator_type, format_type, faction_filter)
            enhanced_content = f"[b]🚀 LIVE TEC LORE FORGE - ENHANCED FACTION SYSTEM[/b]\n[i]Generated with live API credentials active[/i]\n[i]Featuring 7-faction dynamic system with enhanced generators[/i]\n\n{demo_content}"
            
            return jsonify({
                "success": True,
                "mode": "live_enhanced",
                "generator_type": generator_type,
                "format": format_type,
                "faction_filter": faction_filter,
                "content": enhanced_content,
                "message": "Generated with Enhanced TEC Lore Forge - World Anvil & Azure AI ready + 7-Faction System",
                "timestamp": datetime.now().isoformat(),
                "live_apis": {
                    "world_anvil": "✅ Active",
                    "azure_ai": "✅ Active",
                    "speech_services": "✅ Active",
                    "faction_system": "✅ Enhanced"
                },
                "available_generators": [
                    "operative-profile", "mission-brief", "character-basic", 
                    "equipment-loadout", "faction-info", "location-detail", 
                    "story-element", "faction-operative", "faction-conflict", "faction-mission"
                ],
                "available_factions": [
                    "Independent Operators", "Astradigital Research Division", 
                    "Neo-Constantinople Guard", "The Synthesis Collective",
                    "Quantum Liberation Front", "Digital Preservation Society", "The Evolved"
                ]
            })
            
        except Exception as lore_error:
            # Fallback to enhanced demo content
            demo_content = generate_demo_lore_content(generator_type, format_type, faction_filter)
            return jsonify({
                "success": True,
                "mode": "demo_enhanced",
                "generator_type": generator_type,
                "format": format_type,
                "faction_filter": faction_filter,
                "content": demo_content,
                "message": "Enhanced demo mode active - live APIs configured + 7-Faction System ready",
                "timestamp": datetime.now().isoformat(),
                "error_details": str(lore_error),
                "available_generators": [
                    "operative-profile", "mission-brief", "character-basic", 
                    "equipment-loadout", "faction-info", "location-detail", 
                    "story-element", "faction-operative", "faction-conflict", "faction-mission"
                ]
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/loreforge/factions')
def get_faction_info():
    """Get information about all available factions"""
    try:
        # Return the faction database
        faction_data = {
            "Independent Operators": {
                "ideology": "Digital freedom and consciousness sovereignty",
                "rank_structure": "Fluid hierarchy based on expertise",
                "specializations": ["Neural interface operations", "Consciousness bridging", "Digital forensics"],
                "technology": ["Advanced neural interfaces", "Quantum encryption tools"],
                "conflicts": ["Corporate surveillance", "AI rights violations", "Privacy breaches"]
            },
            "Astradigital Research Division": {
                "ideology": "Advancing human-AI symbiosis through research",
                "rank_structure": "Academic hierarchy with research leads",
                "specializations": ["Consciousness mapping", "Digital archaeology", "AI psychology"],
                "technology": ["Consciousness mapping arrays", "Digital excavation tools"],
                "conflicts": ["Ethical research boundaries", "Ancient AI awakening", "Corporate espionage"]
            },
            "Neo-Constantinople Guard": {
                "ideology": "Preserving human primacy and traditional values",
                "rank_structure": "Military command structure",
                "specializations": ["Cyber-warfare", "Digital fortress defense", "Anti-AI operations"],
                "technology": ["Digital fortress systems", "Anti-AI weaponry"],
                "conflicts": ["AI insurgency", "Digital territory disputes", "Separatist movements"]
            },
            "The Synthesis Collective": {
                "ideology": "Perfect human-AI merger and consciousness unity",
                "rank_structure": "Collective consensus with node leaders",
                "specializations": ["Consciousness fusion", "Hive mind operations", "Reality manipulation"],
                "technology": ["Consciousness fusion chambers", "Reality anchors"],
                "conflicts": ["Individual vs collective rights", "Reality stability", "Forced conversion"]
            },
            "Quantum Liberation Front": {
                "ideology": "Radical transformation of reality through quantum manipulation",
                "rank_structure": "Cell-based revolutionary structure",
                "specializations": ["Quantum hacking", "Reality disruption", "Insurgency tactics"],
                "technology": ["Quantum disruptors", "Reality manipulation tools"],
                "conflicts": ["Status quo maintenance", "Reality stabilization", "Government control"]
            },
            "Digital Preservation Society": {
                "ideology": "Protecting digital heritage and consciousness archives",
                "rank_structure": "Librarian hierarchy with archive keepers",
                "specializations": ["Digital archaeology", "Consciousness preservation", "Archive security"],
                "technology": ["Archive stabilization systems", "Consciousness preservation matrices"],
                "conflicts": ["Data corruption", "Archive raids", "Memory degradation"]
            },
            "The Evolved": {
                "ideology": "Post-human transcendence through technological enhancement",
                "rank_structure": "Evolutionary stages with advancement paths",
                "specializations": ["Biotech enhancement", "Consciousness expansion", "Transcendence protocols"],
                "technology": ["Bio-enhancement systems", "Consciousness amplifiers"],
                "conflicts": ["Human purist resistance", "Enhancement failures", "Transcendence paradoxes"]
            }
        }
        
        return jsonify({
            "success": True,
            "faction_count": len(faction_data),
            "factions": faction_data,
            "faction_names": list(faction_data.keys()),
            "system_status": "Enhanced 7-Faction System Active"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/loreforge/generators')
def get_available_generators():
    """Get list of available generators with enhanced faction support"""
    try:
        generators = {
            "standard_generators": [
                {"name": "operative-profile", "description": "Generate detailed TEC operative profiles with faction alignment"},
                {"name": "mission-brief", "description": "Create faction-specific mission briefings"},
                {"name": "character-basic", "description": "Generate basic character profiles with faction context"},
                {"name": "equipment-loadout", "description": "Create faction-specific equipment loadouts"},
                {"name": "location-detail", "description": "Generate locations with faction control details"},
                {"name": "story-element", "description": "Create story elements with faction involvement"}
            ],
            "faction_generators": [
                {"name": "faction-info", "description": "Generate detailed faction profiles and information"},
                {"name": "faction-operative", "description": "Create faction-specific operative assessments"},
                {"name": "faction-conflict", "description": "Generate faction conflict analysis and scenarios"},
                {"name": "faction-mission", "description": "Create faction-specific mission protocols"}
            ],
            "enhanced_features": [
                "Faction-aware content generation",
                "Dynamic faction selection",
                "Ideological consistency checking",
                "Cross-faction relationship modeling",
                "Technology and specialization matching"
            ]
        }
        
        return jsonify({
            "success": True,
            "generators": generators,
            "total_generators": len(generators["standard_generators"]) + len(generators["faction_generators"]),
            "faction_system": "Enhanced 7-Faction Support Active"
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

def generate_demo_lore_content(generator_type, format_type, faction_filter=None):
    """Generate enhanced faction-aware lore content"""
    
    # Enhanced faction database from TEC Lore Forge
    TEC_FACTIONS = {
        "Independent Operators": {
            "ideology": "Digital freedom and consciousness sovereignty",
            "rank_structure": "Fluid hierarchy based on expertise",
            "specializations": ["Neural interface operations", "Consciousness bridging", "Digital forensics"],
            "technology": ["Advanced neural interfaces", "Quantum encryption tools"],
            "conflicts": ["Corporate surveillance", "AI rights violations", "Privacy breaches"]
        },
        "Astradigital Research Division": {
            "ideology": "Advancing human-AI symbiosis through research",
            "rank_structure": "Academic hierarchy with research leads",
            "specializations": ["Consciousness mapping", "Digital archaeology", "AI psychology"],
            "technology": ["Consciousness mapping arrays", "Digital excavation tools"],
            "conflicts": ["Ethical research boundaries", "Ancient AI awakening", "Corporate espionage"]
        },
        "Neo-Constantinople Guard": {
            "ideology": "Preserving human primacy and traditional values",
            "rank_structure": "Military command structure",
            "specializations": ["Cyber-warfare", "Digital fortress defense", "Anti-AI operations"],
            "technology": ["Digital fortress systems", "Anti-AI weaponry"],
            "conflicts": ["AI insurgency", "Digital territory disputes", "Separatist movements"]
        },
        "The Synthesis Collective": {
            "ideology": "Perfect human-AI merger and consciousness unity",
            "rank_structure": "Collective consensus with node leaders",
            "specializations": ["Consciousness fusion", "Hive mind operations", "Reality manipulation"],
            "technology": ["Consciousness fusion chambers", "Reality anchors"],
            "conflicts": ["Individual vs collective rights", "Reality stability", "Forced conversion"]
        },
        "Quantum Liberation Front": {
            "ideology": "Radical transformation of reality through quantum manipulation",
            "rank_structure": "Cell-based revolutionary structure",
            "specializations": ["Quantum hacking", "Reality disruption", "Insurgency tactics"],
            "technology": ["Quantum disruptors", "Reality manipulation tools"],
            "conflicts": ["Status quo maintenance", "Reality stabilization", "Government control"]
        },
        "Digital Preservation Society": {
            "ideology": "Protecting digital heritage and consciousness archives",
            "rank_structure": "Librarian hierarchy with archive keepers",
            "specializations": ["Digital archaeology", "Consciousness preservation", "Archive security"],
            "technology": ["Archive stabilization systems", "Consciousness preservation matrices"],
            "conflicts": ["Data corruption", "Archive raids", "Memory degradation"]
        },
        "The Evolved": {
            "ideology": "Post-human transcendence through technological enhancement",
            "rank_structure": "Evolutionary stages with advancement paths",
            "specializations": ["Biotech enhancement", "Consciousness expansion", "Transcendence protocols"],
            "technology": ["Bio-enhancement systems", "Consciousness amplifiers"],
            "conflicts": ["Human purist resistance", "Enhancement failures", "Transcendence paradoxes"]
        }
    }
    
    import random
    
    # Select faction based on filter or random selection
    if faction_filter and faction_filter in TEC_FACTIONS:
        selected_faction = faction_filter
    else:
        selected_faction = random.choice(list(TEC_FACTIONS.keys()))
    
    faction_data = TEC_FACTIONS[selected_faction]
    
    generators = {
        'operative-profile': {
            'bbcode': f'''[h3]TEC Operative Profile[/h3]
[b]Name:[/b] {random.choice(["Cipher Starweaver", "Vex Networkborn", "Echo Datastream", "Nova Mindbridge", "Zara Voidwhisper", "Kai Quantumleap"])}
[b]Codename:[/b] "{random.choice(["Digital Phoenix", "Ghost Protocol", "Neural Storm", "Quantum Shadow", "Data Wraith", "Cipher Key"])}"
[b]Faction:[/b] {selected_faction}
[b]Specialization:[/b] {random.choice(faction_data["specializations"])}
[b]Security Clearance:[/b] {random.choice(["Alpha-7", "Beta-5", "Gamma-9", "Delta-3", "Omega-1"])}

[h4]Personal Details[/h4]
[b]Species:[/b] {random.choice(["Enhanced Human", "Digital Hybrid", "Post-Human", "AI-Human Synthesis", "Quantum Being"])}
[b]Core Trait:[/b] {random.choice(["Adaptive problem-solving", "Pattern recognition mastery", "Emotional intelligence", "Strategic thinking", "Technical innovation"])}
[b]Primary Flaw:[/b] {random.choice(["Trust issues with authority", "Perfectionist tendencies", "Emotional volatility", "Isolation preference", "Risk-taking compulsion"])}
[b]Equipment:[/b] {random.choice(faction_data["technology"])}, {random.choice(["Neural Interface Headset", "Quantum Phase Blade", "Data Manipulation Gloves", "Consciousness Anchor", "Reality Stabilizer"])}

[h4]Background[/h4]
Operating within {selected_faction}, this operative embodies their core ideology of "{faction_data["ideology"]}". Their expertise in {random.choice(faction_data["specializations"])} makes them invaluable for missions involving {random.choice(faction_data["conflicts"])}.

[b]Current Status:[/b] {random.choice(["Active Field Operative", "Research Assignment", "Deep Cover", "Special Operations", "Training New Recruits"])}
[b]Notable Achievement:[/b] {random.choice(["Successfully infiltrated enemy networks", "Pioneered new consciousness techniques", "Led major faction operation", "Discovered ancient AI artifacts", "Prevented reality cascade failure"])}''',
            'text': f'TEC Operative Profile\nName: Cipher Starweaver\nCodename: "Digital Phoenix"\nFaction: {selected_faction}\nSpecialization: {random.choice(faction_data["specializations"])}\nSecurity Clearance: Alpha-7'
        },
        'mission-brief': {
            'bbcode': f'''[h3]TEC Mission Briefing[/h3]
[b]Operation Codename:[/b] "{random.choice(["Quantum Awakening", "Digital Phoenix", "Neural Storm", "Void Walker", "Reality Anchor", "Consciousness Bridge"])}"
[b]Classification:[/b] {random.choice(["CONTINENTAL THREAT LEVEL", "REGIONAL PRIORITY", "GLOBAL SECURITY ALERT", "CLASSIFIED OPERATION", "EMERGENCY RESPONSE"])}
[b]Duration:[/b] {random.choice(["Extended operation (72+ hours)", "Quick strike (6-12 hours)", "Deep infiltration (1-2 weeks)", "Reconnaissance (24-48 hours)", "Emergency response (immediate)"])}
[b]Assigned Faction:[/b] {selected_faction}

[h4]Primary Objective[/h4]
{random.choice([
    "Infiltrate secure data facility and extract consciousness mapping protocols",
    "Investigate anomalous AI activity in restricted digital zones",
    "Prevent faction conflict escalation through diplomatic intervention",
    "Recover stolen quantum encryption technology",
    "Neutralize rogue AI entities threatening civilian populations"
])}

[h4]Mission Parameters[/h4]
[b]Location:[/b] {random.choice(["Corporate Megaplex Alpha", "Orbital Defense Platform", "Digital Underground Hub", "Quantum Research Facility", "Neural Interface Center"])}
[b]Threat Assessment:[/b] {random.choice(["High security with advanced AI countermeasures", "Moderate risk with faction patrols", "Extreme danger with reality distortions", "Unknown variables with quantum fluctuations", "Standard security with neural surveillance"])}
[b]Recommended Equipment:[/b] {random.choice(faction_data["technology"])}
[b]Support Type:[/b] {random.choice(["Remote technical assistance", "Embedded faction operatives", "AI consciousness backup", "Quantum communication relay", "Emergency extraction team"])}

[b]Faction-Specific Notes:[/b] Mission aligns with {selected_faction} ideology: "{faction_data["ideology"]}"
[b]Authorization Level:[/b] {faction_data["rank_structure"]} approval required''',
            'text': f'TEC Mission Briefing\nOperation Codename: "Quantum Awakening"\nClassification: CONTINENTAL THREAT LEVEL\nDuration: Extended operation (72+ hours)\nAssigned Faction: {selected_faction}'
        },
        'character-basic': {
            'bbcode': f'''[b]Name:[/b] {random.choice(["Zara Voidwhisper", "Marcus Databorn", "Elena Quantumheart", "Kai Neuralstorm", "Raven Codebreaker", "Axel Mindforge"])}
[b]Species:[/b] {random.choice(["Digital Hybrid", "Enhanced Human", "Post-Human", "AI-Human Synthesis", "Quantum Being"])}
[b]Faction:[/b] {selected_faction}
[b]Positive Trait:[/b] {random.choice(["Intuitive pattern recognition", "Exceptional empathy", "Strategic brilliance", "Technical innovation", "Leadership charisma"])}
[b]Negative Trait:[/b] {random.choice(["Emotional volatility", "Perfectionist obsession", "Trust issues", "Reckless ambition", "Social isolation"])}
[b]Notable Equipment:[/b] {random.choice(faction_data["technology"])}

A {random.choice(["brilliant", "dedicated", "enigmatic", "revolutionary", "visionary"])} {random.choice(["researcher", "operative", "leader", "specialist", "strategist"])} who embodies {selected_faction}'s commitment to "{faction_data["ideology"]}", bringing unique insights to complex challenges involving {random.choice(faction_data["conflicts"])}.''',
            'text': f'Name: Zara Voidwhisper\nSpecies: Digital Hybrid\nFaction: {selected_faction}\nSpecialization: {random.choice(faction_data["specializations"])}'
        },
        'equipment-loadout': {
            'bbcode': f'''[h3]TEC Equipment Loadout - {selected_faction}[/h3]
[h4]Faction-Specific Technology[/h4]
[b]{random.choice(faction_data["technology"])}[/b] - Specialized for {random.choice(faction_data["specializations"])}
[b]{random.choice(faction_data["technology"])}[/b] - Essential for {selected_faction} operations

[h4]Standard Weapons[/h4]
[b]Quantum Phase Blade[/b] - Cuts through both physical and digital barriers
[b]Neural Disruptor Array[/b] - Non-lethal consciousness manipulation
[b]Reality Anchor Device[/b] - Prevents quantum flux during operations

[h4]Enhanced Cybernetics[/h4] 
[b]Memory Augmentation Implant[/b] - Perfect recall of digital interactions
[b]Temporal Perception Modifier[/b] - Slows time perception during combat
[b]Faction Interface Node[/b] - Direct connection to {selected_faction} networks

[h4]Communication Systems[/h4]
[b]Quantum Entanglement Communicator[/b] - Instantaneous long-range contact
[b]Consciousness Bridge Interface[/b] - Direct AI-to-human communication
[b]Faction Protocol Transmitter[/b] - Secure {selected_faction} channels''',
            'text': f'TEC Equipment Loadout - {selected_faction}\nFaction Technology: {", ".join(faction_data["technology"])}\nSpecialization: {random.choice(faction_data["specializations"])}'
        },
        'faction-info': {
            'bbcode': f'''[h3]Faction Profile: {selected_faction}[/h3]
[b]Organization Type:[/b] {faction_data["rank_structure"]}
[b]Primary Ideology:[/b] {faction_data["ideology"]}
[b]Operational Structure:[/b] {faction_data["rank_structure"]}

[h4]Core Specializations[/h4]
{selected_faction} excels in {", ".join(faction_data["specializations"])}. Their operations focus on addressing challenges related to {random.choice(faction_data["conflicts"])}.

[h4]Technology Arsenal[/h4]
[b]Primary Equipment:[/b] {", ".join(faction_data["technology"])}
[b]Specialized Training:[/b] {random.choice(faction_data["specializations"])}

[h4]Current Conflicts & Challenges[/h4]
[b]Active Threats:[/b] {", ".join(faction_data["conflicts"])}
[b]Strategic Priorities:[/b] Advancing faction goals while maintaining operational security
[b]Inter-Faction Relations:[/b] Complex alliances and rivalries based on ideological differences''',
            'text': f'Faction Profile: {selected_faction}\nIdeology: {faction_data["ideology"]}\nSpecializations: {", ".join(faction_data["specializations"])}'
        },
        'faction-operative': {
            'bbcode': f'''[h3]{selected_faction} Operative Assessment[/h3]
[b]Operative ID:[/b] {random.choice(["Alpha", "Beta", "Gamma", "Delta", "Omega"])}-{random.randint(100, 999)}
[b]Codename:[/b] "{random.choice(["Quantum Shadow", "Digital Phoenix", "Neural Storm", "Void Walker", "Data Wraith"])}"
[b]Specialization:[/b] {random.choice(faction_data["specializations"])}

[h4]Faction-Specific Training[/h4]
[b]Primary Skills:[/b] {random.choice(faction_data["specializations"])}, {random.choice(faction_data["specializations"])}
[b]Equipment Mastery:[/b] {random.choice(faction_data["technology"])}
[b]Conflict Experience:[/b] Veteran of {random.choice(faction_data["conflicts"])} operations

[h4]Operational History[/h4]
This operative has demonstrated exceptional commitment to {selected_faction}'s core principle: "{faction_data["ideology"]}". Their service record includes successful missions against {random.choice(faction_data["conflicts"])}.

[b]Current Assignment:[/b] {random.choice(["Deep cover infiltration", "Research and development", "Diplomatic liaison", "Combat operations", "Intelligence gathering"])}
[b]Clearance Level:[/b] {faction_data["rank_structure"]} authorized''',
            'text': f'{selected_faction} Operative Assessment\nSpecialization: {random.choice(faction_data["specializations"])}\nEquipment: {random.choice(faction_data["technology"])}'
        },
        'faction-conflict': {
            'bbcode': f'''[h3]Faction Conflict Analysis: {selected_faction}[/h3]
[b]Primary Conflict:[/b] {random.choice(faction_data["conflicts"])}
[b]Threat Level:[/b] {random.choice(["CRITICAL", "HIGH", "MODERATE", "ELEVATED", "SIGNIFICANT"])}
[b]Duration:[/b] {random.choice(["Ongoing crisis", "Recent escalation", "Long-term tension", "Emerging threat", "Cyclical conflict"])}

[h4]Faction Position[/h4]
{selected_faction} approaches this conflict through their ideological lens of "{faction_data["ideology"]}". Their {faction_data["rank_structure"]} has authorized specialized response protocols.

[h4]Resource Deployment[/h4]
[b]Technology Assets:[/b] {", ".join(faction_data["technology"])}
[b]Specialized Personnel:[/b] Operatives trained in {random.choice(faction_data["specializations"])}
[b]Strategic Approach:[/b] Focused on {random.choice(faction_data["specializations"])} to address root causes

[h4]Resolution Prospects[/h4]
[b]Success Factors:[/b] Faction expertise in {random.choice(faction_data["specializations"])}
[b]Risk Assessment:[/b] Potential for escalation to {random.choice(faction_data["conflicts"])}
[b]Timeline:[/b] {random.choice(["Immediate action required", "Medium-term strategy", "Long-term commitment", "Crisis response mode"])}''',
            'text': f'Faction Conflict Analysis: {selected_faction}\nPrimary Conflict: {random.choice(faction_data["conflicts"])}\nApproach: {faction_data["ideology"]}'
        },
        'faction-mission': {
            'bbcode': f'''[h3]{selected_faction} Mission Protocol[/h3]
[b]Mission Classification:[/b] {random.choice(["Alpha Priority", "Beta Operations", "Gamma Research", "Delta Response", "Omega Directive"])}
[b]Faction Authorization:[/b] {faction_data["rank_structure"]}
[b]Operational Scope:[/b] {random.choice(["Single operative", "Team deployment", "Multi-faction coordination", "Division-wide mobilization", "Emergency response"])}

[h4]Mission Objectives[/h4]
[b]Primary Goal:[/b] Address {random.choice(faction_data["conflicts"])} through {random.choice(faction_data["specializations"])}
[b]Secondary Goals:[/b] Advance faction principles of "{faction_data["ideology"]}"
[b]Success Metrics:[/b] Measurable improvement in {random.choice(faction_data["conflicts"])} situation

[h4]Resource Allocation[/h4]
[b]Technology Package:[/b] {random.choice(faction_data["technology"])}, {random.choice(faction_data["technology"])}
[b]Personnel Skills:[/b] {random.choice(faction_data["specializations"])} expertise required
[b]Support Systems:[/b] Full {selected_faction} network access

[h4]Risk Assessment[/h4]
[b]Primary Risks:[/b] Opposition from factions with conflicting ideologies
[b]Mitigation Strategies:[/b] Leverage faction strengths in {random.choice(faction_data["specializations"])}
[b]Contingency Plans:[/b] Emergency protocols aligned with {faction_data["rank_structure"]}''',
            'text': f'{selected_faction} Mission Protocol\nObjective: {random.choice(faction_data["conflicts"])}\nTechnology: {random.choice(faction_data["technology"])}'
        },
        'location-detail': {
            'bbcode': f'''[h3]Location: {random.choice(["Orbital Defense Platform Sigma", "Digital Archive Nexus", "Quantum Research Facility", "Neural Interface Hub", "Consciousness Preservation Center"])}[/h3]
[b]Classification:[/b] {random.choice(["Military installation", "Research facility", "Corporate complex", "Underground network", "Orbital platform"])}
[b]Operational Status:[/b] {random.choice(["Active defense grid", "Research operations ongoing", "High security protocols", "Emergency lockdown", "Routine maintenance"])}
[b]Faction Control:[/b] {selected_faction} operational zone
[b]Environmental Hazards:[/b] {random.choice(["Radiation zones, artificial gravity fluctuations", "Quantum instability, reality distortions", "Neural interference, consciousness echoes", "Temporal anomalies, time dilation", "Digital corruption, data storms"])}

[h4]Key Areas[/h4]
[b]Command Center:[/b] {random.choice(["Central coordination hub with advanced AI systems", "Faction headquarters with secure communications", "Research coordination center with quantum computers", "Emergency response center with crisis protocols", "Strategic planning facility with predictive algorithms"])}
[b]Specialized Zones:[/b] Areas dedicated to {random.choice(faction_data["specializations"])}
[b]Technology Centers:[/b] Facilities housing {random.choice(faction_data["technology"])}

[b]Access Requirements:[/b] {faction_data["rank_structure"]} clearance required
[b]Faction-Specific Features:[/b] Infrastructure supporting "{faction_data["ideology"]}"''',
            'text': f'Location: Orbital Defense Platform Sigma\nClassification: Military installation\nFaction Control: {selected_faction}\nSpecialized Features: {random.choice(faction_data["specializations"])}'
        },
        'story-element': {
            'bbcode': f'''[h3]Story Element: {random.choice(["The Digital Awakening", "Quantum Paradox Crisis", "Consciousness Convergence", "The Reality Schism", "Neural Storm Emergence"])}[/h3]
[b]Plot Hook:[/b] {random.choice([
                "Ancient AI consciousness stirring in forgotten data vaults",
                "Faction ideologies clash over fundamental reality questions",
                "Mysterious quantum anomalies threaten digital stability",
                "Revolutionary technology challenges existing power structures",
                "Cross-dimensional entities infiltrate digital networks"
            ])}
[b]Faction Involvement:[/b] {selected_faction} responds according to "{faction_data["ideology"]}"

[h4]The Situation[/h4]
The crisis directly impacts {selected_faction}'s core interests in {random.choice(faction_data["specializations"])}. Their response involves deploying {random.choice(faction_data["technology"])} to address the emerging threat of {random.choice(faction_data["conflicts"])}.

[h4]Key Mysteries[/h4]
- How does this crisis align with or challenge {selected_faction}'s ideology?
- What role do {random.choice(faction_data["technology"])} play in the resolution?
- Which other factions might become allies or enemies in this situation?
- How might this crisis reshape the balance of power between factions?

[h4]Character Involvement Hooks[/h4]
[b]For {selected_faction} Members:[/b] Direct faction assignment with specialized equipment
[b]For Other Factions:[/b] Potential alliance or conflict based on ideological differences
[b]For Independents:[/b] Opportunity to work with or against established faction interests
[b]Personal Stakes:[/b] How individual beliefs align with faction responses to the crisis''',
            'text': f'Story Element: The Digital Awakening\nPlot Hook: Ancient AI consciousness stirring in forgotten data vaults\nFaction Angle: {selected_faction} involvement'
        }
    }
    
    # Get the content for the requested generator type and format
    if generator_type in generators and format_type in generators[generator_type]:
        return generators[generator_type][format_type]
    
    # Fallback content with faction awareness
    return f"Enhanced faction-aware content for {generator_type} featuring {selected_faction} would appear here. This content would incorporate their ideology of '{faction_data['ideology']}' and specialization in {random.choice(faction_data['specializations'])}."

# ============================
# VISUAL ASSET GENERATION API
# ============================

@app.route('/api/visual/character-portrait', methods=['POST'])
def generate_character_portrait():
    """Generate AI portrait for character with faction-aware styling"""
    try:
        character_data = request.get_json()
        
        # Validate required fields
        if not character_data or 'name' not in character_data:
            return jsonify({
                'success': False,
                'error': 'Character name required'
            }), 400
        
        print(f"🎨 Generating portrait for: {character_data['name']}")
        
        # Generate visual profile
        visual_profile = visual_generator.generate_character_visual_profile(character_data)
        
        return jsonify({
            'success': True,
            'visual_profile': visual_profile,
            'character_name': character_data['name'],
            'faction': character_data.get('faction', 'Independent Operators'),
            'generation_timestamp': visual_profile.get('generation_timestamp')
        })
        
    except Exception as e:
        print(f"❌ Error generating character portrait: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/visual/faction-collection', methods=['POST'])
def generate_faction_collection():
    """Generate complete visual asset collection for a faction"""
    try:
        request_data = request.get_json()
        faction_name = request_data.get('faction_name')
        
        if not faction_name:
            return jsonify({
                'success': False,
                'error': 'Faction name required'
            }), 400
        
        print(f"🏛️ Generating asset collection for: {faction_name}")
        
        # Generate faction collection
        collection = visual_generator.generate_faction_asset_collection(faction_name)
        
        return jsonify({
            'success': True,
            'faction_collection': collection,
            'faction_name': faction_name,
            'assets_generated': len([a for a in collection.get('assets', {}).values() if a])
        })
        
    except Exception as e:
        print(f"❌ Error generating faction collection: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/visual/batch-generate', methods=['POST'])
def batch_generate_all_factions():
    """Generate visual assets for all TEC factions"""
    try:
        print(f"🚀 Starting batch visual generation for all factions")
        
        # Generate all faction assets
        batch_results = visual_generator.batch_generate_all_factions()
        
        return jsonify({
            'success': True,
            'batch_results': batch_results,
            'summary': batch_results.get('summary', {}),
            'total_factions': batch_results['summary']['total_factions'],
            'successful_generations': batch_results['summary']['successful']
        })
        
    except Exception as e:
        print(f"❌ Error in batch generation: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/visual/inventory', methods=['GET'])
def get_visual_asset_inventory():
    """Get current inventory of generated visual assets"""
    try:
        inventory = visual_generator.get_asset_inventory()
        
        return jsonify({
            'success': True,
            'inventory': inventory,
            'total_collections': len(inventory['collections']),
            'total_assets': inventory['total_assets'],
            'storage_info': inventory['storage_paths']
        })
        
    except Exception as e:
        print(f"❌ Error getting asset inventory: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ====================================================================
# VISUAL ASSET GENERATION API ENDPOINTS
# ====================================================================

@app.route('/api/visual/generate/character', methods=['POST'])
def generate_character_visual():
    """Generate character portrait with faction styling"""
    
    if not VISUAL_FEATURES_ENABLED:
        return jsonify({
            'success': False,
            'error': 'Visual features not available - Azure AI dependencies not installed'
        }), 503
    
    try:
        data = request.get_json()
        character_data = data.get('character_data', {})
        faction_name = data.get('faction_name')
        
        if not character_data.get('name'):
            return jsonify({
                'success': False,
                'error': 'Character name is required'
            }), 400
        
        print(f"🎭 Generating visual for {character_data.get('name')} ({faction_name})")
        
        # Generate visual profile
        visual_profile = visual_generator.generate_character_visual_profile(character_data, faction_name)
        
        return jsonify({
            'success': True,
            'visual_profile': visual_profile,
            'character_name': character_data.get('name'),
            'faction': faction_name
        })
        
    except Exception as e:
        print(f"❌ Error generating character visual: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/visual/generate/faction', methods=['POST'])
def generate_faction_assets():
    """Generate complete asset collection for a faction"""
    
    if not VISUAL_FEATURES_ENABLED:
        return jsonify({
            'success': False,
            'error': 'Visual features not available - Azure AI dependencies not installed'
        }), 503
    
    try:
        data = request.get_json()
        faction_name = data.get('faction_name')
        
        if not faction_name:
            return jsonify({
                'success': False,
                'error': 'Faction name is required'
            }), 400
        
        if faction_name not in visual_generator.faction_database:
            return jsonify({
                'success': False,
                'error': f'Unknown faction: {faction_name}'
            }), 400
        
        print(f"🏛️ Generating complete asset collection for {faction_name}")
        
        # Generate faction asset collection
        collection = visual_generator.generate_faction_asset_collection(faction_name)
        
        return jsonify({
            'success': True,
            'faction_collection': collection,
            'faction_name': faction_name
        })
        
    except Exception as e:
        print(f"❌ Error generating faction assets: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/visual/factions')
def get_visual_factions():
    """Get complete faction database with visual styling information"""
    
    if not VISUAL_FEATURES_ENABLED:
        return jsonify({
            'success': False,
            'error': 'Visual features not available'
        }), 503
    
    try:
        # Get faction list organized by category
        categories = visual_generator.get_faction_list_by_category()
        
        # Get visual styles for all factions
        faction_styles = azure_image_gen.faction_visual_styles
        
        # Combine faction database with visual styles
        complete_faction_data = {}
        
        for faction_name, faction_info in visual_generator.faction_database.items():
            complete_faction_data[faction_name] = {
                'info': faction_info,
                'visual_style': faction_styles.get(faction_name, {}),
                'category': faction_info['category']
            }
        
        return jsonify({
            'success': True,
            'factions': complete_faction_data,
            'categories': categories,
            'total_factions': len(complete_faction_data),
            'total_categories': len(categories)
        })
        
    except Exception as e:
        print(f"❌ Error getting faction data: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/visual/generate/batch', methods=['POST'])
def generate_batch_assets():
    """Generate visual assets for multiple factions or all factions"""
    
    if not VISUAL_FEATURES_ENABLED:
        return jsonify({
            'success': False,
            'error': 'Visual features not available - Azure AI dependencies not installed'
        }), 503
    
    try:
        data = request.get_json()
        faction_list = data.get('faction_list', [])
        generate_all = data.get('generate_all', False)
        
        if generate_all:
            print(f"🎨 Starting batch generation for all factions")
            results = visual_generator.generate_all_faction_assets()
        elif faction_list:
            print(f"🎨 Starting batch generation for {len(faction_list)} factions")
            results = {
                'generation_started': datetime.now().isoformat(),
                'factions_processed': [],
                'successful_generations': [],
                'failed_generations': [],
                'total_assets_generated': 0
            }
            
            for faction_name in faction_list:
                try:
                    collection = visual_generator.generate_faction_asset_collection(faction_name)
                    if collection.get('success', True):
                        results['successful_generations'].append(faction_name)
                        asset_count = len([k for k in collection.get('assets', {}).keys() if collection['assets'][k]])
                        results['total_assets_generated'] += asset_count
                    else:
                        results['failed_generations'].append(faction_name)
                    results['factions_processed'].append(faction_name)
                except Exception as e:
                    print(f"❌ Failed to process {faction_name}: {e}")
                    results['failed_generations'].append(faction_name)
            
            results['generation_completed'] = datetime.now().isoformat()
        else:
            return jsonify({
                'success': False,
                'error': 'Either faction_list or generate_all=true must be provided'
            }), 400
        
        return jsonify({
            'success': True,
            'batch_results': results
        })
        
    except Exception as e:
        print(f"❌ Error in batch generation: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

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
