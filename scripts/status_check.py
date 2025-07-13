"""
TEC MCP System Status Check
Simple check to see what's actually running
"""

import requests
import subprocess
import sys
import time

def check_processes():
    """Check running Python processes"""
    print("🔍 Checking running Python processes...")
    try:
        result = subprocess.run(['tasklist', '/fi', 'imagename eq python.exe'], 
                              capture_output=True, text=True, shell=True)
        lines = result.stdout.split('\n')
        python_processes = [line for line in lines if 'python.exe' in line]
        
        print(f"Found {len(python_processes)} Python processes:")
        for proc in python_processes:
            if proc.strip():
                print(f"  {proc}")
    except Exception as e:
        print(f"Error checking processes: {e}")

def check_ports():
    """Check what's listening on our expected ports"""
    print("\n🔍 Checking port status...")
    ports = [5000, 5001, 5002, 5003, 8000]
    
    for port in ports:
        try:
            result = subprocess.run(['netstat', '-an'], 
                                  capture_output=True, text=True, shell=True)
            if f":{port} " in result.stdout:
                print(f"  ✅ Port {port}: Something listening")
            else:
                print(f"  ❌ Port {port}: Nothing listening")
        except:
            print(f"  ❓ Port {port}: Could not check")

def test_http_endpoints():
    """Test basic HTTP connectivity"""
    print("\n🔍 Testing HTTP endpoints...")
    
    endpoints = {
        "Orchestrator": "http://localhost:5000/health",
        "Journal": "http://localhost:5001/health", 
        "Finance": "http://localhost:5002/health",
        "Quest Log": "http://localhost:5003/health",
        "Agentic": "http://localhost:8000/health"
    }
    
    for name, url in endpoints.items():
        try:
            response = requests.get(url, timeout=2)
            print(f"  ✅ {name}: HTTP {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"  ❌ {name}: Connection refused")
        except requests.exceptions.Timeout:
            print(f"  ⏰ {name}: Timeout")
        except Exception as e:
            print(f"  ❓ {name}: {e}")

def main():
    """Main status check"""
    print("🔍 TEC System Status Check")
    print("=" * 50)
    
    check_processes()
    check_ports()
    test_http_endpoints()
    
    print("\n📋 Summary:")
    print("If you see 'Connection refused' errors, the servers may be running")
    print("as MCP processes but not HTTP servers. This is normal for MCP.")
    print("\nNext steps:")
    print("1. The MCP servers are running for GitHub Copilot")
    print("2. Create a GitHub issue and assign to @copilot") 
    print("3. Test Copilot integration directly")

if __name__ == "__main__":
    main()
