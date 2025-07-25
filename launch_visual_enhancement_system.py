#!/usr/bin/env python3
"""
TEC Visual Enhancement System Launcher
Complete deployment script for the enhanced TEC visual generation system
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime

def print_banner():
    """Print the TEC Visual Enhancement System banner"""
    print("=" * 80)
    print("🎨 TEC VISUAL ENHANCEMENT SYSTEM - COMPLETE FACTION DEPLOYMENT")
    print("=" * 80)
    print(f"🕒 Launch Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 CHECKING SYSTEM DEPENDENCIES...")
    
    dependencies = {
        'azure_image_tools': '🎨 Azure AI Image Generation',
        'tec_visual_asset_generator': '🏛️ TEC Visual Asset Generator',
        'tec_persona_api': '🚀 Enhanced Backend API',
        'flask': '🌐 Web Framework',
        'requests': '📡 HTTP Client'
    }
    
    missing_deps = []
    
    for module, description in dependencies.items():
        try:
            if module in ['azure_image_tools', 'tec_visual_asset_generator', 'tec_persona_api']:
                # Check if our custom modules exist
                if os.path.exists(f"{module}.py"):
                    print(f"✅ {description}")
                else:
                    print(f"❌ {description} - File not found")
                    missing_deps.append(module)
            else:
                # Check standard modules
                __import__(module)
                print(f"✅ {description}")
        except ImportError:
            print(f"❌ {description} - Not installed")
            missing_deps.append(module)
    
    if missing_deps:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing_deps)}")
        return False
    
    print("\n✅ All dependencies satisfied!")
    return True

def check_configuration():
    """Check system configuration and credentials"""
    print("\n🔧 CHECKING SYSTEM CONFIGURATION...")
    
    # Check for .env file
    env_file = '.env'
    if os.path.exists(env_file):
        print("✅ Environment configuration file found")
        
        # Check for required environment variables
        required_vars = [
            'AZURE_AI_API_KEY',
            'AZURE_ENDPOINT',
            'WORLD_ANVIL_API_KEY'
        ]
        
        from dotenv import load_dotenv
        load_dotenv()
        
        for var in required_vars:
            if os.getenv(var):
                print(f"✅ {var} configured")
            else:
                print(f"⚠️  {var} not set (will use demo mode)")
        
    else:
        print("⚠️  .env file not found - will use demo mode")
    
    # Check asset directories
    asset_dirs = ['assets', 'assets/portraits', 'assets/emblems', 'assets/environments']
    for directory in asset_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"📁 Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")
    
    return True

def test_visual_system():
    """Test the visual generation system"""
    print("\n🧪 TESTING VISUAL GENERATION SYSTEM...")
    
    try:
        # Import and test Azure Image Tools
        from azure_image_tools import AzureImageGenerator
        image_gen = AzureImageGenerator()
        print("✅ Azure Image Generator initialized")
        
        # Import and test TEC Visual Asset Generator
        from tec_visual_asset_generator import TECVisualAssetGenerator
        visual_gen = TECVisualAssetGenerator()
        print("✅ TEC Visual Asset Generator initialized")
        
        # Test faction database
        faction_count = len(visual_gen.faction_database)
        print(f"✅ Complete faction database loaded: {faction_count} factions")
        
        # Test categories
        categories = visual_gen.get_faction_list_by_category()
        print(f"✅ Faction categories: {len(categories)} types")
        
        for category, factions in categories.items():
            print(f"   🏛️ {category}: {len(factions)} factions")
        
        return True
        
    except Exception as e:
        print(f"❌ Visual system test failed: {e}")
        return False

def launch_backend_server():
    """Launch the enhanced backend API server"""
    print("\n🚀 LAUNCHING ENHANCED BACKEND SERVER...")
    
    try:
        # Import the enhanced API
        from tec_persona_api import app
        
        print("✅ Enhanced TEC Persona API loaded")
        print("🌐 Server will start on: http://localhost:8000")
        print("🎨 Visual API endpoints:")
        print("   • /api/visual/generate/character - Character portrait generation")
        print("   • /api/visual/generate/faction - Faction asset collections")
        print("   • /api/visual/factions - Complete faction database")
        print("   • /api/visual/generate/batch - Batch asset generation")
        print("   • /api/visual/inventory - Asset inventory management")
        
        print("\n🔥 Starting server...")
        
        # Run the server (this will block)
        app.run(
            host='0.0.0.0',
            port=8000,
            debug=False,  # Set to False for production
            threaded=True
        )
        
    except Exception as e:
        print(f"❌ Failed to launch server: {e}")
        return False

def display_system_status():
    """Display complete system status"""
    print("\n📊 SYSTEM STATUS SUMMARY:")
    print("=" * 50)
    
    # Visual system status
    try:
        from tec_visual_asset_generator import TECVisualAssetGenerator
        visual_gen = TECVisualAssetGenerator()
        faction_count = len(visual_gen.faction_database)
        categories = visual_gen.get_faction_list_by_category()
        
        print(f"🎨 Visual Generation System: OPERATIONAL")
        print(f"🏛️ Total Factions: {faction_count}")
        print(f"📋 Faction Categories: {len(categories)}")
        print(f"🎭 Character Portrait Generation: READY")
        print(f"🏢 Environment Art Generation: READY")
        print(f"⚡ Batch Processing: READY")
        
    except Exception as e:
        print(f"🎨 Visual Generation System: ERROR - {e}")
    
    # Backend API status
    print(f"🚀 Enhanced Backend API: READY TO LAUNCH")
    print(f"🌐 Server Address: http://localhost:8000")
    print(f"📡 Visual API Endpoints: 5 endpoints available")
    
    # Configuration status
    env_file_exists = os.path.exists('.env')
    print(f"🔧 Configuration: {'CONFIGURED' if env_file_exists else 'DEMO MODE'}")
    
    print("=" * 50)

def main():
    """Main launcher function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ DEPLOYMENT FAILED - Missing dependencies")
        print("💡 Please install required packages and ensure all files are present")
        return False
    
    # Check configuration
    if not check_configuration():
        print("\n❌ DEPLOYMENT FAILED - Configuration issues")
        return False
    
    # Test visual system
    if not test_visual_system():
        print("\n❌ DEPLOYMENT FAILED - Visual system issues")
        return False
    
    # Display system status
    display_system_status()
    
    print("\n🎉 VISUAL ENHANCEMENT SYSTEM READY!")
    print("\n💡 QUICK START GUIDE:")
    print("   1. Server will start on http://localhost:8000")
    print("   2. Access visual generation at /api/visual/ endpoints")
    print("   3. Use /api/visual/factions to see all available factions")
    print("   4. Generate faction assets with /api/visual/generate/faction")
    
    # Ask user if they want to launch
    try:
        response = input("\n🚀 Launch enhanced backend server now? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            launch_backend_server()
        else:
            print("✅ System ready - run 'python tec_persona_api.py' to start server manually")
            return True
    except KeyboardInterrupt:
        print("\n\n👋 Launch cancelled by user")
        return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 TEC Visual Enhancement System deployment complete!")
        else:
            print("\n❌ Deployment failed - check errors above")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Deployment interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error during deployment: {e}")
        sys.exit(1)
