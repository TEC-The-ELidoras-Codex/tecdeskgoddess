#!/usr/bin/env python3
"""
TEC Simple Startup - Web Interface Ready
A simplified startup script that focuses on getting the web interface working
"""
import os
import sys
import time
import json
import logging
import subprocess
from pathlib import Path
from datetime import datetime

# Set up basic logging without emojis for Windows compatibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tec_startup.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class TECSimpleStartup:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.processes = {}
        self.required_ports = [5000, 5001, 5002, 5003, 8000]
        
    def check_environment(self):
        """Check if basic environment is set up"""
        logger.info("Checking environment...")
        
        # Load .env file if it exists
        env_file = self.base_dir / '.env'
        if env_file.exists():
            logger.info("Loading .env file...")
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        if value and value != 'your_github_token_here':
                            os.environ[key] = value
        
        # Check if we have at least one API key
        api_keys = [
            'GITHUB_TOKEN', 'GEMINI_API_KEY', 'OPENAI_API_KEY', 
            'ANTHROPIC_API_KEY', 'XAI_API_KEY'
        ]
        
        has_api_key = False
        for key in api_keys:
            if os.getenv(key) and os.getenv(key) != f'your_{key.lower()}_here':
                logger.info(f"Found {key}")
                has_api_key = True
        
        if not has_api_key:
            logger.warning("No AI API keys found. Some features may not work.")
        
        return True
    
    def start_api_server(self):
        """Start the web API server"""
        try:
            logger.info("Starting TEC API server on port 8000...")
            
            # Create a simple API server if it doesn't exist
            api_file = self.base_dir / "simple_api.py"
            if not api_file.exists():
                self.create_simple_api()
            
            # Start the API server
            cmd = [sys.executable, "simple_api.py"]
            process = subprocess.Popen(
                cmd,
                cwd=self.base_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes['api'] = process
            logger.info(f"API server started with PID: {process.pid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start API server: {e}")
            return False
    
    def create_simple_api(self):
        """Create a simple API server for the web interface"""
        api_content = '''#!/usr/bin/env python3
"""
Simple TEC API Server
Provides basic API endpoints for the web interface
"""
import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'service': 'TEC API',
        'version': '1.0.0'
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Basic chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        # Simple response logic
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Generate a basic response
        response = generate_response(message)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

def generate_response(message):
    """Generate a basic response to user messages"""
    message_lower = message.lower()
    
    if 'status' in message_lower:
        return "TEC System Status: Web interface is running. MCP servers are in development mode. Basic functionality available."
    
    elif 'journal' in message_lower:
        return "Journal feature: Ready to help you with personal reflection and note-taking. Future updates will include AI-powered analysis."
    
    elif 'finance' in message_lower or 'crypto' in message_lower:
        return "Finance tracking: Currently in development. Will support cryptocurrency monitoring and financial insights."
    
    elif 'quest' in message_lower:
        return "Quest system: RPG-style goal tracking and gamification features coming soon. Your adventure awaits!"
    
    elif 'hello' in message_lower or 'hi' in message_lower:
        return "Greetings! I am Daisy Purecode, your digital sovereignty companion. How can I assist you in The Creator's Rebellion today?"
    
    else:
        return f"I understand you said: '{message}'. The TEC system is currently in development mode. Full AI capabilities will be available once all MCP servers are properly configured."

@app.route('/')
def serve_chat():
    """Serve the chat interface"""
    return send_from_directory('.', 'tec_chat.html')

if __name__ == '__main__':
    logger.info("Starting TEC Simple API Server...")
    logger.info("Web interface available at: http://localhost:8000")
    logger.info("Health check at: http://localhost:8000/health")
    
    app.run(
        host='localhost',
        port=8000,
        debug=False,
        threaded=True
    )
'''
        
        api_file = self.base_dir / "simple_api.py"
        with open(api_file, 'w') as f:
            f.write(api_content)
        
        logger.info("Created simple API server")
    
    def check_status(self):
        """Check status of running services"""
        logger.info("Checking service status...")
        
        for name, process in self.processes.items():
            if process.poll() is None:
                logger.info(f"{name}: Running (PID: {process.pid})")
            else:
                logger.error(f"{name}: Stopped")
        
        return len([p for p in self.processes.values() if p.poll() is None])
    
    def stop_all(self):
        """Stop all running services"""
        logger.info("Stopping all services...")
        
        for name, process in self.processes.items():
            if process.poll() is None:
                logger.info(f"Stopping {name}...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
        
        self.processes.clear()
    
    def run(self):
        """Main startup sequence"""
        logger.info("=" * 60)
        logger.info("TEC: BITLYFE - Simple Web Interface Startup")
        logger.info("The Creator's Rebellion - Daisy Purecode Ready")
        logger.info("=" * 60)
        
        try:
            # Check environment
            if not self.check_environment():
                logger.error("Environment check failed")
                return False
            
            # Start API server
            if not self.start_api_server():
                logger.error("Failed to start API server")
                return False
            
            # Give it a moment to start
            time.sleep(2)
            
            # Check status
            running_services = self.check_status()
            
            if running_services > 0:
                logger.info("=" * 60)
                logger.info("SUCCESS: TEC Web Interface is running!")
                logger.info("Open your browser to: http://localhost:8000")
                logger.info("Chat interface: http://localhost:8000/tec_chat.html")
                logger.info("Health check: http://localhost:8000/health")
                logger.info("=" * 60)
                
                # Keep running
                try:
                    while True:
                        time.sleep(10)
                        # Check if processes are still running
                        if self.check_status() == 0:
                            logger.error("All services stopped unexpectedly")
                            break
                            
                except KeyboardInterrupt:
                    logger.info("Shutdown requested by user")
                
            else:
                logger.error("No services started successfully")
                
        except Exception as e:
            logger.error(f"Startup failed: {e}")
        
        finally:
            self.stop_all()

def main():
    startup = TECSimpleStartup()
    startup.run()

if __name__ == "__main__":
    main()
