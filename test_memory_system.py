"""
Test the TEC Enhanced Memory System
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_memory_system():
    print("🧠 Testing TEC Enhanced Memory System")
    print("=" * 50)
    
    # Test 1: Memory Stats
    print("\n1. Testing Memory Stats...")
    try:
        response = requests.get(f"{BASE_URL}/api/memory/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Memory Stats: {data}")
        else:
            print(f"❌ Memory Stats failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Memory Stats error: {e}")
    
    # Test 2: Chat with Memory Context
    print("\n2. Testing Memory-Enhanced Chat...")
    test_conversations = [
        {"message": "Hello, I'm interested in learning about AI", "character": "Mynx"},
        {"message": "Can you remember what I just said about AI?", "character": "Mynx"},
        {"message": "I also love mystical things and magic", "character": "Polkin"},
        {"message": "What do you remember about my interests?", "character": "Polkin"},
    ]
    
    for i, conv in enumerate(test_conversations):
        print(f"\n  Test {i+1}: {conv['message'][:30]}...")
        try:
            response = requests.post(f"{BASE_URL}/chat", json=conv)
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ Response: {data['response'][:100]}...")
                if 'memory_context' in data:
                    memory = data['memory_context']
                    print(f"  🧠 Memory: Level {memory['relationship_level']}, Conversations: {memory['conversation_count']}")
                else:
                    print("  ⚠️ No memory context returned")
            else:
                print(f"  ❌ Chat failed: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Chat error: {e}")
        
        time.sleep(1)  # Brief pause between requests
    
    # Test 3: Memory Search
    print("\n3. Testing Memory Search...")
    try:
        search_data = {"query": "AI", "limit": 5}
        response = requests.post(f"{BASE_URL}/api/memory/search", json=search_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['count']} memories for 'AI'")
            for memory in data['memories'][:2]:
                print(f"  📝 {memory['content'][:80]}...")
        else:
            print(f"❌ Memory search failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Memory search error: {e}")
    
    # Test 4: Create Manual Memory
    print("\n4. Testing Manual Memory Creation...")
    try:
        memory_data = {
            "content": "User prefers detailed technical explanations",
            "type": "preference",
            "importance": 0.8,
            "tags": ["preference", "technical", "learning"]
        }
        response = requests.post(f"{BASE_URL}/api/memory/create", json=memory_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Created memory: {data['memory_id']}")
        else:
            print(f"❌ Memory creation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Memory creation error: {e}")
    
    # Test 5: Final Stats Check
    print("\n5. Final Memory Stats Check...")
    try:
        response = requests.get(f"{BASE_URL}/api/memory/stats")
        if response.status_code == 200:
            data = response.json()
            stats = data['stats']
            print(f"✅ Final Stats:")
            print(f"   Total Memories: {stats['total_memories']}")
            print(f"   Conversations: {stats['conversation_memories']}")
            print(f"   Facts: {stats['fact_memories']}")
            print(f"   Preferences: {stats['preference_memories']}")
            print(f"   Relationship Level: {stats['relationship_level']}")
        else:
            print(f"❌ Final stats failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Final stats error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Memory System Test Complete!")
    print("💡 Try chatting in the interface to see memory in action!")

if __name__ == "__main__":
    test_memory_system()
