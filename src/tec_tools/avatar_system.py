"""
TEC Enhanced Avatar System
Provides animated character avatars with emotion recognition and memory reactions
"""

import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

class TECAvatarSystem:
    """Advanced avatar system for character animations and emotions"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_emotions = {}
        self.animation_states = {}
        self.memory_reactions = {}
        self.init_character_profiles()
        
    def init_character_profiles(self):
        """Initialize character animation profiles"""
        self.character_profiles = {
            "Polkin": {
                "base_color": "#8b5cf6",  # Purple mystical
                "secondary_color": "#a855f7",
                "animation_style": "mystical",
                "default_emotion": "wise",
                "personality_traits": ["mystical", "wise", "ethereal", "ancient"],
                "gesture_patterns": ["floating", "energy_swirls", "rune_casting"],
                "voice_pattern": "slow_rhythmic",
                "aura_effects": True,
                "particle_type": "mystical_sparkles"
            },
            "Mynx": {
                "base_color": "#06b6d4",  # Cyan tech
                "secondary_color": "#22d3ee", 
                "animation_style": "digital",
                "default_emotion": "analytical",
                "personality_traits": ["logical", "innovative", "precise", "adaptive"],
                "gesture_patterns": ["data_streams", "circuit_traces", "holographic_displays"],
                "voice_pattern": "quick_precise",
                "aura_effects": True,
                "particle_type": "digital_bits"
            },
            "Kaelen": {
                "base_color": "#f59e0b",  # Golden cosmic
                "secondary_color": "#fbbf24",
                "animation_style": "cosmic",
                "default_emotion": "serene",
                "personality_traits": ["peaceful", "wandering", "cosmic", "balanced"],
                "gesture_patterns": ["star_mapping", "cosmic_flows", "celestial_dance"],
                "voice_pattern": "flowing_melodic",
                "aura_effects": True,
                "particle_type": "star_dust"
            }
        }
    
    def analyze_emotion_from_text(self, text: str, character: str) -> Dict[str, Any]:
        """Analyze emotion from conversation text"""
        emotions = {
            "joy": 0.0,
            "sadness": 0.0,
            "anger": 0.0,
            "fear": 0.0,
            "surprise": 0.0,
            "curiosity": 0.0,
            "wisdom": 0.0,
            "excitement": 0.0
        }
        
        text_lower = text.lower()
        
        # Joy indicators
        joy_words = ['happy', 'excited', 'great', 'wonderful', 'amazing', 'love', 'fantastic', 'excellent']
        emotions["joy"] = sum(0.2 for word in joy_words if word in text_lower)
        
        # Curiosity indicators  
        curiosity_words = ['how', 'what', 'why', 'when', 'where', 'curious', 'wonder', 'question']
        emotions["curiosity"] = sum(0.15 for word in curiosity_words if word in text_lower)
        
        # Wisdom indicators
        wisdom_words = ['understand', 'learn', 'wisdom', 'knowledge', 'insight', 'deep', 'meaning']
        emotions["wisdom"] = sum(0.15 for word in wisdom_words if word in text_lower)
        
        # Excitement indicators
        excitement_words = ['wow', 'amazing', 'incredible', 'fantastic', 'awesome', '!']
        emotions["excitement"] = sum(0.1 for word in excitement_words if word in text_lower)
        
        # Character-specific emotion adjustments
        if character == "Polkin":
            emotions["wisdom"] += 0.3  # Always wise
            emotions["curiosity"] += 0.2  # Mystical curiosity
        elif character == "Mynx":  
            emotions["curiosity"] += 0.4  # Highly analytical
            emotions["excitement"] += 0.2  # Tech enthusiasm
        elif character == "Kaelen":
            emotions["wisdom"] += 0.2  # Cosmic wisdom
            emotions["joy"] += 0.2  # Peaceful joy
        
        # Normalize emotions
        max_emotion = max(emotions.values())
        if max_emotion > 1.0:
            emotions = {k: v/max_emotion for k, v in emotions.items()}
        
        # Determine primary emotion
        primary_emotion = max(emotions.keys(), key=lambda k: emotions[k])
        
        return {
            "primary_emotion": primary_emotion,
            "emotion_scores": emotions,
            "intensity": emotions[primary_emotion],
            "character": character
        }
    
    def get_animation_config(self, character: str, emotion_data: Dict, 
                           memory_context: Dict = None) -> Dict[str, Any]:
        """Generate animation configuration based on emotion and memory"""
        profile = self.character_profiles.get(character, self.character_profiles["Polkin"])
        primary_emotion = emotion_data.get("primary_emotion", "neutral")
        intensity = emotion_data.get("intensity", 0.5)
        
        # Base animation config
        config = {
            "character": character,
            "base_color": profile["base_color"],
            "secondary_color": profile["secondary_color"],
            "animation_style": profile["animation_style"],
            "emotion": primary_emotion,
            "intensity": intensity,
            "duration": self._calculate_animation_duration(intensity),
            "effects": []
        }
        
        # Add emotion-specific animations
        config.update(self._get_emotion_animations(character, primary_emotion, intensity))
        
        # Add memory-based enhancements
        if memory_context:
            config.update(self._get_memory_animations(character, memory_context))
        
        # Add particle effects
        config["particles"] = self._get_particle_config(character, primary_emotion, intensity)
        
        # Add gesture patterns
        config["gestures"] = self._get_gesture_patterns(character, primary_emotion)
        
        return config
    
    def _get_emotion_animations(self, character: str, emotion: str, intensity: float) -> Dict:
        """Get emotion-specific animation settings"""
        animations = {}
        
        # Character-specific emotion animations
        if character == "Polkin":
            emotion_map = {
                "wisdom": {
                    "eye_glow": "mystical_purple",
                    "aura_pattern": "wisdom_spirals",
                    "movement": "slow_floating",
                    "energy_field": "ancient_runes"
                },
                "curiosity": {
                    "eye_glow": "searching_light",
                    "aura_pattern": "question_marks",
                    "movement": "gentle_swaying",
                    "energy_field": "mystic_tendrils"
                },
                "joy": {
                    "eye_glow": "warm_golden",
                    "aura_pattern": "celebration_sparkles",
                    "movement": "upward_drift",
                    "energy_field": "joyful_streams"
                }
            }
        elif character == "Mynx":
            emotion_map = {
                "curiosity": {
                    "eye_glow": "scanning_blue",
                    "aura_pattern": "data_analysis",
                    "movement": "precise_tilting",
                    "energy_field": "circuit_patterns"
                },
                "excitement": {
                    "eye_glow": "electric_cyan",
                    "aura_pattern": "power_surge",
                    "movement": "energetic_bouncing",
                    "energy_field": "lightning_arcs"
                },
                "wisdom": {
                    "eye_glow": "steady_blue",
                    "aura_pattern": "knowledge_grid",
                    "movement": "calculated_nods",
                    "energy_field": "data_streams"
                }
            }
        elif character == "Kaelen":
            emotion_map = {
                "joy": {
                    "eye_glow": "stellar_gold",
                    "aura_pattern": "cosmic_celebration",
                    "movement": "orbital_dance",
                    "energy_field": "star_birth"
                },
                "wisdom": {
                    "eye_glow": "ancient_starlight",
                    "aura_pattern": "constellation_map",
                    "movement": "cosmic_meditation",
                    "energy_field": "galaxy_spiral"
                },
                "curiosity": {
                    "eye_glow": "wandering_light",
                    "aura_pattern": "exploration_paths",
                    "movement": "dimensional_shift",
                    "energy_field": "space_ripples"
                }
            }
        
        # Get animation for current emotion or default
        animations = emotion_map.get(emotion, {
            "eye_glow": "neutral_glow",
            "aura_pattern": "default_aura",
            "movement": "idle_breathing",
            "energy_field": "ambient_field"
        })
        
        # Adjust intensity
        animations["intensity_multiplier"] = intensity
        
        return animations
    
    def _get_memory_animations(self, character: str, memory_context: Dict) -> Dict:
        """Get memory-based animation enhancements"""
        memory_animations = {}
        
        relationship_level = memory_context.get("relationship_level", 1)
        conversation_count = memory_context.get("conversation_count", 0)
        
        # Bond level affects animation complexity
        if relationship_level >= 5:
            memory_animations["bond_effects"] = "strong_connection"
            memory_animations["recognition_glow"] = "familiar_warmth"
        elif relationship_level >= 3:
            memory_animations["bond_effects"] = "growing_bond"
            memory_animations["recognition_glow"] = "gentle_recognition"
        else:
            memory_animations["bond_effects"] = "new_acquaintance"
            memory_animations["recognition_glow"] = "curious_interest"
        
        # Conversation history affects responsiveness
        if conversation_count > 10:
            memory_animations["responsiveness"] = "highly_reactive"
            memory_animations["memory_flashes"] = "detailed_recall"
        elif conversation_count > 5:
            memory_animations["responsiveness"] = "moderately_reactive"
            memory_animations["memory_flashes"] = "basic_recall"
        else:
            memory_animations["responsiveness"] = "learning_mode"
            memory_animations["memory_flashes"] = "first_impressions"
        
        return memory_animations
    
    def _get_particle_config(self, character: str, emotion: str, intensity: float) -> Dict:
        """Get particle effect configuration"""
        profile = self.character_profiles[character]
        
        particle_config = {
            "type": profile["particle_type"],
            "count": int(20 + (intensity * 30)),
            "color": profile["base_color"],
            "secondary_color": profile["secondary_color"],
            "movement_pattern": emotion,
            "lifetime": 3 + intensity,
            "spawn_rate": intensity * 10
        }
        
        # Emotion-specific particle modifications
        if emotion == "excitement":
            particle_config["movement_pattern"] = "energetic_burst"
            particle_config["count"] *= 2
        elif emotion == "wisdom":
            particle_config["movement_pattern"] = "slow_orbit"
            particle_config["lifetime"] *= 1.5
        elif emotion == "curiosity":
            particle_config["movement_pattern"] = "searching_spiral"
        
        return particle_config
    
    def _get_gesture_patterns(self, character: str, emotion: str) -> List[str]:
        """Get gesture animation patterns"""
        profile = self.character_profiles[character]
        base_gestures = profile["gesture_patterns"]
        
        # Add emotion-specific gestures
        emotion_gestures = {
            "wisdom": ["thoughtful_pose", "knowledge_gesture"],
            "curiosity": ["head_tilt", "examining_motion"],
            "joy": ["celebratory_wave", "positive_energy"],
            "excitement": ["energetic_gesture", "rapid_movement"]
        }
        
        gestures = base_gestures.copy()
        if emotion in emotion_gestures:
            gestures.extend(emotion_gestures[emotion])
        
        return gestures
    
    def _calculate_animation_duration(self, intensity: float) -> float:
        """Calculate animation duration based on intensity"""
        base_duration = 2.0  # seconds
        intensity_factor = 0.5 + (intensity * 1.5)
        return base_duration * intensity_factor
    
    def generate_avatar_state(self, character: str, message: str, 
                            response: str, memory_context: Dict = None) -> Dict[str, Any]:
        """Generate complete avatar state for a conversation"""
        
        # Analyze emotions from both user message and AI response
        user_emotion = self.analyze_emotion_from_text(message, character)
        ai_emotion = self.analyze_emotion_from_text(response, character)
        
        # Combine emotions (AI response takes precedence)
        combined_emotion = ai_emotion.copy()
        combined_emotion["user_emotion"] = user_emotion["primary_emotion"]
        
        # Generate animation configuration
        animation_config = self.get_animation_config(character, combined_emotion, memory_context)
        
        # Create complete avatar state
        avatar_state = {
            "timestamp": datetime.now().isoformat(),
            "character": character,
            "emotion_analysis": {
                "user_emotion": user_emotion,
                "ai_emotion": ai_emotion,
                "combined": combined_emotion
            },
            "animation_config": animation_config,
            "memory_context": memory_context or {},
            "interaction_type": self._determine_interaction_type(message, response),
            "avatar_instructions": self._generate_avatar_instructions(animation_config)
        }
        
        return avatar_state
    
    def _determine_interaction_type(self, message: str, response: str) -> str:
        """Determine the type of interaction for specialized animations"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['question', 'how', 'what', 'why']):
            return "question_answer"
        elif any(word in message_lower for word in ['hello', 'hi', 'greetings']):
            return "greeting"
        elif any(word in message_lower for word in ['goodbye', 'bye', 'farewell']):
            return "farewell"
        elif any(word in message_lower for word in ['thank', 'thanks', 'appreciate']):
            return "gratitude"
        elif len(message) > 100:
            return "deep_conversation"
        else:
            return "casual_chat"
    
    def _generate_avatar_instructions(self, animation_config: Dict) -> Dict[str, Any]:
        """Generate specific instructions for frontend avatar rendering"""
        return {
            "facial_expression": {
                "emotion": animation_config["emotion"],
                "eye_glow": animation_config.get("eye_glow", "neutral_glow"),
                "intensity": animation_config["intensity"]
            },
            "body_animation": {
                "movement": animation_config.get("movement", "idle_breathing"),
                "gestures": animation_config.get("gestures", []),
                "duration": animation_config["duration"]
            },
            "aura_effects": {
                "pattern": animation_config.get("aura_pattern", "default_aura"),
                "color": animation_config["base_color"],
                "secondary_color": animation_config["secondary_color"],
                "energy_field": animation_config.get("energy_field", "ambient_field")
            },
            "particle_system": animation_config["particles"],
            "memory_indicators": {
                "bond_level": animation_config.get("bond_effects", "new_acquaintance"),
                "recognition": animation_config.get("recognition_glow", "curious_interest"),
                "memory_flash": animation_config.get("memory_flashes", "first_impressions")
            }
        }
    
    def get_idle_animation(self, character: str) -> Dict[str, Any]:
        """Get idle animation state when not in conversation"""
        profile = self.character_profiles[character]
        
        idle_state = {
            "character": character,
            "animation_type": "idle",
            "base_color": profile["base_color"],
            "secondary_color": profile["secondary_color"],
            "movement": "gentle_breathing",
            "aura": "ambient_glow",
            "particles": {
                "type": profile["particle_type"],
                "count": 10,
                "movement": "slow_drift"
            }
        }
        
        return idle_state
    
    def get_character_showcase(self) -> Dict[str, Any]:
        """Get showcase animations for all characters"""
        showcase = {}
        
        for character, profile in self.character_profiles.items():
            showcase[character] = {
                "name": character,
                "colors": {
                    "primary": profile["base_color"],
                    "secondary": profile["secondary_color"]
                },
                "animation_preview": {
                    "style": profile["animation_style"],
                    "signature_move": profile["gesture_patterns"][0],
                    "personality": profile["personality_traits"]
                },
                "preview_config": self.get_animation_config(
                    character, 
                    {"primary_emotion": profile["default_emotion"], "intensity": 0.7}
                )
            }
        
        return showcase
