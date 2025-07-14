#!/usr/bin/env python3
"""
TEC System Diagnostic and Monitor
Comprehensive system health checking and auto-recovery
"""
import os
import sys
import time
import requests
import subprocess
import logging
from pathlib import Path
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tec_diagnostics.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class TECDiagnostics:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.api_url = "http://localhost:8000"
        self.required_files = [
            "tec_chat.html",
            "tec_complete_interface.html",
            "src/simple_api.py",
            "main.py"
        ]
        
    def check_file_integrity(self):
        """Check that all required files exist and have content"""
        logger.info("🔍 Checking file integrity...")
        issues = []
        
        for file_path in self.required_files:
            full_path = self.base_dir / file_path
            if not full_path.exists():
                issues.append(f"❌ Missing file: {file_path}")
            elif full_path.stat().st_size == 0:
                issues.append(f"❌ Empty file: {file_path}")
            else:
                logger.info(f"✅ {file_path}: OK ({full_path.stat().st_size} bytes)")
        
        return issues
    
    def check_api_health(self):
        """Check if API endpoints are responding correctly"""
        logger.info("🔍 Checking API health...")
        issues = []
        
        endpoints = [
            "/health",
            "/",
            "/tec_complete_interface.html",
            "/tec_chat.html"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.api_url}{endpoint}", timeout=5)
                if endpoint == "/health":
                    if response.status_code == 200:
                        logger.info(f"✅ {endpoint}: OK (200)")
                    else:
                        issues.append(f"❌ {endpoint}: Status {response.status_code}")
                else:
                    if response.status_code == 200 and len(response.text) > 100:
                        logger.info(f"✅ {endpoint}: OK (200, {len(response.text)} bytes)")
                    elif response.status_code == 404:
                        issues.append(f"❌ {endpoint}: 404 Not Found")
                    else:
                        issues.append(f"❌ {endpoint}: Status {response.status_code}, {len(response.text)} bytes")
                        
            except requests.exceptions.ConnectionError:
                issues.append(f"❌ {endpoint}: Connection refused (server not running)")
            except Exception as e:
                issues.append(f"❌ {endpoint}: Error - {str(e)}")
        
        return issues
    
    def check_process_status(self):
        """Check if TEC processes are running"""
        logger.info("🔍 Checking process status...")
        try:
            # Check if port 8000 is listening
            result = subprocess.run(
                ["netstat", "-an"], 
                capture_output=True, 
                text=True
            )
            
            if ":8000" in result.stdout:
                logger.info("✅ Port 8000: Listening")
                return []
            else:
                return ["❌ Port 8000: Not listening"]
                
        except Exception as e:
            return [f"❌ Process check error: {str(e)}"]
    
    def auto_fix_files(self):
        """Automatically fix common file issues"""
        logger.info("🔧 Attempting auto-fix...")
        fixes_applied = []
        
        # Check and restore HTML files from examples
        html_files = ["tec_chat.html", "tec_complete_interface.html"]
        
        for html_file in html_files:
            main_file = self.base_dir / html_file
            backup_file = self.base_dir / "examples" / html_file
            
            if not main_file.exists() or main_file.stat().st_size == 0:
                if backup_file.exists() and backup_file.stat().st_size > 0:
                    try:
                        import shutil
                        shutil.copy2(backup_file, main_file)
                        fixes_applied.append(f"✅ Restored {html_file} from examples")
                    except Exception as e:
                        fixes_applied.append(f"❌ Failed to restore {html_file}: {str(e)}")
        
        return fixes_applied
    
    def generate_report(self):
        """Generate comprehensive diagnostic report"""
        logger.info("📊 Generating diagnostic report...")
        
        report = [
            "=" * 60,
            "TEC SYSTEM DIAGNOSTIC REPORT",
            f"Generated: {datetime.now().isoformat()}",
            "=" * 60,
            ""
        ]
        
        # File integrity check
        file_issues = self.check_file_integrity()
        if file_issues:
            report.extend(["🔴 FILE INTEGRITY ISSUES:", ""])
            report.extend(file_issues)
            report.append("")
            
            # Try auto-fix
            fixes = self.auto_fix_files()
            if fixes:
                report.extend(["🔧 AUTO-FIX ATTEMPTS:", ""])
                report.extend(fixes)
                report.append("")
                
                # Re-check after fixes
                file_issues = self.check_file_integrity()
        
        if not file_issues:
            report.extend(["✅ FILE INTEGRITY: All files OK", ""])
        
        # Process status check
        process_issues = self.check_process_status()
        if process_issues:
            report.extend(["🔴 PROCESS ISSUES:", ""])
            report.extend(process_issues)
            report.append("")
        else:
            report.extend(["✅ PROCESS STATUS: OK", ""])
        
        # API health check
        api_issues = self.check_api_health()
        if api_issues:
            report.extend(["🔴 API ISSUES:", ""])
            report.extend(api_issues)
            report.append("")
        else:
            report.extend(["✅ API HEALTH: All endpoints OK", ""])
        
        # Summary
        total_issues = len(file_issues) + len(process_issues) + len(api_issues)
        
        report.extend([
            "=" * 60,
            "SUMMARY",
            "=" * 60
        ])
        
        if total_issues == 0:
            report.append("🎉 ALL SYSTEMS OPERATIONAL")
        else:
            report.append(f"⚠️  TOTAL ISSUES FOUND: {total_issues}")
            
            if not process_issues and file_issues:
                report.extend([
                    "",
                    "💡 RECOMMENDED ACTION:",
                    "   Restart the TEC system: python main.py --simple"
                ])
            elif process_issues:
                report.extend([
                    "",
                    "💡 RECOMMENDED ACTION:",
                    "   Start the TEC system: python main.py --simple"
                ])
        
        report.extend([
            "",
            "=" * 60,
            "TEC Diagnostics Complete",
            "=" * 60
        ])
        
        return "\n".join(report)
    
    def run_diagnostics(self):
        """Run full diagnostic suite"""
        report = self.generate_report()
        
        # Print report
        print(report)
        
        # Save report
        report_file = self.base_dir / f"diagnostic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        
        logger.info(f"📄 Report saved to: {report_file}")
        
        return report

def main():
    diagnostics = TECDiagnostics()
    diagnostics.run_diagnostics()

if __name__ == "__main__":
    main()
