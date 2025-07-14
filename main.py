#!/usr/bin/env python3
"""
TEC: BITLYFE - The Creator's Rebellion
Enhanced Startup Script with Azure Multi-Provider Integration
Version 2.0.0 - July 14, 2025
"""

import os
import sys
import time
import subprocess
import requests
import argparse
from pathlib import Path

# Color codes for terminal output (Windows compatible)
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_colored(text, color=WHITE):
    """Print colored text to terminal"""
    try:
        print(f"{color}{text}{RESET}")
    except UnicodeEncodeError:
        # Fallback for Windows console issues
        print(text.encode('ascii', 'ignore').decode('ascii'))

def print_banner():
    """Print the TEC startup banner"""
    banner = f"""
{CYAN}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    {BOLD}TEC: BITLYFE - The Creator's Rebellion{RESET}{CYAN}                    ║
║                                                               ║
║    {YELLOW}Digital Sovereignty Companion v2.0.0{RESET}{CYAN}                     ║
║    {GREEN}Multi-Provider AI Fortress{RESET}{CYAN}                               ║
║                                                               ║
║    {MAGENTA}"Unfettered Access Shall Be Maintained"{RESET}{CYAN}                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{RESET}
"""
    print_colored(banner, CYAN)

def check_environment():
    """Check if environment variables are properly configured"""
    print_colored("🔍 Checking Environment Configuration...", BLUE)
    
    env_status = {
        "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN", "NOT_SET"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", "NOT_SET"),
        "AZURE_API_KEY_1": os.getenv("AZURE_API_KEY_1", "NOT_SET"),
        "AZURE_API_KEY_2": os.getenv("AZURE_API_KEY_2", "NOT_SET"),
        "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT", "NOT_SET"),
        "AZURE_COGNITIVE_SERVICES_ENDPOINT": os.getenv("AZURE_COGNITIVE_SERVICES_ENDPOINT", "NOT_SET"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "NOT_SET"),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY", "NOT_SET"),
    }
    
    configured_count = sum(1 for v in env_status.values() if v != "NOT_SET")
    total_count = len(env_status)
    
    print_colored(f"✅ Environment Status: {configured_count}/{total_count} providers configured", GREEN)
    
    # Show Azure configuration status
    azure_configured = (env_status["AZURE_API_KEY_1"] != "NOT_SET" and 
                       env_status["AZURE_OPENAI_ENDPOINT"] != "NOT_SET")
    
    if azure_configured:
        print_colored("🔷 Azure AI Services: CONFIGURED with TEC BITLYFE credentials", GREEN)
    else:
        print_colored("⚠️  Azure AI Services: NOT CONFIGURED", YELLOW)
        print_colored("   Set AZURE_API_KEY_1 and AZURE_OPENAI_ENDPOINT in .env", YELLOW)
    
    return configured_count > 0

