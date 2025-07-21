"""
TEC: BITLYFE - Battle Service Layer
Business logic for combat encounters in the Astradigital Arena
"""

from typing import Dict, List, Optional, Any, Union
import uuid
import random
import asyncio
from datetime import datetime

from ..core.battle import Battle, BattleType, BattleState, BattleParticipant
from ..core.player import Player
from ..core.npc import NPC
from ..core.ability import Ability, AbilityLibrary
from .mcp_service import MCPService


class BattleService:
    """
    Service layer for managing battles in TEC: BITLYFE
    Handles battle creation, progression, AI decisions, and result processing
    """
    
    def __init__(self, mcp_service: Optional[MCPService] = None):
        self.active_battles: Dict[str, Battle] = {}
        self.battle_templates: Dict[str, Dict[str, Any]] = {}
        self.mcp_service = mcp_service
        
        # Load ability libraries
        self.tec_abilities = {ability.ability_id: ability for ability in AbilityLibrary.create_tec_abilities()}
        self.basic_abilities = {ability.ability_id: ability for ability in AbilityLibrary.create_basic_abilities()}
        self.all_abilities = {**self.tec_abilities, **self.basic_abilities}
        
        # Initialize battle templates
        self._initialize_battle_templates()
    
    def _initialize_battle_templates(self) -> None:
        """Initialize predefined battle encounters"""
        self.battle_templates = {
            "tutorial_first_battle": {
                "name": "First Steps in the Arena",
                "description": "A gentle introduction to combat in the Astradigital Arena",
                "enemies": [
                    {
                        "name": "Training Construct",
                        "type": "tutorial_dummy",
                        "health": 50,
                        "energy": 30,
                        "abilities": ["basic_attack"],
                        "ai_behavior": "passive"
                    }
                ],
                "rewards": {
                    "experience": 25,
                    "abilities": [],
                    "achievements": ["first_battle"]
                }
            },
            "shadow_beast_encounter": {
                "name": "Shadow in the Data Stream",
                "description": "A corrupted data entity blocks your path",
                "enemies": [
                    {
                        "name": "Shadow Beast",
                        "type": "data_corruption",
                        "health": 80,
                        "energy": 60,
                        "abilities": ["basic_attack", "data_corruption"],
                        "ai_behavior": "aggressive"
                    }
                ],
                "rewards": {
                    "experience": 50,
                    "abilities": ["mynx_firewall_breach"],
                    "achievements": ["data_warrior"]
                }
            },
            "cosmic_trial": {
                "name": "Trial of Cosmic Wisdom",
                "description": "Face the cosmic forces that test your understanding",
                "enemies": [
                    {
                        "name": "Cosmic Guardian",
                        "type": "cosmic_entity",
                        "health": 120,
                        "energy": 100,
                        "abilities": ["basic_attack", "defend", "stellar_wisdom"],
                        "ai_behavior": "strategic"
                    }
                ],
                "rewards": {
                    "experience": 75,
                    "abilities": ["kaelen_stellar_wisdom"],
                    "achievements": ["cosmic_initiate"]
                }
            }
        }
    
    async def create_battle(self, battle_type: BattleType, template_id: Optional[str] = None, 
                          custom_config: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a new battle
        
        Args:
            battle_type: Type of battle to create
            template_id: ID of predefined battle template
            custom_config: Custom battle configuration
            
        Returns:
            Battle ID
        """
        battle_id = str(uuid.uuid4())
        battle = Battle(battle_id, battle_type)
        
        # Apply template configuration
        if template_id and template_id in self.battle_templates:
            template = self.battle_templates[template_id]
            battle.battle_name = template["name"]
            battle.battle_description = template["description"]
            
            # Create enemy NPCs from template
            for enemy_config in template["enemies"]:
                enemy_npc = self._create_enemy_from_config(enemy_config)
                battle.add_participant(enemy_npc)
        
        # Apply custom configuration
        if custom_config:
            if "max_turns" in custom_config:
                battle.max_turns = custom_config["max_turns"]
            if "auto_energy_regen" in custom_config:
                battle.auto_energy_regen = custom_config["auto_energy_regen"]
        
        self.active_battles[battle_id] = battle
        return battle_id
    
    def _create_enemy_from_config(self, config: Dict[str, Any]) -> NPC:
        """Create an NPC enemy from configuration"""
        npc_id = str(uuid.uuid4())
        enemy = NPC(npc_id, config["name"], config.get("type", "enemy"))
        
        # Set stats
        enemy.stats.health = config.get("health", 100)
        enemy.stats.max_health = enemy.stats.health
        enemy.stats.energy = config.get("energy", 80)
        enemy.stats.max_energy = enemy.stats.energy
        
        # Set abilities
        enemy.abilities = config.get("abilities", ["basic_attack", "defend"])
        enemy.ai_ability_priority = enemy.abilities.copy()
        
        # Set AI behavior
        enemy.combat_behavior = config.get("ai_behavior", "defensive")
        
        return enemy
    
    async def add_player_to_battle(self, battle_id: str, player: Player) -> bool:
        """
        Add a player to an existing battle
        
        Returns:
            True if player was added successfully
        """
        if battle_id not in self.active_battles:
            return False
        
        battle = self.active_battles[battle_id]
        if battle.state != BattleState.PREPARING:
            return False
        
        battle.add_participant(player)
        player.in_battle = True
        player.battle_id = battle_id
        
        return True
    
    async def start_battle(self, battle_id: str) -> Dict[str, Any]:
        """
        Start a battle
        
        Returns:
            Battle start result
        """
        if battle_id not in self.active_battles:
            return {'success': False, 'message': 'Battle not found'}
        
        battle = self.active_battles[battle_id]
        started = battle.start_battle()
        
        if started:
            return {
                'success': True,
                'message': 'Battle started',
                'battle_state': battle.get_battle_state()
            }
        else:
            return {
                'success': False,
                'message': 'Failed to start battle (need at least 2 participants)'
            }
    
    async def use_ability(self, battle_id: str, participant_id: str, ability_id: str, 
                         target_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Use an ability in battle
        
        Returns:
            Ability use result
        """
        if battle_id not in self.active_battles:
            return {'success': False, 'message': 'Battle not found'}
        
        battle = self.active_battles[battle_id]
        
        # Get the ability
        ability = self.all_abilities.get(ability_id)
        if not ability:
            return {'success': False, 'message': 'Ability not found'}
        
        # Create a fresh copy of the ability for this use
        ability_copy = Ability.from_dict(ability.to_dict())
        
        # If no targets specified, try to auto-target
        if not target_ids:
            target_ids = self._auto_select_targets(battle, participant_id, ability_copy)
        
        result = battle.use_ability(participant_id, ability_copy, target_ids)
        
        # Check if turn should end
        if result.get('success'):
            # Process AI turns if it's now an AI's turn
            await self._process_ai_turns(battle)
        
        return result
    
    async def end_turn(self, battle_id: str, participant_id: str) -> Dict[str, Any]:
        """
        End a participant's turn
        
        Returns:
            Turn end result
        """
        if battle_id not in self.active_battles:
            return {'success': False, 'message': 'Battle not found'}
        
        battle = self.active_battles[battle_id]
        result = battle.end_turn()
        
        if result.get('success'):
            # Process AI turns
            await self._process_ai_turns(battle)
        
        return result
    
    async def _process_ai_turns(self, battle: Battle) -> None:
        """Process AI turns automatically"""
        while battle.state == BattleState.ACTIVE:
            current = battle.get_current_participant()
            if not current or current.is_player:
                break
                
            # AI decision making
            await self._make_ai_decision(battle, current)
            
            # Check if battle ended
            win_result = battle.check_win_condition()
            if win_result.get('battle_ended'):
                await self._handle_battle_end(battle, win_result)
                break
    
    async def _make_ai_decision(self, battle: Battle, ai_participant: BattleParticipant) -> None:
        """Make an AI decision for an NPC"""
        npc = ai_participant.entity
        
        # Get available abilities
        available_abilities = []
        for ability_id in npc.abilities:
            ability = self.all_abilities.get(ability_id)
            if ability:
                can_use, _ = ability.can_use(
                    ai_participant.current_energy,
                    ai_participant.current_health,
                    battle.turn_number
                )
                if can_use:
                    available_abilities.append(ability)
        
        if not available_abilities:
            # No abilities available, end turn
            battle.end_turn()
            return
        
        # AI strategy based on combat behavior
        if npc.combat_behavior == "aggressive":
            chosen_ability = self._choose_aggressive_ability(available_abilities, ai_participant, battle)
        elif npc.combat_behavior == "defensive":
            chosen_ability = self._choose_defensive_ability(available_abilities, ai_participant, battle)
        elif npc.combat_behavior == "strategic":
            chosen_ability = await self._choose_strategic_ability(available_abilities, ai_participant, battle)
        else:  # passive or unknown
            chosen_ability = available_abilities[0]  # Just use first available
        
        # Select targets
        target_ids = self._auto_select_targets(battle, ai_participant.entity_id, chosen_ability)
        
        # Use the ability
        battle.use_ability(ai_participant.entity_id, chosen_ability, target_ids)
    
    def _choose_aggressive_ability(self, abilities: List[Ability], ai_participant: BattleParticipant, 
                                 battle: Battle) -> Ability:
        """Choose ability for aggressive AI"""
        # Prefer offensive abilities with highest damage
        offensive_abilities = [a for a in abilities if a.ability_type.value == "offensive"]
        if offensive_abilities:
            return max(offensive_abilities, 
                      key=lambda a: max([e.value for e in a.effects if e.effect_type == "damage"], default=0))
        
        return abilities[0]
    
    def _choose_defensive_ability(self, abilities: List[Ability], ai_participant: BattleParticipant,
                                battle: Battle) -> Ability:
        """Choose ability for defensive AI"""
        # If health is low, prioritize healing
        health_ratio = ai_participant.current_health / ai_participant.max_health
        
        if health_ratio < 0.3:
            healing_abilities = [a for a in abilities if a.ability_type.value == "healing"]
            if healing_abilities:
                return healing_abilities[0]
        
        # If enemies are strong, use defensive abilities
        defensive_abilities = [a for a in abilities if a.ability_type.value == "defensive"]
        if defensive_abilities and health_ratio < 0.6:
            return defensive_abilities[0]
        
        # Otherwise attack
        offensive_abilities = [a for a in abilities if a.ability_type.value == "offensive"]
        if offensive_abilities:
            return offensive_abilities[0]
        
        return abilities[0]
    
    async def _choose_strategic_ability(self, abilities: List[Ability], ai_participant: BattleParticipant,
                                      battle: Battle) -> Ability:
        """Choose ability for strategic AI (using MCP if available)"""
        if self.mcp_service:
            try:
                # Get battle context for AI decision
                context = {
                    'ai_health': ai_participant.current_health,
                    'ai_max_health': ai_participant.max_health,
                    'ai_energy': ai_participant.current_energy,
                    'turn_number': battle.turn_number,
                    'available_abilities': [a.name for a in abilities],
                    'enemies': [
                        {
                            'name': p.name,
                            'health': p.current_health,
                            'max_health': p.max_health
                        }
                        for p in battle.participants if p.is_player and p.is_alive
                    ]
                }
                
                # Query AI for strategic decision
                ai_decision = await self.mcp_service.query_model(
                    f"You are a strategic AI in a turn-based battle. Given this context: {context}, "
                    f"which ability should you use? Choose from: {[a.name for a in abilities]}. "
                    f"Respond with just the ability name."
                )
                
                # Find the recommended ability
                ability_name = ai_decision.strip().lower()
                for ability in abilities:
                    if ability.name.lower() in ability_name or ability_name in ability.name.lower():
                        return ability
                        
            except Exception as e:
                # Fallback to defensive behavior if AI query fails
                pass
        
        # Fallback to defensive strategy
        return self._choose_defensive_ability(abilities, ai_participant, battle)
    
    def _auto_select_targets(self, battle: Battle, user_id: str, ability: Ability) -> List[str]:
        """Automatically select targets for an ability"""
        user_participant = battle.get_participant_by_id(user_id)
        if not user_participant:
            return []
        
        targets = []
        
        for effect in ability.effects:
            if effect.target == "self":
                targets = [user_id]
                break
            elif effect.target == "enemy":
                # Find an enemy to target
                enemies = [p for p in battle.participants 
                          if p.is_player != user_participant.is_player and p.is_alive]
                if enemies:
                    # Target enemy with lowest health ratio for offensive abilities
                    if effect.effect_type == "damage":
                        target = min(enemies, key=lambda p: p.current_health / p.max_health)
                    else:
                        target = random.choice(enemies)
                    targets = [target.entity_id]
                break
            elif effect.target == "ally":
                # Find an ally to target
                allies = [p for p in battle.participants 
                         if p.is_player == user_participant.is_player and p.is_alive and p.entity_id != user_id]
                if allies:
                    # Target ally with lowest health for healing abilities
                    if effect.effect_type == "heal":
                        target = min(allies, key=lambda p: p.current_health / p.max_health)
                    else:
                        target = random.choice(allies)
                    targets = [target.entity_id]
                break
        
        return targets
    
    async def _handle_battle_end(self, battle: Battle, win_result: Dict[str, Any]) -> None:
        """Handle battle end processing"""
        battle_id = battle.battle_id
        
        # Process rewards and experience
        for participant in battle.participants:
            if participant.is_player:
                player = participant.entity
                player.in_battle = False
                player.battle_id = None
                
                # Add battle result to history
                result_type = "won" if win_result['winner'] == 'player' else ("lost" if win_result['winner'] == 'npc' else "draw")
                player.add_battle_result({
                    'battle_id': battle_id,
                    'result': result_type,
                    'experience': self._calculate_experience_reward(battle, participant),
                    'opponent': ', '.join([p.name for p in battle.participants if not p.is_player])
                })
                
                # Grant experience
                if result_type == "won":
                    exp_reward = self._calculate_experience_reward(battle, participant)
                    level_up = player.gain_experience(exp_reward)
                    if level_up:
                        battle.log_event("player_level_up", {
                            'player': player.name,
                            'new_level': player.stats.level
                        })
        
        # Log battle completion
        battle.log_event("battle_processed", {
            'winner': win_result['winner'],
            'total_turns': battle.turn_number,
            'participants': [p.name for p in battle.participants]
        })
    
    def _calculate_experience_reward(self, battle: Battle, participant: BattleParticipant) -> int:
        """Calculate experience reward for a participant"""
        base_exp = 25
        
        # Bonus for winning
        if battle.winner == 'player':
            base_exp += 25
        
        # Bonus for longer battles (strategy/skill)
        if battle.turn_number > 10:
            base_exp += 10
        
        # Bonus for facing higher level enemies
        enemy_levels = [p.entity.stats.level for p in battle.participants 
                       if not p.is_player and hasattr(p.entity, 'stats')]
        if enemy_levels:
            avg_enemy_level = sum(enemy_levels) / len(enemy_levels)
            player_level = participant.entity.stats.level
            if avg_enemy_level > player_level:
                base_exp += int((avg_enemy_level - player_level) * 5)
        
        return base_exp
    
    def get_battle_state(self, battle_id: str) -> Optional[Dict[str, Any]]:
        """Get current battle state"""
        if battle_id not in self.active_battles:
            return None
        
        return self.active_battles[battle_id].get_battle_state()
    
    def get_available_abilities(self, participant_id: str, battle_id: str) -> List[Dict[str, Any]]:
        """Get abilities available to a participant"""
        if battle_id not in self.active_battles:
            return []
        
        battle = self.active_battles[battle_id]
        participant = battle.get_participant_by_id(participant_id)
        if not participant:
            return []
        
        available = []
        
        # Get participant's abilities
        if participant.is_player:
            ability_ids = participant.entity.get_equipped_abilities()
        else:
            ability_ids = participant.entity.abilities
        
        for ability_id in ability_ids:
            ability = self.all_abilities.get(ability_id)
            if ability:
                can_use, reason = ability.can_use(
                    participant.current_energy,
                    participant.current_health,
                    battle.turn_number
                )
                
                available.append({
                    'ability_id': ability_id,
                    'name': ability.name,
                    'description': ability.description,
                    'can_use': can_use,
                    'reason': reason,
                    'cost': {
                        'energy': ability.cost.energy,
                        'health': ability.cost.health,
                        'cooldown': ability.cost.cooldown
                    },
                    'effects': [
                        {
                            'type': effect.effect_type,
                            'target': effect.target,
                            'value': effect.value,
                            'description': effect.description
                        }
                        for effect in ability.effects
                    ]
                })
        
        return available
    
    def cleanup_battle(self, battle_id: str) -> bool:
        """Remove a battle from active battles"""
        if battle_id in self.active_battles:
            del self.active_battles[battle_id]
            return True
        return False
    
    def get_battle_templates(self) -> Dict[str, Any]:
        """Get available battle templates"""
        return {
            template_id: {
                'name': template['name'],
                'description': template['description'],
                'difficulty': len(template['enemies']),
                'rewards': template['rewards']
            }
            for template_id, template in self.battle_templates.items()
        }


# Usage example
if __name__ == "__main__":
    import asyncio
    
    async def demo_battle_service():
        print("⚔️ TEC Battle Service Demo")
        print("=" * 40)
        
        # Create battle service
        battle_service = BattleService()
        
        # Show available templates
        templates = battle_service.get_battle_templates()
        print(f"Available battle templates: {len(templates)}")
        for template_id, info in templates.items():
            print(f"  - {template_id}: {info['name']}")
        
        # Create a tutorial battle
        battle_id = await battle_service.create_battle(
            BattleType.TUTORIAL, 
            template_id="tutorial_first_battle"
        )
        print(f"\nCreated tutorial battle: {battle_id}")
        
        # Create a mock player
        from ..core.player import Player
        player = Player("demo_player", "TestWarrior")
        
        # Add player to battle
        added = await battle_service.add_player_to_battle(battle_id, player)
        print(f"Added player to battle: {added}")
        
        if added:
            # Start battle
            result = await battle_service.start_battle(battle_id)
            print(f"Battle start result: {result['success']}")
            
            if result['success']:
                state = battle_service.get_battle_state(battle_id)
                print(f"Current turn: {state['current_participant']}")
                
                # Get available abilities
                abilities = battle_service.get_available_abilities(player.player_id, battle_id)
                print(f"Player has {len(abilities)} abilities available")
        
        print("\n⚡ Battle service ready for integration!")
    
    # Run demo
    asyncio.run(demo_battle_service())
