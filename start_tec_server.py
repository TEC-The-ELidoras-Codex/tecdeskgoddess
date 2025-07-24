#!/usr/bin/env python3
"""
Quick TEC Server Startup Script
"""

import subprocess
import sys
import os

def start_tec_server():
    """Start the TEC persona API server"""
    try:
        print("🚀 Starting TEC Enhanced Persona API Server...")
        
        # Change to the correct directory
        os.chdir(r"c:\Users\Ghedd\TEC_CODE\tecdeskgoddess")
        
        # Start the server
        subprocess.run([sys.executable, "tec_persona_api.py"], check=True)
        
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_tec_server()
