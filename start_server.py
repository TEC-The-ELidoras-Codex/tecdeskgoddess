#!/usr/bin/env python3
"""
TEC API Server Startup Script
"""
import os
import sys
import subprocess

def main():
    """Start the TEC API server"""
    try:
        # Change to the src directory
        os.chdir('src')
        
        # Start the API server
        print("🚀 Starting TEC Enhanced API Server...")
        subprocess.run([sys.executable, 'tec_api_simplified.py'])
        
    except KeyboardInterrupt:
        print("🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
