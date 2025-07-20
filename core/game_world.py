"""
TEC: BITLYFE - GameWorld Core Class
The fundamental game world state manager - tracks all entities and locations
"""

from typing import Dict, List, Optional, Tuple, Set, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid

from .player import Player
from .npc import NPC


@dataclass
class Zone:
    """A zone/area in the game world"""
    zone_id: str
    name: str
    description: str
    biome_type: str = "neutral"  # forest, desert, mountain, city, etc.
    difficulty_level: int = 1
    connected_zones: List[str] = field(default_factory=list)
    spawn_points: List[Dict] = field(default_factory=list)


@dataclass
class Battle:
    """A battle instance between entities"""
    battle_id: str
    participants: List[str]  # Entity IDs (players/NPCs)
    battle_type: str  # pvp, pve, siege, etc.
    status: str = "active"  # active, completed, fled
    started_at: datetime = field(default_factory=datetime.now)
    ended_at: Optional[datetime] = None


class GameWorld:
    """
    Core GameWorld class - Manages the entire game state including all players, NPCs, and locations
    This is the central authority for the game world state
    """
    
    def __init__(self, world_name: str = "TEC: BITLYFE"):
        self.world_name = world_name
        self.created_at = datetime.now()
        self.last_updated = datetime.now()
        
        # Entity Management
        self.players: Dict[str, Player] = {}
        self.npcs: Dict[str, NPC] = {}
        self.online_players: Set[str] = set()
        
        # World Structure
        self.zones: Dict[str, Zone] = {}
        self.default_zone = "starting_area"
        
        # Active Systems
        self.active_battles: Dict[str, Battle] = {}
        self.active_quests: Dict[str, Dict] = {}
        self.world_events: List[Dict] = []
        
        # Global State
        self.world_level: int = 1  # Overall world difficulty
        self.global_reputation: Dict[str, int] = {}  # Faction reputations
        self.world_modifiers: Dict[str, Any] = {}  # Global effects
        
        # Initialize default zone
        self._create_default_zones()
    
    def _create_default_zones(self):
        """Create the initial game zones"""
        starting_area = Zone(
            zone_id="starting_area",
            name="The Nexus",
            description="A mystical crossroads where all journeys begin",
            biome_type="nexus",
            difficulty_level=1,
            spawn_points=[
                {"x": 0.0, "y": 0.0, "z": 0.0, "name": "Central Portal"}
            ]
        )
        self.zones["starting_area"] = starting_area
        
        # Add more zones
        forest_zone = Zone(
            zone_id="enchanted_forest",
            name="The Enchanted Forest",
            description="Ancient trees whisper secrets of old magic",
            biome_type="forest",
            difficulty_level=2,
            connected_zones=["starting_area"],
            spawn_points=[
                {"x": 100.0, "y": 0.0, "z": 0.0, "name": "Forest Entrance"}
            ]
        )
        self.zones["enchanted_forest"] = forest_zone
        
        # Connect zones
        self.zones["starting_area"].connected_zones.append("enchanted_forest")
    
    # Player Management
    def add_player(self, player: Player) -> bool:
        """Add a player to the world"""
        if player.player_id not in self.players:
            self.players[player.player_id] = player
            self.last_updated = datetime.now()
            return True
        return False
    
    def remove_player(self, player_id: str) -> bool:
        """Remove a player from the world"""
        if player_id in self.players:
            # Remove from online players if they're online
            self.online_players.discard(player_id)
            del self.players[player_id]
            self.last_updated = datetime.now()
            return True
        return False
    
    def get_player(self, player_id: str) -> Optional[Player]:
        """Get a player by ID"""
        return self.players.get(player_id)
    
    def player_login(self, player_id: str) -> bool:
        """Mark a player as online"""
        if player_id in self.players:
            self.online_players.add(player_id)
            self.players[player_id].last_active = datetime.now()
            return True
        return False
    
    def player_logout(self, player_id: str) -> bool:
        """Mark a player as offline"""
        if player_id in self.online_players:
            self.online_players.remove(player_id)
            if player_id in self.players:
                self.players[player_id].last_active = datetime.now()
            return True
        return False
    
    def get_online_players(self) -> List[Player]:
        """Get all currently online players"""
        return [self.players[pid] for pid in self.online_players if pid in self.players]
    
    def get_players_in_zone(self, zone_id: str) -> List[Player]:
        """Get all players in a specific zone"""
        return [player for player in self.players.values() 
                if player.location.zone == zone_id]
    
    # NPC Management
    def add_npc(self, npc: NPC) -> bool:
        """Add an NPC to the world"""
        if npc.npc_id not in self.npcs:
            self.npcs[npc.npc_id] = npc
            self.last_updated = datetime.now()
            return True
        return False
    
    def remove_npc(self, npc_id: str) -> bool:
        """Remove an NPC from the world"""
        if npc_id in self.npcs:
            del self.npcs[npc_id]
            self.last_updated = datetime.now()
            return True
        return False
    
    def get_npc(self, npc_id: str) -> Optional[NPC]:
        """Get an NPC by ID"""
        return self.npcs.get(npc_id)
    
    def get_npcs_in_zone(self, zone_id: str) -> List[NPC]:
        """Get all NPCs in a specific zone"""
        return [npc for npc in self.npcs.values() 
                if npc.location_zone == zone_id]
    
    def spawn_npc(self, npc_template: Dict, zone_id: str, x: float = 0.0, y: float = 0.0) -> str:
        """Spawn a new NPC from a template"""
        npc_id = str(uuid.uuid4())
        npc = NPC(npc_id, npc_template["name"], npc_template.get("type", "civilian"))
        
        # Apply template data
        if "personality" in npc_template:
            for trait, value in npc_template["personality"].items():
                setattr(npc.personality, trait, value)
        
        npc.update_location(zone_id, x, y)
        self.add_npc(npc)
        return npc_id
    
    # Zone Management
    def add_zone(self, zone: Zone) -> bool:
        """Add a zone to the world"""
        if zone.zone_id not in self.zones:
            self.zones[zone.zone_id] = zone
            self.last_updated = datetime.now()
            return True
        return False
    
    def get_zone(self, zone_id: str) -> Optional[Zone]:
        """Get a zone by ID"""
        return self.zones.get(zone_id)
    
    def get_connected_zones(self, zone_id: str) -> List[str]:
        """Get zones connected to the given zone"""
        zone = self.get_zone(zone_id)
        return zone.connected_zones if zone else []
    
    def can_travel_to_zone(self, from_zone: str, to_zone: str) -> bool:
        """Check if travel between zones is allowed"""
        zone = self.get_zone(from_zone)
        if zone:
            return to_zone in zone.connected_zones
        return False
    
    def move_player_to_zone(self, player_id: str, zone_id: str, x: float = 0.0, y: float = 0.0) -> bool:
        """Move a player to a different zone"""
        player = self.get_player(player_id)
        zone = self.get_zone(zone_id)
        
        if player and zone:
            # Check if movement is allowed
            if self.can_travel_to_zone(player.location.zone, zone_id) or zone_id == self.default_zone:
                player.update_location(zone_id, x, y)
                self.last_updated = datetime.now()
                return True
        return False
    
    # Battle System
    def start_battle(self, participants: List[str], battle_type: str = "pve") -> str:
        """Start a battle between entities"""
        battle_id = str(uuid.uuid4())
        battle = Battle(
            battle_id=battle_id,
            participants=participants,
            battle_type=battle_type
        )
        
        self.active_battles[battle_id] = battle
        
        # Mark participants as in battle
        for participant_id in participants:
            if participant_id in self.players:
                self.players[participant_id].enter_battle(battle_id)
            elif participant_id in self.npcs:
                self.npcs[participant_id].enter_battle(battle_id)
        
        self.last_updated = datetime.now()
        return battle_id
    
    def end_battle(self, battle_id: str, result: str = "completed") -> bool:
        """End a battle"""
        if battle_id in self.active_battles:
            battle = self.active_battles[battle_id]
            battle.status = result
            battle.ended_at = datetime.now()
            
            # Remove participants from battle
            for participant_id in battle.participants:
                if participant_id in self.players:
                    self.players[participant_id].exit_battle()
                elif participant_id in self.npcs:
                    self.npcs[participant_id].exit_battle()
            
            # Move to completed battles (could be stored separately)
            del self.active_battles[battle_id]
            self.last_updated = datetime.now()
            return True
        return False
    
    def get_battle(self, battle_id: str) -> Optional[Battle]:
        """Get a battle by ID"""
        return self.active_battles.get(battle_id)
    
    def get_player_battle(self, player_id: str) -> Optional[Battle]:
        """Get the battle a player is currently in"""
        player = self.get_player(player_id)
        if player and player.in_battle and player.battle_id:
            return self.get_battle(player.battle_id)
        return None
    
    # Proximity and Interaction
    def get_nearby_entities(self, zone_id: str, x: float, y: float, radius: float = 10.0) -> Dict:
        """Get all entities near a position"""
        nearby = {"players": [], "npcs": []}
        
        # Get nearby players
        for player in self.get_players_in_zone(zone_id):
            distance = ((player.location.x - x) ** 2 + (player.location.y - y) ** 2) ** 0.5
            if distance <= radius:
                nearby["players"].append({
                    "entity": player,
                    "distance": distance
                })
        
        # Get nearby NPCs
        for npc in self.get_npcs_in_zone(zone_id):
            distance = ((npc.x - x) ** 2 + (npc.y - y) ** 2) ** 0.5
            if distance <= radius:
                nearby["npcs"].append({
                    "entity": npc,
                    "distance": distance
                })
        
        return nearby
    
    def can_interact(self, entity1_id: str, entity2_id: str, max_distance: float = 5.0) -> bool:
        """Check if two entities can interact based on proximity"""
        # Get entities
        entity1 = self.get_player(entity1_id) or self.get_npc(entity1_id)
        entity2 = self.get_player(entity2_id) or self.get_npc(entity2_id)
        
        if not entity1 or not entity2:
            return False
        
        # Calculate distance and check zone
        if isinstance(entity1, Player):
            x1, y1 = entity1.location.x, entity1.location.y
            zone1 = entity1.location.zone
        else:  # NPC
            x1, y1 = entity1.x, entity1.y
            zone1 = entity1.location_zone
            
        if isinstance(entity2, Player):
            x2, y2 = entity2.location.x, entity2.location.y
            zone2 = entity2.location.zone
        else:  # NPC
            x2, y2 = entity2.x, entity2.y
            zone2 = entity2.location_zone
        
        # Check if in same zone
        if zone1 != zone2:
            return False
        
        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        return distance <= max_distance
    
    # World Events and State
    def add_world_event(self, event: Dict):
        """Add a world event to the timeline"""
        event['timestamp'] = datetime.now()
        self.world_events.append(event)
        
        # Keep only last 100 events
        if len(self.world_events) > 100:
            self.world_events = self.world_events[-100:]
    
    def get_world_state_summary(self) -> Dict:
        """Get a summary of the current world state"""
        return {
            "world_name": self.world_name,
            "world_level": self.world_level,
            "total_players": len(self.players),
            "online_players": len(self.online_players),
            "total_npcs": len(self.npcs),
            "total_zones": len(self.zones),
            "active_battles": len(self.active_battles),
            "active_quests": len(self.active_quests),
            "last_updated": self.last_updated.isoformat(),
            "created_at": self.created_at.isoformat()
        }
    
    def cleanup_inactive_entities(self, max_offline_hours: int = 24):
        """Clean up entities that have been inactive for too long"""
        cutoff_time = datetime.now() - timedelta(hours=max_offline_hours)
        
        # Clean up offline players (but don't delete them, just mark as inactive)
        inactive_players = []
        for player_id, player in self.players.items():
            if player.last_active < cutoff_time and player_id not in self.online_players:
                inactive_players.append(player_id)
        
        # For now, we'll just return the list of inactive players
        # In a real implementation, you might archive them or mark them as inactive
        return {
            "inactive_players": inactive_players,
            "cleanup_timestamp": datetime.now()
        }
