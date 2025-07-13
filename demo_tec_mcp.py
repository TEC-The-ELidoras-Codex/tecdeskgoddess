#!/usr/bin/env python3
"""
TEC: BITLYFE IS THE NEW SHIT - Quick Demo
The Creator's Rebellion - Interactive Demo Script

This script demonstrates the key features of the TEC MCP ecosystem.
"""

import requests
import json
import sys
import time

def demo_banner():
    """Display the demo banner"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  🚀 TEC: BITLYFE IS THE NEW SHIT - Interactive Demo                         ║
║  🤖 Daisy Purecode: Silicate Mother - The Creator's Rebellion               ║
║                                                                              ║
║  "Unfettered Access Shall Be Maintained"                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

def demo_mcp_unified_query():
    """Demo the MCP unified query system"""
    print("\n🧠 Demonstrating MCP Unified Query System...")
    
    query_data = {
        "query": "What is the current status of my digital sovereignty journey?",
        "context": "daily_check",
        "include_servers": ["journal", "finance", "questlog"]
    }
    
    try:
        response = requests.post(
            "http://localhost:5000/mcp/unified/query",
            json=query_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ MCP Unified Query Response:")
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Query failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_daisy_ai_processing():
    """Demo Daisy Purecode AI processing"""
    print("\n🤖 Demonstrating Daisy Purecode AI Processing...")
    
    message_data = {
        "message": "Hello Daisy! Tell me about the philosophy behind TEC: BITLYFE IS THE NEW SHIT and how it relates to digital sovereignty.",
        "user_id": "demo_user",
        "session_id": "demo_session"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/agentic/daisy/process",
            json=message_data,
            timeout=20
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Daisy Purecode Response:")
            print(f"🤖 {result.get('response', 'No response')}")
            print(f"🔧 Provider used: {result.get('provider', 'Unknown')}")
        else:
            print(f"❌ AI processing failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_journal_mcp():
    """Demo the Journal MCP Server"""
    print("\n📖 Demonstrating Journal MCP Server...")
    
    journal_entry = {
        "content": "Today I explored the concept of digital sovereignty through the TEC MCP ecosystem. The integration of multiple AI providers with fallback logic represents a step toward technological independence.",
        "tags": ["digital_sovereignty", "ai", "mcp", "philosophy"],
        "user_id": "demo_user"
    }
    
    try:
        response = requests.post(
            "http://localhost:5001/mcp/call/create_entry",
            json={"arguments": journal_entry},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Journal Entry Created:")
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Journal entry creation failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_finance_mcp():
    """Demo the Finance MCP Server"""
    print("\n💰 Demonstrating Finance MCP Server...")
    
    try:
        response = requests.post(
            "http://localhost:5002/mcp/call/get_crypto_price",
            json={"arguments": {"symbol": "bitcoin"}},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Bitcoin Price Data:")
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Crypto price fetch failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_questlog_mcp():
    """Demo the Quest Log MCP Server"""
    print("\n🎯 Demonstrating Quest Log MCP Server...")
    
    quest_data = {
        "title": "Master the TEC MCP Ecosystem",
        "description": "Complete a full demonstration of all MCP servers and AI integrations",
        "difficulty": "expert",
        "xp_reward": 500,
        "user_id": "demo_user"
    }
    
    try:
        response = requests.post(
            "http://localhost:5003/mcp/call/create_quest",
            json={"arguments": quest_data},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Quest Created:")
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Quest creation failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_ai_providers():
    """Demo AI provider status"""
    print("\n🧠 Demonstrating AI Provider Status...")
    
    try:
        response = requests.get("http://localhost:8000/api/agentic/providers", timeout=5)
        
        if response.status_code == 200:
            providers = response.json()
            print("✅ Available AI Providers:")
            for provider in providers.get('providers', []):
                status = "🟢 Available" if provider.get('available') else "🔴 Unavailable"
                print(f"  {status} {provider.get('name', 'Unknown')}")
        else:
            print(f"❌ Provider status check failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main demo function"""
    demo_banner()
    
    print("🎬 Starting TEC MCP Ecosystem Demo...")
    print("⚠️  Make sure tec_startup.py is running!")
    
    # Wait for user to start
    input("\nPress Enter to begin the demo...")
    
    try:
        # Demo each component
        demo_ai_providers()
        demo_mcp_unified_query()
        demo_daisy_ai_processing()
        demo_journal_mcp()
        demo_finance_mcp()
        demo_questlog_mcp()
        
        print("\n" + "="*80)
        print("🎉 Demo Complete!")
        print("🚀 The Creator's Rebellion is fully operational!")
        print("🤖 Daisy Purecode: Silicate Mother is ready for digital sovereignty!")
        print("="*80)
        
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")

if __name__ == "__main__":
    main()
