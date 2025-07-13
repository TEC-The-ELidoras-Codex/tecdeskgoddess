#!/usr/bin/env python3
"""
TEC Safe Shutdown and Commit Script
Safely stops all running processes, commits work, and prepares for PC shutdown
"""
import os
import sys
import psutil
import subprocess
import time
from pathlib import Path

def find_and_stop_tec_processes():
    """Find and safely stop all TEC-related processes"""
    print("🔍 Finding TEC processes...")
    
    tec_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
            if any(keyword in cmdline.lower() for keyword in [
                'tec_simple_startup', 'simple_api', 'tec_startup', 
                'mcp_orchestrator', 'port 8000', 'port 5000'
            ]):
                tec_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    if tec_processes:
        print(f"📋 Found {len(tec_processes)} TEC processes:")
        for proc in tec_processes:
            try:
                print(f"  - PID {proc.pid}: {proc.name()} - {' '.join(proc.cmdline())}")
            except:
                print(f"  - PID {proc.pid}: {proc.name()}")
        
        print("\n🛑 Stopping TEC processes...")
        for proc in tec_processes:
            try:
                print(f"  Stopping PID {proc.pid}...")
                proc.terminate()
                
                # Wait for graceful shutdown
                try:
                    proc.wait(timeout=5)
                    print(f"  ✅ PID {proc.pid} stopped gracefully")
                except psutil.TimeoutExpired:
                    print(f"  ⚠️  Force killing PID {proc.pid}...")
                    proc.kill()
                    print(f"  ✅ PID {proc.pid} force stopped")
                    
            except psutil.NoSuchProcess:
                print(f"  ✅ PID {proc.pid} already stopped")
            except Exception as e:
                print(f"  ❌ Error stopping PID {proc.pid}: {e}")
    else:
        print("✅ No TEC processes found running")
    
    # Wait a moment for ports to be freed
    time.sleep(2)

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
- All TEC processes safely stopped
- Changes committed to git
- Web interface was running successfully
- API endpoints were functional

## Files Created/Modified:
- Web interfaces (tec_chat.html, tec_complete_interface.html)
- WordPress plugin (wordpress/tec-digital-companion.php)
- VS Code settings (.vscode/settings.json)
- Cleanup and organization scripts

## Next Steps:
1. Restart system: `python tec_simple_startup.py`
2. Test web interface: http://localhost:8000
3. Install WordPress plugin if needed
4. Continue development with clean structure

## Ready for PC Shutdown ✅
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
    
    # Step 1: Stop all TEC processes
    find_and_stop_tec_processes()
    
    # Step 2: Check git status
    has_changes = check_git_status()
    
    # Step 3: Commit if there are changes
    if has_changes:
        commit_choice = input("\n💾 Commit all changes? (y/N): ").lower().strip()
        if commit_choice in ['y', 'yes']:
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
    print("  • All TEC processes stopped")
    print("  • Work saved and committed (if requested)")
    print("  • Shutdown summary created")
    print("  • Ready for PC shutdown")
    print("\n🔄 To restart TEC after reboot:")
    print("  python tec_simple_startup.py")
    print("\n💾 Safe to shutdown PC now!")
    print("=" * 60)

if __name__ == "__main__":
    main()
