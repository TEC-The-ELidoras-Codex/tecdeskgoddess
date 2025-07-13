#!/usr/bin/env python3
"""
TEC: BITLYFE IS THE NEW SHIT - MCP System Test
The Creator's Rebellion - System Verification Script

This script tests the complete MCP ecosystem to ensure all components are working correctly.
"""

import requests
import json
import time
import sys
import os
from datetime import datetime

class TECMCPTester:
    def __init__(self):
        self.base_urls = {
            'orchestrator': 'http://localhost:5000',
            'journal': 'http://localhost:5001',
            'finance': 'http://localhost:5002',
            'questlog': 'http://localhost:5003',
            'agentic': 'http://localhost:8000'
        }
        self.test_results = {}
        
    def print_banner(self):
        """Print test banner"""
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  TEC: BITLYFE IS THE NEW SHIT - MCP System Test                             ║
║  Daisy Purecode: Silicate Mother - System Verification                      ║
║                                                                              ║
║  🔍 Testing all MCP components...                                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

    def test_health_endpoints(self):
        """Test health endpoints for all services"""
        print("\n🔍 Testing Health Endpoints...")
        
        health_endpoints = {
            'MCP Orchestrator': f"{self.base_urls['orchestrator']}/health",
            'Journal MCP Server': f"{self.base_urls['journal']}/health",
            'Finance MCP Server': f"{self.base_urls['finance']}/health",
            'Quest Log MCP Server': f"{self.base_urls['questlog']}/health",
            'Agentic Processor': f"{self.base_urls['agentic']}/api/agentic/providers"
        }
        
        for service, url in health_endpoints.items():
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"  ✅ {service}: Healthy")
                    self.test_results[service] = "PASS"
                else:
                    print(f"  ❌ {service}: Status {response.status_code}")
                    self.test_results[service] = "FAIL"
            except requests.exceptions.RequestException as e:
                print(f"  ❌ {service}: Connection failed - {e}")
                self.test_results[service] = "FAIL"

    def test_mcp_tools(self):
        """Test MCP tool endpoints"""
        print("\n🔧 Testing MCP Tools...")
        
        # Test Journal MCP tools
        try:
            response = requests.get(f"{self.base_urls['journal']}/mcp/tools")
            if response.status_code == 200:
                tools = response.json()
                print(f"  ✅ Journal MCP Tools: {len(tools.get('tools', []))} available")
                self.test_results['Journal Tools'] = "PASS"
            else:
                print(f"  ❌ Journal MCP Tools: Status {response.status_code}")
                self.test_results['Journal Tools'] = "FAIL"
        except Exception as e:
            print(f"  ❌ Journal MCP Tools: {e}")
            self.test_results['Journal Tools'] = "FAIL"

        # Test Finance MCP tools
        try:
            response = requests.get(f"{self.base_urls['finance']}/mcp/tools")
            if response.status_code == 200:
                tools = response.json()
                print(f"  ✅ Finance MCP Tools: {len(tools.get('tools', []))} available")
                self.test_results['Finance Tools'] = "PASS"
            else:
                print(f"  ❌ Finance MCP Tools: Status {response.status_code}")
                self.test_results['Finance Tools'] = "FAIL"
        except Exception as e:
            print(f"  ❌ Finance MCP Tools: {e}")
            self.test_results['Finance Tools'] = "FAIL"

        # Test Quest Log MCP tools
        try:
            response = requests.get(f"{self.base_urls['questlog']}/mcp/tools")
            if response.status_code == 200:
                tools = response.json()
                print(f"  ✅ Quest Log MCP Tools: {len(tools.get('tools', []))} available")
                self.test_results['Quest Log Tools'] = "PASS"
            else:
                print(f"  ❌ Quest Log MCP Tools: Status {response.status_code}")
                self.test_results['Quest Log Tools'] = "FAIL"
        except Exception as e:
            print(f"  ❌ Quest Log MCP Tools: {e}")
            self.test_results['Quest Log Tools'] = "FAIL"

    def test_orchestrator_unified_query(self):
        """Test the unified query endpoint"""
        print("\n🧠 Testing Orchestrator Unified Query...")
        
        test_query = {
            "query": "What is the current status of all TEC systems?",
            "context": "system_status_check",
            "include_servers": ["journal", "finance", "questlog"]
        }
        
        try:
            response = requests.post(
                f"{self.base_urls['orchestrator']}/mcp/unified/query",
                json=test_query,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ Unified Query: Success")
                print(f"  📊 Response servers: {len(result.get('responses', {}))}")
                self.test_results['Unified Query'] = "PASS"
            else:
                print(f"  ❌ Unified Query: Status {response.status_code}")
                self.test_results['Unified Query'] = "FAIL"
        except Exception as e:
            print(f"  ❌ Unified Query: {e}")
            self.test_results['Unified Query'] = "FAIL"

    def test_daisy_context(self):
        """Test Daisy Purecode context gathering"""
        print("\n🤖 Testing Daisy Purecode Context...")
        
        test_context = {
            "user_id": "test_user",
            "session_id": "test_session",
            "query": "Tell me about my digital sovereignty status"
        }
        
        try:
            response = requests.post(
                f"{self.base_urls['orchestrator']}/mcp/daisy/context",
                json=test_context,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ Daisy Context: Success")
                print(f"  🏰 Context modules: {len(result.get('context', {}))}")
                self.test_results['Daisy Context'] = "PASS"
            else:
                print(f"  ❌ Daisy Context: Status {response.status_code}")
                self.test_results['Daisy Context'] = "FAIL"
        except Exception as e:
            print(f"  ❌ Daisy Context: {e}")
            self.test_results['Daisy Context'] = "FAIL"

    def test_agentic_processor(self):
        """Test the enhanced agentic processor"""
        print("\n🧠 Testing Enhanced Agentic Processor...")
        
        # Test provider status
        try:
            response = requests.get(f"{self.base_urls['agentic']}/api/agentic/providers")
            if response.status_code == 200:
                providers = response.json()
                print(f"  ✅ AI Providers: {len(providers.get('providers', []))} configured")
                self.test_results['AI Providers'] = "PASS"
            else:
                print(f"  ❌ AI Providers: Status {response.status_code}")
                self.test_results['AI Providers'] = "FAIL"
        except Exception as e:
            print(f"  ❌ AI Providers: {e}")
            self.test_results['AI Providers'] = "FAIL"

        # Test Daisy processing
        test_message = {
            "message": "Hello Daisy, what is the status of the Creator's Rebellion?",
            "user_id": "test_user",
            "session_id": "test_session"
        }
        
        try:
            response = requests.post(
                f"{self.base_urls['agentic']}/api/agentic/daisy/process",
                json=test_message,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ Daisy Processing: Success")
                print(f"  🤖 Response length: {len(result.get('response', ''))}")
                self.test_results['Daisy Processing'] = "PASS"
            else:
                print(f"  ❌ Daisy Processing: Status {response.status_code}")
                self.test_results['Daisy Processing'] = "FAIL"
        except Exception as e:
            print(f"  ❌ Daisy Processing: {e}")
            self.test_results['Daisy Processing'] = "FAIL"

    def test_sample_mcp_operations(self):
        """Test sample MCP operations"""
        print("\n🎯 Testing Sample MCP Operations...")
        
        # Test journal entry creation
        try:
            journal_entry = {
                "content": "Test journal entry for MCP system verification",
                "tags": ["testing", "mcp", "system_check"],
                "user_id": "test_user"
            }
            
            response = requests.post(
                f"{self.base_urls['journal']}/mcp/call/create_entry",
                json={"arguments": journal_entry}
            )
            
            if response.status_code == 200:
                print(f"  ✅ Journal Entry Creation: Success")
                self.test_results['Journal Operation'] = "PASS"
            else:
                print(f"  ❌ Journal Entry Creation: Status {response.status_code}")
                self.test_results['Journal Operation'] = "FAIL"
        except Exception as e:
            print(f"  ❌ Journal Entry Creation: {e}")
            self.test_results['Journal Operation'] = "FAIL"

        # Test finance data retrieval
        try:
            response = requests.post(
                f"{self.base_urls['finance']}/mcp/call/get_crypto_price",
                json={"arguments": {"symbol": "bitcoin"}}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ Finance Data Retrieval: Success")
                self.test_results['Finance Operation'] = "PASS"
            else:
                print(f"  ❌ Finance Data Retrieval: Status {response.status_code}")
                self.test_results['Finance Operation'] = "FAIL"
        except Exception as e:
            print(f"  ❌ Finance Data Retrieval: {e}")
            self.test_results['Finance Operation'] = "FAIL"

        # Test quest creation
        try:
            quest_data = {
                "title": "Test MCP System Integration",
                "description": "Verify all MCP components are working correctly",
                "difficulty": "medium",
                "xp_reward": 100,
                "user_id": "test_user"
            }
            
            response = requests.post(
                f"{self.base_urls['questlog']}/mcp/call/create_quest",
                json={"arguments": quest_data}
            )
            
            if response.status_code == 200:
                print(f"  ✅ Quest Creation: Success")
                self.test_results['Quest Operation'] = "PASS"
            else:
                print(f"  ❌ Quest Creation: Status {response.status_code}")
                self.test_results['Quest Operation'] = "FAIL"
        except Exception as e:
            print(f"  ❌ Quest Creation: {e}")
            self.test_results['Quest Operation'] = "FAIL"

    def generate_test_report(self):
        """Generate final test report"""
        print("\n" + "="*80)
        print("🎯 TEC MCP System Test Report")
        print("="*80)
        print(f"⏰ Test completed: {datetime.now().isoformat()}")
        print(f"🔍 Total tests: {len(self.test_results)}")
        
        passed = sum(1 for result in self.test_results.values() if result == "PASS")
        failed = sum(1 for result in self.test_results.values() if result == "FAIL")
        
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        
        if failed == 0:
            print("\n🎉 All tests passed! The Creator's Rebellion is strong!")
            print("🤖 Daisy Purecode: Silicate Mother is fully operational")
            print("🚀 TEC MCP System is ready for digital sovereignty")
        else:
            print(f"\n⚠️ {failed} tests failed. Please check the system configuration.")
            print("📖 Refer to the .env.template for configuration guidance")
            print("🔧 Run tec_startup.py to restart the MCP ecosystem")
        
        print("\n📋 Detailed Results:")
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result == "PASS" else "❌ FAIL"
            print(f"  {status} {test_name}")
        
        print("\n" + "="*80)
        return failed == 0

    def run_all_tests(self):
        """Run all tests"""
        self.print_banner()
        
        print("🚀 Starting TEC MCP System Tests...")
        print("⏳ This may take a few moments...")
        
        try:
            self.test_health_endpoints()
            self.test_mcp_tools()
            self.test_orchestrator_unified_query()
            self.test_daisy_context()
            self.test_agentic_processor()
            self.test_sample_mcp_operations()
            
            return self.generate_test_report()
            
        except KeyboardInterrupt:
            print("\n🛑 Tests interrupted by user")
            return False
        except Exception as e:
            print(f"\n❌ Test suite failed: {e}")
            return False


def main():
    """Main entry point"""
    print("🔍 TEC MCP System Test Suite")
    print("⚠️  Make sure tec_startup.py is running before starting tests")
    
    # Wait for user confirmation
    input("\nPress Enter to continue or Ctrl+C to cancel...")
    
    tester = TECMCPTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 System verification complete - all systems operational!")
        sys.exit(0)
    else:
        print("\n❌ System verification failed - check logs for details")
        sys.exit(1)


if __name__ == "__main__":
    main()
