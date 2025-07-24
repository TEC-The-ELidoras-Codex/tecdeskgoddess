#!/usr/bin/env python3
"""
🚀 TEC LIVE DEPLOYMENT LAUNCHER
Immediate World Anvil publishing with enhanced faction system
"""

import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append('.')

print("🚀 TEC LIVE DEPLOYMENT LAUNCHER")
print("="*60)
print(f"⏰ Launch Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("🎯 Mission: Deploy TEC Faction Content to World Anvil")
print("="*60)

try:
    # Import our enhanced publisher
    from world_anvil_publisher import WorldAnvilPublisher
    
    print("✅ WorldAnvilPublisher loaded successfully!")
    
    # Initialize the publisher
    publisher = WorldAnvilPublisher()
    
    print("\n🎯 DEPLOYMENT SEQUENCE INITIATED")
    print("-"*40)
    
    # Phase 1: Single Content Test
    print("📋 Phase 1: Single Content Test")
    test_content = publisher.generate_faction_aware_content("character", "Independent Operators")
    print(f"   ✅ Generated: {test_content['title']}")
    
    result = publisher.publish_content(test_content)
    if result["success"]:
        print(f"   ✅ Published: {result['published_url']}")
        print(f"   🎭 Mode: {result.get('mode', 'unknown')}")
    else:
        print(f"   ❌ Failed: {result.get('error', 'Unknown')}")
    
    # Phase 2: Faction Showcase
    print(f"\n📋 Phase 2: Faction Showcase")
    showcase_factions = ["Astradigital Research Division", "Quantum Liberation Front"]
    
    for faction in showcase_factions:
        print(f"   🏛️ Processing {faction}...")
        faction_results = publisher.bulk_publish_faction_content(faction, ["character", "organization"])
        successful = len([r for r in faction_results if r["success"]])
        print(f"   ✅ Published {successful}/{len(faction_results)} items for {faction}")
    
    # Phase 3: Status Report
    print(f"\n📋 Phase 3: Deployment Status")
    print(f"   🏛️ Factions Available: {len(publisher.TEC_FACTIONS)}")
    print(f"   🛠️ Content Types: character, location, organization, article")
    print(f"   🌐 API Status: {'Live' if publisher.api_key else 'Simulation'}")
    
    print("\n" + "="*60)
    print("🎉 DEPLOYMENT SEQUENCE COMPLETED!")
    print("="*60)
    
    # Next phase options
    print("🚀 READY FOR ADVANCED DEPLOYMENT:")
    print("   1. Full faction deployment: publisher.publish_all_factions()")
    print("   2. Custom content: publisher.generate_faction_aware_content('type', 'faction')")
    print("   3. Bulk publishing: publisher.bulk_publish_faction_content('faction')")
    
    # Save publisher for interactive use
    globals()['publisher'] = publisher
    print(f"\n💡 Publisher object available as 'publisher' for interactive use")
    
except ImportError as e:
    print(f"❌ Could not import WorldAnvilPublisher: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Deployment error: {e}")
    sys.exit(1)

print(f"\n🔥 TEC Faction System: LIVE AND OPERATIONAL!")
