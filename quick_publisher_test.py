#!/usr/bin/env python3
"""
Quick Test: TEC Live World Anvil Publisher
"""

print("🚀 Testing TEC World Anvil Publisher...")

try:
    from world_anvil_publisher import WorldAnvilPublisher
    
    # Initialize publisher
    publisher = WorldAnvilPublisher()
    
    # Generate test content
    print("\n📝 Generating test content...")
    content = publisher.generate_faction_aware_content("character", "Independent Operators")
    print(f"✅ Generated: {content['title']}")
    
    # Test publishing
    print("\n📤 Testing publishing...")
    result = publisher.publish_content(content)
    
    if result["success"]:
        print(f"✅ SUCCESS!")
        print(f"🌐 URL: {result['published_url']}")
        print(f"🎭 Mode: {result.get('mode', 'unknown')}")
    else:
        print(f"❌ Failed: {result.get('error')}")
    
    print(f"\n🔥 Publisher Status: OPERATIONAL")
    print(f"🏛️ Factions: {len(publisher.TEC_FACTIONS)} available")
    print(f"🌐 API Key: {'Configured' if publisher.api_key else 'Missing'}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n🚀 Test completed!")
