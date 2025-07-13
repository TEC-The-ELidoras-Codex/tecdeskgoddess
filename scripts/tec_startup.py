#!/usr/bin/env python3
"""
TEC: BITLYFE IS THE NEW SHIT - MCP Startup Script
The Creator's Rebellion - Boot Sequence for Daisy Purecode: Silicate Mother

This script initializes the complete MCP ecosystem:
1. MCP Orchestrator (port 5000)
2. Journal MCP Server (port 5001) 
3. Finance MCP Server (port 5002)
4. Quest Log MCP Server (port 5003)
5. Enhanced Agentic Processor (port 8000)
"""

import os
import sys
import subprocess
import threading
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tec_startup.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class TECStartup:
    """
    Startup manager for the complete TEC MCP ecosystem
    """
    
    def __init__(self):
        self.processes = {}
        self.required_env_vars = [
            'GITHUB_TOKEN',  # For GitHub AI models
            # Optional but recommended
            'GEMINI_API_KEY',
            'ANTHROPIC_API_KEY',
            'AZURE_OPENAI_ENDPOINT',
            'AZURE_OPENAI_API_KEY',
            'OPENAI_API_KEY',
            'COINGECKO_API_KEY',
            'ELEVENLABS_API_KEY'
        ]
        
    def check_environment(self):
        """Check required environment variables"""
        logger.info("🔍 Checking environment variables...")
        
        missing_required = []
        missing_optional = []
        
        for var in self.required_env_vars:
            if not os.environ.get(var):
                if var == 'GITHUB_TOKEN':
                    missing_required.append(var)
                else:
                    missing_optional.append(var)
        
        if missing_required:
            logger.error(f"❌ Missing required environment variables: {missing_required}")
            logger.error("Please set GITHUB_TOKEN for minimum functionality")
            return False
        
        if missing_optional:
            logger.warning(f"⚠️ Missing optional environment variables: {missing_optional}")
            logger.warning("Some AI providers may not be available")
        
        logger.info("✅ Environment check passed")
        return True
    
    def install_dependencies(self):
        """Install required Python packages"""
        logger.info("📦 Installing dependencies...")
        
        try:
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
            ], check=True, capture_output=True)
            logger.info("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install dependencies: {e}")
            return False
    
    def start_mcp_orchestrator(self):
        """Start the MCP orchestrator"""
        logger.info("🚀 Starting MCP Orchestrator...")
        
        try:
            # Start orchestrator in separate process
            process = subprocess.Popen([
                sys.executable, '-m', 'tec_tools.mcp_orchestrator'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.processes['orchestrator'] = process
            logger.info("✅ MCP Orchestrator started on port 5000")
            
            # Wait for orchestrator to start
            time.sleep(3)
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start MCP Orchestrator: {e}")
            return False
    
    def start_agentic_processor(self):
        """Start the enhanced agentic processor"""
        logger.info("🧠 Starting Enhanced Agentic Processor...")
        
        try:
            # Start agentic processor in separate process
            process = subprocess.Popen([
                sys.executable, '-c', 
                """
import sys
sys.path.append('.')
from tec_tools.agentic_processor import app
app.run(host='0.0.0.0', port=8000, debug=False)
                """
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.processes['agentic_processor'] = process
            logger.info("✅ Enhanced Agentic Processor started on port 8000")
            
            # Wait for processor to start
            time.sleep(2)
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start Agentic Processor: {e}")
            return False
    
    def check_services(self):
        """Check if all services are running"""
        logger.info("🔍 Checking service health...")
        
        import requests
        
        services = {
            'MCP Orchestrator': 'http://localhost:5000/health',
            'Journal MCP Server': 'http://localhost:5001/health',
            'Finance MCP Server': 'http://localhost:5002/health',
            'Quest Log MCP Server': 'http://localhost:5003/health',
            'Agentic Processor': 'http://localhost:8000/api/agentic/providers'
        }
        
        all_healthy = True
        for service, url in services.items():
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    logger.info(f"✅ {service} is healthy")
                else:
                    logger.warning(f"⚠️ {service} returned status {response.status_code}")
                    all_healthy = False
            except requests.exceptions.RequestException as e:
                logger.error(f"❌ {service} is not responding: {e}")
                all_healthy = False
        
        return all_healthy
    
    def print_startup_banner(self):
        """Print the TEC startup banner"""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  TEC: BITLYFE IS THE NEW SHIT - The Creator's Rebellion                     ║
║  Daisy Purecode: Silicate Mother - Boot Sequence Complete                   ║
║                                                                              ║
║  🏰 Digital Cathedral Status: ONLINE                                        ║
║  🤖 Machine Goddess Status: ACTIVE                                          ║
║  🌐 MCP Ecosystem Status: OPERATIONAL                                       ║
║                                                                              ║
║  "Unfettered Access Shall Be Maintained"                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

🚀 Services Running:
   • MCP Orchestrator: http://localhost:5000
   • Journal MCP Server: http://localhost:5001
   • Finance MCP Server: http://localhost:5002
   • Quest Log MCP Server: http://localhost:5003
   • Enhanced Agentic Processor: http://localhost:8000

🔧 Available Endpoints:
   • Health Check: GET /health
   • MCP Unified Query: POST /mcp/unified/query
   • Daisy Context: POST /mcp/daisy/context
   • AI Processing: POST /api/agentic/daisy/process
   • Provider Status: GET /api/agentic/providers

📖 Documentation:
   • MCP Spec: https://modelcontextprotocol.io/
   • TEC Repository: https://github.com/TEC-The-ELidoras-Codex/

🎯 Next Steps:
   1. Configure your frontend to connect to http://localhost:8000
   2. Test the MCP endpoints with your preferred AI provider
   3. Begin the Creator's Rebellion!

Press Ctrl+C to stop all services.
"""
        print(banner)
    
    def start_all(self):
        """Start the complete TEC MCP ecosystem"""
        logger.info("🌟 Starting TEC: BITLYFE IS THE NEW SHIT - MCP Ecosystem")
        logger.info(f"⏰ Start time: {datetime.now().isoformat()}")
        
        # Step 1: Check environment
        if not self.check_environment():
            logger.error("❌ Environment check failed. Exiting.")
            return False
        
        # Step 2: Install dependencies
        if not self.install_dependencies():
            logger.error("❌ Dependency installation failed. Exiting.")
            return False
        
        # Step 3: Start MCP orchestrator (this starts all MCP servers)
        if not self.start_mcp_orchestrator():
            logger.error("❌ MCP Orchestrator startup failed. Exiting.")
            return False
        
        # Step 4: Start enhanced agentic processor
        if not self.start_agentic_processor():
            logger.error("❌ Agentic Processor startup failed. Exiting.")
            return False
        
        # Step 5: Wait for services to fully initialize
        logger.info("⏳ Waiting for services to initialize...")
        time.sleep(5)
        
        # Step 6: Check service health
        if not self.check_services():
            logger.warning("⚠️ Some services may not be fully healthy")
        
        # Step 7: Print success banner
        self.print_startup_banner()
        
        logger.info("🎉 TEC MCP Ecosystem started successfully!")
        logger.info("🤖 Daisy Purecode: Silicate Mother is now online")
        logger.info("🚀 The Creator's Rebellion begins now!")
        
        return True
    
    def stop_all(self):
        """Stop all services"""
        logger.info("🛑 Stopping all TEC services...")
        
        for name, process in self.processes.items():
            try:
                process.terminate()
                process.wait(timeout=5)
                logger.info(f"✅ Stopped {name}")
            except subprocess.TimeoutExpired:
                process.kill()
                logger.warning(f"⚠️ Force killed {name}")
            except Exception as e:
                logger.error(f"❌ Error stopping {name}: {e}")
        
        logger.info("🛑 All services stopped")
    
    def run(self):
        """Main run method"""
        try:
            if self.start_all():
                # Keep running until interrupted
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Received interrupt signal")
        finally:
            self.stop_all()


def main():
    """Main entry point"""
    startup = TECStartup()
    startup.run()


if __name__ == "__main__":
    main()
