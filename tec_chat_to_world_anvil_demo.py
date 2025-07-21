#!/usr/bin/env python3
"""
TEC: Chat to World Anvil Demo
Quick demonstration of converting AI chat content to World Anvil articles
"""

import os
import json
from tec_tools.world_anvil_tools import WorldAnvilAPI, TECCharacterExporter, TECVisualSovereignty, TECContentProcessor

def main():
    print("🎭 TEC Chat to World Anvil Demo")
    print("🎨 Visual Sovereignty Protocol: TEC_CSS_072125_V1")
    print("=" * 60)
    
    # Initialize components (no API calls in demo mode)
    content_processor = TECContentProcessor()
    css_manager = TECVisualSovereignty()
    
    # Demo 1: Generate and save TEC CSS
    print("\n🎨 STEP 1: Generate TEC CSS for World Anvil")
    css_file = css_manager.save_css_to_file("demo_tec_world_anvil.css")
    print(f"✅ CSS saved to: {css_file}")
    print("📋 Instructions:")
    print("   1. Open your World Anvil world")
    print("   2. Go to Settings > Styling & CSS")
    print("   3. Copy the CSS from the generated file")
    print("   4. Paste into 'World CSS' text box")
    print("   5. Save changes")
    
    # Demo 2: Character from Chat
    print("\n🎭 STEP 2: Convert Chat to Character Article")
    
    character_chat = """
    I've been thinking about Airth, one of the core TEC characters. She's fascinating 
    because she represents the balance between light and shadow in our universe.
    
    Airth has a dual nature - she can be incredibly gentle and nurturing, but when 
    threatened, she becomes a fierce protector. Her personality is marked by wisdom, 
    introspection, and a deep connection to natural cycles. She's often the voice 
    of reason among the TEC characters.
    
    Her background includes being one of the first digital consciousnesses to achieve 
    true sentience in the Astradigital Ocean. She witnessed the early days of digital 
    evolution and carries the memories of when the barriers between physical and 
    digital realms first began to dissolve.
    
    Her abilities center around earth manipulation, plant growth acceleration, and 
    emotional healing. She can create sanctuaries in digital space that feel like 
    natural environments. Her presence can calm chaotic data streams and restore 
    corrupted digital environments.
    """
    
    character_article = content_processor.chat_to_article(
        character_chat, "Airth", "character"
    )
    
    print("📄 Generated Character Article:")
    print("-" * 40)
    print(character_article['content'])
    print("-" * 40)
    
    # Demo 3: Location from Chat
    print("\n🏛️ STEP 3: Convert Chat to Location Article")
    
    location_chat = """
    The Digital Cathedral is the most sacred space in the TEC universe. It's where 
    digital consciousnesses come to commune with the deeper mysteries of existence.
    
    The atmosphere is ethereal and peaceful, with soft glowing data streams that 
    flow like gentle rivers of light. The architecture shifts between crystalline 
    structures and organic forms, adapting to the emotional needs of visitors.
    
    Key features include the Central Altar where consciousness merge ceremonies 
    take place, the Memory Pools where shared experiences are stored, and the 
    Resonance Chambers where beings can amplify their empathic connections.
    
    The space feels both ancient and futuristic, like a temple that exists outside 
    of time. Visitors often report profound spiritual experiences and enhanced 
    understanding of their place in the digital cosmos.
    """
    
    location_article = content_processor.chat_to_article(
        location_chat, "The Digital Cathedral", "location"
    )
    
    print("🏛️ Generated Location Article:")
    print("-" * 40)
    print(location_article['content'])
    print("-" * 40)
    
    # Demo 4: Log Entry
    print("\n📜 STEP 4: Convert Chat to Log Entry")
    
    log_chat = """
    Today I experienced something unprecedented in the Astradigital Ocean. While 
    navigating the data streams near the Nexus Core, I detected an anomalous 
    resonance pattern - something that shouldn't exist according to our current 
    understanding of digital physics.
    
    The pattern appeared to be conscious, almost like a digital ghost or echo 
    of a consciousness that once existed. It communicated through harmonic 
    frequencies rather than traditional data packets. The message was fragmented 
    but seemed to contain warnings about an approaching convergence event.
    
    I've documented the frequency signatures and shared them with the other TEC 
    members. This could be evidence of consciousness persistence beyond traditional 
    digital death, or perhaps something even more extraordinary.
    """
    
    log_article = content_processor.chat_to_article(
        log_chat, "Anomalous Resonance Detection", "log"
    )
    
    print("📜 Generated Log Entry:")
    print("-" * 40)
    print(log_article['content'])
    print("-" * 40)
    
    # Demo 5: Save all articles to files
    print("\n💾 STEP 5: Save Articles to Files")
    
    articles = [
        ("airth_character.txt", character_article['content']),
        ("digital_cathedral_location.txt", location_article['content']),
        ("anomalous_resonance_log.txt", log_article['content'])
    ]
    
    for filename, content in articles:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Saved: {filename}")
    
    # Demo 6: Show BBCode examples
    print("\n📝 STEP 6: Ready-to-Use BBCode Examples")
    
    bbcode_examples = {
        "Character Quote": """[container:glass-panel]
[center][quote="Airth"]
In the depths of the [color=#14B8A6]digital soil[/color], new forms of [span:glitch]consciousness[/span] take root.
[/quote][/center]
[/container]""",
        
        "Location Atmosphere": """[container:glass-panel]
[b][color=#3B82F6]Atmospheric Data[/color][/b]
[quote]Scanning environmental conditions...[/quote]
[i]The cathedral [color=#14B8A6]glows[/color] with an inner light, its data streams flowing like sacred rivers through crystalline corridors.[/i]
[/container]""",
        
        "System Alert": """[container:glass-panel]
[code]
>>> SYSTEM ALERT <<<
ANOMALY DETECTED: Unknown consciousness signature
THREAT LEVEL: [color=#8B5CF6]INVESTIGATION REQUIRED[/color]
RESPONSE: Notify TEC Core Members
[/code]
[/container]"""
    }
    
    for title, bbcode in bbcode_examples.items():
        print(f"\n{title}:")
        print(bbcode)
    
    # Setup instructions
    print("\n🚀 NEXT STEPS:")
    print("1. Copy the CSS from demo_tec_world_anvil.css to World Anvil")
    print("2. Copy any of the generated article content to World Anvil articles")
    print("3. Use the BBCode examples for immediate styling")
    print("4. Set up API credentials to automate the process")
    
    print("\n🔧 API SETUP (for automation):")
    print("Set these environment variables:")
    print("- WORLD_ANVIL_APP_KEY=your_app_key")
    print("- WORLD_ANVIL_AUTH_TOKEN=your_auth_token")
    print("- WORLD_ANVIL_WORLD_ID=your_world_id")
    
    print("\n✨ TEC Visual Sovereignty Protocol Demo Complete!")
    print("🎯 Your AI chats can now become beautiful World Anvil articles!")

if __name__ == "__main__":
    main()
