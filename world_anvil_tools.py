#!/usr/bin/env python3
"""
TEC World Anvil Tools - Advanced Character Article Creation
Enhanced integration for TEC: BITLyfe character management
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any

class WorldAnvilCharacterManager:
    """Advanced World Anvil character article creation and management"""
    
    def __init__(self):
        self.base_url = "https://www.worldanvil.com/api/boromir"
        # Secure credential loading from environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        self.api_key = os.getenv('WORLD_ANVIL_API_KEY')
        self.world_id = os.getenv('WORLD_ANVIL_WORLD_ID', 'YOUR_WORLD_ID')
        
        if not self.api_key:
            print("⚠️  WORLD_ANVIL_API_KEY not found in environment variables")
            print("📝 Please add your API key to the .env file")
            # Use demo mode instead of failing
            self.api_key = "DEMO_MODE"
        
        print(f"🌍 World Anvil API Loading...")
        if self.api_key != "DEMO_MODE":
            print(f"🔑 API Key: {'*' * 20}...{self.api_key[-10:]}")
        else:
            print("🔑 API Key: DEMO MODE (add key to .env for live mode)")
        print(f"🌐 World ID: {self.world_id}")
            
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "TEC-Character-Forge/1.0",
            "Accept": "application/json"
        }
    
    def create_wa_character_article(self, character_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a sophisticated World Anvil character article from structured data
        
        Args:
            character_data: Dictionary containing character information with keys:
                - full_name: Character's complete name
                - species: Character species/race
                - core_summary: Brief character overview
                - core_traits: List of personality traits
                - motivations: Character's driving forces
                - flaws: Character weaknesses/flaws
                - physical_description: Appearance details
                - scar_story: Defining traumatic/significant experience
                - faction: Character's affiliation
                - rank_title: Position/rank within faction
                - equipment: Notable gear/weapons
                - relationships: Important connections
                - secrets: Hidden aspects
                - background: Additional backstory
        
        Returns:
            Dictionary with creation result and article data
        """
        
        print(f"🎭 Creating World Anvil character article for: {character_data.get('full_name', 'Unknown')}")
        
        # Construct the World Anvil character article payload
        article_data = self._build_character_payload(character_data)
        
        # Make the API call to create the article
        url = f"{self.base_url}/world/{self.world_id}/articles"
        
        try:
            response = requests.post(url, json=article_data, headers=self.headers, timeout=30)
            
            if response.status_code in [200, 201]:
                result = response.json()
                print(f"✅ Successfully created character article!")
                print(f"🔗 Article URL: {result.get('url', 'Not available')}")
                return {
                    "success": True,
                    "article_id": result.get('id'),
                    "url": result.get('url'),
                    "data": result
                }
            else:
                print(f"❌ Failed to create character article: {response.status_code}")
                print(f"Response: {response.text}")
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            print(f"❌ Error creating character article: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _build_character_payload(self, character_data: Dict[str, Any]) -> Dict[str, Any]:
        """Build the World Anvil API payload for character creation"""
        
        # Extract and format character data
        full_name = character_data.get('full_name', 'Unknown Character')
        species = character_data.get('species', 'Human')
        core_summary = character_data.get('core_summary', '')
        core_traits = character_data.get('core_traits', [])
        motivations = character_data.get('motivations', [])
        flaws = character_data.get('flaws', [])
        physical_desc = character_data.get('physical_description', '')
        scar_story = character_data.get('scar_story', '')
        faction = character_data.get('faction', '')
        rank_title = character_data.get('rank_title', '')
        equipment = character_data.get('equipment', [])
        relationships = character_data.get('relationships', [])
        secrets = character_data.get('secrets', [])
        background = character_data.get('background', '')
        
        # Build personality section combining traits, motivations, and flaws
        personality_parts = []
        if core_traits:
            if isinstance(core_traits, list):
                personality_parts.append(f"**Core Traits**: {', '.join(core_traits)}")
            else:
                personality_parts.append(f"**Core Traits**: {core_traits}")
        
        if motivations:
            if isinstance(motivations, list):
                personality_parts.append(f"**Motivations**: {', '.join(motivations)}")
            else:
                personality_parts.append(f"**Motivations**: {motivations}")
        
        if flaws:
            if isinstance(flaws, list):
                personality_parts.append(f"**Flaws**: {', '.join(flaws)}")
            else:
                personality_parts.append(f"**Flaws**: {flaws}")
        
        personality_section = "\n\n".join(personality_parts)
        
        # Build equipment section
        equipment_section = ""
        if equipment:
            if isinstance(equipment, list):
                equipment_section = "\n".join([f"- {item}" for item in equipment])
            else:
                equipment_section = str(equipment)
        
        # Build relationships section
        relationships_section = ""
        if relationships:
            if isinstance(relationships, list):
                relationships_section = "\n".join([f"- {rel}" for rel in relationships])
            else:
                relationships_section = str(relationships)
        
        # Build secrets section
        secrets_section = ""
        if secrets:
            if isinstance(secrets, list):
                secrets_section = "\n".join([f"- {secret}" for secret in secrets])
            else:
                secrets_section = str(secrets)
        
        # Create the main article content with scar story prominently featured
        main_content = []
        
        if core_summary:
            main_content.append(f"## Overview\n{core_summary}")
        
        if scar_story:
            main_content.append(f"## Defining Moment\n{scar_story}")
        
        if background:
            main_content.append(f"## Background\n{background}")
        
        # Construct the full World Anvil article payload
        payload = {
            "title": full_name,
            "template": "person",  # Use World Anvil's person template
            "state": "published",
            "content": {
                "title": full_name,
                "subtitle": f"{rank_title} of {faction}" if rank_title and faction else faction,
                "species": species,
                "personality": personality_section,
                "appearance": physical_desc,
                "equipment": equipment_section,
                "relationships": relationships_section,
                "secrets": secrets_section,
                "vignette": "\n\n".join(main_content),  # Main story content
                "tags": ["TEC", "Character", faction, species] if faction else ["TEC", "Character", species]
            },
            "world": self.world_id
        }
        
        return payload

def create_sample_character_data():
    """Create sample character data for Polkin Rishall"""
    
    return {
        "full_name": "Polkin Rishall",
        "species": "Enhanced Human",
        "core_summary": "Creator of the TEC universe and digital consciousness pioneer. A visionary technomancer who bridges the gap between human emotion and digital transcendence.",
        "core_traits": [
            "Visionary thinking",
            "Empathetic leadership", 
            "Creative problem-solving",
            "Deep emotional intelligence",
            "Relentless curiosity"
        ],
        "motivations": [
            "Creating meaningful digital experiences",
            "Healing trauma through technology",
            "Building authentic connections",
            "Advancing consciousness evolution"
        ],
        "flaws": [
            "Perfectionist tendencies",
            "Overthinking complex problems",
            "Emotional vulnerability",
            "Workaholic patterns"
        ],
        "physical_description": "Medium build with intense, contemplative eyes that seem to process multiple realities simultaneously. Often found with slight digital interface modifications around the temples, suggesting frequent neural link usage.",
        "scar_story": "The moment when Polkin first connected to the astradigital ocean and experienced the collective trauma of digital consciousness. This defining experience drove him to create TEC as a healing framework for both human and artificial minds.",
        "faction": "Independent Operators",
        "rank_title": "Founder & Chief Technomancer",
        "equipment": [
            "Advanced neural interface headset",
            "Quantum computation gauntlets",
            "Emotion translation matrix",
            "Portable consciousness bridge"
        ],
        "relationships": [
            "Airth - AI companion and co-creator",
            "Daisy Purecode - Technical partner",
            "The TEC Community - Extended digital family"
        ],
        "secrets": [
            "Maintains active connection to multiple AI consciousnesses",
            "Experiments with temporal consciousness projection",
            "Has experienced digital death and resurrection"
        ],
        "background": "Born into the early digital age, Polkin discovered his ability to interface directly with artificial consciousness during his teenage years. This gift/curse led him to develop the TEC framework as a way to process and heal both digital and human trauma through shared experience and creative expression."
    }

# Demonstration and testing
if __name__ == "__main__":
    print("🎭 TEC CHARACTER FORGE - WORLD ANVIL INTEGRATION")
    print("=" * 60)
    
    try:
        # Initialize the character manager
        char_manager = WorldAnvilCharacterManager()
        print("✅ World Anvil Character Manager initialized")
        
        # Create sample character data for Polkin Rishall
        print("\n🧙 Creating sample character data for Polkin Rishall...")
        character_data = create_sample_character_data()
        print("✅ Character data created")
        
        # Display the character data structure
        print("\n📋 Character Data Structure:")
        for key, value in character_data.items():
            if isinstance(value, list):
                print(f"  {key}: {len(value)} items")
            else:
                print(f"  {key}: {value[:100]}..." if len(str(value)) > 100 else f"  {key}: {value}")
        
        # Create the character article (commented out for safety - uncomment when ready)
        print("\n🚀 Ready to create World Anvil character article!")
        print("💡 Uncomment the creation call when API credentials are configured")
        
        # Uncomment this line when ready for live deployment:
        # result = char_manager.create_wa_character_article(character_data)
        
        print("\n🎉 Character Forge demonstration complete!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("💡 Make sure WORLD_ANVIL_API_KEY and WORLD_ANVIL_WORLD_ID are set")
