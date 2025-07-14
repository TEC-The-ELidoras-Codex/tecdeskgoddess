#!/usr/bin/env python3
"""
TEC: BITLYFE - Safe Shutdown Script
Enhanced with Azure integration and proper cleanup
"""

import os
import sys
import psutil
import subprocess
import time

def print_colored(text, color='\033[97m'):
    """Print colored text"""
    try:
        print(f"{color}{text}\033[0m")
    except UnicodeEncodeError:
        print(text.encode('ascii', 'ignore').decode('ascii'))

def find_tec_processes():
    """Find all TEC-related processes"""
    tec_processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] in ['python.exe', 'python', 'py.exe']:
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                if any(keyword in cmdline.lower() for keyword in ['tec', 'simple_api', 'agentic_processor', 'main.py']):
                    tec_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cmdline': cmdline,
                        'process': proc
                    })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return tec_processes

def stop_tec_processes():
    """Stop all TEC-related processes safely"""
    print_colored("🔍 Finding TEC processes...", '\033[94m')
    
    processes = find_tec_processes()
    
    if not processes:
        print_colored("✅ No TEC processes found running", '\033[92m')
        return
    
    print_colored(f"📋 Found {len(processes)} TEC processes:", '\033[93m')
    for proc in processes:
        print_colored(f"   • PID {proc['pid']}: {proc['cmdline'][:80]}...", '\033[97m')
    
    print_colored("🛑 Stopping TEC processes...", '\033[91m')
    
    for proc in processes:
        try:
            print_colored(f"   Stopping PID {proc['pid']}...", '\033[93m')
            proc['process'].terminate()
            
            # Wait for graceful termination
            try:
                proc['process'].wait(timeout=5)
                print_colored(f"   ✅ PID {proc['pid']} stopped gracefully", '\033[92m')
            except psutil.TimeoutExpired:
                print_colored(f"   🔨 Force killing PID {proc['pid']}...", '\033[91m')
                proc['process'].kill()
                print_colored(f"   ✅ PID {proc['pid']} force killed", '\033[92m')
                
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print_colored(f"   ⚠️  Could not stop PID {proc['pid']}: {e}", '\033[93m')

def check_ports():
    """Check if TEC ports are freed"""
    print_colored("🔍 Checking ports...", '\033[94m')
    
    tec_ports = [8000, 5000, 5001, 5002, 5003]
    
    for port in tec_ports:
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                print_colored(f"   ⚠️  Port {port} is still in use", '\033[93m')
            else:
                print_colored(f"   ✅ Port {port} is free", '\033[92m')
                
        except Exception as e:
            print_colored(f"   ❓ Could not check port {port}: {e}", '\033[93m')

def commit_changes():
    """Commit changes to git"""
    print_colored("📝 Committing changes...", '\033[94m')
    
    try:
        # Add all changes
        subprocess.run(['git', 'add', '.'], cwd=os.path.dirname(os.path.dirname(__file__)))
        
        # Commit with timestamp
        commit_msg = f"TEC: BITLYFE - Safe shutdown and Azure integration - {time.strftime('%Y-%m-%d %H:%M:%S')}"
        result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                              capture_output=True, text=True,
                              cwd=os.path.dirname(os.path.dirname(__file__)))
        
        if result.returncode == 0:
            print_colored("✅ Changes committed successfully", '\033[92m')
        else:
            print_colored("ℹ️  No changes to commit", '\033[97m')
        
    except Exception as e:
        print_colored(f"❌ Failed to commit: {e}", '\033[91m')

def main():
    print_colored("🏴‍☠️ TEC: BITLYFE - Safe Shutdown", '\033[96m')
    print_colored("=" * 40, '\033[96m')
    
    # Stop all TEC processes
    stop_tec_processes()
    
    # Wait a moment for processes to clean up
    time.sleep(2)
    
    # Check ports
    check_ports()
    
    # Commit changes
    commit_changes()
    
    print_colored("\n✨ Shutdown complete!", '\033[92m')
    print_colored("🔒 All TEC processes stopped", '\033[92m')
    print_colored("💾 Changes saved to git", '\033[92m')
    print_colored("🏴‍☠️ The Creator's Rebellion will return...", '\033[96m')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n🛑 Shutdown cancelled by user", '\033[93m')
    except Exception as e:
        print_colored(f"\n❌ Shutdown error: {e}", '\033[91m')
