#!/usr/bin/env python3
"""
TEC System Reset and Test
Clean up and verify everything is working correctly
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path

def reset_and_test():
    """Reset and test the TEC MCP ecosystem"""
    print("🔄 TEC System Reset and Test")
    print("=" * 50)
    
    # 1. Check Python environment
    print("1. 🐍 Checking Python environment...")
    print(f"   Python: {sys.executable}")
    print(f"   Version: {sys.version}")
    
    # 2. Check required files
    print("\n2. 📁 Checking required files...")
    required_files = [
        ".env",
        ".github/copilot/mcp.json",
        "tec_tools/mcp_base.py",
        "tec_tools/mcp_orchestrator.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        return False
    
    # 3. Check environment variables
    print("\n3. 🔑 Checking environment variables...")
    
    # Load .env file
    env_vars = {}
    try:
        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key] = value
                    os.environ[key] = value
    except Exception as e:
        print(f"   ❌ Error reading .env: {e}")
        return False
    
    # Check required keys
    required_keys = ["GITHUB_TOKEN"]
    optional_keys = ["GEMINI_API_KEY", "ANTHROPIC_API_KEY", "OPENAI_API_KEY"]
    
    for key in required_keys:
        if key in env_vars and env_vars[key] != "your_github_token_here":
            print(f"   ✅ {key}: Set")
        else:
            print(f"   ❌ {key}: Missing or placeholder")
            print(f"      Please set {key} in .env file")
            return False
    
    for key in optional_keys:
        if key in env_vars and not env_vars[key].startswith("your_"):
            print(f"   ✅ {key}: Set")
        else:
            print(f"   ⚠️  {key}: Not set (optional)")
    
    # 4. Test MCP configuration
    print("\n4. 🤖 Testing MCP configuration...")
    try:
        with open(".github/copilot/mcp.json", "r") as f:
            mcp_config = json.load(f)
        
        servers = mcp_config.get("mcpServers", {})
        print(f"   ✅ MCP config valid with {len(servers)} servers")
        for server_name in servers:
            print(f"      - {server_name}")
    except Exception as e:
        print(f"   ❌ MCP config error: {e}")
        return False
    
    # 5. Test basic imports
    print("\n5. 📦 Testing Python imports...")
    test_imports = [
        "flask",
        "requests", 
        "openai",
        "anthropic",
        "google.generativeai"
    ]
    
    for module in test_imports:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module} - needs installation")
            return False
    
    # 6. Test MCP server startup (quick test)
    print("\n6. 🚀 Quick MCP server test...")
    try:
        # Test if we can import the MCP modules
        sys.path.append(".")
        from tec_tools import mcp_base
        print("   ✅ MCP base module imports correctly")
        
        from tec_tools import mcp_orchestrator
        print("   ✅ MCP orchestrator module imports correctly")
        
    except Exception as e:
        print(f"   ❌ MCP import error: {e}")
        return False
    
    print("\n🎉 All checks passed!")
    print("✅ TEC MCP system is ready to run")
    print("\n📋 To start the system:")
    print("   1. python tec_startup.py")
    print("   2. python test_mcp_system.py")
    print("   3. Create issue and assign to @copilot")
    
    return True

def fix_common_issues():
    """Fix common setup issues"""
    print("🔧 Fixing common issues...")
    
    # 1. Ensure .env exists
    if not Path(".env").exists():
        print("   Creating .env from template...")
        if Path(".env.template").exists():
            import shutil
            shutil.copy(".env.template", ".env")
        else:
            # Create minimal .env
            with open(".env", "w") as f:
                f.write("# TEC Environment Configuration\n")
                f.write("GITHUB_TOKEN=your_github_token_here\n")
                f.write("GEMINI_API_KEY=your_gemini_key_here\n")
    
    # 2. Ensure MCP config exists
    mcp_dir = Path(".github/copilot")
    mcp_dir.mkdir(parents=True, exist_ok=True)
    
    if not Path(".github/copilot/mcp.json").exists():
        print("   Creating MCP configuration...")
        mcp_config = {
            "mcpServers": {
                "tec-orchestrator": {
                    "command": "python",
                    "args": ["-m", "tec_tools.mcp_orchestrator"],
                    "env": {"PYTHONPATH": "."}
                },
                "tec-journal": {
                    "command": "python", 
                    "args": ["-m", "tec_tools.mcp_journal"],
                    "env": {"PYTHONPATH": "."}
                },
                "tec-finance": {
                    "command": "python",
                    "args": ["-m", "tec_tools.mcp_finance"], 
                    "env": {"PYTHONPATH": "."}
                },
                "tec-questlog": {
                    "command": "python",
                    "args": ["-m", "tec_tools.mcp_questlog"],
                    "env": {"PYTHONPATH": "."}
                }
            }
        }
        
        with open(".github/copilot/mcp.json", "w") as f:
            json.dump(mcp_config, f, indent=2)
    
    print("   ✅ Common issues fixed")

if __name__ == "__main__":
    print("🛠️  TEC System Recovery")
    print("Let's get everything working again!\n")
    
    # Fix common issues first
    fix_common_issues()
    
    # Then run comprehensive test
    success = reset_and_test()
    
    if success:
        print("\n🚀 System is ready! No issues found.")
    else:
        print("\n⚠️  Some issues need attention. Check the output above.")
    
    sys.exit(0 if success else 1)
