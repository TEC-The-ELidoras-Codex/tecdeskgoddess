#!/usr/bin/env python3
"""
TEC Quick Start - Get TEC Life & Finance running NOW!
The Creator's Rebellion - Digital Sovereignty in Action
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
END = '\033[0m'

def print_banner():
    print(f"""{BLUE}{BOLD}
╔══════════════════════════════════════════════════════════════╗
║               TEC: BITLYFE IS THE NEW SHIT                   ║
║                  Quick Start Launcher                        ║
║                "The Creator's Rebellion"                     ║
╚══════════════════════════════════════════════════════════════╝
{END}""")

def check_environment():
    """Check if environment is properly configured"""
    print(f"{YELLOW}🔍 Checking environment...{END}")
    
    # Check for .env file
    if not os.path.exists('.env'):
        print(f"{RED}❌ .env file not found{END}")
        return False
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check critical environment variables
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token or github_token == 'your_github_token_here':
        print(f"{RED}❌ GITHUB_TOKEN not set in .env file{END}")
        print(f"{YELLOW}   Please set your GitHub token in .env file{END}")
        return False
    
    print(f"{GREEN}✅ Environment configured{END}")
    return True

def install_dependencies():
    """Install required Python packages"""
    print(f"{YELLOW}📦 Installing dependencies...{END}")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print(f"{GREEN}✅ Dependencies installed{END}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{RED}❌ Failed to install dependencies: {e}{END}")
        return False

def start_tec_backend():
    """Start TEC backend services"""
    print(f"{YELLOW}🚀 Starting TEC backend...{END}")
    
    try:
        # Start the main API server
        backend_process = subprocess.Popen([
            sys.executable, "-m", "tec_tools.api"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Give it a moment to start
        time.sleep(3)
        
        # Check if it's running
        try:
            response = requests.get("http://localhost:5000/health", timeout=5)
            if response.status_code == 200:
                print(f"{GREEN}✅ TEC Backend running on http://localhost:5000{END}")
                return backend_process
        except:
            pass
        
        # If health check failed, try alternative port
        try:
            response = requests.get("http://localhost:8000/api/agentic/providers", timeout=5)
            if response.status_code == 200:
                print(f"{GREEN}✅ TEC Backend running on http://localhost:8000{END}")
                return backend_process
        except:
            pass
            
        print(f"{RED}❌ Backend failed to start properly{END}")
        return None
        
    except Exception as e:
        print(f"{RED}❌ Failed to start backend: {e}{END}")
        return None

def test_ai_services():
    """Test AI service connections"""
    print(f"{YELLOW}🤖 Testing AI services...{END}")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    # Test GitHub AI
    github_token = os.getenv('GITHUB_TOKEN')
    if github_token:
        try:
            from openai import OpenAI
            client = OpenAI(
                base_url="https://models.github.ai/inference",
                api_key=github_token
            )
            
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": "Hello TEC!"}],
                model="gpt-4o-mini",
                max_tokens=50
            )
            
            print(f"{GREEN}✅ GitHub AI connected{END}")
        except Exception as e:
            print(f"{YELLOW}⚠️ GitHub AI: {e}{END}")
    
    # Test Azure AI
    azure_key = os.getenv('AZURE_AI_KEY_1')
    if azure_key:
        print(f"{GREEN}✅ Azure AI configured{END}")
    else:
        print(f"{YELLOW}⚠️ Azure AI not configured{END}")
    
    # Test Crypto APIs
    crypto_key = os.getenv('CRYPTOCOMPARE_API_KEY')
    if crypto_key:
        print(f"{GREEN}✅ Crypto API configured{END}")
    else:
        print(f"{YELLOW}⚠️ Crypto API not configured{END}")

def test_crypto_manager():
    """Test the crypto manager"""
    print(f"{YELLOW}💰 Testing crypto manager...{END}")
    
    try:
        from tec_tools.crypto_manager import TECCryptoManager
        crypto_manager = TECCryptoManager()
        
        # Test Bitcoin price
        btc_price = crypto_manager.get_price("bitcoin")
        if btc_price:
            print(f"{GREEN}✅ Bitcoin: ${btc_price['price']:,.2f} (via {btc_price['provider']}){END}")
        else:
            print(f"{YELLOW}⚠️ Crypto data unavailable{END}")
            
    except Exception as e:
        print(f"{YELLOW}⚠️ Crypto manager: {e}{END}")

def create_basic_assets():
    """Create basic assets if they don't exist"""
    print(f"{YELLOW}📁 Setting up basic assets...{END}")
    
    # Create basic directories
    os.makedirs("assets/audio", exist_ok=True)
    os.makedirs("assets/face", exist_ok=True)
    os.makedirs("blueprints/components", exist_ok=True)
    os.makedirs("data/journals", exist_ok=True)
    os.makedirs("data/finances", exist_ok=True)
    
    # Create a basic React component template
    react_template = """import React, { useState, useEffect } from 'react';

const TECDashboard = () => {
    const [status, setStatus] = useState('Initializing...');
    const [aiResponse, setAiResponse] = useState('');
    const [cryptoData, setCryptoData] = useState(null);

    useEffect(() => {
        checkBackendStatus();
        fetchCryptoData();
    }, []);

    const checkBackendStatus = async () => {
        try {
            const response = await fetch('http://localhost:5000/health');
            if (response.ok) {
                setStatus('TEC Backend Online ✅');
            }
        } catch (error) {
            setStatus('Backend Offline ❌');
        }
    };

    const testAI = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/agentic/test-github', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: 'Hello from TEC frontend!' })
            });
            const data = await response.json();
            setAiResponse(data.response || 'AI connection failed');
        } catch (error) {
            setAiResponse('Error connecting to AI');
        }
    };

    const fetchCryptoData = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/crypto/bitcoin');
            const data = await response.json();
            setCryptoData(data);
        } catch (error) {
            console.log('Crypto data unavailable');
        }
    };

    return (
        <div className="min-h-screen bg-gray-900 text-white p-8">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-4xl font-bold mb-8 text-center">
                    🛡️ TEC: BITLYFE IS THE NEW SHIT ⚔️
                </h1>
                
                <div className="grid md:grid-cols-2 gap-6">
                    <div className="bg-gray-800 p-6 rounded-lg">
                        <h2 className="text-xl font-semibold mb-4">System Status</h2>
                        <p className="mb-4">{status}</p>
                        <button 
                            onClick={testAI}
                            className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded"
                        >
                            Test AI Connection
                        </button>
                        {aiResponse && (
                            <div className="mt-4 p-3 bg-gray-700 rounded">
                                <p className="text-sm">{aiResponse}</p>
                            </div>
                        )}
                    </div>

                    <div className="bg-gray-800 p-6 rounded-lg">
                        <h2 className="text-xl font-semibold mb-4">Crypto Tracker</h2>
                        {cryptoData ? (
                            <div>
                                <p>Bitcoin: ${cryptoData.price?.toLocaleString()}</p>
                                <p className="text-sm text-gray-400">Via {cryptoData.provider}</p>
                            </div>
                        ) : (
                            <p className="text-gray-400">Loading crypto data...</p>
                        )}
                    </div>
                </div>

                <div className="mt-8 text-center">
                    <p className="text-gray-400">"The Creator's Rebellion" - Digital Sovereignty Achieved</p>
                </div>
            </div>
        </div>
    );
};

export default TECDashboard;
"""
    
    with open("blueprints/components/TECDashboard.jsx", "w") as f:
        f.write(react_template)
    
    print(f"{GREEN}✅ Basic assets created{END}")

