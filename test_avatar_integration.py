#!/usr/bin/env python3
"""
Test script for TEC Avatar Integration
Tests the complete Smart Memory + Animated Avatar system
"""

import requests
import json
import time
import sys

class TECAvatarIntegrationTest:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.test_character = "Polkin"
        
    def test_chat_with_avatar_response(self):
        """Test that chat endpoint returns avatar state along with response"""
        print("🧪 Testing chat endpoint with avatar integration...")
        
        payload = {
            "message": "Hello Polkin! Tell me something mystical about the universe.",
            "character": self.test_character,
            "enhanced": True,
            "settings": {
                "creativity": 80,
                "memory": "long-term",
                "reasoning": "detailed",
                "mode": "chat"
            }
        }
        
        try:
            response = requests.post(f"{self.base_url}/chat", json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Chat Response received")
                print(f"   Character: {data.get('character', 'Unknown')}")
                print(f"   Response: {data.get('response', '')[:100]}...")
                
                # Test avatar state
                if 'avatar_state' in data:
                    avatar_state = data['avatar_state']
                    print(f"✅ Avatar State included:")
                    print(f"   Character: {avatar_state.get('character')}")
                    print(f"   Emotion: {avatar_state.get('animation_config', {}).get('emotion')}")
                    print(f"   Intensity: {avatar_state.get('animation_config', {}).get('intensity')}")
                    
                    # Test avatar instructions
                    if 'avatar_instructions' in avatar_state:
                        instructions = avatar_state['avatar_instructions']
                        print(f"   Facial Expression: {instructions.get('facial_expression', {}).get('emotion')}")
                        print(f"   Particle Count: {instructions.get('particle_system', {}).get('count', 0)}")
                    
                    return True
                else:
                    print("❌ No avatar_state in response")
                    return False
                    
            else:
                print(f"❌ Chat request failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Chat test error: {e}")
            return False
    
    def test_memory_system_integration(self):
        """Test that memory system provides context for avatar animations"""
        print("\n🧪 Testing memory system integration with avatars...")
        
        # First conversation to build memory
        messages = [
            "I'm feeling really excited about learning mystical arts!",
            "Can you teach me about crystal healing?",
            "What's the most powerful spell you know?"
        ]
        
        relationship_progression = []
        
        for i, message in enumerate(messages):
            print(f"   Message {i+1}: {message[:50]}...")
            
            payload = {
                "message": message,
                "character": self.test_character,
                "enhanced": True
            }
            
            try:
                response = requests.post(f"{self.base_url}/chat", json=payload, timeout=20)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check memory context
                    if 'memory_context' in data:
                        memory = data['memory_context']
                        relationship_level = memory.get('relationship_level', 1)
                        relationship_progression.append(relationship_level)
                        print(f"     Relationship Level: {relationship_level}")
                    
                    # Check if avatar state reflects memory
                    if 'avatar_state' in data and 'memory_context' in data['avatar_state']:
                        avatar_memory = data['avatar_state']['memory_context']
                        print(f"     Avatar Memory Context: Level {avatar_memory.get('relationship_level', 1)}")
                    
                    time.sleep(1)  # Brief pause between messages
                    
            except Exception as e:
                print(f"     Error: {e}")
                return False
        
        # Check if relationship progressed or maintained memory context
        if len(set(relationship_progression)) > 1:
            print("✅ Relationship progression detected in avatar context")
            return True
        elif all(level >= 2 for level in relationship_progression):
            print("✅ Stable relationship maintained in avatar context")
            return True
        else:
            print("⚠️  No relationship progression detected")
            return False
    
    def test_avatar_emotion_variety(self):
        """Test that different message types produce different avatar emotions"""
        print("\n🧪 Testing avatar emotion variety...")
        
        emotion_test_messages = [
            ("I'm so happy and excited!", "joy"),
            ("I'm curious about the mysteries of the universe", "curiosity"),
            ("Share your ancient wisdom with me", "wisdom"),
            ("This is amazing! I love magic!", "excitement")
        ]
        
        detected_emotions = []
        
        for message, expected_emotion in emotion_test_messages:
            print(f"   Testing: {message[:40]}...")
            
            payload = {
                "message": message,
                "character": self.test_character,
                "enhanced": True
            }
            
            try:
                response = requests.post(f"{self.base_url}/chat", json=payload, timeout=20)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'avatar_state' in data:
                        avatar_state = data['avatar_state']
                        emotion = avatar_state.get('animation_config', {}).get('emotion')
                        detected_emotions.append(emotion)
                        print(f"     Detected emotion: {emotion}")
                    
                    time.sleep(0.5)
                    
            except Exception as e:
                print(f"     Error: {e}")
        
        unique_emotions = len(set([e for e in detected_emotions if e]))
        print(f"✅ Detected {unique_emotions} unique emotions: {set(detected_emotions)}")
        
        return unique_emotions >= 2
    
    def test_memory_search_functionality(self):
        """Test memory search API endpoint"""
        print("\n🧪 Testing memory search functionality...")
        
        try:
            # Search for memories
            search_response = requests.post(
                f"{self.base_url}/api/memory/search",
                json={"query": "mystical", "limit": 5},
                timeout=10
            )
            
            if search_response.status_code == 200:
                search_data = search_response.json()
                memory_count = len(search_data.get('memories', []))
                print(f"✅ Memory search returned {memory_count} memories")
                
                if memory_count > 0:
                    print(f"   Sample memory: {search_data['memories'][0].get('content', '')[:50]}...")
                
                return True
            else:
                print(f"❌ Memory search failed: {search_response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Memory search error: {e}")
            return False
    
    def test_avatar_api_endpoints(self):
        """Test avatar-specific API endpoints"""
        print("\n🧪 Testing avatar API endpoints...")
        
        endpoints_to_test = [
            ("/api/avatar/showcase", "Avatar showcase", "GET"),
            (f"/api/avatar/idle/{self.test_character}", f"Idle state for {self.test_character}", "GET"),
            ("/api/avatar/emotion", "Emotion analysis", "POST")
        ]
        
        success_count = 0
        
        for endpoint, description, method in endpoints_to_test:
            try:
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                else:
                    response = requests.post(f"{self.base_url}{endpoint}", json={"text": "I am feeling mystical today!"}, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ {description}: OK")
                    success_count += 1
                else:
                    print(f"❌ {description}: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {description}: {e}")
        
        return success_count == len(endpoints_to_test)
    
    def run_all_tests(self):
        """Run complete avatar integration test suite"""
        print("🚀 Starting TEC Avatar Integration Tests")
        print("=" * 50)
        
        tests = [
            ("Chat with Avatar Response", self.test_chat_with_avatar_response),
            ("Memory System Integration", self.test_memory_system_integration),
            ("Avatar Emotion Variety", self.test_avatar_emotion_variety),
            ("Memory Search Functionality", self.test_memory_search_functionality),
            ("Avatar API Endpoints", self.test_avatar_api_endpoints)
        ]
        
        results = []
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
                
                if result:
                    print(f"✅ {test_name}: PASSED")
                else:
                    print(f"❌ {test_name}: FAILED")
                    
            except Exception as e:
                print(f"💥 {test_name}: ERROR - {e}")
                results.append((test_name, False))
        
        # Summary
        print("\n" + "=" * 50)
        print("🏁 TEST SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        print(f"Tests Passed: {passed}/{total}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 All Avatar Integration Tests PASSED!")
            print("   ✅ Smart Memory System working")
            print("   ✅ Animated Avatar System working")
            print("   ✅ Memory + Avatar Integration working")
            return True
        else:
            print("⚠️  Some tests failed. Check the results above.")
            return False

def main():
    print("TEC Avatar Integration Test Suite")
    print("Verifying Smart Memory + Animated Avatar System")
    print("-" * 50)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ TEC server not responding. Please start the server first.")
            sys.exit(1)
    except:
        print("❌ Cannot connect to TEC server. Please start with: python tec_persona_api.py")
        sys.exit(1)
    
    # Run tests
    tester = TECAvatarIntegrationTest()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎯 Next Steps:")
        print("   1. Open tec_enhanced_interface.html in browser")
        print("   2. Test avatar animations and character switching") 
        print("   3. Verify memory status updates in real-time")
        print("   4. Check avatar reactions to different conversation types")
        sys.exit(0)
    else:
        print("\n🔧 Fix any failing tests before proceeding")
        sys.exit(1)

if __name__ == "__main__":
    main()
