"""
TEC: BITLYFE - Core Layer
The "Soul" of TEC - Pure game logic with no external dependencies
"""

from .player import Player
from .npc import NPC
from .game_world import GameWorld
from .item import Item

__all__ = ['Player', 'NPC', 'GameWorld', 'Item']
