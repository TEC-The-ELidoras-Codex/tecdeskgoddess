#!/usr/bin/env python3
"""
Simple TEC System Status Check
"""
import requests
import os

def check_system_status():
    print("=== TEC SYSTEM STATUS CHECK ===")
    
    # Check if key files exist
    files_to_check = [
        'main.py',
        'src/simple_api.py', 
        'tec_chat.html',
        'tec_complete_interface.html'
    ]
    
    print("\n[FILE CHECK]")
    all_files_exist = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✓ {file_path} ({size} bytes)")
        else:
            print(f"✗ {file_path} (missing)")
            all_files_exist = False
    
    # Check API health
    print("\n[API CHECK]")
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            print("✓ API Health: OK")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ API Health: HTTP {response.status_code}")
    except Exception as e:
        print(f"✗ API Health: {e}")
        return False
    
    # Check web interfaces
    print("\n[WEB INTERFACE CHECK]")
    interfaces = [
        ('/', 'Root'),
        ('/tec_chat.html', 'Chat Interface'),
        ('/tec_complete_interface.html', 'Complete Interface')
    ]
    
    for endpoint, name in interfaces:
        try:
            response = requests.get(f'http://localhost:8000{endpoint}', timeout=5)
            if response.status_code == 200:
                print(f"✓ {name}: OK")
            else:
                print(f"✗ {name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"✗ {name}: {e}")
    
    # Check chat functionality
    print("\n[CHAT API CHECK]")
    try:
        response = requests.post('http://localhost:8000/chat', 
                               json={'message': 'status'}, 
                               timeout=5)
        if response.status_code == 200:
            print("✓ Chat API: OK")
            result = response.json()
            print(f"  Response: {result.get('response', 'No response')[:60]}...")
        else:
            print(f"✗ Chat API: HTTP {response.status_code}")
    except Exception as e:
        print(f"✗ Chat API: {e}")
    
    print("\n=== STATUS CHECK COMPLETE ===")
    return True

if __name__ == '__main__':
    check_system_status()
