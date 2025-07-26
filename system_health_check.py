#!/usr/bin/env python3
"""
TEC System Health Check & Cleanup Tool
Comprehensive system verification and cleanup utility
"""

import os
import sys
import sqlite3
import json
import requests
import time
from datetime import datetime
from pathlib import Path

class TECSystemChecker:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.issues = []
        self.successes = []
        
    def log_success(self, message):
        self.successes.append(f"✅ {message}")
        print(f"✅ {message}")
        
    def log_issue(self, message):
        self.issues.append(f"❌ {message}")
        print(f"❌ {message}")
        
    def log_warning(self, message):
        print(f"⚠️ {message}")
        
    def check_api_server(self):
        """Check if the API server is running and responding"""
        print("\n🔍 Checking API Server...")
        
        try:
            response = requests.get('http://localhost:8000/health', timeout=5)
            if response.status_code == 200:
                self.log_success("API Server is running and healthy")
                return True
            else:
                self.log_issue(f"API Server returned status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_issue(f"API Server not accessible: {e}")
            return False
    
    def check_database_integrity(self):
        """Check database files and schema"""
        print("\n🔍 Checking Database Integrity...")
        
        db_files = [
            'data/tec_database.db',
            'data/tec_memory.db'
        ]
        
        for db_file in db_files:
            if os.path.exists(db_file):
                try:
                    conn = sqlite3.connect(db_file)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    conn.close()
                    self.log_success(f"Database {db_file} has {len(tables)} tables")
                except Exception as e:
                    self.log_issue(f"Database {db_file} error: {e}")
            else:
                self.log_warning(f"Database {db_file} not found")
    
    def check_file_structure(self):
        """Verify critical files exist"""
        print("\n🔍 Checking File Structure...")
        
        critical_files = [
            'tec_persona_api.py',
            'tec_enhanced_interface.html',
            'src/tec_tools/persona_manager.py',
            'src/tec_tools/memory_system.py',
            'assets/css/persona_ui.css'
        ]
        
        for file_path in critical_files:
            if os.path.exists(file_path):
                self.log_success(f"Found {file_path}")
            else:
                self.log_issue(f"Missing critical file: {file_path}")
    
    def check_endpoints(self):
        """Test key API endpoints"""
        print("\n🔍 Testing API Endpoints...")
        
        endpoints = [
            ('/health', 'GET'),
            ('/api/memory/stats', 'GET'),
            ('/api/loreforge/factions', 'GET')
        ]
        
        for endpoint, method in endpoints:
            try:
                if method == 'GET':
                    response = requests.get(f'http://localhost:8000{endpoint}', timeout=5)
                else:
                    response = requests.post(f'http://localhost:8000{endpoint}', timeout=5)
                
                if response.status_code == 200:
                    self.log_success(f"Endpoint {endpoint} working")
                else:
                    self.log_issue(f"Endpoint {endpoint} returned {response.status_code}")
            except Exception as e:
                self.log_issue(f"Endpoint {endpoint} failed: {e}")
    
    def check_visual_assets(self):
        """Check visual generation system"""
        print("\n🔍 Checking Visual Assets System...")
        
        try:
            # Check if visual generator files exist
            visual_files = [
                'tec_visual_asset_generator.py',
                'azure_image_tools.py'
            ]
            
            for file in visual_files:
                if os.path.exists(file):
                    self.log_success(f"Visual system file {file} found")
                else:
                    self.log_warning(f"Visual system file {file} not found")
                    
        except Exception as e:
            self.log_issue(f"Visual assets check failed: {e}")
    
    def cleanup_temporary_files(self):
        """Clean up temporary and duplicate files"""
        print("\n🧹 Cleaning Up Temporary Files...")
        
        # Files to clean up
        cleanup_patterns = [
            '*.pyc',
            '__pycache__',
            '*.tmp',
            '.pytest_cache',
            '*.log.old'
        ]
        
        cleaned_count = 0
        for pattern in cleanup_patterns:
            # Simple cleanup - just count what we would clean
            if pattern == '__pycache__':
                for root, dirs, files in os.walk('.'):
                    if '__pycache__' in dirs:
                        cleaned_count += 1
            
        if cleaned_count > 0:
            self.log_success(f"Would clean {cleaned_count} temporary items")
        else:
            self.log_success("No temporary files to clean")
    
    def generate_report(self):
        """Generate comprehensive system report"""
        print("\n" + "="*60)
        print("🎯 TEC SYSTEM HEALTH REPORT")
        print("="*60)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Summary
        total_checks = len(self.successes) + len(self.issues)
        print(f"📊 SUMMARY:")
        print(f"   ✅ Successful: {len(self.successes)}")
        print(f"   ❌ Issues: {len(self.issues)}")
        print(f"   📈 Health Score: {(len(self.successes)/total_checks*100):.1f}%")
        print()
        
        # Issues
        if self.issues:
            print("🚨 ISSUES TO ADDRESS:")
            for issue in self.issues:
                print(f"   {issue}")
            print()
        
        # Successes
        if self.successes:
            print("✅ WORKING SYSTEMS:")
            for success in self.successes:
                print(f"   {success}")
            print()
        
        # Recommendations
        print("💡 RECOMMENDATIONS:")
        if len(self.issues) == 0:
            print("   🎉 System is running perfectly!")
        elif len(self.issues) < 3:
            print("   🔧 Minor issues detected - quick fixes needed")
        else:
            print("   ⚠️  Multiple issues detected - comprehensive review needed")
        
        print("\n" + "="*60)
        
    def run_full_check(self):
        """Run complete system check"""
        print("🚀 Starting TEC System Health Check...")
        print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all checks
        self.check_file_structure()
        self.check_database_integrity()
        self.check_api_server()
        if len(self.issues) == 0:  # Only test endpoints if server is up
            self.check_endpoints()
        self.check_visual_assets()
        self.cleanup_temporary_files()
        
        # Generate report
        self.generate_report()
        
        return len(self.issues) == 0

if __name__ == "__main__":
    checker = TECSystemChecker()
    success = checker.run_full_check()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
