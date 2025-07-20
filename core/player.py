"""
TEC: BITLYFE - Player Core Class
The fundamental Player entity - contains pure data and behavior logic
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PlayerStats:
    """Core player statistics"""
    level: int = 1
    experience: int = 0
    health: int = 100
    max_health: int = 100
    mana: int = 50
    max_mana: int = 50
    strength: int = 10
    agility: int = 10
    intelligence: int = 10
    charisma: int = 10


@dataclass
class PlayerLocation:
    """Player's current location in the game world"""
    zone: str = "starting_area"
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


class Player:
    """
    Core Player class - The fundamental representation of a player in TEC: BITLYFE
    This class contains only pure data and logic, no external dependencies
    """
    
    def __init__(self, player_id: str, name: str):
        self.player_id = player_id
        self.name = name
        self.stats = PlayerStats()
        self.location = PlayerLocation()
        self.inventory: List[str] = []  # Will hold item IDs
        self.active_quests: List[str] = []
        self.completed_quests: List[str] = []
        self.dialogue_history: Dict[str, List] = {}
        self.created_at = datetime.now()
        self.last_active = datetime.now()
        
        # RPG/Gamification elements
        self.biome_affinity: str = "neutral"
        self.reputation: Dict[str, int] = {}
        self.achievements: List[str] = []
        
        # Battle system
        self.in_battle: bool = False
        self.battle_id: Optional[str] = None
    
    def gain_experience(self, amount: int) -> bool:
        """
        Add experience points and handle level ups
        Returns True if player leveled up
        """
        self.stats.experience += amount
        return self._check_level_up()
    
    def _check_level_up(self) -> bool:
        """Check if player should level up and handle the level up"""
        required_exp = self._calculate_required_experience()
        if self.stats.experience >= required_exp:
            self.stats.level += 1
            self._apply_level_up_bonuses()
            return True
        return False
    
    def _calculate_required_experience(self) -> int:
        """Calculate experience required for next level"""
        # Simple exponential growth: level^2 * 100
        return (self.stats.level ** 2) * 100
    
    def _apply_level_up_bonuses(self):
        """Apply stat bonuses when leveling up"""
        # Base stat increases
        self.stats.max_health += 10
        self.stats.max_mana += 5
        self.stats.health = self.stats.max_health  # Full heal on level up
        self.stats.mana = self.stats.max_mana
        
        # Every 5 levels, increase core stats
        if self.stats.level % 5 == 0:
            self.stats.strength += 1
            self.stats.agility += 1
            self.stats.intelligence += 1
            self.stats.charisma += 1
    
    def take_damage(self, amount: int) -> bool:
        """
        Apply damage to player
        Returns True if player is still alive
        """
        self.stats.health = max(0, self.stats.health - amount)
        return self.stats.health > 0
    
    def heal(self, amount: int):
        """Heal the player"""
        self.stats.health = min(self.stats.max_health, self.stats.health + amount)
    
    def use_mana(self, amount: int) -> bool:
        """
        Use mana for abilities
        Returns True if enough mana was available
        """
        if self.stats.mana >= amount:
            self.stats.mana -= amount
            return True
        return False
    
    def restore_mana(self, amount: int):
        """Restore mana"""
        self.stats.mana = min(self.stats.max_mana, self.stats.mana + amount)
    
    def add_item(self, item_id: str):
        """Add an item to inventory"""
        self.inventory.append(item_id)
    
    def remove_item(self, item_id: str) -> bool:
        """Remove an item from inventory, returns True if successful"""
        if item_id in self.inventory:
            self.inventory.remove(item_id)
            return True
        return False
    
    def has_item(self, item_id: str) -> bool:
        """Check if player has a specific item"""
        return item_id in self.inventory
    
    def start_quest(self, quest_id: str):
        """Start a new quest"""
        if quest_id not in self.active_quests and quest_id not in self.completed_quests:
            self.active_quests.append(quest_id)
    
    def complete_quest(self, quest_id: str) -> bool:
        """Complete a quest, returns True if successful"""
        if quest_id in self.active_quests:
            self.active_quests.remove(quest_id)
            self.completed_quests.append(quest_id)
            return True
        return False
    
    def update_location(self, zone: str, x: Optional[float] = None, y: Optional[float] = None, z: Optional[float] = None):
        """Update player's location"""
        self.location.zone = zone
        if x is not None:
            self.location.x = x
        if y is not None:
            self.location.y = y
        if z is not None:
            self.location.z = z
    
    def add_dialogue_entry(self, npc_id: str, dialogue_entry: Dict):
        """Add a dialogue entry to history"""
        if npc_id not in self.dialogue_history:
            self.dialogue_history[npc_id] = []
        self.dialogue_history[npc_id].append(dialogue_entry)
    
    def get_dialogue_history(self, npc_id: str) -> List:
        """Get dialogue history with a specific NPC"""
        return self.dialogue_history.get(npc_id, [])
    
    def is_alive(self) -> bool:
        """Check if player is alive"""
        return self.stats.health > 0
    
    def enter_battle(self, battle_id: str):
        """Enter battle state"""
        self.in_battle = True
        self.battle_id = battle_id
    
    def exit_battle(self):
        """Exit battle state"""
        self.in_battle = False
        self.battle_id = None
    
    def to_dict(self) -> Dict:
        """Convert player to dictionary for serialization"""
        return {
            'player_id': self.player_id,
            'name': self.name,
            'stats': {
                'level': self.stats.level,
                'experience': self.stats.experience,
                'health': self.stats.health,
                'max_health': self.stats.max_health,
                'mana': self.stats.mana,
                'max_mana': self.stats.max_mana,
                'strength': self.stats.strength,
                'agility': self.stats.agility,
                'intelligence': self.stats.intelligence,
                'charisma': self.stats.charisma
            },
            'location': {
                'zone': self.location.zone,
                'x': self.location.x,
                'y': self.location.y,
                'z': self.location.z
            },
            'inventory': self.inventory,
            'active_quests': self.active_quests,
            'completed_quests': self.completed_quests,
            'biome_affinity': self.biome_affinity,
            'reputation': self.reputation,
            'achievements': self.achievements,
            'in_battle': self.in_battle,
            'battle_id': self.battle_id,
            'created_at': self.created_at.isoformat(),
            'last_active': self.last_active.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Player':
        """Create player from dictionary"""
        player = cls(data['player_id'], data['name'])
        
        # Restore stats
        stats_data = data['stats']
        player.stats.level = stats_data['level']
        player.stats.experience = stats_data['experience']
        player.stats.health = stats_data['health']
        player.stats.max_health = stats_data['max_health']
        player.stats.mana = stats_data['mana']
        player.stats.max_mana = stats_data['max_mana']
        player.stats.strength = stats_data['strength']
        player.stats.agility = stats_data['agility']
        player.stats.intelligence = stats_data['intelligence']
        player.stats.charisma = stats_data['charisma']
        
        # Restore location
        location_data = data['location']
        player.location.zone = location_data['zone']
        player.location.x = location_data['x']
        player.location.y = location_data['y']
        player.location.z = location_data['z']
        
        # Restore other data
        player.inventory = data['inventory']
        player.active_quests = data['active_quests']
        player.completed_quests = data['completed_quests']
        player.biome_affinity = data['biome_affinity']
        player.reputation = data['reputation']
        player.achievements = data['achievements']
        player.in_battle = data['in_battle']
        player.battle_id = data['battle_id']
        
        # Restore timestamps
        player.created_at = datetime.fromisoformat(data['created_at'])
        player.last_active = datetime.fromisoformat(data['last_active'])
        
        return player
