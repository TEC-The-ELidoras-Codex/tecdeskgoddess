#!/usr/bin/env python3
"""
TEC System Status Check
"""
import os
import sys
import subprocess
from datetime import datetime

def check_files():
    """Check if all required files exist"""
    required_files = [
        'src/tec_api_simplified.py',
        'src/tec_tools/database_manager.py',
        'src/tec_tools/web3_auth.py',
        'src/tec_tools/agentic_processor.py',
        'tec_complete_interface.html',
        'config/config.json',
        'requirements.txt'
    ]
    
    print("📁 File Check:")
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING")
    print()

def check_imports():
    """Check if all modules can be imported"""
    print("📦 Module Import Check:")
    
    # Change to src directory for imports
    sys.path.insert(0, 'src')
    
    modules = [
        'tec_tools.database_manager',
        'tec_tools.web3_auth',
        'tec_tools.agentic_processor'
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except Exception as e:
            print(f"  ❌ {module} - ERROR: {e}")
    print()

def check_database():
    """Check database functionality"""
    print("🗄️ Database Check:")
    try:
        sys.path.insert(0, 'src')
        from tec_tools.database_manager import DatabaseManager
        
        db = DatabaseManager()
        print(f"  ✅ Database initialized")
        
        # Test user creation
        user = db.create_user('test_user', '0x123...', 'ethereum')
        print(f"  ✅ User creation works")
        
        # Test BITL operations
        new_balance = db.update_bitl_balance('test_user', 100, 'earn', 'testing')
        print(f"  ✅ BITL operations work - Balance: {new_balance}")
        
    except Exception as e:
        print(f"  ❌ Database error: {e}")
    print()

def check_web3():
    """Check Web3 authentication"""
    print("🔐 Web3 Auth Check:")
    try:
        sys.path.insert(0, 'src')
        from tec_tools.web3_auth import Web3AuthManager
        
        with open('config/config.json', 'r') as f:
            import json
            config = json.load(f)
        
        web3_auth = Web3AuthManager(config)
        print(f"  ✅ Web3 auth initialized")
        
        # Test nonce generation
        nonce = web3_auth.generate_nonce('0x123...')
        print(f"  ✅ Nonce generation works: {nonce[:8]}...")
        
    except Exception as e:
        print(f"  ❌ Web3 auth error: {e}")
    print()

def check_personas():
    """Check persona system"""
    print("🤖 Persona System Check:")
    try:
        sys.path.insert(0, 'src')
        from tec_tools.agentic_processor import AgenticProcessor
        
        with open('config/config.json', 'r') as f:
            import json
            config = json.load(f)
        
        processor = AgenticProcessor(config)
        print(f"  ✅ Agentic processor initialized")
        
        # Test persona info
        persona_info = processor.get_persona_info()
        print(f"  ✅ Current persona: {persona_info['name']}")
        
        # Test available personas
        personas = processor.get_available_personas()
        print(f"  ✅ Available personas: {', '.join(personas)}")
        
    except Exception as e:
        print(f"  ❌ Persona system error: {e}")
    print()

def main():
    """Run all checks"""
    print("🔍 TEC System Status Check")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    check_files()
    check_imports()
    check_database()
    check_web3()
    check_personas()
    
    print("✅ System Status Check Complete!")
    print("Ready to start the TEC Enhanced API Server!")

if __name__ == "__main__":
    main()