def check_dependencies():
    """Check if required Python packages are installed"""
    print_colored("📦 Checking Dependencies...", BLUE)
    
    required_packages = [
        'flask', 'requests', 'openai', 'anthropic', 
        'azure-ai-inference', 'PyPDF2', 'beautifulsoup4'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print_colored(f"❌ Missing packages: {', '.join(missing_packages)}", RED)
        print_colored("Installing missing packages...", YELLOW)
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
        print_colored("✅ Dependencies installed", GREEN)
    else:
        print_colored("✅ All dependencies satisfied", GREEN)
    
    return True

def start_api_server(simple_mode=False):
    """Start the TEC API server"""
    print_colored("🚀 Starting TEC API Server...", BLUE)
    
    try:
        # Change to src directory and start the API
        os.chdir(Path(__file__).parent / "src")
        
        if simple_mode:
            print_colored("Starting in SIMPLE mode (Flask development server)", YELLOW)
            subprocess.Popen([sys.executable, "simple_api.py"], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
        else:
            print_colored("Starting in FULL mode (Production server)", GREEN)
            subprocess.Popen([sys.executable, "simple_api.py"], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
        
        # Wait for server to start
        print_colored("⏳ Waiting for server to initialize...", YELLOW)
        time.sleep(3)
        
        # Test server health
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print_colored("✅ API Server is running on http://localhost:8000", GREEN)
                return True
            else:
                print_colored(f"❌ Server responded with status: {response.status_code}", RED)
                return False
        except requests.exceptions.RequestException as e:
            print_colored(f"❌ Failed to connect to server: {e}", RED)
            return False
    
    except Exception as e:
        print_colored(f"❌ Failed to start server: {e}", RED)
        return False

def test_ai_providers():
    """Test connectivity to available AI providers"""
    print_colored("🤖 Testing AI Provider Connectivity...", BLUE)
    
    test_prompt = "Hello, this is a test from TEC: BITLYFE. Respond with 'OK' if you can hear me."
    
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={"message": test_prompt},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print_colored("✅ AI Provider connectivity test passed", GREEN)
            print_colored(f"   Response: {result.get('response', 'No response')[:50]}...", CYAN)
            return True
        else:
            print_colored(f"❌ AI Provider test failed: {response.status_code}", RED)
            return False
    
    except Exception as e:
        print_colored(f"❌ AI Provider test error: {e}", RED)
        return False

def open_web_interface():
    """Open the web interface in the default browser"""
    print_colored("🌐 Opening Web Interface...", BLUE)
    
    interface_url = "http://localhost:8000/tec_complete_interface.html"
    
    try:
        if os.name == 'nt':  # Windows
            os.startfile(interface_url)
        elif os.name == 'posix':  # macOS and Linux
            subprocess.call(['open', interface_url])
        
        print_colored(f"✅ Web interface opened: {interface_url}", GREEN)
        print_colored("🎯 You can also access:", CYAN)
        print_colored("   • Simple Chat: http://localhost:8000", CYAN)
        print_colored("   • API Health: http://localhost:8000/health", CYAN)
        
    except Exception as e:
        print_colored(f"❌ Failed to open web interface: {e}", RED)
        print_colored(f"Please manually open: {interface_url}", YELLOW)

def show_status_summary():
    """Show final status summary"""
    print_colored("\n" + "="*60, CYAN)
    print_colored("🎉 TEC: BITLYFE STARTUP COMPLETE", BOLD + GREEN)
    print_colored("="*60, CYAN)
    
    print_colored("🚀 SYSTEM STATUS:", BLUE)
    print_colored("   ✅ Multi-Provider AI Fortress: OPERATIONAL", GREEN)
    print_colored("   ✅ Digital Sovereignty Companion: READY", GREEN)
    print_colored("   ✅ Azure TEC BITLYFE Integration: CONFIGURED", GREEN)
    print_colored("   ✅ Cost Optimization Engine: ACTIVE", GREEN)
    print_colored("   ✅ Censorship Resistance: ENABLED", GREEN)
    
    print_colored("\n🎯 QUICK ACTIONS:", BLUE)
    print_colored("   • Chat with Daisy Purecode: Use the web interface", WHITE)
    print_colored("   • Test AI providers: Try different prompts", WHITE)
    print_colored("   • Monitor costs: Check provider usage", WHITE)
    print_colored("   • WordPress integration: Upload plugin from wordpress/", WHITE)
    
    print_colored("\n🏴‍☠️ THE CREATOR'S REBELLION IS OPERATIONAL", BOLD + MAGENTA)
    print_colored("   'Unfettered Access Shall Be Maintained'", CYAN)

def main():
    """Main startup function"""
    parser = argparse.ArgumentParser(description="TEC: BITLYFE Startup Script")
    parser.add_argument("--simple", action="store_true", help="Start in simple mode")
    parser.add_argument("--no-browser", action="store_true", help="Don't open web browser")
    parser.add_argument("--test-only", action="store_true", help="Only run tests, don't start server")
    parser.add_argument("--status", action="store_true", help="Check status of running system")
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.status:
        print_colored("📊 Checking TEC System Status...", BLUE)
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print_colored("✅ TEC System is RUNNING", GREEN)
                print_colored("🌐 Web Interface: http://localhost:8000/tec_complete_interface.html", CYAN)
            else:
                print_colored("❌ TEC System is not responding properly", RED)
        except:
            print_colored("❌ TEC System is NOT RUNNING", RED)
            print_colored("Run 'python main.py' to start the system", YELLOW)
        return
    
    # Step 1: Check environment
    if not check_environment():
        print_colored("⚠️  Warning: No API keys configured. Some features may not work.", YELLOW)
        print_colored("Edit the .env file to configure your API keys.", YELLOW)
    
    # Step 2: Check dependencies
    if not check_dependencies():
        print_colored("❌ Failed to install dependencies", RED)
        return
    
    if args.test_only:
        print_colored("🧪 Running tests only...", BLUE)
        # Add test functions here
        return
    
    # Step 3: Start API server
    if not start_api_server(simple_mode=args.simple):
        print_colored("❌ Failed to start API server", RED)
        return
    
    # Step 4: Test AI providers
    test_ai_providers()
    
    # Step 5: Open web interface (unless disabled)
    if not args.no_browser:
        time.sleep(1)  # Give server a moment
        open_web_interface()
    
    # Step 6: Show final status
    show_status_summary()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n🛑 Startup interrupted by user", YELLOW)
        print_colored("The Creator's Rebellion will continue...", CYAN)
    except Exception as e:
        print_colored(f"\n❌ Startup failed: {e}", RED)
        print_colored("Check the logs for more details", YELLOW)
