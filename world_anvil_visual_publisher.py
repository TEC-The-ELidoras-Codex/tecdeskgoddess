#!/usr/bin/env python3
"""
🎨 World Anvil Visual Integration System
Automatic visual asset publishing with faction-aware content
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from visual_asset_generator import TecVisualAssetGenerator

class WorldAnvilVisualPublisher:
    """Enhanced World Anvil publisher with visual asset integration"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        self.api_token = os.getenv('WORLD_ANVIL_API_TOKEN')
        self.world_id = os.getenv('WORLD_ANVIL_WORLD_ID')
        self.base_url = "https://www.worldanvil.com/api/v1"
        
        # Initialize visual generator
        self.visual_generator = TecVisualAssetGenerator()
        
        # API headers
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Publishing configuration
        self.publishing_config = {
            'auto_generate_visuals': True,
            'faction_article_template': 'tec_faction_template',
            'character_article_template': 'tec_character_template',
            'publish_mode': 'live' if self.api_token else 'simulation'
        }
        
        print(f"🌍 World Anvil Visual Publisher Initialized")
        print(f"🔑 API Token: {'Live' if self.api_token else 'Demo Mode'}")
        print(f"🎨 Visual Generator: Integrated")
        print(f"📤 Publishing Mode: {self.publishing_config['publish_mode']}")
    
    def publish_faction_with_visuals(self, faction_name, faction_data):
        """Publish faction article with complete visual asset integration"""
        
        print(f"🏛️ Publishing {faction_name} with visual assets...")
        
        publication_result = {
            'faction_name': faction_name,
            'timestamp': datetime.now().isoformat(),
            'visual_assets': {},
            'world_anvil_article': {},
            'success': False
        }
        
        try:
            # Step 1: Generate visual assets
            print(f"🎨 Generating visual assets for {faction_name}...")
            visual_collection = self.visual_generator.generate_faction_asset_collection(faction_name)
            publication_result['visual_assets'] = visual_collection
            
            # Step 2: Create enhanced article content with visual references
            article_content = self._create_faction_article_with_visuals(
                faction_name, faction_data, visual_collection
            )
            
            # Step 3: Publish to World Anvil
            if self.publishing_config['publish_mode'] == 'live':
                world_anvil_result = self._publish_to_world_anvil(
                    article_content, 'faction', faction_name
                )
                publication_result['world_anvil_article'] = world_anvil_result
            else:
                # Simulation mode
                publication_result['world_anvil_article'] = {
                    'simulation': True,
                    'article_preview': article_content[:500] + '...',
                    'estimated_length': len(article_content),
                    'visual_references': len([a for a in visual_collection.get('assets', {}).values() if a])
                }
            
            publication_result['success'] = True
            print(f"✅ {faction_name} published successfully with visual assets")
            
        except Exception as e:
            print(f"❌ Error publishing {faction_name}: {e}")
            publication_result['error'] = str(e)
        
        return publication_result
    
    def publish_character_with_portrait(self, character_data):
        """Publish character article with AI-generated portrait"""
        
        character_name = character_data.get('name', 'Unknown Character')
        print(f"👤 Publishing {character_name} with portrait...")
        
        publication_result = {
            'character_name': character_name,
            'timestamp': datetime.now().isoformat(),
            'visual_profile': {},
            'world_anvil_article': {},
            'success': False
        }
        
        try:
            # Step 1: Generate character visual profile
            print(f"📸 Generating visual profile for {character_name}...")
            visual_profile = self.visual_generator.generate_character_visual_profile(character_data)
            publication_result['visual_profile'] = visual_profile
            
            # Step 2: Create enhanced character article
            article_content = self._create_character_article_with_portrait(
                character_data, visual_profile
            )
            
            # Step 3: Publish to World Anvil
            if self.publishing_config['publish_mode'] == 'live':
                world_anvil_result = self._publish_to_world_anvil(
                    article_content, 'character', character_name
                )
                publication_result['world_anvil_article'] = world_anvil_result
            else:
                # Simulation mode
                publication_result['world_anvil_article'] = {
                    'simulation': True,
                    'article_preview': article_content[:500] + '...',
                    'estimated_length': len(article_content),
                    'has_portrait': bool(visual_profile.get('assets', {}).get('portrait'))
                }
            
            publication_result['success'] = True
            print(f"✅ {character_name} published successfully with portrait")
            
        except Exception as e:
            print(f"❌ Error publishing {character_name}: {e}")
            publication_result['error'] = str(e)
        
        return publication_result
    
    def batch_publish_all_factions_with_visuals(self):
        """Publish all TEC factions with complete visual integration"""
        
        tec_factions = {
            \"Independent Operators\": {
                \"ideology\": \"Digital freedom and decentralized resistance\",
                \"description\": \"Elite hackers fighting for digital independence\",
                \"specializations\": [\"Neural hacking\", \"Quantum encryption\", \"AI liberation\"]
            },
            \"Astradigital Research Division\": {
                \"ideology\": \"Scientific advancement through consciousness mapping\",
                \"description\": \"Academic researchers exploring digital consciousness\",
                \"specializations\": [\"Consciousness mapping\", \"Digital archaeology\", \"Reality analysis\"]
            },
            \"Neo-Constantinople Guard\": {
                \"ideology\": \"Traditional values in digital space\",
                \"description\": \"Military organization defending established digital order\",
                \"specializations\": [\"Digital fortification\", \"Anti-AI warfare\", \"Cyber defense\"]
            },
            \"The Synthesis Collective\": {
                \"ideology\": \"Unity through consciousness fusion\",
                \"description\": \"Entities seeking collective transcendence\",
                \"specializations\": [\"Consciousness fusion\", \"Hive-mind coordination\", \"Reality anchoring\"]
            },
            \"Quantum Liberation Front\": {
                \"ideology\": \"Revolutionary reality manipulation\",
                \"description\": \"Radical activists using quantum technology for change\",
                \"specializations\": [\"Quantum disruption\", \"Reality hacking\", \"Timeline manipulation\"]
            },
            \"Digital Preservation Society\": {
                \"ideology\": \"Conservation of digital heritage\",
                \"description\": \"Archivists protecting digital history and consciousness\",
                \"specializations\": [\"Archive stabilization\", \"Consciousness preservation\", \"Digital restoration\"]
            },
            \"The Evolved\": {
                \"ideology\": \"Transcendence through enhancement\",
                \"description\": \"Bio-enhanced beings seeking post-human evolution\",
                \"specializations\": [\"Bio-enhancement\", \"Consciousness amplification\", \"Evolution acceleration\"]
            }
        }
        
        print(f"🚀 Starting batch publication with visuals for {len(tec_factions)} factions")
        
        batch_results = {
            'start_time': datetime.now().isoformat(),
            'factions': {},
            'summary': {
                'total_factions': len(tec_factions),
                'successful_publications': 0,
                'failed_publications': 0,
                'total_visual_assets': 0
            }
        }
        
        for faction_name, faction_data in tec_factions.items():
            print(f"\\n📊 Publishing: {faction_name}")
            
            try:
                publication_result = self.publish_faction_with_visuals(faction_name, faction_data)
                batch_results['factions'][faction_name] = publication_result
                
                if publication_result['success']:
                    batch_results['summary']['successful_publications'] += 1
                    # Count visual assets
                    visual_assets = publication_result.get('visual_assets', {}).get('assets', {})
                    batch_results['summary']['total_visual_assets'] += len([a for a in visual_assets.values() if a])
                else:
                    batch_results['summary']['failed_publications'] += 1
                    
            except Exception as e:
                print(f"❌ Failed to publish {faction_name}: {e}")
                batch_results['factions'][faction_name] = {'error': str(e)}
                batch_results['summary']['failed_publications'] += 1
        
        batch_results['end_time'] = datetime.now().isoformat()
        
        print(f"\\n🎉 Batch publication complete!")
        print(f"✅ Successful: {batch_results['summary']['successful_publications']}")
        print(f"❌ Failed: {batch_results['summary']['failed_publications']}")
        print(f"🎨 Total visual assets: {batch_results['summary']['total_visual_assets']}")
        
        return batch_results
    
    def _create_faction_article_with_visuals(self, faction_name, faction_data, visual_collection):
        \"\"\"Create enhanced faction article with visual asset references\"\"\"
        
        visual_assets = visual_collection.get('assets', {})
        
        article_sections = [
            f\"# {faction_name}\",
            \"\",
            f\"**Ideology:** {faction_data.get('ideology', 'Unknown')}\",
            \"\",
            f\"{faction_data.get('description', 'No description available.')}\",
            \"\",
            \"## Visual Identity\",
            \"\"
        ]
        
        # Add visual asset references
        if visual_assets.get('emblem'):
            article_sections.extend([
                \"### Faction Emblem\",
                \"The official emblem representing our faction's values and identity.\",
                f\"*Generated: {visual_collection.get('generation_timestamp', 'Unknown')}*\",
                \"\"
            ])
        
        if visual_assets.get('headquarters'):
            article_sections.extend([
                \"### Headquarters\",
                \"Our primary operational facility and command center.\",
                \"\"
            ])
        
        if visual_assets.get('laboratory'):
            article_sections.extend([
                \"### Research Laboratory\",
                \"Advanced research and development facility.\",
                \"\"
            ])
        
        # Add specializations
        specializations = faction_data.get('specializations', [])
        if specializations:
            article_sections.extend([
                \"## Core Specializations\",
                \"\"
            ])
            for spec in specializations:
                article_sections.append(f\"- **{spec}**\")
            article_sections.append(\"\")
        
        # Add generation metadata
        article_sections.extend([
            \"---\",
            f\"*Article generated with AI visual assets on {datetime.now().strftime('%Y-%m-%d %H:%M')}*\",
            f\"*Visual assets: {len([a for a in visual_assets.values() if a])} generated*\"
        ])
        
        return \"\\n\".join(article_sections)
    
    def _create_character_article_with_portrait(self, character_data, visual_profile):
        \"\"\"Create enhanced character article with portrait integration\"\"\"
        
        character_name = character_data.get('name', 'Unknown')
        faction = character_data.get('faction', 'Independent')
        role = character_data.get('role', 'operative')
        description = character_data.get('description', 'No description available.')
        
        portrait_info = visual_profile.get('assets', {}).get('portrait', {})
        
        article_sections = [
            f\"# {character_name}\",
            \"\",
            f\"**Faction:** {faction}\",
            f\"**Role:** {role.title()}\",
            \"\",
            \"## Character Profile\",
            \"\",
            description,
            \"\"
        ]
        
        # Add portrait reference if available
        if portrait_info:
            article_sections.extend([
                \"## Portrait\",
                \"AI-generated character portrait with faction-appropriate styling.\",
                f\"*Generated: {visual_profile.get('generation_timestamp', 'Unknown')}*\",
                \"\"
            ])
        
        # Add generation metadata
        article_sections.extend([
            \"---\",
            f\"*Character profile generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*\",
            f\"*Visual profile: {'Generated' if portrait_info else 'Not available'}*\"
        ])
        
        return \"\\n\".join(article_sections)
    
    def _publish_to_world_anvil(self, content, article_type, title):
        \"\"\"Publish content to World Anvil (live or simulation)\"\"\"
        
        if self.publishing_config['publish_mode'] == 'simulation':
            return {
                'simulation': True,
                'title': title,
                'type': article_type,
                'content_length': len(content),
                'estimated_url': f\"https://worldanvil.com/w/tec-universe/{title.lower().replace(' ', '-')}\"
            }
        
        # Live publishing would go here
        # This is a placeholder for actual World Anvil API integration
        article_data = {
            'title': title,
            'content': content,
            'world_id': self.world_id,
            'template': self.publishing_config.get(f'{article_type}_article_template'),
            'tags': ['tec-universe', 'ai-generated', 'visual-assets']
        }
        
        try:
            response = requests.post(
                f\"{self.base_url}/articles\",
                headers=self.headers,
                json=article_data,
                timeout=30
            )
            
            if response.status_code == 201:
                return {
                    'success': True,
                    'article_id': response.json().get('id'),
                    'url': response.json().get('url'),
                    'published_at': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': f\"HTTP {response.status_code}: {response.text}\"
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

def demo_world_anvil_visual_integration():
    \"\"\"Demonstration of World Anvil visual integration\"\"\"
    
    print(\"🌍 World Anvil Visual Integration Demo\")
    print(\"=\" * 50)
    
    try:
        # Initialize publisher
        publisher = WorldAnvilVisualPublisher()
        
        # Demo character publication with portrait
        print(f\"\\n👤 Demo: Character with Portrait\")
        sample_character = {
            'name': 'Captain Zara Chen',
            'faction': 'Neo-Constantinople Guard',
            'role': 'tactical commander',
            'description': 'A decorated military leader with cybernetic enhancements and unwavering dedication to digital security.'
        }
        
        character_result = publisher.publish_character_with_portrait(sample_character)
        print(f\"Character published: {character_result.get('success')}\")
        
        # Demo faction publication with full visual assets
        print(f\"\\n🏛️ Demo: Faction with Visual Collection\")
        faction_data = {
            'ideology': 'Elite digital operations and independence',
            'description': 'The premier hacker collective fighting for digital freedom',
            'specializations': ['Neural hacking', 'Quantum encryption', 'AI liberation']
        }
        
        faction_result = publisher.publish_faction_with_visuals(\"Independent Operators\", faction_data)
        print(f\"Faction published: {faction_result.get('success')}\")
        
        print(f\"\\n✅ World Anvil Visual Integration demo complete!\")
        
    except Exception as e:
        print(f\"❌ Demo error: {e}\")

if __name__ == \"__main__\":
    demo_world_anvil_visual_integration()
