#!/usr/bin/env python3
"""
TEC: BITLYFE - Main Entry Point
The Creator's Rebellion - Digital Sovereignty Companion

Usage:
    python main.py              # Start simple web interface
    python main.py --full       # Start full MCP ecosystem
    python main.py --setup      # Run initial setup
    python main.py --status     # Check system status
"""
import sys
import argparse
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    parser = argparse.ArgumentParser(description="TEC: BITLYFE - Digital Sovereignty Companion")
    parser.add_argument('--full', action='store_true', help='Start full MCP ecosystem')
    parser.add_argument('--setup', action='store_true', help='Run initial setup')
    parser.add_argument('--status', action='store_true', help='Check system status')
    parser.add_argument('--simple', action='store_true', help='Start simple web interface (default)')
    
    args = parser.parse_args()
    
    if args.setup:
        import subprocess
        subprocess.run([sys.executable, "scripts/setup_tec.py"])
    elif args.status:
        import subprocess
        subprocess.run([sys.executable, "scripts/status_check.py"])
    elif args.full:
        import subprocess
        subprocess.run([sys.executable, "scripts/tec_startup.py"])
    else:
        # Default: simple startup
        import subprocess
        subprocess.run([sys.executable, "scripts/tec_simple_startup.py"])

if __name__ == "__main__":
    main()
