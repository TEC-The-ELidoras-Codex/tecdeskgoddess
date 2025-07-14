#!/usr/bin/env python3
"""
TEC Terminal Manager
Manages running processes and cleans up unused terminals
"""

import psutil
import subprocess
import sys
import logging
import time
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/terminal_manager.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TerminalManager:
    def __init__(self):
        self.tec_processes = []
        self.python_processes = []
        
    def find_tec_processes(self):
        """Find all TEC-related processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
            try:
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                
                # Look for TEC-related processes
                if any(keyword in cmdline.lower() for keyword in [
                    'tec', 'simple_api', 'main.py', 'flask', 'port 8000'
                ]):
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cmdline': cmdline,
                        'create_time': proc.info['create_time'],
                        'age_hours': (time.time() - proc.info['create_time']) / 3600
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        return processes
    
    def find_orphaned_processes(self):
        """Find processes that might be orphaned or stuck"""
        orphaned = []
        all_processes = self.find_tec_processes()
        
        for proc in all_processes:
            # Consider orphaned if running more than 1 hour without activity
            if proc['age_hours'] > 1:
                try:
                    p = psutil.Process(proc['pid'])
                    # Check if process is responding
                    if p.status() == psutil.STATUS_ZOMBIE:
                        orphaned.append(proc)
                except psutil.NoSuchProcess:
                    continue
                    
        return orphaned
    
    def clean_orphaned_processes(self):
        """Clean up orphaned processes"""
        orphaned = self.find_orphaned_processes()
        cleaned = 0
        
        for proc in orphaned:
            try:
                logger.info(f"Terminating orphaned process: PID {proc['pid']} - {proc['cmdline'][:100]}...")
                p = psutil.Process(proc['pid'])
                p.terminate()
                time.sleep(2)
                if p.is_running():
                    p.kill()
                cleaned += 1
                logger.info(f"Successfully cleaned PID {proc['pid']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                logger.warning(f"Could not clean PID {proc['pid']}: {e}")
                
        return cleaned
    
    def get_active_tec_services(self):
        """Get currently active TEC services"""
        services = {
            'api_server': None,
            'main_process': None,
            'flask_server': None
        }
        
        processes = self.find_tec_processes()
        
        for proc in processes:
            cmdline = proc['cmdline'].lower()
            if 'simple_api.py' in cmdline or 'flask' in cmdline:
                services['flask_server'] = proc
            elif 'main.py' in cmdline:
                services['main_process'] = proc
            elif 'api' in cmdline and 'server' in cmdline:
                services['api_server'] = proc
                
        return services
    
    def stop_all_tec_services(self):
        """Stop all TEC services safely"""
        logger.info("Stopping all TEC services...")
        processes = self.find_tec_processes()
        stopped = 0
        
        for proc in processes:
            try:
                logger.info(f"Stopping PID {proc['pid']}: {proc['cmdline'][:100]}...")
                p = psutil.Process(proc['pid'])
                p.terminate()
                time.sleep(1)
                if p.is_running():
                    p.kill()
                stopped += 1
                logger.info(f"Successfully stopped PID {proc['pid']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                logger.warning(f"Could not stop PID {proc['pid']}: {e}")
                
        return stopped
    
    def restart_tec_system(self):
        """Restart the TEC system cleanly"""
        logger.info("Restarting TEC system...")
        
        # Stop all services
        stopped = self.stop_all_tec_services()
        logger.info(f"Stopped {stopped} processes")
        
        # Wait a moment
        time.sleep(3)
        
        # Start fresh
        try:
            logger.info("Starting fresh TEC system...")
            result = subprocess.run([
                sys.executable, 'main.py', '--simple'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                logger.info("TEC system restarted successfully")
                return True
            else:
                logger.error(f"Failed to restart TEC system: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            logger.info("TEC system is starting in background...")
            return True
        except Exception as e:
            logger.error(f"Error restarting TEC system: {e}")
            return False
    
    def show_status(self):
        """Show current status"""
        print("\n" + "="*60)
        print("TEC TERMINAL MANAGER - SYSTEM STATUS")
        print("="*60)
        
        processes = self.find_tec_processes()
        services = self.get_active_tec_services()
        
        print(f"\nActive TEC Processes: {len(processes)}")
        for proc in processes:
            status = "🟢 Active"
            try:
                p = psutil.Process(proc['pid'])
                if p.status() == psutil.STATUS_ZOMBIE:
                    status = "🔴 Zombie"
                elif not p.is_running():
                    status = "🟡 Stopped"
            except psutil.NoSuchProcess:
                status = "❌ Dead"
                
            print(f"  PID {proc['pid']:5d} | {status} | Age: {proc['age_hours']:.1f}h | {proc['cmdline'][:80]}...")
        
        print(f"\nService Status:")
        for service, proc in services.items():
            if proc:
                print(f"  {service:15s}: 🟢 Running (PID {proc['pid']})")
            else:
                print(f"  {service:15s}: 🔴 Stopped")
        
        orphaned = self.find_orphaned_processes()
        if orphaned:
            print(f"\nOrphaned Processes: {len(orphaned)}")
            for proc in orphaned:
                print(f"  PID {proc['pid']} - Age: {proc['age_hours']:.1f}h")
        
        print("="*60)

def main():
    manager = TerminalManager()
    
    if len(sys.argv) < 2:
        print("TEC Terminal Manager")
        print("Usage:")
        print("  python terminal_manager.py status    - Show current status")
        print("  python terminal_manager.py clean     - Clean orphaned processes")
        print("  python terminal_manager.py stop      - Stop all TEC services")
        print("  python terminal_manager.py restart   - Restart TEC system")
        print("  python terminal_manager.py monitor   - Monitor and auto-clean")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'status':
        manager.show_status()
    
    elif command == 'clean':
        print("Cleaning orphaned processes...")
        cleaned = manager.clean_orphaned_processes()
        print(f"Cleaned {cleaned} orphaned processes")
        manager.show_status()
    
    elif command == 'stop':
        print("Stopping all TEC services...")
        stopped = manager.stop_all_tec_services()
        print(f"Stopped {stopped} processes")
    
    elif command == 'restart':
        success = manager.restart_tec_system()
        if success:
            print("TEC system restarted successfully")
        else:
            print("Failed to restart TEC system")
    
    elif command == 'monitor':
        print("Starting terminal monitor (Ctrl+C to stop)...")
        try:
            while True:
                orphaned = manager.find_orphaned_processes()
                if orphaned:
                    logger.info(f"Found {len(orphaned)} orphaned processes, cleaning...")
                    cleaned = manager.clean_orphaned_processes()
                    logger.info(f"Cleaned {cleaned} processes")
                
                time.sleep(30)  # Check every 30 seconds
        except KeyboardInterrupt:
            print("\nMonitoring stopped")
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
