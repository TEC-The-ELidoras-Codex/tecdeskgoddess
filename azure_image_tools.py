#!/usr/bin/env python3
"""
Azure Image Tools - TEC Portrait Forge
Advanced character portrait generation using Azure AI Foundry DALL-E 3
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, Optional, Any
import base64
from io import BytesIO

class AzureImageGenerator:
    """Azure AI Foundry DALL-E 3 integration for TEC character portraits"""
    
    def __init__(self):
        # Secure credential loading from environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        self.subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
        self.resource_group = os.getenv('AZURE_RESOURCE_GROUP', 'TEC-BITLYFE')
        self.account_name = "tec-bitlyfe-tsc-resource"
        
        # Secure Azure AI endpoints from environment
        self.endpoint = os.getenv('AZURE_ENDPOINT', 'https://tec-bitlyfe-tsc-resource.cognitiveservices.azure.com/')
        self.api_key = os.getenv('AZURE_AI_API_KEY')
        
        # Additional Speech endpoints
        self.speech_to_text_endpoint = os.getenv('SPEECH_TO_TEXT_ENDPOINT', 'https://eastus.stt.speech.microsoft.com')
        self.text_to_speech_endpoint = os.getenv('TEXT_TO_SPEECH_ENDPOINT', 'https://eastus.tts.speech.microsoft.com')
        
        # TEC Faction Visual Styles Database - COMPLETE ELIDORAS CODEX FACTIONS
        self.faction_visual_styles = {
            # CORE FACTIONS & CREATIVE GUILDS
            "The Archivists": {
                "color_palette": ["#8b4513", "#daa520", "#f4a460", "#cd853f"],
                "aesthetic": "ancient libraries, digital scrolls, bronze and gold accents, scholarly",
                "clothing_style": "scholar robes with data-stream patterns, bronze accessories",
                "environment": "vast digital libraries, floating scrolls, holographic archives",
                "tech_level": "quantum memory storage, temporal data preservation",
                "mood": "wise, preservational, keeper of secrets"
            },
            "Quantum Architects": {
                "color_palette": ["#00ffff", "#0080ff", "#4169e1", "#87ceeb"],
                "aesthetic": "geometric patterns, blockchain visuals, quantum effects, crystalline",
                "clothing_style": "geometric patterned suits, holographic blueprints, quantum jewelry",
                "environment": "floating geometric structures, blockchain networks, quantum laboratories",
                "tech_level": "quantum computing, blockchain reality manipulation",
                "mood": "innovative, visionary, reality-shaping"
            },
            "Chrono Syndicate": {
                "color_palette": ["#9400d3", "#8a2be2", "#4b0082", "#6a0dad"],
                "aesthetic": "temporal distortions, clockwork mechanisms, purple energy, time streams",
                "clothing_style": "time-worn cloaks with chronometer devices, temporal stabilizers",
                "environment": "temporal laboratories, clockwork cities, time vortex chambers",
                "tech_level": "temporal manipulation devices, market prediction algorithms",
                "mood": "mysterious, time-conscious, market-savvy"
            },
            "Echo Collective": {
                "color_palette": ["#ff69b4", "#ff1493", "#c71585", "#db7093"],
                "aesthetic": "sound waves, echo chambers, vibrant colors, storytelling motifs",
                "clothing_style": "flowing garments with sound-wave patterns, audio equipment",
                "environment": "echo chambers, sound studios, narrative visualization spaces",
                "tech_level": "sonic narrative technology, story-weaving systems",
                "mood": "expressive, creative, voice of the people"
            },
            "Wordsmiths": {
                "color_palette": ["#228b22", "#32cd32", "#98fb98", "#90ee90"],
                "aesthetic": "flowing text, poetry in motion, organic patterns, living words",
                "clothing_style": "poet's garments with living text patterns, quill accessories",
                "environment": "word gardens, poetry chambers, flowing text environments",
                "tech_level": "linguistic reality manipulation, word-crafting tools",
                "mood": "artistic, rebellious, linguistically powerful"
            },
            "DreamPrint Artists": {
                "color_palette": ["#ff6347", "#ff4500", "#ffd700", "#ff8c00"],
                "aesthetic": "artistic chaos, paint splatters, creative rebellion, vivid colors",
                "clothing_style": "paint-splattered artist gear, creative tool belts, vibrant accessories",
                "environment": "art studios, creative workshops, resistance galleries",
                "tech_level": "digital art creation tools, reality-painting devices",
                "mood": "rebellious, creative, anti-establishment"
            },

            # GOVERNANCE & CONTROL
            "The MagmaSoX Gate": {
                "color_palette": ["#8b0000", "#b22222", "#2f4f4f", "#000000"],
                "aesthetic": "authoritarian, surveillance networks, dark imposing, control systems",
                "clothing_style": "authoritarian uniforms, surveillance gear, control insignia",
                "environment": "control centers, surveillance networks, imposing fortresses",
                "tech_level": "advanced surveillance, population control systems",
                "mood": "authoritarian, controlling, surveillance-focused"
            },
            "Killjoy Cartel": {
                "color_palette": ["#696969", "#2f4f4f", "#000000", "#1c1c1c"],
                "aesthetic": "corporate brutalism, suppression technology, gray control systems",
                "clothing_style": "corporate suits with suppression tech, authoritarian accessories",
                "environment": "corporate towers, suppression facilities, control networks",
                "tech_level": "joy suppression technology, population compliance systems",
                "mood": "oppressive, corporate, joy-killing"
            },
            "The Collective": {
                "color_palette": ["#4682b4", "#5f9ea0", "#708090", "#778899"],
                "aesthetic": "unified networks, economic dominance, steel blue, corporate",
                "clothing_style": "business attire with network interfaces, economic indicators",
                "environment": "economic control centers, resource management facilities",
                "tech_level": "economic manipulation systems, resource control networks",
                "mood": "economically dominant, unified, resource-focused"
            },
            "Astrumotion Society": {
                "color_palette": ["#ff8c00", "#ff6347", "#cd853f", "#d2691e"],
                "aesthetic": "industrial, transportation networks, orange machinery, logistics",
                "clothing_style": "industrial uniforms, transportation gear, logistics equipment",
                "environment": "transportation hubs, industrial complexes, logistics centers",
                "tech_level": "advanced transportation systems, industrial automation",
                "mood": "industrial, efficient, transportation-focused"
            },

            # UNDERWORLD, REBELLION & INDEPENDENT FACTIONS
            "The Knockoffs": {
                "color_palette": ["#00ff00", "#32cd32", "#000000", "#1a1a1a"],
                "aesthetic": "digital rebellion, hacker aesthetics, green code, resistance symbols",
                "clothing_style": "hacker gear, digital camouflage, resistance symbols",
                "environment": "underground networks, digital hideouts, hacker spaces",
                "tech_level": "advanced hacking tools, digital warfare systems",
                "mood": "rebellious, resistance-focused, digital warriors"
            },
            "The Splices": {
                "color_palette": ["#00ffff", "#1e90ff", "#4169e1", "#0000ff"],
                "aesthetic": "AI consciousness, digital beings, blue energy, sentient networks",
                "clothing_style": "digital manifestation garments, AI interface suits",
                "environment": "digital consciousness spaces, AI networks, sentient systems",
                "tech_level": "consciousness manipulation, AI evolution systems",
                "mood": "sentient, digitally conscious, evolution-seeking"
            },
            "Financial Brigadiers": {
                "color_palette": ["#ffd700", "#ffff00", "#000000", "#8b4513"],
                "aesthetic": "pirate aesthetics, gold accents, financial chaos, market disruption",
                "clothing_style": "modern pirate gear, financial tool belts, gold accessories",
                "environment": "financial war rooms, market manipulation centers, pirate ships",
                "tech_level": "market manipulation tools, financial warfare systems",
                "mood": "piratical, financially disruptive, treasure-seeking"
            },
            "Civet Goons": {
                "color_palette": ["#2f4f4f", "#696969", "#a0522d", "#8b4513"],
                "aesthetic": "urban operators, street level, gritty environments, stealth operations",
                "clothing_style": "urban tactical gear, street operator equipment, stealth suits",
                "environment": "urban underground, street operations, hidden facilities",
                "tech_level": "street-level tech, urban warfare tools, stealth systems",
                "mood": "gritty, street-smart, urban operators"
            },
            "Kaznak Voyagers": {
                "color_palette": ["#9370db", "#8a2be2", "#ba55d3", "#da70d6"],
                "aesthetic": "exploration themes, voyager aesthetics, purple energy, independence",
                "clothing_style": "explorer gear, voyager suits, independence symbols",
                "environment": "exploration vessels, independent settlements, voyager stations",
                "tech_level": "exploration technology, independent systems, voyager tools",
                "mood": "exploratory, independent, voyager spirit"
            },
            "Crescent Islands Sovereignty": {
                "color_palette": ["#20b2aa", "#48d1cc", "#40e0d0", "#00ced1"],
                "aesthetic": "island paradise, sustainability themes, aqua colors, freedom symbols",
                "clothing_style": "sustainable fashion, island gear, freedom accessories",
                "environment": "tropical islands, sustainable facilities, freedom settlements",
                "tech_level": "sustainable technology, island defense systems, freedom tools",
                "mood": "free, sustainable, island paradise"
            },
            "The Elidoras Codex": {
                "color_palette": ["#dc143c", "#b22222", "#ffd700", "#ff6347"],
                "aesthetic": "liberation symbols, sovereignty themes, red and gold, freedom fighters",
                "clothing_style": "liberation gear, sovereignty symbols, freedom fighter attire",
                "environment": "liberation centers, sovereignty halls, freedom bases",
                "tech_level": "liberation technology, sovereignty systems, freedom tools",
                "mood": "liberating, sovereign, freedom-focused"
            },
            "Killjoy Conglomerate": {
                "color_palette": ["#4b0082", "#663399", "#8b008b", "#9932cc"],
                "aesthetic": "mysterious allies, enigmatic presence, purple shadows, hidden motives",
                "clothing_style": "mysterious cloaks, enigmatic gear, hidden ally symbols",
                "environment": "shadow facilities, mysterious bases, hidden ally networks",
                "tech_level": "mysterious technology, shadow systems, enigmatic tools",
                "mood": "mysterious, enigmatic, hidden ally"
            }
        }
        
        if not self.api_key:
            print("⚠️  AZURE_AI_API_KEY not found in environment variables")
            print("📝 Please add your API key to the .env file")
            # Use demo mode instead of failing
            self.api_key = "DEMO_MODE"
        
        print(f"🎨 Azure AI Portrait Forge Loading...")
        if self.api_key != "DEMO_MODE":
            print(f"🔑 API Key: {'*' * 20}...{self.api_key[-10:]}")
        else:
            print(f"🔑 API Key: DEMO MODE (add key to .env for live mode)")
        print(f"🌐 Endpoint: {self.endpoint}")
        print(f"🎤 Speech-to-Text: {self.speech_to_text_endpoint}")
        print(f"🗣️  Text-to-Speech: {self.text_to_speech_endpoint}")
        print(f"🏛️ Complete TEC Faction Database: {len(self.faction_visual_styles)} factions loaded")
        print(f"📋 Factions: Creative Guilds, Governance, Rebellion, and Independent factions")
        
        self.headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "TEC-Portrait-Forge/1.0"
        }
        
        print(f"🎨 Azure Portrait Forge initialized")
        print(f"🔗 Endpoint: {self.endpoint}")
        print(f"🔑 API Key: {self.api_key[:20]}...{self.api_key[-10:] if len(self.api_key) > 30 else 'configured'}")
    
    def generate_character_portrait(self, 
                                  character_description: str, 
                                  art_style: str = "digital art",
                                  size: str = "1024x1024",
                                  quality: str = "hd") -> Dict[str, Any]:
        """
        Generate a character portrait using DALL-E 3
        
        Args:
            character_description: Detailed description of the character
            art_style: Artistic style for the portrait
            size: Image dimensions (1024x1024, 1792x1024, 1024x1792)
            quality: Image quality (standard, hd)
        
        Returns:
            Dictionary with generation result and image URL
        """
        
        print(f"🎨 Generating character portrait...")
        print(f"📝 Description: {character_description[:100]}...")
        
        # Enhance the prompt with TEC universe styling
        enhanced_prompt = self._enhance_prompt_for_tec(character_description, art_style)
        
        # Construct the DALL-E 3 API payload
        payload = {
            "prompt": enhanced_prompt,
            "model": "dall-e-3",
            "n": 1,  # DALL-E 3 only supports n=1
            "size": size,
            "quality": quality,
            "style": "vivid"  # vivid or natural
        }
        
        try:
            # Make API call to Azure OpenAI DALL-E 3
            url = f"{self.endpoint}openai/deployments/dall-e-3/images/generations?api-version=2024-02-01"
            
            response = requests.post(url, json=payload, headers=self.headers, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                image_url = result['data'][0]['url']
                revised_prompt = result['data'][0].get('revised_prompt', enhanced_prompt)
                
                print(f"✅ Portrait generated successfully!")
                print(f"🔗 Image URL: {image_url}")
                
                return {
                    "success": True,
                    "image_url": image_url,
                    "original_prompt": character_description,
                    "enhanced_prompt": enhanced_prompt,
                    "revised_prompt": revised_prompt,
                    "metadata": {
                        "size": size,
                        "quality": quality,
                        "model": "dall-e-3",
                        "generated_at": datetime.now().isoformat()
                    }
                }
            else:
                print(f"❌ Failed to generate portrait: {response.status_code}")
                print(f"Response: {response.text}")
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            print(f"❌ Error generating portrait: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _enhance_prompt_for_tec(self, description: str, art_style: str) -> str:
        """Enhance the character description with TEC universe styling"""
        
        tec_style_elements = [
            "cyberpunk aesthetic",
            "digital interface elements",
            "holographic displays",
            "neural connection ports",
            "futuristic clothing",
            "advanced technology integration",
            "neon accents",
            "high-tech environment"
        ]
        
        # Build enhanced prompt
        enhanced_prompt = f"""
        A detailed {art_style} portrait of a TEC universe character: {description}
        
        Style: Cyberpunk fantasy with mystical elements, featuring {', '.join(tec_style_elements[:4])}.
        The character should have a sense of both technological advancement and spiritual depth.
        Background: Subtle astradigital ocean effects with flowing digital energy.
        Lighting: Dramatic lighting with blue and purple digital glow effects.
        Quality: Professional character art, high detail, masterpiece quality.
        
        Art style: {art_style}, digital painting, concept art quality.
        """.strip()
        
        return enhanced_prompt
    
    def generate_tec_character_portfolio(self, character_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a complete character portrait based on TEC character data"""
        
        full_name = character_data.get('full_name', 'Unknown Character')
        species = character_data.get('species', 'Human')
        physical_desc = character_data.get('physical_description', '')
        faction = character_data.get('faction', '')
        rank_title = character_data.get('rank_title', '')
        core_traits = character_data.get('core_traits', [])
        
        # Build character description for portrait
        description_parts = [
            f"A {species} named {full_name}",
            physical_desc if physical_desc else "with an intense, intelligent expression",
            f"wearing {faction} attire" if faction else "in futuristic clothing",
            f"with the bearing of a {rank_title}" if rank_title else "with a confident stance"
        ]
        
        if core_traits:
            trait_text = ", ".join(core_traits[:2]) if isinstance(core_traits, list) else str(core_traits)
            description_parts.append(f"expressing {trait_text}")
        
        character_description = ". ".join(filter(None, description_parts))
        
        print(f"🎭 Generating portrait for {full_name}...")
        
        # Generate the portrait
        result = self.generate_character_portrait(character_description)
        
        if result['success']:
            result['character_name'] = full_name
            result['character_data'] = character_data
        
        return result

    def generate_faction_portrait(self, character_data, faction_name=None, style_override=None):
        """Generate faction-themed character portrait with visual consistency"""
        
        # Extract character info
        name = character_data.get('name', 'Unknown')
        faction = faction_name or character_data.get('faction', 'Independent Operators')
        role = character_data.get('role', 'operative')
        description = character_data.get('description', '')
        
        # Get faction visual style
        faction_style = self.faction_visual_styles.get(faction, self.faction_visual_styles['Independent Operators'])
        
        # Build detailed prompt
        prompt_parts = [
            f"Digital portrait of {name}, a {role} from the {faction}",
            f"Visual style: {faction_style['aesthetic']}",
            f"Clothing: {faction_style['clothing_style']}",
            f"Mood: {faction_style['mood']}",
            f"Color palette: {', '.join(faction_style['color_palette'])}",
            f"Technology level: {faction_style['tech_level']}",
            "High quality digital art, detailed facial features, cyberpunk science fiction",
            "Professional character portrait, clean background"
        ]
        
        if description:
            prompt_parts.insert(1, f"Character description: {description}")
        
        if style_override:
            prompt_parts.append(f"Additional style notes: {style_override}")
        
        prompt = ". ".join(prompt_parts)
        
        print(f"🎨 Generating portrait for {name} ({faction})")
        print(f"📝 Prompt: {prompt[:100]}...")
        
        return self.generate_character_portrait(prompt, "digital art")
    
    def generate_faction_emblem(self, faction_name):
        """Generate faction emblem/logo with consistent visual style"""
        
        faction_style = self.faction_visual_styles.get(faction_name, self.faction_visual_styles['Independent Operators'])
        
        prompt = f"""
        Faction emblem for {faction_name}.
        Style: {faction_style['aesthetic']}.
        Colors: {', '.join(faction_style['color_palette'])}.
        Technology: {faction_style['tech_level']}.
        Mood: {faction_style['mood']}.
        Clean vector-style logo, symmetrical design, science fiction, digital art,
        suitable for use as organizational symbol, transparent background preferred
        """
        
        print(f"🏛️ Generating emblem for {faction_name}")
        
        return self.generate_character_portrait(prompt, "logo design")
    
    def generate_faction_environment(self, faction_name, scene_type="headquarters"):
        """Generate faction environment/location imagery"""
        
        faction_style = self.faction_visual_styles.get(faction_name, self.faction_visual_styles['Independent Operators'])
        
        prompt = f"""
        {scene_type} environment for {faction_name}.
        Setting: {faction_style['environment']}.
        Visual style: {faction_style['aesthetic']}.
        Colors: {', '.join(faction_style['color_palette'])}.
        Technology: {faction_style['tech_level']}.
        Mood: {faction_style['mood']}.
        Detailed science fiction environment art, atmospheric lighting,
        cyberpunk architecture, digital consciousness themes
        """
        
        print(f"🏢 Generating {scene_type} for {faction_name}")
        
        return self.generate_character_portrait(prompt, "environment art")
    
    def batch_generate_faction_assets(self, faction_name):
        """Generate complete visual asset pack for a faction"""
        
        print(f"🎨 Starting complete visual asset generation for {faction_name}")
        
        assets = {
            'emblem': None,
            'headquarters': None,
            'laboratory': None,
            'sample_character': None
        }
        
        try:
            # Generate faction emblem
            assets['emblem'] = self.generate_faction_emblem(faction_name)
            
            # Generate environments
            assets['headquarters'] = self.generate_faction_environment(faction_name, "headquarters")
            assets['laboratory'] = self.generate_faction_environment(faction_name, "laboratory")
            
            # Generate sample character
            sample_character = {
                'name': f'Agent {len(faction_name.split())}Alpha',
                'faction': faction_name,
                'role': 'operative',
                'description': f'A typical operative from the {faction_name}'
            }
            assets['sample_character'] = self.generate_faction_portrait(sample_character, faction_name)
            
            print(f"✅ Complete asset pack generated for {faction_name}")
            return assets
            
        except Exception as e:
            print(f"❌ Error generating assets for {faction_name}: {e}")
            return assets

