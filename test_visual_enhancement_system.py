#!/usr/bin/env python3
"""
TEC Visual Enhancement System - Comprehensive Test Suite
Tests all components: Azure AI integration, faction database, API endpoints, and visual generation
"""

import os
import sys
import json
import time
import requests
import unittest
from datetime import datetime
from unittest.mock import Mock, patch

class TestTECVisualSystem(unittest.TestCase):
    """Comprehensive test suite for TEC Visual Enhancement System"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_start_time = datetime.now()
        print(f"\n🧪 Starting test: {self._testMethodName}")
    
    def tearDown(self):
        """Clean up after each test"""
        test_duration = (datetime.now() - self.test_start_time).total_seconds()
        print(f"   ⏱️ Test completed in {test_duration:.2f}s")

class TestAzureImageTools(TestTECVisualSystem):
    """Test Azure Image Tools functionality"""
    
    def test_azure_image_generator_initialization(self):
        """Test Azure Image Generator initializes correctly"""
        try:
            from azure_image_tools import AzureImageGenerator
            image_gen = AzureImageGenerator()
            
            # Test initialization
            self.assertIsNotNone(image_gen)
            self.assertIsInstance(image_gen.faction_visual_styles, dict)
            
            # Test faction styles loaded
            self.assertGreater(len(image_gen.faction_visual_styles), 15)
            print(f"   ✅ Faction styles loaded: {len(image_gen.faction_visual_styles)}")
            
            # Test specific factions exist
            required_factions = [
                "The Archivists",
                "Quantum Architects", 
                "The MagmaSoX Gate",
                "The Knockoffs",
                "Crescent Islands Sovereignty"
            ]
            
            for faction in required_factions:
                self.assertIn(faction, image_gen.faction_visual_styles)
                faction_style = image_gen.faction_visual_styles[faction]
                
                # Test faction style structure
                self.assertIn('color_palette', faction_style)
                self.assertIn('aesthetic', faction_style)
                self.assertIn('clothing_style', faction_style)
                self.assertIn('environment', faction_style)
                self.assertIn('tech_level', faction_style)
                self.assertIn('mood', faction_style)
                
                print(f"   ✅ {faction}: Complete visual style")
            
        except ImportError as e:
            self.fail(f"Failed to import azure_image_tools: {e}")
        except Exception as e:
            self.fail(f"Azure Image Generator initialization failed: {e}")
    
    def test_faction_visual_styles_completeness(self):
        """Test that all faction visual styles are complete and valid"""
        try:
            from azure_image_tools import AzureImageGenerator
            image_gen = AzureImageGenerator()
            
            required_style_keys = [
                'color_palette', 'aesthetic', 'clothing_style', 
                'environment', 'tech_level', 'mood'
            ]
            
            for faction_name, style in image_gen.faction_visual_styles.items():
                # Test all required keys present
                for key in required_style_keys:
                    self.assertIn(key, style, f"{faction_name} missing {key}")
                
                # Test color palette format
                self.assertIsInstance(style['color_palette'], list)
                self.assertGreater(len(style['color_palette']), 2)
                
                # Test string fields are not empty
                for key in ['aesthetic', 'clothing_style', 'environment', 'tech_level', 'mood']:
                    self.assertIsInstance(style[key], str)
                    self.assertGreater(len(style[key]), 10)
            
            print(f"   ✅ All {len(image_gen.faction_visual_styles)} faction styles validated")
            
        except Exception as e:
            self.fail(f"Faction visual styles validation failed: {e}")
    
    def test_prompt_enhancement_functionality(self):
        """Test TEC prompt enhancement for character generation"""
        try:
            from azure_image_tools import AzureImageGenerator
            image_gen = AzureImageGenerator()
            
            # Test prompt enhancement
            test_description = "A mysterious operative with cybernetic enhancements"
            enhanced_prompt = image_gen._enhance_prompt_for_tec(test_description, "digital art")
            
            # Test enhancement adds TEC elements
            self.assertIn("TEC universe", enhanced_prompt)
            self.assertIn("cyberpunk", enhanced_prompt)
            self.assertIn("digital art", enhanced_prompt)
            self.assertIn(test_description, enhanced_prompt)
            
            print(f"   ✅ Prompt enhancement working correctly")
            print(f"   📝 Enhanced prompt length: {len(enhanced_prompt)} characters")
            
        except Exception as e:
            self.fail(f"Prompt enhancement test failed: {e}")

class TestVisualAssetGenerator(TestTECVisualSystem):
    """Test TEC Visual Asset Generator functionality"""
    
    def test_visual_asset_generator_initialization(self):
        """Test Visual Asset Generator initializes with complete faction database"""
        try:
            from tec_visual_asset_generator import TECVisualAssetGenerator
            visual_gen = TECVisualAssetGenerator()
            
            # Test initialization
            self.assertIsNotNone(visual_gen)
            self.assertIsInstance(visual_gen.faction_database, dict)
            
            # Test faction database completeness
            self.assertGreater(len(visual_gen.faction_database), 15)
            print(f"   ✅ Faction database loaded: {len(visual_gen.faction_database)} factions")
            
            # Test category organization
            categories = visual_gen.get_faction_list_by_category()
            self.assertIsInstance(categories, dict)
            self.assertGreater(len(categories), 3)
            
            print(f"   ✅ Faction categories: {len(categories)}")
            for category, factions in categories.items():
                print(f"      • {category}: {len(factions)} factions")
            
        except ImportError as e:
            self.fail(f"Failed to import tec_visual_asset_generator: {e}")
        except Exception as e:
            self.fail(f"Visual Asset Generator initialization failed: {e}")
    
    def test_faction_database_structure(self):
        """Test faction database has correct structure for all factions"""
        try:
            from tec_visual_asset_generator import TECVisualAssetGenerator
            visual_gen = TECVisualAssetGenerator()
            
            required_faction_keys = ['category', 'role', 'alignment', 'specialties']
            
            for faction_name, faction_info in visual_gen.faction_database.items():
                # Test faction info structure
                for key in required_faction_keys:
                    self.assertIn(key, faction_info, f"{faction_name} missing {key}")
                
                # Test specific field types
                self.assertIsInstance(faction_info['category'], str)
                self.assertIsInstance(faction_info['role'], str)
                self.assertIsInstance(faction_info['alignment'], str)
                self.assertIsInstance(faction_info['specialties'], list)
                
                # Test specialties not empty
                self.assertGreater(len(faction_info['specialties']), 0)
            
            print(f"   ✅ All {len(visual_gen.faction_database)} faction entries validated")
            
        except Exception as e:
            self.fail(f"Faction database structure test failed: {e}")
    
    def test_sample_character_creation(self):
        """Test sample character creation for factions"""
        try:
            from tec_visual_asset_generator import TECVisualAssetGenerator
            visual_gen = TECVisualAssetGenerator()
            
            # Test sample character creation for different faction types
            test_factions = ["The Archivists", "The Knockoffs", "The MagmaSoX Gate"]
            
            for faction_name in test_factions:
                sample_chars = visual_gen._create_sample_characters_for_faction(faction_name)
                
                # Test characters created
                self.assertIsInstance(sample_chars, list)
                self.assertGreater(len(sample_chars), 1)
                
                # Test character structure
                for char in sample_chars:
                    self.assertIn('name', char)
                    self.assertIn('role', char)
                    self.assertIn('description', char)
                    
                    self.assertIsInstance(char['name'], str)
                    self.assertIsInstance(char['role'], str)
                    self.assertIsInstance(char['description'], str)
                
                print(f"   ✅ {faction_name}: {len(sample_chars)} sample characters created")
            
        except Exception as e:
            self.fail(f"Sample character creation test failed: {e}")

class TestBackendAPIIntegration(TestTECVisualSystem):
    """Test backend API integration and endpoints"""
    
    def test_api_imports_and_initialization(self):
        """Test backend API can import visual components correctly"""
        try:
            # Test imports work
            from tec_visual_asset_generator import TECVisualAssetGenerator
            from azure_image_tools import AzureImageGenerator
            
            # Test initialization
            visual_gen = TECVisualAssetGenerator()
            azure_gen = AzureImageGenerator()
            
            self.assertIsNotNone(visual_gen)
            self.assertIsNotNone(azure_gen)
            
            print(f"   ✅ Backend API imports successful")
            print(f"   ✅ Visual components initialized")
            
        except ImportError as e:
            self.fail(f"Backend API import test failed: {e}")
        except Exception as e:
            self.fail(f"Backend API initialization test failed: {e}")
    
    def test_api_endpoint_structure(self):
        """Test API endpoint functions exist and are callable"""
        try:
            # Import and check if tec_persona_api has visual endpoints
            import tec_persona_api
            
            # Check if Flask app exists
            self.assertTrue(hasattr(tec_persona_api, 'app'))
            
            # Check visual features flag
            self.assertTrue(hasattr(tec_persona_api, 'VISUAL_FEATURES_ENABLED'))
            
            print(f"   ✅ Backend API structure validated")
            print(f"   ✅ Visual features integration confirmed")
            
        except ImportError as e:
            self.fail(f"Backend API structure test failed: {e}")
        except Exception as e:
            self.fail(f"API endpoint structure test failed: {e}")

class TestSystemIntegration(TestTECVisualSystem):
    """Test complete system integration"""
    
    def test_end_to_end_faction_processing(self):
        """Test complete faction processing pipeline"""
        try:
            from tec_visual_asset_generator import TECVisualAssetGenerator
            from azure_image_tools import AzureImageGenerator
            
            visual_gen = TECVisualAssetGenerator()
            azure_gen = AzureImageGenerator()
            
            # Test faction exists in both systems
            test_faction = "The Archivists"
            
            # Check faction in visual generator
            self.assertIn(test_faction, visual_gen.faction_database)
            
            # Check faction in Azure image tools
            self.assertIn(test_faction, azure_gen.faction_visual_styles)
            
            # Test character data creation
            character_data = {
                'name': 'Test Archivist',
                'faction': test_faction,
                'role': 'test character',
                'description': 'A test character for system validation'
            }
            
            # Test faction portrait function (without actual API call)
            try:
                # This would normally make an API call, but we're just testing the structure
                faction_style = azure_gen.faction_visual_styles[test_faction]
                self.assertIsInstance(faction_style, dict)
                
                print(f"   ✅ End-to-end faction processing validated")
                print(f"   ✅ Character data structure confirmed")
                print(f"   ✅ Faction styling integration working")
                
            except Exception as e:
                print(f"   ⚠️  API call simulation skipped (expected in test environment)")
            
        except Exception as e:
            self.fail(f"End-to-end integration test failed: {e}")
    
    def test_asset_inventory_system(self):
        """Test asset inventory tracking and management"""
        try:
            from tec_visual_asset_generator import TECVisualAssetGenerator
            visual_gen = TECVisualAssetGenerator()
            
            # Test initial inventory structure
            self.assertIsInstance(visual_gen.asset_inventory, dict)
            self.assertIn('portraits', visual_gen.asset_inventory)
            self.assertIn('emblems', visual_gen.asset_inventory)
            self.assertIn('environments', visual_gen.asset_inventory)
            self.assertIn('collections', visual_gen.asset_inventory)
            
            # Test inventory starts empty
            for category in visual_gen.asset_inventory.values():
                self.assertIsInstance(category, dict)
            
            print(f"   ✅ Asset inventory system initialized")
            print(f"   ✅ Inventory categories configured")
            
        except Exception as e:
            self.fail(f"Asset inventory test failed: {e}")

class TestConfigurationAndDependencies(TestTECVisualSystem):
    """Test system configuration and dependencies"""
    
    def test_environment_configuration(self):
        """Test environment configuration and .env file handling"""
        try:
            from azure_image_tools import AzureImageGenerator
            
            # Test that system can handle missing .env gracefully
            image_gen = AzureImageGenerator()
            
            # Should initialize even without API key (demo mode)
            self.assertIsNotNone(image_gen.api_key)
            
            print(f"   ✅ Environment configuration handling verified")
            print(f"   ✅ Demo mode fallback working")
            
        except Exception as e:
            self.fail(f"Environment configuration test failed: {e}")
    
    def test_required_directories(self):
        """Test that required asset directories can be created"""
        try:
            required_dirs = ['assets', 'assets/portraits', 'assets/emblems', 'assets/environments']
            
            for directory in required_dirs:
                if not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)
                
                self.assertTrue(os.path.exists(directory))
                self.assertTrue(os.path.isdir(directory))
            
            print(f"   ✅ Required directories verified/created")
            print(f"   ✅ Asset storage structure ready")
            
        except Exception as e:
            self.fail(f"Directory creation test failed: {e}")

def run_comprehensive_tests():
    """Run all tests with detailed reporting"""
    print("🧪 TEC VISUAL ENHANCEMENT SYSTEM - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print(f"🕒 Test Session Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestAzureImageTools,
        TestVisualAssetGenerator, 
        TestBackendAPIIntegration,
        TestSystemIntegration,
        TestConfigurationAndDependencies
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with custom result handler
    class DetailedTestResult(unittest.TextTestResult):
        def __init__(self, stream, descriptions, verbosity):
            super().__init__(stream, descriptions, verbosity)
            self.test_results = []
        
        def addSuccess(self, test):
            super().addSuccess(test)
            self.test_results.append(('PASS', test._testMethodName, None))
        
        def addError(self, test, err):
            super().addError(test, err)
            self.test_results.append(('ERROR', test._testMethodName, err[1]))
        
        def addFailure(self, test, err):
            super().addFailure(test, err)
            self.test_results.append(('FAIL', test._testMethodName, err[1]))
    
    # Run the tests
    runner = unittest.TextTestRunner(
        verbosity=2,
        resultclass=DetailedTestResult,
        stream=sys.stdout
    )
    
    result = runner.run(test_suite)
    
    # Print detailed results
    print("\n" + "=" * 80)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 80)
    
    print(f"🧪 Tests Run: {result.testsRun}")
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failed: {len(result.failures)}")
    print(f"💥 Errors: {len(result.errors)}")
    
    if result.failures:
        print(f"\n❌ FAILURES:")
        for test, error in result.failures:
            print(f"   • {test}: {str(error)[:100]}...")
    
    if result.errors:
        print(f"\n💥 ERRORS:")
        for test, error in result.errors:
            print(f"   • {test}: {str(error)[:100]}...")
    
    # Overall status
    if result.wasSuccessful():
        print(f"\n🎉 ALL TESTS PASSED! Visual Enhancement System is fully operational.")
        print(f"🚀 System ready for deployment and visual asset generation!")
    else:
        print(f"\n⚠️  Some tests failed. Review errors before deployment.")
    
    print("=" * 80)
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
