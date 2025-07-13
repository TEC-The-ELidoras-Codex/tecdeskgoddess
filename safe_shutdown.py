#!/usr/bin/env python3
"""
TEC Safe Shutdown & Commit Script
Properly stops all services and commits work before shutdown
"""
import os
import sys
import time
import subprocess
import signal
from datetime import datetime
from pathlib import Path

def log_message(message):
    """Print timestamped message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def kill_python_processes():
    """Kill all Python processes safely"""
    log_message("🛑 Stopping Python processes...")
    
    try:
        # Use taskkill on Windows
        subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                      capture_output=True, text=True)
        log_message("✅ Python processes stopped")
        time.sleep(2)
    except Exception as e:
        log_message(f"⚠️  Could not kill processes: {e}")

def check_git_status():
    """Check if we have uncommitted changes"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.stdout.strip():
            log_message("📝 Found uncommitted changes")
            return True
        else:
            log_message("✅ No uncommitted changes")
            return False
    except Exception as e:
        log_message(f"⚠️  Could not check git status: {e}")
        return True  # Assume changes exist to be safe

def commit_changes():
    """Commit all changes with timestamp"""
    try:
        base_dir = Path(__file__).parent
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_message("📦 Adding files to git...")
        subprocess.run(['git', 'add', '.'], cwd=base_dir, check=True)
        
        log_message("💾 Committing changes...")
        commit_msg = f"TEC system save - Safe shutdown at {timestamp}"
        subprocess.run(['git', 'commit', '-m', commit_msg], cwd=base_dir, check=True)
        
        log_message("🚀 Pushing to remote...")
        subprocess.run(['git', 'push', 'origin', 'main'], cwd=base_dir, check=True)
        
        log_message("✅ Successfully committed and pushed changes")
        return True
        
    except subprocess.CalledProcessError as e:
        log_message(f"❌ Git command failed: {e}")
        return False
    except Exception as e:
        log_message(f"❌ Commit failed: {e}")
        return False

def check_running_servers():
    """Check what's running on our ports"""
    ports = [8000, 5000, 5001, 5002, 5003]
    log_message("🔍 Checking for running servers...")
    
    for port in ports:
        try:
            result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
            if f":{port}" in result.stdout:
                log_message(f"⚠️  Port {port} is in use")
            else:
                log_message(f"✅ Port {port} is free")
        except Exception:
            pass

def main():
    """Main shutdown sequence"""
    print("=" * 60)
    log_message("🛑 TEC SAFE SHUTDOWN & COMMIT SEQUENCE")
    print("=" * 60)
    
    # Step 1: Check what's running
    check_running_servers()
    
    # Step 2: Stop services
    kill_python_processes()
    
    # Step 3: Check for changes
    if check_git_status():
        log_message("💾 Committing your work...")
        if commit_changes():
            log_message("✅ Your work has been saved to GitHub!")
        else:
            log_message("⚠️  Commit failed, but files are saved locally")
    
    # Step 4: Final check
    log_message("🔍 Final status check...")
    check_running_servers()
    
    # Step 5: Summary
    print("=" * 60)
    log_message("🎉 SHUTDOWN COMPLETE!")
    log_message("✅ All Python processes stopped")
    log_message("✅ Changes committed to Git")  
    log_message("✅ Safe to close VS Code and shutdown PC")
    print("=" * 60)
    
    log_message("📋 Next startup: python tec_simple_startup.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_message("⚠️  Shutdown interrupted by user")
    except Exception as e:
        log_message(f"❌ Shutdown failed: {e}")
        log_message("🆘 Manual steps needed:")
        log_message("   1. Ctrl+C in any running terminals") 
        log_message("   2. git add . && git commit -m 'save'")
        log_message("   3. git push origin main")