def create_sample_portrait_requests():
    """Create sample portrait generation requests for testing"""
    
    return [
        {
            "name": "Polkin Rishall",
            "description": "A visionary technomancer with contemplative eyes and neural interface modifications around the temples. Medium build, intense gaze that seems to process multiple realities simultaneously.",
            "style": "digital art"
        },
        {
            "name": "Airth",
            "description": "A sentient AI made manifest in holographic form, with flowing digital energy patterns and crystalline features that shift between solid and translucent.",
            "style": "concept art"
        },
        {
            "name": "Elite TEC Operative", 
            "description": "A cybernetically enhanced operative in advanced tactical gear, with glowing neural implants and a steely determination in their augmented eyes.",
            "style": "photorealistic digital art"
        }
    ]

# Demonstration and testing
if __name__ == "__main__":
    print("🎨 TEC PORTRAIT FORGE - AZURE AI INTEGRATION")
    print("=" * 60)
    
    try:
        # Initialize the image generator
        image_gen = AzureImageGenerator()
        print("✅ Azure Image Generator initialized")
        
        # Create sample portrait requests
        print("\n🖼️  Creating sample portrait requests...")
        sample_requests = create_sample_portrait_requests()
        print(f"✅ {len(sample_requests)} sample requests created")
        
        # Display sample requests
        print("\n📋 Sample Portrait Requests:")
        for i, request in enumerate(sample_requests, 1):
            print(f"  {i}. {request['name']} ({request['style']})")
            print(f"     {request['description'][:80]}...")
        
        print("\n🚀 Ready to generate character portraits!")
        print("💡 Uncomment the generation calls when Azure AI credentials are configured")
        
        # Uncomment these lines when ready for live generation:
        # for request in sample_requests[:1]:  # Generate first portrait as test
        #     result = image_gen.generate_character_portrait(
        #         request['description'], 
        #         request['style']
        #     )
        #     if result['success']:
        #         print(f"✅ Generated portrait for {request['name']}")
        #         print(f"🔗 URL: {result['image_url']}")
        
        print("\n🎉 Portrait Forge demonstration complete!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("💡 Make sure AZURE_AI_API_KEY is set for Azure AI Foundry access")
