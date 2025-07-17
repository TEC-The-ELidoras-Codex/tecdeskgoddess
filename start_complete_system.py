"""
TEC Enhanced Persona System - Complete Startup
Launches API server and opens both interfaces
"""

import subprocess
import time
import webbrowser
import os
import sys
from pathlib import Path

def start_api_server():
    """Start the API server in the background"""
    print("🚀 Starting TEC Enhanced Persona API Server...")
    
    # Use PowerShell to start the server in a new window
    server_command = [
        "powershell", "-Command", 
        f"Start-Process python -ArgumentList 'tec_persona_api.py' -WindowStyle Normal"
    ]
    
    try:
        subprocess.Popen(server_command, shell=True)
        print("✅ API Server starting in new window...")
        return True
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def wait_for_server(max_attempts=10):
    """Wait for server to be ready"""
    import requests
    
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                print("✅ API Server is ready!")
                return True
        except:
            pass
        
        print(f"⏳ Waiting for server... ({attempt + 1}/{max_attempts})")
        time.sleep(2)
    
    return False

def open_interfaces():
    """Open both interfaces in browser"""
    interfaces = [
        ("Enhanced Interface", "http://localhost:8000/tec_enhanced_interface.html"),
        ("Complete Interface", "http://localhost:8000/tec_complete_interface.html")
    ]
    
    for name, url in interfaces:
        print(f"🌐 Opening {name}: {url}")
        webbrowser.open(url)
        time.sleep(1)

def main():
    print("=" * 60)
    print("🎉 TEC Enhanced Persona System - Complete Startup")
    print("=" * 60)
    
    # Check if files exist
    required_files = [
        "tec_persona_api.py",
        "tec_enhanced_interface.html",
        "tec_complete_interface.html"
    ]
    
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    # Start API server
    if not start_api_server():
        print("❌ Failed to start API server")
        return False
    
    # Wait for server to be ready
    print("\n⏳ Waiting for API server to initialize...")
    if not wait_for_server():
        print("❌ API server didn't start in time")
        print("💡 Try running manually: python tec_persona_api.py")
        return False
    
    # Open interfaces
    print("\n🌐 Opening interfaces in browser...")
    open_interfaces()
    
    print("\n" + "=" * 60)
    print("🎉 TEC Enhanced Persona System is now running!")
    print("=" * 60)
    print("📍 API Server: http://localhost:8000")
    print("🎮 Enhanced Interface: http://localhost:8000/tec_enhanced_interface.html")
    print("🌐 Complete Interface: http://localhost:8000/tec_complete_interface.html")
    print("📋 Health Check: http://localhost:8000/health")
    print("=" * 60)
    print("💡 To stop: Close the API server window or press Ctrl+C")
    print("🔄 To restart: Run this script again")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        input("\nPress Enter to exit...")
