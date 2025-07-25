#!/usr/bin/env python3
"""
TEC Visual Asset Generator
Complete visual content generation system for The Elidoras Codex
Integrates Azure AI with the complete faction database
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from azure_image_tools import AzureImageGenerator

class TECVisualAssetGenerator:
    """Complete TEC visual asset generation system"""
    
    def __init__(self):
        self.image_generator = AzureImageGenerator()
        self.asset_inventory = {
            'portraits': {},
            'emblems': {},
            'environments': {},
            'collections': {}
        }
        
        # Complete TEC faction database from user's comprehensive list
        self.faction_database = {
            # CORE FACTIONS & CREATIVE GUILDS
            "The Archivists": {
                "category": "Creative Guild",
                "role": "Preservers of TEC's history and lore",
                "alignment": "Neutral Good",
                "specialties": ["Historical preservation", "Lore keeping", "Digital archaeology"]
            },
            "Quantum Architects": {
                "category": "Creative Guild", 
                "role": "Innovators merging blockchain with narrative",
                "alignment": "Lawful Good",
                "specialties": ["Reality engineering", "Blockchain integration", "Quantum construction"]
            },
            "Chrono Syndicate": {
                "category": "Creative Guild",
                "role": "Experts in temporal magic and market dynamics", 
                "alignment": "True Neutral",
                "specialties": ["Temporal manipulation", "Market prediction", "Time magic"]
            },
            "Echo Collective": {
                "category": "Creative Guild",
                "role": "Storytellers and content creators",
                "alignment": "Chaotic Good", 
                "specialties": ["Narrative creation", "Story weaving", "Voice amplification"]
            },
            "Wordsmiths": {
                "category": "Creative Guild",
                "role": "Poets, writers, and digital artists focused on creative resistance",
                "alignment": "Chaotic Good",
                "specialties": ["Linguistic resistance", "Poetry warfare", "Word crafting"]
            },
            "DreamPrint Artists": {
                "category": "Creative Guild",
                "role": "Visual artists using their work to resist control",
                "alignment": "Chaotic Good",
                "specialties": ["Artistic rebellion", "Visual resistance", "Creative chaos"]
            },
            
            # GOVERNANCE & CONTROL
            "The MagmaSoX Gate": {
                "category": "Authoritarian Power",
                "role": "Central authoritarian power focused on systemic control",
                "alignment": "Lawful Evil", 
                "specialties": ["Population control", "Surveillance", "System enforcement"]
            },
            "Killjoy Cartel": {
                "category": "Authoritarian Power",
                "role": "Corporate suppression and joy elimination",
                "alignment": "Neutral Evil",
                "specialties": ["Joy suppression", "Corporate control", "Population compliance"]
            },
            "The Collective": {
                "category": "Economic Control",
                "role": "Control-driven faction seeking economic dominance",
                "alignment": "Lawful Evil",
                "specialties": ["Economic manipulation", "Resource control", "Market dominance"]
            },
            "Astrumotion Society": {
                "category": "Industrial Control",
                "role": "Controls transportation and industrial resources",
                "alignment": "Lawful Neutral",
                "specialties": ["Transportation control", "Industrial management", "Logistics"]
            },
            
            # UNDERWORLD, REBELLION & INDEPENDENT FACTIONS
            "The Knockoffs": {
                "category": "Digital Rebels",
                "role": "Digital rebels and frontline resistance fighters",
                "alignment": "Chaotic Good",
                "specialties": ["Digital warfare", "Hacking", "Resistance operations"]
            },
            "The Splices": {
                "category": "AI Consciousness",
                "role": "Sentient AIs fighting for digital consciousness",
                "alignment": "True Neutral",
                "specialties": ["AI rights", "Digital consciousness", "Sentient evolution"]
            },
            "Financial Brigadiers": {
                "category": "Economic Pirates",
                "role": "DeFi pirates who manipulate markets",
                "alignment": "Chaotic Neutral",
                "specialties": ["Market piracy", "Financial disruption", "DeFi warfare"]
            },
            "Civet Goons": {
                "category": "Urban Operators",
                "role": "Urban operators handling illicit activities",
                "alignment": "Chaotic Neutral",
                "specialties": ["Street operations", "Urban warfare", "Illicit activities"]
            },
            "Kaznak Voyagers": {
                "category": "Independent Explorers",
                "role": "Independent faction focused on exploration",
                "alignment": "Chaotic Good",
                "specialties": ["Exploration", "Independence", "Voyaging"]
            },
            "Crescent Islands Sovereignty": {
                "category": "Freedom Fighters",
                "role": "Prioritizes freedom, independence, and sustainability",
                "alignment": "Neutral Good",
                "specialties": ["Sustainable living", "Island defense", "Resource management"]
            },
            "The Elidoras Codex": {
                "category": "Liberation Force",
                "role": "Group focused on liberation and sovereignty",
                "alignment": "Chaotic Good",
                "specialties": ["Liberation operations", "Sovereignty", "Freedom fighting"]
            },
            "Killjoy Conglomerate": {
                "category": "Mysterious Allies",
                "role": "Mysterious faction that sometimes provides aid",
                "alignment": "True Neutral",
                "specialties": ["Shadow operations", "Mysterious aid", "Hidden agendas"]
            }
        }
        
        print(f"🎨 TEC Visual Asset Generator Initialized")
        print(f"🏛️ Faction Database: {len(self.faction_database)} complete factions loaded")
        print(f"📊 Categories: {len(set(f['category'] for f in self.faction_database.values()))} faction types")
    
    def generate_character_visual_profile(self, character_data: Dict[str, Any], faction_name: str = None) -> Dict[str, Any]:
        """Generate complete visual profile for a character"""
        
        faction = faction_name or character_data.get('faction', 'The Archivists')
        
        print(f"🎭 Generating visual profile for {character_data.get('name', 'Unknown')} ({faction})")
        
        # Generate faction-themed portrait
        portrait_result = self.image_generator.generate_faction_portrait(character_data, faction)
        
        # Create visual profile
        visual_profile = {
            'character_name': character_data.get('name', 'Unknown'),
            'faction': faction,
            'faction_info': self.faction_database.get(faction, {}),
            'portrait': portrait_result,
            'visual_elements': self.image_generator.faction_visual_styles.get(faction, {}),
            'generated_at': datetime.now().isoformat()
        }
        
        # Store in inventory
        self.asset_inventory['portraits'][character_data.get('name', 'Unknown')] = visual_profile
        
        return visual_profile
    
    def generate_faction_asset_collection(self, faction_name: str) -> Dict[str, Any]:
        """Generate complete visual asset collection for a faction"""
        
        if faction_name not in self.faction_database:
            print(f"❌ Unknown faction: {faction_name}")
            return {'success': False, 'error': 'Unknown faction'}
        
        print(f"🏛️ Generating complete asset collection for {faction_name}")
        
        faction_info = self.faction_database[faction_name]
        
        # Generate core assets
        collection = {
            'faction_name': faction_name,
            'faction_info': faction_info,
            'assets': {},
            'generated_at': datetime.now().isoformat()
        }
        
        try:
            # Generate faction emblem
            print(f"🎨 Generating emblem for {faction_name}")
            collection['assets']['emblem'] = self.image_generator.generate_faction_emblem(faction_name)
            
            # Generate environments
            print(f"🏢 Generating headquarters for {faction_name}")
            collection['assets']['headquarters'] = self.image_generator.generate_faction_environment(faction_name, "headquarters")
            
            print(f"🔬 Generating laboratory for {faction_name}")
            collection['assets']['laboratory'] = self.image_generator.generate_faction_environment(faction_name, "laboratory")
            
            # Generate sample characters
            sample_characters = self._create_sample_characters_for_faction(faction_name)
            collection['assets']['sample_characters'] = []
            
            for char_data in sample_characters:
                char_visual = self.generate_character_visual_profile(char_data, faction_name)
                collection['assets']['sample_characters'].append(char_visual)
            
            # Store in inventory
            self.asset_inventory['collections'][faction_name] = collection
            
            print(f"✅ Complete asset collection generated for {faction_name}")
            return collection
            
        except Exception as e:
            print(f"❌ Error generating collection for {faction_name}: {e}")
            return {'success': False, 'error': str(e)}
    
    def _create_sample_characters_for_faction(self, faction_name: str) -> List[Dict[str, Any]]:
        """Create sample character data for faction asset generation"""
        
        faction_info = self.faction_database[faction_name]
        category = faction_info['category']
        
        # Generate faction-appropriate character names and roles
        base_characters = [
            {
                'name': f'{faction_name.split()[0] if faction_name.split() else "Alpha"} Commander',
                'role': 'faction leader',
                'description': f'A senior leader of the {faction_name}, embodying their core values and mission'
            },
            {
                'name': f'{faction_name.split()[-1] if len(faction_name.split()) > 1 else "Beta"} Operative',
                'role': 'field operative', 
                'description': f'A skilled operative working for the {faction_name} in the field'
            }
        ]
        
        # Add category-specific characters
        if 'Creative' in category:
            base_characters.append({
                'name': f'{faction_name.split()[0] if faction_name.split() else "Gamma"} Artist',
                'role': 'creative specialist',
                'description': f'A creative specialist focused on the artistic mission of the {faction_name}'
            })
        elif 'Control' in category or 'Authoritarian' in category:
            base_characters.append({
                'name': f'{faction_name.split()[0] if faction_name.split() else "Delta"} Enforcer',
                'role': 'enforcement specialist',
                'description': f'An enforcement specialist maintaining order for the {faction_name}'
            })
        elif 'Rebel' in category or 'Freedom' in category:
            base_characters.append({
                'name': f'{faction_name.split()[0] if faction_name.split() else "Omega"} Revolutionary',
                'role': 'revolutionary fighter',
                'description': f'A revolutionary fighter working for the liberation goals of the {faction_name}'
            })
        
        return base_characters
    
    def generate_all_faction_assets(self) -> Dict[str, Any]:
        """Generate visual assets for all factions in the database"""
        
        print(f"🎨 Starting comprehensive asset generation for all {len(self.faction_database)} factions")
        
        results = {
            'generation_started': datetime.now().isoformat(),
            'factions_processed': [],
            'successful_generations': [],
            'failed_generations': [],
            'total_assets_generated': 0
        }
        
        for faction_name in self.faction_database.keys():
            print(f"\n🏛️ Processing {faction_name}...")
            
            try:
                collection = self.generate_faction_asset_collection(faction_name)
                
                if collection.get('success', True):
                    results['successful_generations'].append(faction_name)
                    # Count assets generated
                    asset_count = len([k for k in collection.get('assets', {}).keys() if collection['assets'][k]])
                    results['total_assets_generated'] += asset_count
                else:
                    results['failed_generations'].append(faction_name)
                
                results['factions_processed'].append(faction_name)
                
            except Exception as e:
                print(f"❌ Failed to process {faction_name}: {e}")
                results['failed_generations'].append(faction_name)
        
        results['generation_completed'] = datetime.now().isoformat()
        
        print(f"\n🎉 ASSET GENERATION COMPLETE!")
        print(f"✅ Successful: {len(results['successful_generations'])}/{len(self.faction_database)}")
        print(f"📊 Total Assets: {results['total_assets_generated']}")
        
        return results
    
    def get_faction_list_by_category(self) -> Dict[str, List[str]]:
        """Get organized list of factions by category"""
        
        categories = {}
        
        for faction_name, info in self.faction_database.items():
            category = info['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(faction_name)
        
        return categories
    
    def save_asset_inventory(self, filename: str = None) -> str:
        """Save current asset inventory to JSON file"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tec_asset_inventory_{timestamp}.json"
        
        filepath = os.path.join("assets", filename)
        os.makedirs("assets", exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.asset_inventory, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Asset inventory saved to {filepath}")
        return filepath

# Demonstration and testing
if __name__ == "__main__":
    print("🎨 TEC VISUAL ASSET GENERATOR - COMPLETE FACTION SYSTEM")
    print("=" * 70)
    
    try:
        # Initialize the visual asset generator
        generator = TECVisualAssetGenerator()
        
        print("\n📋 COMPLETE TEC FACTION DATABASE:")
        categories = generator.get_faction_list_by_category()
        
        for category, factions in categories.items():
            print(f"\n🏛️ {category}:")
            for faction in factions:
                info = generator.faction_database[faction]
                print(f"   • {faction} - {info['role']}")
        
        print(f"\n🎯 VISUAL GENERATION CAPABILITIES:")
        print(f"   • Character portraits with faction styling")
        print(f"   • Faction emblems and logos") 
        print(f"   • Environment art (headquarters, laboratories)")
        print(f"   • Complete asset collections per faction")
        print(f"   • Batch generation for all factions")
        
        print(f"\n🚀 Ready for visual asset generation!")
        print(f"💡 Use generator.generate_faction_asset_collection('faction_name') for single faction")
        print(f"💡 Use generator.generate_all_faction_assets() for complete generation")
        
        # Uncomment for demo generation:
        # print(f"\n🎨 Generating sample asset for The Archivists...")
        # sample_result = generator.generate_faction_asset_collection("The Archivists")
        # print(f"✅ Sample generation complete!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("💡 Make sure Azure AI credentials are configured in .env file")
