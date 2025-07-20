"""
TEC: BITLYFE - Item Core Class
The fundamental Item entity - represents all items, weapons, lore artifacts, etc.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ItemType(Enum):
    """Types of items in the game"""
    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"
    QUEST = "quest"
    LORE = "lore"
    CURRENCY = "currency"
    MATERIAL = "material"
    TOOL = "tool"
    ARTIFACT = "artifact"


class ItemRarity(Enum):
    """Item rarity levels"""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHIC = "mythic"


@dataclass
class ItemStats:
    """Stats that an item provides or requires"""
    damage: int = 0
    defense: int = 0
    strength_bonus: int = 0
    agility_bonus: int = 0
    intelligence_bonus: int = 0
    charisma_bonus: int = 0
    health_bonus: int = 0
    mana_bonus: int = 0
    critical_chance: float = 0.0
    durability: int = 100
    max_durability: int = 100


class Item:
    """
    Core Item class - The fundamental representation of any item in TEC: BITLYFE
    This includes weapons, armor, consumables, quest items, lore artifacts, etc.
    """
    
    def __init__(self, item_id: str, name: str, item_type: ItemType, rarity: ItemRarity = ItemRarity.COMMON):
        self.item_id = item_id
        self.name = name
        self.item_type = item_type
        self.rarity = rarity
        
        # Basic Properties
        self.description: str = ""
        self.lore_text: str = ""
        self.value: int = 0  # Base gold/currency value
        self.weight: float = 1.0
        self.stack_size: int = 1  # How many can stack in one inventory slot
        
        # Stats and Effects
        self.stats = ItemStats()
        self.requirements: Dict[str, int] = {}  # level, strength, etc. required to use
        self.effects: List[Dict] = []  # Special effects (healing, buffs, etc.)
        
        # Usage Properties
        self.is_consumable: bool = item_type == ItemType.CONSUMABLE
        self.is_equipable: bool = item_type in [ItemType.WEAPON, ItemType.ARMOR]
        self.is_tradeable: bool = True
        self.is_droppable: bool = True
        self.is_quest_item: bool = item_type == ItemType.QUEST
        
        # Crafting and Enhancement
        self.can_be_crafted: bool = False
        self.crafting_recipe: List[Dict] = []  # Required materials and quantities
        self.can_be_enhanced: bool = False
        self.enhancement_level: int = 0
        self.max_enhancement: int = 10
        
        # Lore and Story
        self.discovery_location: str = ""
        self.associated_npcs: List[str] = []  # NPCs related to this item
        self.associated_quests: List[str] = []  # Quests that involve this item
        self.flavor_text: str = ""
        
        # Metadata
        self.created_at = datetime.now()
        self.last_modified = datetime.now()
        self.created_by: str = "system"  # player_id or "system"
        
        # Special Properties for different item types
        self.weapon_type: Optional[str] = None  # sword, bow, staff, etc.
        self.armor_slot: Optional[str] = None  # head, chest, legs, etc.
        self.consumable_effect: Optional[str] = None  # heal, mana_restore, buff, etc.
    
    def use_item(self, user_id: str, target_id: Optional[str] = None) -> Dict:
        """
        Use/consume the item
        Returns the result of using the item
        """
        if not self.is_consumable:
            return {"success": False, "message": "Item is not consumable"}
        
        result = {
            "success": True,
            "user_id": user_id,
            "target_id": target_id or user_id,
            "item_id": self.item_id,
            "effects_applied": [],
            "message": f"Used {self.name}"
        }
        
        # Apply effects based on item type
        for effect in self.effects:
            result["effects_applied"].append(effect)
        
        # Reduce durability if applicable
        if self.stats.durability > 0:
            self.stats.durability -= 1
            if self.stats.durability <= 0:
                result["item_broken"] = True
                result["message"] += " (Item broke from use)"
        
        return result
    
    def repair(self, amount: Optional[int] = None) -> bool:
        """Repair the item's durability"""
        if amount is None:
            amount = self.stats.max_durability
        
        old_durability = self.stats.durability
        self.stats.durability = min(self.stats.max_durability, self.stats.durability + amount)
        return self.stats.durability > old_durability
    
    def enhance(self) -> bool:
        """Enhance/upgrade the item"""
        if not self.can_be_enhanced or self.enhancement_level >= self.max_enhancement:
            return False
        
        self.enhancement_level += 1
        
        # Apply enhancement bonuses (simple linear scaling for now)
        enhancement_multiplier = 1 + (self.enhancement_level * 0.1)
        
        # Enhance stats
        if self.stats.damage > 0:
            self.stats.damage = int(self.stats.damage * enhancement_multiplier)
        if self.stats.defense > 0:
            self.stats.defense = int(self.stats.defense * enhancement_multiplier)
        
        # Enhance bonuses
        for attr in ['strength_bonus', 'agility_bonus', 'intelligence_bonus', 'charisma_bonus']:
            current_value = getattr(self.stats, attr)
            if current_value > 0:
                setattr(self.stats, attr, int(current_value * enhancement_multiplier))
        
        self.last_modified = datetime.now()
        return True
    
    def meets_requirements(self, player_stats: Dict) -> bool:
        """Check if a player meets the requirements to use this item"""
        for req_type, req_value in self.requirements.items():
            if req_type == "level":
                if player_stats.get("level", 1) < req_value:
                    return False
            elif req_type in player_stats:
                if player_stats[req_type] < req_value:
                    return False
        return True
    
    def get_tooltip_info(self) -> Dict:
        """Get formatted information for UI tooltips"""
        tooltip = {
            "name": self.name,
            "type": self.item_type.value,
            "rarity": self.rarity.value,
            "description": self.description,
            "value": self.value,
            "weight": self.weight
        }
        
        # Add stats if relevant
        if self.is_equipable:
            stats_info = {}
            if self.stats.damage > 0:
                stats_info["damage"] = self.stats.damage
            if self.stats.defense > 0:
                stats_info["defense"] = self.stats.defense
            if self.stats.strength_bonus != 0:
                stats_info["strength"] = f"+{self.stats.strength_bonus}"
            if self.stats.agility_bonus != 0:
                stats_info["agility"] = f"+{self.stats.agility_bonus}"
            if self.stats.intelligence_bonus != 0:
                stats_info["intelligence"] = f"+{self.stats.intelligence_bonus}"
            if self.stats.charisma_bonus != 0:
                stats_info["charisma"] = f"+{self.stats.charisma_bonus}"
            
            tooltip["stats"] = stats_info
            tooltip["durability"] = f"{self.stats.durability}/{self.stats.max_durability}"
        
        # Add requirements
        if self.requirements:
            tooltip["requirements"] = self.requirements
        
        # Add enhancement info
        if self.enhancement_level > 0:
            tooltip["enhancement"] = f"+{self.enhancement_level}"
        
        # Add effects for consumables
        if self.effects:
            tooltip["effects"] = [effect.get("description", str(effect)) for effect in self.effects]
        
        # Add lore if present
        if self.lore_text:
            tooltip["lore"] = self.lore_text
        
        return tooltip
    
    def get_market_value(self) -> int:
        """Calculate the current market value of the item"""
        base_value = self.value
        
        # Rarity multiplier
        rarity_multipliers = {
            ItemRarity.COMMON: 1.0,
            ItemRarity.UNCOMMON: 2.0,
            ItemRarity.RARE: 5.0,
            ItemRarity.EPIC: 15.0,
            ItemRarity.LEGENDARY: 50.0,
            ItemRarity.MYTHIC: 200.0
        }
        
        value = base_value * rarity_multipliers.get(self.rarity, 1.0)
        
        # Enhancement multiplier
        if self.enhancement_level > 0:
            value *= (1 + self.enhancement_level * 0.5)
        
        # Durability modifier
        if self.stats.max_durability > 0:
            durability_ratio = self.stats.durability / self.stats.max_durability
            value *= (0.1 + 0.9 * durability_ratio)  # 10% minimum value for broken items
        
        return int(value)
    
    def create_copy(self, new_item_id: str) -> 'Item':
        """Create a copy of this item with a new ID"""
        new_item = Item(new_item_id, self.name, self.item_type, self.rarity)
        
        # Copy all properties
        new_item.description = self.description
        new_item.lore_text = self.lore_text
        new_item.value = self.value
        new_item.weight = self.weight
        new_item.stack_size = self.stack_size
        
        # Copy stats
        new_item.stats = ItemStats(
            damage=self.stats.damage,
            defense=self.stats.defense,
            strength_bonus=self.stats.strength_bonus,
            agility_bonus=self.stats.agility_bonus,
            intelligence_bonus=self.stats.intelligence_bonus,
            charisma_bonus=self.stats.charisma_bonus,
            health_bonus=self.stats.health_bonus,
            mana_bonus=self.stats.mana_bonus,
            critical_chance=self.stats.critical_chance,
            durability=self.stats.durability,
            max_durability=self.stats.max_durability
        )
        
        new_item.requirements = self.requirements.copy()
        new_item.effects = [effect.copy() for effect in self.effects]
        
        # Copy usage properties
        new_item.is_consumable = self.is_consumable
        new_item.is_equipable = self.is_equipable
        new_item.is_tradeable = self.is_tradeable
        new_item.is_droppable = self.is_droppable
        new_item.is_quest_item = self.is_quest_item
        
        return new_item
    
    def to_dict(self) -> Dict:
        """Convert item to dictionary for serialization"""
        return {
            'item_id': self.item_id,
            'name': self.name,
            'item_type': self.item_type.value,
            'rarity': self.rarity.value,
            'description': self.description,
            'lore_text': self.lore_text,
            'value': self.value,
            'weight': self.weight,
            'stack_size': self.stack_size,
            'stats': {
                'damage': self.stats.damage,
                'defense': self.stats.defense,
                'strength_bonus': self.stats.strength_bonus,
                'agility_bonus': self.stats.agility_bonus,
                'intelligence_bonus': self.stats.intelligence_bonus,
                'charisma_bonus': self.stats.charisma_bonus,
                'health_bonus': self.stats.health_bonus,
                'mana_bonus': self.stats.mana_bonus,
                'critical_chance': self.stats.critical_chance,
                'durability': self.stats.durability,
                'max_durability': self.stats.max_durability
            },
            'requirements': self.requirements,
            'effects': self.effects,
            'is_consumable': self.is_consumable,
            'is_equipable': self.is_equipable,
            'is_tradeable': self.is_tradeable,
            'is_droppable': self.is_droppable,
            'is_quest_item': self.is_quest_item,
            'enhancement_level': self.enhancement_level,
            'weapon_type': self.weapon_type,
            'armor_slot': self.armor_slot,
            'consumable_effect': self.consumable_effect,
            'created_at': self.created_at.isoformat(),
            'last_modified': self.last_modified.isoformat(),
            'created_by': self.created_by
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Item':
        """Create item from dictionary"""
        item = cls(
            data['item_id'],
            data['name'],
            ItemType(data['item_type']),
            ItemRarity(data['rarity'])
        )
        
        # Restore properties
        item.description = data['description']
        item.lore_text = data['lore_text']
        item.value = data['value']
        item.weight = data['weight']
        item.stack_size = data['stack_size']
        
        # Restore stats
        stats_data = data['stats']
        item.stats = ItemStats(
            damage=stats_data['damage'],
            defense=stats_data['defense'],
            strength_bonus=stats_data['strength_bonus'],
            agility_bonus=stats_data['agility_bonus'],
            intelligence_bonus=stats_data['intelligence_bonus'],
            charisma_bonus=stats_data['charisma_bonus'],
            health_bonus=stats_data['health_bonus'],
            mana_bonus=stats_data['mana_bonus'],
            critical_chance=stats_data['critical_chance'],
            durability=stats_data['durability'],
            max_durability=stats_data['max_durability']
        )
        
        item.requirements = data['requirements']
        item.effects = data['effects']
        item.is_consumable = data['is_consumable']
        item.is_equipable = data['is_equipable']
        item.is_tradeable = data['is_tradeable']
        item.is_droppable = data['is_droppable']
        item.is_quest_item = data['is_quest_item']
        item.enhancement_level = data['enhancement_level']
        item.weapon_type = data['weapon_type']
        item.armor_slot = data['armor_slot']
        item.consumable_effect = data['consumable_effect']
        item.created_by = data['created_by']
        
        # Restore timestamps
        item.created_at = datetime.fromisoformat(data['created_at'])
        item.last_modified = datetime.fromisoformat(data['last_modified'])
        
        return item
