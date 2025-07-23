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
        
        if not self.api_key:
            print("⚠️  AZURE_AI_API_KEY not found in environment variables")
            print("📝 Please add your API key to the .env file")
            # Use demo mode instead of failing
            self.api_key = "DEMO_MODE"
        
        print(f"🎨 Azure AI Portrait Forge Loading...")
        if self.api_key != "DEMO_MODE":
            print(f"🔑 API Key: {'*' * 20}...{self.api_key[-10:]}")
        else:
            print("🔑 API Key: DEMO MODE (add key to .env for live mode)")
        print(f"🌐 Endpoint: {self.endpoint}")
        print(f"🎤 Speech-to-Text: {self.speech_to_text_endpoint}")
        print(f"🗣️  Text-to-Speech: {self.text_to_speech_endpoint}")
        
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
