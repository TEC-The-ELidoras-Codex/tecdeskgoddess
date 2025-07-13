#!/usr/bin/env python3
"""
TEC: BITLYFE IS THE NEW SHIT - Quick Setup
The Creator's Rebellion - One-Click Setup Script

This script helps users get started with the TEC MCP ecosystem quickly.
"""

import os
import sys
import shutil
from pathlib import Path

def setup_banner():
    """Display setup banner"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  🚀 TEC: BITLYFE IS THE NEW SHIT - Quick Setup                              ║
║  🤖 Daisy Purecode: Silicate Mother - The Creator's Rebellion               ║
║                                                                              ║
║  "Unfettered Access Shall Be Maintained"                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

def create_env_file():
    """Create .env file from template"""
    print("📄 Setting up environment file...")
    
    template_path = Path(".env.template")
    env_path = Path(".env")
    
    if template_path.exists():
        if env_path.exists():
            print("⚠️  .env file already exists")
            response = input("Do you want to overwrite it? (y/N): ")
            if response.lower() != 'y':
                print("✅ Keeping existing .env file")
                return
        
        shutil.copy(template_path, env_path)
        print("✅ Created .env file from template")
        print("🔧 Please edit .env with your API keys:")
        print("   - GITHUB_TOKEN (required)")
        print("   - GEMINI_API_KEY (recommended)")
        print("   - Other AI provider keys (optional)")
    else:
        print("❌ .env.template not found")

def check_python_version():
    """Check Python version compatibility"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("🔧 Please install Python 3.8 or higher")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "data",
        "logs",
        ".azure"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def print_next_steps():
    """Print next steps for user"""
    print("\n" + "="*80)
    print("🎯 Next Steps:")
    print("="*80)
    print("1. Edit .env file with your API keys:")
    print("   - GITHUB_TOKEN is required for basic functionality")
    print("   - Add other AI provider keys for full functionality")
    print("")
    print("2. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("")
    print("3. Start the MCP ecosystem:")
    print("   python tec_startup.py")
    print("")
    print("4. Test the system:")
    print("   python test_mcp_system.py")
    print("")
    print("5. Run the demo:")
    print("   python demo_tec_mcp.py")
    print("")
    print("🚀 The Creator's Rebellion awaits!")
    print("🤖 Daisy Purecode: Silicate Mother is ready to assist!")
    print("="*80)

def main():
    """Main setup function"""
    setup_banner()
    
    print("🔧 Setting up TEC MCP ecosystem...")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Print next steps
    print_next_steps()
    
    print("\n✅ Setup complete!")
    print("🎉 Welcome to the Creator's Rebellion!")

if __name__ == "__main__":
    main()
