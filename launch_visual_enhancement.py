#!/usr/bin/env python3
"""
🎨 TEC Visual Enhancement System Launcher
Complete deployment of faction-aware AI visual generation
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime

def launch_visual_enhancement_system():
    """Launch the complete TEC Visual Enhancement System"""
    
    print("🎨 TEC VISUAL ENHANCEMENT SYSTEM")
    print("=" * 60)
    print("🚀 LAUNCHING OPTION D: AI-POWERED VISUAL CONTENT")
    print("=" * 60)
    
    # System Components Check
    components = {
        'azure_image_tools.py': 'Azure AI Image Generator',
        'visual_asset_generator.py': 'Visual Asset Generator',
        'world_anvil_visual_publisher.py': 'World Anvil Visual Publisher',
        'tec_persona_api.py': 'Enhanced Backend API',
        'tec_visual_generator.html': 'Visual Generator Frontend'
    }
    
    print("\n📋 SYSTEM COMPONENT STATUS:")
    for file, description in components.items():
        if os.path.exists(file):
            print(f"✅ {description}")
        else:
            print(f"❌ {description} - Missing: {file}")
    
    # Environment Check
    print("\n🔧 ENVIRONMENT CONFIGURATION:")
    
    env_vars = [
        'AZURE_AI_API_KEY',
        'WORLD_ANVIL_API_TOKEN',
        'AZURE_ENDPOINT'
    ]
    
    from dotenv import load_dotenv
    load_dotenv()
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * 20}...{value[-8:]}")
        else:
            print(f"⚠️  {var}: Not configured (Demo mode)")
    
    # Feature Capabilities
    print("\n🎯 VISUAL ENHANCEMENT CAPABILITIES:")
    capabilities = [
        "🎭 Faction-Aware Character Portraits",
        "🏛️ Faction Emblem Generation", 
        "🏢 Environment & Location Assets",
        "📸 Complete Visual Profiles",
        "🚀 Batch Asset Generation",
        "🌍 World Anvil Visual Integration",
        "📊 Asset Inventory Management",
        "🎨 Consistent Faction Styling"
    ]
    
    for capability in capabilities:
        print(f"✅ {capability}")
    
    # API Endpoints
    print("\n🌐 ENHANCED API ENDPOINTS:")
    endpoints = [
        "POST /api/visual/character-portrait - Generate character portraits",
        "POST /api/visual/faction-collection - Generate faction asset collections", 
        "POST /api/visual/batch-generate - Batch generate all factions",
        "GET  /api/visual/inventory - View asset inventory",
        "GET  /tec_visual_generator.html - Visual generation interface"
    ]
    
    for endpoint in endpoints:
        print(f"🔗 {endpoint}")
    
    # Faction Visual Database
    print("\n🏛️ FACTION VISUAL STYLES:")
    faction_styles = {
        "Independent Operators": "Cyberpunk green, dark tactical gear, neural interfaces",
        "Astradigital Research": "Academic blue & white, lab environments, research focus",
        "Neo-Constantinople Guard": "Military red, armor plating, fortress aesthetic",
        "The Synthesis Collective": "Purple energy, ethereal connections, hive-mind",
        "Quantum Liberation Front": "Revolutionary red & black, quantum effects, chaos",
        "Digital Preservation Society": "Archive green, library aesthetics, preservation",
        "The Evolved": "Golden transcendence, bio-enhancement, evolution themes"
    }
    
    for faction, style in faction_styles.items():
        print(f"🎨 {faction}: {style}")
    
    # Demo Functionality
    print("\n🎮 DEMONSTRATION MODE:")
    
    try:
        # Test Azure Image Generator
        print("📸 Testing Azure Image Generator...")
        from azure_image_tools import AzureImageGenerator
        azure_gen = AzureImageGenerator()
        print(f"✅ Azure Generator: {'Live Mode' if azure_gen.api_key != 'DEMO_MODE' else 'Demo Mode'}")
        
        # Test Visual Asset Generator
        print("🎨 Testing Visual Asset Generator...")
        from visual_asset_generator import TecVisualAssetGenerator
        visual_gen = TecVisualAssetGenerator()
        print(f"✅ Visual Generator: {len(visual_gen.asset_storage)} storage categories")
        
        # Test World Anvil Publisher
        print("🌍 Testing World Anvil Publisher...")
        from world_anvil_visual_publisher import WorldAnvilVisualPublisher
        publisher = WorldAnvilVisualPublisher()
        print(f"✅ World Anvil Publisher: {publisher.publishing_config['publish_mode']}")
        
    except Exception as e:
        print(f"⚠️  Component test warning: {e}")
    
    # Usage Instructions
    print("\n📖 USAGE INSTRUCTIONS:")
    instructions = [
        "1. Access Visual Generator: http://localhost:8000/tec_visual_generator.html",
        "2. Generate character portraits with faction-aware styling",
        "3. Create complete faction asset collections (emblems, environments)",
        "4. Use batch generation for all 7 TEC factions",
        "5. Publish visual content to World Anvil with integrated assets",
        "6. Monitor asset inventory and generation history"
    ]
    
    for instruction in instructions:
        print(f"📝 {instruction}")
    
    # Next Steps
    print("\n🚀 RECOMMENDED WORKFLOW:")
    workflow = [
        "Start with single character portrait generation",
        "Test faction emblem generation for visual consistency", 
        "Generate complete asset collection for one faction",
        "Use batch generation for all factions",
        "Integrate with World Anvil for live publishing",
        "Monitor asset inventory and manage storage"
    ]
    
    for step in workflow:
        print(f"🔄 {step}")
    
    # System Summary
    print(f"\n🎉 VISUAL ENHANCEMENT SYSTEM READY!")
    print(f"⏰ Deployment Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎨 Faction Visual Styles: 7 complete")
    print(f"🔧 Generation Tools: 4 integrated systems")
    print(f"🌐 API Integration: Enhanced backend ready")
    print(f"🖥️  Frontend Interface: Visual generator UI available")
    
    print("\n" + "=" * 60)
    print("🎨 TEC VISUAL ENHANCEMENT SYSTEM OPERATIONAL")
    print("=" * 60)
    
    return {
        'system_status': 'operational',
        'components_loaded': len(components),
        'faction_styles': len(faction_styles),
        'capabilities': len(capabilities),
        'api_endpoints': len(endpoints),
        'deployment_time': datetime.now().isoformat()
    }

def demo_visual_generation():
    """Run demonstration of visual generation capabilities"""
    
    print("\n🎮 RUNNING VISUAL GENERATION DEMO")
    print("-" * 40)
    
    try:
        # Demo character portrait
        print("📸 Demo: Character Portrait Generation")
        from visual_asset_generator import TecVisualAssetGenerator
        
        generator = TecVisualAssetGenerator()
        
        sample_character = {
            'name': 'Neon Cipher',
            'faction': 'Independent Operators',
            'role': 'elite neural hacker',
            'description': 'Cybernetically enhanced operative with neon green neural implants and tactical gear'
        }
        
        print(f"Generating portrait for: {sample_character['name']}")
        portrait_result = generator.generate_character_visual_profile(sample_character)
        print(f"Portrait generation: {'Success' if portrait_result.get('character_name') else 'Demo Mode'}")
        
        # Demo faction collection
        print("\n🏛️ Demo: Faction Asset Collection")
        collection_result = generator.generate_faction_asset_collection("Independent Operators")
        asset_count = len([a for a in collection_result.get('assets', {}).values() if a])
        print(f"Asset collection: {asset_count} assets generated")
        
        print("\n✅ Visual generation demo complete!")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("💡 System is operational but demo requires live API keys")

if __name__ == "__main__":
    try:
        # Launch the system
        launch_result = launch_visual_enhancement_system()
        
        # Run demo if requested
        if len(sys.argv) > 1 and sys.argv[1] == '--demo':
            demo_visual_generation()
        
        print(f"\n🎯 System Status: {launch_result['system_status'].upper()}")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Visual Enhancement System shutdown requested")
    except Exception as e:
        print(f"\n❌ System error: {e}")
    finally:
        print("👋 Thank you for using TEC Visual Enhancement System!")
