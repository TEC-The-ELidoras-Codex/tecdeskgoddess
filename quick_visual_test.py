#!/usr/bin/env python3
"""
Simple TEC Visual System Test - Quick Verification
"""

print("🧪 TEC VISUAL SYSTEM - QUICK VERIFICATION TEST")
print("=" * 60)

tests_passed = 0
tests_total = 0

def test_component(name, test_func):
    global tests_passed, tests_total
    tests_total += 1
    print(f"\n🔍 Testing {name}...")
    try:
        result = test_func()
        if result:
            print(f"✅ {name}: PASSED")
            tests_passed += 1
        else:
            print(f"❌ {name}: FAILED")
    except Exception as e:
        print(f"💥 {name}: ERROR - {e}")

def test_azure_image_tools():
    """Test Azure Image Tools import and initialization"""
    try:
        from azure_image_tools import AzureImageGenerator
        image_gen = AzureImageGenerator()
        
        # Check faction styles loaded
        faction_count = len(image_gen.faction_visual_styles)
        print(f"   📊 Faction styles loaded: {faction_count}")
        
        # Check specific faction exists
        if "The Archivists" in image_gen.faction_visual_styles:
            print(f"   ✅ Sample faction (The Archivists) found")
            return faction_count >= 15
        else:
            print(f"   ❌ Sample faction not found")
            return False
            
    except Exception as e:
        print(f"   💥 Import error: {e}")
        return False

def test_visual_asset_generator():
    """Test Visual Asset Generator import and initialization"""
    try:
        from tec_visual_asset_generator import TECVisualAssetGenerator
        visual_gen = TECVisualAssetGenerator()
        
        # Check faction database loaded
        faction_count = len(visual_gen.faction_database)
        print(f"   📊 Faction database loaded: {faction_count}")
        
        # Check categories
        categories = visual_gen.get_faction_list_by_category()
        print(f"   📋 Categories: {len(categories)}")
        
        return faction_count >= 15 and len(categories) >= 3
        
    except Exception as e:
        print(f"   💥 Import error: {e}")
        return False

def test_backend_api_imports():
    """Test backend API can import visual components"""
    try:
        # Test individual imports
        from tec_visual_asset_generator import TECVisualAssetGenerator
        from azure_image_tools import AzureImageGenerator
        
        # Test initialization
        visual_gen = TECVisualAssetGenerator()
        azure_gen = AzureImageGenerator()
        
        print(f"   ✅ Visual components imported successfully")
        return True
        
    except Exception as e:
        print(f"   💥 Backend import error: {e}")
        return False

def test_faction_database_consistency():
    """Test faction database consistency between components"""
    try:
        from tec_visual_asset_generator import TECVisualAssetGenerator
        from azure_image_tools import AzureImageGenerator
        
        visual_gen = TECVisualAssetGenerator()
        azure_gen = AzureImageGenerator()
        
        # Check faction consistency
        visual_factions = set(visual_gen.faction_database.keys())
        azure_factions = set(azure_gen.faction_visual_styles.keys())
        
        # Find common factions
        common_factions = visual_factions.intersection(azure_factions)
        
        print(f"   📊 Visual generator factions: {len(visual_factions)}")
        print(f"   📊 Azure factions: {len(azure_factions)}")
        print(f"   📊 Common factions: {len(common_factions)}")
        
        # Test specific faction exists in both
        test_faction = "The Archivists"
        if test_faction in common_factions:
            print(f"   ✅ Test faction '{test_faction}' found in both systems")
            return len(common_factions) >= 10
        else:
            print(f"   ❌ Test faction not found in both systems")
            return False
            
    except Exception as e:
        print(f"   💥 Consistency check error: {e}")
        return False

def test_file_structure():
    """Test required files exist"""
    import os
    
    required_files = [
        'azure_image_tools.py',
        'tec_visual_asset_generator.py', 
        'tec_persona_api.py',
        'tec_visual_enhancement_interface.html'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - Missing")
            missing_files.append(file)
    
    return len(missing_files) == 0

# Run all tests
print("🚀 Starting verification tests...\n")

test_component("File Structure", test_file_structure)
test_component("Azure Image Tools", test_azure_image_tools)
test_component("Visual Asset Generator", test_visual_asset_generator)
test_component("Backend API Imports", test_backend_api_imports)
test_component("Faction Database Consistency", test_faction_database_consistency)

# Print results
print("\n" + "=" * 60)
print("📊 VERIFICATION RESULTS")
print("=" * 60)
print(f"🧪 Tests Run: {tests_total}")
print(f"✅ Passed: {tests_passed}")
print(f"❌ Failed: {tests_total - tests_passed}")

if tests_passed == tests_total:
    print(f"\n🎉 ALL VERIFICATION TESTS PASSED!")
    print(f"🚀 TEC Visual Enhancement System is ready for deployment!")
    print(f"\n💡 Next steps:")
    print(f"   1. Run: python tec_persona_api.py")
    print(f"   2. Open: http://localhost:8000/tec_visual_enhancement_interface.html")
    print(f"   3. Start generating visual assets!")
else:
    print(f"\n⚠️  Some tests failed. Review errors above.")

print("=" * 60)
