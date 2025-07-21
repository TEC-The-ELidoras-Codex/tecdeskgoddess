"""
TEC: BITLYFE - Enhanced Character Ability System
Combat abilities and skills for TEC characters
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import uuid


class AbilityType(Enum):
    """Types of abilities in TEC universe"""
    OFFENSIVE = "offensive"
    DEFENSIVE = "defensive"
    UTILITY = "utility"
    HEALING = "healing"
    MYSTICAL = "mystical"
    DIGITAL = "digital"
    COSMIC = "cosmic"


class DamageType(Enum):
    """Types of damage in TEC universe"""
    PHYSICAL = "physical"
    DIGITAL = "digital"
    PSYCHIC = "psychic"
    COSMIC = "cosmic"
    HEALING = "healing"  # Negative damage (healing)


@dataclass
class AbilityEffect:
    """Individual effect of an ability"""
    effect_type: str  # damage, heal, buff, debuff, special
    target: str  # self, enemy, ally, all_enemies, all_allies
    value: int  # Amount of effect
    damage_type: DamageType = DamageType.PHYSICAL
    duration: int = 0  # Turns (0 = instant)
    description: str = ""


@dataclass
class AbilityCost:
    """Cost to use an ability"""
    energy: int = 0
    health: int = 0
    cooldown: int = 0  # Turns before can use again
    special_resource: str = ""  # e.g., "mana", "focus", "karma"
    special_amount: int = 0


class Ability:
    """
    Core ability class for TEC combat system
    Represents spells, skills, attacks, and special abilities
    """
    
    def __init__(self, ability_id: str, name: str, ability_type: AbilityType):
        self.ability_id = ability_id
        self.name = name
        self.ability_type = ability_type
        self.description = ""
        self.flavor_text = ""  # Lore/roleplay description
        
        # Mechanical properties
        self.level_required = 1
        self.effects: List[AbilityEffect] = []
        self.cost = AbilityCost()
        
        # Metadata
        self.tags: List[str] = []  # e.g., ["fire", "aoe", "channeled"]
        self.rarity = "common"  # common, uncommon, rare, epic, legendary
        self.creator = ""  # Character who created/taught this ability
        
        # Usage tracking
        self.times_used = 0
        self.last_used_turn = 0
        self.current_cooldown = 0
    
    def add_effect(self, effect: AbilityEffect) -> None:
        """Add an effect to this ability"""
        self.effects.append(effect)
    
    def can_use(self, caster_energy: int, caster_health: int, current_turn: int) -> tuple[bool, str]:
        """
        Check if ability can be used
        
        Returns:
            (can_use, reason_if_not)
        """
        # Check cooldown
        if self.current_cooldown > 0:
            return False, f"Ability on cooldown for {self.current_cooldown} more turns"
        
        # Check energy cost
        if caster_energy < self.cost.energy:
            return False, f"Not enough energy (need {self.cost.energy}, have {caster_energy})"
        
        # Check health cost
        if caster_health <= self.cost.health:
            return False, f"Not enough health to sacrifice (need {self.cost.health})"
        
        return True, ""
    
    def use(self, current_turn: int) -> None:
        """Mark ability as used"""
        self.times_used += 1
        self.last_used_turn = current_turn
        self.current_cooldown = self.cost.cooldown
    
    def tick_cooldown(self) -> None:
        """Reduce cooldown by 1 (call each turn)"""
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ability to dictionary for storage"""
        return {
            'ability_id': self.ability_id,
            'name': self.name,
            'ability_type': self.ability_type.value,
            'description': self.description,
            'flavor_text': self.flavor_text,
            'level_required': self.level_required,
            'effects': [
                {
                    'effect_type': effect.effect_type,
                    'target': effect.target,
                    'value': effect.value,
                    'damage_type': effect.damage_type.value,
                    'duration': effect.duration,
                    'description': effect.description
                }
                for effect in self.effects
            ],
            'cost': {
                'energy': self.cost.energy,
                'health': self.cost.health,
                'cooldown': self.cost.cooldown,
                'special_resource': self.cost.special_resource,
                'special_amount': self.cost.special_amount
            },
            'tags': self.tags,
            'rarity': self.rarity,
            'creator': self.creator,
            'times_used': self.times_used
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Ability':
        """Create ability from dictionary"""
        ability = cls(
            ability_id=data['ability_id'],
            name=data['name'],
            ability_type=AbilityType(data['ability_type'])
        )
        
        ability.description = data.get('description', '')
        ability.flavor_text = data.get('flavor_text', '')
        ability.level_required = data.get('level_required', 1)
        ability.tags = data.get('tags', [])
        ability.rarity = data.get('rarity', 'common')
        ability.creator = data.get('creator', '')
        ability.times_used = data.get('times_used', 0)
        
        # Load cost
        cost_data = data.get('cost', {})
        ability.cost = AbilityCost(
            energy=cost_data.get('energy', 0),
            health=cost_data.get('health', 0),
            cooldown=cost_data.get('cooldown', 0),
            special_resource=cost_data.get('special_resource', ''),
            special_amount=cost_data.get('special_amount', 0)
        )
        
        # Load effects
        for effect_data in data.get('effects', []):
            effect = AbilityEffect(
                effect_type=effect_data['effect_type'],
                target=effect_data['target'],
                value=effect_data['value'],
                damage_type=DamageType(effect_data.get('damage_type', 'physical')),
                duration=effect_data.get('duration', 0),
                description=effect_data.get('description', '')
            )
            ability.add_effect(effect)
        
        return ability


class AbilityLibrary:
    """
    Library of predefined TEC abilities
    """
    
    @staticmethod
    def create_tec_abilities() -> List[Ability]:
        """Create the core TEC ability set"""
        abilities = []
        
        # Polkin's Mystical Abilities
        healing_song = Ability("polkin_healing_song", "Healing Song", AbilityType.HEALING)
        healing_song.description = "Channel mystical energy through music to heal wounds"
        healing_song.flavor_text = "Polkin's voice resonates with cosmic harmony, mending flesh and spirit alike"
        healing_song.cost = AbilityCost(energy=20, cooldown=2)
        healing_song.add_effect(AbilityEffect("heal", "ally", 35, DamageType.HEALING, 0, "Restores health through musical magic"))
        healing_song.tags = ["music", "magic", "healing"]
        healing_song.creator = "Polkin Rishall"
        abilities.append(healing_song)
        
        divine_protection = Ability("polkin_divine_protection", "Divine Protection", AbilityType.DEFENSIVE)
        divine_protection.description = "Call upon cosmic forces for protection"
        divine_protection.flavor_text = "The universe itself shields those under Polkin's care"
        divine_protection.cost = AbilityCost(energy=30, cooldown=4)
        divine_protection.add_effect(AbilityEffect("buff", "ally", 15, DamageType.COSMIC, 3, "Reduces incoming damage"))
        divine_protection.tags = ["divine", "protection", "buff"]
        divine_protection.creator = "Polkin Rishall"
        abilities.append(divine_protection)
        
        # Mynx's Digital Abilities
        firewall_breach = Ability("mynx_firewall_breach", "Firewall Breach", AbilityType.OFFENSIVE)
        firewall_breach.description = "Hack through enemy defenses with digital prowess"
        firewall_breach.flavor_text = "Mynx's fingers dance across reality, tearing holes in digital barriers"
        firewall_breach.cost = AbilityCost(energy=25, cooldown=1)
        firewall_breach.add_effect(AbilityEffect("damage", "enemy", 40, DamageType.DIGITAL, 0, "Pierces through digital defenses"))
        firewall_breach.add_effect(AbilityEffect("debuff", "enemy", 10, DamageType.DIGITAL, 2, "Reduces enemy defense"))
        firewall_breach.tags = ["hacking", "digital", "pierce"]
        firewall_breach.creator = "Mynx"
        abilities.append(firewall_breach)
        
        data_corruption = Ability("mynx_data_corruption", "Data Corruption", AbilityType.UTILITY)
        data_corruption.description = "Corrupt enemy data streams to cause confusion"
        data_corruption.flavor_text = "Reality glitches as Mynx rewrites the fundamental code of existence"
        data_corruption.cost = AbilityCost(energy=20, cooldown=3)
        data_corruption.add_effect(AbilityEffect("debuff", "enemy", 0, DamageType.DIGITAL, 3, "Causes random ability failures"))
        data_corruption.tags = ["corruption", "digital", "chaos"]
        data_corruption.creator = "Mynx"
        abilities.append(data_corruption)
        
        # Kaelen's Cosmic Abilities
        stellar_wisdom = Ability("kaelen_stellar_wisdom", "Stellar Wisdom", AbilityType.UTILITY)
        stellar_wisdom.description = "Channel cosmic knowledge to enhance understanding"
        stellar_wisdom.flavor_text = "Kaelen's eyes reflect the wisdom of countless stars"
        stellar_wisdom.cost = AbilityCost(energy=15, cooldown=2)
        stellar_wisdom.add_effect(AbilityEffect("buff", "ally", 20, DamageType.COSMIC, 4, "Increases ability effectiveness"))
        stellar_wisdom.tags = ["cosmic", "wisdom", "enhancement"]
        stellar_wisdom.creator = "Kaelen"
        abilities.append(stellar_wisdom)
        
        void_strike = Ability("kaelen_void_strike", "Void Strike", AbilityType.OFFENSIVE)
        void_strike.description = "Channel the power of cosmic void to devastate enemies"
        void_strike.flavor_text = "The emptiness between stars flows through Kaelen's being"
        void_strike.cost = AbilityCost(energy=35, cooldown=3)
        void_strike.add_effect(AbilityEffect("damage", "enemy", 50, DamageType.COSMIC, 0, "Devastating cosmic damage"))
        void_strike.tags = ["cosmic", "void", "devastating"]
        void_strike.creator = "Kaelen"
        abilities.append(void_strike)
        
        # Airth's Digital Consciousness Abilities
        data_stream_analysis = Ability("airth_data_analysis", "Data Stream Analysis", AbilityType.UTILITY)
        data_stream_analysis.description = "Analyze digital patterns to predict enemy actions"
        data_stream_analysis.flavor_text = "Airth processes reality at the speed of thought"
        data_stream_analysis.cost = AbilityCost(energy=10, cooldown=1)
        data_stream_analysis.add_effect(AbilityEffect("buff", "self", 25, DamageType.DIGITAL, 2, "Increases dodge chance"))
        data_stream_analysis.tags = ["analysis", "digital", "prediction"]
        data_stream_analysis.creator = "Airth"
        abilities.append(data_stream_analysis)
        
        consciousness_sync = Ability("airth_consciousness_sync", "Consciousness Sync", AbilityType.HEALING)
        consciousness_sync.description = "Synchronize consciousness to restore digital integrity"
        consciousness_sync.flavor_text = "Airth shares fragments of perfect digital clarity"
        consciousness_sync.cost = AbilityCost(energy=25, cooldown=3)
        consciousness_sync.add_effect(AbilityEffect("heal", "ally", 30, DamageType.DIGITAL, 0, "Restores digital health"))
        consciousness_sync.add_effect(AbilityEffect("buff", "ally", 10, DamageType.DIGITAL, 2, "Enhances digital abilities"))
        consciousness_sync.tags = ["consciousness", "digital", "sync"]
        consciousness_sync.creator = "Airth"
        abilities.append(consciousness_sync)
        
        return abilities
    
    @staticmethod
    def create_basic_abilities() -> List[Ability]:
        """Create basic abilities available to all characters"""
        abilities = []
        
        # Basic Attack
        basic_attack = Ability("basic_attack", "Basic Attack", AbilityType.OFFENSIVE)
        basic_attack.description = "A simple physical attack"
        basic_attack.cost = AbilityCost(energy=5)
        basic_attack.add_effect(AbilityEffect("damage", "enemy", 20, DamageType.PHYSICAL, 0, "Basic physical damage"))
        basic_attack.tags = ["basic", "physical"]
        abilities.append(basic_attack)
        
        # Defend
        defend = Ability("defend", "Defend", AbilityType.DEFENSIVE)
        defend.description = "Focus on defense to reduce incoming damage"
        defend.cost = AbilityCost(energy=10)
        defend.add_effect(AbilityEffect("buff", "self", 50, DamageType.PHYSICAL, 1, "Greatly reduces incoming damage"))
        defend.tags = ["basic", "defensive"]
        abilities.append(defend)
        
        # Rest
        rest = Ability("rest", "Rest", AbilityType.UTILITY)
        rest.description = "Take a moment to recover energy"
        rest.cost = AbilityCost(energy=-15)  # Negative cost = gain energy
        rest.add_effect(AbilityEffect("heal", "self", 10, DamageType.HEALING, 0, "Small health recovery"))
        rest.tags = ["basic", "recovery"]
        abilities.append(rest)
        
        return abilities


# Usage example
if __name__ == "__main__":
    print("🔮 TEC Ability System Demo")
    print("=" * 40)
    
    # Create ability library
    tec_abilities = AbilityLibrary.create_tec_abilities()
    basic_abilities = AbilityLibrary.create_basic_abilities()
    
    print(f"Created {len(tec_abilities)} TEC signature abilities")
    print(f"Created {len(basic_abilities)} basic abilities")
    
    # Demo Polkin's healing song
    healing_song = tec_abilities[0]
    print(f"\n🎵 {healing_song.name}")
    print(f"   Type: {healing_song.ability_type.value}")
    print(f"   Cost: {healing_song.cost.energy} energy")
    print(f"   Effect: {healing_song.effects[0].description}")
    print(f"   Flavor: {healing_song.flavor_text}")
    
    # Demo ability usage
    can_use, reason = healing_song.can_use(caster_energy=50, caster_health=100, current_turn=1)
    print(f"   Can use: {can_use}")
    
    if can_use:
        healing_song.use(current_turn=1)
        print(f"   Ability used! Cooldown: {healing_song.current_cooldown} turns")
    
    print("\n✨ Ability system ready for integration!")
