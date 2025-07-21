"""
TEC: BITLYFE - NPC Service
Handles all NPC-related business logic, AI behavior, and interactions
"""

from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import uuid
import logging
import random

from ..core.npc import NPC, NPCPersonality
from ..core.game_world import GameWorld
from .mcp_service import MCPService

logger = logging.getLogger(__name__)


class NPCService:
    """
    NPC Service - Manages all NPC-related operations and AI behavior
    This service orchestrates NPC interactions, dialogue generation, and AI behavior
    """
    
    def __init__(self, game_world: GameWorld, mcp_service: MCPService):
        self.game_world = game_world
        self.mcp_service = mcp_service
        self.npc_templates = self._initialize_npc_templates()
        self.dialogue_cache = {}  # Cache recent AI responses
        self.behavior_timers = {}  # Track NPC behavior cycles
    
    def _initialize_npc_templates(self) -> Dict:
        """Initialize templates for different NPC types"""
        return {
            "merchant": {
                "personality": {
                    "friendliness": 70,
                    "aggression": 20,
                    "curiosity": 50,
                    "is_merchant": True
                },
                "names": ["Trader Gareth", "Merchant Elena", "Shopkeeper Boris", "Vendor Aria"],
                "dialogue_style": "business-focused, friendly but profit-minded",
                "inventory": ["health_potion", "mana_potion", "iron_sword", "leather_armor"]
            },
            "guard": {
                "personality": {
                    "friendliness": 40,
                    "aggression": 70,
                    "loyalty": 90,
                    "is_hostile": False
                },
                "names": ["Guard Captain Rex", "Sentinel Maya", "Watchman Cole", "Defender Zara"],
                "dialogue_style": "authoritative, protective, law-focused",
                "patrol_behavior": True
            },
            "sage": {
                "personality": {
                    "friendliness": 60,
                    "intelligence": 95,
                    "curiosity": 85,
                    "is_quest_giver": True
                },
                "names": ["Elder Wisdom", "Sage Merlin", "Oracle Cassandra", "Scholar Thane"],
                "dialogue_style": "wise, cryptic, knowledge-focused",
                "quest_types": ["knowledge", "exploration", "mystery"]
            },
            "villager": {
                "personality": {
                    "friendliness": 60,
                    "curiosity": 40,
                    "aggression": 10
                },
                "names": ["Farmer Joe", "Baker Sarah", "Miller Tom", "Weaver Luna"],
                "dialogue_style": "simple, humble, community-focused",
                "gossip_knowledge": True
            },
            "warrior": {
                "personality": {
                    "friendliness": 50,
                    "aggression": 80,
                    "loyalty": 70
                },
                "names": ["Knight Valor", "Warrior Grim", "Champion Lyra", "Berserker Thorg"],
                "dialogue_style": "direct, honor-focused, battle-minded",
                "challenge_behavior": True
            }
        }
    
    def spawn_npc(self, npc_type: str, zone_id: str, x: float = 0.0, y: float = 0.0, 
                  custom_name: Optional[str] = None) -> Tuple[bool, str, Optional[str]]:
        """
        Spawn a new NPC of the specified type
        Returns (success, message, npc_id)
        """
        try:
            if npc_type not in self.npc_templates:
                return False, f"Unknown NPC type: {npc_type}", None
            
            template = self.npc_templates[npc_type]
            
            # Generate NPC ID and name
            npc_id = f"{npc_type}_{uuid.uuid4().hex[:8]}"
            name = custom_name or random.choice(template["names"])
            
            # Create the NPC
            npc = NPC(npc_id, name, npc_type)
            
            # Apply template personality
            for trait, value in template["personality"].items():
                if hasattr(npc.personality, trait):
                    setattr(npc.personality, trait, value)
            
            # Set location
            npc.update_location(zone_id, x, y)
            
            # Add template-specific items
            if "inventory" in template:
                for item in template["inventory"]:
                    item_id = f"{item}_{uuid.uuid4().hex[:8]}"
                    npc.add_item(item_id)
                    if npc.personality.is_merchant:
                        npc.shop_inventory.append(item_id)
            
            # Add to game world
            if self.game_world.add_npc(npc):
                logger.info(f"Spawned {npc_type} NPC: {name} at {zone_id}")
                return True, f"Spawned {name} the {npc_type}", npc_id
            else:
                return False, "Failed to add NPC to game world", None
                
        except Exception as e:
            logger.error(f"Error spawning NPC {npc_type}: {e}")
            return False, f"Error spawning NPC: {e}", None
    
    async def handle_player_interaction(self, player_id: str, npc_id: str, 
                                       interaction_type: str = "talk", 
                                       message: str = "") -> Tuple[bool, str, Dict]:
        """
        Handle interaction between a player and NPC
        Returns (success, response_message, interaction_data)
        """
        try:
            # Get entities
            player = self.game_world.get_player(player_id)
            npc = self.game_world.get_npc(npc_id)
            
            if not player:
                return False, "Player not found", {}
            if not npc:
                return False, "NPC not found", {}
            
            # Check if interaction is possible
            if not self.game_world.can_interact(player_id, npc_id):
                return False, "You are too far away to interact", {}
            
            # Process the interaction
            interaction_result = npc.interact_with_player(player_id, interaction_type)
            
            # Generate AI response for dialogue
            if interaction_type == "talk":
                ai_response = await self._generate_npc_dialogue(npc, player, message)
                response_message = ai_response.get("content", "I have nothing to say.")
                
                # Store dialogue in NPC's history
                npc.add_dialogue_entry(player_id, message, response_message)
                
                # Check for mood changes based on conversation
                self._update_npc_mood_from_interaction(npc, player, message, ai_response)
                
            elif interaction_type == "trade":
                success, response_message = self._handle_trade_interaction(player, npc)
                if not success:
                    return False, response_message, {}
                    
            elif interaction_type == "challenge":
                success, response_message = self._handle_challenge_interaction(player, npc)
                if not success:
                    return False, response_message, {}
                    
            else:
                response_message = f"{npc.name} acknowledges your {interaction_type}."
            
            # Update interaction data
            interaction_data = {
                "npc_id": npc_id,
                "npc_name": npc.name,
                "interaction_type": interaction_type,
                "player_message": message,
                "npc_response": response_message,
                "relationship_level": npc.get_relationship_level(player_id),
                "relationship_score": npc.get_relationship(player_id),
                "npc_mood": npc.current_mood,
                "available_actions": self._get_available_npc_actions(npc, player)
            }
            
            return True, response_message, interaction_data
            
        except Exception as e:
            logger.error(f"Error handling interaction between {player_id} and {npc_id}: {e}")
            return False, f"Interaction error: {e}", {}
    
    async def _generate_npc_dialogue(self, npc: NPC, player, message: str) -> Dict:
        """Generate AI-powered dialogue for the NPC"""
        try:
            # Check cache first (for very recent identical messages)
            cache_key = f"{npc.npc_id}_{hash(message)}"
            if cache_key in self.dialogue_cache:
                cached_response = self.dialogue_cache[cache_key]
                if (datetime.now() - cached_response["timestamp"]).seconds < 60:  # 1 minute cache
                    return cached_response["response"]
            
            # Prepare NPC data for AI
            npc_data = npc.get_ai_prompt_data(player.player_id)
            conversation_context = npc.get_dialogue_context(player.player_id)
            
            # Call MCP service to generate dialogue
            ai_response = await self.mcp_service.generate_npc_dialogue(
                npc_data, message, conversation_context
            )
            
            # Cache the response
            self.dialogue_cache[cache_key] = {
                "timestamp": datetime.now(),
                "response": ai_response
            }
            
            # Clean old cache entries
            self._clean_dialogue_cache()
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Error generating NPC dialogue: {e}")
            return {
                "success": False,
                "content": "I seem to be having trouble speaking right now...",
                "error": str(e)
            }
    
    def _update_npc_mood_from_interaction(self, npc: NPC, player, message: str, ai_response: Dict):
        """Update NPC mood based on the interaction"""
        # Simple mood logic based on message sentiment and relationship
        relationship_score = npc.get_relationship(player.player_id)
        
        # Positive interactions
        if any(word in message.lower() for word in ["help", "please", "thank", "appreciate"]):
            if relationship_score > 50:
                npc.update_mood("happy", "positive interaction with friend")
            else:
                npc.update_mood("pleased", "polite interaction")
        
        # Negative interactions
        elif any(word in message.lower() for word in ["stupid", "hate", "idiot", "useless"]):
            if relationship_score < -20:
                npc.update_mood("angry", "hostile interaction")
            else:
                npc.update_mood("annoyed", "rude interaction")
        
        # Questioning/curious interactions
        elif "?" in message or any(word in message.lower() for word in ["what", "how", "why", "where"]):
            if npc.personality.curiosity > 60:
                npc.update_mood("curious", "interesting question asked")
    
    def _handle_trade_interaction(self, player, npc: NPC) -> Tuple[bool, str]:
        """Handle trade interactions with merchant NPCs"""
        if not npc.personality.is_merchant:
            return False, f"{npc.name} is not a merchant."
        
        if not npc.shop_inventory:
            return False, f"{npc.name} has nothing to sell right now."
        
        # For now, return available items (full trade system would be more complex)
        item_list = ", ".join(npc.shop_inventory[:5])  # Show first 5 items
        return True, f"{npc.name} offers: {item_list}. What would you like to buy?"
    
    def _handle_challenge_interaction(self, player, npc: NPC) -> Tuple[bool, str]:
        """Handle challenge/battle interactions"""
        if npc.personality.is_hostile:
            return True, f"{npc.name} accepts your challenge! Prepare for battle!"
        
        relationship = npc.get_relationship(player.player_id)
        if relationship < -20:
            return True, f"{npc.name} is angry enough to fight you!"
        
        if hasattr(npc, 'challenge_behavior') and npc.npc_type == "warrior":
            return True, f"{npc.name} grins and accepts your challenge to honorable combat!"
        
        return False, f"{npc.name} has no interest in fighting you."
    
    def _get_available_npc_actions(self, npc: NPC, player) -> List[str]:
        """Get available actions for this NPC interaction"""
        actions = ["talk"]
        
        if npc.personality.is_merchant and npc.shop_inventory:
            actions.append("trade")
        
        if npc.personality.is_quest_giver and npc.available_quests:
            actions.append("get_quest")
        
        # Battle actions
        if (npc.personality.is_hostile or 
            npc.get_relationship(player.player_id) < -20 or 
            npc.npc_type == "warrior"):
            actions.append("challenge")
        
        return actions
    
    def get_npc_quest(self, player_id: str, npc_id: str) -> Tuple[bool, str, Optional[Dict]]:
        """Get a quest from a quest-giving NPC"""
        try:
            npc = self.game_world.get_npc(npc_id)
            if not npc:
                return False, "NPC not found", None
            
            if not npc.personality.is_quest_giver:
                return False, f"{npc.name} doesn't give quests", None
            
            if not npc.available_quests:
                return False, f"{npc.name} has no quests available right now", None
            
            # Get first available quest
            quest_id = npc.available_quests[0]
            
            # Generate quest details (in full implementation, these would come from a quest system)
            quest_data = {
                "quest_id": quest_id,
                "title": f"Quest from {npc.name}",
                "description": f"A mysterious task given by {npc.name}",
                "objectives": ["Complete the assigned task"],
                "rewards": {"experience": 100, "gold": 50},
                "difficulty": "normal"
            }
            
            # Remove quest from NPC's available list and give to player
            if npc.give_quest(quest_id, player_id):
                return True, f"{npc.name} has given you a quest!", quest_data
            else:
                return False, "Failed to assign quest", None
                
        except Exception as e:
            logger.error(f"Error getting quest from NPC {npc_id}: {e}")
            return False, f"Error getting quest: {e}", None
    
    def update_npc_behavior(self, npc_id: str) -> bool:
        """Update NPC's AI behavior (called periodically)"""
        try:
            npc = self.game_world.get_npc(npc_id)
            if not npc:
                return False
            
            # Simple behavior patterns
            current_time = datetime.now()
            
            # Mood decay - NPCs gradually return to neutral mood
            if npc.current_mood != "neutral":
                last_mood_change = npc.last_interaction_time or current_time
                if (current_time - last_mood_change).total_seconds() > 300:  # 5 minutes
                    npc.update_mood("neutral", "mood naturally faded")
            
            # Random mood changes for more dynamic NPCs
            if random.random() < 0.01:  # 1% chance per update
                moods = ["happy", "sad", "excited", "thoughtful", "restless"]
                new_mood = random.choice(moods)
                npc.update_mood(new_mood, "random mood shift")
            
            # Goal updates based on NPC type
            if npc.npc_type == "merchant" and npc.current_goal == "idle":
                npc.set_goal("seeking_customers")
            elif npc.npc_type == "guard" and npc.current_goal == "idle":
                npc.set_goal("patrolling")
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating NPC behavior for {npc_id}: {e}")
            return False
    
    def get_npcs_in_zone(self, zone_id: str) -> List[Dict]:
        """Get all NPCs in a specific zone with their status"""
        try:
            npcs = self.game_world.get_npcs_in_zone(zone_id)
            npc_data = []
            
            for npc in npcs:
                npc_info = {
                    "npc_id": npc.npc_id,
                    "name": npc.name,
                    "type": npc.npc_type,
                    "mood": npc.current_mood,
                    "goal": npc.current_goal,
                    "position": {"x": npc.x, "y": npc.y},
                    "can_trade": npc.personality.is_merchant,
                    "has_quests": len(npc.available_quests) > 0,
                    "is_hostile": npc.personality.is_hostile
                }
                npc_data.append(npc_info)
            
            return npc_data
            
        except Exception as e:
            logger.error(f"Error getting NPCs in zone {zone_id}: {e}")
            return []
    
    def _clean_dialogue_cache(self):
        """Clean old entries from dialogue cache"""
        current_time = datetime.now()
        keys_to_remove = []
        
        for key, cached_data in self.dialogue_cache.items():
            if (current_time - cached_data["timestamp"]).total_seconds() > 300:  # 5 minutes
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.dialogue_cache[key]
    
    def get_npc_status(self, npc_id: str) -> Tuple[bool, str, Optional[Dict]]:
        """Get detailed status of an NPC"""
        try:
            npc = self.game_world.get_npc(npc_id)
            if not npc:
                return False, "NPC not found", None
            
            status = {
                "basic_info": {
                    "name": npc.name,
                    "type": npc.npc_type,
                    "level": npc.stats.level,
                    "health": f"{npc.stats.health}/{npc.stats.max_health}"
                },
                "personality": {
                    "friendliness": npc.personality.friendliness,
                    "aggression": npc.personality.aggression,
                    "curiosity": npc.personality.curiosity,
                    "intelligence": npc.personality.intelligence
                },
                "current_state": {
                    "mood": npc.current_mood,
                    "goal": npc.current_goal,
                    "location": f"{npc.location_zone} ({npc.x}, {npc.y})",
                    "in_battle": npc.in_battle
                },
                "capabilities": {
                    "is_merchant": npc.personality.is_merchant,
                    "is_quest_giver": npc.personality.is_quest_giver,
                    "shop_items": len(npc.shop_inventory),
                    "available_quests": len(npc.available_quests)
                },
                "social": {
                    "total_relationships": len(npc.relationships),
                    "memory_entries": len(npc.memory),
                    "last_interaction": npc.last_interaction_time.isoformat() if npc.last_interaction_time else None
                }
            }
            
            return True, "NPC status retrieved", status
            
        except Exception as e:
            logger.error(f"Error getting NPC status for {npc_id}: {e}")
            return False, f"Error retrieving status: {e}", None
    
    def populate_zone_with_npcs(self, zone_id: str, npc_count: int = 5) -> List[str]:
        """Populate a zone with random NPCs"""
        spawned_npcs = []
        
        try:
            zone = self.game_world.get_zone(zone_id)
            if not zone:
                return spawned_npcs
            
            # Determine NPC types based on zone biome
            npc_weights = self._get_npc_weights_for_biome(zone.biome_type)
            
            for i in range(npc_count):
                # Choose random NPC type based on weights
                npc_type = random.choices(
                    list(npc_weights.keys()),
                    weights=list(npc_weights.values())
                )[0]
                
                # Random position within zone
                x = random.uniform(-50, 50)
                y = random.uniform(-50, 50)
                
                success, message, npc_id = self.spawn_npc(npc_type, zone_id, x, y)
                if success and npc_id:
                    spawned_npcs.append(npc_id)
            
            logger.info(f"Populated {zone_id} with {len(spawned_npcs)} NPCs")
            return spawned_npcs
            
        except Exception as e:
            logger.error(f"Error populating zone {zone_id} with NPCs: {e}")
            return spawned_npcs
    
    def _get_npc_weights_for_biome(self, biome_type: str) -> Dict[str, float]:
        """Get NPC type weights based on biome"""
        weights = {
            "forest": {"villager": 0.4, "sage": 0.2, "merchant": 0.2, "guard": 0.1, "warrior": 0.1},
            "city": {"merchant": 0.3, "guard": 0.3, "villager": 0.2, "sage": 0.1, "warrior": 0.1},
            "mountain": {"warrior": 0.3, "sage": 0.2, "guard": 0.2, "villager": 0.2, "merchant": 0.1},
            "desert": {"merchant": 0.3, "warrior": 0.3, "sage": 0.2, "guard": 0.1, "villager": 0.1},
            "nexus": {"merchant": 0.2, "guard": 0.2, "sage": 0.2, "villager": 0.2, "warrior": 0.2}
        }
        
        return weights.get(biome_type, weights["nexus"])
