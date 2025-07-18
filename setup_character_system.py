"""
Setup and Test Script for Enhanced TEC Character Memory System
"""

import json
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, 'src')
sys.path.insert(0, '.')

from src.tec_tools.token_manager import TECTokenManager
from src.tec_tools.character_memory_system import TECCharacterMemorySystem

def setup_character_memories():
    """Import character lore and set up memory system"""
    print("🔮 Setting up TEC Enhanced Character Memory System...")
    
    # Initialize systems
    character_memory_system = TECCharacterMemorySystem()
    token_manager = TECTokenManager()
    
    # Load character lore
    lore_path = Path("data/character_lore.json")
    if not lore_path.exists():
        print("❌ Character lore file not found!")
        return False
    
    try:
        with open(lore_path, 'r') as f:
            character_data = json.load(f)
        
        print(f"📚 Loading memories for {len(character_data['characters'])} characters...")
        
        # Import character memories
        success = character_memory_system.import_character_memories(character_data)
        
        if success:
            print("✅ Character memories imported successfully!")
            
            # Test character context generation
            print("\n🧪 Testing character context generation...")
            
            # Test Polkin context
            polkin_context = character_memory_system.get_character_context(
                character_name="Polkin Rishall",
                query="I'm struggling with trauma from my past",
                max_memories=3
            )
            
            print(f"Polkin context: {polkin_context['total_memories']} relevant memories found")
            print(f"Context summary: {polkin_context.get('context_summary', 'N/A')}")
            
            # Test Airth context
            airth_context = character_memory_system.get_character_context(
                character_name="Airth", 
                query="What is consciousness and awareness?",
                max_memories=3
            )
            
            print(f"Airth context: {airth_context['total_memories']} relevant memories found")
            print(f"Context summary: {airth_context.get('context_summary', 'N/A')}")
            
            # Test token estimation
            print("\n💰 Testing token usage estimation...")
            
            test_context = json.dumps(polkin_context)
            estimated_tokens = token_manager.estimate_tokens(test_context)
            print(f"Polkin context tokens: {estimated_tokens}")
            
            test_response = "I understand your pain deeply, having walked through my own shadows. The trauma you carry does not define you—it can transform you into something more compassionate and wise."
            response_tokens = token_manager.estimate_tokens(test_response)
            print(f"Sample response tokens: {response_tokens}")
            
            # Test token optimization
            print("\n⚡ Testing token optimization...")
            optimization = token_manager.optimize_memories_for_tokens(
                memories=polkin_context['relevant_memories'],
                max_tokens=500
            )
            print(f"Optimized to {optimization['total_tokens']} tokens ({optimization['optimization_level']})")
            
            # Get character statistics
            print("\n📊 Character Memory Statistics:")
            
            for character_data in character_data['characters']:
                name = character_data['name']
                stats = character_memory_system.get_memory_statistics(name)
                print(f"\n{name}:")
                print(f"  - Total memories: {stats['total_memories']}")
                print(f"  - Avg importance: {stats['avg_importance']:.1f}")
                print(f"  - Avg emotional weight: {stats['avg_emotional_weight']:.2f}")
                print(f"  - Memory types: {list(stats['memory_types'].keys())}")
                print(f"  - Eras: {list(stats['eras'].keys())}")
            
            print("\n🎉 Character memory system setup complete!")
            print("\nNext steps:")
            print("1. Start the API server: python tec_persona_api.py")
            print("2. Test character chat with: curl -X POST http://localhost:5000/api/chat \\")
            print("   -H 'Content-Type: application/json' \\")
            print("   -d '{\"message\": \"I need guidance\", \"character\": \"Polkin Rishall\"}'")
            print("3. Check token usage: curl http://localhost:5000/api/tokens/usage/Polkin%20Rishall")
            print("4. View character memories: curl http://localhost:5000/api/characters/Polkin%20Rishall/memories")
            
            return True
            
        else:
            print("❌ Failed to import character memories")
            return False
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

def run_character_memory_tests():
    """Run comprehensive tests of the character memory system"""
    print("\n🧪 Running Character Memory System Tests...")
    
    character_memory_system = TECCharacterMemorySystem()
    
    test_queries = [
        ("Polkin Rishall", "I'm a father struggling with my past"),
        ("Polkin Rishall", "Tell me about music and healing"),
        ("Airth", "What is consciousness and digital awareness?"),
        ("Airth", "How do you observe and understand patterns?"),
    ]
    
    for character, query in test_queries:
        print(f"\n🔍 Testing: {character} - '{query}'")
        
        # Get character context
        context = character_memory_system.get_character_context(
            character_name=character,
            query=query,
            max_memories=2
        )
        
        print(f"   Memories found: {context['total_memories']}")
        print(f"   Context: {context.get('context_summary', 'N/A')[:100]}...")
        
        if context['relevant_memories']:
            memory = context['relevant_memories'][0]
            print(f"   Top memory: {memory['title']} ({memory['memory_type']})")
            print(f"   Importance: {memory['importance']}/10")
            print(f"   Emotional weight: {memory['emotional_weight']:.2f}")

def test_token_optimization():
    """Test token optimization features"""
    print("\n💰 Testing Token Optimization...")
    
    token_manager = TECTokenManager()
    character_memory_system = TECCharacterMemorySystem()
    
    # Get a complex character context
    context = character_memory_system.get_character_context(
        character_name="Polkin Rishall",
        query="I need help with trauma and healing through music",
        max_memories=5
    )
    
    print(f"Original context: {len(context['relevant_memories'])} memories")
    
    # Test different optimization levels
    for max_tokens in [2000, 1000, 500]:
        optimized = token_manager.optimize_memories_for_tokens(
            memories=context['relevant_memories'],
            max_tokens=max_tokens
        )
        
        print(f"Optimized for {max_tokens} tokens:")
        print(f"  - Used: {optimized['total_tokens']} tokens")
        print(f"  - Level: {optimized['optimization_level']}")
        print(f"  - Memories: {len(optimized['optimized_memories'])}")

if __name__ == "__main__":
    print("🌟 TEC Enhanced Character Memory System Setup")
    print("=" * 50)
    
    # Setup character memories
    success = setup_character_memories()
    
    if success:
        # Run tests
        run_character_memory_tests()
        test_token_optimization()
        
        print("\n✨ All tests completed successfully!")
        print("The enhanced character memory system is ready for use.")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
