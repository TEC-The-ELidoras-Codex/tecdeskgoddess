"""
TEC: BITLYFE - Battle System Core
Manages combat encounters in the Astradigital Arena
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import uuid
import random
from datetime import datetime

from .ability import Ability, AbilityEffect, DamageType
from .player import Player
from .npc import NPC


class BattleState(Enum):
    """States of battle"""
    PREPARING = "preparing"
    ACTIVE = "active"
    PAUSED = "paused"
    FINISHED = "finished"


class BattleType(Enum):
    """Types of battles in TEC"""
    PVE = "pve"  # Player vs Environment (NPC)
    PVP = "pvp"  # Player vs Player
    ARENA = "arena"  # Astradigital Arena combat
    TUTORIAL = "tutorial"  # Learning battle
    BOSS = "boss"  # Major encounter


@dataclass
class BattleParticipant:
    """Wrapper for battle participants with combat state"""
    entity: Union[Player, NPC]
    is_player: bool
    current_health: int
    current_energy: int
    max_health: int
    max_energy: int
    
    # Battle-specific stats
    temp_attack_bonus: int = 0
    temp_defense_bonus: int = 0
    status_effects: List[Dict[str, Any]] = None
    
    # Turn management
    has_acted_this_turn: bool = False
    turn_order_speed: int = 0
    
    def __post_init__(self):
        if self.status_effects is None:
            self.status_effects = []
    
    @property
    def is_alive(self) -> bool:
        """Check if participant is alive"""
        return self.current_health > 0
    
    @property
    def is_defeated(self) -> bool:
        """Check if participant is defeated"""
        return self.current_health <= 0
    
    @property
    def name(self) -> str:
        """Get participant name"""
        return self.entity.name if hasattr(self.entity, 'name') else "Unknown"
    
    @property
    def entity_id(self) -> str:
        """Get entity ID"""
        if hasattr(self.entity, 'player_id'):
            return self.entity.player_id
        elif hasattr(self.entity, 'npc_id'):
            return self.entity.npc_id
        return str(uuid.uuid4())
    
    def apply_damage(self, amount: int, damage_type: DamageType) -> int:
        """
        Apply damage to participant
        
        Returns:
            Actual damage dealt after resistances
        """
        # Apply defense bonuses
        defense = self.temp_defense_bonus
        actual_damage = max(1, amount - defense)  # Minimum 1 damage
        
        self.current_health = max(0, self.current_health - actual_damage)
        return actual_damage
    
    def apply_healing(self, amount: int) -> int:
        """
        Apply healing to participant
        
        Returns:
            Actual healing applied
        """
        old_health = self.current_health
        self.current_health = min(self.max_health, self.current_health + amount)
        return self.current_health - old_health
    
    def consume_energy(self, amount: int) -> bool:
        """
        Consume energy for ability use
        
        Returns:
            True if energy was available and consumed
        """
        if self.current_energy >= amount:
            self.current_energy -= amount
            return True
        return False
    
    def restore_energy(self, amount: int) -> int:
        """
        Restore energy to participant
        
        Returns:
            Actual energy restored
        """
        old_energy = self.current_energy
        self.current_energy = min(self.max_energy, self.current_energy + amount)
        return self.current_energy - old_energy
    
    def add_status_effect(self, effect: Dict[str, Any]) -> None:
        """Add a status effect"""
        self.status_effects.append(effect)
    
    def tick_status_effects(self) -> List[str]:
        """
        Process status effects for one turn
        
        Returns:
            List of effect descriptions that occurred
        """
        messages = []
        effects_to_remove = []
        
        for i, effect in enumerate(self.status_effects):
            # Apply effect
            if effect['type'] == 'damage_over_time':
                damage = self.apply_damage(effect['value'], DamageType.PSYCHIC)
                messages.append(f"{self.name} takes {damage} {effect['name']} damage")
            elif effect['type'] == 'heal_over_time':
                healing = self.apply_healing(effect['value'])
                messages.append(f"{self.name} heals {healing} from {effect['name']}")
            
            # Reduce duration
            effect['duration'] -= 1
            if effect['duration'] <= 0:
                effects_to_remove.append(i)
                messages.append(f"{effect['name']} effect ends on {self.name}")
        
        # Remove expired effects
        for i in reversed(effects_to_remove):
            del self.status_effects[i]
        
        return messages


class Battle:
    """
    Core battle class for TEC combat system
    Manages turn-based combat in the Astradigital Arena
    """
    
    def __init__(self, battle_id: str, battle_type: BattleType):
        self.battle_id = battle_id
        self.battle_type = battle_type
        self.state = BattleState.PREPARING
        
        # Battle metadata
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.ended_at: Optional[datetime] = None
        self.winner: Optional[str] = None
        
        # Participants
        self.participants: List[BattleParticipant] = []
        self.turn_order: List[int] = []  # Indices into participants list
        self.current_turn_index = 0
        self.turn_number = 1
        
        # Battle log
        self.battle_log: List[Dict[str, Any]] = []
        self.last_action: Optional[Dict[str, Any]] = None
        
        # Battle settings
        self.max_turns = 50  # Prevent infinite battles
        self.auto_energy_regen = 10  # Energy regenerated each turn
    
    def add_participant(self, entity: Union[Player, NPC]) -> str:
        """
        Add a participant to the battle
        
        Returns:
            Participant ID for reference
        """
        is_player = isinstance(entity, Player)
        
        # Get stats from entity
        if is_player:
            max_health = getattr(entity, 'health', 100)
            max_energy = getattr(entity, 'energy', 100)
        else:
            stats = getattr(entity, 'stats', None)
            max_health = stats.health if stats else 100
            max_energy = getattr(entity, 'energy', 100)
        
        participant = BattleParticipant(
            entity=entity,
            is_player=is_player,
            current_health=max_health,
            current_energy=max_energy,
            max_health=max_health,
            max_energy=max_energy,
            turn_order_speed=random.randint(1, 20)  # Random initiative
        )
        
        self.participants.append(participant)
        
        # Log participant joining
        self.log_event("participant_joined", {
            'participant': participant.name,
            'is_player': is_player,
            'health': max_health,
            'energy': max_energy
        })
        
        return participant.entity_id
    
    def start_battle(self) -> bool:
        """
        Start the battle
        
        Returns:
            True if battle started successfully
        """
        if len(self.participants) < 2:
            return False
        
        self.state = BattleState.ACTIVE
        self.started_at = datetime.now()
        
        # Determine turn order based on speed
        self.turn_order = list(range(len(self.participants)))
        self.turn_order.sort(key=lambda i: self.participants[i].turn_order_speed, reverse=True)
        
        self.log_event("battle_started", {
            'participants': [p.name for p in self.participants],
            'turn_order': [self.participants[i].name for i in self.turn_order]
        })
        
        return True
    
    def get_current_participant(self) -> Optional[BattleParticipant]:
        """Get the participant whose turn it is"""
        if not self.turn_order or self.state != BattleState.ACTIVE:
            return None
        
        current_participant_index = self.turn_order[self.current_turn_index]
        return self.participants[current_participant_index]
    
    def use_ability(self, participant_id: str, ability: Ability, target_ids: List[str]) -> Dict[str, Any]:
        """
        Use an ability in battle
        
        Returns:
            Result of the ability use
        """
        if self.state != BattleState.ACTIVE:
            return {'success': False, 'message': 'Battle is not active'}
        
        # Find participant
        participant = self.get_participant_by_id(participant_id)
        if not participant:
            return {'success': False, 'message': 'Participant not found'}
        
        # Check if it's their turn
        current = self.get_current_participant()
        if not current or current.entity_id != participant_id:
            return {'success': False, 'message': 'Not your turn'}
        
        # Check if already acted
        if participant.has_acted_this_turn:
            return {'success': False, 'message': 'Already acted this turn'}
        
        # Check if ability can be used
        can_use, reason = ability.can_use(
            participant.current_energy,
            participant.current_health,
            self.turn_number
        )
        
        if not can_use:
            return {'success': False, 'message': reason}
        
        # Use ability
        result = self._execute_ability(participant, ability, target_ids)
        
        # Mark as having acted
        participant.has_acted_this_turn = True
        
        # Log the action
        self.log_event("ability_used", {
            'user': participant.name,
            'ability': ability.name,
            'targets': target_ids,
            'result': result
        })
        
        return result
    
    def _execute_ability(self, user: BattleParticipant, ability: Ability, target_ids: List[str]) -> Dict[str, Any]:
        """Execute an ability and apply its effects"""
        results = []
        
        # Consume resources
        user.consume_energy(ability.cost.energy)
        if ability.cost.health > 0:
            user.apply_damage(ability.cost.health, DamageType.PHYSICAL)
        
        # Apply each effect
        for effect in ability.effects:
            targets = self._resolve_targets(effect.target, user, target_ids)
            
            for target in targets:
                effect_result = self._apply_effect(effect, user, target)
                results.append(effect_result)
        
        # Mark ability as used
        ability.use(self.turn_number)
        
        return {
            'success': True,
            'ability_name': ability.name,
            'effects': results,
            'message': f"{user.name} used {ability.name}"
        }
    
    def _resolve_targets(self, target_type: str, user: BattleParticipant, target_ids: List[str]) -> List[BattleParticipant]:
        """Resolve target string to actual participants"""
        targets = []
        
        if target_type == "self":
            targets = [user]
        elif target_type == "enemy":
            # Find enemies (different team)
            if target_ids:
                target = self.get_participant_by_id(target_ids[0])
                if target and target.is_player != user.is_player:
                    targets = [target]
        elif target_type == "ally":
            # Find allies (same team)
            if target_ids:
                target = self.get_participant_by_id(target_ids[0])
                if target and target.is_player == user.is_player:
                    targets = [target]
        elif target_type == "all_enemies":
            targets = [p for p in self.participants if p.is_player != user.is_player and p.is_alive]
        elif target_type == "all_allies":
            targets = [p for p in self.participants if p.is_player == user.is_player and p.is_alive]
        
        return targets
    
    def _apply_effect(self, effect: AbilityEffect, user: BattleParticipant, target: BattleParticipant) -> Dict[str, Any]:
        """Apply a single ability effect"""
        result = {
            'effect_type': effect.effect_type,
            'target': target.name,
            'value': 0,
            'message': ''
        }
        
        if effect.effect_type == "damage":
            damage = target.apply_damage(effect.value, effect.damage_type)
            result['value'] = damage
            result['message'] = f"{target.name} takes {damage} {effect.damage_type.value} damage"
            
        elif effect.effect_type == "heal":
            healing = target.apply_healing(effect.value)
            result['value'] = healing
            result['message'] = f"{target.name} heals {healing} health"
            
        elif effect.effect_type == "buff":
            if "attack" in effect.description.lower():
                target.temp_attack_bonus += effect.value
            elif "defense" in effect.description.lower():
                target.temp_defense_bonus += effect.value
            
            if effect.duration > 0:
                target.add_status_effect({
                    'name': f"Buff ({effect.description})",
                    'type': 'buff',
                    'value': effect.value,
                    'duration': effect.duration
                })
            
            result['value'] = effect.value
            result['message'] = f"{target.name} gains {effect.description}"
            
        elif effect.effect_type == "debuff":
            if effect.duration > 0:
                target.add_status_effect({
                    'name': f"Debuff ({effect.description})",
                    'type': 'debuff',
                    'value': effect.value,
                    'duration': effect.duration
                })
            
            result['value'] = effect.value
            result['message'] = f"{target.name} suffers {effect.description}"
        
        return result
    
    def end_turn(self) -> Dict[str, Any]:
        """End the current participant's turn"""
        if self.state != BattleState.ACTIVE:
            return {'success': False, 'message': 'Battle is not active'}
        
        current = self.get_current_participant()
        if not current:
            return {'success': False, 'message': 'No current participant'}
        
        # Mark as acted (in case they didn't use an ability)
        current.has_acted_this_turn = True
        
        # Check if all participants have acted
        all_acted = all(p.has_acted_this_turn or not p.is_alive for p in self.participants)
        
        if all_acted:
            return self._start_new_turn()
        else:
            # Move to next participant
            self._advance_turn()
            return {'success': True, 'message': 'Turn ended', 'next_participant': self.get_current_participant().name}
    
    def _start_new_turn(self) -> Dict[str, Any]:
        """Start a new turn for all participants"""
        self.turn_number += 1
        
        # Reset turn flags
        for participant in self.participants:
            participant.has_acted_this_turn = False
            
            # Regenerate energy
            if participant.is_alive:
                participant.restore_energy(self.auto_energy_regen)
        
        # Process status effects
        status_messages = []
        for participant in self.participants:
            if participant.is_alive:
                participant.tick_status_effects()
                # Tick ability cooldowns
                if hasattr(participant.entity, 'abilities'):
                    for ability in participant.entity.abilities:
                        ability.tick_cooldown()
        
        # Reset turn order
        self.current_turn_index = 0
        
        # Check win conditions
        win_result = self.check_win_condition()
        if win_result['battle_ended']:
            return win_result
        
        # Check max turns
        if self.turn_number > self.max_turns:
            return self._end_battle('draw', 'Maximum turns reached')
        
        self.log_event("new_turn", {
            'turn_number': self.turn_number,
            'first_to_act': self.get_current_participant().name
        })
        
        return {
            'success': True,
            'message': f'Turn {self.turn_number} begins',
            'current_participant': self.get_current_participant().name,
            'status_effects': status_messages
        }
    
    def _advance_turn(self) -> None:
        """Advance to the next participant in turn order"""
        while True:
            self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)
            current = self.get_current_participant()
            
            # Skip if dead or already acted
            if current and current.is_alive and not current.has_acted_this_turn:
                break
            
            # If we've gone through everyone, start a new turn
            if self.current_turn_index == 0:
                break
    
    def check_win_condition(self) -> Dict[str, Any]:
        """Check if battle has ended"""
        alive_players = [p for p in self.participants if p.is_player and p.is_alive]
        alive_npcs = [p for p in self.participants if not p.is_player and p.is_alive]
        
        if not alive_players:
            return self._end_battle('npc', 'All players defeated')
        elif not alive_npcs:
            return self._end_battle('player', 'All enemies defeated')
        
        return {'battle_ended': False}
    
    def _end_battle(self, winner: str, reason: str) -> Dict[str, Any]:
        """End the battle"""
        self.state = BattleState.FINISHED
        self.ended_at = datetime.now()
        self.winner = winner
        
        self.log_event("battle_ended", {
            'winner': winner,
            'reason': reason,
            'turns': self.turn_number,
            'duration_seconds': (self.ended_at - self.started_at).total_seconds()
        })
        
        return {
            'success': True,
            'battle_ended': True,
            'winner': winner,
            'reason': reason,
            'message': f'Battle ended: {reason}'
        }
    
    def get_participant_by_id(self, participant_id: str) -> Optional[BattleParticipant]:
        """Find participant by entity ID"""
        for participant in self.participants:
            if participant.entity_id == participant_id:
                return participant
        return None
    
    def log_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log a battle event"""
        self.battle_log.append({
            'timestamp': datetime.now().isoformat(),
            'turn': self.turn_number,
            'event_type': event_type,
            'data': data
        })
    
    def get_battle_state(self) -> Dict[str, Any]:
        """Get current battle state for UI"""
        return {
            'battle_id': self.battle_id,
            'state': self.state.value,
            'turn_number': self.turn_number,
            'current_participant': self.get_current_participant().name if self.get_current_participant() else None,
            'participants': [
                {
                    'id': p.entity_id,
                    'name': p.name,
                    'is_player': p.is_player,
                    'health': p.current_health,
                    'max_health': p.max_health,
                    'energy': p.current_energy,
                    'max_energy': p.max_energy,
                    'is_alive': p.is_alive,
                    'status_effects': p.status_effects,
                    'has_acted': p.has_acted_this_turn
                }
                for p in self.participants
            ],
            'battle_log': self.battle_log[-10:],  # Last 10 events
            'winner': self.winner
        }


# Usage example
if __name__ == "__main__":
    print("⚔️ TEC Battle System Demo")
    print("=" * 40)
    
    # This would normally use actual Player/NPC instances
    # For demo, we'll create mock objects
    class MockPlayer:
        def __init__(self, name, player_id):
            self.name = name
            self.player_id = player_id
            self.health = 100
            self.energy = 100
    
    class MockNPC:
        def __init__(self, name, npc_id):
            self.name = name
            self.npc_id = npc_id
            self.stats = type('Stats', (), {'health': 80})()
            self.energy = 80
    
    # Create battle
    battle = Battle("demo_battle", BattleType.ARENA)
    
    # Add participants
    player = MockPlayer("Test Player", "player_1")
    enemy = MockNPC("Shadow Beast", "npc_1")
    
    battle.add_participant(player)
    battle.add_participant(enemy)
    
    # Start battle
    started = battle.start_battle()
    print(f"Battle started: {started}")
    
    if started:
        state = battle.get_battle_state()
        print(f"Current turn: {state['current_participant']}")
        print(f"Participants: {len(state['participants'])}")
    
    print("\n⚡ Battle system ready for integration!")
