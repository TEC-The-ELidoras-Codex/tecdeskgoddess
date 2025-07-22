#!/usr/bin/env python3
"""
👤 TEC Character Generator - Advanced Operative Profiles
Create detailed TEC universe characters with full backstories
"""

import random
import json
from datetime import datetime

class TECCharacterGenerator:
    """Advanced character generation for the TEC universe"""
    
    def __init__(self):
        self.setup_character_data()
        self.print_header()
        
    def print_header(self):
        print("=" * 80)
        print("👤 TEC ADVANCED CHARACTER GENERATOR")
        print("=" * 80)
        print("🎯 Protocol: Deep Character Creation")
        print("⚔️ Visual Sovereignty: TEC_CSS_072125_V1")
        print("📅 Date: July 21, 2025")
        print("=" * 80)
        
    def setup_character_data(self):
        """Initialize comprehensive character generation data"""
        
        # Names with cyberpunk flavor
        self.first_names = {
            "traditional": ["Alex", "Morgan", "Riley", "Jordan", "Casey", "Taylor", "Sage", "Phoenix"],
            "cyberpunk": ["Cipher", "Echo", "Vex", "Nova", "Raven", "Atlas", "Zara", "Kaelen"],
            "tec_specific": ["Polkin", "Airth", "Mynx", "Iris", "Ghost", "Void", "Neo", "Flux"]
        }
        
        self.last_names = {
            "tech": ["Datastream", "Codewright", "Bitforge", "Synthcore", "Netwalk", "Quantum"],
            "mystical": ["Voidwalker", "Starlink", "Nebular", "Crystalcore", "Astralborn"],
            "traditional": ["Rishall", "Blackwood", "Sterling", "Ashford", "Kane", "Cross"]
        }
        
        # Factions with detailed info
        self.factions = {
            "The Enclave Coalition": {
                "description": "Central governing body seeking unity and order",
                "values": ["unity", "order", "progress", "security"],
                "ranks": ["Council Member", "Senior Coordinator", "Field Coordinator", "Agent"],
                "equipment_style": "military-grade",
                "personality_traits": ["diplomatic", "strategic", "authoritative"]
            },
            "Digital Mystics": {
                "description": "Spiritual technologists bridging magic and data",
                "values": ["wisdom", "harmony", "transcendence", "balance"],
                "ranks": ["Astradigital Sage", "Void Navigator", "Digital Oracle", "Data Shaman"],
                "equipment_style": "mystical-tech",
                "personality_traits": ["intuitive", "philosophical", "serene"]
            },
            "Corporate Syndicate": {
                "description": "Business empire controlling vast resources",
                "values": ["profit", "efficiency", "competition", "innovation"],
                "ranks": ["CEO", "Senior VP", "Director", "Manager", "Analyst"],
                "equipment_style": "corporate-luxury",
                "personality_traits": ["ambitious", "calculating", "professional"]
            },
            "Astradigital Navy": {
                "description": "Elite space force protecting TEC territories",
                "values": ["honor", "duty", "courage", "loyalty"],
                "ranks": ["Fleet Admiral", "Admiral", "Captain", "Commander", "Lieutenant"],
                "equipment_style": "military-naval",
                "personality_traits": ["disciplined", "brave", "tactical"]
            },
            "Void Runners": {
                "description": "Independent operators thriving in chaos",
                "values": ["freedom", "adaptability", "survival", "profit"],
                "ranks": ["Void Captain", "Navigator", "Operative", "Runner"],
                "equipment_style": "scavenged-modular",
                "personality_traits": ["resourceful", "independent", "unpredictable"]
            }
        }
        
        # Specializations with detailed descriptions
        self.specializations = {
            "Neural Interface Designer": {
                "description": "Creates mind-machine connection systems",
                "skills": ["neural mapping", "consciousness transfer", "AI integration"],
                "equipment": ["neural crown", "consciousness scanner", "AI companion"]
            },
            "Data Archaeologist": {
                "description": "Recovers lost information from digital ruins",
                "skills": ["data recovery", "encryption breaking", "historical analysis"],
                "equipment": ["quantum scanner", "data mining rig", "temporal trace detector"]
            },
            "Quantum Communications": {
                "description": "Manages instantaneous interstellar communication",
                "skills": ["quantum entanglement", "signal amplification", "encryption protocols"],
                "equipment": ["quantum transmitter", "entanglement chamber", "signal processor"]
            },
            "Cyber Warfare Expert": {
                "description": "Conducts digital combat operations",
                "skills": ["system infiltration", "viral programming", "network defense"],
                "equipment": ["hacking deck", "viral compiler", "security scanner"]
            },
            "Infiltration Specialist": {
                "description": "Masters of stealth and social engineering",
                "skills": ["disguise", "lock picking", "social manipulation"],
                "equipment": ["stealth cloak", "biometric spoofer", "voice modulator"]
            }
        }
        
        # Personality traits
        self.positive_traits = [
            "unwavering loyalty", "exceptional technical prowess", "natural leadership",
            "empathic resonance", "creative problem-solving", "digital intuition",
            "calm under pressure", "protective instincts", "analytical precision",
            "inspirational presence", "strategic thinking", "adaptive intelligence"
        ]
        
        self.negative_traits = [
            "trust issues", "data addiction", "authority defiance",
            "perfectionist paralysis", "emotional disconnection", "reckless curiosity",
            "corporate paranoia", "memory fragmentation", "isolation tendencies",
            "reality dissociation", "obsessive behavior", "past trauma"
        ]
        
        # Backstory elements
        self.origins = [
            "Born in the digital slums of Neo-Tokyo",
            "Raised aboard a deep space mining vessel",
            "Former corporate executive who discovered dark secrets",
            "Survivor of the Great Data Purge",
            "Child prodigy recruited by TEC at age 12",
            "Reformed criminal seeking redemption",
            "Military veteran adapting to civilian life",
            "Academy graduate with mysterious past"
        ]
        
        self.motivations = [
            "Seeking revenge against those who destroyed their family",
            "Trying to uncover the truth about their altered memories",
            "Protecting innocent civilians from corporate exploitation",
            "Searching for a lost loved one in the digital void",
            "Attempting to bridge the gap between human and AI",
            "Working to prevent an impending technological disaster",
            "Striving to prove their worth to their faction",
            "Fighting to maintain their humanity in a digital world"
        ]
        
    def generate_character(self, faction_preference=None):
        """Generate a complete TEC character profile"""
        
        # Select faction
        if faction_preference and faction_preference in self.factions:
            faction = faction_preference
        else:
            faction = random.choice(list(self.factions.keys()))
            
        faction_data = self.factions[faction]
        
        # Generate name
        name_style = random.choice(["traditional", "cyberpunk", "tec_specific"])
        first_name = random.choice(self.first_names[name_style])
        
        last_style = random.choice(["tech", "mystical", "traditional"])
        last_name = random.choice(self.last_names[last_style])
        
        # Generate core attributes
        specialization = random.choice(list(self.specializations.keys()))
        spec_data = self.specializations[specialization]
        
        rank = random.choice(faction_data["ranks"])
        clearance_levels = ["Alpha Prime - Cosmic", "Alpha - Stellar", "Beta - Orbital", 
                          "Gamma - Continental", "Delta - Regional", "Epsilon - Local"]
        clearance = random.choice(clearance_levels)
        
        # Generate personality
        positive_trait = random.choice(self.positive_traits)
        negative_trait = random.choice(self.negative_traits)
        faction_trait = random.choice(faction_data["personality_traits"])
        
        # Generate backstory
        origin = random.choice(self.origins)
        motivation = random.choice(self.motivations)
        
        # Generate codename
        codenames = [
            "Ghost Protocol", "Data Phantom", "Zero Day", "Black Ice", "Neural Storm",
            "Void Walker", "Neon Shadow", "Code Breaker", "Digital Reaper", "Quantum Echo",
            "Pulse Rider", "Matrix Hunter", "Cyber Wraith", "Data Sage", "Void Touched"
        ]
        codename = random.choice(codenames)
        
        # Compile character
        character = {
            "basic_info": {
                "name": f"{first_name} {last_name}",
                "codename": codename,
                "faction": faction,
                "rank": rank,
                "specialization": specialization,
                "clearance": clearance
            },
            "personality": {
                "positive_trait": positive_trait,
                "negative_trait": negative_trait,
                "faction_trait": faction_trait,
                "core_values": faction_data["values"]
            },
            "background": {
                "origin": origin,
                "motivation": motivation,
                "faction_description": faction_data["description"]
            },
            "capabilities": {
                "skills": spec_data["skills"],
                "equipment": spec_data["equipment"],
                "equipment_style": faction_data["equipment_style"]
            },
            "metadata": {
                "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "generator_version": "TEC_Lore_Forge_v1.0"
            }
        }
        
        return character
        
    def print_character_profile(self, character):
        """Print a beautifully formatted character profile"""
        
        basic = character["basic_info"]
        personality = character["personality"]
        background = character["background"]
        capabilities = character["capabilities"]
        
        print("\n" + "="*80)
        print("👤 TEC OPERATIVE DOSSIER - CLASSIFIED")
        print("="*80)
        
        # Basic Information
        print(f"📛 OPERATIVE NAME: {basic['name']}")
        print(f"🎭 CODENAME: {basic['codename']}")
        print(f"⚔️ FACTION: {basic['faction']}")
        print(f"🏅 RANK/TITLE: {basic['rank']}")
        print(f"🎯 SPECIALIZATION: {basic['specialization']}")
        print(f"🔐 SECURITY CLEARANCE: {basic['clearance']}")
        
        print(f"\n📋 FACTION OVERVIEW:")
        print(f"   {background['faction_description']}")
        print(f"   Core Values: {', '.join(personality['core_values'])}")
        
        # Psychological Profile
        print(f"\n🧠 PSYCHOLOGICAL PROFILE:")
        print(f"   ✅ PRIMARY STRENGTH: {personality['positive_trait']}")
        print(f"   ⚠️ NOTABLE WEAKNESS: {personality['negative_trait']}")
        print(f"   🎯 FACTION TRAIT: {personality['faction_trait']}")
        
        # Background
        print(f"\n📚 BACKGROUND:")
        print(f"   🏠 ORIGIN: {background['origin']}")
        print(f"   💭 MOTIVATION: {background['motivation']}")
        
        # Capabilities
        print(f"\n🛠️ OPERATIONAL CAPABILITIES:")
        print(f"   🎪 CORE SKILLS: {', '.join(capabilities['skills'])}")
        print(f"   ⚙️ EQUIPMENT: {', '.join(capabilities['equipment'])}")
        print(f"   🎨 GEAR STYLE: {capabilities['equipment_style']}")
        
        print("="*80)
        
    def generate_character_squad(self, count=3, faction=None):
        """Generate a squad of characters"""
        print(f"\n🎯 GENERATING {count}-MEMBER TEC OPERATIVE SQUAD")
        if faction:
            print(f"⚔️ FACTION: {faction}")
        print("="*60)
        
        squad = []
        for i in range(count):
            character = self.generate_character(faction)
            squad.append(character)
            self.print_character_profile(character)
            
        return squad
        
    def save_characters_to_file(self, characters, filename="tec_characters.json"):
        """Save generated characters to JSON file"""
        with open(filename, 'w') as f:
            json.dump(characters, f, indent=2)
        print(f"\n💾 Characters saved to {filename}")

if __name__ == "__main__":
    generator = TECCharacterGenerator()
    
    print("\n🚀 GENERATING TEC OPERATIVE PROFILES...")
    
    # Generate characters from different factions
    characters = []
    
    # One from each major faction
    for faction in ["Digital Mystics", "Corporate Syndicate", "Astradigital Navy"]:
        character = generator.generate_character(faction)
        characters.append(character)
        generator.print_character_profile(character)
    
    # Save characters
    generator.save_characters_to_file(characters)
    
    print(f"\n🎉 CHARACTER GENERATION COMPLETE!")
    print(f"✅ Generated {len(characters)} detailed operative profiles")
    print(f"💾 Characters saved to tec_characters.json")
    print(f"🌟 Ready for deployment in TEC universe campaigns!")
