import requests
import json

# Test chat endpoint
url = "http://localhost:8000/chat"
data = {"message": "Hello! How is the Web3 authentication working?"}

response = requests.post(url, json=data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
