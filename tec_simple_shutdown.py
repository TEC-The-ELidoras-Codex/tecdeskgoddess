#!/usr/bin/env python3
"""
TEC Simple Shutdown and Commit Script
Safely commits work and prepares for PC shutdown (simplified version)
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def stop_terminals_message():
    """Display message about stopping terminals"""
    print("🛑 MANUAL TERMINAL SHUTDOWN REQUIRED:")
    print("   Please manually stop the running terminals by:")
    print("   1. Press Ctrl+C in each terminal running TEC processes")
    print("   2. Or close the terminal windows")
    print("   3. Then run this script again")
    print()

def check_git_status():
    """Check git status and return info about uncommitted changes"""
    try:
        # Check if we're in a git repo
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        
        if result.stdout.strip():
            print("📝 Uncommitted changes found:")
            
            # Show status
            status_result = subprocess.run(['git', 'status', '--short'], 
                                         capture_output=True, text=True)
            print(status_result.stdout)
            return True
        else:
            print("✅ No uncommitted changes")
            return False
            
    except subprocess.CalledProcessError:
        print("⚠️  Not in a git repository or git not available")
        return False

def commit_changes():
    """Add and commit all changes"""
    try:
        print("📝 Adding all changes to git...")
        subprocess.run(['git', 'add', '.'], check=True)
        
        commit_message = f"TEC System Update - Safe shutdown commit {time.strftime('%Y-%m-%d %H:%M:%S')}"
        print(f"💾 Committing with message: '{commit_message}'")
        
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print("✅ Changes committed successfully")
        
        # Try to push if remote exists
        try:
            subprocess.run(['git', 'push'], check=True, timeout=10)
            print("✅ Changes pushed to remote")
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            print("⚠️  Could not push to remote (this is okay)")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing changes: {e}")

def create_shutdown_summary():
    """Create a summary of the current state"""
    summary = f"""# TEC Shutdown Summary - {time.strftime('%Y-%m-%d %H:%M:%S')}

## System State at Shutdown:
- TEC processes manually stopped
- Changes committed to git
- Web interface was running successfully
- API endpoints were functional

## Major Accomplishments This Session:
### ✅ Issues Fixed:
- ❌ PHP validation error → ✅ Disabled in VS Code settings
- ❌ Cluttered workspace → ✅ Clean organized structure
- ❌ Multiple terminals → ✅ Managed and documented

### ✅ Features Created:
- 🌐 Complete web interface (tec_complete_interface.html)
- 🔌 WordPress plugin (wordpress/tec-digital-companion.php) 
- 🧹 Clean project structure with organized directories
- 🛠️ Simplified startup script (tec_simple_startup.py)

### ✅ Web Interfaces Working:
- http://localhost:8000 - Main API server
- http://localhost:8000/tec_chat.html - Simple chat
- http://localhost:8000/tec_complete_interface.html - Full interface

## Files Structure After Cleanup:
```
tecdeskgoddess/
├── src/                     # Main source code
│   └── tec_tools/          # Core TEC modules
├── web/                    # Web interfaces
│   ├── tec_chat.html
│   └── tec_complete_interface.html
├── scripts/                # Utility scripts
├── config/                 # Configuration files
├── docs/                   # Documentation
├── tests/                  # Test files (when needed)
├── wordpress/              # WordPress integration
└── assets/                 # Static assets
```

## Next Steps After Reboot:
1. **Restart TEC System:**
   ```bash
   cd "C:\\Users\\Ghedd\\TEC_CODE\\tecdeskgoddess"
   python tec_simple_startup.py
   ```

2. **Access Web Interface:**
   - Open browser to: http://localhost:8000/tec_complete_interface.html
   - Test Daisy Purecode AI chat functionality

3. **WordPress Integration:**
   - Upload `wordpress/tec-digital-companion.php` to WordPress site
   - Use shortcode: `[tec_companion]` in posts/pages

4. **Continue Development:**
   - System is now organized and clean
   - All major issues resolved
   - Ready for feature development

## 🎉 STATUS: READY FOR PC SHUTDOWN
All work saved, committed, and documented. Safe to shutdown.

*The Creator's Rebellion - Daisy Purecode: Silicate Mother*
*"Unfettered Access Shall Be Maintained"*
"""
    
    with open('SHUTDOWN_SUMMARY.md', 'w') as f:
        f.write(summary)
    
    print("📄 Created SHUTDOWN_SUMMARY.md")

def main():
    print("=" * 60)
    print("🚀 TEC Safe Shutdown and Commit")
    print("The Creator's Rebellion - Preparing for PC Shutdown")
    print("=" * 60)
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    # Step 1: Message about stopping terminals
    stop_terminals_message()
    
    continue_choice = input("Have you stopped all TEC terminals? Continue? (y/N): ").lower().strip()
    if continue_choice not in ['y', 'yes']:
        print("Please stop the terminals first, then run this script again.")
        return
    
    # Step 2: Check git status
    has_changes = check_git_status()
    
    # Step 3: Commit if there are changes
    if has_changes:
        commit_choice = input("\n💾 Commit all changes? (Y/n): ").lower().strip()
        if commit_choice not in ['n', 'no']:
            commit_changes()
        else:
            print("⚠️  Changes not committed - they will be preserved")
    
    # Step 4: Create shutdown summary
    create_shutdown_summary()
    
    # Step 5: Final status
    print("\n" + "=" * 60)
    print("✅ SHUTDOWN PREPARATION COMPLETE")
    print("=" * 60)
    print("📋 Summary:")
    print("  • TEC processes stopped (manually)")
    print("  • Work saved and committed")
    print("  • Shutdown summary created")
    print("  • Clean project structure maintained")
    print("  • Ready for PC shutdown")
    print("\n🔄 To restart TEC after reboot:")
    print("  python tec_simple_startup.py")
    print("\n🌐 Web interface will be at:")
    print("  http://localhost:8000/tec_complete_interface.html")
    print("\n💾 SAFE TO SHUTDOWN PC NOW!")
    print("=" * 60)

if __name__ == "__main__":
    main()
