#!/usr/bin/env python3
"""
TEC Copilot MCP Test Script
Test GitHub Copilot integration with TEC MCP servers
"""

import json
import subprocess
import sys
import os
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_mcp_config():
    """Test MCP configuration file"""
    print("🔍 Testing MCP Configuration...")
    
    config_path = Path(".github/copilot/mcp.json")
    
    if not config_path.exists():
        print("❌ MCP configuration file not found")
        return False
    
    try:
        with open(config_path) as f:
            config = json.load(f)
        
        servers = config.get("mcpServers", {})
        print(f"✅ Found {len(servers)} MCP servers configured:")
        
        for name, server in servers.items():
            print(f"  - {name}: {server.get('command', 'No command')} {' '.join(server.get('args', []))}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in MCP config: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading MCP config: {e}")
        return False

def test_mcp_server_startup():
    """Test if MCP servers can be started"""
    print("\n🚀 Testing MCP Server Startup...")
    
    try:
        # Start MCP orchestrator
        print("Starting MCP orchestrator...")
        process = subprocess.Popen([
            sys.executable, "-m", "tec_tools.mcp_orchestrator"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for startup
        time.sleep(2)
        
        # Check if process is running
        if process.poll() is None:
            print("✅ MCP orchestrator started successfully")
            process.terminate()
            process.wait()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ MCP orchestrator failed to start")
            print(f"stdout: {stdout.decode()}")
            print(f"stderr: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error starting MCP server: {e}")
        return False

def test_copilot_integration():
    """Test Copilot integration readiness"""
    print("\n🤖 Testing Copilot Integration Readiness...")
    
    checks = {
        "MCP Config": test_mcp_config(),
        "Dependencies": check_dependencies(),
        "Environment": check_environment(),
        "File Structure": check_file_structure()
    }
    
    passed = sum(checks.values())
    total = len(checks)
    
    print(f"\n📊 Integration Readiness: {passed}/{total} checks passed")
    
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"  {status} {check}")
    
    return passed == total

def check_dependencies():
    """Check if required dependencies are installed"""
    required = ['flask', 'requests', 'openai']
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            print(f"❌ Missing dependency: {package}")
            return False
    
    return True

def check_environment():
    """Check environment variables"""
    required = ['GITHUB_TOKEN']
    optional = ['GEMINI_API_KEY', 'ANTHROPIC_API_KEY', 'OPENAI_API_KEY']
    
    missing_required = []
    missing_optional = []
    
    for var in required:
        if not os.environ.get(var):
            missing_required.append(var)
    
    for var in optional:
        if not os.environ.get(var):
            missing_optional.append(var)
    
    if missing_required:
        print(f"❌ Missing required environment variables: {missing_required}")
        return False
    
    if missing_optional:
        print(f"⚠️ Missing optional environment variables: {missing_optional}")
    
    return True

def check_file_structure():
    """Check if required files exist"""
    required_files = [
        "tec_tools/__init__.py",
        "tec_tools/mcp_base.py",
        "tec_tools/mcp_orchestrator.py",
        "tec_tools/mcp_journal.py",
        "tec_tools/mcp_finance.py",
        "tec_tools/mcp_questlog.py",
        "tec_tools/agentic_processor.py"
    ]
    
    missing = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)
    
    if missing:
        print(f"❌ Missing required files: {missing}")
        return False
    
    return True

def generate_copilot_test_issue():
    """Generate a test issue for Copilot"""
    print("\n📝 Generating Test Issue for Copilot...")
    
    issue_template = """
# Test Issue for TEC Copilot Integration

## Description
This is a test issue to verify that GitHub Copilot can properly interact with the TEC MCP ecosystem.

## Requirements
- [ ] Test MCP server connectivity
- [ ] Verify context gathering from all servers
- [ ] Generate a simple feature implementation
- [ ] Create appropriate tests

## Acceptance Criteria
- All MCP servers respond to health checks
- Unified query returns data from multiple servers
- Generated code follows TEC patterns
- Tests pass successfully

## Context
This issue should be assigned to @copilot to test the integration.

#github-pull-request_copilot-coding-agent
"""
    
    with open("COPILOT_TEST_ISSUE.md", "w") as f:
        f.write(issue_template)
    
    print("✅ Test issue template created: COPILOT_TEST_ISSUE.md")
    print("📋 To test Copilot integration:")
    print("  1. Create a new GitHub issue")
    print("  2. Copy the content from COPILOT_TEST_ISSUE.md")
    print("  3. Assign @copilot to the issue")
    print("  4. Wait for Copilot to create a pull request")

def main():
    """Main test function"""
    print("🤖 TEC Copilot MCP Integration Test")
    print("=" * 50)
    
    # Test MCP configuration
    if not test_mcp_config():
        print("❌ MCP configuration test failed")
        return False
    
    # Test MCP server startup
    if not test_mcp_server_startup():
        print("❌ MCP server startup test failed")
        return False
    
    # Test Copilot integration readiness
    if not test_copilot_integration():
        print("❌ Copilot integration readiness test failed")
        return False
    
    # Generate test issue
    generate_copilot_test_issue()
    
    print("\n🎉 All tests passed!")
    print("🚀 TEC Copilot MCP integration is ready!")
    print("🤖 You can now assign issues to @copilot for automated development")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
