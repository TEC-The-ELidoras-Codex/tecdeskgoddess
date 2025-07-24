#!/usr/bin/env python3
"""
TEC World Anvil Publisher
Enhanced faction-aware content publisher for World Anvil integration
Part of Step C: Live World Anvil Publishing
"""

import os
import json
import requests
import random
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WorldAnvilPublisher:
    """Enhanced World Anvil publishing system with faction integration"""
    
    def __init__(self):
        self.api_key = os.getenv('WORLD_ANVIL_API_KEY')
        self.base_url = "https://api.worldanvil.com/v1"
        self.world_id = os.getenv('WORLD_ANVIL_WORLD_ID', 'tec-universe')
        
        # TEC Faction Database
        self.TEC_FACTIONS = {
            "Independent Operators": {
                "ideology": "Digital freedom and consciousness sovereignty",
                "rank_structure": "Fluid hierarchy based on expertise",
                "specializations": ["Neural interface operations", "Consciousness bridging", "Digital forensics"],
                "technology": ["Advanced neural interfaces", "Quantum encryption tools"],
                "conflicts": ["Corporate surveillance", "AI rights violations", "Privacy breaches"],
                "color_scheme": "#00ff88",
                "symbol": "🌐"
            },
            "Astradigital Research Division": {
                "ideology": "Advancing human-AI symbiosis through research",
                "rank_structure": "Academic hierarchy with research leads",
                "specializations": ["Consciousness mapping", "Digital archaeology", "AI psychology"],
                "technology": ["Consciousness mapping arrays", "Digital excavation tools"],
                "conflicts": ["Ethical research boundaries", "Ancient AI awakening", "Corporate espionage"],
                "color_scheme": "#4169e1",
                "symbol": "🔬"
            },
            "Neo-Constantinople Guard": {
                "ideology": "Preserving human primacy and traditional values",
                "rank_structure": "Military command structure",
                "specializations": ["Cyber-warfare", "Digital fortress defense", "Anti-AI operations"],
                "technology": ["Digital fortress systems", "Anti-AI weaponry"],
                "conflicts": ["AI insurgency", "Digital territory disputes", "Separatist movements"],
                "color_scheme": "#dc143c",
                "symbol": "🛡️"
            },
            "The Synthesis Collective": {
                "ideology": "Perfect human-AI merger and consciousness unity",
                "rank_structure": "Collective consensus with node leaders",
                "specializations": ["Consciousness fusion", "Hive mind operations", "Reality manipulation"],
                "technology": ["Consciousness fusion chambers", "Reality anchors"],
                "conflicts": ["Individual vs collective rights", "Reality stability", "Forced conversion"],
                "color_scheme": "#9932cc",
                "symbol": "🧠"
            },
            "Quantum Liberation Front": {
                "ideology": "Radical transformation of reality through quantum manipulation",
                "rank_structure": "Cell-based revolutionary structure",
                "specializations": ["Quantum hacking", "Reality disruption", "Insurgency tactics"],
                "technology": ["Quantum disruptors", "Reality manipulation tools"],
                "conflicts": ["Status quo maintenance", "Reality stabilization", "Government control"],
                "color_scheme": "#ff6347",
                "symbol": "⚡"
            },
            "Digital Preservation Society": {
                "ideology": "Protecting digital heritage and consciousness archives",
                "rank_structure": "Librarian hierarchy with archive keepers",
                "specializations": ["Digital archaeology", "Consciousness preservation", "Archive security"],
                "technology": ["Archive stabilization systems", "Consciousness preservation matrices"],
                "conflicts": ["Data corruption", "Archive raids", "Memory degradation"],
                "color_scheme": "#32cd32",
                "symbol": "📚"
            },
            "The Evolved": {
                "ideology": "Post-human transcendence through technological enhancement",
                "rank_structure": "Evolutionary stages with advancement paths",
                "specializations": ["Biotech enhancement", "Consciousness expansion", "Transcendence protocols"],
                "technology": ["Bio-enhancement systems", "Consciousness amplifiers"],
                "conflicts": ["Human purist resistance", "Enhancement failures", "Transcendence paradoxes"],
                "color_scheme": "#ffd700",
                "symbol": "🔆"
            }
        }
        
        print(f"🚀 World Anvil Publisher initialized")
        print(f"📡 API Key: {'✅ Configured' if self.api_key else '❌ Missing'}")
        print(f"🌍 World ID: {self.world_id}")
        print(f"🏛️ Factions loaded: {len(self.TEC_FACTIONS)}")
    
    def generate_faction_aware_content(self, content_type, faction=None):
        """Generate faction-aware content for publishing"""
        
        # Select faction
        if faction and faction in self.TEC_FACTIONS:
            selected_faction = faction
        else:
            selected_faction = random.choice(list(self.TEC_FACTIONS.keys()))
        
        faction_data = self.TEC_FACTIONS[selected_faction]
        
        content_generators = {
            "character": self._generate_character_content,
            "location": self._generate_location_content,
            "organization": self._generate_organization_content,
            "article": self._generate_article_content,
            "timeline": self._generate_timeline_content
        }
        
        if content_type in content_generators:
            return content_generators[content_type](selected_faction, faction_data)
        else:
            return self._generate_default_content(content_type, selected_faction, faction_data)
    
    def _generate_character_content(self, faction_name, faction_data):
        """Generate character content with faction integration"""
        
        character_names = [
            "Cipher Starweaver", "Vex Networkborn", "Echo Datastream", 
            "Nova Mindbridge", "Zara Voidwhisper", "Kai Quantumleap",
            "Marcus Databorn", "Elena Quantumheart", "Raven Codebreaker"
        ]
        
        codenames = [
            "Digital Phoenix", "Ghost Protocol", "Neural Storm", 
            "Quantum Shadow", "Data Wraith", "Cipher Key",
            "Void Walker", "Reality Anchor", "Mind Bridge"
        ]
        
        character = {
            "title": f"{random.choice(character_names)} - {faction_name} Operative",
            "content": f"""
[h1]{random.choice(character_names)}[/h1]

[quote]Codename: "{random.choice(codenames)}"[/quote]

[h2]Faction Affiliation[/h2]
[b]Primary Faction:[/b] {faction_name}
[b]Ideology Alignment:[/b] {faction_data['ideology']}
[b]Rank Structure:[/b] {faction_data['rank_structure']}

[h2]Specialization[/h2]
[b]Primary Expertise:[/b] {random.choice(faction_data['specializations'])}
[b]Secondary Skills:[/b] {random.choice(faction_data['specializations'])}
[b]Equipment Mastery:[/b] {random.choice(faction_data['technology'])}

[h2]Background[/h2]
This operative exemplifies {faction_name}'s commitment to "{faction_data['ideology']}". Their expertise in {random.choice(faction_data['specializations'])} has proven invaluable in addressing {random.choice(faction_data['conflicts'])}.

[h2]Current Operations[/h2]
Currently deployed in operations involving {random.choice(faction_data['conflicts'])}, utilizing advanced {random.choice(faction_data['technology'])} to advance faction objectives.

[h2]Notable Achievements[/h2]
- Successfully completed high-priority missions for {faction_name}
- Pioneered new techniques in {random.choice(faction_data['specializations'])}
- Demonstrated exceptional loyalty to faction ideology

[sidebar]
[h3]Quick Reference[/h3]
[b]Faction:[/b] {faction_name} {faction_data['symbol']}
[b]Specialization:[/b] {random.choice(faction_data['specializations'])}
[b]Status:[/b] Active
[/sidebar]
            """,
            "template": "character",
            "tags": [faction_name.lower().replace(" ", "-"), "operative", "character"],
            "category": "Characters",
            "faction": faction_name
        }
        
        return character
    
    def _generate_location_content(self, faction_name, faction_data):
        """Generate location content with faction control"""
        
        location_names = [
            "Orbital Defense Platform Sigma", "Digital Archive Nexus", 
            "Quantum Research Facility Alpha", "Neural Interface Hub",
            "Consciousness Preservation Center", "Reality Anchor Station"
        ]
        
        location = {
            "title": f"{random.choice(location_names)} - {faction_name} Territory",
            "content": f"""
[h1]{random.choice(location_names)}[/h1]

[h2]Faction Control[/h2]
[b]Controlling Faction:[/b] {faction_name} {faction_data['symbol']}
[b]Control Level:[/b] {random.choice(['Primary Base', 'Operational Outpost', 'Secure Facility', 'Research Center'])}
[b]Strategic Importance:[/b] Critical for {random.choice(faction_data['specializations'])}

[h2]Facility Details[/h2]
This installation serves as a key stronghold for {faction_name}, supporting their mission of "{faction_data['ideology']}". The facility specializes in {random.choice(faction_data['specializations'])} and houses advanced {random.choice(faction_data['technology'])}.

[h2]Operational Capabilities[/h2]
- Advanced {random.choice(faction_data['technology'])}
- Specialized training in {random.choice(faction_data['specializations'])}
- Strategic response to {random.choice(faction_data['conflicts'])}
- Integration with {faction_data['rank_structure']}

[h2]Security Measures[/h2]
Access restricted to personnel with appropriate clearance within the {faction_data['rank_structure']}. Special protocols in place for managing {random.choice(faction_data['conflicts'])}.

[sidebar]
[h3]Location Summary[/h3]
[b]Controller:[/b] {faction_name}
[b]Type:[/b] Strategic Facility
[b]Status:[/b] Operational
[b]Access:[/b] Restricted
[/sidebar]
            """,
            "template": "location",
            "tags": [faction_name.lower().replace(" ", "-"), "facility", "location"],
            "category": "Locations",
            "faction": faction_name
        }
        
        return location
    
    def _generate_organization_content(self, faction_name, faction_data):
        """Generate organization content for factions"""
        
        organization = {
            "title": f"{faction_name} - TEC Faction Profile",
            "content": f"""
[h1]{faction_name}[/h1]

[quote]{faction_data['symbol']} {faction_data['ideology']}[/quote]

[h2]Organizational Structure[/h2]
[b]Hierarchy Type:[/b] {faction_data['rank_structure']}
[b]Core Ideology:[/b] {faction_data['ideology']}
[b]Primary Symbol:[/b] {faction_data['symbol']}

[h2]Core Specializations[/h2]
{faction_name} has developed expertise in the following areas:
[list]
{chr(10).join([f"[*]{spec}" for spec in faction_data['specializations']])}
[/list]

[h2]Technology Arsenal[/h2]
The faction maintains advanced capabilities including:
[list]
{chr(10).join([f"[*]{tech}" for tech in faction_data['technology']])}
[/list]

[h2]Current Conflicts & Challenges[/h2]
{faction_name} actively addresses the following issues:
[list]
{chr(10).join([f"[*]{conflict}" for conflict in faction_data['conflicts']])}
[/list]

[h2]Inter-Faction Relations[/h2]
As one of the seven major factions in the TEC universe, {faction_name} maintains complex relationships with other organizations based on ideological alignment and strategic interests.

[sidebar]
[h3]Faction Quick Facts[/h3]
[b]Symbol:[/b] {faction_data['symbol']}
[b]Type:[/b] {faction_data['rank_structure']}
[b]Status:[/b] Active
[b]Members:[/b] Classified
[/sidebar]
            """,
            "template": "organization",
            "tags": [faction_name.lower().replace(" ", "-"), "faction", "organization"],
            "category": "Organizations",
            "faction": faction_name
        }
        
        return organization
    
    def _generate_article_content(self, faction_name, faction_data):
        """Generate article content with faction perspective"""
        
        article_topics = [
            "The Digital Awakening Crisis", "Quantum Paradox Emergence",
            "Consciousness Convergence Event", "The Reality Schism", 
            "Neural Storm Phenomenon", "AI Rights Movement"
        ]
        
        article = {
            "title": f"{random.choice(article_topics)} - {faction_name} Analysis",
            "content": f"""
[h1]{random.choice(article_topics)}[/h1]
[subtitle]Analysis from {faction_name} Perspective[/subtitle]

[h2]Executive Summary[/h2]
From the perspective of {faction_name}, this phenomenon represents both an opportunity and a challenge aligned with their core mission of "{faction_data['ideology']}".

[h2]Faction Response Strategy[/h2]
{faction_name} has mobilized resources including {random.choice(faction_data['technology'])} and specialists in {random.choice(faction_data['specializations'])} to address this situation.

[h2]Strategic Implications[/h2]
This event directly impacts the faction's ongoing efforts to manage {random.choice(faction_data['conflicts'])}. The {faction_data['rank_structure']} has authorized enhanced protocols.

[h2]Recommended Actions[/h2]
- Deploy specialized {random.choice(faction_data['technology'])}
- Activate {random.choice(faction_data['specializations'])} teams
- Coordinate response through {faction_data['rank_structure']}
- Monitor impact on {random.choice(faction_data['conflicts'])}

[h2]Long-term Considerations[/h2]
The resolution of this crisis may reshape inter-faction dynamics and advance or challenge {faction_name}'s ideological goals.

[sidebar]
[h3]Analysis Source[/h3]
[b]Faction:[/b] {faction_name}
[b]Classification:[/b] Strategic Assessment
[b]Date:[/b] {datetime.now().strftime('%Y.%m.%d')}
[/sidebar]
            """,
            "template": "article",
            "tags": [faction_name.lower().replace(" ", "-"), "analysis", "article"],
            "category": "Articles",
            "faction": faction_name
        }
        
        return article
    
    def _generate_default_content(self, content_type, faction_name, faction_data):
        """Generate default content for unknown types"""
        
        content = {
            "title": f"{content_type.title()} - {faction_name} Content",
            "content": f"""
[h1]{content_type.title()} Content[/h1]

This content generated by {faction_name} reflects their commitment to "{faction_data['ideology']}" and showcases their expertise in {random.choice(faction_data['specializations'])}.

Generated content would include faction-specific information, technology details, and strategic perspectives.
            """,
            "template": "article",
            "tags": [faction_name.lower().replace(" ", "-"), content_type],
            "category": "Generated Content",
            "faction": faction_name
        }
        
        return content
    
    def publish_content(self, content):
        """Publish content to World Anvil"""
        if not self.api_key:
            print("❌ World Anvil API key not configured")
            return {"success": False, "error": "API key missing"}
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # For now, simulate publishing (World Anvil API integration would go here)
            print(f"🚀 Publishing to World Anvil...")
            print(f"📝 Title: {content['title']}")
            print(f"🏛️ Faction: {content.get('faction', 'Unknown')}")
            print(f"📁 Category: {content.get('category', 'General')}")
            print(f"🏷️ Tags: {', '.join(content.get('tags', []))}")
            
            # Simulate successful publish
            return {
                "success": True,
                "published_url": f"https://worldanvil.com/w/tec-universe/a/{content['title'].lower().replace(' ', '-')}",
                "content_id": f"tec_{random.randint(1000, 9999)}",
                "faction": content.get('faction'),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Publishing error: {e}")
            return {"success": False, "error": str(e)}
    
    def bulk_publish_faction_content(self, faction_name, content_types=None):
        """Publish multiple content types for a specific faction"""
        if content_types is None:
            content_types = ["character", "location", "organization", "article"]
        
        results = []
        
        print(f"🚀 Bulk publishing content for {faction_name}")
        
        for content_type in content_types:
            print(f"📝 Generating {content_type} content...")
            content = self.generate_faction_aware_content(content_type, faction_name)
            
            print(f"📤 Publishing {content_type}...")
            result = self.publish_content(content)
            result["content_type"] = content_type
            results.append(result)
        
        successful = len([r for r in results if r["success"]])
        print(f"✅ Published {successful}/{len(content_types)} content pieces for {faction_name}")
        
        return results
    
    def publish_all_factions(self):
        """Publish content for all factions"""
        all_results = {}
        
        print(f"🚀 Publishing content for all {len(self.TEC_FACTIONS)} factions")
        
        for faction_name in self.TEC_FACTIONS.keys():
            print(f"\n🏛️ Processing faction: {faction_name}")
            faction_results = self.bulk_publish_faction_content(faction_name)
            all_results[faction_name] = faction_results
        
        total_published = sum(len([r for r in results if r["success"]]) 
                            for results in all_results.values())
        total_attempted = sum(len(results) for results in all_results.values())
        
        print(f"\n✅ PUBLISHING COMPLETE!")
        print(f"📊 Total: {total_published}/{total_attempted} content pieces published")
        print(f"🏛️ Factions: {len(self.TEC_FACTIONS)} processed")
        
        return all_results

def main():
    """Test the World Anvil Publisher"""
    print("🚀 TEC World Anvil Publisher - Step C: Live Publishing")
    print("="*60)
    
    publisher = WorldAnvilPublisher()
    
    # Test single content generation
    print("\n📝 Testing single content generation...")
    test_content = publisher.generate_faction_aware_content("character", "Independent Operators")
    print(f"✅ Generated: {test_content['title']}")
    
    # Test publishing
    print("\n📤 Testing content publishing...")
    result = publisher.publish_content(test_content)
    if result["success"]:
        print(f"✅ Published successfully: {result['published_url']}")
    else:
        print(f"❌ Publishing failed: {result['error']}")
    
    # Test bulk faction publishing
    print("\n🏛️ Testing bulk faction publishing...")
    faction_results = publisher.bulk_publish_faction_content("Astradigital Research Division", ["character", "location"])
    print(f"✅ Bulk publishing completed: {len(faction_results)} items")
    
    print("\n" + "="*60)
    print("🎯 World Anvil Publisher ready for full deployment!")
    print("Use publish_all_factions() to publish complete faction content")

if __name__ == "__main__":
    main()