def main():
    print_banner()
    
    # Step 1: Check environment
    if not check_environment():
        print(f"\n{RED}Please configure your .env file first!{END}")
        print(f"{YELLOW}Set GITHUB_TOKEN=your_actual_github_token{END}")
        return
    
    # Step 2: Install dependencies
    if not install_dependencies():
        return
    
    # Step 3: Create basic assets
    create_basic_assets()
    
    # Step 4: Test services
    test_ai_services()
    test_crypto_manager()
    
    # Step 5: Start backend
    backend_process = start_tec_backend()
    
    if backend_process:
        print(f"\n{GREEN}{BOLD}🎯 TEC LIFE & FINANCE IS RUNNING!{END}")
        print(f"{BLUE}Backend: http://localhost:5000 or http://localhost:8000{END}")
        print(f"{BLUE}Frontend: Ready for React development in blueprints/{END}")
        print(f"\n{YELLOW}Next steps:{END}")
        print(f"1. Test AI: http://localhost:5000/api/agentic/test-github")
        print(f"2. Check crypto: Open crypto_manager.py and run it")
        print(f"3. Build React frontend using TECDashboard.jsx template")
        print(f"\n{BOLD}Press Ctrl+C to stop{END}")
        
        try:
            # Keep the backend running
            backend_process.wait()
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Shutting down TEC backend...{END}")
            backend_process.terminate()
            print(f"{GREEN}TEC stopped successfully{END}")
    else:
        print(f"\n{RED}Failed to start TEC backend{END}")
        print(f"{YELLOW}Check your configuration and try again{END}")

if __name__ == "__main__":
    main()
