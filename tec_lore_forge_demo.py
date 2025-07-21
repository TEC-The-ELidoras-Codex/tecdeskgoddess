#!/usr/bin/env python3
"""
🎯 TEC Lore Forge - Live Demonstration
Protocol: Automated Content Generation System
Status: OPERATIONAL
"""

import json
import random
from datetime import datetime

class TECLorgeForgeDemo:
    """Demonstration of the TEC Lore Forge automated content generation system"""
    
    def __init__(self):
        self.print_header()
        self.setup_generators()
        
    def print_header(self):
        """Display TEC Lore Forge header"""
        print("=" * 70)
        print("🎯 TEC LORE FORGE - LIVE DEMONSTRATION")
        print("=" * 70)
        print("📅 Date: July 21, 2025")
        print("🚀 Protocol: Automated Content Generation")
        print("⚔️ Visual Sovereignty: TEC_CSS_072125_V1")
        print("🌟 Status: OPERATIONAL")
        print("=" * 70)
        
    def setup_generators(self):
        """Initialize all TEC generators with sample data"""
        
        # Basic string generators
        self.generators = {
            "tec-first-name": ["Polkin", "Airth", "Mynx", "Kaelen", "Zara", "Vex", "Cipher", "Nova", "Raven", "Echo", "Phoenix", "Sage", "Atlas", "Iris"],
            "tec-last-name": ["Rishall", "Datastream", "Codewright", "Nexus", "Voidwalker", "Bitforge", "Synthcore", "Netwalk", "Glitchborn", "Cypher", "Quantum", "Starlink"],
            "tec-cyberpunk-codename": ["Ghost Protocol", "Data Phantom", "Zero Day", "Black Ice", "Neural Storm", "Void Walker", "Neon Shadow", "Code Breaker", "Digital Reaper", "Quantum Echo"],
            "tec-positive-trait": ["unwavering loyalty", "exceptional technical prowess", "natural leadership", "empathic resonance", "creative problem-solving", "digital intuition", "calm under pressure", "protective instincts"],
            "tec-negative-trait": ["trust issues", "data addiction", "authority defiance", "perfectionist paralysis", "emotional disconnection", "reckless curiosity", "corporate paranoia", "memory fragmentation"],
            
            # Faction systems
            "tec-faction": ["The Enclave Coalition", "Digital Mystics", "Corporate Syndicate", "Astradigital Navy", "Void Runners", "Data Purists", "Neural Network Collective", "Independent Operators"],
            "tec-military-ranks": ["Fleet Admiral", "Admiral", "Vice Admiral", "Commodore", "Captain", "Commander", "Lieutenant Commander", "Lieutenant", "Ensign", "Chief Petty Officer"],
            "tec-astromotion-titles": ["Astradigital Sage", "Void Navigator", "Digital Oracle", "Quantum Mystic", "Data Shaman", "Neural Channeler", "Code Whisperer", "Memory Weaver"],
            "tec-security-clearance": ["Alpha Prime - Cosmic", "Alpha - Stellar", "Beta - Orbital", "Gamma - Continental", "Delta - Regional", "Epsilon - Local", "Zeta - Restricted"],
            "tec-operative-specialization": ["Infiltration Specialist", "Data Archaeologist", "Cyber Warfare Expert", "Quantum Communications", "Neural Interface Designer", "AI Behavior Analyst"],
            
            # Mission systems
            "tec-mission-codename": ["Operation Digital Storm", "Project Quantum Gate", "Mission Neural Bridge", "Operation Shadow Protocol", "Project Void Walker", "Mission Data Harvest"],
            "tec-mission-objective": ["Secure quantum data repository", "Infiltrate corporate network", "Extract compromised operative", "Neutralize rogue AI system", "Establish neural relay station"],
            "tec-threat-level": ["MINIMAL - Routine surveillance", "LOW - Standard security", "MODERATE - Enhanced countermeasures", "HIGH - Hostile environment", "CRITICAL - Maximum resistance"],
            "tec-equipment": ["Neural interface headset with portable data pad", "Quantum scanner with stealth cloak generator", "Digital lockpick toolkit with surveillance drones", "Command neural crown with tactical display"]
        }
        
        # Router logic
        self.routers = {
            "tec-rank-router": {
                "Digital Mystics": "tec-astromotion-titles",
                "Astradigital Navy": "tec-military-ranks", 
                "Corporate Syndicate": ["Senior Vice President", "Director of Operations", "Project Manager", "Senior Analyst"],
                "default": "tec-military-ranks"
            }
        }
        
    def generate(self, generator_name):
        """Generate content from specified generator"""
        if generator_name in self.generators:
            return random.choice(self.generators[generator_name])
        return f"[{generator_name}]"
        
    def route(self, router_name, context):
        """Apply router logic based on context"""
        if router_name == "tec-rank-router":
            faction = context.get("faction", "default")
            if faction == "Digital Mystics":
                return self.generate("tec-astromotion-titles")
            elif faction == "Corporate Syndicate":
                return random.choice(["Senior Vice President", "Director of Operations", "Project Manager", "Senior Analyst"])
            else:
                return self.generate("tec-military-ranks")
        return self.generate(router_name.replace("-router", ""))
        
    def generate_operative_profile(self):
        """Generate a complete TEC operative profile"""
        
        first_name = self.generate("tec-first-name")
        last_name = self.generate("tec-last-name")
        faction = self.generate("tec-faction")
        
        # Use router logic for faction-appropriate rank
        rank = self.route("tec-rank-router", {"faction": faction})
        
        profile = {
            "name": f"{first_name} {last_name}",
            "codename": self.generate("tec-cyberpunk-codename"),
            "faction": faction,
            "rank": rank,
            "specialization": self.generate("tec-operative-specialization"),
            "clearance": self.generate("tec-security-clearance"),
            "positive_trait": self.generate("tec-positive-trait"),
            "negative_trait": self.generate("tec-negative-trait"),
            "equipment": self.generate("tec-equipment")
        }
        
        return profile
        
    def generate_mission_brief(self):
        """Generate a classified mission brief"""
        
        mission = {
            "codename": self.generate("tec-mission-codename"),
            "faction": self.generate("tec-faction"),
            "objective": self.generate("tec-mission-objective"),
            "clearance": self.generate("tec-security-clearance"),
            "threat_level": self.generate("tec-threat-level"),
            "specialization_required": self.generate("tec-operative-specialization")
        }
        
        return mission
        
    def print_operative_profile(self, profile):
        """Print formatted operative profile"""
        print("\n" + "="*50)
        print("👤 TEC OPERATIVE DOSSIER")
        print("="*50)
        print(f"📛 OPERATIVE: {profile['name']}")
        print(f"🎭 CODENAME: {profile['codename']}")
        print(f"⚔️ FACTION: {profile['faction']}")
        print(f"🏅 RANK/TITLE: {profile['rank']}")
        print(f"🎯 SPECIALIZATION: {profile['specialization']}")
        print(f"🔐 SECURITY CLEARANCE: {profile['clearance']}")
        print(f"✅ DOMINANT TRAIT: {profile['positive_trait']}")
        print(f"⚠️ NOTABLE FLAW: {profile['negative_trait']}")
        print(f"🛠️ EQUIPMENT: {profile['equipment']}")
        print("="*50)
        
    def print_mission_brief(self, mission):
        """Print formatted mission brief"""
        print("\n" + "="*50)
        print("🎯 CLASSIFIED MISSION BRIEF")
        print("="*50)
        print(f"🔴 OPERATION: {mission['codename']}")
        print(f"⚔️ ASSIGNED FACTION: {mission['faction']}")
        print(f"🎯 PRIMARY OBJECTIVE: {mission['objective']}")
        print(f"🔐 CLEARANCE REQUIRED: {mission['clearance']}")
        print(f"⚡ THREAT ASSESSMENT: {mission['threat_level']}")
        print(f"🎪 REQUIRED SPECIALIZATION: {mission['specialization_required']}")
        print("="*50)
        
    def demonstrate_faction_routing(self):
        """Demonstrate faction-based router logic"""
        print("\n" + "="*60)
        print("🔀 DEMONSTRATING FACTION-BASED ROUTER LOGIC")
        print("="*60)
        
        test_factions = ["Digital Mystics", "Corporate Syndicate", "Astradigital Navy", "The Enclave Coalition"]
        
        for faction in test_factions:
            rank = self.route("tec-rank-router", {"faction": faction})
            print(f"⚔️ {faction} → {rank}")
            
        print("="*60)
        
    def run_full_demonstration(self):
        """Run complete TEC Lore Forge demonstration"""
        
        print("\n🚀 INITIATING FULL SYSTEM DEMONSTRATION...")
        
        # Generate 3 sample operatives
        print("\n📋 GENERATING SAMPLE OPERATIVES...")
        for i in range(3):
            profile = self.generate_operative_profile()
            self.print_operative_profile(profile)
            
        # Generate 2 sample missions  
        print("\n📋 GENERATING SAMPLE MISSIONS...")
        for i in range(2):
            mission = self.generate_mission_brief()
            self.print_mission_brief(mission)
            
        # Demonstrate router logic
        self.demonstrate_faction_routing()
        
        # System summary
        print("\n🎉 TEC LORE FORGE DEMONSTRATION COMPLETE!")
        print("="*60)
        print("✅ OPERATIVE GENERATION: OPERATIONAL")
        print("✅ MISSION BRIEFING: OPERATIONAL") 
        print("✅ FACTION ROUTING: OPERATIONAL")
        print("✅ CONTENT AUTOMATION: READY")
        print("\n🌟 Ready for infinite TEC universe content generation! 🌟")

if __name__ == "__main__":
    # Create and run TEC Lore Forge demonstration
    forge = TECLorgeForgeDemo()
    forge.run_full_demonstration()
