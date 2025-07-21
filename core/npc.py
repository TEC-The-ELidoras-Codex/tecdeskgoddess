"""
TEC: BITLYFE - NPC Core Class
The fundamental NPC entity - contains pure AI behavior and personality logic
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class NPCPersonality:
    """Core NPC personality traits"""
    friendliness: int = 50  # 0-100 scale
    aggression: int = 50
    curiosity: int = 50
    loyalty: int = 50
    intelligence: int = 50
    humor: int = 50
    
    # Special traits
    is_merchant: bool = False
    is_quest_giver: bool = False
    is_hostile: bool = False
    is_ally: bool = False


@dataclass
class NPCStats:
    """NPC combat and interaction stats"""
    level: int = 1
    health: int = 100
    max_health: int = 100
    energy: int = 80  # NPCs generally have less energy than players
    max_energy: int = 80
    
    # Combat stats
    attack: int = 10
    defense: int = 10
    speed: int = 10
    
    # TEC-specific stats
    consciousness: int = 5  # Most NPCs have lower consciousness
    harmony: int = 5
    wisdom: int = 5


class NPC:
    """
    Core NPC class - The fundamental representation of an AI character in TEC: BITLYFE
    This class contains personality, dialogue state, and behavior logic
    """
    
    def __init__(self, npc_id: str, name: str, npc_type: str = "civilian"):
        self.npc_id = npc_id
        self.name = name
        self.npc_type = npc_type  # civilian, merchant, guard, quest_giver, boss, etc.
        self.personality = NPCPersonality()
        self.stats = NPCStats()
        
        # AI Behavior State
        self.current_mood: str = "neutral"  # happy, sad, angry, excited, etc.
        self.current_goal: str = "idle"  # What the NPC is currently trying to do
        self.memory: List[Dict] = []  # Short-term memory of recent interactions
        self.relationships: Dict[str, int] = {}  # player_id -> relationship score (-100 to 100)
        
        # Dialogue System
        self.dialogue_history: Dict[str, List] = {}  # player_id -> conversation history
        self.conversation_context: Dict[str, Any] = {}  # Current conversation state
        self.last_spoken_to: Optional[str] = None
        self.last_interaction_time: Optional[datetime] = None
        
        # Location and Movement
        self.location_zone: str = "starting_area"
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0
        self.patrol_route: List[Dict] = []  # List of waypoints for movement
        self.home_location: Dict = {"zone": "starting_area", "x": 0.0, "y": 0.0, "z": 0.0}
        
        # Inventory and Items
        self.inventory: List[str] = []  # item IDs
        self.shop_inventory: List[str] = []  # For merchant NPCs
        self.loot_table: List[str] = []  # Items dropped when defeated
        
        # Quest and Mission Data
        self.available_quests: List[str] = []
        self.completed_quests_given: List[str] = []
        
        # Battle System
        self.in_battle: bool = False
        self.battle_id: Optional[str] = None
        self.combat_behavior: str = "defensive"  # aggressive, defensive, support, flee
        
        # Ability System
        self.abilities: List[str] = ["basic_attack", "defend"]  # Default NPC abilities
        self.ai_ability_priority: List[str] = []  # Preferred ability order for AI
        
        # Metadata
        self.created_at = datetime.now()
        self.last_active = datetime.now()
        self.spawn_rate: float = 1.0  # How often this NPC should appear
        self.is_unique: bool = False  # Is this a unique, named character?
    
    def interact_with_player(self, player_id: str, interaction_type: str = "talk") -> Dict:
        """
        Process an interaction with a player
        Returns interaction result data
        """
        self.last_spoken_to = player_id
        self.last_interaction_time = datetime.now()
        
        # Update relationship based on interaction
        self._update_relationship(player_id, interaction_type)
        
        # Add to memory
        memory_entry = {
            "player_id": player_id,
            "type": interaction_type,
            "timestamp": datetime.now(),
            "mood": self.current_mood
        }
        self.memory.append(memory_entry)
        
        # Keep only last 10 memories
        if len(self.memory) > 10:
            self.memory = self.memory[-10:]
        
        return {
            "npc_id": self.npc_id,
            "interaction_type": interaction_type,
            "relationship_level": self.get_relationship(player_id),
            "mood": self.current_mood,
            "can_trade": self.personality.is_merchant,
            "has_quests": len(self.available_quests) > 0
        }
    
    def _update_relationship(self, player_id: str, interaction_type: str):
        """Update relationship score based on interaction"""
        if player_id not in self.relationships:
            self.relationships[player_id] = 0
        
        # Different interactions affect relationship differently
        if interaction_type == "talk":
            self.relationships[player_id] += 1
        elif interaction_type == "give_gift":
            self.relationships[player_id] += 5
        elif interaction_type == "attack":
            self.relationships[player_id] -= 10
        elif interaction_type == "help":
            self.relationships[player_id] += 3
        elif interaction_type == "trade":
            self.relationships[player_id] += 2
        
        # Cap relationship at -100 to 100
        self.relationships[player_id] = max(-100, min(100, self.relationships[player_id]))
    
    def get_relationship(self, player_id: str) -> int:
        """Get relationship score with a player"""
        return self.relationships.get(player_id, 0)
    
    def get_relationship_level(self, player_id: str) -> str:
        """Get descriptive relationship level"""
        score = self.get_relationship(player_id)
        if score >= 80:
            return "beloved"
        elif score >= 60:
            return "trusted"
        elif score >= 40:
            return "friendly"
        elif score >= 20:
            return "acquainted"
        elif score >= -20:
            return "neutral"
        elif score >= -40:
            return "disliked"
        elif score >= -60:
            return "hostile"
        else:
            return "enemy"
    
    def add_dialogue_entry(self, player_id: str, player_message: str, npc_response: str):
        """Add a dialogue exchange to history"""
        if player_id not in self.dialogue_history:
            self.dialogue_history[player_id] = []
        
        dialogue_entry = {
            "timestamp": datetime.now(),
            "player_message": player_message,
            "npc_response": npc_response,
            "mood": self.current_mood,
            "relationship": self.get_relationship(player_id)
        }
        
        self.dialogue_history[player_id].append(dialogue_entry)
        
        # Keep only last 20 dialogue entries per player
        if len(self.dialogue_history[player_id]) > 20:
            self.dialogue_history[player_id] = self.dialogue_history[player_id][-20:]
    
    def get_dialogue_context(self, player_id: str) -> Dict:
        """Get conversation context for AI generation"""
        recent_history = self.dialogue_history.get(player_id, [])[-5:]  # Last 5 exchanges
        
        return {
            "npc_name": self.name,
            "npc_type": self.npc_type,
            "personality": {
                "friendliness": self.personality.friendliness,
                "aggression": self.personality.aggression,
                "curiosity": self.personality.curiosity,
                "humor": self.personality.humor
            },
            "current_mood": self.current_mood,
            "relationship_level": self.get_relationship_level(player_id),
            "relationship_score": self.get_relationship(player_id),
            "recent_dialogue": recent_history,
            "available_quests": self.available_quests,
            "is_merchant": self.personality.is_merchant,
            "location": f"{self.location_zone} ({self.x}, {self.y})"
        }
    
    def update_mood(self, new_mood: str, reason: str = ""):
        """Update the NPC's current mood"""
        old_mood = self.current_mood
        self.current_mood = new_mood
        
        # Add mood change to memory
        mood_memory = {
            "type": "mood_change",
            "old_mood": old_mood,
            "new_mood": new_mood,
            "reason": reason,
            "timestamp": datetime.now()
        }
        self.memory.append(mood_memory)
    
    def set_goal(self, goal: str):
        """Set the NPC's current goal/objective"""
        self.current_goal = goal
    
    def update_location(self, zone: str, x: float, y: float, z: float = 0.0):
        """Update NPC's location"""
        self.location_zone = zone
        self.x = x
        self.y = y
        self.z = z
    
    def add_item(self, item_id: str):
        """Add an item to NPC's inventory"""
        self.inventory.append(item_id)
    
    def remove_item(self, item_id: str) -> bool:
        """Remove an item from inventory"""
        if item_id in self.inventory:
            self.inventory.remove(item_id)
            return True
        return False
    
    def has_item(self, item_id: str) -> bool:
        """Check if NPC has a specific item"""
        return item_id in self.inventory
    
    def add_quest(self, quest_id: str):
        """Add a quest that this NPC can give"""
        if quest_id not in self.available_quests:
            self.available_quests.append(quest_id)
    
    def give_quest(self, quest_id: str, player_id: str) -> bool:
        """Give a quest to a player"""
        if quest_id in self.available_quests:
            self.available_quests.remove(quest_id)
            self.completed_quests_given.append(quest_id)
            return True
        return False
    
    def take_damage(self, amount: int) -> bool:
        """Apply damage to NPC, returns True if still alive"""
        self.stats.health = max(0, self.stats.health - amount)
        if self.stats.health <= 0:
            self.current_mood = "defeated"
        return self.stats.health > 0
    
    def heal(self, amount: int):
        """Heal the NPC"""
        self.stats.health = min(self.stats.max_health, self.stats.health + amount)
    
    def is_alive(self) -> bool:
        """Check if NPC is alive"""
        return self.stats.health > 0
    
    def enter_battle(self, battle_id: str):
        """Enter battle state"""
        self.in_battle = True
        self.battle_id = battle_id
        self.current_mood = "combat"
    
    def exit_battle(self):
        """Exit battle state"""
        self.in_battle = False
        self.battle_id = None
        if self.is_alive():
            self.current_mood = "neutral"
    
    def get_ai_prompt_data(self, player_id: str) -> Dict:
        """Get data formatted for AI model prompts"""
        return {
            "npc_profile": {
                "name": self.name,
                "type": self.npc_type,
                "level": self.stats.level,
                "personality_traits": {
                    "friendliness": self.personality.friendliness,
                    "aggression": self.personality.aggression,
                    "curiosity": self.personality.curiosity,
                    "loyalty": self.personality.loyalty,
                    "intelligence": self.personality.intelligence,
                    "humor": self.personality.humor
                },
                "special_roles": {
                    "is_merchant": self.personality.is_merchant,
                    "is_quest_giver": self.personality.is_quest_giver,
                    "is_hostile": self.personality.is_hostile
                }
            },
            "current_state": {
                "mood": self.current_mood,
                "goal": self.current_goal,
                "location": f"{self.location_zone}",
                "health_percentage": (self.stats.health / self.stats.max_health) * 100
            },
            "player_relationship": {
                "score": self.get_relationship(player_id),
                "level": self.get_relationship_level(player_id)
            },
            "conversation_context": self.get_dialogue_context(player_id),
            "available_actions": {
                "can_trade": self.personality.is_merchant and len(self.shop_inventory) > 0,
                "has_quests": len(self.available_quests) > 0,
                "can_battle": not self.personality.is_hostile or self.get_relationship(player_id) < -20
            }
        }
    
    def to_dict(self) -> Dict:
        """Convert NPC to dictionary for serialization"""
        return {
            'npc_id': self.npc_id,
            'name': self.name,
            'npc_type': self.npc_type,
            'personality': {
                'friendliness': self.personality.friendliness,
                'aggression': self.personality.aggression,
                'curiosity': self.personality.curiosity,
                'loyalty': self.personality.loyalty,
                'intelligence': self.personality.intelligence,
                'humor': self.personality.humor,
                'is_merchant': self.personality.is_merchant,
                'is_quest_giver': self.personality.is_quest_giver,
                'is_hostile': self.personality.is_hostile,
                'is_ally': self.personality.is_ally
            },
            'stats': {
                'level': self.stats.level,
                'health': self.stats.health,
                'max_health': self.stats.max_health,
                'strength': self.stats.strength,
                'agility': self.stats.agility,
                'intelligence': self.stats.intelligence,
                'charisma': self.stats.charisma
            },
            'current_mood': self.current_mood,
            'current_goal': self.current_goal,
            'location': {
                'zone': self.location_zone,
                'x': self.x,
                'y': self.y,
                'z': self.z
            },
            'relationships': self.relationships,
            'inventory': self.inventory,
            'shop_inventory': self.shop_inventory,
            'available_quests': self.available_quests,
            'in_battle': self.in_battle,
            'battle_id': self.battle_id,
            'created_at': self.created_at.isoformat(),
            'last_active': self.last_active.isoformat()
        }
