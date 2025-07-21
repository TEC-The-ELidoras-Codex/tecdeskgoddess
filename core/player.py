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
    energy: int = 100  # Renamed from mana for TEC consistency
    max_energy: int = 100
    
    # Combat stats
    attack: int = 10  # Renamed from strength for clarity
    defense: int = 10  # New defensive stat
    speed: int = 10  # Renamed from agility for clarity
    
    # TEC-specific stats
    consciousness: int = 10  # Digital awareness (renamed from intelligence)
    harmony: int = 10  # Musical/cosmic attunement (renamed from charisma)
    wisdom: int = 10  # Accumulated knowledge (new)


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
        
        # TEC character system
        self.selected_character = "polkin"  # Default persona
        self.character_affinity: Dict[str, int] = {
            "polkin": 50,
            "mynx": 30,
            "kaelen": 20,
            "airth": 40
        }
        
        # Ability system
        self.known_abilities: List[str] = []  # Ability IDs
        self.equipped_abilities: List[str] = ["basic_attack", "defend", "rest"]  # Up to 4 combat abilities
        
        # Battle system
        self.in_battle: bool = False
        self.battle_id: Optional[str] = None
        self.battle_history: List[Dict] = []
    
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
        self.stats.max_energy += 5
        self.stats.health = self.stats.max_health  # Full heal on level up
        self.stats.energy = self.stats.max_energy
        
        # Combat stat increases
        self.stats.attack += 2
        self.stats.defense += 2
        self.stats.speed += 1
        
        # Every 5 levels, increase TEC stats
        if self.stats.level % 5 == 0:
            self.stats.consciousness += 1
            self.stats.harmony += 1
            self.stats.wisdom += 1
    
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
    
    def use_energy(self, amount: int) -> bool:
        """
        Use energy for abilities
        Returns True if enough energy was available
        """
        if self.stats.energy >= amount:
            self.stats.energy -= amount
            return True
        return False
    
    def restore_energy(self, amount: int):
        """Restore energy"""
        self.stats.energy = min(self.stats.max_energy, self.stats.energy + amount)
    
    def learn_ability(self, ability_id: str) -> bool:
        """
        Learn a new ability
        Returns True if ability was learned successfully
        """
        if ability_id not in self.known_abilities:
            self.known_abilities.append(ability_id)
            return True
        return False
    
    def equip_ability(self, ability_id: str, slot: int) -> bool:
        """
        Equip an ability to a combat slot (0-3)
        Returns True if equipped successfully
        """
        if ability_id not in self.known_abilities and ability_id not in ["basic_attack", "defend", "rest"]:
            return False
        
        if slot < 0 or slot >= 4:
            return False
        
        # Ensure equipped_abilities has enough slots
        while len(self.equipped_abilities) <= slot:
            self.equipped_abilities.append("")
        
        self.equipped_abilities[slot] = ability_id
        return True
    
    def get_equipped_abilities(self) -> List[str]:
        """Get list of equipped ability IDs"""
        return [aid for aid in self.equipped_abilities if aid]
    
    def select_character(self, character: str) -> bool:
        """
        Select active character persona
        Returns True if character was selected successfully
        """
        if character in self.character_affinity:
            self.selected_character = character
            return True
        return False
    
    def increase_character_affinity(self, character: str, amount: int) -> None:
        """Increase affinity with a TEC character"""
        if character in self.character_affinity:
            self.character_affinity[character] = min(100, self.character_affinity[character] + amount)
    
    def add_battle_result(self, battle_result: Dict) -> None:
        """Add a battle result to history"""
        self.battle_history.append({
            'timestamp': datetime.now().isoformat(),
            'battle_id': battle_result.get('battle_id'),
            'result': battle_result.get('result'),  # won, lost, draw
            'experience_gained': battle_result.get('experience', 0),
            'opponent': battle_result.get('opponent', 'unknown')
        })
        
        # Keep only last 50 battles
        if len(self.battle_history) > 50:
            self.battle_history = self.battle_history[-50:]
    
    def get_battle_stats(self) -> Dict:
        """Get battle statistics"""
        if not self.battle_history:
            return {
                'total_battles': 0,
                'wins': 0,
                'losses': 0,
                'draws': 0,
                'win_rate': 0.0
            }
        
        wins = sum(1 for battle in self.battle_history if battle['result'] == 'won')
        losses = sum(1 for battle in self.battle_history if battle['result'] == 'lost')
        draws = sum(1 for battle in self.battle_history if battle['result'] == 'draw')
        total = len(self.battle_history)
        
        return {
            'total_battles': total,
            'wins': wins,
            'losses': losses,
            'draws': draws,
            'win_rate': (wins / total) * 100 if total > 0 else 0.0
        }
    
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
