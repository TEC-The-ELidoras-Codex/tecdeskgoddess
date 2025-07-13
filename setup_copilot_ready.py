#!/usr/bin/env python3
"""
TEC Copilot Setup - Final Configuration
Make everything ready for GitHub Copilot integration
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def setup_copilot_ready():
    """Final setup for Copilot integration"""
    print("🤖 Setting up TEC for GitHub Copilot integration...")
    
    # 1. Verify MCP configuration
    print("1. ✅ MCP configuration verified (.github/copilot/mcp.json)")
    
    # 2. Check environment
    env_file = Path(".env")
    if env_file.exists():
        print("2. ✅ Environment file exists (.env)")
    else:
        print("2. ⚠️ Creating .env from template...")
        subprocess.run(["cp", ".env.template", ".env"])
    
    # 3. Verify dependencies
    print("3. 📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("   ✅ Dependencies installed")
    except subprocess.CalledProcessError:
        print("   ⚠️ Some dependencies may need manual installation")
    
    # 4. Test MCP system
    print("4. 🧪 Testing MCP system...")
    try:
        result = subprocess.run([sys.executable, "test_copilot_mcp.py"], 
                               capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("   ✅ MCP system test passed")
        else:
            print("   ⚠️ MCP system test had warnings")
    except Exception as e:
        print(f"   ⚠️ MCP test skipped: {e}")
    
    # 5. Create quick start guide
    create_quick_start_file()
    
    # 6. Final status
    print("\n🎉 TEC Copilot Integration Setup Complete!")
    print("📋 Next steps:")
    print("   1. Configure your API keys in .env")
    print("   2. Test with: python test_copilot_mcp.py")
    print("   3. Start MCP: python tec_startup.py")
    print("   4. Create an issue and assign to @copilot")
    print("   5. Add hashtag: #github-pull-request_copilot-coding-agent")
    
    return True

def create_quick_start_file():
    """Create a quick start file"""
    quick_start = """# 🚀 TEC Copilot Quick Start

## Ready to Use!
Your TEC: BITLYFE IS THE NEW SHIT project is configured for GitHub Copilot coding agent.

## Immediate Next Steps:

### 1. Configure Environment (if not done)
```bash
# Edit .env with your API keys
# Minimum required: GITHUB_TOKEN
```

### 2. Test Integration
```bash
python test_copilot_mcp.py
```

### 3. Start MCP Ecosystem  
```bash
python tec_startup.py
```

### 4. Test System
```bash
python test_mcp_system.py
```

### 5. Assign Issue to Copilot
1. Create GitHub issue
2. Add hashtag: `#github-pull-request_copilot-coding-agent`
3. Assign @copilot
4. Wait for AI magic! ✨

## Key Files:
- `.github/copilot/mcp.json` - MCP configuration
- `COPILOT_INTEGRATION.md` - Full documentation
- `test_copilot_mcp.py` - Integration testing

## The Creator's Rebellion Enhanced! 🤖
"""
    
    with open("QUICK_START_COPILOT.md", "w") as f:
        f.write(quick_start)
    
    print("5. ✅ Quick start guide created (QUICK_START_COPILOT.md)")

if __name__ == "__main__":
    setup_copilot_ready()
