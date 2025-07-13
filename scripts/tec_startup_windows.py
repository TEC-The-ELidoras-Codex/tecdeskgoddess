#!/usr/bin/env python3
"""
TEC: BITLYFE IS THE NEW SHIT - Clean Windows Startup
Windows-compatible startup script without Unicode issues
"""

import os
import sys
import subprocess
import time
import json
import logging
from pathlib import Path
from datetime import datetime

# Configure logging for Windows
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('tec_startup.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)

class TECStartupWindows:
    """Windows-compatible TEC system startup manager"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.processes = {}
        self.startup_time = datetime.now()
        
        # Load environment variables from .env
        self.load_environment()
    
    def load_environment(self):
        """Load environment variables from .env file"""
        env_file = self.base_dir / ".env"
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
    
    def check_environment(self):
        """Check if required environment variables are set"""
        logger.info("Checking environment variables...")
        
        required_vars = ['GITHUB_TOKEN']
        optional_vars = ['GEMINI_API_KEY', 'ANTHROPIC_API_KEY', 'OPENAI_API_KEY']
        
        missing_required = []
        for var in required_vars:
            value = os.getenv(var)
            if not value or value.startswith('your_'):
                missing_required.append(var)
            else:
                logger.info(f"  OK {var}: Set")
        
        for var in optional_vars:
            value = os.getenv(var)
            if value and not value.startswith('your_'):
                logger.info(f"  OK {var}: Set")
            else:
                logger.info(f"  Warning {var}: Not set (optional)")
        
        if missing_required:
            logger.error(f"Missing required environment variables: {missing_required}")
            logger.error("Please set GITHUB_TOKEN for minimum functionality")
            return False
        
        return True
    
    def check_dependencies(self):
        """Check if required Python packages are installed"""
        logger.info("Checking Python dependencies...")
        
        required_packages = [
            'flask', 'requests', 'openai', 'anthropic', 'google.generativeai'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
                logger.info(f"  OK {package}")
            except ImportError:
                missing_packages.append(package)
                logger.error(f"  Missing {package}")
        
        if missing_packages:
            logger.error(f"Missing packages: {missing_packages}")
            logger.error("Run: pip install -r requirements.txt")
            return False
        
        return True
    
    def check_files(self):
        """Check if required files exist"""
        logger.info("Checking required files...")
        
        required_files = [
            '.env',
            '.github/copilot/mcp.json',
            'tec_tools/mcp_base.py',
            'tec_tools/mcp_orchestrator.py'
        ]
        
        missing_files = []
        for file_path in required_files:
            if (self.base_dir / file_path).exists():
                logger.info(f"  OK {file_path}")
            else:
                missing_files.append(file_path)
                logger.error(f"  Missing {file_path}")
        
        if missing_files:
            logger.error(f"Missing files: {missing_files}")
            return False
        
        return True
    
    def start_mcp_server(self, server_name, module_path):
        """Start an individual MCP server"""
        logger.info(f"Starting {server_name}...")
        
        try:
            process = subprocess.Popen(
                [sys.executable, '-m', module_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(self.base_dir),
                env=os.environ.copy()
            )
            
            self.processes[server_name] = process
            logger.info(f"  Started {server_name} (PID: {process.pid})")
            return True
            
        except Exception as e:
            logger.error(f"  Failed to start {server_name}: {e}")
            return False
    
    def start_all_servers(self):
        """Start all MCP servers"""
        logger.info("Starting MCP servers...")
        
        servers = {
            'tec-orchestrator': 'tec_tools.mcp_orchestrator',
            'tec-journal': 'tec_tools.mcp_journal',
            'tec-finance': 'tec_tools.mcp_finance',
            'tec-questlog': 'tec_tools.mcp_questlog'
        }
        
        success_count = 0
        for server_name, module_path in servers.items():
            if self.start_mcp_server(server_name, module_path):
                success_count += 1
            time.sleep(1)  # Small delay between starts
        
        logger.info(f"Started {success_count}/{len(servers)} servers")
        return success_count > 0
    
    def check_server_health(self):
        """Check if servers are running"""
        logger.info("Checking server health...")
        
        running_count = 0
        for server_name, process in self.processes.items():
            if process.poll() is None:  # Still running
                logger.info(f"  OK {server_name} (PID: {process.pid})")
                running_count += 1
            else:
                logger.error(f"  Stopped {server_name}")
        
        return running_count
    
    def stop_all_servers(self):
        """Stop all running servers"""
        logger.info("Stopping all services...")
        
        for server_name, process in self.processes.items():
            try:
                if process.poll() is None:  # Still running
                    process.terminate()
                    process.wait(timeout=5)
                    logger.info(f"  Stopped {server_name}")
            except Exception as e:
                logger.error(f"  Error stopping {server_name}: {e}")
                try:
                    process.kill()
                except:
                    pass
        
        self.processes.clear()
        logger.info("All services stopped")
    
    def run_full_startup(self):
        """Run the complete startup sequence"""
        logger.info("TEC: BITLYFE IS THE NEW SHIT - Starting MCP Ecosystem")
        logger.info(f"Start time: {self.startup_time.isoformat()}")
        
        try:
            # Phase 1: Pre-flight checks
            logger.info("Phase 1: Pre-flight checks")
            if not self.check_environment():
                logger.error("Environment check failed. Exiting.")
                return False
            
            if not self.check_dependencies():
                logger.error("Dependencies check failed. Exiting.")
                return False
            
            if not self.check_files():
                logger.error("File check failed. Exiting.")
                return False
            
            # Phase 2: Start services
            logger.info("Phase 2: Starting services")
            if not self.start_all_servers():
                logger.error("Failed to start servers. Exiting.")
                return False
            
            # Phase 3: Health check
            logger.info("Phase 3: Health check")
            time.sleep(3)  # Let servers settle
            running_count = self.check_server_health()
            
            if running_count > 0:
                logger.info(f"SUCCESS: {running_count} servers running")
                logger.info("TEC MCP ecosystem is operational!")
                logger.info("Next steps:")
                logger.info("  1. Test with: python test_mcp_system.py")
                logger.info("  2. Create GitHub issue and assign to @copilot")
                logger.info("  3. Start coding with Copilot!")
                return True
            else:
                logger.error("No servers running. Startup failed.")
                return False
                
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            return False
        except Exception as e:
            logger.error(f"Startup failed: {e}")
            return False
        finally:
            # Don't auto-stop servers on success, let them run
            pass
    
    def run_quick_test(self):
        """Run a quick connectivity test"""
        logger.info("Quick connectivity test...")
        
        # Test basic imports
        try:
            sys.path.append(str(self.base_dir))
            from tec_tools import mcp_base
            from tec_tools import mcp_orchestrator
            logger.info("  OK MCP modules import correctly")
        except Exception as e:
            logger.error(f"  Failed MCP import test: {e}")
            return False
        
        # Test environment
        if not self.check_environment():
            return False
        
        logger.info("Quick test passed!")
        return True

def main():
    """Main startup function"""
    startup = TECStartupWindows()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Quick test mode
        success = startup.run_quick_test()
    else:
        # Full startup mode
        success = startup.run_full_startup()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
