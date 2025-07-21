"""
TEC: BITLYFE - Player Service
Handles all player-related business logic and operations
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import uuid
import logging

from ..core.player import Player
from ..core.game_world import GameWorld

logger = logging.getLogger(__name__)


class PlayerService:
    """
    Player Service - Manages all player-related operations
    This service orchestrates player creation, progression, and interactions
    """
    
    def __init__(self, game_world: GameWorld):
        self.game_world = game_world
        self.experience_tables = self._initialize_experience_tables()
        self.level_rewards = self._initialize_level_rewards()
    
    def _initialize_experience_tables(self) -> Dict:
        """Initialize experience requirements for different activities"""
        return {
            "combat": {"kill_enemy": 50, "win_battle": 100, "perfect_battle": 150},
            "social": {"complete_dialogue": 10, "make_friend": 25, "help_npc": 30},
            "exploration": {"discover_location": 20, "find_secret": 75, "complete_area": 100},
            "crafting": {"craft_item": 15, "enhance_item": 25, "create_legendary": 200},
            "quests": {"complete_quest": 100, "complete_epic_quest": 500}
        }
    
    def _initialize_level_rewards(self) -> Dict:
        """Initialize rewards for reaching certain levels"""
        return {
            5: {"title": "Novice Adventurer", "item": "iron_sword"},
            10: {"title": "Experienced Explorer", "item": "magic_cloak"},
            15: {"title": "Seasoned Warrior", "item": "enchanted_armor"},
            20: {"title": "Master Adventurer", "item": "legendary_weapon"},
            25: {"title": "Hero of TEC", "item": "mythic_artifact"}
        }
    
    def create_player(self, player_id: str, name: str, starting_zone: str = None) -> Tuple[bool, str, Optional[Player]]:
        """
        Create a new player and add them to the game world
        Returns (success, message, player_object)
        """
        try:
            # Check if player already exists
            if self.game_world.get_player(player_id):
                return False, "Player already exists", None
            
            # Validate name
            if not name or len(name.strip()) < 2:
                return False, "Player name must be at least 2 characters", None
            
            if len(name) > 20:
                return False, "Player name cannot exceed 20 characters", None
            
            # Create the player
            player = Player(player_id, name.strip())
            
            # Set starting location
            start_zone = starting_zone or self.game_world.default_zone
            if start_zone in self.game_world.zones:
                zone = self.game_world.zones[start_zone]
                spawn_point = zone.spawn_points[0] if zone.spawn_points else {"x": 0.0, "y": 0.0, "z": 0.0}
                player.update_location(start_zone, spawn_point.get("x", 0.0), spawn_point.get("y", 0.0), spawn_point.get("z", 0.0))
            
            # Give starting items
            self._give_starting_items(player)
            
            # Add to game world
            if self.game_world.add_player(player):
                logger.info(f"Created new player: {name} ({player_id})")
                return True, f"Welcome to TEC: BITLYFE, {name}!", player
            else:
                return False, "Failed to add player to game world", None
                
        except Exception as e:
            logger.error(f"Error creating player {name}: {e}")
            return False, f"Error creating player: {e}", None
    
    def _give_starting_items(self, player: Player):
        """Give new players their starting equipment"""
        starting_items = [
            "basic_sword",
            "leather_armor", 
            "health_potion",
            "traveler_cloak",
            "journal"
        ]
        
        for item_id in starting_items:
            player.add_item(f"{item_id}_{uuid.uuid4().hex[:8]}")
    
    def player_login(self, player_id: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Handle player login
        Returns (success, message, player_data)
        """
        try:
            player = self.game_world.get_player(player_id)
            if not player:
                return False, "Player not found", None
            
            # Mark as online
            self.game_world.player_login(player_id)
            player.last_active = datetime.now()
            
            # Get player status
            player_data = {
                "player": player.to_dict(),
                "location_info": self._get_location_info(player),
                "nearby_entities": self._get_nearby_entities(player),
                "active_effects": self._get_active_effects(player),
                "available_actions": self._get_available_actions(player)
            }
            
            logger.info(f"Player {player.name} logged in")
            return True, f"Welcome back, {player.name}!", player_data
            
        except Exception as e:
            logger.error(f"Error during player login {player_id}: {e}")
            return False, f"Login error: {e}", None
    
    def player_logout(self, player_id: str) -> Tuple[bool, str]:
        """Handle player logout"""
        try:
            player = self.game_world.get_player(player_id)
            if player:
                player.last_active = datetime.now()
                self.game_world.player_logout(player_id)
                logger.info(f"Player {player.name} logged out")
                return True, "Goodbye!"
            return False, "Player not found"
            
        except Exception as e:
            logger.error(f"Error during player logout {player_id}: {e}")
            return False, f"Logout error: {e}"
    
    def award_experience(self, player_id: str, activity_type: str, activity: str, amount: Optional[int] = None) -> Tuple[bool, str, bool]:
        """
        Award experience to a player
        Returns (success, message, leveled_up)
        """
        try:
            player = self.game_world.get_player(player_id)
            if not player:
                return False, "Player not found", False
            
            # Calculate experience amount
            if amount is None:
                exp_table = self.experience_tables.get(activity_type, {})
                amount = exp_table.get(activity, 10)  # Default 10 exp
            
            # Apply any multipliers
            amount = self._apply_experience_multipliers(player, amount, activity_type)
            
            # Award the experience
            leveled_up = player.gain_experience(amount)
            
            message = f"Gained {amount} experience"
            if leveled_up:
                message += f" and reached level {player.stats.level}!"
                self._handle_level_up(player)
            else:
                exp_needed = player._calculate_required_experience() - player.stats.experience
                message += f" ({exp_needed} needed for next level)"
            
            logger.info(f"Player {player.name} gained {amount} exp from {activity_type}:{activity}")
            return True, message, leveled_up
            
        except Exception as e:
            logger.error(f"Error awarding experience to {player_id}: {e}")
            return False, f"Error awarding experience: {e}", False
    
    def _apply_experience_multipliers(self, player: Player, base_amount: int, activity_type: str) -> int:
        """Apply various multipliers to experience gains"""
        multiplier = 1.0
        
        # Biome affinity bonus
        if activity_type == "exploration" and player.biome_affinity != "neutral":
            multiplier += 0.1
        
        # Low level bonus (help new players catch up)
        if player.stats.level < 10:
            multiplier += 0.2
        
        # Weekend bonus (if it's weekend)
        if datetime.now().weekday() >= 5:  # Saturday or Sunday
            multiplier += 0.1
        
        return int(base_amount * multiplier)
    
    def _handle_level_up(self, player: Player):
        """Handle level up rewards and notifications"""
        level = player.stats.level
        
        # Check for level rewards
        if level in self.level_rewards:
            reward = self.level_rewards[level]
            
            # Give title
            if "title" in reward:
                if "titles" not in player.achievements:
                    player.achievements.append("titles")
                # In a full implementation, you'd have a titles system
            
            # Give item
            if "item" in reward:
                item_id = f"{reward['item']}_{uuid.uuid4().hex[:8]}"
                player.add_item(item_id)
        
        # Every 5 levels, increase biome affinity options
        if level % 5 == 0 and level > 5:
            # Player can choose a new biome affinity
            pass  # This would trigger a choice UI
    
    def move_player(self, player_id: str, target_zone: str, x: float = 0.0, y: float = 0.0) -> Tuple[bool, str]:
        """Move a player to a new location"""
        try:
            player = self.game_world.get_player(player_id)
            if not player:
                return False, "Player not found"
            
            # Check if player can move (not in battle, etc.)
            if player.in_battle:
                return False, "Cannot move while in battle"
            
            # Attempt to move
            if self.game_world.move_player_to_zone(player_id, target_zone, x, y):
                zone = self.game_world.get_zone(target_zone)
                message = f"Traveled to {zone.name if zone else target_zone}"
                
                # Award exploration experience
                self.award_experience(player_id, "exploration", "discover_location")
                
                return True, message
            else:
                return False, "Cannot travel to that location"
                
        except Exception as e:
            logger.error(f"Error moving player {player_id}: {e}")
            return False, f"Movement error: {e}"
    
    def use_item(self, player_id: str, item_id: str, target_id: Optional[str] = None) -> Tuple[bool, str, Dict]:
        """Handle player using an item"""
        try:
            player = self.game_world.get_player(player_id)
            if not player:
                return False, "Player not found", {}
            
            if not player.has_item(item_id):
                return False, "You don't have that item", {}
            
            # For now, simulate item use (in full implementation, get Item object)
            item_effects = {
                "health_gained": 0,
                "mana_gained": 0,
                "buffs_applied": [],
                "item_consumed": False
            }
            
            # Simple item effects simulation
            if "health_potion" in item_id:
                heal_amount = 25
                player.heal(heal_amount)
                player.remove_item(item_id)
                item_effects["health_gained"] = heal_amount
                item_effects["item_consumed"] = True
                message = f"Used health potion, restored {heal_amount} health"
            elif "mana_potion" in item_id:
                mana_amount = 20
                player.restore_mana(mana_amount)
                player.remove_item(item_id)
                item_effects["mana_gained"] = mana_amount
                item_effects["item_consumed"] = True
                message = f"Used mana potion, restored {mana_amount} mana"
            else:
                message = f"Used {item_id}"
            
            return True, message, item_effects
            
        except Exception as e:
            logger.error(f"Error using item {item_id} for player {player_id}: {e}")
            return False, f"Error using item: {e}", {}
    
    def start_quest(self, player_id: str, quest_id: str) -> Tuple[bool, str]:
        """Start a quest for a player"""
        try:
            player = self.game_world.get_player(player_id)
            if not player:
                return False, "Player not found"
            
            # Check if quest is already active or completed
            if quest_id in player.active_quests:
                return False, "Quest is already active"
            
            if quest_id in player.completed_quests:
                return False, "Quest is already completed"
            
            # Start the quest
            player.start_quest(quest_id)
            
            # Award experience for accepting quest
            self.award_experience(player_id, "quests", "accept_quest", 10)
            
            return True, f"Quest {quest_id} started!"
            
        except Exception as e:
            logger.error(f"Error starting quest {quest_id} for player {player_id}: {e}")
            return False, f"Error starting quest: {e}"
    
    def complete_quest(self, player_id: str, quest_id: str) -> Tuple[bool, str, Dict]:
        """Complete a quest for a player"""
        try:
            player = self.game_world.get_player(player_id)
            if not player:
                return False, "Player not found", {}
            
            if quest_id not in player.active_quests:
                return False, "Quest is not active", {}
            
            # Complete the quest
            player.complete_quest(quest_id)
            
            # Award experience and rewards
            exp_reward = 100  # Base quest experience
            self.award_experience(player_id, "quests", "complete_quest", exp_reward)
            
            # Quest rewards (simplified)
            rewards = {
                "experience": exp_reward,
                "gold": 50,
                "items": [],
                "reputation": {}
            }
            
            return True, f"Quest {quest_id} completed!", rewards
            
        except Exception as e:
            logger.error(f"Error completing quest {quest_id} for player {player_id}: {e}")
            return False, f"Error completing quest: {e}", {}
    
    def _get_location_info(self, player: Player) -> Dict:
        """Get information about the player's current location"""
        zone = self.game_world.get_zone(player.location.zone)
        if zone:
            return {
                "zone_id": zone.zone_id,
                "zone_name": zone.name,
                "description": zone.description,
                "biome": zone.biome_type,
                "difficulty": zone.difficulty_level,
                "connected_zones": zone.connected_zones
            }
        return {}
    
    def _get_nearby_entities(self, player: Player) -> Dict:
        """Get entities near the player"""
        nearby = self.game_world.get_nearby_entities(
            player.location.zone, 
            player.location.x, 
            player.location.y
        )
        
        return {
            "players": [{"id": p["entity"].player_id, "name": p["entity"].name, "distance": p["distance"]} 
                       for p in nearby["players"]],
            "npcs": [{"id": n["entity"].npc_id, "name": n["entity"].name, "distance": n["distance"]} 
                    for n in nearby["npcs"]]
        }
    
    def _get_active_effects(self, player: Player) -> List[Dict]:
        """Get active effects on the player"""
        effects = []
        
        # Add any temporary effects (buffs, debuffs, etc.)
        # This would be expanded in a full implementation
        
        return effects
    
    def _get_available_actions(self, player: Player) -> List[str]:
        """Get available actions for the player"""
        actions = ["move", "inventory", "stats"]
        
        if player.in_battle:
            actions.extend(["attack", "defend", "use_skill", "flee"])
        else:
            actions.extend(["explore", "rest"])
        
        # Check for nearby NPCs
        nearby = self._get_nearby_entities(player)
        if nearby["npcs"]:
            actions.append("talk")
        
        if nearby["players"]:
            actions.extend(["trade", "challenge"])
        
        return actions
    
    def get_player_stats(self, player_id: str) -> Tuple[bool, str, Optional[Dict]]:
        """Get detailed player statistics"""
        try:
            player = self.game_world.get_player(player_id)
            if not player:
                return False, "Player not found", None
            
            stats = {
                "basic_info": {
                    "name": player.name,
                    "level": player.stats.level,
                    "experience": player.stats.experience,
                    "next_level_exp": player._calculate_required_experience()
                },
                "combat_stats": {
                    "health": f"{player.stats.health}/{player.stats.max_health}",
                    "mana": f"{player.stats.mana}/{player.stats.max_mana}",
                    "strength": player.stats.strength,
                    "agility": player.stats.agility,
                    "intelligence": player.stats.intelligence,
                    "charisma": player.stats.charisma
                },
                "progression": {
                    "active_quests": len(player.active_quests),
                    "completed_quests": len(player.completed_quests),
                    "achievements": len(player.achievements),
                    "biome_affinity": player.biome_affinity
                },
                "inventory": {
                    "item_count": len(player.inventory),
                    "items": player.inventory[:10]  # Show first 10 items
                }
            }
            
            return True, "Player stats retrieved", stats
            
        except Exception as e:
            logger.error(f"Error getting stats for player {player_id}: {e}")
            return False, f"Error retrieving stats: {e}", None
    
    def get_leaderboard(self, category: str = "level", limit: int = 10) -> List[Dict]:
        """Get leaderboard data"""
        try:
            all_players = list(self.game_world.players.values())
            
            if category == "level":
                sorted_players = sorted(all_players, key=lambda p: p.stats.level, reverse=True)
            elif category == "experience":
                sorted_players = sorted(all_players, key=lambda p: p.stats.experience, reverse=True)
            else:
                sorted_players = all_players
            
            leaderboard = []
            for i, player in enumerate(sorted_players[:limit]):
                leaderboard.append({
                    "rank": i + 1,
                    "name": player.name,
                    "level": player.stats.level,
                    "experience": player.stats.experience,
                    "biome_affinity": player.biome_affinity
                })
            
            return leaderboard
            
        except Exception as e:
            logger.error(f"Error generating leaderboard: {e}")
            return []
