#!/usr/bin/env python3
"""
🎨 TEC Visual Asset Generator
Faction-aware image generation system with World Anvil integration
"""

import os
import json
import time
from datetime import datetime
from azure_image_tools import AzureImageGenerator

class TecVisualAssetGenerator:
    """Complete visual asset generation system for TEC universe"""
    
    def __init__(self):
        self.azure_generator = AzureImageGenerator()
        self.faction_queue = []
        self.generation_history = []
        
        # Asset storage configuration
        self.asset_storage = {
            'portraits': 'assets/face/portraits/',
            'emblems': 'assets/face/emblems/',
            'environments': 'assets/face/environments/',
            'collections': 'assets/face/collections/'
        }
        
        # Ensure directories exist
        for directory in self.asset_storage.values():
            os.makedirs(directory, exist_ok=True)
        
        print(f"🎨 TEC Visual Asset Generator Initialized")
        print(f"📁 Asset Storage: {len(self.asset_storage)} categories")
        print(f"🎯 Azure AI Generator: {'Live' if self.azure_generator.api_key != 'DEMO_MODE' else 'Demo Mode'}")
    
    def generate_character_visual_profile(self, character_data):
        """Generate complete visual profile for a character"""
        
        character_name = character_data.get('name', 'Unknown')
        faction = character_data.get('faction', 'Independent Operators')
        
        print(f"🎭 Generating visual profile for {character_name}")
        
        visual_profile = {
            'character_name': character_name,
            'faction': faction,
            'generation_timestamp': datetime.now().isoformat(),
            'assets': {}
        }
        
        try:
            # Portrait generation
            print(f"📸 Generating portrait...")
            portrait_result = self.azure_generator.generate_faction_portrait(
                character_data, faction
            )
            visual_profile['assets']['portrait'] = portrait_result
            
            # Add to generation history
            self.generation_history.append({
                'type': 'character_profile',
                'character': character_name,
                'faction': faction,
                'timestamp': datetime.now().isoformat(),
                'success': portrait_result.get('success', False)
            })
            
            print(f"✅ Visual profile generated for {character_name}")
            return visual_profile
            
        except Exception as e:
            print(f"❌ Error generating visual profile: {e}")
            visual_profile['error'] = str(e)
            return visual_profile
    
    def generate_faction_asset_collection(self, faction_name):
        """Generate complete visual asset collection for a faction"""
        
        print(f"🏛️ Generating asset collection for {faction_name}")
        
        collection = {
            'faction_name': faction_name,
            'generation_timestamp': datetime.now().isoformat(),
            'assets': {
                'emblem': None,
                'headquarters': None,
                'laboratory': None,
                'sample_operative': None
            },
            'generation_log': []
        }
        
        try:
            # Generate faction emblem
            print(f"🎖️ Generating faction emblem...")
            emblem_result = self.azure_generator.generate_faction_emblem(faction_name)
            collection['assets']['emblem'] = emblem_result
            collection['generation_log'].append(f"Emblem: {'Success' if emblem_result.get('success') else 'Failed'}")
            
            # Generate headquarters environment
            print(f"🏢 Generating headquarters...")
            hq_result = self.azure_generator.generate_faction_environment(faction_name, "headquarters")
            collection['assets']['headquarters'] = hq_result
            collection['generation_log'].append(f"Headquarters: {'Success' if hq_result.get('success') else 'Failed'}")
            
            # Generate laboratory environment
            print(f"🔬 Generating laboratory...")
            lab_result = self.azure_generator.generate_faction_environment(faction_name, "laboratory")
            collection['assets']['laboratory'] = lab_result
            collection['generation_log'].append(f"Laboratory: {'Success' if lab_result.get('success') else 'Failed'}")
            
            # Generate sample operative
            print(f"👤 Generating sample operative...")
            sample_character = {
                'name': f'{faction_name.split()[0]} Operative',
                'faction': faction_name,
                'role': 'field operative',
                'description': f'A skilled operative representing the {faction_name}'
            }
            operative_result = self.azure_generator.generate_faction_portrait(sample_character, faction_name)
            collection['assets']['sample_operative'] = operative_result
            collection['generation_log'].append(f"Sample Operative: {'Success' if operative_result.get('success') else 'Failed'}")
            
            # Save collection metadata
            collection_file = os.path.join(
                self.asset_storage['collections'], 
                f"{faction_name.replace(' ', '_')}_collection.json"
            )
            with open(collection_file, 'w') as f:
                json.dump(collection, f, indent=2)
            
            print(f"✅ Complete asset collection generated for {faction_name}")
            print(f"📝 Collection saved: {collection_file}")
            
            return collection
            
        except Exception as e:
            print(f"❌ Error generating faction collection: {e}")
            collection['error'] = str(e)
            return collection
    
    def batch_generate_all_factions(self):
        """Generate visual assets for all TEC factions"""
        
        tec_factions = [
            "Independent Operators",
            "Astradigital Research Division", 
            "Neo-Constantinople Guard",
            "The Synthesis Collective",
            "Quantum Liberation Front",
            "Digital Preservation Society",
            "The Evolved"
        ]
        
        print(f"🚀 Starting batch generation for {len(tec_factions)} factions")
        
        batch_results = {
            'start_time': datetime.now().isoformat(),
            'factions': {},
            'summary': {
                'total_factions': len(tec_factions),
                'successful': 0,
                'failed': 0
            }
        }
        
        for i, faction in enumerate(tec_factions, 1):
            print(f"\n📊 Processing {i}/{len(tec_factions)}: {faction}")
            
            try:
                faction_collection = self.generate_faction_asset_collection(faction)
                batch_results['factions'][faction] = faction_collection
                
                if 'error' not in faction_collection:
                    batch_results['summary']['successful'] += 1
                else:
                    batch_results['summary']['failed'] += 1
                    
                # Brief pause between generations
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Failed to process {faction}: {e}")
                batch_results['factions'][faction] = {'error': str(e)}
                batch_results['summary']['failed'] += 1
        
        batch_results['end_time'] = datetime.now().isoformat()
        
        # Save batch results
        batch_file = os.path.join(
            self.asset_storage['collections'],
            f"batch_generation_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        )
        with open(batch_file, 'w') as f:
            json.dump(batch_results, f, indent=2)
        
        print(f"\n🎉 Batch generation complete!")
        print(f"✅ Successful: {batch_results['summary']['successful']}")
        print(f"❌ Failed: {batch_results['summary']['failed']}")
        print(f"📁 Results saved: {batch_file}")
        
        return batch_results
    
    def get_asset_inventory(self):
        """Get current inventory of generated assets"""
        
        inventory = {
            'timestamp': datetime.now().isoformat(),
            'storage_paths': self.asset_storage,
            'collections': [],
            'total_assets': 0
        }
        
        # Scan collections directory
        collections_dir = self.asset_storage['collections']
        if os.path.exists(collections_dir):
            for filename in os.listdir(collections_dir):
                if filename.endswith('.json'):
                    collection_path = os.path.join(collections_dir, filename)
                    try:
                        with open(collection_path, 'r') as f:
                            collection_data = json.load(f)
                        
                        inventory['collections'].append({
                            'filename': filename,
                            'faction': collection_data.get('faction_name', 'Unknown'),
                            'timestamp': collection_data.get('generation_timestamp', 'Unknown'),
                            'assets_count': len([a for a in collection_data.get('assets', {}).values() if a])
                        })
                        
                        inventory['total_assets'] += len([a for a in collection_data.get('assets', {}).values() if a])
                        
                    except Exception as e:
                        print(f"⚠️ Error reading collection {filename}: {e}")
        
        return inventory

def demo_visual_asset_generation():
    """Demonstration of visual asset generation capabilities"""
    
    print("🎨 TEC Visual Asset Generator Demo")
    print("=" * 50)
    
    try:
        # Initialize generator
        generator = TecVisualAssetGenerator()
        
        # Demo character profile generation
        print(f"\n📸 Demo: Character Visual Profile")
        sample_character = {
            'name': 'Delta Prime',
            'faction': 'Independent Operators',
            'role': 'elite hacker',
            'description': 'A cybernetically enhanced hacker with neon green neural implants'
        }
        
        character_profile = generator.generate_character_visual_profile(sample_character)
        print(f"Character profile generated: {character_profile.get('character_name')}")
        
        # Demo faction collection generation
        print(f"\n🏛️ Demo: Faction Asset Collection")
        faction_collection = generator.generate_faction_asset_collection("Independent Operators")
        print(f"Faction collection generated: {len(faction_collection.get('assets', {}))} assets")
        
        # Show inventory
        print(f"\n📊 Current Asset Inventory:")
        inventory = generator.get_asset_inventory()
        print(f"Collections: {len(inventory['collections'])}")
        print(f"Total assets: {inventory['total_assets']}")
        
        print(f"\n✅ Visual Asset Generator demo complete!")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")

if __name__ == "__main__":
    demo_visual_asset_generation()
