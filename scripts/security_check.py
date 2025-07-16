#!/usr/bin/env python3
"""
TEC Security Check Script
Scans for API keys and sensitive data before commits
"""

import os
import re
import sys
from pathlib import Path

def check_for_sensitive_data():
    """Check for API keys and sensitive data in staged files"""
    
    # Patterns to search for
    sensitive_patterns = [
        r'sk-[a-zA-Z0-9]{48}',  # OpenAI API keys
        r'AIza[0-9A-Za-z-_]{35}',  # Google API keys
        r'AKIA[0-9A-Z]{16}',  # AWS Access Keys
        r'ghp_[a-zA-Z0-9]{36}',  # GitHub Personal Access Tokens
        r'xoxb-[0-9]{13}-[0-9]{13}-[a-zA-Z0-9]{24}',  # Slack Bot tokens
        r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',  # UUIDs (could be API keys)
    ]
    
    # Files to check
    files_to_check = []
    
    # Get staged files
    try:
        result = os.popen('git diff --cached --name-only').read()
        files_to_check = result.strip().split('\n') if result.strip() else []
    except:
        # If git command fails, check common files
        files_to_check = ['main.py', 'tec_complete_interface.html', 'CHEAT_SHEET.md']
    
    issues_found = []
    
    for file_path in files_to_check:
        if not file_path or not os.path.exists(file_path):
            continue
            
        # Skip binary files and common safe files
        if file_path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.ico', '.zip', '.exe')):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Check for sensitive patterns
            for pattern in sensitive_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    issues_found.append(f"Potential API key found in {file_path}: {pattern}")
                    
            # Check for common sensitive strings
            if 'password' in content.lower() and '=' in content:
                if not any(skip in content.lower() for skip in ['password_field', 'password_input', 'password_label']):
                    issues_found.append(f"Potential password found in {file_path}")
                    
        except Exception as e:
            # Don't fail on file read errors
            pass
    
    return issues_found

def main():
    """Main security check function"""
    
    print("TEC Security Check - Scanning for sensitive data...")
    
    issues = check_for_sensitive_data()
    
    if issues:
        print("\nSecurity issues detected:")
        for issue in issues:
            print(f"   {issue}")
        print("\nTips:")
        print("   • Move API keys to .env file")
        print("   • Use environment variables")
        print("   • Check .gitignore includes .env")
        print("   • Remove sensitive data from staged files")
        return 1
    else:
        print("No sensitive data detected - Safe to commit!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
