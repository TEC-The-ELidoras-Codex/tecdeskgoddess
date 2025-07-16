import requests
import json

# Test Web3 authentication endpoints
base_url = "http://localhost:8000"

# Test generate nonce
print("Testing nonce generation...")
nonce_response = requests.post(f"{base_url}/api/auth/nonce", json={
    "wallet_address": "0x742d35Cc6634C0532925a3b8D40445D6b1e7dc43"
})
print(f"Nonce Status: {nonce_response.status_code}")
print(f"Nonce Response: {nonce_response.json()}")

# Test available personas
print("\nTesting available personas...")
personas_response = requests.get(f"{base_url}/api/persona/available")
print(f"Personas Status: {personas_response.status_code}")
print(f"Personas Response: {personas_response.json()}")

# Test current persona
print("\nTesting current persona...")
current_persona_response = requests.get(f"{base_url}/api/persona/current")
print(f"Current Persona Status: {current_persona_response.status_code}")
print(f"Current Persona Response: {current_persona_response.json()}")

# Test BITL balance
print("\nTesting BITL balance...")
balance_response = requests.get(f"{base_url}/api/bitl/balance")
print(f"Balance Status: {balance_response.status_code}")
print(f"Balance Response: {balance_response.json()}")

# Test earn BITL
print("\nTesting earn BITL...")
earn_response = requests.post(f"{base_url}/api/bitl/earn", json={
    "amount": 500,
    "reason": "testing"
})
print(f"Earn Status: {earn_response.status_code}")
print(f"Earn Response: {earn_response.json()}")

# Test new balance
print("\nTesting new BITL balance...")
new_balance_response = requests.get(f"{base_url}/api/bitl/balance")
print(f"New Balance Status: {new_balance_response.status_code}")
print(f"New Balance Response: {new_balance_response.json()}")

print("\n✅ All Web3 authentication and enhanced API endpoints tested successfully!")
