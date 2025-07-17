"""
TEC Enhanced Persona System - Complete System Test
Tests all major components and features
"""

import os
import sys
import sqlite3
import requests
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, 'src')

def test_database_layer():
    """Test the database and persona manager"""
    print("🗄️  Testing Database Layer...")
    
    try:
        from tec_tools.persona_manager import PersonaManager
        pm = PersonaManager()
        print("   ✅ PersonaManager initialized successfully")
        
        # Test character lore
        characters = ['Polkin', 'Mynx', 'Kaelen']
        loaded_chars = []
        
        for char in characters:
            lore = pm.get_character_lore(char)
            if lore:
                loaded_chars.append(char)
                print(f"   ✅ {char} lore loaded successfully")
            else:
                print(f"   ❌ {char} lore not found")
        
        if len(loaded_chars) == len(characters):
            print("   ✅ All character lore loaded successfully")
            return True
        else:
            print(f"   ⚠️  Only {len(loaded_chars)}/{len(characters)} characters loaded")
            return False
            
    except Exception as e:
        print(f"   ❌ Database test failed: {e}")
        return False

def test_data_persistence():
    """Test data persistence system"""
    print("💾 Testing Data Persistence...")
    
    try:
        from tec_tools.data_persistence import TECDataManager
        dm = TECDataManager()
        print("   ✅ Data manager initialized")
        
        # Test settings
        test_settings = {
            "test_mode": True,
            "version": "2.0.0",
            "ai_settings": {"creativity": 75}
        }
        
        if dm.save_settings(test_settings):
            print("   ✅ Settings save successful")
        else:
            print("   ❌ Settings save failed")
            return False
        
        loaded_settings = dm.load_settings()
        if loaded_settings.get("test_mode"):
            print("   ✅ Settings load successful")
        else:
            print("   ❌ Settings load failed")
            return False
        
        # Test backup
        backup_file = dm.create_backup("test_backup")
        if backup_file and Path(backup_file).exists():
            print("   ✅ Backup creation successful")
        else:
            print("   ❌ Backup creation failed")
            return False
        
        # Test stats
        stats = dm.get_system_stats()
        if stats.get("database_size", 0) > 0:
            print("   ✅ System stats retrieval successful")
            print(f"      Database size: {stats['database_size']} bytes")
            print(f"      Backups count: {stats['backups_count']}")
        else:
            print("   ❌ System stats failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Data persistence test failed: {e}")
        return False

def test_api_server():
    """Test if API server is running"""
    print("🌐 Testing API Server...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ API health check successful")
            print(f"      Response: {response.text}")
        else:
            print(f"   ❌ API health check failed: {response.status_code}")
            return False
        
        # Test persona endpoints if available
        try:
            persona_response = requests.get("http://localhost:8000/api/persona/current", timeout=5)
            if persona_response.status_code == 200:
                print("   ✅ Persona API endpoint accessible")
            else:
                print("   ⚠️  Persona API endpoint not available (might be normal)")
        except:
            print("   ⚠️  Persona API endpoint not available (might be normal)")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("   ❌ API server not running")
        print("      Run: python tec_persona_api.py")
        return False
    except Exception as e:
        print(f"   ❌ API test failed: {e}")
        return False

def test_frontend_files():
    """Test frontend file existence"""
    print("🎨 Testing Frontend Files...")
    
    required_files = [
        "tec_enhanced_interface.html",
        "tec_complete_interface.html", 
        "assets/css/persona_ui.css",
        "persona_ui_component.html"
    ]
    
    all_present = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path} present")
        else:
            print(f"   ❌ {file_path} missing")
            all_present = False
    
    return all_present

def test_docker_compatibility():
    """Test Docker deployment compatibility"""
    print("🐳 Testing Docker Compatibility...")
    
    required_docker_files = [
        "Dockerfile",
        "docker-compose.yml",
        "requirements.txt"
    ]
    
    all_present = True
    
    for file_path in required_docker_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path} present")
        else:
            print(f"   ❌ {file_path} missing")
            all_present = False
    
    # Check if Docker is available
    try:
        import subprocess
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Docker available: {result.stdout.strip()}")
        else:
            print("   ⚠️  Docker not available (install for container deployment)")
    except FileNotFoundError:
        print("   ⚠️  Docker not installed (install for container deployment)")
    
    return all_present

def test_huggingface_compatibility():
    """Test Hugging Face Spaces compatibility"""
    print("🤗 Testing Hugging Face Compatibility...")
    
    if Path("app.py").exists():
        print("   ✅ app.py present (HF Spaces entry point)")
    else:
        print("   ❌ app.py missing")
        return False
    
    # Check for gradio in requirements
    if Path("requirements.txt").exists():
        with open("requirements.txt", "r") as f:
            requirements = f.read()
            if "gradio" in requirements:
                print("   ✅ Gradio dependency present")
            else:
                print("   ❌ Gradio dependency missing")
                return False
    
    return True

def test_cross_platform_paths():
    """Test cross-platform path compatibility"""
    print("🖥️  Testing Cross-Platform Compatibility...")
    
    try:
        # Test data directory creation
        data_path = Path("./data")
        data_path.mkdir(exist_ok=True)
        print("   ✅ Data directory creation successful")
        
        # Test path separators
        test_file = data_path / "test_file.txt"
        test_file.write_text("test")
        if test_file.exists():
            print("   ✅ Cross-platform path handling successful")
            test_file.unlink()  # Clean up
        else:
            print("   ❌ Cross-platform path handling failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Cross-platform test failed: {e}")
        return False

def main():
    """Run complete system test"""
    print("🧪 TEC Enhanced Persona System - Complete Test Suite")
    print("=" * 60)
    
    tests = [
        ("Database Layer", test_database_layer),
        ("Data Persistence", test_data_persistence),
        ("API Server", test_api_server),
        ("Frontend Files", test_frontend_files),
        ("Docker Compatibility", test_docker_compatibility),
        ("Hugging Face Compatibility", test_huggingface_compatibility),
        ("Cross-Platform Paths", test_cross_platform_paths)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print()
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"   ❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 OVERALL RESULT: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! System is ready for deployment.")
        print("\n🚀 Next Steps:")
        print("   1. For local use: python tec_persona_api.py")
        print("   2. For Docker: ./deploy.sh (Linux) or ./deploy.ps1 (Windows)")
        print("   3. For Hugging Face: Push to HF Spaces with app.py")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
