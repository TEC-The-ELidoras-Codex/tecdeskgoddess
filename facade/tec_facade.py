"""
TEC: BITLYFE - Game Facade
The main interface that the UI layer communicates with
This hides all the complexity of the Service and Core layers
"""

import asyncio
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import logging

from ..core.game_world import GameWorld
from ..services.player_service import PlayerService
from ..services.npc_service import NPCService
from ..services.mcp_service import MCPService

logger = logging.getLogger(__name__)


class GameFacade:
    """
    Game Facade - The single entry point for all game operations
    This provides a simple, clean API that the UI layer can use
    """
    
    def __init__(self):
        # Initialize core systems
        self.game_world = GameWorld("TEC: BITLYFE")
        self.mcp_service = MCPService()
        self.player_service = PlayerService(self.game_world)
        self.npc_service = NPCService(self.game_world, self.mcp_service)
        
        # Game state
        self.is_initialized = False
        self.battle_system_active = False
        
        logger.info("Game Facade initialized")
    
    async def initialize_game(self) -> Dict:
        """Initialize the game world and systems"""
        try:
            # Populate starting areas with NPCs
            starting_npcs = self.npc_service.populate_zone_with_npcs("starting_area", 3)
            forest_npcs = self.npc_service.populate_zone_with_npcs("enchanted_forest", 5)
            
            self.is_initialized = True
            
            return {
                "success": True,
                "message": "TEC: BITLYFE world initialized",
                "world_state": self.get_world_state(),
                "spawned_npcs": {
                    "starting_area": starting_npcs,
                    "enchanted_forest": forest_npcs
                }
            }
            
        except Exception as e:
            logger.error(f"Error initializing game: {e}")
            return {
                "success": False,
                "message": f"Failed to initialize game: {e}"
            }
    
    # === PLAYER OPERATIONS ===
    
    def create_player(self, player_id: str, name: str) -> Dict:
        """Create a new player"""
        success, message, player = self.player_service.create_player(player_id, name)
        
        response = {
            "success": success,
            "message": message,
            "player_data": player.to_dict() if player else None
        }
        
        if success:
            # Auto-login the new player
            self.player_login(player_id)
            
        return response
    
    def player_login(self, player_id: str) -> Dict:
        """Handle player login"""
        success, message, player_data = self.player_service.player_login(player_id)
        
        return {
            "success": success,
            "message": message,
            "player_data": player_data,
            "world_state": self.get_world_state() if success else None
        }
    
    def player_logout(self, player_id: str) -> Dict:
        """Handle player logout"""
        success, message = self.player_service.player_logout(player_id)
        
        return {
            "success": success,
            "message": message
        }
    
    def get_player_state(self, player_id: str) -> Dict:
        """Get current player state and nearby information"""
        player = self.game_world.get_player(player_id)
        if not player:
            return {"success": False, "message": "Player not found"}
        
        # Get comprehensive player state
        success, message, stats = self.player_service.get_player_stats(player_id)
        if not success:
            return {"success": False, "message": message}
        
        # Get nearby entities and location info
        location_info = self.player_service._get_location_info(player)
        nearby_entities = self.player_service._get_nearby_entities(player)
        available_actions = self.player_service._get_available_actions(player)
        
        return {
            "success": True,
            "player_stats": stats,
            "location": location_info,
            "nearby": nearby_entities,
            "available_actions": available_actions,
            "current_battle": self.get_player_battle_state(player_id) if player.in_battle else None
        }
    
    def move_player(self, player_id: str, target_zone: str, x: float = 0.0, y: float = 0.0) -> Dict:
        """Move player to a new location"""
        success, message = self.player_service.move_player(player_id, target_zone, x, y)
        
        response = {
            "success": success,
            "message": message
        }
        
        if success:
            response["new_state"] = self.get_player_state(player_id)
        
        return response
    
    def use_item(self, player_id: str, item_id: str, target_id: Optional[str] = None) -> Dict:
        """Use an item"""
        success, message, effects = self.player_service.use_item(player_id, item_id, target_id)
        
        return {
            "success": success,
            "message": message,
            "effects": effects,
            "updated_state": self.get_player_state(player_id) if success else None
        }
    
    # === NPC INTERACTIONS ===
    
    async def talk_to_npc(self, player_id: str, npc_id: str, message: str) -> Dict:
        """Handle player talking to an NPC"""
        success, response, interaction_data = await self.npc_service.handle_player_interaction(
            player_id, npc_id, "talk", message
        )
        
        result = {
            "success": success,
            "npc_response": response,
            "interaction_data": interaction_data
        }
        
        if success:
            # Award social experience
            self.player_service.award_experience(player_id, "social", "complete_dialogue")
        
        return result
    
    async def trade_with_npc(self, player_id: str, npc_id: str) -> Dict:
        """Handle trading with an NPC"""
        success, response, interaction_data = await self.npc_service.handle_player_interaction(
            player_id, npc_id, "trade"
        )
        
        return {
            "success": success,
            "message": response,
            "trade_data": interaction_data
        }
    
    def get_quest_from_npc(self, player_id: str, npc_id: str) -> Dict:
        """Get a quest from an NPC"""
        success, message, quest_data = self.npc_service.get_npc_quest(player_id, npc_id)
        
        response = {
            "success": success,
            "message": message,
            "quest_data": quest_data
        }
        
        if success and quest_data:
            # Start the quest for the player
            self.player_service.start_quest(player_id, quest_data["quest_id"])
        
        return response
    
    async def challenge_npc(self, player_id: str, npc_id: str) -> Dict:
        """Challenge an NPC to battle"""
        success, response, interaction_data = await self.npc_service.handle_player_interaction(
            player_id, npc_id, "challenge"
        )
        
        if success:
            # Start battle
            battle_result = self.start_battle([player_id, npc_id], "pve")
            return {
                "success": True,
                "message": response,
                "battle_started": battle_result["success"],
                "battle_data": battle_result.get("battle_data")
            }
        
        return {
            "success": False,
            "message": response
        }
    
    # === BATTLE SYSTEM ===
    
    def start_battle(self, participants: List[str], battle_type: str = "pve") -> Dict:
        """Start a battle between entities"""
        try:
            battle_id = self.game_world.start_battle(participants, battle_type)
            
            # Generate epic battle description
            battle_data = {
                "participants": participants,
                "type": battle_type,
                "location": "mystical battlefield"
            }
            
            # Get battle description (sync call for now, could be async)
            description = "An epic battle begins!"
            
            self.battle_system_active = True
            
            return {
                "success": True,
                "message": "Battle started!",
                "battle_data": {
                    "battle_id": battle_id,
                    "participants": participants,
                    "type": battle_type,
                    "description": description,
                    "status": "active"
                }
            }
            
        except Exception as e:
            logger.error(f"Error starting battle: {e}")
            return {
                "success": False,
                "message": f"Failed to start battle: {e}"
            }
    
    def get_player_battle_state(self, player_id: str) -> Optional[Dict]:
        """Get the current battle state for a player"""
        battle = self.game_world.get_player_battle(player_id)
        if not battle:
            return None
        
        return {
            "battle_id": battle.battle_id,
            "participants": battle.participants,
            "type": battle.battle_type,
            "status": battle.status,
            "started_at": battle.started_at.isoformat()
        }
    
    def perform_battle_action(self, player_id: str, action: str, target_id: Optional[str] = None) -> Dict:
        """Perform a battle action"""
        player = self.game_world.get_player(player_id)
        if not player or not player.in_battle:
            return {"success": False, "message": "Not in battle"}
        
        # Simple battle action processing (would be much more complex in full implementation)
        if action == "attack":
            if target_id:
                target = self.game_world.get_player(target_id) or self.game_world.get_npc(target_id)
                if target:
                    damage = 20  # Simple damage calculation
                    if hasattr(target, 'take_damage'):
                        alive = target.take_damage(damage)
                        message = f"Attacked {getattr(target, 'name', target_id)} for {damage} damage"
                        
                        if not alive:
                            message += f" and defeated them!"
                            # Award experience for victory
                            self.player_service.award_experience(player_id, "combat", "kill_enemy")
                            
                            # End battle if one participant is defeated
                            if player.battle_id:
                                self.end_battle(player.battle_id, "victory")
                        
                        return {"success": True, "message": message}
            
            return {"success": False, "message": "No valid target"}
        
        elif action == "flee":
            if player.battle_id:
                self.end_battle(player.battle_id, "fled")
                return {"success": True, "message": "You fled from battle!"}
            else:
                return {"success": False, "message": "Not in a valid battle"}
        
        return {"success": False, "message": "Unknown battle action"}
    
    def end_battle(self, battle_id: str, result: str = "completed") -> Dict:
        """End a battle"""
        success = self.game_world.end_battle(battle_id, result)
        
        if success:
            self.battle_system_active = len(self.game_world.active_battles) > 0
        
        return {
            "success": success,
            "message": f"Battle ended: {result}"
        }
    
    # === QUEST SYSTEM ===
    
    def start_quest(self, player_id: str, quest_id: str) -> Dict:
        """Start a quest"""
        success, message = self.player_service.start_quest(player_id, quest_id)
        
        return {
            "success": success,
            "message": message
        }
    
    def complete_quest(self, player_id: str, quest_id: str) -> Dict:
        """Complete a quest"""
        success, message, rewards = self.player_service.complete_quest(player_id, quest_id)
        
        return {
            "success": success,
            "message": message,
            "rewards": rewards,
            "updated_state": self.get_player_state(player_id) if success else None
        }
    
    # === WORLD STATE ===
    
    def get_world_state(self) -> Dict:
        """Get current world state summary"""
        return self.game_world.get_world_state_summary()
    
    def get_zone_info(self, zone_id: str) -> Dict:
        """Get detailed information about a zone"""
        zone = self.game_world.get_zone(zone_id)
        if not zone:
            return {"success": False, "message": "Zone not found"}
        
        # Get NPCs in zone
        npcs = self.npc_service.get_npcs_in_zone(zone_id)
        players = self.game_world.get_players_in_zone(zone_id)
        
        return {
            "success": True,
            "zone": {
                "id": zone.zone_id,
                "name": zone.name,
                "description": zone.description,
                "biome": zone.biome_type,
                "difficulty": zone.difficulty_level,
                "connected_zones": zone.connected_zones
            },
            "npcs": npcs,
            "players": [{"id": p.player_id, "name": p.name, "level": p.stats.level} for p in players],
            "spawn_points": zone.spawn_points
        }
    
    def get_leaderboard(self, category: str = "level") -> Dict:
        """Get leaderboard data"""
        leaderboard = self.player_service.get_leaderboard(category)
        
        return {
            "success": True,
            "category": category,
            "leaderboard": leaderboard
        }
    
    # === AI AND MCP STATUS ===
    
    def get_ai_status(self) -> Dict:
        """Get AI service status"""
        return {
            "success": True,
            "mcp_status": self.mcp_service.get_service_status()
        }
    
    def switch_ai_provider(self, provider_name: str) -> Dict:
        """Switch AI provider"""
        success = self.mcp_service.set_provider(provider_name)
        
        return {
            "success": success,
            "message": f"Switched to {provider_name}" if success else f"Failed to switch to {provider_name}",
            "current_provider": self.mcp_service.current_provider
        }
    
    def enable_local_ai(self, model_path: str) -> Dict:
        """Enable local AI model"""
        success = self.mcp_service.enable_local_model(model_path)
        
        return {
            "success": success,
            "message": "Local AI enabled" if success else "Failed to enable local AI"
        }
    
    # === UTILITY METHODS ===
    
    def process_chat_command(self, player_id: str, command: str) -> Dict:
        """Process a chat command from the player"""
        command = command.strip().lower()
        
        if command.startswith("/"):
            # Handle slash commands
            parts = command[1:].split()
            cmd = parts[0] if parts else ""
            
            if cmd == "help":
                return {
                    "success": True,
                    "message": "Available commands: /stats, /location, /nearby, /quests, /inventory",
                    "type": "system"
                }
            
            elif cmd == "stats":
                state = self.get_player_state(player_id)
                if state["success"]:
                    stats = state["player_stats"]["basic_info"]
                    return {
                        "success": True,
                        "message": f"Level {stats['level']} - {stats['experience']}/{stats['next_level_exp']} XP",
                        "type": "system"
                    }
            
            elif cmd == "location":
                state = self.get_player_state(player_id)
                if state["success"]:
                    loc = state["location"]
                    return {
                        "success": True,
                        "message": f"Current location: {loc['zone_name']} ({loc['biome']} biome)",
                        "type": "system"
                    }
            
            elif cmd == "nearby":
                state = self.get_player_state(player_id)
                if state["success"]:
                    nearby = state["nearby"]
                    npcs = [npc["name"] for npc in nearby["npcs"]]
                    players = [p["name"] for p in nearby["players"]]
                    
                    message = "Nearby: "
                    if npcs:
                        message += f"NPCs: {', '.join(npcs)}"
                    if players:
                        message += f" Players: {', '.join(players)}"
                    if not npcs and not players:
                        message += "No one around"
                    
                    return {
                        "success": True,
                        "message": message,
                        "type": "system"
                    }
            
            return {
                "success": False,
                "message": f"Unknown command: {cmd}",
                "type": "error"
            }
        
        else:
            # Regular chat message
            return {
                "success": True,
                "message": f"You say: {command}",
                "type": "chat"
            }
    
    def get_status_summary(self) -> Dict:
        """Get a comprehensive status summary of the game"""
        world_state = self.get_world_state()
        ai_status = self.get_ai_status()
        
        return {
            "game_initialized": self.is_initialized,
            "world_state": world_state,
            "ai_status": ai_status,
            "battle_system_active": self.battle_system_active,
            "timestamp": datetime.now().isoformat()
        }
